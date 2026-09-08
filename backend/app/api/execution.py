from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.runner import run_code_or_file

router = APIRouter(prefix="/execute", tags=["execution"])


class CodeExecutionRequest(BaseModel):
    code: str
    timeout: Optional[float] = 15.0
    stdin_input: Optional[str] = None


class FileExecutionRequest(BaseModel):
    file_path: str
    timeout: Optional[float] = 15.0
    stdin_input: Optional[str] = None


@router.post("/code")
async def execute_code_snippet(payload: CodeExecutionRequest):
    """Executes a Python code string inside the workspace environment."""
    result = await run_code_or_file(
        code=payload.code,
        timeout=payload.timeout or 15.0,
        stdin_input=payload.stdin_input
    )
    return result


@router.post("/file")
async def execute_workspace_file(payload: FileExecutionRequest):
    """Executes a file from the user workspace."""
    result = await run_code_or_file(
        file_path=payload.file_path,
        timeout=payload.timeout or 15.0,
        stdin_input=payload.stdin_input
    )
    return result
