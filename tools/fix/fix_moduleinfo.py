#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ModuleInfo URL 配置"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from bkflow.admin.models import ModuleInfo

print("=== Updating ModuleInfo ===")

# 查找现有记录
module = ModuleInfo.objects.filter(space_id=1).first()

if not module:
    print("Error: No ModuleInfo found for space_id=1")
    print("Please run create_moduleinfo.py first")
    exit(1)

print(f"Current URL: {module.url}")

# 问题分析：
# TaskComponentClient 会调用 {url}/task/
# 但我们的服务是 interface 模块，没有 /task/ 根路由
#
# 解决方案：
# 在本地开发环境中，我们没有单独的 engine 模块
# 需要删除这个 ModuleInfo 记录，或者设置为一个标记值表示不使用

print("\n[INFO] In local development, we don't have a separate engine module.")
print("[INFO] Task admin features require a separate engine deployment.")
print("\nOptions:")
print("1. Delete ModuleInfo (task features will be disabled)")
print("2. Keep ModuleInfo but it will fail (404 errors)")
print("\nFor now, keeping the record. Task list page will show errors.")
print("To use task features, you need to:")
print("1. Start a separate engine instance on another port")
print("2. Update ModuleInfo.url to point to that engine")
