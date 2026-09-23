#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试 CSRF 完整流程"""

import requests

# 创建 session 以保持 cookie
session = requests.Session()

# 第1步：访问一个页面以获取 CSRF cookie
print("第1步：获取 CSRF cookie...")
response = session.get('http://localhost:8000/is_admin_user/')
print(f"Status: {response.status_code}")
print(f"Cookies: {session.cookies.get_dict()}")

# 第2步：从 cookie 中获取 CSRF token
csrf_token = session.cookies.get('bkflow_csrftoken')
print(f"\nCSRF Token: {csrf_token}")

if not csrf_token:
    print("错误：没有获取到 CSRF cookie！")
    exit(1)

# 第3步：使用 CSRF token 发送 POST 请求
print("\n第3步：测试创建空间...")
headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrf_token,
    'Referer': 'http://localhost:8000/',
}

data = {
    "name": "测试空间",
    "app_code": "bkflow",
    "desc": "测试描述"
}

response = session.post(
    'http://localhost:8000/api/space/',
    json=data,
    headers=headers
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code == 200:
    print("\n✅ 成功！CSRF 验证通过")
else:
    print("\n❌ 失败")
