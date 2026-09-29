import os
import sys

# 设置环境
with open('.env', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip()

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.dev'
os.environ['BKFLOW_MODULE_TYPE'] = 'interface'

import django
django.setup()

from django.test import RequestFactory
from bkflow.template.views.template import TemplateViewSet

# 创建一个模拟的 POST 请求
factory = RequestFactory()
request = factory.post('/api/template/1/create_mock_task/',
                       data='{"name":"test"}',
                       content_type='application/json')

# 模拟用户
from django.contrib.auth import get_user_model
User = get_user_model()
request.user = User.objects.first() or User(username='admin', bk_username='admin')

# 尝试调用视图
viewset = TemplateViewSet()
viewset.action = 'create_mock_task'
viewset.request = request
viewset.format_kwarg = None

try:
    response = viewset.create_mock_task(request, pk=1)
    print(f"SUCCESS: {response.status_code}")
    print(f"Data: {response.data}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
