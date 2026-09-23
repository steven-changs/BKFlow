# BKFlow 服务启动脚本 - 简化版
# 使用 .env 文件 + 环境变量覆盖

$projectPath = "D:\program\project\BKFlow"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "BKFlow 服务启动" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# 函数：加载 .env 并覆盖特定变量
function Start-BKFlowService {
    param(
        [string]$ServiceName,
        [int]$Port,
        [string]$ModuleType,
        [string]$Command
    )

    Write-Host "`n启动 $ServiceName (模块类型: $ModuleType)..." -ForegroundColor Yellow

    $scriptBlock = @"
cd '$projectPath'
# 加载 .env 文件
Get-Content .env | ForEach-Object {
    if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') {
        [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process')
    }
}
# 覆盖模块类型
`$env:BKFLOW_MODULE_TYPE='$ModuleType'
Write-Host '========================================' -ForegroundColor Green
Write-Host '$ServiceName' -ForegroundColor Green
Write-Host 'Module Type: $ModuleType' -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Green
$Command
"@

    Start-Process powershell -ArgumentList "-NoExit", "-Command", $scriptBlock
    Start-Sleep -Seconds 2
}

# 1. 启动 Interface
Start-BKFlowService -ServiceName "Interface (8000)" -Port 8000 -ModuleType "interface" -Command "python manage.py runserver 0.0.0.0:8000 --noreload"

# 2. 启动 Engine
Start-BKFlowService -ServiceName "Engine (8001)" -Port 8001 -ModuleType "engine" -Command "python manage.py runserver 0.0.0.0:8001 --noreload"

# 3. 启动 Celery Worker
Start-BKFlowService -ServiceName "Celery Worker" -Port 0 -ModuleType "engine" -Command "celery -A config worker -l info -P gevent -c 100"

# 4. 启动 Celery Beat
Start-BKFlowService -ServiceName "Celery Beat" -Port 0 -ModuleType "engine" -Command "celery -A config beat -l info"

# 5. 启动前端
Write-Host "`n启动前端 (9007)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\frontend'; Write-Host 'Frontend (9007)' -ForegroundColor Green; npm run dev"

Write-Host "`n等待服务启动..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# 验证服务
Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "服务状态" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$ports = @(8000, 8001, 9007)
foreach ($port in $ports) {
    $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        Write-Host "[OK] Port $port" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Port $port" -ForegroundColor Red
    }
}

$pythonCount = (Get-Process python -ErrorAction SilentlyContinue).Count
Write-Host "`nPython processes: $pythonCount" -ForegroundColor Cyan

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "Access: https://localhost:9007" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
