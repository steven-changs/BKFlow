#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""BKFlow 模式切换工具"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from bkflow.admin.models import ModuleInfo, ModuleType, IsolationLevel

def enable_engine():
    """启用 Engine 模块（完整模式）"""
    print("=== Enabling Engine Module (Full Mode) ===\n")

    # 检查是否已存在
    existing = ModuleInfo.objects.filter(space_id=1).first()
    if existing:
        print(f"[INFO] ModuleInfo already exists")
        print(f"  Space ID: {existing.space_id}")
        print(f"  URL: {existing.url}")
        print(f"  Token: {existing.token}")

        # 更新 URL 确保指向 Engine
        if existing.url != 'http://localhost:8001':
            existing.url = 'http://localhost:8001'
            existing.save()
            print(f"\n[UPDATED] URL changed to http://localhost:8001")
    else:
        # 创建新记录
        module_info = ModuleInfo.objects.create(
            space_id=1,
            code='default',
            url='http://localhost:8001',  # Engine 运行在 8001
            token='local-dev-token',
            type=ModuleType.TASK.value,
            isolation_level=IsolationLevel.ONLY_CALCULATION.value
        )
        print(f"[CREATED] ModuleInfo record")
        print(f"  ID: {module_info.id}")
        print(f"  Space ID: {module_info.space_id}")
        print(f"  URL: {module_info.url}")

    print("\n[SUCCESS] Engine module enabled")
    print("\nNext steps:")
    print("  1. Make sure Engine is running on port 8001")
    print("  2. Run: .\\scripts\\start-engine.ps1 (if not started)")
    print("  3. Refresh your browser")
    print("\nAll features are now available!")

def disable_engine():
    """禁用 Engine 模块（简化模式）"""
    print("=== Disabling Engine Module (Simple Mode) ===\n")

    deleted_count = ModuleInfo.objects.all().delete()[0]
    print(f"[DELETED] {deleted_count} ModuleInfo record(s)")

    remaining = ModuleInfo.objects.count()
    print(f"[INFO] Remaining records: {remaining}")

    print("\n[SUCCESS] Engine module disabled")
    print("\nResult:")
    print("  Available:")
    print("    - Space management")
    print("    - Template management")
    print("    - Plugin management")
    print("    - Permission management")
    print("  ")
    print("  Unavailable:")
    print("    - Task execution")
    print("    - Task list (will show error)")
    print("\nYou can stop the Engine service on port 8001 (if running)")

def check_mode():
    """检查当前模式"""
    print("=== Current Mode ===\n")

    count = ModuleInfo.objects.count()
    if count == 0:
        print("[MODE] Simple Mode (Engine Disabled)")
        print("  - Only Interface module is needed")
        print("  - Task features are unavailable")
        print("\nTo switch to Full Mode: python switch_mode.py --mode full")
    else:
        module = ModuleInfo.objects.first()
        print("[MODE] Full Mode (Engine Enabled)")
        print(f"  - Engine URL: {module.url}")
        print(f"  - Space ID: {module.space_id}")
        print("  - All features are available")
        print("\nTo switch to Simple Mode: python switch_mode.py --mode simple")

    print(f"\nTotal ModuleInfo records: {count}")

def main():
    if len(sys.argv) < 2:
        print("BKFlow Mode Switcher")
        print("\nUsage:")
        print("  python switch_mode.py --mode simple    # Switch to Simple Mode")
        print("  python switch_mode.py --mode full      # Switch to Full Mode")
        print("  python switch_mode.py --check          # Check current mode")
        print("\nModes:")
        print("  simple - Only Interface module (no task features)")
        print("  full   - Interface + Engine (all features)")
        sys.exit(1)

    command = sys.argv[1]

    if command == '--check':
        check_mode()
    elif command == '--mode':
        if len(sys.argv) < 3:
            print("Error: --mode requires an argument (simple or full)")
            sys.exit(1)

        mode = sys.argv[2].lower()
        if mode == 'simple':
            disable_engine()
        elif mode == 'full':
            enable_engine()
        else:
            print(f"Error: Unknown mode '{mode}'. Use 'simple' or 'full'")
            sys.exit(1)
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == '__main__':
    main()
