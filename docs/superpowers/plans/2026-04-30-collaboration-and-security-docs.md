# Collaboration And Security Docs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add GitHub issue forms, a pull request template, a contributor guide, a practical security policy, and small README collaboration updates without changing product behavior.

**Architecture:** Keep all changes at the repository-documentation layer. Place GitHub-specific templates under `.github/`, keep contributor/security policies at the repo root, and make only narrow README edits so the showcase-oriented structure stays intact.

**Tech Stack:** GitHub issue forms, Markdown, YAML, GitHub Actions metadata, Python 3 for lightweight verification

---

## File Structure

- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/pull_request_template.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Modify: `README.md`

The repository already contains `.github/workflows/ci.yml` and a showcase-oriented `README.md`. It does not yet contain issue forms, a PR template, `CONTRIBUTING.md`, or `SECURITY.md`. The plan keeps README changes narrow and does not add Discussions, Code of Conduct, or support-policy assets.

### Task 1: Add GitHub Issue Forms And PR Template

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/pull_request_template.md`

- [ ] **Step 1: Create the issue template directory**

Run:

```bash
mkdir -p .github/ISSUE_TEMPLATE
```

Expected:
- `.github/ISSUE_TEMPLATE` exists

- [ ] **Step 2: Create `.github/ISSUE_TEMPLATE/bug_report.yml`**

Write `.github/ISSUE_TEMPLATE/bug_report.yml` with this exact content:

```yaml
name: Bug report
description: Report a reproducible problem in the repository, templates, docs, or prototype workflow.
title: "[Bug]: "
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting an issue.
        Please provide enough detail to distinguish a repository bug from a local setup or environment problem.

  - type: input
    id: summary
    attributes:
      label: 问题摘要
      description: 用一句话说明问题。
      placeholder: 例如：`prepare-task` 在缺少模块路径时给出了错误建议
    validations:
      required: true

  - type: dropdown
    id: affected_area
    attributes:
      label: 影响范围
      description: 这个问题最接近哪个区域？
      options:
        - Orchestrator CLI
        - Jira integration
        - Codex runner
        - Schema / prompt contract
        - Documentation
        - GitHub / CI
        - Other
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: 复现步骤
      description: 按顺序写出可以稳定复现问题的步骤。
      placeholder: |
        1. 运行 `python scripts/orchestrator.py ...`
        2. 使用某个输入或 issue key
        3. 观察报错或异常行为
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: 预期行为
      description: 你原本期待发生什么？
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: 实际行为
      description: 实际发生了什么？请贴出关键报错或异常输出。
    validations:
      required: true

  - type: checkboxes
    id: involved_surfaces
    attributes:
      label: 涉及面
      description: 请选择所有相关项。
      options:
        - label: Jira
        - label: Codex
        - label: Local toolchain
        - label: Schema / prompts
        - label: Documentation
        - label: CI / GitHub
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: 本地环境说明
      description: 可选。补充 Python 版本、操作系统、是否连接本地 Jira、是否使用真实 `codex exec` 等。
      placeholder: |
        Python 3.13
        Ubuntu 24.04
        Local Jira Server
        Dry-run / real Codex mode
    validations:
      required: false

  - type: textarea
    id: logs
    attributes:
      label: 日志 / 截图
      description: 可选。补充截图、命令输出或最小上下文。
    validations:
      required: false
```

- [ ] **Step 3: Create `.github/ISSUE_TEMPLATE/feature_request.yml`**

Write `.github/ISSUE_TEMPLATE/feature_request.yml` with this exact content:

```yaml
name: Feature request
description: Propose a well-scoped improvement to the repository, workflow, or contributor experience.
title: "[Feature]: "
body:
  - type: markdown
    attributes:
      value: |
        Please frame requests around the problem to solve, the user value, and whether the change affects Jira governance or Codex execution boundaries.

  - type: input
    id: summary
    attributes:
      label: 请求摘要
      description: 用一句话概括想要的改进。
      placeholder: 例如：增加针对 task scope 修正建议的批量预览能力
    validations:
      required: true

  - type: textarea
    id: current_problem
    attributes:
      label: 当前问题 / 缺口
      description: 现在的流程哪里不够好？缺了什么？
    validations:
      required: true

  - type: textarea
    id: proposed_change
    attributes:
      label: 建议改进
      description: 你建议新增或改变什么？
    validations:
      required: true

  - type: textarea
    id: user_value
    attributes:
      label: 预期价值
      description: 这项改进对谁有价值？会让什么更好？
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: 替代方案
      description: 可选。你是否考虑过其他做法？
    validations:
      required: false

  - type: dropdown
    id: jira_boundary
    attributes:
      label: 是否影响 Jira 治理边界？
      description: 例如 Sprint、Priority、Assignee、流程控制责任等。
      options:
        - No
        - Yes
        - Not sure
    validations:
      required: true

  - type: dropdown
    id: codex_boundary
    attributes:
      label: 是否影响 Codex 执行边界？
      description: 例如 Codex 可以读取什么、执行什么、回写什么。
      options:
        - No
        - Yes
        - Not sure
    validations:
      required: true
```

- [ ] **Step 4: Create `.github/pull_request_template.md`**

Write `.github/pull_request_template.md` with this exact content:

```markdown
## Summary

- 

## Why This Change Exists

- 

## Scope

- Affected areas:
- In scope:
- Out of scope:

## Testing / Verification

- [ ] `python -m py_compile scripts/*.py`
- [ ] `python scripts/orchestrator.py --help`
- [ ] `python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json`
- [ ] `python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json`
- [ ] Other verification (describe below)

## Risks / Limitations

- 
```

- [ ] **Step 5: Verify the template files have the required structure and key fields**

Run:

```bash
python - <<'PY'
from pathlib import Path

forms = {
    ".github/ISSUE_TEMPLATE/bug_report.yml": {
        "top_level": ["name:", "description:", "title:", "body:"],
        "labels": ["问题摘要", "复现步骤", "预期行为", "实际行为", "涉及面"],
        "min_blocks": 7,
    },
    ".github/ISSUE_TEMPLATE/feature_request.yml": {
        "top_level": ["name:", "description:", "title:", "body:"],
        "labels": ["请求摘要", "当前问题 / 缺口", "建议改进", "预期价值"],
        "min_blocks": 7,
    },
}

for path, rules in forms.items():
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    for marker in rules["top_level"]:
        if not any(line.startswith(marker) for line in lines):
            raise SystemExit(f"missing top-level key {marker!r} in {path}")
    block_count = sum(1 for line in lines if line.startswith("  - type:"))
    if block_count < rules["min_blocks"]:
        raise SystemExit(f"expected at least {rules['min_blocks']} form blocks in {path}, found {block_count}")
    for label in rules["labels"]:
        if f"label: {label}" not in text:
            raise SystemExit(f"missing label {label!r} in {path}")

pr_text = Path(".github/pull_request_template.md").read_text(encoding="utf-8")
for marker in [
    "## Summary",
    "## Why This Change Exists",
    "## Testing / Verification",
    "## Risks / Limitations",
]:
    if marker not in pr_text:
        raise SystemExit(f"missing marker {marker!r} in .github/pull_request_template.md")

print("template structure verified")
PY
```

Expected:
- Output is `template structure verified`

- [ ] **Step 6: Commit the issue forms and PR template**

Run:

```bash
git add .github/ISSUE_TEMPLATE/bug_report.yml \
  .github/ISSUE_TEMPLATE/feature_request.yml \
  .github/pull_request_template.md
git commit -m "docs: add GitHub collaboration templates"
```

Expected:
- Commit succeeds with only the three template files staged for this task

### Task 2: Add `CONTRIBUTING.md`

**Files:**
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Create `CONTRIBUTING.md`**

Write `CONTRIBUTING.md` with this exact content:

```markdown
# Contributing

Thanks for your interest in contributing to Jira + Codex AI Management.

This repository is currently a private, invite-only prototype workspace. The guidance below is intended to make collaboration smoother for invited contributors today and easier to reuse if the repository becomes public later.

## What Contributions Are Welcome

The following kinds of contributions are welcome:

- Bug fixes
- Documentation improvements
- CI or GitHub template improvements
- Focused code changes
- Well-scoped feature work

## When To Open An Issue First

Please open an issue before starting work if your change touches any of the following:

- Jira governance boundaries
- Codex execution semantics
- Orchestrator architecture
- Large refactors
- New end-to-end workflow behavior

For small documentation updates, isolated bug fixes, or narrow CI/template improvements, opening a PR directly is fine.

## Development Expectations

Keep changes focused.

- Prefer small, reviewable PRs over broad bundles of unrelated work
- Do not mix behavior changes and cosmetic cleanup unless they are tightly coupled
- Preserve the repository's current prototype boundaries unless the change is explicitly intended to revisit them

## Local Verification

Before opening a PR, run the baseline local checks:

```bash
python -m py_compile scripts/*.py
python scripts/orchestrator.py --help
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
```

If your change touches Jira integration, Codex execution behavior, task preparation, or writeback logic, include additional validation notes in the PR describing:

- what you tested
- what environment assumptions were required
- what you could not verify locally

## Pull Request Expectations

Use the pull request template and explain:

- what changed
- why it changed
- how you verified it
- what risks or limitations remain

If your change intentionally leaves follow-up work, state that explicitly.

## Repository Hygiene

Do not commit:

- `.env`
- secrets, credentials, or tokens
- private Jira payloads copied from local systems
- local-only absolute paths unless they are already part of a documented example
- generated caches or machine-specific artifacts

## Need Help?

If you are not sure whether a change fits the repository boundary, open an issue first and describe the proposed direction before implementing it.
```

- [ ] **Step 2: Verify `CONTRIBUTING.md` covers the required sections**

Run:

```bash
python - <<'PY'
from pathlib import Path
text = Path("CONTRIBUTING.md").read_text(encoding="utf-8")
required = [
    "# Contributing",
    "## What Contributions Are Welcome",
    "## When To Open An Issue First",
    "## Local Verification",
    "## Pull Request Expectations",
    "## Repository Hygiene",
]
for marker in required:
    if marker not in text:
        raise SystemExit(f"missing section: {marker}")
print("contributing sections verified")
PY
```

Expected:
- Output is `contributing sections verified`

- [ ] **Step 3: Commit the contributor guide**

Run:

```bash
git add CONTRIBUTING.md
git commit -m "docs: add contributor guide"
```

Expected:
- Commit succeeds with only `CONTRIBUTING.md` staged for this task

### Task 3: Confirm Private Reporting Channel And Add `SECURITY.md`

**Files:**
- Create: `SECURITY.md`

- [ ] **Step 1: Confirm which private reporting channel will be used**

Choose exactly one of these paths before editing `SECURITY.md`:

Path A:
- GitHub private vulnerability reporting is enabled for `tomllt/jira-codex-ai-management`

Path B:
- The maintainer provides a real monitored email address for vulnerability reports

If neither path is true, stop immediately and ask the user for a real channel. Do not create `SECURITY.md` with placeholders or vague instructions.

- [ ] **Step 2: If Path A is true, create `SECURITY.md` with the GitHub private reporting version**

Write `SECURITY.md` with this exact content if GitHub private vulnerability reporting is enabled:

```markdown
# Security Policy

## Reporting A Vulnerability

Please do **not** report security issues in public GitHub issues.

Use this repository's private GitHub vulnerability reporting flow instead. Submit the report through the repository's Security tab so the maintainer can triage it without exposing sensitive details publicly.

## What To Report Privately

Report privately if the issue involves any of the following:

- Jira credentials, tokens, or authentication handling
- `.env` contents or secrets exposure
- local absolute workdir paths that reveal sensitive repository layout
- copied task or requirement data from private local Jira instances
- real `codex exec` traces or outputs that expose sensitive local repository context
- unsafe command execution or privilege boundary problems

## What Not To Post Publicly

Do not post the following in public issues or PRs:

- passwords, API tokens, or cookies
- private Jira issue content
- internal repository paths from private machines
- execution transcripts that expose sensitive data

If you are unsure whether something is sensitive, treat it as sensitive and use the private reporting path.

## Response Expectations

This repository does not provide a formal SLA, but reported vulnerabilities will be reviewed on a best-effort basis.

When possible, reports should include:

- a short summary
- impact
- reproduction steps
- any mitigation ideas

## Out Of Scope For Formal Guarantees

This repository is a prototype and does not claim enterprise-grade operational guarantees, dedicated on-call coverage, or audited production security controls.
```

- [ ] **Step 3: If Path B is true, stop and get the real maintainer email before writing `SECURITY.md`**

Run:

```bash
export SECURITY_REPORT_EMAIL="real-maintainer-email@example.org"
python - <<'PY'
import os

email = os.environ.get("SECURITY_REPORT_EMAIL", "").strip()
if not email or "@" not in email or email.endswith("@example.org") or "example.com" in email:
    raise SystemExit("SECURITY_REPORT_EMAIL must be set to a real maintainer-controlled email address")
print(f"security email accepted: {email}")
PY
```

Expected:
- Output begins with `security email accepted:`
- The value is a real maintainer-controlled address, not a placeholder

- [ ] **Step 4: If Path B is true, create `SECURITY.md` with the maintainer-email version**

Run:

```bash
cat > SECURITY.md <<EOF
# Security Policy

## Reporting A Vulnerability

Please do **not** report security issues in public GitHub issues.

Send vulnerability reports privately to: \`${SECURITY_REPORT_EMAIL}\`

Include enough detail for triage, but avoid forwarding secrets unless they are strictly necessary to explain the issue.

## What To Report Privately

Report privately if the issue involves any of the following:

- Jira credentials, tokens, or authentication handling
- \`.env\` contents or secrets exposure
- local absolute workdir paths that reveal sensitive repository layout
- copied task or requirement data from private local Jira instances
- real \`codex exec\` traces or outputs that expose sensitive local repository context
- unsafe command execution or privilege boundary problems

## What Not To Post Publicly

Do not post the following in public issues or PRs:

- passwords, API tokens, or cookies
- private Jira issue content
- internal repository paths from private machines
- execution transcripts that expose sensitive data

If you are unsure whether something is sensitive, treat it as sensitive and use the private reporting path.

## Response Expectations

This repository does not provide a formal SLA, but reported vulnerabilities will be reviewed on a best-effort basis.

When possible, reports should include:

- a short summary
- impact
- reproduction steps
- any mitigation ideas

## Out Of Scope For Formal Guarantees

This repository is a prototype and does not claim enterprise-grade operational guarantees, dedicated on-call coverage, or audited production security controls.
EOF
```

Expected:
- `SECURITY.md` exists
- The committed file contains the real email address, not a placeholder

- [ ] **Step 5: Verify `SECURITY.md` has no placeholders and contains a private channel**

Run:

```bash
python - <<'PY'
from pathlib import Path
text = Path("SECURITY.md").read_text(encoding="utf-8")
required = [
    "# Security Policy",
    "## Reporting A Vulnerability",
    "## What To Report Privately",
    "## What Not To Post Publicly",
]
for marker in required:
    if marker not in text:
        raise SystemExit(f"missing section: {marker}")
if "maintainer@example.com" in text:
    raise SystemExit("placeholder email still present")
if "private GitHub vulnerability reporting flow" not in text and "Send vulnerability reports privately to:" not in text:
    raise SystemExit("no private reporting channel found")
print("security policy verified")
PY
```

Expected:
- Output is `security policy verified`

- [ ] **Step 6: Commit the security policy**

Run:

```bash
git add SECURITY.md
git commit -m "docs: add security policy"
```

Expected:
- Commit succeeds with only `SECURITY.md` staged for this task

### Task 4: Add README Badges And Collaboration Entry Points

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add the two required badges directly below the title**

Update the top of `README.md` so the first lines become:

```markdown
# Jira + Codex AI Management

[![CI](https://github.com/tomllt/jira-codex-ai-management/actions/workflows/ci.yml/badge.svg)](https://github.com/tomllt/jira-codex-ai-management/actions/workflows/ci.yml)
![License: Apache-2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

一个把 `Jira` 治理边界和 `Codex CLI` 执行能力连接起来的 AI 协同原型，用于把已批准的研发工作转成可执行任务，并以结构化结果回写到 Jira。
```

- [ ] **Step 2: Add a collaboration and security pointer section without restructuring the README**

Insert this exact section immediately after the `Quick Start` section and its trailing sentence:

```markdown
## Contributing And Security

- 协作说明见 `CONTRIBUTING.md`
- 安全问题与私下披露说明见 `SECURITY.md`
```

- [ ] **Step 3: Verify the README still has the existing showcase structure plus the new collaboration markers**

Run:

```bash
python - <<'PY'
from pathlib import Path
text = Path("README.md").read_text(encoding="utf-8")
required = [
    "[![CI]",
    "License: Apache-2.0",
    "## What It Is",
    "## Quick Start",
    "## Contributing And Security",
    "`CONTRIBUTING.md`",
    "`SECURITY.md`",
]
for marker in required:
    if marker not in text:
        raise SystemExit(f"missing marker: {marker}")
print("readme collaboration markers verified")
PY
```

Expected:
- Output is `readme collaboration markers verified`

- [ ] **Step 4: Commit the README collaboration additions**

Run:

```bash
git add README.md
git commit -m "docs: add collaboration and security entry points"
```

Expected:
- Commit succeeds with only `README.md` staged for this task

### Task 5: End-To-End Verification

**Files:**
- Verify: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Verify: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Verify: `.github/pull_request_template.md`
- Verify: `CONTRIBUTING.md`
- Verify: `SECURITY.md`
- Verify: `README.md`

- [ ] **Step 1: Run repository baseline checks to ensure no behavioral regression was introduced**

Run:

```bash
python -m py_compile scripts/*.py
python scripts/orchestrator.py --help >/tmp/jcam-help.txt
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
```

Expected:
- `py_compile` exits `0`
- both `validate` commands print `"valid": true`

- [ ] **Step 2: Verify all collaboration and security files exist**

Run:

```bash
for path in \
  .github/ISSUE_TEMPLATE/bug_report.yml \
  .github/ISSUE_TEMPLATE/feature_request.yml \
  .github/pull_request_template.md \
  CONTRIBUTING.md \
  SECURITY.md \
  README.md; do
  test -f "$path" || echo "missing: $path"
done
```

Expected:
- No output

- [ ] **Step 3: Check for accidental secret placeholders or unsafe committed values**

Run:

```bash
rg -n "maintainer@example.com|<your-|TODO|TBD" \
  .github/ISSUE_TEMPLATE \
  .github/pull_request_template.md \
  CONTRIBUTING.md \
  SECURITY.md \
  README.md || true
```

Expected:
- No output

- [ ] **Step 4: Confirm the branch is clean before push or merge**

Run:

```bash
git status --short --branch
```

Expected:
- Output shows only the current branch header
- No unstaged or uncommitted files remain

- [ ] **Step 5: If implementation is being completed in a feature branch, merge back to `main`, then push `main`**

Run:

```bash
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
  git checkout main
  git pull --ff-only
  git merge --ff-only "$current_branch"
  python -m py_compile scripts/*.py
  python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
  python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
fi
git push origin main
```

Expected:
- Push succeeds
- The canonical branch on the remote is `main`

- [ ] **Step 6: Verify that GitHub Actions picked up the integrated change set**

Run:

```bash
gh run list --repo tomllt/jira-codex-ai-management --limit 5
```

Expected:
- At least one recent `CI` run is visible for the pushed change set
