# -*- coding: utf-8 -*-
"""检查 ModuleInfo 详细配置"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from bkflow.space.models import ModuleInfo

print("=" * 60)
print("ModuleInfo 配置详情")
print("=" * 60)

all_modules = ModuleInfo.objects.all()
if not all_modules:
    print("❌ 没有找到任何 ModuleInfo 记录！")
else:
    for module in all_modules:
        print(f"\nID: {module.id}")
        print(f"类型: {module.type}")
        print(f"Space ID: {module.space_id}")
        print(f"URL: {module.url!r}")
        print(f"Token: {module.token!r}")
        print("-" * 60)

print("\n" + "=" * 60)
print("检查 space_id=1 的配置")
print("=" * 60)

interface_for_space1 = ModuleInfo.objects.filter(type='INTERFACE', space_id=1).first()
if interface_for_space1:
    print(f"✓ 找到 Interface (space_id=1): {interface_for_space1.url}")
else:
    print("❌ 没有找到 space_id=1 的 Interface 配置")

# 检查通用配置 (space_id=0)
interface_for_space0 = ModuleInfo.objects.filter(type='INTERFACE', space_id=0).first()
if interface_for_space0:
    print(f"✓ 找到 Interface (space_id=0): {interface_for_space0.url}")
else:
    print("❌ 没有找到 space_id=0 的 Interface 配置")
