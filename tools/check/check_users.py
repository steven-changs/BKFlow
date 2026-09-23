#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查数据库中的用户"""

import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
print(f"User model: {User}")
print(f"Total users: {User.objects.count()}")

users = User.objects.all()[:10]
for u in users:
    print(f"  - username={u.username}, superuser={u.is_superuser}, staff={u.is_staff}")

# 检查是否存在 admin 用户
admin_user = User.objects.filter(username='admin').first()
if admin_user:
    print(f"\nAdmin user exists: superuser={admin_user.is_superuser}")
else:
    print("\nNo admin user found. Creating one...")
    admin_user = User.objects.create_superuser(
        username='admin',
        password='admin123',
        is_superuser=True,
        is_staff=True
    )
    print(f"Admin user created: {admin_user.username}")
