# -*- coding: utf-8 -*-
"""
本地开发环境：禁用 DRF 的 CSRF 检查
"""
from rest_framework.authentication import SessionAuthentication


class DisableCSRFSessionAuthentication(SessionAuthentication):
    """本地开发环境禁用 CSRF 检查"""
    def enforce_csrf(self, request):
        return  # 跳过 CSRF 检查


# 猴子补丁：替换 DRF 的默认 SessionAuthentication
import rest_framework.authentication
rest_framework.authentication.SessionAuthentication = DisableCSRFSessionAuthentication
