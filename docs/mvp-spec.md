# MVP 详细规格

## MVP 目标

- 支持 AI 从 Epic 自动生成 `Story` / `Task`
- 保证人工负责 Sprint 排期与任务分发
- 保证 `Codex CLI` 只消费当前 Sprint 的可执行任务
- 允许 `Codex CLI` 更新执行状态并回写结果
- 形成可审计、可扩展的 AI 管理闭环

## MVP 范围

### 包含

- Epic 分析
- Story / Task 自动创建
- Sprint 内任务拉取
- Codex 执行状态更新
- Comment 回写
- 风险与阻塞回写

### 不包含

- 自动排 Sprint
- 自动关闭 Epic
- 自动决定优先级
- 自动分配 Assignee
- 自动发布上线

## Issue 类型

- `Epic`：需求和目标入口
- `Story`：用户价值或业务能力切片
- `Task`：可执行交付项
- `Sub-task`：MVP 可选，后续按团队习惯引入

## 状态模型

### Story 状态

- `AI Drafted`
- `Ready for Sprint`
- `In Sprint`
- `Done`

### Task 状态

- `AI Drafted`
- `Ready for Sprint`
- `Ready for Codex`
- `Codex In Progress`
- `Codex Blocked`
- `Human Review`
- `Done`

## 状态流转规则

### AI 允许

- 创建 `Story` / `Task`
- 初始状态设为 `AI Drafted`

### 人工允许

- `AI Drafted` -> `Ready for Sprint`
- `Ready for Sprint` -> 放入 `Sprint`
- 进入 Sprint 后改为 `Ready for Codex`

### Codex 允许

- `Ready for Codex` -> `Codex In Progress`
- `Codex In Progress` -> `Human Review`
- `Codex In Progress` -> `Codex Blocked`

### 人工或自动规则允许

- `Human Review` -> `Done`

## 字段权限边界

### Codex 不允许修改

- `Sprint`
- `Priority`
- `Story Points`
- `Assignee`
- `Fix Version`

### Codex 允许修改

- `Status`
- `Comment`
- `Labels`
- `AI Result Summary`
- `AI Risk Notes`
- `PR Link`
- `Commit Link`

## Sprint 执行准入规则

一个任务只有满足以下条件才允许进入 `Ready for Codex`：

- 已进入当前 Sprint
- 标签包含 `codex`
- `Repo` 不为空
- `Workdir` 不为空
- `Acceptance Criteria` 不为空
- `Definition of Done` 不为空
- 依赖和阻塞已明确

## 任务领取逻辑

为避免多个执行器抢占同一任务，使用“先抢锁再执行”的模型：

1. 查询 Sprint 内符合条件的候选任务
2. 原子更新状态为 `Codex In Progress`
3. 写入执行代理标记与开始时间
4. 更新成功后才真正开始执行

## 执行结果回写

执行完成后，回写以下内容：

- 状态变更
- 执行摘要
- 修改文件列表
- 测试命令与结果
- 风险与阻塞
- 下一步建议
- PR / Commit 链接

## 成功标准

- AI 自动生成 Story / Task 的采纳率较高
- 进入 `Ready for Codex` 的任务能够被稳定消费
- `Codex CLI` 执行成功后能稳定转入 `Human Review`
- 阻塞任务能明确给出原因与所需人工输入
- 整体流程具备可追踪与可审计性
