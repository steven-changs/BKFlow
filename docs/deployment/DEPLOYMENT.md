# BKFlow 本地部署指南

## 当前环境状态

### 已有资源
- **MySQL 8.0**: `localhost:3306` (D:\MySQL\MySQL Server 8.0\)
- **Redis**: `localhost:6379` (C:\Program Files\Redis\)
- **Python**: 3.6.5 (需升级到 3.9.12)

---

## 方案 A：本地环境部署（推荐优先尝试）

### 1. 安装 Python 3.9

下载并安装 Python 3.9.12：
- 官网: https://www.python.org/downloads/release/python-3912/
- 下载 Windows installer (64-bit)
- 安装时勾选 "Add Python to PATH"
- 或安装到自定义目录（如 `D:\Python39`）

验证安装：
```powershell
python --version
# 或如果有多个 Python 版本
py -3.9 --version
```

### 2. 创建虚拟环境

```powershell
cd D:\program\project\BKFlow

# 使用 Python 3.9 创建虚拟环境
python -m venv venv_bkflow
# 或
py -3.9 -m venv venv_bkflow

# 激活虚拟环境
.\venv_bkflow\Scripts\Activate.ps1

# 如果遇到执行策略错误，运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. 安装依赖

```powershell
# 在激活的虚拟环境中
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 配置数据库

```powershell
# 连接到本地 MySQL 创建数据库
mysql -u root -p

# 在 MySQL 中执行：
CREATE DATABASE bkflow DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bkflow'@'localhost' IDENTIFIED BY 'bkflow123';
GRANT ALL PRIVILEGES ON bkflow.* TO 'bkflow'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. 配置环境变量

使用 `.env.local` 文件（已创建，见下文）

### 6. 数据库迁移

```powershell
# 在激活的虚拟环境中
python manage.py migrate
python manage.py createsuperuser
```

### 7. 启动服务

```powershell
# 终端1: Django 开发服务器
python manage.py runserver 0.0.0.0:8000

# 终端2: Celery Worker
celery -A bkflow worker -l info -P eventlet

# 终端3: Celery Beat
celery -A bkflow beat -l info
```

访问: http://localhost:8000

---

## 方案 B：Docker 部署（备用方案）

### 适用场景
- Python 3.9 安装有问题
- 依赖安装失败
- 想要完全隔离的环境
- 需要快速清理重建

### 使用方法

```powershell
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务（不删除数据）
docker-compose stop

# 完全删除重建
docker-compose down -v --rmi all
```

详见 `docker-compose.yml` 和 `Dockerfile`

---

## 区分标识

### 本地部署标识
- 虚拟环境: `venv_bkflow/`
- 配置文件: `.env.local`
- 数据库: `bkflow` (本地 MySQL)
- Redis DB: 0 (本地 Redis)

### Docker 部署标识
- 容器前缀: `bkflow_*`
- 配置文件: `.env.docker`
- 数据库: `bkflow_mysql` 容器
- Redis: `bkflow_redis` 容器
- Volumes: `bkflow_mysql_data`, `bkflow_redis_data`

---

## 故障排查

### 本地部署常见问题

**1. 依赖安装失败**
```powershell
# 某些包可能需要 Visual C++ 编译工具
# 下载安装: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**2. Celery 在 Windows 上问题**
```powershell
# 使用 eventlet 代替默认的 pool
pip install eventlet
celery -A bkflow worker -l info -P eventlet
```

**3. MySQL 连接失败**
- 检查 MySQL 服务是否运行: `Get-Service MySQL80`
- 检查端口: `netstat -ano | Select-String 3306`
- 验证用户权限

**4. Redis 连接失败**
- 检查 Redis 服务: `Get-Service Redis`
- 检查端口: `netstat -ano | Select-String 6379`

### Docker 部署常见问题

**1. 磁盘空间不足**
```powershell
# 清理未使用的资源
docker system prune -a --volumes
```

**2. 容器启动失败**
```powershell
# 查看具体错误
docker-compose logs <service_name>
```

---

## 快速命令参考

### 本地环境
```powershell
# 激活环境
.\venv_bkflow\Scripts\Activate.ps1

# 运行迁移
python manage.py migrate

# 启动服务
python manage.py runserver

# 停用环境
deactivate
```

### Docker 环境
```powershell
# 启动
docker-compose up -d

# 查看状态
docker-compose ps

# 进入容器
docker-compose exec app bash

# 完全清理
docker-compose down -v --rmi all
```
