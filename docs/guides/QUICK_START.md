# BKFlow 快速启动指南

## 🚀 两种启动模式

### 模式 1：简化模式（推荐初学）
**只启动 Interface + Frontend，不启动 Engine**

**适合**：学习前端、数据模型、模板管理
**不支持**：任务执行、任务列表

### 模式 2：完整模式（推荐开发）
**启动 Interface + Engine + Frontend**

**适合**：测试完整流程、开发插件、任务调试
**支持**：所有功能

---

## 📝 快速启动命令

### 启动简化模式

**终端 1 - Interface**
```powershell
cd D:\program\project\BKFlow
.\scripts\start-interface.ps1
```

**终端 2 - Frontend**
```powershell
cd D:\program\project\BKFlow\frontend
npm run dev
```

**配置模式**
```powershell
# 在第三个终端执行
cd D:\program\project\BKFlow
python switch_mode.py --mode simple
```

✅ 访问：https://localhost:9007

---

### 启动完整模式

**终端 1 - Interface**
```powershell
cd D:\program\project\BKFlow
.\scripts\start-interface.ps1
```

**终端 2 - Engine**
```powershell
cd D:\program\project\BKFlow
.\scripts\start-engine.ps1
```

**终端 3 - Frontend**
```powershell
cd D:\program\project\BKFlow\frontend
npm run dev
```

**配置模式**
```powershell
# 在第四个终端执行
cd D:\program\project\BKFlow
python switch_mode.py --mode full
```

✅ 访问：https://localhost:9007

---

## 🔄 模式切换

### 检查当前模式
```powershell
python switch_mode.py --check
```

### 切换到简化模式
```powershell
python switch_mode.py --mode simple
```

### 切换到完整模式
```powershell
python switch_mode.py --mode full
```

---

## 🔍 检查服务状态

```powershell
python check_services.py
```

---

## 📊 服务端口总览

| 服务 | 端口 | 简化模式 | 完整模式 |
|------|------|----------|----------|
| Interface | 8000 | ✅ 必需 | ✅ 必需 |
| Engine | 8001 | ❌ 不需要 | ✅ 必需 |
| Frontend | 9007 | ✅ 必需 | ✅ 必需 |

---

## 🎯 功能对比

| 功能 | 简化模式 | 完整模式 |
|------|----------|----------|
| 空间管理 | ✅ | ✅ |
| 模板管理 | ✅ | ✅ |
| 插件管理 | ✅ | ✅ |
| **任务执行** | ❌ | ✅ |
| **任务列表** | ❌ | ✅ |
