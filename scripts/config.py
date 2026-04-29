"""Configuration helpers for the Jira + Codex prototype."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    jira_base_url: str
    jira_username: str
    jira_password: str
    jira_project_key: str
    jira_api_version: str = "2"
    jira_default_issue_type_story: str = "故事"
    jira_default_issue_type_task: str = "任务"
    jira_default_issue_type_subtask: str = "子任务"
    codex_ready_status: str = "待办"
    codex_in_progress_status: str = "处理中"
    codex_blocked_status: str = "处理中"
    human_review_status: str = "处理中"
    done_status: str = "完成"
    label_codex: str = "codex"
    label_ai_drafted: str = "ai-drafted"
    label_ready_for_codex: str = "ready-for-codex"
    label_codex_blocked: str = "codex-blocked"
    label_needs_human_review: str = "needs-human-review"
    label_codex_running: str = "codex-running"


def load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_settings() -> Settings:
    root = Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env")

    return Settings(
        jira_base_url=os.getenv("JIRA_BASE_URL", ""),
        jira_username=os.getenv("JIRA_USERNAME", os.getenv("JIRA_EMAIL", "")),
        jira_password=os.getenv("JIRA_PASSWORD", os.getenv("JIRA_API_TOKEN", "")),
        jira_project_key=os.getenv("JIRA_PROJECT_KEY", ""),
        jira_api_version=os.getenv("JIRA_API_VERSION", "2"),
        jira_default_issue_type_story=os.getenv("JIRA_ISSUE_TYPE_STORY", "故事"),
        jira_default_issue_type_task=os.getenv("JIRA_ISSUE_TYPE_TASK", "任务"),
        jira_default_issue_type_subtask=os.getenv("JIRA_ISSUE_TYPE_SUBTASK", "子任务"),
        codex_ready_status=os.getenv("JIRA_STATUS_READY_FOR_CODEX", "待办"),
        codex_in_progress_status=os.getenv("JIRA_STATUS_CODEX_IN_PROGRESS", "处理中"),
        codex_blocked_status=os.getenv("JIRA_STATUS_CODEX_BLOCKED", "处理中"),
        human_review_status=os.getenv("JIRA_STATUS_HUMAN_REVIEW", "处理中"),
        done_status=os.getenv("JIRA_STATUS_DONE", "完成"),
        label_codex=os.getenv("JIRA_LABEL_CODEX", "codex"),
        label_ai_drafted=os.getenv("JIRA_LABEL_AI_DRAFTED", "ai-drafted"),
        label_ready_for_codex=os.getenv("JIRA_LABEL_READY_FOR_CODEX", "ready-for-codex"),
        label_codex_blocked=os.getenv("JIRA_LABEL_CODEX_BLOCKED", "codex-blocked"),
        label_needs_human_review=os.getenv("JIRA_LABEL_NEEDS_HUMAN_REVIEW", "needs-human-review"),
        label_codex_running=os.getenv("JIRA_LABEL_CODEX_RUNNING", "codex-running"),
    )


def validate_settings(settings: Settings) -> list[str]:
    missing: list[str] = []
    if not settings.jira_base_url:
        missing.append("JIRA_BASE_URL")
    if not settings.jira_username:
        missing.append("JIRA_USERNAME")
    if not settings.jira_password:
        missing.append("JIRA_PASSWORD")
    if not settings.jira_project_key:
        missing.append("JIRA_PROJECT_KEY")
    return missing
