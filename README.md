# Jira + Codex AI Management

[![CI](https://github.com/tomllt/jira-codex-ai-management/actions/workflows/ci.yml/badge.svg)](https://github.com/tomllt/jira-codex-ai-management/actions/workflows/ci.yml)
![License: Apache-2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

一个把 `Jira` 治理边界和 `Codex CLI` 执行能力连接起来的 AI 协同原型，用于把已批准的研发工作转成可执行任务，并以结构化结果回写到 Jira。

## What It Is

这是一个面向研发流程的 `Jira + Codex CLI` 协同原型。它不试图替代 Jira，也不试图让 AI 接管项目管理，而是把 AI 放进需求拆解、任务准备、执行落地和结果回写这条链路中。

在这个模型里：

- `Jira` 负责流程控制、任务审计、Sprint 边界和人工治理
- `Codex CLI` 负责分析、任务执行和结构化结果输出
- 当前仓库负责 Orchestrator、Schema、Prompt、示例数据和本地原型命令

## Why It Exists

很多 AI 工程实践只关注“生成代码”，但实际研发流程里，需求转 Story、Story 转 Task、Task 进入执行边界、执行结果回写和阻塞可追踪同样关键。

这个项目的目标是验证一条更完整的路径：

- AI 可以参与需求分析和任务准备
- 人工仍然保留 Sprint、优先级和资源调度控制权
- 已批准任务可以被 Codex 稳定消费并回写结果
- 全过程保持结构化输出和审计留痕

## Core Capabilities

当前仓库已经验证或包含以下原型能力：

- 基于结构化 plan 自动创建 Jira Story / Task
- 查询 Sprint 内 `Ready for Codex` 任务
- 任务 claim、执行状态流转和 comment / label 回写
- `run-task` / `run-next` 的 dry-run 与真实执行骨架
- `prepare-task` / `preflight-task` / `suggest-task-fixes` 的执行前守门流程
- 基于 Schema 的 planning / execution JSON 校验

## Architecture

### Jira

- 唯一任务事实源
- 唯一流程审计源
- Sprint 规划与治理中心

### Codex CLI

- 负责需求分析、任务执行和结构化结果输出
- 只处理进入执行边界的任务

### Orchestrator CLI

- 负责编排 Jira 与 Codex
- 负责建单、查询、claim、执行与回写入口

### Schemas / Prompts / Examples

- `schemas/`：结构化契约
- `prompts/`：需求分析与任务执行提示模板
- `examples/`：示例 plan、执行结果与 comment 数据

## Quick Start

```bash
cp .env.example .env
python scripts/orchestrator.py check-config
python scripts/orchestrator.py check-jira
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
python scripts/orchestrator.py search-ready --limit 10
```

更多命令和说明见 `docs/implementation.md`。

## Contributing And Security

- 协作说明见 `CONTRIBUTING.md`
- 安全问题与私下披露说明见 `SECURITY.md`

## Current Status

当前仓库是一个**已验证原型**，不是成熟产品。

已经确认的部分包括：

- 本地 Jira Server 接入可用
- `search-ready`、`claim`、`run-task --dry-run`、`run-next --dry-run` 已验证
- 真实 `codex exec` 已通过 `/root/.codex` 配置成功调起
- `Workdir` / `Module` / `Test Command` 的执行前校验链路已落地

当前限制仍然包括：

- 真实执行依赖 Jira task 中存在有效的 `Workdir`、`Module Scope` 和 `Test Command`
- 不同语言栈和本地工具链是否可用仍会影响真实执行
- 当前实现仍以 `scripts/` 原型结构为主，后续需要迁移到更清晰的工程化包结构

## Roadmap

当前路线聚焦在从“可运行原型”走向“可持续演进的工程化工具”：

1. 分层重构与测试骨架
2. Orchestrator / Adapter / Runner 职责收敛
3. 真实执行链路加固
4. Jira 字段治理与链路增强
5. 持续消费和运行可见性

更详细的阶段规划见：

- `docs/roadmap.md`
- `.planning/ROADMAP.md`

## Docs Index

- `docs/overview.md`：整体定位、目标、能力边界
- `docs/workflow.md`：端到端流程与职责划分
- `docs/mvp-spec.md`：MVP 详细规格
- `docs/skills-architecture.md`：Jira Skill / Orchestrator / Codex CLI 架构草图
- `docs/data-models.md`：字段、状态、JSON Schema 与模板
- `docs/implementation.md`：当前实现方式与命令
- `docs/roadmap.md`：分阶段落地建议
- `docs/README.md`：文档索引
- `docs/2026-04-28-refactor-implementation-plan.md`：原型分层重构实施计划

## Prototype Assets

- `schemas/ai-plan.schema.json`
- `schemas/execution-result.schema.json`
- `prompts/epic_to_plan.prompt.md`
- `prompts/task_execution.prompt.md`
- `examples/sample-ai-plan.json`
- `examples/sample-execution-result.json`
- `examples/sample-jira-comment.md`
- `scripts/orchestrator.py`

## Local Validation Notes

当前本地已验证的 Jira 环境：

- 地址：`http://127.0.0.1:18080`
- 部署类型：`Jira Server`
- 版本：`8.16.1`
- 推荐 API 版本：`2`

已经验证过的本地结果包括：

- 创建测试任务与样例 Story / Task
- Ready 任务检索
- claim 状态迁移
- dry-run comment / label 回写
- 真实 `codex exec` 调起

## License

This project is licensed under the Apache License 2.0. See `LICENSE`.
