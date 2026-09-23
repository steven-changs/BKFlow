# -*- coding: utf-8 -*-
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
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EnvVarManager(models.Manager):
    def get_var(self, key, default=None):
        obj = self.filter(key=key).first()
        return obj.value if obj else default


class EnvironmentVariables(models.Model):
    key = models.CharField("变量KEY", max_length=255, unique=True)
    name = models.CharField("变量描述", max_length=255, blank=True)
    value = models.CharField("变量值", max_length=1000, blank=True)

    objects = EnvVarManager()

    def __str__(self):
        return "%s_%s" % (self.key, self.name)

    class Meta:
        verbose_name = "环境变量 EnvironmentVariables"
        verbose_name_plural = "环境变量 EnvironmentVariables"


class UserPreference(models.Model):
    """用户偏好设置"""
    username = models.CharField(_("用户名"), max_length=128, unique=True, db_index=True)
    last_selected_space_id = models.IntegerField(_("上次选择的空间ID"), null=True, blank=True)
    preferences = models.JSONField(_("其他偏好设置"), default=dict, blank=True)
    create_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    update_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = "用户偏好设置 UserPreference"
        verbose_name_plural = "用户偏好设置 UserPreference"
        db_table = "user_preference"

    def __str__(self):
        return f"{self.username} - Space: {self.last_selected_space_id}"
