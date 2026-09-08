# Python Deep Dive Lab - Startup Script
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Starting Python Deep Dive Lab..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$ROOT_DIR = Split-Path -Parent $PSScriptRoot
Set-Location $ROOT_DIR

# Check if frontend is built
if (-not (Test-Path "$ROOT_DIR\frontend\dist\index.html")) {
    Write-Host "Building frontend assets with pnpm..." -ForegroundColor Yellow
    Set-Location "$ROOT_DIR\frontend"
    pnpm install
    pnpm build
    Set-Location $ROOT_DIR
}

Write-Host "Starting API & Web Application Server..." -ForegroundColor Green
Write-Host "Open http://localhost:8000 in your browser." -ForegroundColor Green

# Start python backend
python backend/run.py
