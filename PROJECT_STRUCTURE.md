# BKFlow 项目文件组织结构

本文档说明了项目中各个目录的用途和包含的文件类型。

---

## 📁 目录结构总览

```
BKFlow/
├── tools/              # 开发和运维工具
│   ├── check/          # 检查和诊断工具
│   ├── fix/            # 修复和配置工具
│   ├── test/           # 测试脚本
│   └── callback/       # 回调接收服务
├── docs/               # 项目文档
│   ├── debug/          # 调试指南
│   ├── deployment/     # 部署文档
│   └── guides/         # 使用指南
├── scripts/            # 启动和管理脚本
├── owner/              # 个人笔记和会话继承文件
├── bkflow/             # 核心业务代码
├── frontend/           # 前端代码
└── config/             # 配置文件
```

---

## 📂 详细说明

### 1. `tools/` - 开发和运维工具

包含各种辅助开发和运维的 Python 脚本。

#### `tools/check/` - 检查和诊断工具
用于检查系统状态、配置和服务健康度。

| 文件 | 用途 |
|------|------|
| `check_auth.py` | 检查用户认证配置 |
| `check_celery_config.py` | 检查 Celery 配置 |
| `check_celery_queues.py` | 检查 Celery 队列状态 |
| `check_middleware.py` | 检查中间件配置 |
| `check_moduleinfo.py` | 检查模块信息表 |
| `check_moduleinfo_detail.py` | 检查模块信息详细内容 |
| `check_services.py` | 检查所有服务状态 |
| `check_task_status.py` | 检查任务执行状态 |
| `check_users.py` | 检查用户数据 |
| `diagnose_celery.py` | Celery 问题诊断工具 |

**使用方式**：
```bash
cd D:\program\project\BKFlow
python tools/check/check_services.py
```

---

#### `tools/fix/` - 修复和配置工具
用于修复数据问题和调整系统配置。

| 文件 | 用途 |
|------|------|
| `create_moduleinfo.py` | 创建模块信息记录 |
| `create_moduleinfo_space2.py` | 为空间2创建模块信息 |
| `fix_moduleinfo.py` | 修复模块信息数据 |
| `disable_task_module.py` | 禁用任务模块 |
| `switch_mode.py` | 切换模块类型（interface/engine） |

**使用方式**：
```bash
python tools/fix/fix_moduleinfo.py
```

---

#### `tools/test/` - 测试脚本
用于测试各种功能和接口。

| 文件 | 用途 |
|------|------|
| `test_csrf.py` | 测试 CSRF 保护 |
| `test_csrf_bypass.py` | 测试 CSRF 绕过 |
| `test_csrf_fix.py` | 测试 CSRF 修复方案 |
| `test_request.py` | 测试 HTTP 请求 |
| `test_space.py` | 测试空间相关功能 |
| `test_view.py` | 测试视图功能 |

**使用方式**：
```bash
python tools/test/test_space.py
```

---

#### `tools/callback/` - 回调接收服务
用于接收和查看 BKFlow 流程执行完成后的回调通知。

| 文件 | 用途 |
|------|------|
| `callback_receiver.py` | Flask 版本的回调接收服务（需要安装 Flask） |
| `callback_receiver_simple.py` | 轻量版回调接收服务（无需额外依赖，推荐使用） |

**使用方式**：
```bash
# 启动回调接收服务
python tools/callback/callback_receiver_simple.py

# 访问 http://localhost:5000 查看回调记录
# 在 BKFlow 流程配置中填写回调地址: http://localhost:5000/callback
```

**功能特点**：
- ✅ Web 界面查看回调记录
- ✅ 区分成功/失败状态
- ✅ 显示完整的任务输出数据
- ✅ 自动刷新（每 10 秒）
- ✅ 控制台同步打印

---

### 2. `docs/` - 项目文档

包含各种文档和指南。

#### `docs/debug/` - 调试指南
各种问题的调试和排查文档。

| 文件 | 内容 |
|------|------|
| `BROWSER_DEBUG.md` | 浏览器调试指南 |
| `CSRF_DEBUG_FIX.md` | CSRF 问题修复记录 |
| `CSRF_QUICK_FIX.md` | CSRF 快速修复方案 |
| `CSRF_TROUBLESHOOTING.md` | CSRF 问题排查 |
| `CSRF_VERIFICATION.md` | CSRF 验证说明 |
| `NODE_CONFIG_ERROR.md` | Node 配置错误处理 |
| `PYCHARM_DEBUG_GUIDE.md` | PyCharm 调试配置 |
| `VARIABLE_DEBUG_GUIDE.md` | 变量调试指南 |
| `TASK_MODULE_ISSUE.md` | 任务模块问题记录 |

---

#### `docs/deployment/` - 部署文档
部署相关的文档和总结。

| 文件 | 内容 |
|------|------|
| `DEPLOYMENT.md` | 部署指南 |
| `DEPLOYMENT_COMPLETE_GUIDE.md` | 完整部署指南 |
| `DEPLOYMENT_SUMMARY.txt` | 部署总结 |

---

#### `docs/guides/` - 使用指南
各种功能的使用说明和最佳实践。

| 文件 | 内容 |
|------|------|
| `EXPERIENCE_GUIDE.md` | 功能体验指南 |
| `FRONTEND_GUIDE.md` | 前端开发指南 |
| `LOGIN_GUIDE.md` | 登录功能说明 |
| `MODE_SWITCH_GUIDE.md` | 模式切换指南 |
| `QUICKSTART.md` | 快速开始 |
| `QUICK_START.md` | 快速启动 |
| `SETUP_COMPLETE.md` | 安装完成说明 |
| `CHECKLIST.md` | 检查清单 |
| `CURRENT_STATUS.md` | 当前状态记录 |
| `SESSION_ACHIEVEMENTS.md` | 会话成就记录 |
| `SESSION_SUMMARY.md` | 会话总结 |
| `NEXT_STEPS.txt` | 下一步计划 |
| `REFERENCE.md` | 参考资料 |

---

### 3. `scripts/` - 启动和管理脚本

包含启动服务和管理系统的 PowerShell 脚本。

| 文件 | 用途 |
|------|------|
| `start-bkflow.ps1` | 一键启动所有 BKFlow 服务 |
| `start-all.ps1` | 启动所有服务（旧版本） |
| `start-interface.ps1` | 启动 Interface 服务 |
| `start-engine.ps1` | 启动 Engine 服务 |
| `start-celery-worker.ps1` | 启动 Celery Worker |
| `start-celery-beat.ps1` | 启动 Celery Beat |
| `start-frontend.ps1` | 启动前端服务 |
| `docker-manage.ps1` | Docker 管理脚本 |

**推荐使用**：
```powershell
.\scripts\start-bkflow.ps1
```

这个脚本会按顺序启动：
1. Interface (8000)
2. Engine (8001)
3. Celery Worker
4. Celery Beat
5. Frontend (9007)

---

### 4. `owner/` - 个人笔记和会话继承

包含个人笔记、会话继承文件和学习资料。

**目录结构**：
```
owner/
├── 会话继承.txt                    # 会话继承主文件
├── 前端错误排查记录.md              # 前端问题记录
├── engine相关/                     # Engine 相关文档
│   └── 引擎操作表单填写指南.md
└── 其他笔记...
```

---

## 🚀 快速使用指南

### 启动服务
```powershell
# 方式1：使用启动脚本（推荐）
.\scripts\start-bkflow.ps1

# 方式2：手动启动各个服务
.\scripts\start-interface.ps1
.\scripts\start-engine.ps1
.\scripts\start-celery-worker.ps1
.\scripts\start-celery-beat.ps1
.\scripts\start-frontend.ps1
```

### 检查系统状态
```bash
# 检查所有服务
python tools/check/check_services.py

# 检查 Celery
python tools/check/check_celery_queues.py

# 诊断 Celery 问题
python tools/check/diagnose_celery.py
```

### 修复问题
```bash
# 修复模块信息
python tools/fix/fix_moduleinfo.py

# 切换模块类型
python tools/fix/switch_mode.py
```

### 测试功能
```bash
# 测试空间功能
python tools/test/test_space.py

# 测试请求
python tools/test/test_request.py
```

### 启动回调接收服务
```bash
# 启动回调服务
python tools/callback/callback_receiver_simple.py

# 访问
http://localhost:5000
```

---

## 📝 注意事项

1. **执行路径**：所有脚本都应该在项目根目录 `D:\program\project\BKFlow` 下执行
2. **环境变量**：启动脚本会自动加载 `.env` 文件中的环境变量
3. **模块类型**：
   - Interface 和 Engine 需要设置不同的 `BKFLOW_MODULE_TYPE`
   - Celery Worker 和 Beat 必须使用 `engine` 模块类型
4. **依赖**：
   - `callback_receiver_simple.py` 无需额外依赖（推荐）
   - `callback_receiver.py` 需要安装 Flask（可能有版本冲突）

---

## 🔗 相关链接

- **项目主 README**: `README.md`
- **会话继承文件**: `owner/会话继承.txt`
- **前端错误排查**: `owner/前端错误排查记录.md`
- **引擎操作指南**: `owner/engine相关/引擎操作表单填写指南.md`

---

## 📞 问题反馈

如果遇到问题：
1. 先查看 `docs/debug/` 下的相关文档
2. 使用 `tools/check/` 下的诊断工具
3. 查看服务日志窗口的错误信息
4. 记录问题到 `owner/` 目录下

---

**最后更新**: 2026-09-23
