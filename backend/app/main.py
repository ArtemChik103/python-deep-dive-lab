import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.curriculum import router as curriculum_router
from app.api.execution import router as execution_router
from app.api.files import router as files_router
from app.api.packages import router as packages_router
from app.config import FRONTEND_DIST_DIR
from app.core.file_manager import init_sample_workspace
from app.core.venv_manager import ensure_sandbox_venv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("pydeep.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Python Deep Dive Lab Server...")
    init_sample_workspace()
    await ensure_sandbox_venv()
    logger.info("Application environment initialized successfully.")
    yield
    logger.info("Shutting down Python Deep Dive Lab Server...")


app = FastAPI(
    title="Python Deep Dive Lab API",
    description="Interactive deep Python learning platform with real execution, files, pip manager, and progressive hints",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(curriculum_router, prefix="/api")
app.include_router(execution_router, prefix="/api")
app.include_router(files_router, prefix="/api")
app.include_router(packages_router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Python Deep Dive Lab API"}


# Serve static frontend in production if built
if FRONTEND_DIST_DIR.exists() and (FRONTEND_DIST_DIR / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        target = FRONTEND_DIST_DIR / full_path
        if target.is_file():
            return FileResponse(target)
        return FileResponse(FRONTEND_DIST_DIR / "index.html")
