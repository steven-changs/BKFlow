#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试空间创建"""

import os
import sys
import django
import json

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from django.test import RequestFactory
from bkflow.space.views import SpaceViewSet

# 创建请求工厂
factory = RequestFactory()

# 创建 POST 请求
data = {
    "name": "测试空间",
    "app_code": "bkflow",
    "desc": "本地测试空间"
}

request = factory.post('/api/space/',
                      data=json.dumps(data),
                      content_type='application/json')

# 模拟用户
from django.contrib.auth import get_user_model
User = get_user_model()
admin_user = User.objects.filter(username='admin').first()
request.user = admin_user

# 调用视图
view = SpaceViewSet.as_view({'post': 'create'})
try:
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.data}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
