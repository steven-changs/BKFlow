# BKFlow 本地开发环境配置总结

## 项目概述
BKFlow 是基于腾讯蓝鲸（BlueKing）PaaS 平台的流程管理系统，使用 Django + Vue.js 架构。

## 当前状态 ✅

### 服务运行状态
- **后端服务**: http://localhost:8000 (Django) - 正常运行
- **前端服务**: http://localhost:9007 (Vue.js) - 正常运行
- **数据库**: MySQL (localhost:3306/bkflow) - 已配置
- **Redis**: localhost:6379 - 已配置

### 登录方式
**手动登录**: 访问 http://localhost:8000/login/plain/ 可以自动设置 admin 用户的 session，然后重定向到首页。

## 技术栈
- **后端**: Django 3.x + Python 3.11.15
- **前端**: Vue.js (开发服务器运行在 9007 端口)
- **数据库**: MySQL 8.0
- **缓存**: Redis
- **Python 环境**: D:\program\env\bkflow_env (系统级虚拟环境)

## 关键配置文件

### 1. `.env` - 环境变量配置
位置: `D:\program\project\BKFlow\.env`

```bash
# 基础配置
BKPAAS_ENVIRONMENT=dev
BK_ENV=development
APP_ID=bkflow
APP_CODE=bkflow
BKPAAS_APP_ID=bkflow
BKPAAS_APP_SECRET=bkflow-local-dev-secret-12345678
APP_TOKEN=bkflow-local-dev-token-12345678
SECRET_KEY=bkflow-local-dev-secret-key-change-in-production
BKPAAS_MAJOR_VERSION=3

# 数据库配置
DB_PREFIX=MYSQL_NAME
MYSQL_NAME=bkflow
MYSQL_USER=bkflow
MYSQL_PASSWORD=bkflow123
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# 服务地址
BK_PAAS_HOST=http://localhost:8000
BK_PAAS_INNER_HOST=http://localhost:8000
BK_PAAS2_URL=http://localhost:8000
BKPAAS_DOMAIN=localhost
BKPAAS_BK_DOMAIN=localhost
BKPAAS_ENGINE_REGION=ieod
BK_COMPONENT_API_URL=http://localhost:8000/api
BK_PAAS_ESB_HOST=http://localhost:8000/api
BK_API_URL_TMPL=http://localhost:8000/api/{api_name}/
BK_APIGW_NAME=bkflow
BK_APIGW_NETLOC_PATTERN=^(?P<api_name>[\w-]+)\.localhost

# 跳过检查
SKIP_APIGW_CHECK=True
BK_APIGW_REQUIRE_EXEMPT=True

# 租户模式
BKPAAS_MULTI_TENANT_MODE=false
ENABLE_MULTI_TENANT_MODE=false

# 调试配置
ENABLE_DEBUG_LOG=1
DEBUG=True

# Celery 配置
BK_CELERYD_CONCURRENCY=2
CELERY_SEND_EVENTS=False

# 内部验证
APP_INTERNAL_VALIDATION_SKIP=True
APP_INTERNAL_TOKEN=local-dev-token

# 模块配置
BKFLOW_MODULE_TYPE=interface
BKFLOW_MODULE_CODE=default
RUN_VER=open

# 认证配置
BKPAAS_LOGIN_EXEMPT=True
BKAPP_USE_PLAIN_AUTHENTICATION=True
BKPAAS_LOGIN_PLAIN_USERNAME=admin
```

### 2. `local_settings.py` - 本地开发配置
位置: `D:\program\project\BKFlow\local_settings.py`

这个文件提供本地开发的配置覆盖，包括:
- MySQL 数据库连接配置
- Redis 配置
- 自动登录中间件（尝试但未成功）
- 基础环境变量（ENVIRONMENT, RUN_VER, INIT_SUPERUSER）

**重要**: 已添加到 `.gitignore`，不会提交到代码库。

### 3. `bkflow/mock_login.py` - 登录视图
位置: `D:\program\project\BKFlow\bkflow\mock_login.py`

提供两个登录端点:
- `/login/plain/` - 设置 session 后重定向到首页
- `/auto-login/` - 返回 JSON 响应的自动登录 API

### 4. `bkflow/urls.py` - URL 路由
在主 urlpatterns 之前添加了免登录路由:
```python
url(r'^login/plain/', plain_login_view, name='plain_login'),
url(r'^auto-login/', auto_login_view, name='auto_login'),
```

### 5. `config/dev.py` - 开发环境配置
在文件末尾尝试添加自动登录中间件（但由于框架复杂性未生效）。

## 启动服务

### 方法 1: PowerShell 手动启动

**启动后端**:
```powershell
# 加载环境变量并启动 Django
Get-Content .env | ForEach-Object { 
    if ($_ -match '^([^=]+)=(.*)$') { 
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') 
    } 
}
$env:DJANGO_SETTINGS_MODULE='config.dev'
python manage.py runserver 0.0.0.0:8000 --noreload
```

**启动前端** (新建终端):
```powershell
cd frontend
npm run dev
```

### 方法 2: 使用 PowerShell 脚本
已创建的脚本文件（在 `scripts/` 目录下）:
- `start-local.ps1` - 启动后端的脚本
- `start-frontend.ps1` - 启动前端的脚本
- `start-all.ps1` - 同时启动前后端

### 检查服务状态
```powershell
# 查看端口监听状态
Get-NetTCPConnection -LocalPort 8000,9007 -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,State,OwningProcess

# 查看进程
Get-Process | Where-Object {$_.ProcessName -match "python|node"}
```

## 已解决的问题

### 1. 缺失 mysqlclient 模块
**问题**: `ModuleNotFoundError: No module named 'MySQLdb'`
**解决**: 
```powershell
D:\program\env\bkflow_env\Scripts\pip.exe install mysqlclient
```

### 2. 缺失 ENVIRONMENT 配置
**问题**: `AttributeError: 'Settings' object has no attribute 'ENVIRONMENT'`
**解决**: 在 `local_settings.py` 中添加 `ENVIRONMENT = "dev"`

### 3. Windows 控制台编码问题
**问题**: `UnicodeEncodeError: 'gbk' codec can't encode character`
**解决**: 将 Unicode 字符（✓ ✗）替换为 ASCII 字符（[OK] [WARN]）

### 4. 环境变量未加载
**问题**: 启动时提示配置项为 None
**解决**: 启动前先加载 `.env` 文件中的环境变量

## 未解决的问题（需要手动登录）

### 自动登录中间件无效
**问题**: 尽管尝试多次配置自动登录中间件，BlueKing 框架的认证系统仍会将所有请求重定向到登录页。

**原因**:
1. BlueKing 框架的多层认证机制（bk_token、LoginRequiredMiddleware、ConfFixture）
2. 中间件加载顺序问题
3. 框架的认证中间件优先级高于自定义中间件

**当前解决方案**:
使用手动登录 - 访问 http://localhost:8000/login/plain/ 一次后，session 会保持，可以正常使用系统。

## 数据库信息

### MySQL 配置
- **主机**: localhost
- **端口**: 3306
- **数据库名**: bkflow
- **用户名**: bkflow
- **密码**: bkflow123

### 管理员账号
- **用户名**: admin
- **密码**: (需要在数据库中查看或重置)

### 初始化数据库
```powershell
# 迁移数据库
python manage.py migrate

# 创建超级用户（如果需要）
python manage.py createsuperuser
```

## 前端配置

### 前端开发服务器
- **端口**: 9007
- **启动命令**: `npm run dev` (在 frontend 目录下)
- **后端 API 代理**: 配置在 `frontend/vue.config.js` 或类似配置文件中

## 相关文档
项目中已创建的文档:
- `LOGIN_GUIDE.md` - 详细的登录问题排查指南
- `DEPLOYMENT.md` - 部署相关文档
- `QUICKSTART.md` - 快速开始指南
- `REFERENCE.md` - 参考文档

## Git 状态
```
当前分支: master
主分支: master
Git 用户: gys_stevenchangs_pmc

修改的文件:
M .gitignore
M bkflow/urls.py
M config/dev.py

未跟踪的文件:
?? bkflow/mock_login.py
?? local_settings.py
?? 多个文档和脚本文件
```

## 下一步可选任务

1. **实现前端自动登录** (可选)
   - 在前端应用启动时自动调用 `/login/plain/` 或 `/auto-login/`
   - 只在本地开发模式下启用
   - 需要修改前端入口文件（如 `frontend/src/main.js`）

2. **优化启动脚本** (可选)
   - 改进 PowerShell 启动脚本
   - 添加服务健康检查
   - 自动打开浏览器

3. **探索替代认证方案** (可选)
   - 研究 BlueKing 框架的认证后端替换
   - 修改框架源码禁用开发模式的认证检查

## 快速开始（新会话使用）

1. **确认服务是否运行**:
   ```powershell
   Get-NetTCPConnection -LocalPort 8000,9007 -ErrorAction SilentlyContinue
   ```

2. **如果服务未运行，启动服务**:
   ```powershell
   # 启动后端
   Get-Content .env | ForEach-Object { if ($_ -match '^([^=]+)=(.*)$') { [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') } }; $env:DJANGO_SETTINGS_MODULE='config.dev'; python manage.py runserver 0.0.0.0:8000 --noreload
   
   # 新终端启动前端
   cd frontend; npm run dev
   ```

3. **访问应用**:
   - 前端: http://localhost:9007
   - 后端: http://localhost:8000
   - 登录: http://localhost:8000/login/plain/

## 重要提示

1. **Python 环境**: 使用系统级虚拟环境 `D:\program\env\bkflow_env`，不是项目内的 venv
2. **环境变量**: 必须在启动 Django 前加载 `.env` 文件
3. **登录机制**: 当前需要手动访问 `/login/plain/` 进行登录
4. **配置文件**: `local_settings.py` 已添加到 `.gitignore`，不会提交
5. **端口占用**: 确保 8000 和 9007 端口没有被其他进程占用

## 联系和参考
- 项目目录: `D:\program\project\BKFlow`
- Python 环境: `D:\program\env\bkflow_env`
- 操作系统: Windows 11 Pro
- Shell: PowerShell (主要) / Git Bash (辅助)
