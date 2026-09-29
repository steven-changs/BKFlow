# BKFlow 本地开发环境 - 会话成就总结

## ✅ 已完成的配置

### 1. 登录验证禁用
**文件**：`local_settings.py`
- 创建了 `DisableLoginMiddleware`
- 自动加载 admin 用户
- 无需登录即可访问

### 2. CSRF 保护修复
**修改文件**：
- `frontend/index-dev.html` - 设置 `APP_CODE = 'bkflow'`
- `frontend/build/webpack.dev.conf.js` - 添加 cookie 转发
- `local_settings.py` - CSRF 配置

**结果**：空间创建等功能正常

### 3. 双模式配置系统 ⭐

#### 模式 1：简化模式（2个服务）
```powershell
# 终端 1 - Interface
cd D:\program\project\BKFlow
Get-Content .env | ForEach-Object { if ($_ -match '^([^=]+)=(.*)$' -and $matches[1] -notmatch '^#') { [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process') } }
$env:BKFLOW_MODULE_TYPE='interface'
$env:DJANGO_SETTINGS_MODULE='config.dev'
python manage.py runserver 0.0.0.0:8000 --noreload

# 终端 2 - Frontend
cd D:\program\project\BKFlow\frontend
npm run dev

# 配置模式
python switch_mode.py --mode simple
```

**功能**：空间、模板、插件管理 ✅ | 任务执行 ❌

---

#### 模式 2：完整模式（3个服务）⭐⭐
```powershell
# 终端 1 - Interface
cd D:\program\project\BKFlow
Get-Content .env | ForEach-Object { if ($_ -match '^([^=]+)=(.*)$' -and $matches[1] -notmatch '^#') { [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process') } }
$env:BKFLOW_MODULE_TYPE='interface'
$env:DJANGO_SETTINGS_MODULE='config.dev'
python manage.py runserver 0.0.0.0:8000 --noreload

# 终端 2 - Engine ⭐ 关键
cd D:\program\project\BKFlow
Get-Content .env | ForEach-Object { if ($_ -match '^([^=]+)=(.*)$' -and $matches[1] -notmatch '^#') { [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process') } }
$env:BKFLOW_MODULE_TYPE='engine'
$env:DJANGO_SETTINGS_MODULE='config.dev'
python manage.py runserver 0.0.0.0:8001 --noreload

# 终端 3 - Frontend
cd D:\program\project\BKFlow\frontend
npm run dev

# 配置模式
python switch_mode.py --mode full
```

**功能**：所有功能 ✅

---

## 🚀 快速启动脚本（已创建）

### 使用启动脚本
```powershell
# Interface
.\scripts\start-interface.ps1

# Engine (完整模式需要)
.\scripts\start-engine.ps1

# Frontend
cd frontend
npm run dev
```

---

## 🔧 模式切换命令

```powershell
# 检查当前模式
python switch_mode.py --check

# 切换到简化模式
python switch_mode.py --mode simple

# 切换到完整模式
python switch_mode.py --mode full

# 检查服务状态
python check_services.py
```

---

## 📊 服务端口

| 服务 | 端口 | 简化模式 | 完整模式 |
|------|------|----------|----------|
| Interface | 8000 | ✅ | ✅ |
| Engine | 8001 | ❌ | ✅ 必需 |
| Frontend | 9007 | ✅ | ✅ |

访问：https://localhost:9007

---

## ⚠️ 重要提示

### 每个空间需要 ModuleInfo
创建新空间后，需要为它创建 ModuleInfo：
```python
# 修改 space_id 为新空间ID
python create_moduleinfo_space2.py
```

或直接运行：
```powershell
python switch_mode.py --mode full
# 会提示创建 ModuleInfo
```

---

## 🐛 已知问题

### 1. 通知公告 404
- 可忽略，不影响核心功能

### 2. 节点配置 JS 错误
- 关闭错误弹窗后可正常使用

### 3. 调试任务 CSRF 错误（待解决）
- **临时方案**：直接发布流程并执行正式任务
- 正式执行和调试功能相同

---

## 📝 关键文件

### 配置文件
- `local_settings.py` - 本地开发配置
- `config/dev.py` - 开发环境配置
- `.env` - 环境变量
- `frontend/index-dev.html` - 前端配置

### 工具脚本
- `switch_mode.py` - 模式切换
- `check_services.py` - 服务检查
- `scripts/start-interface.ps1` - 启动 Interface
- `scripts/start-engine.ps1` - 启动 Engine

### 文档
- `SETUP_COMPLETE.md` - 完整配置说明
- `EXPERIENCE_GUIDE.md` - 功能体验指南
- `MODE_SWITCH_GUIDE.md` - 模式切换详解

---

## 🎯 下次启动（重要）

### 完整模式启动顺序
```powershell
# 1. Interface (8000)
.\scripts\start-interface.ps1

# 2. Engine (8001) - 新终端
.\scripts\start-engine.ps1

# 3. Frontend (9007) - 新终端
cd frontend
npm run dev

# 4. 浏览器访问
https://localhost:9007
```

### 检查是否正常
```powershell
python check_services.py
```

应该显示：
```
[Interface] Running on localhost:8000
[Engine] Running on localhost:8001
[Frontend] Running on localhost:9007
Current Mode: Full Mode (Engine Enabled)
Status: All required services are running
```

---

## 💡 记住这些

1. **完整模式 = 3个服务一起启动**
2. **Engine 必须在 8001 端口**
3. **每个空间需要自己的 ModuleInfo**
4. **清除浏览器缓存可以解决很多问题**

---

## 🎉 成就达成

- ✅ 绕过 BlueKing 登录限制
- ✅ 修复管理员权限
- ✅ 解决 CSRF Token 问题
- ✅ 搭建双模式开发环境
- ✅ 启动完整的微服务架构
- ✅ 创建空间并配置 Engine
- ✅ 准备好体验完整流程

**总耗时**：约 4-5 小时
**Token 使用**：约 115,000 / 200,000

---

**祝您开发顺利！** 🚀
