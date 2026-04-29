# Jira + Codex AI Management

## What This Is

这是一个把 Jira 项目管理流程与 Codex CLI 执行能力接起来的 Python CLI 原型。它面向研发团队，把需求分析、Story/Task 拆解、Sprint 内任务消费、执行结果回写和审计留痕放进同一条可控流水线。当前仓库已经验证了原型闭环，接下来的工作重点是把脚本式实现沉淀为可持续演进的分层应用。

## Core Value

已批准进入执行边界的 Jira 任务，能够被 Codex 稳定消费、执行并以结构化结果回写，且全过程保持人工治理权与审计可追踪。

## Requirements

### Validated

- ✓ Story / Task 可由结构化 plan 自动创建并写入 Jira
- ✓ `Ready for Codex` 任务可被查询、claim、dry-run 执行并回写 comment / label / 状态
- ✓ Jira task 的 `Repo` / `Workdir` / `Module` / `Test Command` 已可用于执行前预检
- ✓ `prepare-task`、`suggest-task-fixes`、`apply-task-fixes` 已能支持执行前修正
- ✓ `draft-plan-from-requirement` / `create-from-requirement` 已形成需求入口原型

### Active

- [ ] 将当前 `scripts/` 原型重构为 `src/jira_codex` 分层包结构，并保持 CLI 兼容
- [ ] 为配置、schema、Jira 适配器、执行器与 orchestrator 建立可维护的测试覆盖
- [ ] 完成真实 Codex 执行场景下的任务上下文、工具依赖与回写链路加固
- [ ] 增加 Jira 自定义字段映射、Epic 关联增强、run-loop 与治理指标

### Out of Scope

- 自动排 Sprint 或自动决定优先级 — 当前目标是增强执行，不接管项目治理
- 自动分配 Assignee — 人工保留资源调度权
- 自动关闭 Story / Epic — 避免 AI 越权改变治理里程碑
- 完整 Web 控制台 — 当前仓库以 Python CLI 和 Jira 集成为主

## Context

- 当前代码库是单层根目录结构，核心实现仍集中在 `scripts/`
- 已有文档覆盖定位、流程、MVP 规格、数据模型、架构草图、实现方式和后续路线
- 已验证本地 Jira Server (`8.16.1`) 接入、真实 `codex exec` 调起、以及 `Workdir`/`Module`/`Test Command` 预检链路
- 当前主要问题不再是“能否跑起来”，而是“如何把原型稳定演进成可维护系统”
- 文档存在少量状态漂移，例如部分“未实现”描述已被代码局部覆盖，但未同步更新

## Constraints

- **Tech stack**: Python 3 + argparse + urllib + Codex CLI + Jira REST API — 当前实现与运行环境已围绕此组合建立
- **Compatibility**: 重构期间必须保持现有 `scripts/orchestrator.py` 命令可用 — 避免中断已验证的原型流程
- **Governance**: Codex 不得修改 Sprint、Priority、Assignee、Fix Version 等治理字段 — 人工保留排期与资源控制权
- **Execution context**: Jira task 必须提供真实 `Workdir`、匹配的 `Module Scope` 与可执行 `Test Command` — 否则真实执行无法落地
- **Runtime**: 当前仓库刚接入 GSD 管理，后续计划与执行应以 `.planning/` 为事实源 — 避免文档与实施再次分叉

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Jira 作为任务事实源与审计源 | 保持研发协作与 AI 行为留痕集中在同一系统 | ✓ Good |
| Codex 只消费进入执行边界的任务 | 防止 AI 越过人工排期与审批边界 | ✓ Good |
| 使用结构化 JSON 契约承接 AI 规划与执行回写 | 降低 Jira 写回与后续自动化的歧义 | ✓ Good |
| 短期保留 `scripts/` 兼容入口，长期迁移到 `src/jira_codex` | 允许在不中断现有 CLI 的前提下完成分层重构 | — Pending |
| 先补齐工程化和治理能力，再扩展持续消费与指标 | 当前主要风险在可维护性与可控性，而不是功能想象空间 | — Pending |

---
*Last updated: 2026-04-29 after GSD docs ingest bootstrap*
