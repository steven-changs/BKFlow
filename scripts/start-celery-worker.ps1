# ============================================
# BKFlow Celery Worker Startup Script
# Uses eventlet pool for Windows compatibility
# ============================================

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "BKFlow Celery Worker Startup" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
if (Test-Path "D:\program\env\bkflow_env\Scripts\Activate.ps1") {
    Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Green
    & "D:\program\env\bkflow_env\Scripts\Activate.ps1"
} else {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    exit 1
}

# Set environment variables
Write-Host "[2/3] Setting environment variables..." -ForegroundColor Green
. "$PSScriptRoot\set-env.ps1"

# Start Celery Worker
Write-Host "[3/3] Starting Celery Worker..." -ForegroundColor Green
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Celery Worker is running..." -ForegroundColor Cyan
Write-Host "Using eventlet pool (Windows compatible)" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

celery -A blueapps.core.celery worker -l info -P eventlet
