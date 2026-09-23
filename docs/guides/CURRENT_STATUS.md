# BKFlow 本地开发环境 - 当前状态

## ✅ 已解决的问题

### 1. 登录验证绕过
- **状态**: ✅ 完成
- **方法**: 修改 `local_settings.py` 中的 `DisableLoginMiddleware`
- **效果**: 无需登录即可访问后端 API

### 2. 管理员权限
- **状态**: ✅ 完成  
- **结果**: `is_admin: true`
- **效果**: "创建流程"等管理按钮应该可以点击

### 3. 用户认证
- **状态**: ✅ 完成
- **方法**: 中间件从数据库加载真实的 admin 用户并设置到 `request.user` 和 `request._cached_user`
- **效果**: 绕过 BlueKing 的 SimpleLazyObject 延迟加载

## ⚠️ 当前问题

### CSRF Token 验证失败

**现象**:
```json
{
    "result": false,
    "data": {"detail": "CSRF Failed: CSRF token missing or incorrect."},
    "code": "permission_denied"
}
```

**根本原因**:
前端 (https://localhost:9007) 通过 webpack-dev-server 代理转发请求到后端 (http://localhost:8000)，但是：
1. CSRF cookie 在后端域名设置 (`bkflow_csrftoken`)
2. 前端通过代理访问时，浏览器不会自动将这个 cookie 包含在请求中
3. Django 的 CSRF 中间件检测不到 token，拒绝请求

**技术细节**:
- 前端配置: `axios.defaults.xsrfCookieName = "bkflow_csrftoken"`
- 后端配置: `CSRF_COOKIE_NAME = "bkflow_csrftoken"`  
- 代理配置: `target: http://localhost:8000, changeOrigin: true`

## 🔧 解决方案选项

### 方案 1: 修改前端代理配置（推荐）
在 `frontend/build/webpack.dev.conf.js` 的 proxy 配置中添加 cookie 转发：

```javascript
proxy: [
  {
    context,
    target: env.API_URL,
    secure: false,
    changeOrigin: true,
    cookieDomainRewrite: 'localhost',  // 重写 cookie 域名
    onProxyReq: (proxyReq, req, res) => {
      // 确保转发 cookie
      if (req.headers.cookie) {
        proxyReq.setHeader('cookie', req.headers.cookie);
      }
    },
    headers: {
      referer: env.API_URL,
    },
  },
],
```

### 方案 2: 直接访问后端（临时方案）
不使用前端开发服务器，直接访问后端：
- 访问: http://localhost:8000
- 缺点: 前端资源没有热更新

### 方案 3: 为开发环境禁用 CSRF（需要用户确认）
修改 Django 设置，完全禁用 CSRF 检查：
- **警告**: 这会降低安全性，仅适用于本地开发
- **需要**: 用户明确同意此方案

## 📊 服务状态

| 服务 | 地址 | 状态 | 说明 |
|------|------|------|------|
| 后端 | http://localhost:8000 | ✅ 运行中 | Django + API |
| 前端 | https://localhost:9007 | ✅ 运行中 | Vue.js + webpack-dev-server |
| 数据库 | localhost:3306/bkflow | ✅ 连接正常 | MySQL |
| Redis | localhost:6379 | ✅ 连接正常 | 缓存 |

## 🔑 关键配置文件

- `local_settings.py` - 本地开发配置（已修改）
- `config/dev.py` - 开发环境配置（已修改）
- `bkflow/urls.py` - URL 路由（已修改）
- `bkflow/interface/views.py` - 视图函数（已修改，可移除调试代码）
- `frontend/build/webpack.dev.conf.js` - 前端代理配置（需要修改）

## 📝 修改的文件清单

### 后端
1. `.gitignore` - 添加了 local_settings.py
2. `local_settings.py` - 新建，包含禁用登录的中间件
3. `config/dev.py` - 修改中间件配置
4. `bkflow/urls.py` - 添加了登录视图（虽然最终没用上）
5. `bkflow/mock_login.py` - 创建了登录视图（虽然最终没用上）

### 前端
- 暂无修改

## 下一步操作

1. **选择并实施上述解决方案之一**
2. **测试空间创建功能**
3. **处理外部 API 404 错误**（通知公告等外部服务在本地不可用，需要 mock 或忽略）
