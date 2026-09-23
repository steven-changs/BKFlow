#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查 BKFlow 服务状态"""

import socket
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from bkflow.admin.models import ModuleInfo

def check_port(host, port, service_name):
    """检查端口是否开放"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()

    if result == 0:
        print(f"  [{service_name}] Running on {host}:{port}")
        return True
    else:
        print(f"  [{service_name}] NOT running on {host}:{port}")
        return False

def check_services():
    """检查所有服务状态"""
    print("=" * 50)
    print("BKFlow Services Status")
    print("=" * 50)
    print()

    # 检查各个服务
    services = {
        'Interface': ('localhost', 8000),
        'Engine': ('localhost', 8001),
        'Frontend': ('localhost', 9007),
        'MySQL': ('localhost', 3306),
        'Redis': ('localhost', 6379),
    }

    status = {}
    for name, (host, port) in services.items():
        status[name] = check_port(host, port, name)

    print()
    print("-" * 50)

    # 检查模式
    module_count = ModuleInfo.objects.count()
    if module_count == 0:
        print("Current Mode: Simple Mode (Engine Disabled)")
        print()
        print("Expected services:")
        print("  - Interface (8000): Required")
        print("  - Frontend (9007): Required")
        print("  - Engine (8001): Not needed")
    else:
        module = ModuleInfo.objects.first()
        print(f"Current Mode: Full Mode (Engine Enabled)")
        print(f"Engine URL: {module.url}")
        print()
        print("Expected services:")
        print("  - Interface (8000): Required")
        print("  - Engine (8001): Required")
        print("  - Frontend (9007): Required")

    print()
    print("-" * 50)
    print()

    # 总结
    required_simple = ['Interface', 'Frontend']
    required_full = ['Interface', 'Engine', 'Frontend']

    if module_count == 0:
        # 简化模式
        all_running = all(status.get(s, False) for s in required_simple)
        if all_running:
            print("Status: All required services are running")
        else:
            print("Status: Some services are missing")
            for s in required_simple:
                if not status.get(s, False):
                    print(f"  - {s} is not running")
    else:
        # 完整模式
        all_running = all(status.get(s, False) for s in required_full)
        if all_running:
            print("Status: All required services are running")
        else:
            print("Status: Some services are missing")
            for s in required_full:
                if not status.get(s, False):
                    print(f"  - {s} is not running")

    print()
    print("=" * 50)

if __name__ == '__main__':
    check_services()
