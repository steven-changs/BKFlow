# -*- coding: utf-8 -*-
"""
Docker 环境配置
通过环境变量注入配置
"""
import os

# ============================================
# Docker MySQL 配置
# ============================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DATABASE_NAME", "bkflow"),
        "USER": os.getenv("DATABASE_USER", "bkflow"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "bkflow123"),
        "HOST": os.getenv("DATABASE_HOST", "mysql"),
        "PORT": os.getenv("DATABASE_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    },
}

# ============================================
# Docker Redis 配置
# ============================================
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# Celery broker
if REDIS_PASSWORD:
    BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# ============================================
# 开发环境配置
# ============================================
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

print("=" * 60)
print("Docker 环境配置已加载")
print(f"数据库: {DATABASES['default']['NAME']}@{DATABASES['default']['HOST']}")
print(f"Redis: {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
print("=" * 60)
