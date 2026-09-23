# ============================================
# BKFlow One-Click Start All Services
# Starts all required services in multiple terminal windows
# ============================================

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "BKFlow One-Click Startup Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check virtual environment
if (-not (Test-Path "D:\program\env\bkflow_env")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please complete initialization steps first" -ForegroundColor Yellow
    exit 1
}

# Check MySQL
$mysqlService = Get-Service -Name MySQL80 -ErrorAction SilentlyContinue
if ($mysqlService.Status -ne "Running") {
    Write-Host "[WARNING] MySQL not running, starting..." -ForegroundColor Yellow
    Start-Service MySQL80
    Start-Sleep -Seconds 2
}

# Check Redis
$redisService = Get-Service -Name Redis -ErrorAction SilentlyContinue
if ($redisService.Status -ne "Running") {
    Write-Host "[WARNING] Redis not running, starting..." -ForegroundColor Yellow
    Start-Service Redis
    Start-Sleep -Seconds 2
}

Write-Host "MySQL and Redis are ready" -ForegroundColor Green
Write-Host ""
Write-Host "Starting services in 3 new terminal windows..." -ForegroundColor Cyan
Write-Host ""

# Start Django server
Write-Host "[1/3] Starting Django server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\program\project\BKFlow; .\scripts\start-local.ps1"

Start-Sleep -Seconds 2

# Start Celery Worker
Write-Host "[2/3] Starting Celery Worker..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\program\project\BKFlow; .\scripts\start-celery-worker.ps1"

Start-Sleep -Seconds 2

# Start Celery Beat
Write-Host "[3/3] Starting Celery Beat..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\program\project\BKFlow; .\scripts\start-celery-beat.ps1"

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "All services started!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Service Information:" -ForegroundColor Cyan
Write-Host "  Web Application: http://localhost:8000" -ForegroundColor White
Write-Host "  Admin Panel: http://localhost:8000/bkflow_admin" -ForegroundColor White
Write-Host ""
Write-Host "3 terminal windows opened:" -ForegroundColor Cyan
Write-Host "  1. Django Server" -ForegroundColor White
Write-Host "  2. Celery Worker" -ForegroundColor White
Write-Host "  3. Celery Beat" -ForegroundColor White
Write-Host ""
Write-Host "Tip: Close terminal windows to stop services" -ForegroundColor Yellow
Write-Host ""
