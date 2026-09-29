# BKFlow 快速启动脚本
# 用法: .\start-bkflow.ps1

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "BKFlow 快速启动" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$projectPath = "D:\program\project\BKFlow"

# 启动 Interface
Write-Host "`n[1/5] 启动 Interface..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; Get-Content .env | ForEach-Object { if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') { [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process') } }; `$env:BKFLOW_MODULE_TYPE='interface'; Write-Host 'Interface (Module: interface)' -ForegroundColor Green; python manage.py runserver 0.0.0.0:8000 --noreload"
Start-Sleep -Seconds 3

# 启动 Engine
Write-Host "[2/5] 启动 Engine..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; Get-Content .env | ForEach-Object { if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') { [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process') } }; `$env:BKFLOW_MODULE_TYPE='engine'; Write-Host 'Engine (Module: engine)' -ForegroundColor Green; python manage.py runserver 0.0.0.0:8001 --noreload"
Start-Sleep -Seconds 3

# 启动 Celery Worker
Write-Host "[3/5] 启动 Celery Worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; Get-Content .env | ForEach-Object { if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') { [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process') } }; `$env:BKFLOW_MODULE_TYPE='engine'; Write-Host 'Celery Worker (Module: engine)' -ForegroundColor Green; celery -A config worker -l info -P gevent -c 100"
Start-Sleep -Seconds 3

# 启动 Celery Beat
Write-Host "[4/5] 启动 Celery Beat..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; Get-Content .env | ForEach-Object { if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') { [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process') } }; `$env:BKFLOW_MODULE_TYPE='engine'; Write-Host 'Celery Beat (Module: engine)' -ForegroundColor Green; celery -A config beat -l info"
Start-Sleep -Seconds 3

# 启动前端
Write-Host "[5/5] 启动前端..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\frontend'; Write-Host 'Frontend (Port 9007)' -ForegroundColor Green; npm run dev"

Write-Host "`n等待服务启动..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# 验证
Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "服务状态" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$ports = @(8000, 8001, 9007)
foreach ($port in $ports) {
    $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        Write-Host "[OK] Port $port" -ForegroundColor Green
    } else {
        Write-Host "[WAIT] Port $port" -ForegroundColor Yellow
    }
}

$pythonCount = (Get-Process python -ErrorAction SilentlyContinue).Count
Write-Host "`nPython processes: $pythonCount" -ForegroundColor Cyan

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "访问地址: https://localhost:9007" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
