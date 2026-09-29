# -*- coding: utf-8 -*-
"""Celery 诊断脚本"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
os.environ.setdefault('BKFLOW_MODULE_TYPE', 'engine')
django.setup()

from django.conf import settings
from pipeline.celery.settings import CELERY_QUEUES
import redis

print("=" * 80)
print("Celery 诊断信息")
print("=" * 80)

# 1. 模块配置
print(f"\n1. 模块配置:")
print(f"   Module Type: {settings.BKFLOW_MODULE.type}")
print(f"   Module Code: {settings.BKFLOW_MODULE.code}")

# 2. Celery 配置
print(f"\n2. Celery 配置:")
print(f"   Broker URL: {settings.BROKER_URL}")
print(f"   Result Backend: {getattr(settings, 'CELERY_RESULT_BACKEND', 'Not set')}")

# 3. 配置的队列
print(f"\n3. 配置的队列列表 ({len(CELERY_QUEUES)} 个):")
for i, q in enumerate(CELERY_QUEUES, 1):
    print(f"   {i:2d}. {q.name}")

# 4. Redis 队列状态
print(f"\n4. Redis 队列状态:")
r = redis.Redis(host='localhost', port=6379, db=0)
print(f"   Redis 连接: {'OK' if r.ping() else 'Failed'}")

# 检查每个队列的长度
for q in CELERY_QUEUES[:10]:  # 只检查前10个
    queue_name = q.name
    length = r.llen(queue_name)
    if length > 0:
        print(f"   ✓ {queue_name}: {length} 个待处理任务")

# 5. 检查 Bamboo Engine 使用的队列
print(f"\n5. Bamboo Engine 配置:")
from bamboo_engine import api as bamboo_engine_api
from bamboo_engine.eri import ContextValue, ContextValueType
from pipeline.eri.runtime import BambooDjangoRuntime

runtime = BambooDjangoRuntime()
print(f"   Runtime: {type(runtime).__name__}")

# 6. 查看最近的任务
print(f"\n6. 最近的任务:")
from bkflow.task.models import TaskInstance
recent_tasks = TaskInstance.objects.all().order_by('-id')[:3]
for task in recent_tasks:
    status = "已完成" if task.is_finished else ("执行中" if task.is_started else "未启动")
    print(f"   任务 {task.id}: {task.name} - {status}")
    if task.is_started and not task.is_finished:
        print(f"      开始时间: {task.start_time}")
        print(f"      Pipeline ID: {task.instance_id}")

print("\n" + "=" * 80)
