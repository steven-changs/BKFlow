# 调试任务 CSRF 错误修复指南

## 问题描述

执行流程调试时遇到 CSRF 错误：
```json
{
  "result": false,
  "code": "0000000",
  "message": "CSRF Failed: CSRF cookie not set.",
  "data": {}
}
```

## 根本原因

1. 前端期望的 CSRF Cookie 名称：`bkflow_csrftoken`
2. 后端需要正确设置这个 cookie
3. 调试任务接口 `POST /api/template/{id}/create_mock_task/` 需要 CSRF 保护

## 已完成的修复

### 1. 更新 `local_settings.py`

添加了 CSRF cookie 配置：
```python
# 开发环境 CSRF 配置
APP_CODE = 'bkflow'
CSRF_COOKIE_NAME = APP_CODE + "_csrftoken"  # 前端期望的 cookie 名称
```

更新了中间件以确保 CSRF cookie 被设置：
```python
def __call__(self, request):
    # ... 用户认证代码 ...
    
    response = self.get_response(request)
    
    # 确保 CSRF cookie 被设置
    from django.middleware.csrf import get_token
    get_token(request)
    
    return response
```

### 2. 更新 `bkflow/urls.py`

添加了 CSRF token 获取端点：
```python
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

# 在 urlpatterns 中添加
url(r'^api/get_csrf_token/$', get_csrf_token),
```

## 测试步骤

### 步骤 1：验证配置

```powershell
python test_csrf_fix.py
```

应该看到：
```
✅ CSRF Cookie 名称配置正确
```

### 步骤 2：重启服务

**重要：必须重启所有服务才能生效**

```powershell
# 停止所有正在运行的服务（Ctrl+C）

# 重启 Interface
.\scripts\start-interface.ps1

# 重启 Engine（新终端）
.\scripts\start-engine.ps1

# 重启 Frontend（新终端）
cd frontend
npm run dev
```

### 步骤 3：清除浏览器数据

1. 打开 Chrome DevTools (F12)
2. 右键点击刷新按钮
3. 选择"清空缓存并硬性重新加载"
4. 或者：Application → Cookies → 删除所有 localhost 的 cookies

### 步骤 4：测试 CSRF Token

在浏览器控制台中执行：
```javascript
// 检查 CSRF cookie
document.cookie.split(';').filter(c => c.includes('csrf'))

// 应该看到：bkflow_csrftoken=...
```

或访问：`https://localhost:9007/api/get_csrf_token/`

应该返回：
```json
{
  "result": true,
  "data": {
    "csrf_token": "..."
  },
  "message": "CSRF token generated"
}
```

### 步骤 5：测试调试任务

1. 进入流程编辑页面
2. 添加一个节点（例如：消息展示）
3. 点击"调试"按钮
4. 检查是否还有 CSRF 错误

## 前端 CSRF 工作原理

前端配置（`frontend/src/api/ajax.js`）：
```javascript
axios.defaults.xsrfCookieName = `${window.APP_CODE}_csrftoken`;  // 读取的 cookie 名称
axios.defaults.xsrfHeaderName = 'X-CSRFToken';  // 发送的 header 名称
```

axios 会自动：
1. 从 cookie 中读取 `bkflow_csrftoken`
2. 在 POST 请求中添加 `X-CSRFToken` header

## 调试检查清单

如果问题仍然存在，请检查：

### ✅ 后端检查
```powershell
# 1. 运行配置检查
python test_csrf_fix.py

# 2. 检查 Interface 日志
# 应该看到：APP_CODE = bkflow
```

### ✅ 浏览器检查

1. **检查 Cookie**
   ```javascript
   // F12 → Console
   document.cookie.split(';').forEach(c => console.log(c.trim()))
   ```
   应该包含：`bkflow_csrftoken=...`

2. **检查请求 Headers**
   - F12 → Network
   - 找到 `create_mock_task` 请求
   - 查看 Request Headers
   - 应该包含：`X-CSRFToken: ...`

3. **检查 Cookie 来源**
   - F12 → Application → Cookies → https://localhost:9007
   - 查找 `bkflow_csrftoken`
   - 应该存在且有值

### ✅ 网络检查

确保 webpack dev server 正确转发 cookies：
```javascript
// frontend/build/webpack.dev.conf.js
proxy: [{
  cookieDomainRewrite: 'localhost',
  cookiePathRewrite: '/',
  onProxyReq: (proxyReq, req, res) => {
    if (req.headers.cookie) {
      proxyReq.setHeader('cookie', req.headers.cookie);
    }
  }
}]
```

## 备用方案：禁用调试接口的 CSRF 保护

如果上述方法都不行，可以临时禁用调试接口的 CSRF 保护（仅用于本地开发）：

查找 `bkflow/template/views.py` 中的 `create_mock_task` 视图，添加装饰器：
```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # 仅用于本地开发
def create_mock_task(request, template_id):
    # ...
```

**注意：这只是临时方案，不建议用于生产环境**

## 推荐方案：使用正式任务

调试任务和正式任务的功能完全相同，如果调试一直有问题，可以：

1. 点击"发布"按钮发布流程
2. 点击"新建任务"创建正式任务
3. 填写参数后执行

正式任务执行接口没有 CSRF 问题。

## 总结

调试 CSRF 问题的关键点：
1. ✅ `CSRF_COOKIE_NAME = 'bkflow_csrftoken'`
2. ✅ 中间件确保每个请求都设置 CSRF cookie
3. ✅ 前端配置匹配后端
4. ✅ 重启所有服务
5. ✅ 清除浏览器缓存和 cookies

完成这些步骤后，调试功能应该可以正常使用了。
