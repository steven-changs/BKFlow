# CSRF 调试任务修复 - 快速操作指南

## 问题
执行流程调试时报错：`CSRF Failed: CSRF cookie not set.`

## 已完成的修复

### 1. `local_settings.py` 
- ✅ 添加 `APP_CODE = 'bkflow'`
- ✅ 添加 `CSRF_COOKIE_NAME = 'bkflow_csrftoken'`
- ✅ 更新中间件自动设置 CSRF cookie

### 2. `bkflow/urls.py`
- ✅ 添加 `/api/get_csrf_token/` 端点

## 🚀 立即执行的步骤

### 步骤 1：验证配置
```powershell
python test_csrf_fix.py
```

### 步骤 2：重启所有服务（必须）
```powershell
# 1. 停止所有服务 (Ctrl+C)

# 2. 重启 Interface
.\scripts\start-interface.ps1

# 3. 重启 Engine (新终端)
.\scripts\start-engine.ps1

# 4. 重启 Frontend (新终端)
cd frontend
npm run dev
```

### 步骤 3：清除浏览器缓存
1. F12 打开开发者工具
2. 右键刷新按钮 → "清空缓存并硬性重新加载"
3. 或者：Application → Cookies → 删除所有 localhost cookies

### 步骤 4：验证 CSRF Cookie
浏览器访问：`https://localhost:9007/api/get_csrf_token/`

应该返回：
```json
{
  "result": true,
  "data": {"csrf_token": "..."},
  "message": "CSRF token generated"
}
```

在浏览器控制台执行：
```javascript
document.cookie.split(';').filter(c => c.includes('csrf'))
```
应该看到：`["bkflow_csrftoken=..."]`

### 步骤 5：测试调试任务
1. 创建或编辑流程
2. 添加节点
3. 点击"调试"按钮
4. 检查是否还有 CSRF 错误

## 🔍 问题排查

### 如果仍然报 CSRF 错误：

**检查 1：CSRF Cookie 是否存在**
```javascript
// 浏览器控制台
document.cookie
```
必须包含：`bkflow_csrftoken=...`

**检查 2：请求是否携带 CSRF Token**
- F12 → Network
- 找到 `create_mock_task` 请求
- Request Headers 应该包含：`X-CSRFToken: ...`

**检查 3：服务是否正确重启**
```powershell
python check_services.py
```

## 📝 关键配置对照

| 配置项 | 位置 | 期望值 |
|--------|------|--------|
| CSRF_COOKIE_NAME | local_settings.py | bkflow_csrftoken |
| xsrfCookieName | frontend ajax.js | bkflow_csrftoken |
| xsrfHeaderName | frontend ajax.js | X-CSRFToken |

## 🎯 备用方案

如果调试功能持续有问题，可以使用正式任务：

1. 点击"发布"发布流程
2. 点击"新建任务"
3. 执行正式任务（功能完全相同）

## 📞 需要帮助？

如果问题仍未解决，请提供：
1. `python test_csrf_fix.py` 的输出
2. 浏览器 Network 面板的 `create_mock_task` 请求截图
3. 浏览器 Console 的错误信息

详细文档：`CSRF_DEBUG_FIX.md`
