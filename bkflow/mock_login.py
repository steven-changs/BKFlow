# -*- coding: utf-8 -*-
"""
本地开发模拟登录视图
"""
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def mock_login(request):
    """模拟登录 - 自动设置 session"""
    # 设置 session 模拟已登录用户
    request.session['bk_uid'] = 'admin'
    request.session['bk_username'] = 'admin'
    request.session['bk_token'] = 'mock-token-for-local-dev'

    # 获取回调 URL
    callback_url = request.GET.get('c_url', '/')

    return HttpResponseRedirect(callback_url)


@csrf_exempt
def mock_login_success(request):
    """模拟登录成功页面"""
    return JsonResponse({
        'result': True,
        'message': 'Login successful (mock)',
        'data': {
            'username': 'admin',
            'is_superuser': True
        }
    })
