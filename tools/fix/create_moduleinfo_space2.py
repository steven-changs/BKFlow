#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为 Space 2 创建 ModuleInfo"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from bkflow.admin.models import ModuleInfo, ModuleType, IsolationLevel

print("=== Creating ModuleInfo for Space 2 ===\n")

# 检查是否已存在
existing = ModuleInfo.objects.filter(space_id=2).first()
if existing:
    print(f"[INFO] ModuleInfo for Space 2 already exists")
    print(f"  Space ID: {existing.space_id}")
    print(f"  URL: {existing.url}")
else:
    # 创建新记录
    module_info = ModuleInfo.objects.create(
        space_id=2,
        code='default',
        url='http://localhost:8001',  # Engine 运行在 8001
        token='local-dev-token',
        type=ModuleType.TASK.value,
        isolation_level=IsolationLevel.ONLY_CALCULATION.value
    )
    print(f"[CREATED] ModuleInfo for Space 2")
    print(f"  ID: {module_info.id}")
    print(f"  Space ID: {module_info.space_id}")
    print(f"  URL: {module_info.url}")

# 显示所有记录
print("\n=== All ModuleInfo Records ===")
all_modules = ModuleInfo.objects.all()
for m in all_modules:
    print(f"  - ID: {m.id}, Space: {m.space_id}, URL: {m.url}")

print(f"\nTotal: {all_modules.count()} records")
