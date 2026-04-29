# Skill 与架构草图

## 模块角色

### Jira Skill

负责与 Jira API 交互，并完成结构化数据的落表与回写。

职责包括：

- 读取 Epic / Story / Task 内容
- 创建 Story / Task / Comment
- 更新字段、标签、状态
- 按 JQL 查询 Sprint 中的可执行任务
- 记录执行结果与审计信息

### Codex CLI

负责高认知分析与执行。

职责包括：

- 分析需求
- 生成 Story / Task 方案
- 结合代码仓库进行设计分析
- 执行 Sprint 中的开发任务
- 输出结构化执行结果

### Orchestrator

负责编排 Jira Skill 与 Codex CLI。

职责包括：

- 触发 Epic 分析流程
- 调用 Codex 生成 Story / Task 结构化结果
- 调用 Jira Skill 自动建单
- 定时读取 Sprint 任务
- 为 Codex 组装执行上下文
- 回写执行结果

## 核心 Skill 建议

### `jira-requirement-analyzer`

输入：Epic / 需求单

输出：

- 需求摘要
- 目标与边界
- 风险与依赖
- 建议 Story 列表

### `jira-story-task-generator`

输入：Epic 或 Story

输出：

- Story 草案
- Task / Sub-task 草案
- AC / DoD / 标签 / 执行提示

### `jira-sprint-dispatch-reader`

输入：Sprint 或 JQL

输出：

- 当前 Sprint 中 `Ready for Codex` 的任务列表

### `jira-execution-updater`

输入：issue key + 执行结果

输出：

- 状态更新
- comment 回写
- 风险与阻塞说明

## 接口建议

### 需求分析阶段

- `generate_from_epic(epic_key) -> plan_json`
- `create_issues(plan_json) -> created_issue_keys`

### Sprint 执行阶段

- `fetch_ready_tasks(sprint_id | jql) -> task_list`
- `claim_task(issue_key) -> success/fail`
- `run_task(task_context) -> execution_result_json`
- `update_task_result(execution_result_json) -> jira_updated`

## 任务消费规则

建议 Runner 只消费满足以下条件的任务：

- 处于当前 Sprint
- 状态为 `Ready for Codex`
- 标签包含 `codex`
- 关键字段完整

建议 JQL：

```jql
project = PROJ
AND sprint in openSprints()
AND issuetype in (Task, Sub-task)
AND status = "Ready for Codex"
AND labels = codex
ORDER BY priority DESC, created ASC
```

## 审计与安全

- AI 建单与执行回写全部写 comment 或字段留痕
- `Codex CLI` 不允许更改 Sprint、Priority、Assignee 等治理字段
- 不允许自动关闭 Story / Epic
- 阻塞任务必须回写明确原因和所需人工输入
