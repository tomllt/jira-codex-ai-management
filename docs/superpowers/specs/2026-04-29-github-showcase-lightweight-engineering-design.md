# GitHub Showcase Lightweight Engineering Design

**Date:** 2026-04-29
**Project:** Jira + Codex AI Management
**Status:** Approved for planning

## Goal

Make the repository present well as a public-facing technical prototype without overstating its maturity. The result should improve discoverability, first-impression clarity, and baseline engineering hygiene while preserving the current product behavior and lightweight repo structure.

## Scope

This design covers four changes only:

1. Add an `Apache-2.0` license.
2. Improve GitHub repository metadata for public-style presentation.
3. Add a lightweight GitHub Actions CI workflow with no external service dependencies.
4. Restructure `README.md` so the first screen explains the project clearly to external readers.

## Non-Goals

- No code refactor
- No new product features
- No Jira integration changes
- No real `codex exec` automation in CI
- No packaging or release setup such as `pyproject.toml`, PyPI publishing, or versioned releases
- No attempt to present the project as production-ready software

## Target Audience

The primary audience is an external technical reader who discovers the repository on GitHub and needs to understand:

- what the project is,
- why it exists,
- what it can already do,
- how it is structured,
- how far along it really is.

The repository should still remain usable for the current owner as an active prototype workspace.

## Design Principles

### Honest Positioning

The repository must clearly describe itself as a validated prototype, not as a mature platform. Public-facing polish is useful only if it stays consistent with the actual implementation state.

### Lightweight Engineering

All additions should be low-maintenance. CI should validate the repository's most important local contracts without introducing brittle infrastructure or dependency-heavy setup.

### Discovery Before Detail

The top of the README should answer "what is this?" and "why should I care?" before it dives into local setup, verification notes, or document inventory.

### Preserve Existing Working Shape

The current `scripts/`, `schemas/`, `prompts/`, and `docs/` layout remains the canonical structure for this milestone. This design improves presentation around that structure rather than changing it.

## Repository Metadata Design

### Description

Set the GitHub repository description to:

`AI-assisted Jira orchestration prototype for turning approved work into Codex-executable tasks with structured writeback.`

This wording is short, externally understandable, and aligned with the repository's actual capabilities.

### Homepage

Leave the GitHub homepage unset for now. There is no separate project site, and pointing it back to the repository would add no value.

### Topics

Set the repository topics to:

- `jira`
- `codex`
- `ai-agent`
- `workflow-automation`
- `project-management`
- `developer-tools`
- `python`
- `prototype`
- `llm-orchestration`

These topics optimize for discoverability without diluting the repository's focus.

## License Design

Add a root `LICENSE` file using `Apache License 2.0`.

### Rationale

- It is suitable for a technical prototype that may later be shared more broadly.
- It provides a clearer legal posture than leaving the repository unlicensed.
- It is more protective than MIT in one important respect: explicit patent language.

## README Design

`README.md` should be reorganized around the following structure.

### 1. Title And One-Sentence Positioning

Open with the project name and a concise explanation that this is a Jira + Codex collaboration prototype for turning approved work into executable AI tasks with structured execution feedback.

### 2. What It Is

Explain the system in 2-3 short paragraphs:

- Jira handles workflow governance, auditability, and scheduling boundaries.
- Codex CLI handles analysis, task preparation, and execution work inside those boundaries.
- The repository implements the orchestration layer, schemas, prompts, and prototype CLI flows that connect them.

### 3. Why It Exists

Describe the problem framing:

- AI should contribute earlier than code generation alone.
- Human operators should retain control over sprint planning and governance fields.
- Approved work should move through a structured, auditable execution loop.

### 4. Core Capabilities

List the highest-signal currently implemented capabilities, such as:

- structured Story / Task creation from plan artifacts,
- ready-task querying,
- task claim and writeback,
- dry-run and real Codex execution scaffolding,
- preflight and task-fix preparation flows.

Keep this section short and outcome-oriented.

### 5. Architecture

Describe the four main pieces:

- Jira
- Codex CLI
- Orchestrator CLI
- Schemas / Prompts / Examples

This section should explain boundaries, not implementation minutiae.

### 6. Quick Start

Keep only the minimum useful commands:

- copy `.env.example`
- run config check
- run Jira check
- validate example schemas
- create example plan or query ready work

Avoid long command dumps near the top of the file.

### 7. Current Status

State explicitly that:

- the repository is a validated prototype,
- core local Jira integration and prototype orchestration have been exercised,
- real execution still depends on valid task context and local tool availability.

This section is the honesty anchor for the rest of the README.

### 8. Roadmap

Compress the future work into a readable progression:

- documentation and prototype baseline,
- engineering refactor,
- governance hardening,
- continuous dispatch and visibility.

The roadmap should be directional rather than overloaded with internal planning detail.

### 9. Docs Index

Move the detailed document list to the lower part of the README as a reference section.

### README Content Rules

- Keep the primary narrative in Chinese.
- Keep the first screen shorter than the current README.
- Move detailed local validation notes further down.
- Do not remove useful information; reorganize it by reader priority.

## CI Design

Add a GitHub Actions workflow at `.github/workflows/ci.yml`.

### Triggers

- `push` to `main`
- `pull_request` targeting `main`

### Runner

- `ubuntu-latest`

### Python Version

Use a single current stable Python version to minimize maintenance burden. No version matrix is needed for this milestone.

### Checks

Run the following commands:

```bash
python -m py_compile scripts/*.py
python scripts/orchestrator.py --help
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
```

### CI Boundaries

The workflow must not:

- require `.env`,
- call the local Jira server,
- call real `codex exec`,
- assume package managers or external runtimes beyond Python itself.

### Rationale

This CI validates the repo's most important zero-dependency contracts:

- the scripts still parse,
- the main CLI still starts,
- the documented example schemas remain valid.

That is enough to catch accidental breakage without creating noisy failures from environment-coupled behavior.

## Files To Change

- `LICENSE`
- `README.md`
- `.github/workflows/ci.yml`

The GitHub repository settings will also be updated for description and topics.

## Acceptance Criteria

The work is successful when all of the following are true:

1. The repository has an `Apache-2.0` license at the root.
2. The GitHub repository description and topics match the public-facing positioning above.
3. The README first screen explains the project clearly to an external reader without hiding its prototype status.
4. A GitHub Actions workflow exists and passes using only local, dependency-light checks.
5. No product behavior, orchestration logic, or runtime integration semantics are changed by this work.

## Risks

### Overselling The Project

If the README becomes too polished without preserving the prototype caveats, external readers may infer production readiness. The `Current Status` section must prevent that.

### CI Drift

If CI grows beyond zero-dependency checks, it may become flaky or misleading. This design intentionally keeps the workflow narrow.

### README Regression For Local Use

The current README contains detailed local notes that are still useful. Reorganization must preserve them lower in the file rather than deleting them.

## Recommended Next Step

After this spec is reviewed, the next action is to create an implementation plan that executes the metadata update, file changes, CI workflow, and verification steps in a small number of low-risk tasks.
