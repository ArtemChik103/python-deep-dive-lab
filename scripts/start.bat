@echo off
title Python Deep Dive Lab
echo ==========================================
echo  Starting Python Deep Dive Lab...
echo ==========================================

cd /d "%~dp0\.."

if not exist "frontend\dist\index.html" (
    echo Building frontend assets with pnpm...
    cd frontend
    call pnpm install
    call pnpm build
    cd ..
)

echo Starting Web Application Server at http://localhost:8000 ...
python backend\run.py
pause
