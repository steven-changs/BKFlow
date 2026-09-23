#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 CSRF Token 配置
"""
import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from django.conf import settings

print("=" * 60)
print("CSRF 配置检查")
print("=" * 60)

# 检查关键配置
configs = [
    ('APP_CODE', getattr(settings, 'APP_CODE', 'NOT SET')),
    ('CSRF_COOKIE_NAME', getattr(settings, 'CSRF_COOKIE_NAME', 'NOT SET')),
    ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', 'NOT SET')),
    ('CSRF_COOKIE_HTTPONLY', getattr(settings, 'CSRF_COOKIE_HTTPONLY', 'NOT SET')),
    ('CSRF_COOKIE_SAMESITE', getattr(settings, 'CSRF_COOKIE_SAMESITE', 'NOT SET')),
    ('CSRF_TRUSTED_ORIGINS', getattr(settings, 'CSRF_TRUSTED_ORIGINS', [])),
]

for key, value in configs:
    print(f"{key}: {value}")

print("\n" + "=" * 60)
print("前端期望的 Cookie 名称: bkflow_csrftoken")
print("=" * 60)

# 检查是否匹配
expected = "bkflow_csrftoken"
actual = getattr(settings, 'CSRF_COOKIE_NAME', None)
if actual == expected:
    print("✅ CSRF Cookie 名称配置正确")
else:
    print(f"❌ CSRF Cookie 名称不匹配")
    print(f"   期望: {expected}")
    print(f"   实际: {actual}")
