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

from rest_framework.settings import api_settings

print("DEFAULT_AUTHENTICATION_CLASSES:")
for cls in api_settings.DEFAULT_AUTHENTICATION_CLASSES:
    print(f"  {cls}")
    print(f"    Module: {cls.__module__}")
    print(f"    Class: {cls.__name__}")
