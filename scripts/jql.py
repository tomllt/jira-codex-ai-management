"""JQL builders for the Jira + Codex prototype."""

from __future__ import annotations


TASK_ISSUE_TYPE_ID = "10002"
SUBTASK_ISSUE_TYPE_ID = "10003"
TODO_STATUS_ID = "10000"


def build_ready_for_codex_jql(project_key: str, _ready_status: str, label_codex: str, label_ready_for_codex: str) -> str:
    return (
        f'project = "{project_key}" '
        f'AND issuetype in ({TASK_ISSUE_TYPE_ID}, {SUBTASK_ISSUE_TYPE_ID}) '
        f'AND status = {TODO_STATUS_ID} '
        f'AND labels = "{label_codex}" '
        f'AND labels = "{label_ready_for_codex}" '
        f'ORDER BY priority DESC, created ASC'
    )
