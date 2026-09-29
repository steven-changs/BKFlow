#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建 ModuleInfo 初始数据"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from bkflow.admin.models import ModuleInfo, ModuleType, IsolationLevel
from django.conf import settings

print("=== Creating ModuleInfo ===")

# 从环境变量或配置获取模块信息
module_type = getattr(settings, 'BKFLOW_MODULE_TYPE', 'interface')
module_code = getattr(settings, 'BKFLOW_MODULE_CODE', 'default')

print(f"Module Type: {module_type}")
print(f"Module Code: {module_code}")

# 检查是否已存在
existing = ModuleInfo.objects.filter(space_id=1).first()
if existing:
    print(f"ModuleInfo already exists: space_id={existing.space_id}, code={existing.code}")
else:
    # 创建新记录
    module_info = ModuleInfo.objects.create(
        space_id=1,  # 空间 ID
        code=module_code,
        url='http://localhost:8000',  # 模块 URL
        token='local-dev-token',  # 模块 token
        type=ModuleType.TASK.value,
        isolation_level=IsolationLevel.ONLY_CALCULATION.value
    )
    print(f"Created ModuleInfo: ID={module_info.id}, Space={module_info.space_id}, Code={module_info.code}")

# 验证
all_modules = ModuleInfo.objects.all()
print(f"\nTotal ModuleInfo records: {all_modules.count()}")
for m in all_modules:
    print(f"  - ID: {m.id}, Space: {m.space_id}, Code: {m.code}, URL: {m.url}")
