# -*- coding: utf-8 -*-
"""检查 Celery Worker 配置"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
os.environ.setdefault('BKFLOW_MODULE_TYPE', 'engine')
django.setup()

from django.conf import settings
from pipeline.celery.settings import CELERY_QUEUES

print("=" * 80)
print("Celery Worker 配置检查")
print("=" * 80)
print(f"\nModule Type: {settings.BKFLOW_MODULE.type}")
print(f"Module Code: {settings.BKFLOW_MODULE.code}")
print(f"\n配置的队列 ({len(CELERY_QUEUES)} 个):")
for i, q in enumerate(CELERY_QUEUES, 1):
    print(f"  {i:2d}. {q.name}")

# 检查是否包含 Bamboo Engine 队列
bamboo_queues = [q.name for q in CELERY_QUEUES if 'er_execute' in q.name or 'er_schedule' in q.name]
print(f"\nBamboo Engine 队列: {len(bamboo_queues)} 个")
for q in bamboo_queues:
    print(f"  - {q}")

if not bamboo_queues:
    print("\n!!! 错误：没有找到 Bamboo Engine 队列 (er_execute, er_schedule)")
    print("!!! 这意味着 Celery Worker 使用了错误的模块类型")
    sys.exit(1)
else:
    print("\n✓ 配置正确")
