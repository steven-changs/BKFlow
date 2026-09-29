# ============================================
# BKFlow Docker 快速部署脚本
# 方案 B: Docker 容器化部署
# ============================================

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("up", "down", "restart", "logs", "clean", "status")]
    [string]$Action = "up"
)

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "BKFlow Docker 部署管理" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

switch ($Action) {
    "up" {
        Write-Host "[操作] 启动所有服务..." -ForegroundColor Green
        docker-compose up -d
        Write-Host ""
        Write-Host "✓ 服务已启动" -ForegroundColor Green
        Write-Host "访问地址: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "查看日志: .\scripts\docker-manage.ps1 logs" -ForegroundColor Yellow
    }
    "down" {
        Write-Host "[操作] 停止并删除容器..." -ForegroundColor Yellow
        docker-compose down
        Write-Host ""
        Write-Host "✓ 容器已停止并删除（数据保留）" -ForegroundColor Green
    }
    "restart" {
        Write-Host "[操作] 重启所有服务..." -ForegroundColor Yellow
        docker-compose restart
        Write-Host ""
        Write-Host "✓ 服务已重启" -ForegroundColor Green
    }
    "logs" {
        Write-Host "[操作] 查看实时日志..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    "clean" {
        Write-Host "[警告] 这将删除所有容器、镜像和数据卷!" -ForegroundColor Red
        $confirm = Read-Host "确认删除? (yes/no)"
        if ($confirm -eq "yes") {
            Write-Host "[操作] 完全清理..." -ForegroundColor Red
            docker-compose down -v --rmi all
            Write-Host ""
            Write-Host "✓ 已完全清理" -ForegroundColor Green
        } else {
            Write-Host "操作已取消" -ForegroundColor Yellow
        }
    }
    "status" {
        Write-Host "[信息] 容器状态:" -ForegroundColor Cyan
        docker-compose ps
        Write-Host ""
        Write-Host "[信息] 磁盘占用:" -ForegroundColor Cyan
        docker system df
    }
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "可用命令:" -ForegroundColor Cyan
Write-Host "  up      - 启动所有服务" -ForegroundColor White
Write-Host "  down    - 停止并删除容器（保留数据）" -ForegroundColor White
Write-Host "  restart - 重启服务" -ForegroundColor White
Write-Host "  logs    - 查看实时日志" -ForegroundColor White
Write-Host "  status  - 查看状态和磁盘占用" -ForegroundColor White
Write-Host "  clean   - 完全清理（删除所有数据）" -ForegroundColor White
Write-Host "====================================" -ForegroundColor Cyan
