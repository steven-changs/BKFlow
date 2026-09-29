# ============================================
# BKFlow 前端开发服务启动脚本
# ============================================

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "BKFlow Frontend Development Server" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Node.js
Write-Host "[1/4] Checking Node.js..." -ForegroundColor Green
$nodeVersion = node --version
$npmVersion = npm --version
Write-Host "Node.js: $nodeVersion" -ForegroundColor White
Write-Host "npm: $npmVersion" -ForegroundColor White

if (-not $nodeVersion) {
    Write-Host "[ERROR] Node.js not found!" -ForegroundColor Red
    Write-Host "Please install Node.js >= 18.20.4" -ForegroundColor Yellow
    exit 1
}

# 进入前端目录
Write-Host ""
Write-Host "[2/4] Entering frontend directory..." -ForegroundColor Green
Set-Location D:\program\project\BKFlow\frontend

# 检查依赖
Write-Host ""
Write-Host "[3/4] Checking dependencies..." -ForegroundColor Green
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies (this may take a while)..." -ForegroundColor Yellow
    npm install
} else {
    Write-Host "Dependencies already installed" -ForegroundColor White
}

# 启动开发服务器
Write-Host ""
Write-Host "[4/4] Starting development server..." -ForegroundColor Green
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Frontend server starting..." -ForegroundColor Cyan
Write-Host "Access URL: http://localhost:9007" -ForegroundColor Green
Write-Host "API Backend: http://localhost:8000" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: Make sure Django backend is running on port 8000" -ForegroundColor Yellow
Write-Host ""

# 启动
npm run dev
