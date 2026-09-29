# ============================================
# BKFlow Local Development Startup Script
# Solution A: Local Environment Deployment
# ============================================

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "BKFlow Local Environment Startup" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check virtual environment
if (-not (Test-Path "D:\program\env\bkflow_env")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: py -3.11 -m venv D:\program\env\bkflow_env" -ForegroundColor Yellow
    Write-Host "Then run: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "[1/5] Activating virtual environment..." -ForegroundColor Green
& "D:\program\env\bkflow_env\Scripts\Activate.ps1"

# Set environment variables
Write-Host "[2/5] Setting environment variables..." -ForegroundColor Green
. "$PSScriptRoot\set-env.ps1"

# Check MySQL connection
Write-Host "[3/5] Checking MySQL connection..." -ForegroundColor Green
$mysqlService = Get-Service -Name MySQL80 -ErrorAction SilentlyContinue
if ($mysqlService.Status -ne "Running") {
    Write-Host "[WARNING] MySQL service is not running!" -ForegroundColor Yellow
    Write-Host "Start MySQL: Start-Service MySQL80" -ForegroundColor Yellow
    exit 1
}

# Check Redis connection
Write-Host "[4/5] Checking Redis connection..." -ForegroundColor Green
$redisService = Get-Service -Name Redis -ErrorAction SilentlyContinue
if ($redisService.Status -ne "Running") {
    Write-Host "[WARNING] Redis service is not running!" -ForegroundColor Yellow
    Write-Host "Start Redis: Start-Service Redis" -ForegroundColor Yellow
    exit 1
}

Write-Host "[5/5] Starting Django development server..." -ForegroundColor Green
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Service starting..." -ForegroundColor Cyan
Write-Host "Access URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Start Django server
python manage.py runserver 0.0.0.0:8000
