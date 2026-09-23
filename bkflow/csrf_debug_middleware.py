# -*- coding: utf-8 -*-
"""
调试中间件：记录请求的 CSRF 相关信息并强制跳过 CSRF 检查
"""
import sys


class CSRFDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        sys.stderr.write("[CSRFDebugMiddleware] Initialized\n")
        sys.stderr.flush()

    def __call__(self, request):
        # 对所有请求强制跳过 CSRF 检查
        setattr(request, '_dont_enforce_csrf_checks', True)

        if 'create_mock_task' in request.path or 'api/template' in request.path:
            sys.stderr.write(f"\n[CSRF Debug Middleware] ===== REQUEST START =====\n")
            sys.stderr.write(f"[CSRF Debug Middleware] Path: {request.path}\n")
            sys.stderr.write(f"[CSRF Debug Middleware] Method: {request.method}\n")
            sys.stderr.write(f"[CSRF Debug Middleware] COOKIES: {request.COOKIES}\n")
            sys.stderr.write(f"[CSRF Debug Middleware] X-CSRFTOKEN: {request.META.get('HTTP_X_CSRFTOKEN', 'NOT SET')}\n")
            sys.stderr.write(f"[CSRF Debug Middleware] _dont_enforce_csrf_checks: {getattr(request, '_dont_enforce_csrf_checks', False)}\n")
            sys.stderr.flush()

        response = self.get_response(request)

        if 'create_mock_task' in request.path or ('api/template' in request.path and response.status_code >= 400):
            sys.stderr.write(f"[CSRF Debug Middleware] Response status: {response.status_code}\n")
            sys.stderr.write(f"[CSRF Debug Middleware] ===== REQUEST END =====\n\n")
            sys.stderr.flush()

        return response
