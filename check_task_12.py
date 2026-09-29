"""
检查任务状态脚本
"""
import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.default')
django.setup()

from bkflow.task.models import TaskInfo

# 查询任务 12
task_id = 12
try:
    task = TaskInfo.objects.get(id=task_id)
    print(f"\n任务 #{task_id} 信息：")
    print("="*60)
    print(f"任务名称: {task.name}")
    print(f"流程模板: {task.template.name if task.template else 'N/A'}")
    print(f"创建时间: {task.create_time}")
    print(f"开始时间: {task.start_time}")
    print(f"完成时间: {task.finish_time}")
    print(f"执行人: {task.executor}")
    print(f"是否完成: {task.is_finished}")
    print(f"是否启动: {task.is_started}")
    print(f"是否删除: {task.is_deleted}")
    print("="*60)

    if task.is_finished:
        print("✅ 任务已完成")
        print(f"完成时间: {task.finish_time}")
        print("\n如果配置了回调，应该已经触发。")
        print("请检查:")
        print("1. 回调服务是否收到数据: http://localhost:5000")
        print("2. BKFlow 回调记录表格中是否有记录")
    else:
        print("⏳ 任务还在执行中")
        print(f"开始时间: {task.start_time}")
        print("\n需要等待任务执行完成才会触发回调。")

except TaskInfo.DoesNotExist:
    print(f"❌ 任务 #{task_id} 不存在")
except Exception as e:
    print(f"❌ 查询失败: {e}")
