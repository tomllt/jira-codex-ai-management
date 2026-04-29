# Roadmap: Jira + Codex AI Management

## Overview

这个项目已经完成文档沉淀和一轮可运行原型验证，后续路线不再是“从零构思”，而是把现有 Jira + Codex 闭环工程化、分层化并治理化。路线图因此从 brownfield 现状出发，先解决包结构、测试与职责边界，再补齐真实执行加固、Jira 字段治理、持续消费和指标能力。

## Phases

- [ ] **Phase 1: Layered Refactor Foundation** - 建立 `src/jira_codex` 包骨架、兼容 shim 和基础测试，为后续平移提供安全落点。
- [ ] **Phase 2: Application Extraction And CLI Slimming** - 把 planner、Jira adapter、Codex runner 与 orchestrator 逻辑从脚本入口拆到明确层级。
- [ ] **Phase 3: Real Execution Hardening** - 强化 requirement-to-task 质量、真实 repo 上下文校验和真实 Codex 执行闭环。
- [ ] **Phase 4: Jira Governance And Data Enrichment** - 增加自定义字段映射、Epic 链路增强、claim 审计与治理约束。
- [ ] **Phase 5: Continuous Dispatch And Visibility** - 增加持续消费入口、运行健康信息和关键运营指标。

## Phase Details

### Phase 1: Layered Refactor Foundation
**Goal**: 以不破坏现有 CLI 的方式创建 `src/jira_codex` 分层包、迁移首批低风险模块，并建立最小测试骨架。
**Depends on**: Nothing (first phase)
**Requirements**: ARCH-01, ARCH-02
**Success Criteria** (what must be TRUE):
1. User can import project code from `src/jira_codex` without breaking existing `scripts/*.py` command entry points.
2. Configuration, schema validation, and Jira client responsibilities exist in explicit package locations instead of only in top-level scripts.
3. The repository contains a working unit-test layout that protects the first migration steps.
**Plans**: 3 plans

Plans:
- [ ] 01-01: Create `src/jira_codex` package skeleton, test directories, and compatibility import strategy
- [ ] 01-02: Migrate settings, schema validator, and Jira client into package modules with compatibility shims
- [ ] 01-03: Add initial unit tests and sync implementation docs with the refactor baseline

### Phase 2: Application Extraction And CLI Slimming
**Goal**: 让 CLI 只负责参数解析与分发，把核心应用逻辑移入更清晰的 application / adapters / domain 边界。
**Depends on**: Phase 1
**Requirements**: ARCH-03, INTK-01, INTK-02, EXEC-01, EXEC-02
**Success Criteria** (what must be TRUE):
1. User can run the same orchestrator commands after the migration with no behavior regression at the CLI boundary.
2. Planning, search-ready, claim, and writeback flows are callable through package services rather than only script-local functions.
3. Refactor-sensitive paths are covered by tests that fail if imports or contracts drift.
**Plans**: 4 plans

Plans:
- [ ] 02-01: Extract planner, comment-builder, and JQL helpers into package modules
- [ ] 02-02: Move orchestrator command handlers behind application services
- [ ] 02-03: Define lightweight domain contracts for task context, execution result, and writeback mapping
- [ ] 02-04: Expand tests around CLI compatibility and package-level service behavior

### Phase 3: Real Execution Hardening
**Goal**: 提升 requirement 起草质量与真实任务执行可靠性，避免“能调起但无法落地”的任务进入执行。
**Depends on**: Phase 2
**Requirements**: EXEC-03, EXEC-04, INTK-03, READY-01, READY-02, READY-03
**Success Criteria** (what must be TRUE):
1. User can validate a task's local repo context before execution and see actionable remediation guidance when it is invalid.
2. User can execute a real Jira task against a real local repository with deterministic timeout and structured result handling.
3. Requirement-derived tasks contain fewer placeholder values and a clearer path to become executable.
**Plans**: 4 plans

Plans:
- [ ] 03-01: Harden `prepare-task` / preflight rules for repo, module, and test-command fidelity
- [ ] 03-02: Improve planner output quality and reduce placeholder `TODO` scope fields
- [ ] 03-03: Validate real `run-task` flows against known local repositories and capture failure modes
- [ ] 03-04: Add tests for execution result handling, timeout behavior, and writeback mapping

### Phase 4: Jira Governance And Data Enrichment
**Goal**: 让 Jira 中的执行上下文和治理边界更稳定，减少对自由文本描述的脆弱依赖。
**Depends on**: Phase 3
**Requirements**: GOV-01, GOV-02, GOV-03
**Success Criteria** (what must be TRUE):
1. User can configure or map Jira custom fields for execution context and AI result fields.
2. Task / Story / Epic relationships are written back with clearer lineage and less manual补录.
3. Claim and blocked flows leave enough audit context to diagnose double-consumption or handoff failures.
**Plans**: 4 plans

Plans:
- [ ] 04-01: Introduce configurable Jira field mapping for repo/workdir/result metadata
- [ ] 04-02: Add Epic / Story linkage enrichment in issue creation and writeback flows
- [ ] 04-03: Strengthen claim semantics, audit markers, and blocked-state diagnostics
- [ ] 04-04: Sync docs, examples, and schemas with the governed Jira model

### Phase 5: Continuous Dispatch And Visibility
**Goal**: 把单次执行入口扩展为可持续运行的受控消费流程，并补齐关键健康指标。
**Depends on**: Phase 4
**Requirements**: OPS-01, OPS-02
**Success Criteria** (what must be TRUE):
1. User can run a safe loop that continuously polls ready tasks and processes them one at a time.
2. User can inspect basic operational metrics such as success, blocked, and suggestion adoption rates.
3. Operators can understand whether the system is ready for unattended use from the generated outputs.
**Plans**: 3 plans

Plans:
- [ ] 05-01: Implement `run-loop` or equivalent dispatcher with conservative execution semantics
- [ ] 05-02: Capture and report blocked, success, and remediation metrics
- [ ] 05-03: Add operator-facing documentation and verification steps for continuous use

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Layered Refactor Foundation | 0/3 | Not started | - |
| 2. Application Extraction And CLI Slimming | 0/4 | Not started | - |
| 3. Real Execution Hardening | 0/4 | Not started | - |
| 4. Jira Governance And Data Enrichment | 0/4 | Not started | - |
| 5. Continuous Dispatch And Visibility | 0/3 | Not started | - |
