# BKFlow PyCharm 调试配置指南

## 问题说明
PyCharm 默认不会自动加载 .env 文件，需要手动配置环境变量。

## 解决方案

### 方法1: 使用 EnvFile 插件（推荐）

1. 安装插件：
   - File → Settings → Plugins
   - 搜索 "EnvFile"
   - 安装并重启 PyCharm

2. 配置运行：
   - Edit Configurations
   - 选择你的运行配置
   - 勾选 "Enable EnvFile"
   - 添加 .env 文件路径

### 方法2: 手动添加环境变量

在 PyCharm 运行配置中手动添加环境变量：

**最少必需的环境变量：**
```
BKPAAS_APP_ID=bkflow
APP_TOKEN=bkflow-local-dev-token-12345678
BKPAAS_MAJOR_VERSION=3
BKFLOW_MODULE_TYPE=engine
BK_PAAS2_URL=http://localhost:8000
BKPAAS_BK_DOMAIN=localhost
BK_APIGW_NETLOC_PATTERN=^(?P<api_name>[\w-]+)\.localhost
BKPAAS_ENGINE_REGION=default
BK_COMPONENT_API_URL=http://localhost:8000/api
BK_API_URL_TMPL=http://localhost:8000/api/{api_name}/
SKIP_APIGW_CHECK=True
DB_PREFIX=MYSQL_NAME
MYSQL_NAME=bkflow
MYSQL_USER=bkflow
MYSQL_PASSWORD=bkflow123
MYSQL_HOST=localhost
MYSQL_PORT=3306
REDIS_HOST=localhost
REDIS_PORT=6379
BKPAAS_ENVIRONMENT=dev
```

### 方法3: 快速导入所有变量（最简单）

1. 打开运行配置 (Run → Edit Configurations)
2. 选择 Django Server
3. 找到 "Environment variables" 字段
4. 点击右侧的文件夹图标
5. 点击 "Load from file..."
6. 选择项目根目录的 `.env` 文件
7. 点击 OK

## 详细步骤（方法3）

### Django Server 配置

1. **Run → Edit Configurations → + → Django Server**
2. 配置内容：
   - Name: `Django Server`
   - Host: `0.0.0.0`
   - Port: `8000`
   - Environment variables: 点击 📁 图标 → "Load from file" → 选择 `.env`
   - Python interpreter: `bkflow_env`
   - Working directory: `D:\program\project\BKFlow`

### Celery Worker 配置

1. **Run → Edit Configurations → + → Python**
2. 配置内容：
   - Name: `Celery Worker`
   - Script path: 改为 **Module name**，填入 `celery`
   - Parameters: `-A blueapps.core.celery worker -l info -P eventlet`
   - Environment variables: 从 `.env` 加载
   - Python interpreter: `bkflow_env`
   - Working directory: `D:\program\project\BKFlow`

### Celery Beat 配置

1. **Run → Edit Configurations → + → Python**
2. 配置内容：
   - Name: `Celery Beat`
   - Script path: 改为 **Module name**，填入 `celery`
   - Parameters: `-A blueapps.core.celery beat -l info`
   - Environment variables: 从 `.env` 加载
   - Python interpreter: `bkflow_env`
   - Working directory: `D:\program\project\BKFlow`

## 验证配置

配置完成后，点击运行按钮，如果看到：
```
============================================================
本地开发环境配置已加载
虚拟环境: D:\program\env\bkflow_env
数据库: bkflow@localhost
...
```
说明配置成功！

## 调试快捷键

- **F5**: 开始调试
- **F9**: 设置/取消断点
- **F8**: 单步跳过
- **F7**: 单步进入
- **Shift+F8**: 单步跳出

## 故障排查

如果仍然报错缺少环境变量：
1. 检查 Environment variables 是否正确加载
2. 确认 Python interpreter 是 `bkflow_env`
3. 确认 Working directory 是项目根目录
4. 重启 PyCharm
