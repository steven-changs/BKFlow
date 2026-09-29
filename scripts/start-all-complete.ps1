# BKFlow 完整启动脚本
# 启动 Interface、Engine、Celery Worker、Celery Beat 和前端

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "BKFlow 完整启动脚本" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = "D:\program\project\BKFlow"

# 检查并关闭已有进程
Write-Host "[1/6] 检查并关闭已有服务..." -ForegroundColor Yellow

# 关闭端口占用的进程
$ports = @(8000, 8001, 9007)
foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($connections) {
        foreach ($conn in $connections) {
            Write-Host "  关闭端口 $port 的进程 (PID: $($conn.OwningProcess))" -ForegroundColor Gray
            Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
        }
    }
}

# 关闭 Celery 进程
$celeryProcesses = Get-Process | Where-Object { $_.CommandLine -like '*celery*' -and $_.CommandLine -like '*bkflow*' }
if ($celeryProcesses) {
    Write-Host "  关闭 Celery 进程..." -ForegroundColor Gray
    $celeryProcesses | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
}

Start-Sleep -Seconds 2

# 启动 Interface (8000)
Write-Host ""
Write-Host "[2/6] 启动 Interface (端口 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath'
    Get-Content .env | ForEach-Object {
        if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') {
            [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process')
        }
    }
    `$env:BKFLOW_MODULE_TYPE='interface'
    `$env:DJANGO_SETTINGS_MODULE='config.dev'
    Write-Host '============================================' -ForegroundColor Green
    Write-Host 'Interface 服务启动中 (端口 8000)' -ForegroundColor Green
    Write-Host '============================================' -ForegroundColor Green
    python manage.py runserver 0.0.0.0:8000 --noreload
"@

Start-Sleep -Seconds 3

# 启动 Engine (8001)
Write-Host "[3/6] 启动 Engine (端口 8001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath'
    Get-Content .env | ForEach-Object {
        if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') {
            [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process')
        }
    }
    `$env:BKFLOW_MODULE_TYPE='engine'
    `$env:DJANGO_SETTINGS_MODULE='config.dev'
    Write-Host '============================================' -ForegroundColor Green
    Write-Host 'Engine 服务启动中 (端口 8001)' -ForegroundColor Green
    Write-Host '============================================' -ForegroundColor Green
    python manage.py runserver 0.0.0.0:8001 --noreload
"@

Start-Sleep -Seconds 3

# 启动 Celery Worker
Write-Host "[4/6] 启动 Celery Worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath'
    Get-Content .env | ForEach-Object {
        if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') {
            [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process')
        }
    }
    `$env:BKFLOW_MODULE_TYPE='engine'
    `$env:DJANGO_SETTINGS_MODULE='config.dev'
    Write-Host '============================================' -ForegroundColor Green
    Write-Host 'Celery Worker 启动中 (监听所有队列)' -ForegroundColor Green
    Write-Host '============================================' -ForegroundColor Green
    celery -A config worker -l info -P gevent -c 100
"@

Start-Sleep -Seconds 3

# 启动 Celery Beat
Write-Host "[5/6] 启动 Celery Beat..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath'
    Get-Content .env | ForEach-Object {
        if (`$_ -match '^([^=]+)=(.*)$' -and `$matches[1] -notmatch '^#') {
            [System.Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process')
        }
    }
    `$env:BKFLOW_MODULE_TYPE='engine'
    `$env:DJANGO_SETTINGS_MODULE='config.dev'
    Write-Host '============================================' -ForegroundColor Green
    Write-Host 'Celery Beat 启动中' -ForegroundColor Green
    Write-Host '============================================' -ForegroundColor Green
    celery -A bkflow beat -l info
"@

Start-Sleep -Seconds 3

# 启动前端 (9007)
Write-Host "[6/6] 启动前端 (端口 9007)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath\frontend'
    Write-Host '============================================' -ForegroundColor Green
    Write-Host '前端服务启动中 (端口 9007)' -ForegroundColor Green
    Write-Host '============================================' -ForegroundColor Green
    npm run dev
"@

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "等待服务启动..." -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Start-Sleep -Seconds 10

# 验证服务
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "服务状态检查" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$services = @(
    @{Name="Interface"; Port=8000},
    @{Name="Engine"; Port=8001},
    @{Name="Frontend"; Port=9007}
)

foreach ($service in $services) {
    $conn = Get-NetTCPConnection -LocalPort $service.Port -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        Write-Host "[✓] $($service.Name) (端口 $($service.Port)): 运行中" -ForegroundColor Green
    } else {
        Write-Host "[✗] $($service.Name) (端口 $($service.Port)): 未启动" -ForegroundColor Red
    }
}

# 检查 Celery
$celeryCount = (Get-Process | Where-Object { $_.CommandLine -like '*celery*bkflow*' }).Count
if ($celeryCount -ge 2) {
    Write-Host "[✓] Celery Worker & Beat: 运行中 ($celeryCount 个进程)" -ForegroundColor Green
} else {
    Write-Host "[✗] Celery Worker & Beat: 未完全启动" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "所有服务已启动！" -ForegroundColor Green
Write-Host "访问地址: https://localhost:9007" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "提示: 现在可以在浏览器中创建并执行任务了" -ForegroundColor Yellow
Write-Host ""
