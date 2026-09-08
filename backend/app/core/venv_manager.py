import asyncio
import json
import logging
import os
import re
import subprocess
import sys
from typing import Any, Dict, List

from app.config import SANDBOX_PIP, SANDBOX_PYTHON, SANDBOX_VENV_DIR

logger = logging.getLogger("pydeep.venv")

SAFE_PACKAGE_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.\[\],<>=~!]+$")


def get_current_python_exe() -> str:
    """Returns sandbox python if ready, else system python."""
    if SANDBOX_PYTHON.exists():
        return str(SANDBOX_PYTHON)
    return sys.executable


def get_current_pip_exe() -> str:
    """Returns sandbox pip if ready, else system pip."""
    if SANDBOX_PIP.exists():
        return str(SANDBOX_PIP)
    return f"{sys.executable} -m pip"


def ensure_sandbox_venv_sync() -> bool:
    """Creates the user sandbox virtual environment if not already present."""
    if SANDBOX_PYTHON.exists():
        return True

    logger.info(f"Creating sandbox virtual environment at {SANDBOX_VENV_DIR}...")
    try:
        cmd = [sys.executable, "-m", "venv", str(SANDBOX_VENV_DIR)]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if res.returncode != 0:
            logger.error(f"Failed to create venv: {res.stderr}")
            return False
        logger.info("Sandbox virtual environment initialized successfully.")
        return True
    except Exception as e:
        logger.error(f"Exception during venv creation: {e}")
        return False


async def ensure_sandbox_venv() -> bool:
    return await asyncio.to_thread(ensure_sandbox_venv_sync)


async def list_installed_packages() -> List[Dict[str, str]]:
    """Returns the list of installed packages in the sandbox venv."""
    await ensure_sandbox_venv()
    python_exe = get_current_python_exe()

    try:
        proc = await asyncio.create_subprocess_exec(
            python_exe, "-m", "pip", "list", "--format=json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0 and stdout:
            data = json.loads(stdout.decode("utf-8", errors="replace"))
            return [{"name": item.get("name", ""), "version": item.get("version", "")} for item in data]
        return []
    except Exception as e:
        logger.error(f"Error listing packages: {e}")
        return []


async def install_package(package_spec: str) -> Dict[str, Any]:
    """Installs a package into the sandbox virtual environment."""
    package_spec = package_spec.strip()
    if not package_spec or not SAFE_PACKAGE_PATTERN.match(package_spec):
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Invalid or unsafe package specification: '{package_spec}'",
            "returncode": -1
        }

    await ensure_sandbox_venv()
    python_exe = get_current_python_exe()

    try:
        proc = await asyncio.create_subprocess_exec(
            python_exe, "-m", "pip", "install", package_spec, "--no-input",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        out_text = stdout.decode("utf-8", errors="replace")
        err_text = stderr.decode("utf-8", errors="replace")

        return {
            "success": proc.returncode == 0,
            "stdout": out_text,
            "stderr": err_text,
            "returncode": proc.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Failed to run pip install: {str(e)}",
            "returncode": -1
        }


async def uninstall_package(package_name: str) -> Dict[str, Any]:
    """Uninstalls a package from the sandbox virtual environment."""
    package_name = package_name.strip()
    if not package_name or not re.match(r"^[a-zA-Z0-9_\-]+$", package_name):
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Invalid package name: '{package_name}'",
            "returncode": -1
        }

    await ensure_sandbox_venv()
    python_exe = get_current_python_exe()

    try:
        proc = await asyncio.create_subprocess_exec(
            python_exe, "-m", "pip", "uninstall", "-y", package_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return {
            "success": proc.returncode == 0,
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "returncode": proc.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Failed to run pip uninstall: {str(e)}",
            "returncode": -1
        }
