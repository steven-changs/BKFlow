#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""禁用任务模块功能"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from bkflow.admin.models import ModuleInfo

print("=== Disabling Task Module ===")

# 删除所有 ModuleInfo 记录
deleted_count = ModuleInfo.objects.all().delete()[0]

print(f"Deleted {deleted_count} ModuleInfo record(s)")

# 验证
remaining = ModuleInfo.objects.count()
print(f"Remaining ModuleInfo records: {remaining}")

if remaining == 0:
    print("\n[SUCCESS] Task module disabled")
    print("\nResult:")
    print("  - Space management: Available")
    print("  - Template management: Available")
    print("  - Plugin management: Available")
    print("  - Task management: Disabled (will show 'ModuleInfo does not exist' error)")
    print("\nTo re-enable task features, you need to:")
    print("  1. Start a separate engine instance")
    print("  2. Run create_moduleinfo.py with correct engine URL")
else:
    print(f"\n[WARNING] Still have {remaining} records")
