# 数据模型与模板

## 推荐字段清单

### Task 必备字段

- `Repo`
- `Workdir`
- `Module Scope`
- `Acceptance Criteria`
- `Definition of Done`
- `Execution Hint`
- `Test Command`
- `PR Link`
- `Commit Link`
- `AI Status`
- `AI Confidence`
- `AI Risk Notes`

### 推荐标签

- `ai-drafted`
- `codex`
- `backend`
- `frontend`
- `qa`
- `docs`
- `needs-human-review`
- `blocked`

## Story 模板

```text
Background
- <业务背景>

User Value
- 作为 <角色>，我希望 <能力>，从而 <收益>

Scope
- <本 Story 范围>

Non-goals
- <不做什么>

Acceptance Criteria
- [ ] <AC1>
- [ ] <AC2>
- [ ] <AC3>

Dependencies
- <依赖项>

Risks
- <风险项>
```

## Task 模板

```text
Background
- Derived from <STORY-KEY>

Objective
- <本任务目标>

Technical Scope
- Repo: <repo>
- Workdir: <workdir>
- Module Scope: <paths>

Definition of Done
- [ ] <DoD1>
- [ ] <DoD2>

Acceptance Criteria
- [ ] <AC1>
- [ ] <AC2>

Execution Hint
- <对 Codex 的执行提示>

Test Command
- <command>

Risks / Notes
- <说明>
```

## AI 生成计划 JSON

```json
{
  "epic_key": "PROJ-123",
  "epic_summary": "支付回调幂等能力建设",
  "stories": [
    {
      "summary": "支持支付回调幂等处理",
      "description": "作为支付系统，我希望重复回调不会重复入账，从而保证账务一致性。",
      "labels": ["ai-drafted"],
      "acceptance_criteria": [
        "重复回调不会导致重复记账",
        "异常回调会被记录并可追踪"
      ],
      "dependencies": [
        "依赖现有订单状态查询接口"
      ],
      "risks": [
        "历史数据可能缺少唯一事件标识"
      ],
      "tasks": [
        {
          "summary": "实现支付回调幂等校验逻辑",
          "issue_type": "Task",
          "labels": ["ai-drafted", "codex", "backend"],
          "repo": "payment-service",
          "workdir": "/workspace/payment-service",
          "module_scope": [
            "src/payment/callback_handler.py",
            "src/payment/service.py"
          ],
          "definition_of_done": [
            "重复回调不会重复执行入账逻辑",
            "新增对应单元测试"
          ],
          "acceptance_criteria": [
            "同一事件二次回调时返回成功但不重复写账",
            "失败路径保留错误日志"
          ],
          "execution_hint": "优先检查现有事件ID去重机制，不要修改对外接口契约。",
          "test_command": "pytest tests/payment -q",
          "risk_notes": [
            "若缺少唯一事件ID，需要补充兼容策略"
          ],
          "ai_confidence": 0.86
        }
      ]
    }
  ],
  "questions_for_human": [
    "是否允许引入新的幂等存储表？"
  ]
}
```

## Codex 执行输入模板

```text
Task: PROJ-456
Summary: 实现支付回调幂等校验逻辑

Background:
<task description>

Acceptance Criteria:
- ...
- ...

Definition of Done:
- ...
- ...

Repo:
payment-service

Workdir:
/workspace/payment-service

Module Scope:
- src/payment/callback_handler.py
- src/payment/service.py

Constraints:
- 不修改外部 API 契约
- 优先复用现有幂等机制
- 修改尽量保持最小范围

Required Output:
- 变更摘要
- 修改文件列表
- 测试结果
- 风险与阻塞
- 建议回写 Jira comment
```

## Codex 执行结果 JSON

```json
{
  "issue_key": "PROJ-456",
  "result": "human_review",
  "summary": [
    "已实现支付回调幂等校验",
    "补充重复回调测试用例"
  ],
  "files_touched": [
    "src/payment/callback_handler.py",
    "tests/payment/test_callback_handler.py"
  ],
  "test_results": [
    {
      "command": "pytest tests/payment -q",
      "status": "passed"
    }
  ],
  "risks": [
    "当前依赖事件ID唯一性，若上游不保证可能需要二次补强"
  ],
  "blockers": [],
  "artifacts": {
    "commit_link": "",
    "pr_link": ""
  }
}
```
