# CSRF 调试错误排查指南

## 当前状态

✅ 后端配置正确：`CSRF_COOKIE_NAME = 'bkflow_csrftoken'`
✅ CSRF cookie 正确设置：`set-cookie: bkflow_csrftoken=...`
✅ CSRF token 端点工作正常
❌ 调试任务仍报错：`CSRF Failed: CSRF cookie not set.`

## 问题分析

错误信息 "CSRF cookie not set" 意味着：
- Django 后端在验证 CSRF 时，无法从请求中读取到 `bkflow_csrftoken` cookie
- 可能原因：
  1. 浏览器没有保存 cookie
  2. Cookie 的 Domain/Path 不匹配
  3. 前端请求没有携带 cookie
  4. Webpack 代理没有正确转发 cookie

## 解决方案

### 方案 1：浏览器端验证（最重要）

**步骤 1：清除所有缓存和 Cookie**
```
1. 打开 Chrome DevTools (F12)
2. Application → Storage → Clear site data
3. 勾选所有选项（Cookies, Cache, Storage）
4. 点击 "Clear site data"
5. 关闭浏览器，重新打开
```

**步骤 2：手动触发 CSRF Cookie 设置**
```
1. 访问：https://localhost:9007/api/get_csrf_token/
2. F12 → Application → Cookies → https://localhost:9007
3. 确认看到：bkflow_csrftoken
```

**步骤 3：检查 Cookie 是否在请求中**
```
1. 进入流程编辑页面
2. 点击"调试"
3. F12 → Network → 找到 create_mock_task 请求
4. Request Headers 检查：
   - Cookie: 应该包含 bkflow_csrftoken=...
   - X-CSRFToken: 应该有值
```

### 方案 2：临时禁用 CSRF 保护（仅用于调试）

如果方案 1 不行，可以临时禁用调试接口的 CSRF 保护：

**编辑文件：** `bkflow/template/views/template.py`

在第 647 行的 `create_mock_task` 方法上添加装饰器：

```python
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class TemplateViewSet(TenantScopeMixin, UserModelViewSet):
    # ... 其他代码 ...
    
    @method_decorator(csrf_exempt)  # 添加这行
    @action(methods=["POST"], detail=True, url_path="create_mock_task")
    def create_mock_task(self, request, *args, **kwargs):
        # ... 原有代码 ...
```

**重启 Interface 服务：**
```powershell
# 停止当前服务 (找到 Interface 进程并 Ctrl+C)
# 重新启动
.\scripts\start-interface.ps1
```

**注意：这只是临时方案，不要用于生产环境**

### 方案 3：修改 DRF 认证类（推荐用于本地开发）

编辑文件：`bkflow/template/views/template.py`

在 `TemplateViewSet` 类中添加：

```python
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """本地开发用：禁用 CSRF 检查的 Session 认证"""
    def enforce_csrf(self, request):
        return  # 跳过 CSRF 检查

class TemplateViewSet(TenantScopeMixin, UserModelViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]  # 添加这行
    # ... 其他代码保持不变 ...
```

### 方案 4：使用正式任务代替调试（最简单）

如果以上方案都太复杂，直接使用正式任务：

1. 点击"发布"按钮发布流程
2. 点击"新建任务"
3. 填写参数
4. 执行任务

**正式任务和调试任务功能完全相同，只是不会保存到数据库**

## 深度排查

### 检查点 1：Cookie Domain

```javascript
// 浏览器控制台
document.cookie.split(';').forEach(c => {
  const [name, value] = c.trim().split('=');
  if (name.includes('csrf')) {
    console.log('Cookie名称:', name);
    console.log('Cookie值:', value);
  }
});
```

### 检查点 2：Axios 配置

```javascript
// 浏览器控制台
console.log('CSRF Cookie Name:', window.APP_CODE + '_csrftoken');
console.log('Expected:', 'bkflow_csrftoken');
```

### 检查点 3：网络请求

```
F12 → Network → create_mock_task
- Request URL: https://localhost:9007/api/template/1/create_mock_task/
- Request Method: POST
- Request Headers:
  * Cookie: 必须包含 bkflow_csrftoken
  * X-CSRFToken: 必须有值
  * Content-Type: application/json
```

### 检查点 4：后端日志

查看 Interface 服务的控制台输出，看是否有 CSRF 相关的错误信息。

## 已更新的配置

### local_settings.py
```python
CSRF_COOKIE_NAME = 'bkflow_csrftoken'
CSRF_USE_SESSIONS = False
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_TRUSTED_ORIGINS = ['https://localhost:9007', ...]
```

### 前端 ajax.js
```javascript
axios.defaults.xsrfCookieName = 'bkflow_csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
```

## 推荐操作顺序

1. **先尝试方案 1**（清除缓存）- 最简单
2. **如果不行，尝试方案 4**（使用正式任务）- 最快
3. **如果需要调试功能，尝试方案 3**（修改认证类）- 最优雅
4. **最后考虑方案 2**（完全禁用 CSRF）- 最直接但不推荐

## 需要帮助？

如果问题仍未解决，请提供：
1. 浏览器控制台的 `document.cookie` 输出
2. Network 面板中 create_mock_task 请求的完整 Headers
3. Interface 服务的控制台输出（特别是 CSRF 相关的日志）
