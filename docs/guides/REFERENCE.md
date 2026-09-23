# BKFlow 快速参考

## 🚀 快速启动

```powershell
# 一键启动所有服务
cd D:\program\project\BKFlow
.\scripts\start-all.ps1
```

访问: http://localhost:8000

---

## 📁 目录结构

```
D:\program\env\bkflow_env\          # 虚拟环境
D:\program\project\BKFlow\
  ├── local_settings.py             # 本地配置（已配置）
  ├── scripts/                      # 启动脚本
  │   ├── start-all.ps1            # 一键启动
  │   ├── start-local.ps1          # Django
  │   ├── start-celery-worker.ps1  # Worker
  │   ├── start-celery-beat.ps1    # Beat
  │   ├── init-db.ps1              # 数据库初始化
  │   └── create-database.sql      # SQL 脚本
  ├── QUICKSTART.md                # 快速开始
  ├── DEPLOYMENT.md                # 详细部署
  └── CHECKLIST.md                 # 检查清单
```

---

## 🔧 常用命令

### 激活虚拟环境
```powershell
& D:\program\env\bkflow_env\Scripts\Activate.ps1
```

### 数据库操作
```powershell
python manage.py migrate           # 执行迁移
python manage.py makemigrations    # 创建迁移
python manage.py createsuperuser   # 创建管理员
```

### 服务控制
```powershell
# MySQL
Get-Service MySQL80
Start-Service MySQL80
Stop-Service MySQL80

# Redis
Get-Service Redis
Start-Service Redis
Stop-Service Redis
```

---

## 🌐 访问地址

- **Web 应用**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **MySQL**: localhost:3306 (bkflow/bkflow123)
- **Redis**: localhost:6379

---

## 📊 资源占用

- **运行时内存**: ~800MB
- **磁盘空间**: ~2GB
- **服务数量**: 3个（Django + 2个Celery）

---

## 🛠️ 故障排查速查

### Django 启动失败
```powershell
python manage.py check
```

### 数据库连接测试
```powershell
mysql -u bkflow -pbkflow123 bkflow
```

### Redis 连接测试
```powershell
redis-cli ping
```

### 查看日志
```powershell
Get-Content .\logs\*.log -Tail 50
```

---

## 🗑️ 快速清理

```powershell
# 1. 停止所有服务（关闭终端）
# 2. 删除数据库
mysql -u root -p -e "DROP DATABASE bkflow;"
# 3. 删除虚拟环境
Remove-Item -Recurse -Force D:\program\env\bkflow_env
```

---

## 📞 获取帮助

- QUICKSTART.md - 完整安装步骤
- DEPLOYMENT.md - 详细部署说明
- CHECKLIST.md - 部署检查清单
