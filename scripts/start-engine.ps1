# 启动 Engine 模块
# 使用方法: .\scripts\start-engine.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Starting Engine Module" -ForegroundColor Cyan
Write-Host "  Port: 8001" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# 加载环境变量
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$' -and $matches[1] -notmatch '^#') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        [System.Environment]::SetEnvironmentVariable($key, $value, 'Process')
    }
}

# 设置为 engine 模式
$env:BKFLOW_MODULE_TYPE = 'engine'
$env:DJANGO_SETTINGS_MODULE = 'config.dev'

Write-Host "[OK] Environment variables loaded" -ForegroundColor Green
Write-Host "[OK] Module type: engine" -ForegroundColor Green
Write-Host ""
Write-Host "Starting Django server on 0.0.0.0:8001..." -ForegroundColor Yellow
Write-Host ""

# 启动服务
python manage.py runserver 0.0.0.0:8001 --noreload
