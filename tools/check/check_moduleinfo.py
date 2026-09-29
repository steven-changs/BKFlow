#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查 ModuleInfo 数据"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from bkflow.admin.models import ModuleInfo

print("=== ModuleInfo 记录 ===")
modules = ModuleInfo.objects.all()
print(f"总数: {modules.count()}")

for m in modules:
    print(f"  - ID: {m.id}, Code: {m.code}, Type: {m.type}")

if modules.count() == 0:
    print("\n❌ 没有 ModuleInfo 记录！")
    print("\n需要创建初始数据。检查是否需要运行数据迁移或初始化脚本。")

    # 检查环境变量
    from django.conf import settings
    print(f"\nBKFLOW_MODULE_TYPE: {getattr(settings, 'BKFLOW_MODULE_TYPE', 'NOT SET')}")
    print(f"BKFLOW_MODULE_CODE: {getattr(settings, 'BKFLOW_MODULE_CODE', 'NOT SET')}")
