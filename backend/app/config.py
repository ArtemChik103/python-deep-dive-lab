import os
import sys
from pathlib import Path

# Paths
BACKEND_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BACKEND_DIR.parent
USER_WORKSPACE_DIR = BACKEND_DIR / "user_workspace"
USER_WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

SANDBOX_VENV_DIR = ROOT_DIR / "workspace_env"

# Resolve python & pip in sandbox venv
if os.name == "nt":
    SANDBOX_PYTHON = SANDBOX_VENV_DIR / "Scripts" / "python.exe"
    SANDBOX_PIP = SANDBOX_VENV_DIR / "Scripts" / "pip.exe"
else:
    SANDBOX_PYTHON = SANDBOX_VENV_DIR / "bin" / "python"
    SANDBOX_PIP = SANDBOX_VENV_DIR / "bin" / "pip"

# Defaults
DEFAULT_TIMEOUT_SECONDS = 15.0
MAX_OUTPUT_BYTES = 512 * 1024  # 512 KB
FRONTEND_DIST_DIR = ROOT_DIR / "frontend" / "dist"
