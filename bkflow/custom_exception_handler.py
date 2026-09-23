# -*- coding: utf-8 -*-
"""
自定义异常处理器：捕获并记录 CSRF 错误的堆栈跟踪
"""
import sys
import traceback
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    """捕获并记录所有异常的堆栈跟踪"""
    if 'CSRF' in str(exc):
        sys.stderr.write(f"\n[EXCEPTION HANDLER] CSRF Exception caught!\n")
        sys.stderr.write(f"[EXCEPTION HANDLER] Exception type: {type(exc).__name__}\n")
        sys.stderr.write(f"[EXCEPTION HANDLER] Exception message: {exc}\n")
        sys.stderr.write(f"[EXCEPTION HANDLER] Traceback:\n")
        sys.stderr.write(''.join(traceback.format_tb(exc.__traceback__)))
        sys.stderr.write(f"\n")
        sys.stderr.flush()

    # 调用默认的异常处理器
    return drf_exception_handler(exc, context)
