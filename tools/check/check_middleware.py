import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.dev'

# 加载 .env
with open('.env', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip()

os.environ['BKFLOW_MODULE_TYPE'] = 'interface'

import django
django.setup()

from django.conf import settings
from rest_framework.authentication import SessionAuthentication

print("MIDDLEWARE:")
for i, m in enumerate(settings.MIDDLEWARE):
    marker = " <-- DEBUG" if 'CSRFDebug' in m else ""
    print(f"  {i+1}. {m}{marker}")

print(f"\nHas CsrfViewMiddleware: {any('CsrfViewMiddleware' in m for m in settings.MIDDLEWARE)}")
print(f"Has CSRFDebugMiddleware: {any('CSRFDebug' in m for m in settings.MIDDLEWARE)}")
print(f"\nSessionAuthentication class: {SessionAuthentication}")
print(f"SessionAuthentication module: {SessionAuthentication.__module__}")


