import asyncio
import base64
import os
import shutil
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import (
    DEFAULT_TIMEOUT_SECONDS,
    MAX_OUTPUT_BYTES,
    USER_WORKSPACE_DIR,
)
from app.core.file_manager import get_safe_path
from app.core.venv_manager import ensure_sandbox_venv, get_current_python_exe

# Wrapper code that hooks matplotlib to capture plots non-interactively
PLOT_HOOK_CODE = '''
# Auto-injected plot interceptor
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import os
    
    _orig_show = plt.show
    _plot_counter = [0]
    _plot_dir = os.environ.get('_PYDEEP_PLOT_DIR', '')

    def _custom_show(*args, **kwargs):
        if _plot_dir and os.path.isdir(_plot_dir):
            _plot_counter[0] += 1
            filename = os.path.join(_plot_dir, f"plot_{_plot_counter[0]}.png")
            plt.savefig(filename, bbox_inches='tight', dpi=130)
            plt.close()
        else:
            _orig_show(*args, **kwargs)

    plt.show = _custom_show
except Exception:
    pass
'''


async def run_code_or_file(
    code: Optional[str] = None,
    file_path: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    stdin_input: Optional[str] = None,
    extra_env: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Executes code string or a target file in USER_WORKSPACE_DIR using the sandbox virtual environment.
    Captures stdout, stderr, execution time, returncode, and any matplotlib plots.
    """
    await ensure_sandbox_venv()
    python_exe = get_current_python_exe()

    # Create temporary folder for plot captures
    temp_plot_dir = tempfile.mkdtemp(prefix="pydeep_plots_")
    
    # Determine script to execute
    temp_script_path: Optional[Path] = None
    target_path: Path

    try:
        if file_path:
            target_path = get_safe_path(file_path)
            if not target_path.exists():
                return {
                    "stdout": "",
                    "stderr": f"Error: File not found: {file_path}",
                    "returncode": 1,
                    "execution_time_ms": 0,
                    "plots": []
                }
            # Prepend plot hook to file content in a temp runner to prevent altering original file
            original_code = target_path.read_text(encoding="utf-8", errors="replace")
            combined_code = PLOT_HOOK_CODE + "\n" + original_code
            temp_script_path = USER_WORKSPACE_DIR / f"_runner_exec_{int(time.time()*1000)}.py"
            temp_script_path.write_text(combined_code, encoding="utf-8")
            exec_file = temp_script_path
        else:
            code = code or ""
            combined_code = PLOT_HOOK_CODE + "\n" + code
            temp_script_path = USER_WORKSPACE_DIR / f"_runner_exec_{int(time.time()*1000)}.py"
            temp_script_path.write_text(combined_code, encoding="utf-8")
            exec_file = temp_script_path

        env = os.environ.copy()
        env["PYTHONPATH"] = str(USER_WORKSPACE_DIR)
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        env["MPLBACKEND"] = "Agg"
        env["_PYDEEP_PLOT_DIR"] = temp_plot_dir
        if extra_env:
            env.update(extra_env)

        start_time = time.perf_counter()

        proc = await asyncio.create_subprocess_exec(
            python_exe,
            "-u",
            str(exec_file.relative_to(USER_WORKSPACE_DIR)),
            cwd=str(USER_WORKSPACE_DIR),
            env=env,
            stdin=asyncio.subprocess.PIPE if stdin_input is not None else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        timed_out = False
        try:
            stdin_bytes = stdin_input.encode("utf-8") if stdin_input else None
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(input=stdin_bytes),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            timed_out = True
            try:
                proc.kill()
                await proc.wait()
            except Exception:
                pass
            stdout_bytes = b""
            stderr_bytes = f"Execution timed out after {timeout} seconds. Check for infinite loops or blocking calls.".encode("utf-8")

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Truncate if exceeds MAX_OUTPUT_BYTES
        stdout_str = stdout_bytes.decode("utf-8", errors="replace")
        if len(stdout_str) > MAX_OUTPUT_BYTES:
            stdout_str = stdout_str[:MAX_OUTPUT_BYTES] + "\n\n[Output truncated: exceeded 512 KB limit]"

        stderr_str = stderr_bytes.decode("utf-8", errors="replace")
        if len(stderr_str) > MAX_OUTPUT_BYTES:
            stderr_str = stderr_str[:MAX_OUTPUT_BYTES] + "\n\n[Stderr truncated: exceeded 512 KB limit]"

        # Collect any generated plots
        plots_b64: List[str] = []
        plot_path = Path(temp_plot_dir)
        if plot_path.exists():
            for img_file in sorted(plot_path.glob("*.png")):
                try:
                    data = img_file.read_bytes()
                    encoded = base64.b64encode(data).decode("utf-8")
                    plots_b64.append(f"data:image/png;base64,{encoded}")
                except Exception:
                    pass

        return {
            "stdout": stdout_str,
            "stderr": stderr_str,
            "returncode": -1 if timed_out else proc.returncode,
            "timed_out": timed_out,
            "execution_time_ms": elapsed_ms,
            "plots": plots_b64
        }

    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"System error executing script: {str(e)}\n{traceback.format_exc()}",
            "returncode": -1,
            "timed_out": False,
            "execution_time_ms": 0,
            "plots": []
        }
    finally:
        # Cleanup temp runner script
        if temp_script_path and temp_script_path.exists():
            try:
                temp_script_path.unlink()
            except Exception:
                pass
        # Cleanup temp plot dir
        if os.path.exists(temp_plot_dir):
            try:
                shutil.rmtree(temp_plot_dir)
            except Exception:
                pass
