"""Helpers to build Jira comments from Codex execution results."""

from __future__ import annotations

from typing import Any


def _lines(title: str, items: list[str]) -> list[str]:
    section = [title]
    if items:
        section.extend([f"- {item}" for item in items])
    else:
        section.append("- None")
    return section


def build_execution_comment(execution_result: dict[str, Any], target_status: str) -> str:
    test_lines = [
        f'{item.get("command", "")} {_format_test_status(item.get("status", ""))}'.rstrip()
        for item in execution_result.get("test_results", [])
    ]

    lines: list[str] = [
        "[Codex Execution Update]",
        "",
        f"Status: {target_status}",
        "",
    ]
    lines.extend(_lines("Summary", execution_result.get("summary", [])))
    lines.append("")
    lines.extend(_lines("Files Touched", execution_result.get("files_touched", [])))
    lines.append("")
    lines.extend(_lines("Validation", test_lines))
    lines.append("")
    lines.extend(_lines("Risks / Notes", execution_result.get("risks", [])))

    blockers = execution_result.get("blockers", [])
    if blockers:
        lines.append("")
        lines.extend(_lines("Blockers", blockers))

    lines.append("")
    lines.extend(_lines("Next Step", [_next_step_text(target_status)]))
    return "\n".join(lines)


def map_result_to_status(result: str, blocked_status: str, review_status: str, in_progress_status: str) -> str:
    if result == "blocked":
        return blocked_status
    if result == "human_review":
        return review_status
    return in_progress_status


def labels_for_result(result: str, label_running: str, label_blocked: str, label_review: str) -> tuple[list[str], list[str]]:
    if result == "blocked":
        return [label_blocked], [label_running, label_review]
    if result == "human_review":
        return [label_review], [label_running, label_blocked]
    return [label_running], [label_blocked, label_review]


def _format_test_status(status: str) -> str:
    if status == "passed":
        return "✅"
    if status == "failed":
        return "❌"
    if status == "skipped":
        return "⚪"
    return status


def _next_step_text(status: str) -> str:
    if status == "处理中":
        return "请查看标签判断是阻塞中还是待人工复核"
    if status == "完成":
        return "任务已完成"
    return "任务仍在执行中或需要补充上下文"
