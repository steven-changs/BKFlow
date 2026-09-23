# -*- coding: utf-8 -*-
"""检查任务执行状态"""
import os
import django

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
os.environ.setdefault('BKFLOW_MODULE_TYPE', 'engine')
django.setup()

from bkflow.task.models import TaskInstance

print("=" * 60)
print("任务状态查询")
print("=" * 60)

task = TaskInstance.objects.filter(id=3).first()
if task:
    print(f"任务ID: {task.id}")
    print(f"任务名称: {task.name}")
    print(f"已启动: {task.is_started}")
    print(f"已完成: {task.is_finished}")
    print(f"开始时间: {task.start_time}")
    print(f"完成时间: {task.finish_time}")
    print(f"执行人: {task.executor}")
    print(f"Pipeline 实例ID: {task.instance_id}")
else:
    print("任务不存在")

# 查看所有任务
print("\n" + "=" * 60)
print("所有任务列表")
print("=" * 60)
all_tasks = TaskInstance.objects.all().order_by('-id')[:5]
for t in all_tasks:
    status = "已完成" if t.is_finished else ("执行中" if t.is_started else "未启动")
    print(f"ID: {t.id} | 名称: {t.name} | 状态: {status}")
