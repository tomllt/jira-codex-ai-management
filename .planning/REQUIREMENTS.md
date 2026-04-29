# Requirements: Jira + Codex AI Management

**Defined:** 2026-04-29
**Core Value:** 已批准进入执行边界的 Jira 任务，能够被 Codex 稳定消费、执行并以结构化结果回写，且全过程保持人工治理权与审计可追踪。

## v1 Requirements

### Intake And Planning

- [ ] **INTK-01**: User can convert a Jira Epic or requirement document into an `ai-plan` JSON payload compatible with the project schema.
- [ ] **INTK-02**: User can create Jira Story / Task issues from a generated plan while preserving labels, acceptance criteria, definition of done, and technical context.
- [ ] **INTK-03**: Generated tasks always include either executable `Repo` / `Workdir` / `Module Scope` / `Test Command` values or an explicit remediation path.

### Execution And Writeback

- [ ] **EXEC-01**: User can query only Jira tasks that are in the current Sprint, marked for Codex, and otherwise eligible for execution.
- [ ] **EXEC-02**: User can claim a task for Codex execution and reflect running / blocked / review states back to Jira without changing governance fields.
- [ ] **EXEC-03**: User can execute a task in dry-run or real Codex mode with timeout control and structured JSON result output.
- [ ] **EXEC-04**: User can write back execution summary, changed files, test results, risks, blockers, and next-step context to Jira.

### Readiness And Quality Gates

- [ ] **READY-01**: User can assess whether a Jira task is executable by validating local `Workdir`, `Module Scope`, and `Test Command` before running Codex.
- [ ] **READY-02**: User can generate suggested task fixes and selectively apply them back to Jira before execution.
- [ ] **READY-03**: User can run a single preparation command that chains suggestion, optional apply, and preflight into one guardrail flow.

### Architecture And Maintainability

- [ ] **ARCH-01**: The codebase exposes a layered package under `src/jira_codex` while preserving current CLI behavior through compatibility shims.
- [ ] **ARCH-02**: Configuration loading, schema validation, Jira integration, and command orchestration each live in explicit package boundaries.
- [ ] **ARCH-03**: Core flows have unit tests that protect brownfield refactors from import or behavior regressions.

### Governance And Operations

- [ ] **GOV-01**: Codex automation cannot consume backlog work that has not been explicitly moved into the execution boundary.
- [ ] **GOV-02**: Jira custom field mapping for repository context and AI result fields is configurable instead of relying only on free-form description parsing.
- [ ] **GOV-03**: Task claiming and execution leave enough metadata to diagnose double-consumption, blockers, and review handoff failures.
- [ ] **OPS-01**: User can run a safe continuous dispatcher (`run-loop` or equivalent) that consumes ready tasks one at a time.
- [ ] **OPS-02**: User can inspect success rate, blocked rate, and AI suggestion adoption metrics for operational feedback.

## v2 Requirements

### Platform Extensions

- **PLAT-01**: User can operate the system from a richer UI or dashboard instead of CLI-only workflows.
- **PLAT-02**: User can coordinate multiple execution workers with explicit lock visibility and recovery flows.
- **PLAT-03**: User can integrate more project systems beyond the current local Jira Server setup.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Automatic sprint planning | Human must retain planning and prioritization control |
| Automatic assignee decisions | Resource allocation is a management responsibility, not an execution concern |
| Automatic Story / Epic closure | AI should not finalize governance milestones autonomously |
| Full web console in the current milestone | Immediate value is in hardening the Python CLI workflow and Jira integration |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ARCH-01 | Phase 1 | Pending |
| ARCH-02 | Phase 1 | Pending |
| ARCH-03 | Phase 2 | Pending |
| INTK-01 | Phase 2 | Pending |
| INTK-02 | Phase 2 | Pending |
| EXEC-01 | Phase 2 | Pending |
| EXEC-02 | Phase 2 | Pending |
| EXEC-03 | Phase 3 | Pending |
| EXEC-04 | Phase 3 | Pending |
| INTK-03 | Phase 3 | Pending |
| READY-01 | Phase 3 | Pending |
| READY-02 | Phase 3 | Pending |
| READY-03 | Phase 3 | Pending |
| GOV-01 | Phase 4 | Pending |
| GOV-02 | Phase 4 | Pending |
| GOV-03 | Phase 4 | Pending |
| OPS-01 | Phase 5 | Pending |
| OPS-02 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0

---
*Requirements defined: 2026-04-29*
*Last updated: 2026-04-29 after GSD docs ingest bootstrap*
