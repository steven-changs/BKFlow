# BKFlow 双模式配置指南

## 📋 两种运行模式

### 模式 1：仅 Interface（简化模式）
**适用场景**：学习前端、数据模型、API 开发
- 运行服务：Interface (8000) + Frontend (9007)
- 可用功能：空间、模板、插件、权限管理
- 不可用：任务执行、任务列表

### 模式 2：Interface + Engine（完整模式）
**适用场景**：测试完整流程、开发插件、任务执行
- 运行服务：Interface (8000) + Engine (8001) + Frontend (9007)
- 可用功能：所有功能

---

## 🚀 快速切换

### 切换到简化模式
```powershell
python switch_mode.py --mode simple
```

### 切换到完整模式
```powershell
python switch_mode.py --mode full
```

---

## 📝 手动操作指南

### 启动简化模式

**步骤 1：启动 Interface**
```powershell
cd D:\program\project\BKFlow
.\scripts\start-interface.ps1
```

**步骤 2：启动 Frontend**
```powershell
cd frontend
npm run dev
```

**步骤 3：禁用 Engine**
```powershell
python disable_task_module.py
```

✅ 访问：https://localhost:9007

---

### 启动完整模式

**步骤 1：启动 Interface**
```powershell
.\scripts\start-interface.ps1
```

**步骤 2：启动 Engine**
```powershell
.\scripts\start-engine.ps1
```

**步骤 3：启动 Frontend**
```powershell
cd frontend
npm run dev
```

**步骤 4：配置 ModuleInfo**
```powershell
python enable_task_module.py
```

✅ 访问：https://localhost:9007

---

## 🛠️ 服务状态检查

```powershell
# 检查所有服务
python check_services.py

# 检查当前模式
python check_mode.py
```

---

## 📊 端口使用

| 服务 | 端口 | 状态 |
|------|------|------|
| Interface | 8000 | 总是运行 |
| Engine | 8001 | 仅完整模式 |
| Frontend | 9007 | 总是运行 |
| MySQL | 3306 | 总是运行 |
| Redis | 6379 | 总是运行 |

---

## ⚠️ 注意事项

1. **切换模式时需要重启服务**
2. **完整模式需要运行 3 个终端窗口**
3. **简化模式只需要 2 个终端窗口**
4. **数据库中的 ModuleInfo 记录决定了模式**

---

## 🐛 故障排除

### 任务页面显示 "ModuleInfo does not exist"
→ 当前是简化模式，运行 `python enable_task_module.py` 切换到完整模式

### Engine 启动失败
→ 检查 8001 端口是否被占用：`Get-NetTCPConnection -LocalPort 8001`

### Frontend 无法连接后端
→ 检查 CSRF token 和 APP_CODE 配置
