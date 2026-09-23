# ============================================
# BKFlow Celery Beat Startup Script
# Periodic task scheduler
# ============================================

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "BKFlow Celery Beat Startup" -ForegroundColor Cyan
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

# Start Celery Beat
Write-Host "[3/3] Starting Celery Beat..." -ForegroundColor Green
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Celery Beat is running..." -ForegroundColor Cyan
Write-Host "Periodic task scheduler started" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

celery -A blueapps.core.celery beat -l info
