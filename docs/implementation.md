# 实现使用说明

## 当前实现范围

当前项目已经包含第一版可运行原型：

- Jira 配置加载
- Ready-for-Codex JQL 生成
- Jira REST Client
- Jira comment 构建
- Orchestrator CLI 命令
- 基于 plan JSON 的 Story / Task 自动建单
- Codex Runner dry-run / CLI 调用骨架
- `run-task` 执行与 Jira 回写闭环
- `run-next` 批量消费入口
- 轻量 schema 校验

当前仍未实现：

- AI 规划 JSON 自动生成
- Jira 自定义字段映射
- Story 与 Epic 的父子链路增强
- 多任务并发与锁机制完善

## 当前目录状态

- 当前仓库已整理为单层根目录结构。
- 历史遗留的同名嵌套目录已移除，正式重构计划文档统一放在 `docs/2026-04-28-refactor-implementation-plan.md`。
- `scripts/` 仍是当前兼容执行入口；后续若按计划推进分层重构，目标结构将落到 `src/jira_codex/`。

## 配置

复制环境模板：

```bash
cp .env.example .env
```

当前本地 Jira 推荐配置：

- `JIRA_BASE_URL=http://127.0.0.1:18080`
- `JIRA_USERNAME=tomllt`
- `JIRA_PASSWORD=<你的密码>`
- `JIRA_PROJECT_KEY=ON`
- `JIRA_API_VERSION=2`

如需真实调用 Codex CLI，可配置：

- `CODEX_COMMAND=codex`
- `CODEX_HOME=/root/.codex`
- `CODEX_USER_HOME=/root`

## 当前 Jira workflow 适配结果

你当前本地 Jira 项目 `ON` 的真实状态与类型如下：

- 状态：`待办` / `处理中` / `完成`
- 类型：`Epic` / `故事` / `任务` / `子任务` / `故障`

因此当前原型采用：

- 用 `状态` 表达主生命周期
- 用 `label` 表达 Codex 细分执行态

### 当前标签约定

- `codex`
- `ai-drafted`
- `ready-for-codex`
- `codex-running`
- `codex-blocked`
- `needs-human-review`

### 当前状态映射

- 可执行任务：`待办` + `codex` + `ready-for-codex`
- Codex 已领取：`处理中` + `codex-running`
- Codex 阻塞：`处理中` + `codex-blocked`
- 待人工复核：`处理中` + `needs-human-review`
- 人工完成：`完成`

## 可用命令

在项目根目录运行：

```bash
python scripts/orchestrator.py check-config
python scripts/orchestrator.py check-jira
python scripts/orchestrator.py validate ai-plan examples/sample-ai-plan.json
python scripts/orchestrator.py validate execution-result examples/sample-execution-result.json
python scripts/orchestrator.py build-jql
python scripts/orchestrator.py plan-example
python scripts/orchestrator.py result-example
python scripts/orchestrator.py comment-example
python scripts/orchestrator.py search-ready --limit 10
python scripts/orchestrator.py get-issue ON-3
python scripts/orchestrator.py draft-plan-from-requirement ON-REQ-001 "Web Console 导航测试治理" examples/sample-requirement-ontonexus-web-console.md --repo OntoNexus --workdir /root/workspace/OntoNexus/apps/web-console --label frontend --label web-console
python scripts/orchestrator.py create-from-requirement ON-REQ-002 "Web Console 导航测试治理（需求入口验证）" examples/sample-requirement-ontonexus-web-console.md --repo OntoNexus --workdir /root/workspace/OntoNexus/apps/web-console --label frontend --label web-console
python scripts/orchestrator.py prepare-task ON-11 --only test_command --no-writeback
python scripts/orchestrator.py prepare-task ON-11 --auto-apply --only test_command --no-writeback
python scripts/orchestrator.py set-workdir ON-9 /root/workspace/OntoNexus
python scripts/orchestrator.py refine-task-scope ON-11 --workdir /root/workspace/OntoNexus/apps/web-console --module src/App.test.tsx --module src/shellNavigation.ts --test-command "pnpm test"
python scripts/orchestrator.py claim ON-3
python scripts/orchestrator.py writeback-example --issue-key ON-3
python scripts/orchestrator.py create-from-plan examples/sample-ai-plan.json
python scripts/orchestrator.py run-task ON-3 --dry-run --no-claim --no-writeback
python scripts/orchestrator.py run-task ON-3 --dry-run --no-claim
python scripts/orchestrator.py run-next --dry-run --no-writeback
python scripts/orchestrator.py run-task ON-9 --no-claim --no-writeback --timeout 5
```

## `run-task` 行为

- 默认会先 claim 任务，再调用 Codex Runner，最后写回 Jira
- `--dry-run` 不会调用真实 Codex CLI，只生成确定性的模拟执行结果
- `--no-claim` 跳过状态迁移和 `codex-running` 标签更新
- `--no-writeback` 跳过 comment 和 label 回写
- `--timeout <seconds>` 可控制单任务执行超时时间

## `preflight-task` 行为

- 不调用真实 Codex CLI
- 只检查 Jira task 的执行上下文是否可落地
- 当前会检查：
  - `Workdir` 是否存在
  - `Workdir` 是否是目录
  - `Module` 路径是否真实存在
  - `Test Command` 对应工具是否可执行
- 默认会把审查结果回写到 Jira
- `--no-writeback` 可只输出 JSON，不修改 Jira

## `suggest-task-fixes` 行为

- 不修改 Jira
- 只基于当前 task 描述和本地仓库给出修复建议
- 当前会尝试建议：
  - 更合理的 `Module` 路径
  - 当前环境可用的 `Test Command`
  - 对 `Workdir` 状态给出说明
- 适合作为 AI 自动建单后的第一轮修复提示

## `apply-task-fixes` 行为

- 读取 `suggest-task-fixes` 的建议结果
- 只应用与当前 task 不同的建议项
- 当前可自动应用：
  - `Repo`
  - `Workdir`
  - `Module`
  - `Test Command`
- 支持：
  - `--dry-run`：只预览，不写 Jira
  - `--only <field>`：只应用指定字段
  - `--exclude <field>`：排除指定字段
- 适合放在 `suggest-task-fixes` 和 `preflight-task` 之间

## `prepare-task` 行为

- 聚合执行：`suggest-task-fixes -> apply-task-fixes -> preflight-task`
- 默认只输出建议和 preflight 结果，不自动改 Jira task 描述
- `--auto-apply` 会先应用所选建议，再立即执行 preflight
- 支持：
  - `--only <field>`：只选择某些字段参与修复
  - `--exclude <field>`：排除某些字段
  - `--no-writeback`：preflight 不回写 Jira
- 适合作为 Jira Skill 的推荐主入口

## `draft-plan-from-requirement` / `create-from-requirement`

- `draft-plan-from-requirement`：把需求文档转成兼容 `ai-plan.schema.json` 的结构化 plan
- `create-from-requirement`：在生成 plan 后直接创建 Story / Task 到 Jira
- 两者都支持：
  - `--repo`
  - `--workdir`
  - `--label`
  - `--use-codex`：启用真实 Codex 规划
  - `--timeout`
- 当前默认推荐先用 deterministic draft 模式快速起草，再进入 `prepare-task`

适合用作：

- AI 自动建单后的第一轮可执行性审查
- 人工排期前的任务质量过滤
- `run-task` 之前的轻量守门步骤
- `refine-task-scope` 之前的建议生成步骤

## `run-next` 行为

- 从 `search-ready` 的结果中取第一个 ready 任务
- 自动 claim
- 调用 Codex Runner
- 根据参数选择是否回写
- `--timeout <seconds>` 可控制执行超时时间

适合后续扩展为：

- 定时消费 Sprint 任务
- 一次执行一个 ready 任务
- 作为 cron / CI job 的最小入口

## 当前 Codex CLI 接入结果

已经确认本机存在可用命令：

- `codex`
- `codex exec`

并且已经确认要使用的配置目录是：

- `CODEX_HOME=/root/.codex`
- `HOME=/root`

当前 `CodexRunner` 已显式使用这套配置，并通过独立验证命令确认生效：

- 返回 provider：`univibe`
- 不再出现之前的 `401 Unauthorized`

## 当前 Workdir 接入结果

`CodexRunner` 已经会从 Jira task 描述中自动解析：

- `Repo`
- `Workdir`
- `Module`
- `Test Command`

并在真实执行前做最小上下文预检：

- `Workdir` 是否存在
- `Workdir` 是否是目录
- `Module` 路径是否存在于 `Workdir` 下
- `Test Command` 的可执行命令是否存在于 PATH

并在真实执行时把 `Workdir` 传给：

```bash
codex exec -C <workdir> ...
```

当前验证结果表明：

- `Workdir` 解析成功
- `--timeout` 参数生效
- 可用 `set-workdir` 命令直接修正 Jira task 的执行目录
- 可用 `refine-task-scope` 命令直接修正 Jira task 的 repo/workdir/module/test-command
- `pnpm` 类测试命令会优先尝试本机 `pnpm`，其次尝试 `corepack pnpm`
- 当前样例任务 `ON-9` 已改成 `/root/workspace/OntoNexus`
- 当前阻塞已从“路径不存在”升级为“任务模块路径与仓库不匹配”
- `ON-9` 中的模块 `src/payment/callback_handler.py`、`src/payment/service.py` 不存在于 `OntoNexus`
- 新建的 `ON-11` 已验证为匹配 `OntoNexus/apps/web-console` 的真实任务
- `ON-11` 当前进一步暴露出环境阻塞：本机没有 `pnpm`，而 `corepack` 也无法在当前网络/代理环境下成功准备 pnpm

这说明当前最后的落地前提是：

- Jira 任务中的 `Workdir` 必须指向真实仓库
- Jira 任务中的 `Module` / `Test Command` 也必须与该仓库实际技术栈一致

## 已验证的真实结果

已经在你的本地 Jira `ON` 项目中验证成功：

- 创建测试任务：`ON-1`
- 创建样例故事：`ON-2`
- 创建样例任务：`ON-3`
- `search-ready` 能检索到 `ON-3`
- `claim ON-3` 能把任务转为 `处理中` 并加上 `codex-running`
- `run-task ON-3 --dry-run --no-claim` 能写入 comment，并将标签更新为 `needs-human-review`
- 新创建样例故事：`ON-8`
- 新创建样例任务：`ON-9`
- `run-next --dry-run --no-writeback` 能正确消费 `ON-9`
- `validate ai-plan` / `validate execution-result` 均通过
- 真实 `codex exec` 已通过 `/root/.codex` 配置验证可用
- `run-task ON-9 --no-claim --no-writeback --timeout 5` 已验证到真实 `Workdir` 检查阶段

## 说明

- 当前 JQL 为兼容你的本地 Jira，采用了状态和 issue type 的 ID 进行过滤
- 当前 `create-from-plan` 会创建 `故事` 和 `任务`
- 当前 `claim` 会做真实状态迁移和 label 更新
- 当前 `writeback-example` 会对真实 issue 写 comment 并更新 label
- 当前 schema 校验器是轻量内置实现，不依赖额外三方库
- 当前真实执行如果要真正修改代码，下一步必须把 Jira task 的 `Workdir` 改成真实仓库路径

## 下一步实现建议

- 先确定你本机真实代码仓库路径
- 将 Jira task 中的 `Workdir` 写成真实存在路径
- 对需求文本，推荐顺序是：
  - `python scripts/orchestrator.py draft-plan-from-requirement <EPIC_KEY> <EPIC_SUMMARY> <FILE> --repo <REPO> --workdir <WORKDIR>`
  - `python scripts/orchestrator.py create-from-requirement <EPIC_KEY> <EPIC_SUMMARY> <FILE> --repo <REPO> --workdir <WORKDIR>`
- 对 AI 自动生成的 Jira task，推荐顺序是：
  - `python scripts/orchestrator.py prepare-task <ISSUE> --no-writeback`
  - `python scripts/orchestrator.py prepare-task <ISSUE> --auto-apply --only test_command --no-writeback`
  - `python scripts/orchestrator.py run-task <ISSUE> --no-claim --no-writeback --timeout 300`
- 后续再增加：
  - Jira 自定义字段映射
  - Epic 关联字段写入能力
  - `run-loop` 持续消费 ready 队列
  - 基于建议结果的审批式自动应用
