import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import USER_WORKSPACE_DIR


def get_safe_path(relative_path: str) -> Path:
    """Resolves relative_path inside USER_WORKSPACE_DIR, raising ValueError if escaping."""
    normalized = os.path.normpath(relative_path).lstrip("/\\")
    full_path = (USER_WORKSPACE_DIR / normalized).resolve()
    if not str(full_path).startswith(str(USER_WORKSPACE_DIR.resolve())):
        raise ValueError(f"Path traversal detected: {relative_path}")
    return full_path


def get_file_tree(current_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Builds a recursive directory tree for user workspace."""
    if current_dir is None:
        current_dir = USER_WORKSPACE_DIR

    entries = []
    try:
        items = sorted(current_dir.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        for item in items:
            if item.name.startswith(".") or item.name == "__pycache__":
                continue
            
            rel_path = str(item.relative_to(USER_WORKSPACE_DIR)).replace("\\", "/")
            if item.is_dir():
                entries.append({
                    "name": item.name,
                    "path": rel_path,
                    "is_directory": True,
                    "children": get_file_tree(item)
                })
            else:
                entries.append({
                    "name": item.name,
                    "path": rel_path,
                    "is_directory": False,
                    "size": item.stat().st_size
                })
    except Exception:
        pass
    return entries


def read_file_content(relative_path: str) -> str:
    path = get_safe_path(relative_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {relative_path}")
    return path.read_text(encoding="utf-8", errors="replace")


def write_file_content(relative_path: str, content: str) -> Dict[str, Any]:
    path = get_safe_path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {
        "success": True,
        "path": relative_path,
        "size": path.stat().st_size
    }


def create_directory_path(relative_path: str) -> Dict[str, Any]:
    path = get_safe_path(relative_path)
    path.mkdir(parents=True, exist_ok=True)
    return {"success": True, "path": relative_path}


def delete_file_or_dir(relative_path: str) -> Dict[str, Any]:
    path = get_safe_path(relative_path)
    if not path.exists():
        raise FileNotFoundError(f"Item not found: {relative_path}")
    if path.resolve() == USER_WORKSPACE_DIR.resolve():
        raise ValueError("Cannot delete root workspace")
        
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return {"success": True, "path": relative_path}


def rename_file_or_dir(old_rel_path: str, new_rel_path: str) -> Dict[str, Any]:
    old_p = get_safe_path(old_rel_path)
    new_p = get_safe_path(new_rel_path)
    if not old_p.exists():
        raise FileNotFoundError(f"Item not found: {old_rel_path}")
    if new_p.exists():
        raise FileExistsError(f"Target already exists: {new_rel_path}")
    
    new_p.parent.mkdir(parents=True, exist_ok=True)
    old_p.rename(new_p)
    return {"success": True, "old_path": old_rel_path, "new_path": new_rel_path}


def init_sample_workspace() -> None:
    """Populates starter files if workspace is completely empty."""
    py_files = list(USER_WORKSPACE_DIR.glob("*.py"))
    if py_files:
        return

    # Sample helper module
    helpers_code = '''"""
Custom Math & Data Utilities module.
You can import this module in main.py using:
    from math_utils import fibonacci, is_prime, moving_average
"""

def fibonacci(n: int) -> list[int]:
    """Generates first n Fibonacci numbers."""
    if n <= 0:
        return []
    res = [0, 1]
    while len(res) < n:
        res.append(res[-1] + res[-2])
    return res[:n]


def is_prime(n: int) -> bool:
    """Checks if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def moving_average(values: list[float], window_size: int = 3) -> list[float]:
    """Calculates rolling simple moving average."""
    if not values or window_size <= 0:
        return []
    result = []
    for i in range(len(values) - window_size + 1):
        window = values[i : i + window_size]
        result.append(round(sum(window) / window_size, 2))
    return result
'''

    main_code = '''"""
Python Deep Dive Lab - Sandbox Playground
Here you can run any Python code, create multiple modules, and install pip packages!
"""
import sys
from math_utils import fibonacci, is_prime, moving_average

print(f"=== Welcome to Python Deep Dive Lab! ===")
print(f"Python interpreter: {sys.version.split()[0]}")
print()

# 1. Multi-file imports test
fib_10 = fibonacci(10)
print(f"Fibonacci(10): {fib_10}")

primes = [x for x in range(2, 30) if is_prime(x)]
print(f"Primes up to 30: {primes}")

sample_data = [10.0, 20.0, 30.0, 40.0, 50.0]
print(f"Moving average: {moving_average(sample_data, window_size=3)}")
print()

# 2. Try importing external libraries (e.g., numpy, rich, matplotlib)
try:
    import rich
    from rich import print as rprint
    rprint("[bold green]✓ 'rich' library is available and working![/bold green]")
except ImportError:
    print("Tip: Open 'Packages' in the sidebar to install 'rich', 'numpy', etc.")
'''

    readme_code = '''# Workspace Playground

This workspace lets you experiment with Python without boundaries:
- Create additional `.py` files and import them seamlessly.
- Install external libraries via the **Packages** manager in the sidebar.
- Inspect execution output, performance time, and generated graphics.
'''

    write_file_content("math_utils.py", helpers_code)
    write_file_content("main.py", main_code)
    write_file_content("README.md", readme_code)
