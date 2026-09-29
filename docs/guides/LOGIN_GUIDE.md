# BKFlow 本地开发登录指南

## 当前状态

- ✅ 后端服务运行中: http://localhost:8000
- ✅ 前端服务运行中: http://localhost:9007
- ✅ 数据库已初始化，admin 用户已创建
- ⚠️ 自动登录中间件配置遇到问题，需要手动登录一次

## 快速登录步骤

### 方法 1: 浏览器直接登录（推荐）

1. 打开浏览器，访问: http://localhost:8000/login/plain/
2. 这会自动设置登录 session 并重定向到首页
3. 然后访问前端: http://localhost:9007
4. 现在应该已经登录为 admin 用户了

### 方法 2: 使用 curl 获取 cookie

```bash
# 1. 获取登录 cookie
curl -c cookies.txt "http://localhost:8000/login/plain/"

# 2. 使用 cookie 测试权限
curl -b cookies.txt "http://localhost:8000/is_admin_user/"
```

## 验证登录状态

访问以下 API 检查是否已登录：
- http://localhost:8000/is_admin_user/ - 应该返回 `{"result": true, "data": {"is_admin": true, ...}}`

## 配置说明

### 已配置的自动登录功能

在 `local_settings.py` 中已经配置了：

1. **初始超级管理员**: `INIT_SUPERUSER = ["admin"]`
2. **免登录账号**: 环境变量 `BKPAAS_LOGIN_PLAIN_USERNAME=admin`
3. **自动登录中间件**: `SimpleAutoLoginMiddleware`（尝试自动设置 session）

### 免登录路由

项目中已添加以下免登录路由（在 `bkflow/urls.py`）：

```python
# 免登录路由 - 本地开发使用
url(r'^login/plain/$', plain_login_view, name='plain_login'),
url(r'^auto-login/$', auto_login_view, name='auto_login'),
```

## 故障排查

### 如果登录后仍然跳转到登录页

1. 清除浏览器 cookie
2. 重新访问 http://localhost:8000/login/plain/
3. 检查浏览器开发者工具，确认 `bkflow_sessionid` cookie 已设置

### 如果后端未响应

```powershell
# 检查后端进程
netstat -ano | Select-String "8000"

# 如果需要重启
Stop-Process -Id <PID> -Force
cd D:\program\project\BKFlow
.\scripts\start-local.ps1
```

### 如果前端未响应

```powershell
# 检查前端进程
netstat -ano | Select-String "9007"

# 如果需要重启
cd D:\program\project\BKFlow\frontend
npm run dev
```

## 下一步开发建议

由于自动登录中间件配置复杂，建议考虑以下改进方案：

### 方案 A: 前端自动调用登录 API
在前端入口文件（如 `src/main.js`）中添加启动时自动调用 `/login/plain/`

### 方案 B: 修改登录中间件位置
将自动登录逻辑放在 Django 中间件的更早位置，在认证中间件之前执行

### 方案 C: 使用自定义认证后端
创建一个始终返回 admin 用户的认证后端，替代默认的认证逻辑

## 相关文件

- `local_settings.py` - 本地开发配置
- `config/dev.py` - 开发环境配置  
- `bkflow/urls.py` - URL 路由配置
- `bkflow/interface/views.py` - 登录视图实现
- `.env` - 环境变量配置

## 技术细节

### Session 配置

后端使用 Django session 进行认证，session 存储在数据库中：
- Session key: `bkflow_sessionid`
- 有效期: 14 天
- 需要包含: `bk_uid`, `bk_username`, `bk_token`

### 权限检查

主要权限检查 API：
- `/is_admin_user/` - 检查是否为管理员
- `/is_admin_or_current_space_superuser/` - 检查是否为空间管理员

这些 API 依赖 `request.user.is_superuser` 和 `request.user.username`
