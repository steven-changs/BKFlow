# BKFlow 本地开发环境配置完整指南

## 📋 目录
1. [环境变量详解](#环境变量详解)
2. [本地开发 vs 真实环境](#本地开发-vs-真实环境)
3. [部署检查清单](#部署检查清单)
4. [常见问题和解决方案](#常见问题和解决方案)
5. [开发最佳实践](#开发最佳实践)

---

## 1. 环境变量详解

### 当前 .env 文件中的 URL 说明

```bash
# 这些 URL 目前都指向本地，是模拟值
BK_PAAS_HOST=http://localhost:8000          # 蓝鲸 PaaS 平台地址（模拟）
BK_COMPONENT_API_URL=http://localhost:8000/api  # 组件 API 地址（模拟）
BK_API_URL_TMPL=http://localhost:8000/api/{api_name}/  # API 模板（模拟）
```

### ❓ 问题：这些 URL 需要替换成真实值吗？

**答案取决于你的开发场景：**

### 场景 A：纯本地开发（当前配置）✅
**适用情况：**
- 只是学习 BKFlow 的功能
- 开发自定义流程和插件
- 测试流程引擎逻辑
- 不需要调用蓝鲸平台的其他服务

**当前配置：完全适用**
- 所有 URL 指向 localhost
- BKFlow 可以独立运行
- 不依赖外部蓝鲸平台

**限制：**
- ❌ 无法调用真实的蓝鲸 API（如 CMDB、作业平台）
- ❌ 无法使用蓝鲸插件（需要真实的插件服务）
- ❌ 无法使用蓝鲸统一登录
- ❌ 无法发送蓝鲸通知

### 场景 B：连接真实蓝鲸环境 🔗
**适用情况：**
- 需要调用蓝鲸平台的 API
- 需要使用蓝鲸插件（CMDB、作业平台等）
- 需要测试与蓝鲸平台的集成
- 开发生产环境的流程

**需要修改的配置：**

```bash
# .env.blueking (连接真实蓝鲸环境的配置)

# ============================================
# 真实蓝鲸平台地址（需要从你的蓝鲸管理员获取）
# ============================================
BK_PAAS_HOST=http://paas.your-company.com           # 蓝鲸 PaaS 平台地址
BK_PAAS_INNER_HOST=http://paas.your-company.com     # 内网地址
BK_COMPONENT_API_URL=http://paas.your-company.com/api/c/compapi/v2/  # 组件 API

# 蓝鲸应用认证信息（需要在蓝鲸开发者中心创建应用）
BKPAAS_APP_ID=your-app-id              # 你的应用 ID
BKPAAS_APP_SECRET=your-app-secret      # 你的应用密钥
APP_TOKEN=your-app-token               # 应用 Token

# API 网关配置
BK_APIGW_NAME=bkflow
BK_API_URL_TMPL=http://apigw.your-company.com/api/{api_name}/
BK_APIGW_NETLOC_PATTERN=^(?P<api_name>[\w-]+)\.apigw\.your-company\.com

# 其他服务地址
BK_ITSM_API_ENTRY=http://itsm.your-company.com      # ITSM 服务
MEMBER_SELECTOR_DATA_HOST=http://paas.your-company.com/api  # 人员选择器
```

---

## 2. 本地开发 vs 真实环境

### 对比表

| 配置项 | 本地开发（当前） | 连接真实蓝鲸环境 | 生产环境 |
|--------|-----------------|-----------------|----------|
| **数据库** | 本地 MySQL | 本地 MySQL | 独立 MySQL 服务器 |
| **Redis** | 本地 Redis | 本地 Redis | Redis 集群 |
| **蓝鲸 API** | 模拟（localhost） | 真实蓝鲸平台 | 真实蓝鲸平台 |
| **插件调用** | ❌ 不可用 | ✅ 可用 | ✅ 可用 |
| **认证方式** | 跳过验证 | 蓝鲸统一登录 | 蓝鲸统一登录 |
| **适用场景** | 学习、开发流程逻辑 | 集成测试 | 生产运行 |

### 判断标准：我应该用哪种配置？

**使用本地开发配置（当前 .env）如果：**
- ✅ 你还没有蓝鲸平台账号
- ✅ 只是想学习流程引擎的使用
- ✅ 开发不需要调用外部服务的流程
- ✅ 开发自定义节点和插件

**需要连接真实蓝鲸环境如果：**
- ❌ 流程中需要调用 CMDB 获取主机信息
- ❌ 流程中需要执行作业平台任务
- ❌ 需要发送蓝鲸通知
- ❌ 需要使用蓝鲸人员选择器
- ❌ 需要测试与蓝鲸平台的集成

---

## 3. 部署检查清单

### ✅ 基础环境检查

#### 3.1 Python 环境
- [ ] Python 版本 3.11.x ✅
- [ ] 虚拟环境已创建 (`D:\program\env\bkflow_env`) ✅
- [ ] 所有依赖已安装 ✅

**验证命令：**
```powershell
& D:\program\env\bkflow_env\Scripts\Activate.ps1
python --version
pip list | Select-String "Django|celery|redis"
```

#### 3.2 数据库配置
- [ ] MySQL 8.0 已安装并运行 ✅
- [ ] 数据库 `bkflow` 已创建 ✅
- [ ] 用户 `bkflow` 已创建并授权 ✅
- [ ] 数据库迁移已完成 ✅

**验证命令：**
```powershell
# 检查 MySQL 服务
Get-Service MySQL80

# 测试数据库连接
mysql -u bkflow -pbkflow123 -e "SELECT VERSION(); SHOW DATABASES LIKE 'bkflow';"
```

#### 3.3 Redis 配置
- [ ] Redis 已安装并运行 ✅
- [ ] 端口 6379 可访问 ✅

**验证命令：**
```powershell
# 检查 Redis 服务
Get-Service Redis

# 测试 Redis 连接
redis-cli ping
```

#### 3.4 端口占用检查
- [ ] 8000 端口未被占用（Django）
- [ ] 3306 端口未被占用（MySQL）
- [ ] 6379 端口未被占用（Redis）

**验证命令：**
```powershell
# 检查端口占用
netstat -ano | findstr "8000"
netstat -ano | findstr "3306"
netstat -ano | findstr "6379"
```

### ✅ 应用配置检查

#### 3.5 环境变量配置
- [ ] `.env` 文件已创建 ✅
- [ ] 所有必需环境变量已设置 ✅
- [ ] 数据库连接信息正确 ✅
- [ ] Redis 连接信息正确 ✅

**关键环境变量清单：**
```bash
# 必需配置（缺一不可）
BKPAAS_APP_ID=bkflow              # 应用 ID
APP_TOKEN=***                      # 应用 Token
MYSQL_NAME=bkflow                  # 数据库名
MYSQL_USER=bkflow                  # 数据库用户
MYSQL_PASSWORD=bkflow123           # 数据库密码
REDIS_HOST=localhost               # Redis 地址
BKFLOW_MODULE_TYPE=engine          # 模块类型
```

#### 3.6 Django 配置
- [ ] `manage.py check` 无错误 ✅
- [ ] 静态文件目录存在
- [ ] 日志目录有写权限

**验证命令：**
```powershell
cd D:\program\project\BKFlow
& D:\program\env\bkflow_env\Scripts\Activate.ps1
. .\scripts\set-env.ps1
python manage.py check
python manage.py check --deploy  # 生产环境检查
```

### ✅ 功能测试检查

#### 3.7 Django 服务
- [ ] 可以正常启动 ✅
- [ ] 访问 http://localhost:8000 正常
- [ ] 管理后台可访问 http://localhost:8000/bkflow_admin/
- [ ] API 文档可访问 http://localhost:8000/swagger/

#### 3.8 Celery 服务
- [ ] Celery Worker 可以启动 ✅
- [ ] Celery Beat 可以启动 ✅
- [ ] 可以连接到 Redis
- [ ] 任务可以正常执行

**测试 Celery：**
```powershell
# 启动 Worker
celery -A blueapps.core.celery worker -l info -P eventlet

# 在另一个终端测试任务
python manage.py shell
>>> from celery import current_app
>>> current_app.send_task('celery.ping')
```

#### 3.9 数据库功能
- [ ] 可以创建流程模板
- [ ] 可以启动流程实例
- [ ] 数据可以正常保存和查询

---

## 4. 常见问题和解决方案

### 问题 1: 提示缺少环境变量
**症状：**
```
RuntimeError: Environment variable "XXX" not found
```

**解决：**
1. 检查 `.env` 文件是否存在
2. 检查 PyCharm 运行配置是否加载了环境变量
3. 使用 `.\scripts\start-local.ps1` 验证脚本启动是否正常

### 问题 2: 数据库连接失败
**症状：**
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```

**解决：**
```powershell
# 1. 检查 MySQL 服务
Get-Service MySQL80
Start-Service MySQL80

# 2. 测试连接
mysql -u bkflow -pbkflow123 bkflow

# 3. 检查环境变量
echo $env:MYSQL_HOST
echo $env:MYSQL_PORT
```

### 问题 3: Redis 连接失败
**症状：**
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**解决：**
```powershell
# 1. 检查 Redis 服务
Get-Service Redis
Start-Service Redis

# 2. 测试连接
redis-cli ping

# 3. 检查配置
echo $env:REDIS_HOST
echo $env:REDIS_PORT
```

### 问题 4: 端口被占用
**症状：**
```
Error: That port is already in use.
```

**解决：**
```powershell
# 查找占用进程
netstat -ano | findstr "8000"

# 方式1: 停止占用进程
taskkill /PID <进程ID> /F

# 方式2: 使用其他端口
python manage.py runserver 0.0.0.0:8001
```

### 问题 5: Celery 找不到应用
**症状：**
```
Error: Invalid value for '-A': Module 'bkflow' has no attribute 'celery'
```

**解决：**
使用正确的应用名称：
```bash
celery -A blueapps.core.celery worker -l info -P eventlet
```

---

## 5. 开发最佳实践

### 5.1 版本控制

**不要提交到 Git 的文件：**
```gitignore
# 环境变量（包含敏感信息）
.env
*.env
!.env.example

# 数据库
*.db
*.sqlite3
celerybeat-schedule.db

# 日志
logs/
*.log

# PyCharm
.idea/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
```

**应该提交的配置示例：**
```bash
# .env.example（不含敏感信息）
BKPAAS_APP_ID=your-app-id
APP_TOKEN=your-app-token
MYSQL_NAME=bkflow
MYSQL_USER=bkflow
MYSQL_PASSWORD=change-me
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 5.2 多环境配置

创建不同环境的配置文件：

```
.env                    # 默认本地开发（当前配置）
.env.dev               # 本地开发详细配置
.env.test              # 测试环境
.env.blueking          # 连接真实蓝鲸环境
.env.example           # 配置模板（提交到 Git）
```

在 PyCharm 中创建多个运行配置，每个加载不同的 .env 文件。

### 5.3 数据库管理

**定期备份：**
```powershell
# 备份数据库
mysqldump -u bkflow -pbkflow123 bkflow > backup_$(Get-Date -Format 'yyyyMMdd').sql

# 恢复数据库
mysql -u bkflow -pbkflow123 bkflow < backup_20260920.sql
```

**重置数据库：**
```powershell
# 删除所有表
mysql -u root -p123456 -e "DROP DATABASE IF EXISTS bkflow; CREATE DATABASE bkflow DEFAULT CHARACTER SET utf8mb4;"

# 重新迁移
python manage.py migrate

# 重新创建超级用户
python manage.py createsuperuser
```

### 5.4 日志管理

**查看实时日志：**
```powershell
# Django 日志（在运行窗口查看）

# Celery 日志（在运行窗口查看）

# 如果配置了文件日志
Get-Content .\logs\bkflow.log -Tail 100 -Wait
```

### 5.5 开发调试技巧

**1. 使用 Django Debug Toolbar**
```python
# settings.py 已包含调试工具（开发环境）
# 访问页面时可以看到 SQL 查询、模板渲染等信息
```

**2. 使用 PyCharm 断点调试**
- 在代码行号旁点击设置断点
- F9: 设置/取消断点
- F5: 开始调试
- F8: 单步跳过
- F7: 单步进入

**3. 使用 Django Shell**
```powershell
python manage.py shell

>>> from bkflow.task.models import TaskInstance
>>> TaskInstance.objects.all()
```

**4. 查看 SQL 查询**
```python
from django.db import connection
print(connection.queries)
```

---

## 6. 生产环境部署注意事项

### 如果将来需要部署到生产环境，需要修改：

#### 6.1 安全配置
```bash
# .env.production
DEBUG=False                                  # 关闭调试模式
SECRET_KEY=<生成强随机密钥>                  # 使用强密钥
ALLOWED_HOSTS=your-domain.com,your-ip       # 限制允许的域名

# 数据库使用强密码
MYSQL_PASSWORD=<强密码>

# Redis 配置密码
REDIS_PASSWORD=<强密码>
```

#### 6.2 服务器配置
- 使用 Gunicorn 或 uWSGI 代替 `runserver`
- 配置 Nginx 反向代理
- 使用 Supervisor 管理进程
- 配置 HTTPS 证书

#### 6.3 性能优化
- 启用数据库连接池
- 配置 Redis 缓存
- 配置 CDN 加速静态文件
- 增加 Celery Worker 数量

---

## 7. 快速参考

### 常用命令

```powershell
# 启动所有服务
.\scripts\start-all.ps1

# 单独启动服务
.\scripts\start-local.ps1          # Django
.\scripts\start-celery-worker.ps1  # Worker
.\scripts\start-celery-beat.ps1    # Beat

# 数据库操作
python manage.py makemigrations    # 创建迁移
python manage.py migrate           # 执行迁移
python manage.py createsuperuser   # 创建管理员

# 查看信息
python manage.py showmigrations    # 查看迁移状态
python manage.py check             # 检查配置
python manage.py shell             # 进入 Shell
```

### 访问地址

```
主页: http://localhost:8000/
管理后台: http://localhost:8000/bkflow_admin/
任务管理: http://localhost:8000/task/
API 文档: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/
```

### 重要文件位置

```
配置文件: .env
数据库: localhost:3306/bkflow
Redis: localhost:6379
虚拟环境: D:\program\env\bkflow_env
项目目录: D:\program\project\BKFlow
```

---

## 总结

### 当前配置状态 ✅
你的本地开发环境已完全配置好，可以：
- ✅ 独立运行 BKFlow
- ✅ 开发和调试流程
- ✅ 学习流程引擎功能
- ✅ 使用 PyCharm 断点调试

### 配置限制 ⚠️
当前配置不能：
- ❌ 调用真实蓝鲸平台 API
- ❌ 使用蓝鲸插件（CMDB、作业平台等）
- ❌ 使用蓝鲸统一登录

### 下一步建议 📝

**如果只是学习和开发：**
- 当前配置完全够用
- 专注于流程设计和逻辑开发

**如果需要集成蓝鲸平台：**
1. 联系蓝鲸管理员获取平台地址和应用凭证
2. 创建 `.env.blueking` 配置文件
3. 在 PyCharm 中创建新的运行配置加载该文件
4. 测试与蓝鲸平台的连接

**如果需要部署到生产：**
1. 参考"生产环境部署注意事项"章节
2. 使用 Docker 容器化部署（项目已提供 Dockerfile）
3. 配置负载均衡和高可用

需要任何帮助，随时告诉我！
