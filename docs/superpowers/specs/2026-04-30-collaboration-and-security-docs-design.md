# Collaboration And Security Docs Design

**Date:** 2026-04-30
**Project:** Jira + Codex AI Management
**Status:** Approved for planning

## Goal

Add a clear, lightweight collaboration layer for external contributors without overstating project maturity or introducing heavy governance overhead. The repository should make it obvious how to report bugs, suggest features, open pull requests, contribute safely, and disclose security concerns.

This design also acknowledges the repository's current state: the repo is private today. These collaboration assets should therefore work for invited collaborators immediately while also being suitable for a future public-facing state if repository visibility changes later.

## Scope

This design covers six repository-facing assets:

1. GitHub issue form for bug reports
2. GitHub issue form for feature requests
3. Pull request template
4. `CONTRIBUTING.md`
5. `SECURITY.md`
6. Small README enhancements for badges and contributor/security entry points

## Non-Goals

- No product behavior changes
- No Jira workflow or Codex execution logic changes
- No GitHub Discussions setup
- No Code of Conduct
- No support policy or SLA document
- No enterprise-style approval workflow
- No large README rewrite beyond the small collaboration-related additions

## Audience

This work serves three reader types:

- Invited collaborators who can access the private repository today
- Future external contributors if the repository is made public later
- Maintainers who need better issue quality and clearer contributor expectations
- Security-conscious readers who need to know what should be reported privately

## Design Principles

### Open But Governed

The repository should welcome collaboration, including code contributions, while still protecting the project's workflow boundaries and prototype status. Because the repository is currently private, the first practical audience is invited collaborators rather than anonymous public drive-by contributors.

### Lightweight By Default

The new templates and docs should collect only the information that materially improves review quality. They should not feel like enterprise intake forms.

### Reality-Aligned Safety

`SECURITY.md` should reflect the real sensitive surfaces in this repository: credentials, `.env`, local Jira access, local workdir paths, and real `codex exec` context.

### Consistency With Existing Style

The repository already prefers structured artifacts and explicit execution context. The issue forms, PR template, and collaboration docs should extend that same style.

## File Design

### `.github/ISSUE_TEMPLATE/bug_report.yml`

Use GitHub issue forms rather than a freeform Markdown template.

The form should collect:

- required: concise summary
- required: reproduction steps
- required: expected behavior
- required: actual behavior
- required: affected area
- optional: local environment notes
- required: whether Jira, Codex, local toolchain, schema, docs, or CI are involved
- optional: screenshots or logs

#### Purpose

Improve diagnostic quality without overwhelming reporters. The key distinction is whether the report describes a repository defect or an environment/setup mismatch.

### `.github/ISSUE_TEMPLATE/feature_request.yml`

Use a GitHub issue form focused on problem framing rather than implementation prescription.

The form should collect:

- required: concise request summary
- required: current pain point or missing capability
- required: proposed improvement
- optional: alternatives considered
- required: expected user value
- required: whether the change affects Jira governance boundaries
- required: whether the change affects Codex execution boundaries

#### Purpose

Prevent feature requests from becoming vague idea dumps. Encourage requests that acknowledge the repository's workflow model and product boundaries.

### `.github/pull_request_template.md`

Add a short, structured PR template.

Sections should include:

- summary
- why this change exists
- scope
- testing / verification
- risks / limitations

#### Purpose

Bring outside PRs up to the repository's existing standard of structured explanation without making PR creation tedious.

### `CONTRIBUTING.md`

Write a repository-specific contributor guide.

It should explain:

- welcome contribution types
- when to open an issue first
- expectations for small vs. large changes
- local verification expectations
- commit and PR expectations
- repository hygiene rules
- what must never be committed

#### Contribution Posture

This repository should explicitly welcome:

- bug fixes
- documentation improvements
- CI/template improvements
- focused code changes
- well-scoped feature work

But it should also state that contributors should discuss first when touching:

- Jira governance boundaries
- Codex execution semantics
- orchestrator architecture
- large refactors

### `SECURITY.md`

Write a practical security policy tuned to this repository.

It should explain:

- how to report a vulnerability privately
- what should not be posted publicly in issues
- what counts as a security issue here
- expected best-effort response language
- what is currently out of scope for formal guarantees

#### Private Reporting Channel Requirement

This spec does not allow the implementation to invent a placeholder reporting channel. Before implementing `SECURITY.md`, one maintainer-controlled private channel must be explicitly confirmed and used in the document.

Accepted options, in priority order:

1. GitHub private vulnerability reporting for this repository, if enabled
2. A maintainer-controlled email address that can actually receive reports

If neither exists at implementation time, implementation must stop and ask for a real channel instead of shipping a vague or placeholder `SECURITY.md`.

#### Repository-Specific Sensitive Areas

The security doc should explicitly mention:

- Jira credentials and API tokens
- `.env` contents
- local absolute workdir paths
- private requirement/task context copied from local Jira
- real `codex exec` traces that may expose sensitive repository details

### `README.md`

Only make narrow collaboration-related updates.

Add:

- exactly two badges near the top: CI status and license
- a pointer to `CONTRIBUTING.md`
- a pointer to `SECURITY.md`

Do not restructure the README again. The existing showcase-oriented shape should remain intact.

## Content Style

### Governance Strength

The overall style should be standard-governance, not minimalist and not corporate-heavy.

That means:

- enough structure to improve quality
- enough openness to invite participation
- enough boundary-setting to avoid chaotic contributions

### Tone

Use direct, calm language.

- welcoming, but not gushy
- explicit, but not bureaucratic
- security-aware, but not alarmist

## README Badge Policy

Use only a few badges with clear value.

Recommended badge categories:

- CI status
- license

Avoid badge walls or decorative badges.

## Acceptance Criteria

The design is successful when:

1. Opening a new issue presents at least `bug report` and `feature request` forms.
2. New PRs show a structured template covering summary, validation, and risks.
3. `CONTRIBUTING.md` clearly explains how to collaborate and what contribution types need discussion first.
4. `SECURITY.md` clearly distinguishes private disclosure from normal public issue filing.
5. README includes visible entry points to collaboration and security guidance.
6. The result supports invited collaborators now and future public collaboration later without implying the repository has heavyweight maintainer operations.

## Risks

### Templates Too Light

If the forms ask for too little information, maintainers still receive low-quality reports and proposals.

### Templates Too Heavy

If the forms are too rigid, contributors will avoid using them or provide low-signal filler responses.

### Security Policy Too Generic

If `SECURITY.md` reads like a generic boilerplate, it will fail to warn about the repository's real risks around credentials and local execution context.

### README Clutter

If too many badges or links are added, the improved showcase README will regress into noise.

## Recommended Next Step

After this spec is reviewed, the next step is to produce an implementation plan that creates the issue forms, PR template, contributor guide, security policy, and minimal README additions in a few low-risk tasks with explicit verification steps.
