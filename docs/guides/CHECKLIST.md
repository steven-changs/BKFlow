# BKFlow 本地部署检查清单

## 📋 部署前检查

### 1. 环境检查
- [x] Python 3.11.15 已安装
- [x] MySQL 8.0 运行中 (localhost:3306)
- [x] Redis 运行中 (localhost:6379)
- [x] 虚拟环境已创建 (D:\program\env\bkflow_env)
- [ ] 依赖已安装

### 2. 数据库初始化
```powershell
# 连接 MySQL
mysql -u root -p

# 执行 SQL（或运行脚本文件）
source D:\program\project\BKFlow\scripts\create-database.sql
```

检查项：
- [ ] 数据库 `bkflow` 已创建
- [ ] 用户 `bkflow` 已创建并授权

### 3. Django 数据库迁移
```powershell
cd D:\program\project\BKFlow
.\scripts\init-db.ps1
```

检查项：
- [ ] 数据库迁移成功
- [ ] 超级用户已创建

### 4. 服务启动
```powershell
# 方式1: 一键启动（推荐）
.\scripts\start-all.ps1

# 方式2: 手动启动（分3个终端）
# 终端1
.\scripts\start-local.ps1

# 终端2
.\scripts\start-celery-worker.ps1

# 终端3
.\scripts\start-celery-beat.ps1
```

检查项：
- [ ] Django 服务器启动成功 (http://localhost:8000)
- [ ] Celery Worker 运行正常
- [ ] Celery Beat 运行正常

---

## 🔍 故障排查

### 依赖安装失败

**问题**: 某些包需要 C++ 编译工具
```powershell
# 下载并安装 Visual C++ Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**问题**: django-bkvision 找不到
```text
解决: 已自动跳过（腾讯内部包，不影响核心功能）
```

### 数据库连接失败

**检查 MySQL 服务**
```powershell
Get-Service MySQL80
Start-Service MySQL80
```

**测试连接**
```powershell
mysql -u bkflow -pbkflow123 -h localhost bkflow
```

### Redis 连接失败

**检查 Redis 服务**
```powershell
Get-Service Redis
Start-Service Redis
```

**测试连接**
```powershell
redis-cli ping
# 应该返回 PONG
```

### Django 启动报错

**查看详细错误**
```powershell
cd D:\program\project\BKFlow
& D:\program\env\bkflow_env\Scripts\Activate.ps1
$env:BKPAAS_ENVIRONMENT="dev"
python manage.py check
```

**常见问题**
- 数据库未创建 → 运行 create-database.sql
- 数据库未迁移 → 运行 python manage.py migrate
- 配置文件错误 → 检查 local_settings.py

### Celery 启动失败

**Windows 必须使用 eventlet**
```powershell
pip install eventlet
celery -A bkflow worker -l info -P eventlet
```

**检查 Redis 连接**
```powershell
# 在虚拟环境中
python -c "import redis; r=redis.Redis(host='localhost', port=6379, db=0); print(r.ping())"
```

---

## ✅ 验证部署

### 1. 访问 Web 界面
打开浏览器访问: http://localhost:8000

### 2. 检查管理后台
访问: http://localhost:8000/admin
使用创建的超级用户登录

### 3. 测试 API
```powershell
# 测试健康检查端点（如果有）
curl http://localhost:8000/healthz
```

### 4. 检查日志
```powershell
# Django 日志
Get-Content .\logs\*.log -Tail 50

# Celery 日志
# 查看 Celery 终端输出
```

---

## 📊 资源占用

当前配置预计占用：
- **内存**: ~800MB（运行时）
- **磁盘**: ~2GB（虚拟环境 + 依赖）
- **数据库**: ~100MB（初始）

---

## 🗑️ 清理重新部署

如需重新部署：

### 1. 停止所有服务
关闭所有终端窗口（Django、Celery Worker、Celery Beat）

### 2. 清理数据库
```powershell
mysql -u root -p -e "DROP DATABASE IF EXISTS bkflow; DROP USER IF EXISTS 'bkflow'@'localhost';"
```

### 3. 删除虚拟环境
```powershell
Remove-Item -Recurse -Force D:\program\env\bkflow_env
```

### 4. 重新部署
从步骤 1 重新开始

---

## 📝 日常操作命令

### 激活虚拟环境
```powershell
& D:\program\env\bkflow_env\Scripts\Activate.ps1
```

### 数据库操作
```powershell
# 创建迁移
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# Django Shell
python manage.py shell
```

### 静态文件
```powershell
python manage.py collectstatic
```

### 查看路由
```powershell
python manage.py show_urls
```

---

## 🎯 下一步

部署成功后：
1. 阅读项目文档了解 API 使用
2. 配置蓝鲸平台对接（如需要）
3. 根据业务需求进行定制开发

---

## 📚 相关文件

- `local_settings.py` - 本地配置
- `scripts/` - 各种启动脚本
- `QUICKSTART.md` - 快速开始指南
- `DEPLOYMENT.md` - 详细部署文档
- `README.md` - 项目说明

---

## 联系方式

如有问题：
- 查看蓝鲸官方文档: https://bk.tencent.com/docs/
- GitHub Issues: https://github.com/TencentBlueKing/bkflow/issues
- 蓝鲸论坛: https://bk.tencent.com/s-mart/community
