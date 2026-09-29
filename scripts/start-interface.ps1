# 启动 Interface 模块
# 使用方法: .\scripts\start-interface.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Starting Interface Module" -ForegroundColor Cyan
Write-Host "  Port: 8000" -ForegroundColor Cyan
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

# 确保是 interface 模式
$env:BKFLOW_MODULE_TYPE = 'interface'
$env:DJANGO_SETTINGS_MODULE = 'config.dev'

Write-Host "[OK] Environment variables loaded" -ForegroundColor Green
Write-Host "[OK] Module type: interface" -ForegroundColor Green
Write-Host ""
Write-Host "Starting Django server on 0.0.0.0:8000..." -ForegroundColor Yellow
Write-Host ""

# 启动服务
python manage.py runserver 0.0.0.0:8000 --noreload
