# BKFlow 本地开发环境变量配置
# 使用方法: 在启动前 source 此文件或手动设置这些环境变量

# ============================================
# 基础配置
# ============================================
$env:BKPAAS_ENVIRONMENT = "dev"
$env:BK_ENV = "development"

# ============================================
# 应用基本信息
# ============================================
$env:APP_ID = "bkflow"
$env:APP_CODE = "bkflow"
$env:BKPAAS_APP_ID = "bkflow"
$env:BKPAAS_APP_SECRET = "bkflow-local-dev-secret-12345678"
$env:APP_TOKEN = "bkflow-local-dev-token-12345678"
$env:SECRET_KEY = "bkflow-local-dev-secret-key-change-in-production"
$env:BKPAAS_MAJOR_VERSION = "3"

# ============================================
# 数据库配置
# ============================================
$env:DB_PREFIX = "MYSQL_NAME"
$env:MYSQL_NAME = "bkflow"
$env:MYSQL_USER = "bkflow"
$env:MYSQL_PASSWORD = "bkflow123"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_PORT = "3306"

# ============================================
# Redis 配置
# ============================================
$env:REDIS_HOST = "localhost"
$env:REDIS_PORT = "6379"
$env:REDIS_DB = "0"
$env:REDIS_PASSWORD = ""

# ============================================
# 蓝鲸平台相关（本地开发模拟）
# ============================================
$env:BK_PAAS_HOST = "http://localhost:8000"
$env:BK_PAAS_INNER_HOST = "http://localhost:8000"
$env:BK_PAAS2_URL = "http://localhost:8000"
$env:BKPAAS_DOMAIN = "localhost"
$env:BKPAAS_BK_DOMAIN = "localhost"
$env:BKPAAS_ENGINE_REGION = "default"
$env:BK_COMPONENT_API_URL = "http://localhost:8000/api"
$env:BK_PAAS_ESB_HOST = "http://localhost:8000/api"
$env:BK_API_URL_TMPL = "http://localhost:8000/api/{api_name}/"
$env:BK_APIGW_NAME = "bkflow"

# API Gateway 配置（本地开发跳过校验）
$env:BK_APIGW_NETLOC_PATTERN = "^(?P<api_name>[\w-]+)\.localhost"
$env:SKIP_APIGW_CHECK = "True"
$env:BK_APIGW_REQUIRE_EXEMPT = "True"

# ============================================
# 多租户模式（本地开发关闭）
# ============================================
$env:BKPAAS_MULTI_TENANT_MODE = "false"
$env:ENABLE_MULTI_TENANT_MODE = "false"

# ============================================
# 调试相关
# ============================================
$env:ENABLE_DEBUG_LOG = "1"
$env:DEBUG = "True"

# ============================================
# Celery 配置
# ============================================
$env:BK_CELERYD_CONCURRENCY = "2"
$env:CELERY_SEND_EVENTS = "False"

# ============================================
# 其他配置
# ============================================
$env:APP_INTERNAL_VALIDATION_SKIP = "True"
$env:APP_INTERNAL_TOKEN = "local-dev-token"
$env:BKFLOW_MODULE_TYPE = "interface"
$env:BKFLOW_MODULE_CODE = "default"
$env:RUN_VER = "open"

Write-Host "Environment variables set successfully" -ForegroundColor Green
