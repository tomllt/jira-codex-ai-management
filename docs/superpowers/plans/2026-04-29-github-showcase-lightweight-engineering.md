# GitHub Showcase Lightweight Engineering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Apache-2.0 licensing, public-facing repository metadata, lightweight CI, and a clearer showcase README without changing product behavior.

**Architecture:** Keep the repository's current lightweight structure intact. Limit changes to repository presentation, GitHub settings, and zero-dependency verification so the project looks more credible on GitHub without pretending to be a production platform.

**Tech Stack:** GitHub CLI, GitHub Actions, Markdown, YAML, Python 3

---

## File Structure

- Create: `LICENSE`
- Create: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify (remote setting): GitHub repository `tomllt/jira-codex-ai-management` description and topics

The repo currently has no `.github/` directory, no root `LICENSE`, and a README that is useful for local work but too dense and inward-facing for public discovery. The implementation should keep `docs/`, `scripts/`, `schemas/`, `prompts/`, and `.planning/` unchanged except for how they are described.

### Task 1: Add Apache-2.0 License And Public Repository Metadata

**Files:**
- Create: `LICENSE`
- Remote update: GitHub repo settings for `tomllt/jira-codex-ai-management`

- [ ] **Step 1: Confirm the repo is on the expected branch and remote**

Run:

```bash
git branch --show-current
git remote -v
```

Expected:
- Current branch is `main`
- `origin` points to `https://github.com/tomllt/jira-codex-ai-management.git`

- [ ] **Step 2: Create the Apache-2.0 license file**

Write `LICENSE` with this exact content:

```text
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

"License" shall mean the terms and conditions for use, reproduction,
and distribution as defined by Sections 1 through 9 of this document.

"Licensor" shall mean the copyright owner or entity authorized by
the copyright owner that is granting the License.

"Legal Entity" shall mean the union of the acting entity and all
other entities that control, are controlled by, or are under common
control with that entity. For the purposes of this definition,
"control" means (i) the power, direct or indirect, to cause the
direction or management of such entity, whether by contract or
otherwise, or (ii) ownership of fifty percent (50%) or more of the
outstanding shares, or (iii) beneficial ownership of such entity.

"You" (or "Your") shall mean an individual or Legal Entity
exercising permissions granted by this License.

"Source" form shall mean the preferred form for making modifications,
including but not limited to software source code, documentation
source, and configuration files.

"Object" form shall mean any form resulting from mechanical
transformation or translation of a Source form, including but
not limited to compiled object code, generated documentation,
and conversions to other media types.

"Work" shall mean the work of authorship, whether in Source or
Object form, made available under the License, as indicated by a
copyright notice that is included in or attached to the work
(an example is provided in the Appendix below).

"Derivative Works" shall mean any work, whether in Source or Object
form, that is based on (or derived from) the Work and for which the
editorial revisions, annotations, elaborations, or other modifications
represent, as a whole, an original work of authorship. For the purposes
of this License, Derivative Works shall not include works that remain
separable from, or merely link (or bind by name) to the interfaces of,
the Work and Derivative Works thereof.

"Contribution" shall mean any work of authorship, including
the original version of the Work and any modifications or additions
to that Work or Derivative Works thereof, that is intentionally
submitted to Licensor for inclusion in the Work by the copyright owner
or by an individual or Legal Entity authorized to submit on behalf of
the copyright owner. For the purposes of this definition, "submitted"
means any form of electronic, verbal, or written communication sent
to the Licensor or its representatives, including but not limited to
communication on electronic mailing lists, source code control systems,
and issue tracking systems that are managed by, or on behalf of, the
Licensor for the purpose of discussing and improving the Work, but
excluding communication that is conspicuously marked or otherwise
designated in writing by the copyright owner as "Not a Contribution."

"Contributor" shall mean Licensor and any individual or Legal Entity
on behalf of whom a Contribution has been received by Licensor and
subsequently incorporated within the Work.

2. Grant of Copyright License. Subject to the terms and conditions of
this License, each Contributor hereby grants to You a perpetual,
worldwide, non-exclusive, no-charge, royalty-free, irrevocable
copyright license to reproduce, prepare Derivative Works of,
publicly display, publicly perform, sublicense, and distribute the
Work and such Derivative Works in Source or Object form.

3. Grant of Patent License. Subject to the terms and conditions of
this License, each Contributor hereby grants to You a perpetual,
worldwide, non-exclusive, no-charge, royalty-free, irrevocable
(except as stated in this section) patent license to make, have made,
use, offer to sell, sell, import, and otherwise transfer the Work,
where such license applies only to those patent claims licensable
by such Contributor that are necessarily infringed by their
Contribution(s) alone or by combination of their Contribution(s)
with the Work to which such Contribution(s) was submitted. If You
institute patent litigation against any entity (including a
cross-claim or counterclaim in a lawsuit) alleging that the Work
or a Contribution incorporated within the Work constitutes direct
or contributory patent infringement, then any patent licenses
granted to You under this License for that Work shall terminate
as of the date such litigation is filed.

4. Redistribution. You may reproduce and distribute copies of the
Work or Derivative Works thereof in any medium, with or without
modifications, and in Source or Object form, provided that You
meet the following conditions:

(a) You must give any other recipients of the Work or
Derivative Works a copy of this License; and

(b) You must cause any modified files to carry prominent notices
stating that You changed the files; and

(c) You must retain, in the Source form of any Derivative Works
that You distribute, all copyright, patent, trademark, and
attribution notices from the Source form of the Work,
excluding those notices that do not pertain to any part of
the Derivative Works; and

(d) If the Work includes a "NOTICE" text file as part of its
distribution, then any Derivative Works that You distribute must
include a readable copy of the attribution notices contained
within such NOTICE file, excluding those notices that do not
pertain to any part of the Derivative Works, in at least one
of the following places: within a NOTICE text file distributed
as part of the Derivative Works; within the Source form or
documentation, if provided along with the Derivative Works; or,
within a display generated by the Derivative Works, if and
wherever such third-party notices normally appear. The contents
of the NOTICE file are for informational purposes only and
do not modify the License. You may add Your own attribution
notices within Derivative Works that You distribute, alongside
or as an addendum to the NOTICE text from the Work, provided
that such additional attribution notices cannot be construed
as modifying the License.

You may add Your own copyright statement to Your modifications and
may provide additional or different license terms and conditions
for use, reproduction, or distribution of Your modifications, or
for any such Derivative Works as a whole, provided Your use,
reproduction, and distribution of the Work otherwise complies with
the conditions stated in this License.

5. Submission of Contributions. Unless You explicitly state otherwise,
any Contribution intentionally submitted for inclusion in the Work
by You to the Licensor shall be under the terms and conditions of
this License, without any additional terms or conditions.
Notwithstanding the above, nothing herein shall supersede or modify
the terms of any separate license agreement you may have executed
with Licensor regarding such Contributions.

6. Trademarks. This License does not grant permission to use the trade
names, trademarks, service marks, or product names of the Licensor,
except as required for reasonable and customary use in describing the
origin of the Work and reproducing the content of the NOTICE file.

7. Disclaimer of Warranty. Unless required by applicable law or
agreed to in writing, Licensor provides the Work (and each
Contributor provides its Contributions) on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied, including, without limitation, any warranties or conditions
of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
PARTICULAR PURPOSE. You are solely responsible for determining the
appropriateness of using or redistributing the Work and assume any
risks associated with Your exercise of permissions under this License.

8. Limitation of Liability. In no event and under no legal theory,
whether in tort (including negligence), contract, or otherwise,
unless required by applicable law (such as deliberate and grossly
negligent acts) or agreed to in writing, shall any Contributor be
liable to You for damages, including any direct, indirect, special,
incidental, or consequential damages of any character arising as a
result of this License or out of the use or inability to use the
Work (including but not limited to damages for loss of goodwill,
work stoppage, computer failure or malfunction, or any and all
other commercial damages or losses), even if such Contributor
has been advised of the possibility of such damages.

9. Accepting Warranty or Additional Liability. While redistributing
the Work or Derivative Works thereof, You may choose to offer,
and charge a fee for, acceptance of support, warranty, indemnity,
or other liability obligations and/or rights consistent with this
License. However, in accepting such obligations, You may act only
on Your own behalf and on Your sole responsibility, not on behalf
of any other Contributor, and only if You agree to indemnify,
defend, and hold each Contributor harmless for any liability
incurred by, or claims asserted against, such Contributor by reason
of your accepting any such warranty or additional liability.

END OF TERMS AND CONDITIONS

APPENDIX: How to apply the Apache License to your work.

To apply the Apache License to your work, attach the following
boilerplate notice, with the fields enclosed by brackets "[]"
replaced with your own identifying information. (Don't include
the brackets!) The text should be enclosed in the appropriate
comment syntax for the file format. We also recommend that a
file or class name and description of purpose be included on the
same "printed page" as the copyright notice for easier
identification within third-party archives.

Copyright [yyyy] [name of copyright owner]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

- [ ] **Step 3: Verify the license file exists and starts correctly**

Run:

```bash
sed -n '1,20p' LICENSE
```

Expected:
- Output starts with `Apache License`
- Output includes `Version 2.0, January 2004`

- [ ] **Step 4: Update the GitHub repository description and topics**

Run:

```bash
gh repo edit tomllt/jira-codex-ai-management \
  --description "AI-assisted Jira orchestration prototype for turning approved work into Codex-executable tasks with structured writeback." \
  --add-topic jira \
  --add-topic codex \
  --add-topic ai-agent \
  --add-topic workflow-automation \
  --add-topic project-management \
  --add-topic developer-tools \
  --add-topic python \
  --add-topic prototype \
  --add-topic llm-orchestration
```

Expected:
- Command exits `0`
- The repository remains private

- [ ] **Step 5: Verify the remote repository metadata**

Run:

```bash
gh repo view tomllt/jira-codex-ai-management \
  --json description,isPrivate,repositoryTopics \
  --jq '{description: .description, isPrivate: .isPrivate, topics: [.repositoryTopics[].name]}'
```

Expected:
- `description` matches the target sentence
- `isPrivate` is `true`
- `topics` contains all nine configured topics

- [ ] **Step 6: Commit the license change**

Run:

```bash
git add LICENSE
git commit -m "docs: add Apache 2.0 license"
```

Expected:
- Commit succeeds with only the new `LICENSE` tracked in this task

### Task 2: Add Lightweight GitHub Actions CI

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create the workflow directory**

Run:

```bash
mkdir -p .github/workflows
```

Expected:
- `.github/workflows` exists

- [ ] **Step 2: Write the CI workflow**

Create `.github/workflows/ci.yml` with this exact content:

```yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  smoke:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Compile prototype scripts
        run: python -m py_compile scripts/*.py

      - name: Show CLI help
        run: python scripts/orchestrator.py --help

      - name: Validate AI plan example
        run: python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json

      - name: Validate execution result example
        run: python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
```

- [ ] **Step 3: Validate the workflow file reads cleanly**

Run:

```bash
sed -n '1,240p' .github/workflows/ci.yml
```

Expected:
- YAML shows one job named `smoke`
- The workflow contains only zero-dependency checks

- [ ] **Step 4: Run the local compile step**

Run:

```bash
python -m py_compile scripts/*.py
```

Expected:
- No output
- Exit code `0`

- [ ] **Step 5: Run the local CLI help check**

Run:

```bash
python scripts/orchestrator.py --help
```

Expected:
- Output begins with `usage: orchestrator.py`
- Exit code `0`

- [ ] **Step 6: Run the local schema example checks**

Run:

```bash
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
```

Expected:
- Both commands print JSON with `"valid": true`
- Both commands exit `0`

- [ ] **Step 7: Commit the CI workflow**

Run:

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add lightweight GitHub Actions checks"
```

Expected:
- Commit succeeds with only the workflow change tracked in this task

### Task 3: Rewrite README For Public-Facing Discovery

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the README opening structure with a showcase-first narrative**

Overwrite `README.md` with this exact content:

```markdown
# Jira + Codex AI Management

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
```

- [ ] **Step 2: Preview the rewritten README structure**

Run:

```bash
sed -n '1,260p' README.md
```

Expected:
- The first screen begins with positioning, not with a document dump
- `Current Status` explicitly says the repo is a validated prototype
- The detailed local notes still exist near the bottom

- [ ] **Step 3: Check that the README still points to real files**

Run:

```bash
for path in \
  docs/overview.md \
  docs/workflow.md \
  docs/mvp-spec.md \
  docs/skills-architecture.md \
  docs/data-models.md \
  docs/implementation.md \
  docs/roadmap.md \
  docs/README.md \
  docs/2026-04-28-refactor-implementation-plan.md \
  schemas/ai-plan.schema.json \
  schemas/execution-result.schema.json \
  prompts/epic_to_plan.prompt.md \
  prompts/task_execution.prompt.md \
  examples/sample-ai-plan.json \
  examples/sample-execution-result.json \
  examples/sample-jira-comment.md \
  scripts/orchestrator.py; do
  test -e "$path" || echo "missing: $path"
done
```

Expected:
- No output

- [ ] **Step 4: Commit the README rewrite**

Run:

```bash
git add README.md
git commit -m "docs: refresh README for GitHub showcase"
```

Expected:
- Commit succeeds with only the README rewrite tracked in this task

### Task 4: End-To-End Verification And Push

**Files:**
- Verify: `LICENSE`
- Verify: `.github/workflows/ci.yml`
- Verify: `README.md`

- [ ] **Step 1: Run the full local verification sequence**

Run:

```bash
python -m py_compile scripts/*.py
python scripts/orchestrator.py --help >/tmp/jcam-help.txt
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
gh repo view tomllt/jira-codex-ai-management --json description,isPrivate,repositoryTopics
git status --short --branch
```

Expected:
- Python compile step exits `0`
- Both `validate` commands print `"valid": true`
- GitHub repo remains private and shows the new description/topics
- `git status --short --branch` shows a clean branch before push

- [ ] **Step 2: Push the completed branch to GitHub**

Run:

```bash
git push origin main
```

Expected:
- Push succeeds
- GitHub Actions CI starts automatically on `main`

- [ ] **Step 3: Verify the workflow was registered remotely**

Run:

```bash
gh run list --repo tomllt/jira-codex-ai-management --limit 5
```

Expected:
- At least one recent workflow run named `CI` appears

- [ ] **Step 4: Confirm the final repository presentation**

Run:

```bash
gh repo view tomllt/jira-codex-ai-management \
  --json url,description,isPrivate,repositoryTopics \
  --jq '{url: .url, description: .description, isPrivate: .isPrivate, topics: [.repositoryTopics[].name]}'
```

Expected:
- URL is `https://github.com/tomllt/jira-codex-ai-management`
- `description` matches the target sentence
- `isPrivate` is `true`
- Topics list is complete

- [ ] **Step 5: Commit any final touch-ups if verification required them**

Run:

```bash
git status --short --branch
```

Expected:
- No output other than `## main...origin/main`
- If there are no changes, do not create an extra commit
