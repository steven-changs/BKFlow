# ============================================
# BKFlow 数据库初始化脚本
# 用于本地环境首次部署
# ============================================

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "BKFlow 数据库初始化" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 激活虚拟环境
if (Test-Path "D:\program\env\bkflow_env\Scripts\Activate.ps1") {
    Write-Host "[1/5] 激活虚拟环境..." -ForegroundColor Green
    & "D:\program\env\bkflow_env\Scripts\Activate.ps1"
} else {
    Write-Host "[错误] 虚拟环境不存在!" -ForegroundColor Red
    exit 1
}

# 设置环境变量
Write-Host "[2/5] 设置环境变量..." -ForegroundColor Green
. "$PSScriptRoot\set-env.ps1"

# 检查数据库连接
Write-Host "[3/5] 检查数据库连接..." -ForegroundColor Green
Write-Host "请确保已在 MySQL 中创建数据库:" -ForegroundColor Yellow
Write-Host "  CREATE DATABASE bkflow DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" -ForegroundColor Yellow
Write-Host "  CREATE USER 'bkflow'@'localhost' IDENTIFIED BY 'bkflow123';" -ForegroundColor Yellow
Write-Host "  GRANT ALL PRIVILEGES ON bkflow.* TO 'bkflow'@'localhost';" -ForegroundColor Yellow
Write-Host ""
$continue = Read-Host "是否已创建数据库? (yes/no)"

if ($continue -ne "yes") {
    Write-Host "请先创建数据库后再运行此脚本" -ForegroundColor Yellow
    exit 0
}

# 执行数据库迁移
Write-Host "[4/5] 执行数据库迁移..." -ForegroundColor Green
python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 数据库迁移失败!" -ForegroundColor Red
    exit 1
}

# 创建超级用户
Write-Host "[5/5] 创建管理员账号..." -ForegroundColor Green
Write-Host "请按提示输入管理员信息:" -ForegroundColor Yellow
python manage.py createsuperuser

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "✓ 数据库初始化完成!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步:" -ForegroundColor Cyan
Write-Host "  1. 启动服务: .\scripts\start-local.ps1" -ForegroundColor White
Write-Host "  2. 启动 Celery Worker: .\scripts\start-celery-worker.ps1" -ForegroundColor White
Write-Host "  3. 启动 Celery Beat: .\scripts\start-celery-beat.ps1" -ForegroundColor White
Write-Host ""
