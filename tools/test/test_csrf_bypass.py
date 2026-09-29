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
from bkflow.disable_csrf import DisableCSRFSessionAuthentication

# 创建一个模拟请求
factory = RequestFactory()
request = factory.post('/test/', data='{}', content_type='application/json')

# 测试 enforce_csrf 方法
auth = DisableCSRFSessionAuthentication()
try:
    result = auth.enforce_csrf(request)
    print(f"[OK] enforce_csrf returned: {result}")
    print(f"[OK] No exception raised - CSRF check is bypassed")
except Exception as e:
    print(f"[ERROR] Exception raised: {type(e).__name__}: {e}")
