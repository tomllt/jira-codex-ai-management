# Jira + Codex AI Management

一个面向 `Jira + Codex CLI` 协同的 AI 半自动化项目原型，用于沉淀并逐步实现需求分析、故事定义、任务拆解、Jira 自动建单、Sprint 内任务执行与状态回写。

## 目标

- 让 AI 自动分析需求并生成 `Story` / `Task`
- 保持人工掌握 Sprint 排期与分发权
- 让 `Codex CLI` 只消费 Sprint 中批准执行的任务
- 允许 `Codex CLI` 更新执行态状态并回写执行结果
- 建立可审计、可扩展的 Jira 管理赋能方案

## 当前文档

- `docs/overview.md`：整体定位、目标、能力边界
- `docs/workflow.md`：端到端流程与职责划分
- `docs/mvp-spec.md`：MVP 详细规格
- `docs/skills-architecture.md`：Jira Skill / Orchestrator / Codex CLI 架构草图
- `docs/data-models.md`：字段、状态、JSON Schema 与模板
- `docs/implementation.md`：当前实现方式与命令
- `docs/roadmap.md`：分阶段落地建议
- `docs/README.md`：文档索引

## Prototype 资产

- `schemas/ai-plan.schema.json`：Epic 分析输出 schema
- `schemas/execution-result.schema.json`：任务执行结果 schema
- `prompts/epic_to_plan.prompt.md`：Epic -> Story/Task 规划 prompt
- `prompts/task_execution.prompt.md`：Sprint Task 执行 prompt
- `examples/sample-ai-plan.json`：建单示例
- `examples/sample-execution-result.json`：执行结果示例
- `examples/sample-jira-comment.md`：Jira comment 示例
- `scripts/config.py`：环境变量与配置加载
- `scripts/jql.py`：Ready-for-Codex JQL 生成
- `scripts/comment_builder.py`：执行结果 comment 构建
- `scripts/jira_client.py`：轻量 Jira REST Client
- `scripts/schema_validate.py`：轻量 schema 校验
- `scripts/codex_runner.py`：Codex 执行 runner
- `scripts/orchestrator.py`：原型编排器 CLI
- `.env.example`：配置模板
- `PROTOTYPE.md`：原型目录说明

## 当前本地 Jira 接入

当前已探测到本地 Docker Jira：

- 本地访问地址：`http://127.0.0.1:18080`
- 容器名：`jira-software`
- 部署类型：`Jira Server`
- 版本：`8.16.1`
- 推荐 API 版本：`2`

## 当前已实现能力

当前项目已经包含：

- 分析文档与数据契约
- Story / Task 自动建单
- Ready 任务查询
- 任务 claim
- Dry-run 执行结果生成
- Jira comment / label / 状态回写
- `run-task` 单任务执行入口
- `run-next` 单次消费入口
- 轻量 schema 校验
- 真实 `codex exec` 接入骨架
- `/root/.codex` 配置显式接入
- `Workdir` 自动解析与 `-C` 执行
- `Module` / `Workdir` 一致性预检
- `Test Command` 可执行环境预检
- `pnpm -> corepack pnpm` 自动兼容尝试
- `preflight-task` 任务可执行性审查
- `suggest-task-fixes` 任务 scope 修正建议
- `apply-task-fixes` 一键应用建议修正
- `apply-task-fixes --dry-run/--only/--exclude` 审批式应用
- `prepare-task` 聚合建议/应用/preflight
- `draft-plan-from-requirement` / `create-from-requirement` 需求入口
- `set-workdir` Jira 描述修正命令
- `refine-task-scope` Jira 任务范围精修命令
- `--timeout` 执行超时控制

## 当前真实 Codex 状态

已确认：

- 本机存在 `codex`
- `codex exec` 可用
- `CodexRunner` 现在显式使用：
  - `CODEX_HOME=/root/.codex`
  - `HOME=/root`
- 真实调用时不再出现认证 `401`
- `/root/.codex` 中的 provider 已生效，验证输出显示为 `univibe`

当前新的关键前提是：

- Jira task 里的 `Workdir` 必须是真实存在的本机仓库路径
- Jira task 里的 `Module` / `Test Command` 也必须和目标仓库实际结构一致
- 真实执行前还需要满足对应语言/包管理器工具在 PATH 中可用

## 快速开始

```bash
cp .env.example .env
python scripts/orchestrator.py check-config
python scripts/orchestrator.py check-jira
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py create-from-plan examples/sample-ai-plan.json
python scripts/orchestrator.py search-ready --limit 10
python scripts/orchestrator.py run-next --dry-run --no-writeback
```

更多命令见 `docs/implementation.md`。

## 已验证结果

已经在本地 Jira `ON` 项目中验证：

- 创建测试任务：`ON-1`
- 创建样例故事：`ON-2`、`ON-8`
- 创建样例任务：`ON-3`、`ON-9`
- `search-ready` 能检索 ready 任务
- `claim` 能更新状态和标签
- `run-task --dry-run` 能回写 comment 和标签
- `run-next --dry-run --no-writeback` 能自动消费下一条 ready 任务
- 真实 `codex exec` 已通过 `/root/.codex` 配置成功启动并返回结果
- 真实执行已验证到 `Workdir` 检查阶段

## 下一步建议

1. 确定真实仓库路径并更新 Jira task 的 `Workdir`
2. 用 `run-task --timeout 300` 做一次真实执行验证
3. 增加 Jira 自定义字段映射
4. 增加 `run-loop` 持续消费 ready 任务
5. 增加 Epic 关联字段写入
