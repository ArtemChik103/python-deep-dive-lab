import os
import sys
from pathlib import Path
import uvicorn

# Ensure backend root is on sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("ENV", "development") == "development"
    print(f"Starting Python Deep Dive Lab API server on http://localhost:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)
