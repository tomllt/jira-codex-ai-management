# Jira Codex Refactor Implementation Plan

> **For Hermes:** Use `subagent-driven-development` skill to implement this plan task-by-task.

**Goal:** 将当前 `scripts/orchestrator.py` 为核心的原型脚本重构为可持续演进的分层应用结构，同时保持现有 CLI 命令和 Jira/Codex 主流程可用。

**Architecture:** 采用 `interfaces -> application -> domain -> adapters` 的分层结构。CLI 只负责参数解析和命令分发；应用层负责需求规划、任务预检、任务执行与结果回写；适配器层负责 Jira/Codex/Schema/描述模板等外部交互；领域层负责状态、标签、上下文与执行结果规则。

**Tech Stack:** Python 3、argparse、urllib、JSON Schema（现有 lightweight validator）、Codex CLI、Jira REST API。

---

## Preconditions

在开始前先阅读并理解：
- `README.md`
- `docs/overview.md`
- `docs/workflow.md`
- `docs/implementation.md`
- `scripts/orchestrator.py`
- `scripts/codex_runner.py`
- `scripts/planner_runner.py`
- `scripts/jira_client.py`

在整个实施过程中遵守：
- 保持现有命令兼容
- 小步提交
- 每个任务都先验证再进入下一步
- 不同时引入行为变更和结构变更，除非该任务明确要求

---

### Task 1: Create package skeleton

**Objective:** 创建新的 `src/jira_codex` 包结构，为后续平移做准备。

**Files:**
- Create: `src/jira_codex/__init__.py`
- Create: `src/jira_codex/config/__init__.py`
- Create: `src/jira_codex/domain/__init__.py`
- Create: `src/jira_codex/application/__init__.py`
- Create: `src/jira_codex/adapters/__init__.py`
- Create: `src/jira_codex/adapters/jira/__init__.py`
- Create: `src/jira_codex/adapters/codex/__init__.py`
- Create: `src/jira_codex/adapters/schema/__init__.py`
- Create: `src/jira_codex/interfaces/__init__.py`
- Create: `src/jira_codex/interfaces/cli/__init__.py`
- Create: `tests/unit/.gitkeep`
- Create: `tests/integration/.gitkeep`

**Step 1: Write failing test**

无需测试，纯结构准备。

**Step 2: Create directories and empty package files**

Create empty files with exactly these paths:

```text
src/jira_codex/__init__.py
src/jira_codex/config/__init__.py
src/jira_codex/domain/__init__.py
src/jira_codex/application/__init__.py
src/jira_codex/adapters/__init__.py
src/jira_codex/adapters/jira/__init__.py
src/jira_codex/adapters/codex/__init__.py
src/jira_codex/adapters/schema/__init__.py
src/jira_codex/interfaces/__init__.py
src/jira_codex/interfaces/cli/__init__.py
tests/unit/.gitkeep
tests/integration/.gitkeep
```

**Step 3: Verify structure**

Run: `find src/jira_codex -maxdepth 3 -type f | sort`
Expected: 列出所有新建 `__init__.py` 文件

**Step 4: Commit**

```bash
git add src/jira_codex tests
git commit -m "refactor: add layered package skeleton"
```

---

### Task 2: Move configuration helpers into package

**Objective:** 将配置加载逻辑迁移到新包中，并保持行为不变。

**Files:**
- Create: `src/jira_codex/config/settings.py`
- Modify: `scripts/config.py`
- Test: `tests/unit/test_settings.py`

**Step 1: Write failing test**

Create `tests/unit/test_settings.py`:

```python
from jira_codex.config.settings import Settings, validate_settings


def test_validate_settings_returns_missing_required_keys():
    settings = Settings(
        jira_base_url="",
        jira_username="",
        jira_password="",
        jira_project_key="",
    )

    missing = validate_settings(settings)

    assert missing == [
        "JIRA_BASE_URL",
        "JIRA_USERNAME",
        "JIRA_PASSWORD",
        "JIRA_PROJECT_KEY",
    ]
```

**Step 2: Run test to verify failure**

Run: `PYTHONPATH=src pytest tests/unit/test_settings.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'jira_codex'`

**Step 3: Write minimal implementation**

Create `src/jira_codex/config/settings.py` by moving the current content from `scripts/config.py` with the same public API:
- `Settings`
- `load_dotenv()`
- `load_settings()`
- `validate_settings()`

Then replace `scripts/config.py` with a compatibility shim:

```python
from jira_codex.config.settings import Settings, load_dotenv, load_settings, validate_settings

__all__ = ["Settings", "load_dotenv", "load_settings", "validate_settings"]
```

**Step 4: Run test to verify pass**

Run: `PYTHONPATH=src pytest tests/unit/test_settings.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jira_codex/config/settings.py scripts/config.py tests/unit/test_settings.py
git commit -m "refactor: move settings helpers into package"
```

---

### Task 3: Move schema validator into adapter layer

**Objective:** 将 schema 校验逻辑迁移到 `adapters/schema`，为后续 runner 解耦。

**Files:**
- Create: `src/jira_codex/adapters/schema/validator.py`
- Modify: `scripts/schema_validate.py`
- Test: `tests/unit/test_schema_validator.py`

**Step 1: Write failing test**

Create `tests/unit/test_schema_validator.py`:

```python
from jira_codex.adapters.schema.validator import SchemaValidationError, validate


def test_validate_raises_for_missing_required_field():
    schema = {
        "type": "object",
        "required": ["name"],
        "properties": {"name": {"type": "string"}},
    }

    try:
        validate({}, schema)
    except SchemaValidationError as exc:
        assert "missing required field 'name'" in str(exc)
    else:
        raise AssertionError("Expected SchemaValidationError")
```

**Step 2: Run test to verify failure**

Run: `PYTHONPATH=src pytest tests/unit/test_schema_validator.py -v`
Expected: FAIL — module not found

**Step 3: Write minimal implementation**

Move the contents of `scripts/schema_validate.py` into `src/jira_codex/adapters/schema/validator.py`.

Replace `scripts/schema_validate.py` with:

```python
from jira_codex.adapters.schema.validator import (
    AI_PLAN_SCHEMA,
    EXECUTION_RESULT_SCHEMA,
    SchemaValidationError,
    load_schema,
    validate,
    validate_ai_plan,
    validate_execution_result,
    validate_with_schema_name,
)
```

**Step 4: Run test to verify pass**

Run: `PYTHONPATH=src pytest tests/unit/test_schema_validator.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jira_codex/adapters/schema/validator.py scripts/schema_validate.py tests/unit/test_schema_validator.py
git commit -m "refactor: move schema validator into adapter layer"
```

---

### Task 4: Move Jira client into adapter layer

**Objective:** 将 Jira REST client 平移到新结构，并保留现有 import 兼容。

**Files:**
- Create: `src/jira_codex/adapters/jira/client.py`
- Modify: `scripts/jira_client.py`
- Test: `tests/unit/test_jira_client.py`

**Step 1: Write failing test**

Create `tests/unit/test_jira_client.py`:

```python
from jira_codex.adapters.jira.client import JiraClient
```

**Step 2: Run test to verify failure**

Run: `PYTHONPATH=src pytest tests/unit/test_jira_client.py -v`
Expected: FAIL — module not found

**Step 3: Write minimal implementation**

Move current client implementation into `src/jira_codex/adapters/jira/client.py` and keep `scripts/jira_client.py` as compatibility shim.

**Step 4: Run test to verify pass**

Run: `PYTHONPATH=src pytest tests/unit/test_jira_client.py -v`
Expected: PASS

---

后续任务继续按同样方式拆分迁移，确保每一步都保持 CLI 行为可用。