# BKFlow 前端开发完整指南

## 📋 前端架构说明

BKFlow 采用**前后端分离**架构：
- **后端 API**: Django REST Framework (端口 8000) ✅ 已配置
- **前端界面**: Vue 2 + Webpack Dev Server (端口 9007) ⬅️ 接下来配置

## 🚀 快速启动步骤

### 步骤 1: 确认后端已运行
前端需要调用后端 API，确保 Django 服务在运行：
```
✅ Django 应该运行在: http://localhost:8000
```

### 步骤 2: 安装前端依赖
打开 PowerShell，执行：
```powershell
cd D:\program\project\BKFlow\frontend
npm install
```

**预计时间**: 3-5 分钟（首次安装）

### 步骤 3: 启动前端开发服务器

#### 方式 A: 使用启动脚本（推荐）
```powershell
cd D:\program\project\BKFlow
.\scripts\start-frontend.ps1
```

#### 方式 B: 手动启动
```powershell
cd D:\program\project\BKFlow\frontend
npm run dev
```

### 步骤 4: 访问前端页面
启动成功后，在浏览器访问：
```
http://localhost:9007
```

---

## 📁 已配置的文件

### 1. `.env.local` (已创建) ✅
```bash
DEV_HOST=localhost
API_URL=http://localhost:8000
```

### 2. `index-dev.html` (已存在) ✅
开发环境的 HTML 入口文件，已包含基本配置。

---

## 🔧 前端开发环境配置

### Node.js 版本检查 ✅
```powershell
node --version   # 当前: v24.14.1 (满足 >= 18.20.4)
npm --version    # 当前: 11.11.0
```

### 开发端口
- **前端开发服务器**: http://localhost:9007
- **后端 API**: http://localhost:8000
- **Webpack 会自动代理 API 请求**: 前端 `/api/*` → 后端 `http://localhost:8000/api/*`

---

## 🎯 完整启动流程

### 启动所有服务（前端 + 后端）

**终端 1: 启动后端**
```powershell
cd D:\program\project\BKFlow
.\scripts\start-local.ps1
```
等待看到：`Starting development server at http://0.0.0.0:8000/`

**终端 2: 启动前端**
```powershell
cd D:\program\project\BKFlow
.\scripts\start-frontend.ps1
```
等待看到：`Compiled successfully`

**访问应用**
```
前端页面: http://localhost:9007
后端 API: http://localhost:8000
管理后台: http://localhost:8000/bkflow_admin/
```

---

## 💡 PyCharm 配置前端调试

### 配置 npm 运行

1. **Run → Edit Configurations → + → npm**
2. 配置内容：
   - **Name**: `Frontend Dev Server`
   - **package.json**: `D:\program\project\BKFlow\frontend\package.json`
   - **Command**: `run`
   - **Scripts**: `dev`
   - **Working directory**: `D:\program\project\BKFlow\frontend`

3. 点击 **OK**

现在可以在 PyCharm 中同时运行：
- Django Server (F5 调试)
- Frontend Dev Server (普通运行)
- Celery Worker (可选)
- Celery Beat (可选)

---

## 🐛 故障排查

### 问题 1: 端口 9007 被占用
**症状:**
```
Error: listen EADDRINUSE: address already in use :::9007
```

**解决:**
```powershell
# 查找占用进程
netstat -ano | findstr "9007"

# 停止进程
taskkill /PID <进程ID> /F
```

### 问题 2: npm install 失败
**症状:**
```
npm ERR! code ENETUNREACH
```

**解决:**
```powershell
# 切换 npm 镜像源
npm config set registry https://registry.npmmirror.com

# 重新安装
npm install
```

### 问题 3: 前端无法访问后端 API
**症状:**
前端页面加载，但数据请求失败

**检查清单:**
- [ ] 后端服务是否运行在 8000 端口
- [ ] `.env.local` 中 `API_URL` 是否正确
- [ ] 浏览器控制台是否有 CORS 错误

**解决:**
确保后端在运行：
```powershell
# 在浏览器访问，应该返回 404 页面（说明后端正常）
http://localhost:8000
```

### 问题 4: 编译错误
**症状:**
```
Module not found: Error: Can't resolve 'xxx'
```

**解决:**
```powershell
# 清理并重新安装
cd D:\program\project\BKFlow\frontend
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json
npm install
```

### 问题 5: 前端热重载不生效
**症状:**
修改代码后页面不自动刷新

**解决:**
这是正常的，Webpack Dev Server 已配置热重载。如果不生效：
1. 刷新浏览器 (F5)
2. 重启前端开发服务器

---

## 📊 开发模式 vs 生产构建

### 开发模式（当前）
```powershell
npm run dev
```
- ✅ 热重载
- ✅ Source Map
- ✅ 开发工具
- ❌ 代码未压缩

### 生产构建
```powershell
npm run build
```
- ✅ 代码压缩
- ✅ 资源优化
- ❌ 无热重载
- 输出目录: `frontend/dist/`

---

## 🔍 前端项目结构

```
frontend/
├── src/
│   ├── views/           # 页面组件
│   │   ├── admin/       # 管理员面板
│   │   ├── task/        # 任务模块
│   │   └── template/    # 流程模板模块
│   ├── components/      # 公共组件
│   ├── router/          # 路由配置
│   ├── store/           # Vuex 状态管理
│   ├── api/             # API 请求封装
│   ├── utils/           # 工具函数
│   └── assets/          # 静态资源
├── build/               # Webpack 配置
├── index-dev.html       # 开发环境入口
├── package.json         # 依赖配置
└── .env.local          # 本地环境变量 ✅ 已创建
```

---

## 🎨 前端技术栈

- **框架**: Vue 2.7.14
- **UI 库**: 
  - bk-magic-vue (蓝鲸 MagicBox UI)
  - Element UI
- **流程图**: @antv/x6
- **代码编辑器**: Monaco Editor
- **状态管理**: Vuex
- **路由**: Vue Router
- **构建工具**: Webpack 5

---

## 📝 常用命令

```powershell
# 进入前端目录
cd D:\program\project\BKFlow\frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint

# 代码自动修复
npm run fix

# 运行测试
npm run test:plugin-form
```

---

## 🌐 访问地址汇总

| 服务 | 地址 | 说明 |
|------|------|------|
| **前端页面** | http://localhost:9007 | Vue 开发服务器 |
| **后端 API** | http://localhost:8000 | Django REST API |
| **管理后台** | http://localhost:8000/bkflow_admin/ | Django Admin |
| **API 文档** | http://localhost:8000/swagger/ | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc/ | API 文档 |

---

## ⚙️ 前端环境变量说明

`.env.local` 文件中的配置：

```bash
# 开发域名（本地开发用 localhost）
DEV_HOST=localhost

# 后端 API 地址
API_URL=http://localhost:8000
```

**其他可选配置：**
```bash
# 如果需要连接真实蓝鲸环境
# API_URL=http://your-blueking-server.com
# DEV_HOST=dev.your-domain.com
```

---

## 🎯 下一步

1. **启动前端**
   ```powershell
   .\scripts\start-frontend.ps1
   ```

2. **访问页面**
   ```
   http://localhost:9007
   ```

3. **开始开发**
   - 修改 `frontend/src/` 下的文件
   - 浏览器自动热重载
   - 在 PyCharm 中调试后端 API

---

## 💻 完整开发环境

现在你拥有完整的开发环境：

- ✅ **后端**: Django + Celery（可调试）
- ✅ **前端**: Vue 2 + Webpack Dev Server（热重载）
- ✅ **数据库**: MySQL 8.0
- ✅ **缓存**: Redis
- ✅ **开发工具**: PyCharm（断点调试）

开始愉快的开发之旅吧！🚀
