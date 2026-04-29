# 工作流设计

## 目标流程

整体流程分为三段：

1. AI 规划建单
2. 人工排期发车
3. AI Sprint 内执行

## 端到端流程

### 1. 需求进入 Jira

- 产品、项目经理或其他上游系统创建 `Epic` / 需求单
- Epic 描述中包含背景、目标、约束、验收标准、范围等内容

### 2. AI 分析需求

- `Jira Skill` 读取 Epic 内容
- `Codex CLI` 分析需求并输出结构化结果
- 输出内容包括：
  - 需求摘要
  - 建议 Story 列表
  - 每个 Story 的 AC
  - 每个 Story 的 Task 拆解
  - 风险与依赖
  - 需要人工确认的问题

### 3. 自动创建 Story / Task

- `Jira Skill` 根据结构化结果自动创建 `Story` 和 `Task`
- 创建后的 issue 初始状态为 `AI Drafted`
- 自动写入标签、AC、DoD、技术说明、执行提示等字段

### 4. 人工审核与 Sprint 排期

- 负责人在 backlog 中审核 AI 生成的 Story / Task
- 人工修订标题、描述、边界、优先级、估时等内容
- 人工决定是否放入 Sprint
- 人工将准备好的执行任务状态改为 `Ready for Codex`

### 5. Codex 从 Sprint 拉取任务

- `Orchestrator` 或 Runner 定时查询当前 Sprint
- 只拉取满足以下条件的任务：
  - 在当前 Sprint
  - 状态为 `Ready for Codex`
  - 标签包含 `codex`
  - 必填字段完整

### 6. Codex 执行任务

- `Codex CLI` 领取任务并改状态为 `Codex In Progress`
- 读取 Jira 任务上下文与代码仓库上下文
- 完成代码修改、验证、结果整理

### 7. 回写执行结果

- `Jira Skill` 回写 comment、风险、测试结果、产出链接
- 状态更新为：
  - `Human Review`，表示已执行完成待人工复核
  - 或 `Codex Blocked`，表示执行中遇到阻塞

### 8. 人工复核与完成

- 人工检查代码、PR、测试、回写说明
- 决定是否合并、补充修改或完成任务
- 人工或自动规则将任务状态置为 `Done`

## 职责边界

### Jira

- 唯一任务事实源
- 唯一流程审计源
- Sprint 规划与协作中心

### AI 规划层

- 需求分析
- Story 定义
- Task 拆解
- 技术说明补全
- 自动建单

### Codex 执行层

- 只处理 Sprint 内批准执行的任务
- 执行代码变更与验证
- 回写执行结果与执行态状态

## 治理原则

- AI 可自动建 `Story` / `Task`
- 人工保留 Sprint、优先级、资源调度控制权
- `Codex CLI` 不消费 backlog 中未排期任务
- `Codex CLI` 不修改治理类关键字段
- 所有 AI 操作必须留痕
