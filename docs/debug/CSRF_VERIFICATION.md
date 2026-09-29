# CSRF 配置验证脚本

## 配置检查

### 1. local_settings.py 配置
✅ APP_CODE = 'bkflow'
✅ CSRF_COOKIE_NAME = 'bkflow_csrftoken'
✅ 中间件已更新（自动设置 CSRF cookie）

### 2. bkflow/urls.py 配置
✅ 添加了 /api/get_csrf_token/ 端点

### 3. 前端配置 (frontend/src/api/ajax.js)
✅ axios.defaults.xsrfCookieName = 'bkflow_csrftoken'
✅ axios.defaults.xsrfHeaderName = 'X-CSRFToken'

## 手动验证步骤

### 步骤 1：重启所有服务

**必须重启才能生效！**

```powershell
# 停止所有服务 (Ctrl+C)

# 终端 1 - Interface
.\scripts\start-interface.ps1

# 终端 2 - Engine  
.\scripts\start-engine.ps1

# 终端 3 - Frontend
cd frontend
npm run dev
```

### 步骤 2：测试 CSRF Token 端点

重启后，在浏览器访问：
```
https://localhost:9007/api/get_csrf_token/
```

**期望结果：**
```json
{
  "result": true,
  "data": {
    "csrf_token": "一串随机字符"
  },
  "message": "CSRF token generated"
}
```

### 步骤 3：检查 Cookie

在浏览器控制台 (F12) 执行：
```javascript
// 查看所有 cookies
document.cookie

// 过滤 csrf 相关的 cookie
document.cookie.split(';').filter(c => c.includes('csrf'))
```

**期望结果：**
应该看到 `bkflow_csrftoken=...`

### 步骤 4：清除浏览器缓存

1. F12 打开开发者工具
2. 右键点击刷新按钮
3. 选择 "清空缓存并硬性重新加载"

或者：
1. F12 → Application → Cookies
2. 删除所有 localhost 的 cookies
3. 刷新页面

### 步骤 5：测试调试任务

1. 登录系统
2. 进入空间
3. 创建或编辑流程
4. 添加一个节点（例如：消息展示）
5. 点击"调试"按钮
6. 查看 Network 面板

**检查请求：**
- URL: `POST /api/template/{id}/create_mock_task/`
- Request Headers 应该包含: `X-CSRFToken: ...`
- Cookies 应该包含: `bkflow_csrftoken=...`

**如果成功：**
调试任务开始执行，不再报 CSRF 错误

**如果失败：**
继续查看下面的排查步骤

## 问题排查

### 问题 1：访问 /api/get_csrf_token/ 返回 404

**原因：** 服务未重启
**解决：** 必须重启 Interface 服务

### 问题 2：Cookie 中没有 bkflow_csrftoken

**原因：** 浏览器缓存问题
**解决：** 
1. 清除浏览器缓存和 cookies
2. 先访问 `/api/get_csrf_token/` 触发 cookie 设置
3. 刷新页面

### 问题 3：请求中没有 X-CSRFToken header

**原因：** 前端 axios 没有读取到 cookie
**解决：**
1. 检查 cookie 的 Domain 是否正确（应该是 localhost）
2. 检查 cookie 的 Path 是否正确（应该是 /）
3. 清除缓存重试

### 问题 4：仍然报 CSRF 错误

**临时方案：** 使用正式任务代替调试
1. 点击"发布"按钮发布流程
2. 点击"新建任务"创建正式任务
3. 执行正式任务（功能完全相同）

## 验证成功的标志

✅ 访问 `/api/get_csrf_token/` 返回 JSON 数据
✅ Cookie 中有 `bkflow_csrftoken`
✅ 调试请求的 Headers 中有 `X-CSRFToken`
✅ 调试任务不再报 CSRF 错误
✅ 调试任务正常执行

## 配置文件位置

- `D:\program\project\BKFlow\local_settings.py` (142-143行)
- `D:\program\project\BKFlow\bkflow\urls.py` (53-62行, 68行)
- `D:\program\project\BKFlow\frontend\src\api\ajax.js` (14-15行)

## 关键配置对照

| 项目 | 配置位置 | 配置值 |
|------|---------|--------|
| 后端 Cookie 名称 | local_settings.py | bkflow_csrftoken |
| 前端期望 Cookie 名称 | ajax.js | bkflow_csrftoken |
| 前端发送 Header 名称 | ajax.js | X-CSRFToken |

**所有配置已经正确匹配！只需重启服务即可生效。**
