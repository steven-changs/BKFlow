"""
模拟 BKFlow 发送任务完成回调
用于测试回调服务是否正常工作
"""
import requests
import json
from datetime import datetime

# 模拟成功的任务回调
success_callback = {
    "executor": "admin",
    "finish_time": int(datetime.now().timestamp()),
    "outputs": {
        "${_result}": True,
        "${test}": "测试值123"
    },
    "start_time": int(datetime.now().timestamp()) - 300,  # 5分钟前开始
    "task_id": 12,
    "task_name": "流程体验-空间配置_测试任务"
}

# 模拟失败的任务回调
failed_callback = {
    "executor": "admin",
    "extra_data": {
        "failed_message": "节点执行失败：测试错误",
        "failed_node": "n123456789",
        "failed_node_name": "测试节点"
    },
    "finish_time": int(datetime.now().timestamp()),
    "start_time": int(datetime.now().timestamp()) - 200,
    "task_id": 13,
    "task_name": "流程体验-空间配置_失败任务"
}

print("="*60)
print("测试回调服务")
print("="*60)

# 测试成功回调
print("\n[1] 发送成功任务回调...")
try:
    response = requests.post(
        "http://localhost:5000/callback",
        json=success_callback,
        timeout=10
    )
    print(f"[OK] 状态码: {response.status_code}")
    print(f"[OK] 响应: {response.json()}")
except Exception as e:
    print(f"[ERROR] 失败: {e}")

# 测试失败回调
print("\n[2] 发送失败任务回调...")
try:
    response = requests.post(
        "http://localhost:5000/callback",
        json=failed_callback,
        timeout=10
    )
    print(f"[OK] 状态码: {response.status_code}")
    print(f"[OK] 响应: {response.json()}")
except Exception as e:
    print(f"[ERROR] 失败: {e}")

print("\n" + "="*60)
print("测试完成")
print("="*60)
print("\n访问 http://localhost:5000 查看回调记录")
print("应该能看到 2 条新的回调记录（1条成功，1条失败）")
