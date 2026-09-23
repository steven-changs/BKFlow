# BKFlow 本地部署快速开始

> 针对 Windows 环境，提供本地部署和 Docker 部署两种方案

---

## 📋 前置条件

### 已有资源
✅ MySQL 8.0 - `localhost:3306`  
✅ Redis - `localhost:6379`  
⚠️ Python 3.6.5（需升级到 3.9.12）

---

## 🚀 方案 A：本地环境部署（推荐）

### 步骤 1: 安装 Python 3.9.12

1. 下载：https://www.python.org/downloads/release/python-3912/
2. 安装时勾选 "Add Python to PATH"
3. 验证：`python --version` 或 `py -3.9 --version`

### 步骤 2: 创建虚拟环境

```powershell
# 进入项目目录
cd D:\program\project\BKFlow

# 创建虚拟环境
python -m venv venv_bkflow
# 或使用特定版本
py -3.9 -m venv venv_bkflow

# 激活虚拟环境
.\venv_bkflow\Scripts\Activate.ps1

# 如果遇到执行策略错误
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 步骤 3: 安装依赖

```powershell
# 在激活的虚拟环境中
pip install --upgrade pip
pip install -r requirements.txt

# Windows 下需要额外安装 eventlet（Celery 支持）
pip install eventlet
```

### 步骤 4: 创建数据库

```powershell
# 连接到 MySQL
mysql -u root -p

# 执行以下 SQL
CREATE DATABASE bkflow DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bkflow'@'localhost' IDENTIFIED BY 'bkflow123';
GRANT ALL PRIVILEGES ON bkflow.* TO 'bkflow'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 步骤 5: 初始化数据库

```powershell
# 使用自动化脚本
.\scripts\init-db.ps1
```

### 步骤 6: 启动服务

需要开启 **3 个终端窗口**：

**终端 1 - Django 服务器**
```powershell
.\scripts\start-local.ps1
# 或手动启动
.\venv_bkflow\Scripts\Activate.ps1
$env:BKPAAS_ENVIRONMENT="dev"
python manage.py runserver 0.0.0.0:8000
```

**终端 2 - Celery Worker**
```powershell
.\scripts\start-celery-worker.ps1
# 或手动启动
.\venv_bkflow\Scripts\Activate.ps1
$env:BKPAAS_ENVIRONMENT="dev"
celery -A bkflow worker -l info -P eventlet
```

**终端 3 - Celery Beat**
```powershell
.\scripts\start-celery-beat.ps1
# 或手动启动
.\venv_bkflow\Scripts\Activate.ps1
$env:BKPAAS_ENVIRONMENT="dev"
celery -A bkflow beat -l info
```

### 访问应用

🌐 http://localhost:8000

---

## 🐳 方案 B：Docker 部署（备用）

### 适用场景
- Python 3.9 安装失败
- 依赖安装有问题
- 想要完全隔离的环境
- 需要快速清理重建

### 快速启动

```powershell
# 启动所有服务
.\scripts\docker-manage.ps1 up

# 查看状态
.\scripts\docker-manage.ps1 status

# 查看日志
.\scripts\docker-manage.ps1 logs

# 重启服务
.\scripts\docker-manage.ps1 restart

# 停止服务（保留数据）
.\scripts\docker-manage.ps1 down

# 完全清理（删除所有数据）
.\scripts\docker-manage.ps1 clean
```

### 首次初始化

```powershell
# 启动服务
docker-compose up -d

# 进入应用容器
docker-compose exec app bash

# 创建超级用户
python manage.py createsuperuser

# 退出容器
exit
```

### 访问应用

🌐 http://localhost:8000

### Docker 服务说明

| 服务 | 容器名 | 端口映射 | 说明 |
|------|--------|----------|------|
| MySQL | bkflow_mysql | 3307→3306 | 数据库（避免冲突用 3307） |
| Redis | bkflow_redis | 6380→6379 | 缓存（避免冲突用 6380） |
| Django | bkflow_app | 8000→8000 | Web 应用 |
| Celery Worker | bkflow_celery_worker | - | 异步任务 |
| Celery Beat | bkflow_celery_beat | - | 定时任务 |

---

## 🔍 环境标识对比

### 本地部署
- 📁 虚拟环境：`venv_bkflow/`
- ⚙️ 配置文件：`local_settings.py`
- 🗄️ 数据库：本地 MySQL `bkflow`
- 🔴 Redis：本地 Redis DB 0
- 🔌 端口：MySQL 3306, Redis 6379

### Docker 部署
- 🐳 容器前缀：`bkflow_*`
- ⚙️ 配置文件：`docker_settings.py`
- 🗄️ 数据库：容器 `bkflow_mysql`
- 🔴 Redis：容器 `bkflow_redis`
- 🔌 端口：MySQL 3307, Redis 6380（避免冲突）
- 💾 数据卷：`bkflow_mysql_data`, `bkflow_redis_data`

---

## ⚠️ 常见问题

### 本地部署问题

**1. Python 版本冲突**
```powershell
# 使用 py launcher 指定版本
py -3.9 -m venv venv_bkflow
```

**2. 依赖安装失败（需要 C++ 编译工具）**
- 下载安装：https://visualstudio.microsoft.com/visual-cpp-build-tools/
- 勾选 "Desktop development with C++"

**3. Celery 启动失败**
```powershell
# Windows 必须使用 eventlet pool
pip install eventlet
celery -A bkflow worker -l info -P eventlet
```

**4. MySQL 连接失败**
```powershell
# 检查服务状态
Get-Service MySQL80

# 启动服务
Start-Service MySQL80

# 检查端口
netstat -ano | Select-String 3306
```

**5. Redis 连接失败**
```powershell
# 检查服务状态
Get-Service Redis

# 启动服务
Start-Service Redis
```

### Docker 部署问题

**1. Docker Desktop 未启动**
- 启动 Docker Desktop 并等待完全启动

**2. 端口冲突**
- Docker 配置已使用 3307/6380 避免与本地冲突
- 如仍有冲突，修改 `docker-compose.yml` 中的端口映射

**3. 磁盘空间不足**
```powershell
# 清理未使用资源
docker system prune -a --volumes

# 查看占用
docker system df
```

**4. 容器启动失败**
```powershell
# 查看具体错误
docker-compose logs app
docker-compose logs mysql
```

---

## 📝 日常操作

### 本地环境

```powershell
# 激活环境
.\venv_bkflow\Scripts\Activate.ps1

# 数据库迁移
python manage.py migrate

# 创建迁移文件
python manage.py makemigrations

# 收集静态文件
python manage.py collectstatic

# Django Shell
python manage.py shell

# 停用环境
deactivate
```

### Docker 环境

```powershell
# 进入应用容器
docker-compose exec app bash

# 查看日志
docker-compose logs -f app

# 重启单个服务
docker-compose restart app

# 查看资源占用
docker stats
```

---

## 🗑️ 清理重新部署

### 本地环境

```powershell
# 1. 停止所有服务（Ctrl+C）

# 2. 删除虚拟环境
Remove-Item -Recurse -Force .\venv_bkflow

# 3. 删除数据库
mysql -u root -p -e "DROP DATABASE IF EXISTS bkflow;"

# 4. 重新开始部署
# 从步骤 2 重新执行
```

### Docker 环境

```powershell
# 完全清理（一键删除所有容器、镜像、数据）
.\scripts\docker-manage.ps1 clean

# 或手动执行
docker-compose down -v --rmi all

# 重新部署
docker-compose up -d
```

---

## 💡 推荐工作流

### 首次部署
1. ✅ 优先尝试 **本地部署**（更快、更省资源）
2. ❌ 如果遇到问题，切换到 **Docker 部署**

### 日常开发
- 使用 **本地部署**（代码修改即时生效）

### 测试/演示
- 使用 **Docker 部署**（环境一致性）

### 快速清理
- **本地**：删除虚拟环境和数据库
- **Docker**：`docker-compose down -v --rmi all`

---

## 📊 资源占用参考

### 本地部署（运行时）
- 内存：~800MB（Django + Celery）
- 磁盘：~2GB（虚拟环境 + 依赖）

### Docker 部署（运行时）
- 内存：~1.5GB（所有容器）
- 磁盘：~5GB（镜像 + 数据）

### Docker 部署（停止时）
- 内存：0MB（不占用）
- 磁盘：~5GB（仍占用）

---

## 📚 相关文档

- 详细部署说明：`DEPLOYMENT.md`
- 配置文件：
  - 本地：`local_settings.py`
  - Docker：`docker_settings.py`
- Docker 配置：`docker-compose.yml`

---

## 🆘 获取帮助

如有问题：
1. 查看 `DEPLOYMENT.md` 详细文档
2. 查看项目 README.md
3. 查看蓝鲸官方文档：https://bk.tencent.com/docs/
