from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.core.file_manager import (
    create_directory_path,
    delete_file_or_dir,
    get_file_tree,
    init_sample_workspace,
    read_file_content,
    rename_file_or_dir,
    write_file_content,
)

router = APIRouter(prefix="/files", tags=["files"])


class FileSaveRequest(BaseModel):
    path: str
    content: str


class FileCreateRequest(BaseModel):
    path: str
    is_directory: bool = False
    initial_content: str = ""


class FileRenameRequest(BaseModel):
    old_path: str
    new_path: str


@router.get("/tree")
async def get_workspace_tree():
    """Returns the user workspace directory tree."""
    tree = get_file_tree()
    return {"files": tree}


@router.get("/read")
async def read_file(path: str = Query(..., description="Relative path in user workspace")):
    """Reads a text file from the workspace."""
    try:
        content = read_file_content(path)
        return {"path": path, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_file(payload: FileSaveRequest):
    """Saves or overwrites a file in the workspace."""
    try:
        result = write_file_content(payload.path, payload.content)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
async def create_file_or_folder(payload: FileCreateRequest):
    """Creates a new file or directory in the workspace."""
    try:
        if payload.is_directory:
            result = create_directory_path(payload.path)
        else:
            result = write_file_content(payload.path, payload.initial_content)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rename")
async def rename_file(payload: FileRenameRequest):
    """Renames or moves a file/folder within the workspace."""
    try:
        result = rename_file_or_dir(payload.old_path, payload.new_path)
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Item not found: {payload.old_path}")
    except FileExistsError:
        raise HTTPException(status_code=409, detail=f"Destination already exists: {payload.new_path}")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete")
async def delete_file(path: str = Query(..., description="Relative path to file or folder")):
    """Deletes a file or directory from the workspace."""
    try:
        result = delete_file_or_dir(path)
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Item not found: {path}")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset-workspace")
async def reset_workspace():
    """Resets workspace to default sample modules and tutorials."""
    init_sample_workspace()
    return {"success": True, "files": get_file_tree()}
