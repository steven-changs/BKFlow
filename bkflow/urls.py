"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸流程引擎服务 (BlueKing Flow Engine Service) available.
Copyright (C) 2024 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.

We undertake not to change the open source license (MIT license) applicable

to the current version of the project delivered to anyone in the future.
"""
from blueapps.account.decorators import login_exempt
from django.conf import settings
from django.conf.urls import url
from django.urls import include, path, register_converter
from django.views.decorators.csrf import csrf_exempt
from pipeline.contrib.engine_admin import views as engine_admin_views
from pipeline.contrib.engine_admin.urls import EngineConverter

from module_settings import BKFLOWModuleType

# 本地开发免登录视图
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token

@csrf_exempt
@login_exempt
def auto_login(request):
    """自动登录视图"""
    # 设置 session
    request.session['bk_uid'] = 'admin'
    request.session['bk_username'] = 'admin'
    request.session['bk_token'] = 'local-dev-token'

    # 重定向到回调地址
    c_url = request.GET.get('c_url', '/')
    return HttpResponseRedirect(c_url)

@csrf_exempt
@login_exempt
def login_success(request):
    """登录成功回调"""
    return JsonResponse({'result': True, 'message': 'Auto login success', 'data': {'username': 'admin'}})

@login_exempt
@ensure_csrf_cookie
def get_csrf_token(request):
    """获取 CSRF Token 的端点"""
    token = get_token(request)
    return JsonResponse({
        'result': True,
        'data': {'csrf_token': token},
        'message': 'CSRF token generated'
    })

urlpatterns = [
    url(r'^login/$', auto_login),
    url(r'^login/plain/$', auto_login),
    url(r'^account/login_success/$', login_success),
    url(r'^api/get_csrf_token/$', get_csrf_token),  # 添加 CSRF token 端点
]

if settings.BKFLOW_MODULE.type == BKFLOWModuleType.interface:
    urlpatterns += [
        url(r"^", include("bkflow.interface.urls")),
        url(r"^api/user/", include("bkflow.interface.user_urls")),  # 用户偏好设置 API
        url(r"^api/template/", include("bkflow.template.urls")),
        url(r"^api/decision_table/", include("bkflow.decision_table.urls")),
        url(r"^api/space/", include("bkflow.space.urls")),
        url(r"^api/plugin/", include("bkflow.plugin.urls")),
        url(r"^api/bk_plugin/", include("bkflow.bk_plugin.urls")),
        url(r"^api/admin/", include("bkflow.admin.urls")),
        url(r"^api/permission/", include("bkflow.permission.urls")),
        url(r"^api/plugin_query/", include("bkflow.pipeline_plugins.query.urls")),
        url(r"^api/plugin_service/", include("plugin_service.urls")),
        url(r"^api/api_plugin_demo/", include("bkflow.api_plugin_demo.urls")),
        url(r"^api/statistics/", include("bkflow.statistics.urls")),
        *(
            [url(r"^bkvision/", include("django_bkvision.urls"))]
            if "django_bkvision" in settings.INSTALLED_APPS
            else []
        ),
        url(r"^api/label/", include("bkflow.label.urls")),
        url(r"^notice/", include("bk_notice_sdk.urls")),
        url(r"^version_log/", include("version_log.urls", namespace="version_log")),
        url(r"^api/variable/", include("bkflow.variable_manager.urls")),
    ]
elif settings.BKFLOW_MODULE.type == BKFLOWModuleType.engine:
    engine_admin_actions = [
        "task_pause",
        "task_resume",
        "task_revoke",
        "node_retry",
        "node_skip",
        "node_callback",
        "node_skip_exg",
        "node_skip_cpg",
        "node_forced_fail",
    ]
    register_converter(EngineConverter, "engine")
    engine_admin_urlpatterns = [
        path(
            f"task_engine_admin/api/v1/<engine:engine_type>/{action}/<str:instance_id>/",
            csrf_exempt(login_exempt(getattr(engine_admin_views, action))),
        )
        for action in engine_admin_actions
    ]
    urlpatterns += [
        url(r"^task/", include("bkflow.task.urls")),
    ] + engine_admin_urlpatterns
