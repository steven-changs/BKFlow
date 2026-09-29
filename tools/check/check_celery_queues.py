# -*- coding: utf-8 -*-
"""查看 Celery 队列配置"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
os.environ.setdefault('BKFLOW_MODULE_TYPE', 'engine')
django.setup()

from django.conf import settings
from pipeline.celery.settings import CELERY_QUEUES

print("=" * 60)
print("Celery 队列配置")
print("=" * 60)
print(f"Module Code: {settings.BKFLOW_MODULE.code}")
print(f"Module Type: {settings.BKFLOW_MODULE.type}")
print("")
print("配置的队列列表：")
for q in CELERY_QUEUES:
    print(f"  - {q.name}")
