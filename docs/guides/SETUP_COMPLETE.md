# ✅ BKFlow 双模式配置完成

## 🎉 配置完成清单

已为您创建以下文件和脚本：

### 📂 启动脚本
- ✅ `scripts/start-interface.ps1` - 启动 Interface 模块
- ✅ `scripts/start-engine.ps1` - 启动 Engine 模块

### 🔧 工具脚本
- ✅ `switch_mode.py` - 模式切换工具
- ✅ `check_services.py` - 服务状态检查
- ✅ `disable_task_module.py` - 禁用任务模块
- ✅ `create_moduleinfo.py` - 创建 ModuleInfo
- ✅ `check_moduleinfo.py` - 检查 ModuleInfo

### 📖 文档
- ✅ `QUICK_START.md` - 快速启动指南
- ✅ `MODE_SWITCH_GUIDE.md` - 详细切换指南
- ✅ `TASK_MODULE_ISSUE.md` - 任务模块问题分析
- ✅ `CURRENT_STATUS.md` - 当前状态总结

---

## 🚀 现在您可以：

### 立即使用（简化模式）

**当前状态**：✅ 简化模式已激活

**正在运行**：
- ✅ Interface (8000)
- ✅ Backend (8000) 
- ❌ Engine (8001) - 不需要
- ❌ Frontend (9007) - 需要启动

**下一步**：
```powershell
# 启动前端
cd frontend
npm run dev
```

然后访问：https://localhost:9007

---

### 切换到完整模式

**步骤 1：切换模式**
```powershell
python switch_mode.py --mode full
```

**步骤 2：启动 Engine**
```powershell
# 打开新终端
.\scripts\start-engine.ps1
```

**步骤 3：验证**
```powershell
python check_services.py
```

应该看到：
```
[Interface] Running on localhost:8000
[Engine] Running on localhost:8001
[Frontend] Running on localhost:9007
Current Mode: Full Mode (Engine Enabled)
```

---

## 📝 快速命令参考

### 模式管理
```powershell
# 检查当前模式
python switch_mode.py --check

# 切换到简化模式
python switch_mode.py --mode simple

# 切换到完整模式
python switch_mode.py --mode full
```

### 服务管理
```powershell
# 检查服务状态
python check_services.py

# 启动 Interface
.\scripts\start-interface.ps1

# 启动 Engine
.\scripts\start-engine.ps1

# 启动 Frontend
cd frontend
npm run dev
```

---

## 🎯 两种模式对比

| 特性 | 简化模式 | 完整模式 |
|------|----------|----------|
| **终端数量** | 2 个 | 3 个 |
| **启动时间** | 快 ⚡ | 慢 🐌 |
| **学习曲线** | 简单 📚 | 复杂 📖📖 |
| **空间管理** | ✅ | ✅ |
| **模板管理** | ✅ | ✅ |
| **任务执行** | ❌ | ✅ |
| **任务列表** | ❌ | ✅ |
| **插件调试** | ⚠️ 有限 | ✅ 完整 |

---

## 💡 使用建议

### 第1-2周：使用简化模式
专注学习：
- 前端界面和组件
- 数据模型和 API
- 空间和模板概念
- 权限系统

### 第3周+：切换到完整模式
深入开发：
- 创建和执行任务
- 开发自定义插件
- 理解任务引擎
- 性能调优

---

## ⚠️ 注意事项

1. **切换模式不需要重启服务**
   - 只需运行 `python switch_mode.py --mode <模式>`
   - 然后刷新浏览器

2. **简化模式下避免访问任务页面**
   - 会显示 "ModuleInfo does not exist" 错误
   - 这是正常的，不影响其他功能

3. **完整模式需要确保 Engine 运行**
   - 检查：`python check_services.py`
   - 启动：`.\scripts\start-engine.ps1`

4. **数据库是共享的**
   - 两种模式使用同一个数据库
   - 切换模式不会丢失数据

---

## 🐛 故障排除

### 问题：前端显示 CSRF 错误
**解决**：清除浏览器缓存和 Cookie，刷新页面

### 问题：Engine 启动失败
**检查**：8001 端口是否被占用
```powershell
Get-NetTCPConnection -LocalPort 8001
```

### 问题：服务状态不正确
**检查**：
```powershell
python check_services.py
```

### 问题：不确定当前模式
**检查**：
```powershell
python switch_mode.py --check
```

---

## 📞 获取帮助

如果遇到问题，按以下顺序检查：

1. ✅ 检查服务状态：`python check_services.py`
2. ✅ 检查当前模式：`python switch_mode.py --check`
3. ✅ 查看详细文档：`MODE_SWITCH_GUIDE.md`
4. ✅ 查看快速指南：`QUICK_START.md`

---

## 🎓 学习路径建议

```
Week 1-2: 简化模式
  └─ 熟悉界面
  └─ 学习数据模型
  └─ 前端开发

Week 3: 完整模式
  └─ 创建简单任务
  └─ 理解执行流程
  └─ 查看执行日志

Week 4+: 深入开发
  └─ 自定义插件
  └─ 性能优化
  └─ 微服务架构
```

---

## ✨ 祝您学习愉快！

现在您已经拥有一个灵活的开发环境，可以：
- 🎯 根据需要自由切换模式
- 🔍 随时检查服务状态
- 📚 专注于不同的学习阶段
- 🚀 逐步掌握完整系统

开始探索 BKFlow 吧！
