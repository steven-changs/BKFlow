# BKFlow 完整启动脚本 v2
# 正确处理不同模块类型的环境变量

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "BKFlow 完整启动脚本 v2" -ForegroundColor Cyan
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
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.StartTime -gt (Get-Date).AddHours(-1)
} | ForEach-Object {
    Write-Host "  关闭 Python 进程 (PID: $($_.Id))" -ForegroundColor Gray
    Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 2

# 启动 Interface (8000)
Write-Host ""
Write-Host "[2/6] 启动 Interface (端口 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath'
    # 不要从 .env 加载，直接设置环境变量
    `$env:BKPAAS_ENVIRONMENT='dev'
    `$env:BK_ENV='development'
    `$env:APP_ID='bkflow'
    `$env:APP_CODE='bkflow'
    `$env:BKPAAS_APP_ID='bkflow'
    `$env:BKPAAS_APP_SECRET='bkflow-local-dev-secret-12345678'
    `$env:APP_TOKEN='bkflow-local-dev-token-12345678'
    `$env:SECRET_KEY='bkflow-local-dev-secret-key-change-in-production'
    `$env:MYSQL_NAME='bkflow'
    `$env:MYSQL_USER='bkflow'
    `$env:MYSQL_PASSWORD='bkflow123'
    `$env:MYSQL_HOST='localhost'
    `$env:MYSQL_PORT='3306'
    `$env:REDIS_HOST='localhost'
    `$env:REDIS_PORT='6379'
    `$env:REDIS_DB='0'
    `$env:BK_PAAS_HOST='http://localhost:8000'
    `$env:BKPAAS_DOMAIN='localhost'
    `$env:BKPAAS_ENGINE_REGION='ieod'
    `$env:BK_COMPONENT_API_URL='http://localhost:8000/api'
    `$env:BK_APIGW_NETLOC_PATTERN='^(?P<api_name>[\w-]+)\.localhost'
    `$env:SKIP_APIGW_CHECK='True'
    `$env:APP_INTERNAL_TOKEN='local-dev-token'
    `$env:RUN_VER='open'
    `$env:BKPAAS_LOGIN_EXEMPT='True'
    `$env:BKAPP_USE_PLAIN_AUTHENTICATION='True'
    `$env:BKPAAS_LOGIN_PLAIN_USERNAME='admin'
    `$env:INTERFACE_APP_URL='http://localhost:8000'

    # Interface 模块配置
    `$env:BKFLOW_MODULE_TYPE='interface'
    `$env:BKFLOW_MODULE_CODE='default'
    `$env:DJANGO_SETTINGS_MODULE='config.dev'

    Write-Host '============================================' -ForegroundColor Green
    Write-Host 'Interface 服务启动中 (端口 8000)' -ForegroundColor Green
    Write-Host 'Module Type: interface' -ForegroundColor Cyan
    Write-Host '============================================' -ForegroundColor Green
    python manage.py runserver 0.0.0.0:8000 --noreload
"@

Start-Sleep -Seconds 3

# 启动 Engine (8001)
Write-Host "[3/6] 启动 Engine (端口 8001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath'
    # 加载基础环境变量
    `$env:BKPAAS_ENVIRONMENT='dev'
    `$env:BK_ENV='development'
    `$env:APP_ID='bkflow'
    `$env:APP_CODE='bkflow'
    `$env:BKPAAS_APP_ID='bkflow'
    `$env:BKPAAS_APP_SECRET='bkflow-local-dev-secret-12345678'
    `$env:APP_TOKEN='bkflow-local-dev-token-12345678'
    `$env:SECRET_KEY='bkflow-local-dev-secret-key-change-in-production'
    `$env:MYSQL_NAME='bkflow'
    `$env:MYSQL_USER='bkflow'
    `$env:MYSQL_PASSWORD='bkflow123'
    `$env:MYSQL_HOST='localhost'
    `$env:MYSQL_PORT='3306'
    `$env:REDIS_HOST='localhost'
    `$env:REDIS_PORT='6379'
    `$env:REDIS_DB='0'
    `$env:BK_PAAS_HOST='http://localhost:8000'
    `$env:BKPAAS_DOMAIN='localhost'
    `$env:BKPAAS_ENGINE_REGION='ieod'
    `$env:BK_COMPONENT_API_URL='http://localhost:8000/api'
    `$env:BK_APIGW_NETLOC_PATTERN='^(?P<api_name>[\w-]+)\.localhost'
    `$env:SKIP_APIGW_CHECK='True'
    `$env:APP_INTERNAL_TOKEN='local-dev-token'
    `$env:RUN_VER='open'
    `$env:BKPAAS_LOGIN_EXEMPT='True'
    `$env:BKAPP_USE_PLAIN_AUTHENTICATION='True'
    `$env:BKPAAS_LOGIN_PLAIN_USERNAME='admin'
    `$env:INTERFACE_APP_URL='http://localhost:8000'

    # Engine 模块配置（关键！）
    `$env:BKFLOW_MODULE_TYPE='engine'
    `$env:BKFLOW_MODULE_CODE='default'
    `$env:DJANGO_SETTINGS_MODULE='config.dev'

    Write-Host '============================================' -ForegroundColor Green
    Write-Host 'Engine 服务启动中 (端口 8001)' -ForegroundColor Green
    Write-Host 'Module Type: engine' -ForegroundColor Cyan
    Write-Host '============================================' -ForegroundColor Green
    python manage.py runserver 0.0.0.0:8001 --noreload
"@

Start-Sleep -Seconds 3

# 启动 Celery Worker (必须使用 engine 模块类型)
Write-Host "[4/6] 启动 Celery Worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath'
    # 加载基础环境变量
    `$env:BKPAAS_ENVIRONMENT='dev'
    `$env:BK_ENV='development'
    `$env:APP_ID='bkflow'
    `$env:APP_CODE='bkflow'
    `$env:BKPAAS_APP_ID='bkflow'
    `$env:BKPAAS_APP_SECRET='bkflow-local-dev-secret-12345678'
    `$env:APP_TOKEN='bkflow-local-dev-token-12345678'
    `$env:SECRET_KEY='bkflow-local-dev-secret-key-change-in-production'
    `$env:MYSQL_NAME='bkflow'
    `$env:MYSQL_USER='bkflow'
    `$env:MYSQL_PASSWORD='bkflow123'
    `$env:MYSQL_HOST='localhost'
    `$env:MYSQL_PORT='3306'
    `$env:REDIS_HOST='localhost'
    `$env:REDIS_PORT='6379'
    `$env:REDIS_DB='0'
    `$env:BK_PAAS_HOST='http://localhost:8000'
    `$env:BKPAAS_DOMAIN='localhost'
    `$env:BKPAAS_ENGINE_REGION='ieod'
    `$env:BK_COMPONENT_API_URL='http://localhost:8000/api'
    `$env:BK_APIGW_NETLOC_PATTERN='^(?P<api_name>[\w-]+)\.localhost'
    `$env:SKIP_APIGW_CHECK='True'
    `$env:APP_INTERNAL_TOKEN='local-dev-token'
    `$env:RUN_VER='open'
    `$env:INTERFACE_APP_URL='http://localhost:8000'

    # Celery 必须使用 engine 模块类型
    `$env:BKFLOW_MODULE_TYPE='engine'
    `$env:BKFLOW_MODULE_CODE='default'
    `$env:DJANGO_SETTINGS_MODULE='config.dev'

    Write-Host '============================================' -ForegroundColor Green
    Write-Host 'Celery Worker 启动中' -ForegroundColor Green
    Write-Host 'Module Type: engine' -ForegroundColor Cyan
    Write-Host '============================================' -ForegroundColor Green
    celery -A config worker -l info -P gevent -c 100
"@

Start-Sleep -Seconds 3

# 启动 Celery Beat
Write-Host "[5/6] 启动 Celery Beat..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    cd '$projectPath'
    # 加载基础环境变量
    `$env:BKPAAS_ENVIRONMENT='dev'
    `$env:MYSQL_NAME='bkflow'
    `$env:MYSQL_USER='bkflow'
    `$env:MYSQL_PASSWORD='bkflow123'
    `$env:MYSQL_HOST='localhost'
    `$env:MYSQL_PORT='3306'
    `$env:REDIS_HOST='localhost'
    `$env:REDIS_PORT='6379'
    `$env:REDIS_DB='0'
    `$env:BKPAAS_DOMAIN='localhost'
    `$env:INTERFACE_APP_URL='http://localhost:8000'

    # Celery Beat 使用 engine 模块类型
    `$env:BKFLOW_MODULE_TYPE='engine'
    `$env:BKFLOW_MODULE_CODE='default'
    `$env:DJANGO_SETTINGS_MODULE='config.dev'

    Write-Host '============================================' -ForegroundColor Green
    Write-Host 'Celery Beat 启动中' -ForegroundColor Green
    Write-Host 'Module Type: engine' -ForegroundColor Cyan
    Write-Host '============================================' -ForegroundColor Green
    celery -A config beat -l info
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
$celeryCount = (Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.StartTime -gt (Get-Date).AddMinutes(-2) }).Count
if ($celeryCount -ge 4) {
    Write-Host "[✓] 所有服务 (Interface, Engine, Celery Worker, Beat): 运行中 ($celeryCount 个进程)" -ForegroundColor Green
} else {
    Write-Host "[!] 部分服务可能未启动 (当前 $celeryCount 个 Python 进程)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "所有服务已启动！" -ForegroundColor Green
Write-Host "访问地址: https://localhost:9007" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "重要提示:" -ForegroundColor Yellow
Write-Host "- Interface 使用 interface 模块类型" -ForegroundColor Gray
Write-Host "- Engine 和 Celery 使用 engine 模块类型" -ForegroundColor Gray
Write-Host "- 查看每个窗口确认模块类型正确显示" -ForegroundColor Gray
Write-Host ""
