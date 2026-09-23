# BKFlow 任务列表 404 错误 - 完整分析

## 问题现象

访问任务管理页面时报错：
```
ModuleInfo matching query does not exist.
```

解决后又出现：
```
Request API error, status_code: 404, url: http://localhost:8000/task/
```

---

## 根本原因

**BKFlow 是一个微服务架构的应用**，包含两个独立的模块：

### 1. Interface 模块（前端接口模块）
- **作用**：提供前端 API、用户界面相关的接口
- **当前状态**：✅ 运行在 localhost:8000
- **包含的功能**：
  - 空间管理 (`/api/space/`)
  - 模板管理 (`/api/template/`)
  - 权限管理 (`/api/permission/`)
  - 用户界面相关 API

### 2. Engine 模块（任务执行引擎）
- **作用**：执行具体的任务、管理任务状态
- **当前状态**：❌ 未运行
- **包含的功能**：
  - 任务列表 (`/task/`)
  - 任务执行
  - 节点操作
  - 任务状态查询

### 工作流程

```
用户访问任务页面
    ↓
前端请求: https://localhost:9007/task_admin/get_task_list/1/
    ↓
代理转发到: http://localhost:8000/task_admin/get_task_list/1/
    ↓
Interface 模块接收请求
    ↓
查询 ModuleInfo 表获取 Engine 模块地址
    ↓
调用 Engine 模块: {ModuleInfo.url}/task/?space_id=1&...
    ↓
❌ 404 错误：Engine 模块未运行
```

---

## 为什么会有这个架构？

1. **职责分离**
   - Interface 模块：轻量级，处理用户请求
   - Engine 模块：重量级，执行任务计算

2. **可扩展性**
   - 可以运行多个 Engine 实例来处理大量任务
   - Interface 模块可以分发任务到不同的 Engine

3. **隔离性**
   - 任务执行不会影响前端接口的响应
   - 可以独立重启、升级各个模块

---

## 解决方案

### 方案 1：启动 Engine 模块（推荐用于完整功能）

需要在另一个端口启动 Engine 模块：

1. **修改环境变量**
   创建 `.env.engine` 文件：
   ```bash
   # 复制 .env 并修改
   BKFLOW_MODULE_TYPE=engine  # 改为 engine
   BKFLOW_MODULE_CODE=default
   # 其他配置保持不变
   ```

2. **启动 Engine 服务**
   ```bash
   # 在新的终端窗口中
   export DJANGO_SETTINGS_MODULE=config.dev
   python manage.py runserver 0.0.0.0:8001 --settings=config.dev
   ```
   注意：需要加载 engine 专用的环境变量

3. **更新 ModuleInfo**
   ```python
   from bkflow.admin.models import ModuleInfo
   module = ModuleInfo.objects.get(space_id=1)
   module.url = 'http://localhost:8001'  # Engine 服务地址
   module.save()
   ```

### 方案 2：禁用任务管理功能（临时方案）

如果暂时不需要任务管理功能：

```python
# 删除 ModuleInfo 记录
from bkflow.admin.models import ModuleInfo
ModuleInfo.objects.filter(space_id=1).delete()
```

**结果**：
- ✅ 空间管理、模板管理等功能正常
- ❌ 任务列表页面会报 "ModuleInfo does not exist" 错误
- ❌ 无法创建和执行任务

### 方案 3：Mock Engine API（开发调试用）

创建一个简单的 mock 服务来模拟 Engine 模块的响应。

---

## 当前状态总结

| 模块 | 状态 | 端口 | 功能 |
|------|------|------|------|
| Interface | ✅ 运行中 | 8000 | 空间、模板、权限管理 |
| Engine | ❌ 未运行 | - | 任务执行 |
| Frontend | ✅ 运行中 | 9007 | 前端界面 |

**可用功能**：
- ✅ 登录（已禁用验证）
- ✅ 空间管理
- ✅ 模板管理
- ❌ 任务管理（需要 Engine 模块）

---

## 数据库表说明

### ModuleInfo 表
存储各个模块的连接信息：

| 字段 | 说明 | 示例值 |
|------|------|--------|
| space_id | 空间ID | 1 |
| code | 模块代码 | default |
| url | 模块访问地址 | http://localhost:8001 |
| token | 认证令牌 | local-dev-token |
| type | 模块类型 | TASK |
| isolation_level | 隔离级别 | only_calculation |

**作用**：Interface 模块通过这个表找到对应的 Engine 模块地址。

---

## 建议

### 对于本地开发环境：

1. **如果只需要测试界面**：使用方案 2，禁用任务功能

2. **如果需要完整功能**：使用方案 1，启动两个服务
   - Terminal 1: Interface (port 8000)
   - Terminal 2: Engine (port 8001)
   - Terminal 3: Frontend (port 9007)

3. **如果需要简化部署**：可以考虑修改代码，让 Interface 和 Engine 运行在同一进程中（需要修改架构）

---

## 下一步

请告诉我您想要哪个方案：
1. 启动 Engine 模块（需要我帮您配置）
2. 暂时禁用任务功能（专注于其他功能）
3. 创建 Mock Engine 服务（用于前端调试）
