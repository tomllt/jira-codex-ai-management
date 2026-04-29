#!/usr/bin/env python3
"""Prototype orchestrator for Jira + Codex CLI workflow."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

from codex_runner import CodexRunner
from comment_builder import build_execution_comment, labels_for_result, map_result_to_status
from config import load_settings, validate_settings
from jira_client import JiraClient, build_story_fields, build_task_fields
from jql import build_ready_for_codex_jql
from planner_runner import PlannerRunner
from schema_validate import SchemaValidationError, validate_ai_plan, validate_execution_result


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"
DEFAULT_TIMEOUT_SECONDS = 1800


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def require_settings() -> tuple[Any, JiraClient]:
    settings = load_settings()
    missing = validate_settings(settings)
    if missing:
        raise SystemExit(f"Missing required config: {', '.join(missing)}")
    return settings, JiraClient(settings)


def cmd_plan_example() -> None:
    print_json(load_json(EXAMPLES_DIR / "sample-ai-plan.json"))


def cmd_result_example() -> None:
    print_json(load_json(EXAMPLES_DIR / "sample-execution-result.json"))


def cmd_check_config() -> None:
    settings = load_settings()
    missing = validate_settings(settings)
    result = {
        "jira_base_url": settings.jira_base_url,
        "jira_project_key": settings.jira_project_key,
        "jira_api_version": settings.jira_api_version,
        "jira_username": settings.jira_username,
        "missing": missing,
        "valid": not missing,
    }
    print_json(result)


def cmd_check_jira() -> None:
    settings, client = require_settings()
    server_info = client.get_server_info()
    myself = client.get_myself()
    project = client.get_project(settings.jira_project_key)
    result = {
        "connected": True,
        "jira_base_url": settings.jira_base_url,
        "jira_project_key": settings.jira_project_key,
        "server": {
            "title": server_info.get("serverTitle", ""),
            "version": server_info.get("version", ""),
            "deployment_type": server_info.get("deploymentType", ""),
            "base_url": server_info.get("baseUrl", ""),
        },
        "auth": {
            "name": myself.get("name", ""),
            "display_name": myself.get("displayName", ""),
            "email_address": myself.get("emailAddress", ""),
            "active": myself.get("active", False),
        },
        "project": {
            "key": project.get("key", ""),
            "name": project.get("name", ""),
            "project_type_key": project.get("projectTypeKey", ""),
        },
    }
    print_json(result)


def cmd_validate(kind: str, path: str) -> None:
    data = load_json(Path(path))
    try:
        if kind == "ai-plan":
            validate_ai_plan(data)
        elif kind == "execution-result":
            validate_execution_result(data)
        else:
            raise SystemExit(f"Unknown schema kind: {kind}")
    except SchemaValidationError as exc:
        raise SystemExit(f"Schema validation failed: {exc}") from exc
    print_json({"valid": True, "kind": kind, "path": path})


def cmd_build_jql() -> None:
    settings = load_settings()
    if not settings.jira_project_key:
        raise SystemExit("Missing required config: JIRA_PROJECT_KEY")
    print(_build_ready_jql(settings))


def _build_ready_jql(settings: Any) -> str:
    return build_ready_for_codex_jql(
        settings.jira_project_key,
        settings.codex_ready_status,
        settings.label_codex,
        settings.label_ready_for_codex,
    )


def _search_ready(settings: Any, client: JiraClient, limit: int) -> dict[str, Any]:
    return client.search_issues(
        jql=_build_ready_jql(settings),
        fields=["summary", "status", "labels", "issuetype", "description", "comment"],
        max_results=limit,
    )


def cmd_search_ready(limit: int) -> None:
    settings, client = require_settings()
    print_json(_search_ready(settings, client, limit))


def cmd_get_issue(issue_key: str) -> None:
    _, client = require_settings()
    print_json(client.get_issue(issue_key))


def _claim_task(settings: Any, client: JiraClient, issue_key: str) -> dict[str, Any]:
    response = client.claim_task(issue_key, settings.codex_in_progress_status)
    client.update_issue_labels(
        issue_key,
        add_labels=[settings.label_codex_running],
        remove_labels=[settings.label_ready_for_codex, settings.label_codex_blocked, settings.label_needs_human_review],
    )
    return response


def cmd_claim(issue_key: str) -> None:
    settings, client = require_settings()
    response = _claim_task(settings, client, issue_key)
    print_json({"issue_key": issue_key, "claimed": True, "response": response})


def cmd_comment_from_example() -> None:
    settings = load_settings()
    result = load_json(EXAMPLES_DIR / "sample-execution-result.json")
    validate_execution_result(result)
    target_status = map_result_to_status(
        result=result["result"],
        blocked_status=settings.codex_blocked_status,
        review_status=settings.human_review_status,
        in_progress_status=settings.codex_in_progress_status,
    )
    print(build_execution_comment(result, target_status))


def _writeback_result(settings: Any, client: JiraClient, execution_result: dict[str, Any]) -> dict[str, Any]:
    validate_execution_result(execution_result)
    target_status = map_result_to_status(
        result=execution_result["result"],
        blocked_status=settings.codex_blocked_status,
        review_status=settings.human_review_status,
        in_progress_status=settings.codex_in_progress_status,
    )
    add_labels, remove_labels = labels_for_result(
        result=execution_result["result"],
        label_running=settings.label_codex_running,
        label_blocked=settings.label_codex_blocked,
        label_review=settings.label_needs_human_review,
    )
    comment = build_execution_comment(execution_result, target_status)
    issue_key = execution_result["issue_key"]
    transition_id = client.find_transition_id_by_name(issue_key, target_status)
    if transition_id:
        client.transition_issue(issue_key, transition_id)
    client.update_issue_labels(issue_key, add_labels=add_labels, remove_labels=remove_labels)
    comment_response = client.add_comment(issue_key, comment)
    return {
        "issue_key": issue_key,
        "target_status": target_status,
        "transition_id": transition_id,
        "labels_added": add_labels,
        "labels_removed": remove_labels,
        "comment_response": comment_response,
    }


def cmd_writeback_from_example(issue_key: str | None) -> None:
    settings, client = require_settings()
    result = load_json(EXAMPLES_DIR / "sample-execution-result.json")
    if issue_key:
        result["issue_key"] = issue_key
    print_json(_writeback_result(settings, client, result))


def _assess_issue(settings: Any, client: JiraClient, issue_key: str, writeback: bool) -> dict[str, Any]:
    issue = client.get_issue(issue_key)
    runner = CodexRunner()
    execution_result = runner.assess(issue)
    validate_execution_result(execution_result)
    response: dict[str, Any] = {
        "issue_key": issue_key,
        "assessment_result": execution_result,
    }
    if writeback:
        response["writeback"] = _writeback_result(settings, client, execution_result)
    return response


def _run_issue(
    settings: Any,
    client: JiraClient,
    issue_key: str,
    dry_run: bool,
    no_claim: bool,
    no_writeback: bool,
    timeout_seconds: int,
) -> dict[str, Any]:
    response: dict[str, Any] = {"issue_key": issue_key, "dry_run": dry_run, "timeout_seconds": timeout_seconds}
    if not no_claim:
        response["claim"] = _claim_task(settings, client, issue_key)
    issue = client.get_issue(issue_key)
    runner = CodexRunner(timeout_seconds=timeout_seconds)
    execution_result = runner.run(issue, dry_run=dry_run, timeout_seconds=timeout_seconds)
    validate_execution_result(execution_result)
    response["execution_result"] = execution_result
    if not no_writeback:
        response["writeback"] = _writeback_result(settings, client, execution_result)
    return response


def cmd_run_task(issue_key: str, dry_run: bool, no_claim: bool, no_writeback: bool, timeout_seconds: int) -> None:
    settings, client = require_settings()
    print_json(_run_issue(settings, client, issue_key, dry_run, no_claim, no_writeback, timeout_seconds))


def cmd_preflight_task(issue_key: str, no_writeback: bool) -> None:
    settings, client = require_settings()
    print_json(_assess_issue(settings, client, issue_key, writeback=not no_writeback))


def cmd_suggest_task_fixes(issue_key: str) -> None:
    _, client = require_settings()
    issue = client.get_issue(issue_key)
    runner = CodexRunner()
    print_json(runner.suggest_scope_fixes(issue))


def _prepare_task(
    settings: Any,
    client: JiraClient,
    issue_key: str,
    auto_apply: bool,
    only_fields: list[str] | None,
    exclude_fields: list[str] | None,
    writeback: bool,
) -> dict[str, Any]:
    issue = client.get_issue(issue_key)
    runner = CodexRunner()
    suggestion = runner.suggest_scope_fixes(issue)
    selected_updates = _select_suggested_updates(suggestion, set(only_fields or []), set(exclude_fields or []))

    response: dict[str, Any] = {
        "issue_key": issue_key,
        "suggestion": suggestion,
        "selected_updates": selected_updates,
        "auto_apply": auto_apply,
    }

    if auto_apply and any(value is not None for value in selected_updates.values()):
        response["apply_result"] = _update_task_scope(
            client,
            issue_key,
            repo=selected_updates["repo"],
            workdir=selected_updates["workdir"],
            modules=selected_updates["modules"],
            test_command=selected_updates["test_command"],
        )

    response["preflight_result"] = _assess_issue(settings, client, issue_key, writeback=writeback)
    return response


def cmd_prepare_task(
    issue_key: str,
    auto_apply: bool,
    only_fields: list[str] | None,
    exclude_fields: list[str] | None,
    no_writeback: bool,
) -> None:
    settings, client = require_settings()
    print_json(
        _prepare_task(
            settings,
            client,
            issue_key,
            auto_apply=auto_apply,
            only_fields=only_fields,
            exclude_fields=exclude_fields,
            writeback=not no_writeback,
        )
    )


def cmd_run_next(dry_run: bool, no_writeback: bool, timeout_seconds: int) -> None:
    settings, client = require_settings()
    search_result = _search_ready(settings, client, limit=1)
    issues = search_result.get("issues", [])
    if not issues:
        print_json({"ran": False, "reason": "No ready-for-codex issues found"})
        return
    issue_key = issues[0]["key"]
    result = _run_issue(
        settings,
        client,
        issue_key,
        dry_run=dry_run,
        no_claim=False,
        no_writeback=no_writeback,
        timeout_seconds=timeout_seconds,
    )
    result["ran"] = True
    print_json(result)


def _story_description(story: dict[str, Any]) -> str:
    parts = [
        f"Summary\n- {story['description']}",
        "",
        "Acceptance Criteria",
        *[f"- {item}" for item in story.get("acceptance_criteria", [])],
        "",
        "Dependencies",
        *[f"- {item}" for item in story.get("dependencies", [])],
        "",
        "Risks",
        *[f"- {item}" for item in story.get("risks", [])],
    ]
    return "\n".join(parts)


def _task_description(task: dict[str, Any]) -> str:
    parts = [
        "Technical Scope",
        f"- Repo: {task.get('repo', '')}",
        f"- Workdir: {task.get('workdir', '')}",
        *[f"- Module: {item}" for item in task.get("module_scope", [])],
        "",
        "Definition of Done",
        *[f"- {item}" for item in task.get("definition_of_done", [])],
        "",
        "Acceptance Criteria",
        *[f"- {item}" for item in task.get("acceptance_criteria", [])],
        "",
        "Execution Hint",
        f"- {task.get('execution_hint', '')}",
        "",
        "Test Command",
        f"- {task.get('test_command', '')}",
        "",
        "Risk Notes",
        *[f"- {item}" for item in task.get("risk_notes", [])],
    ]
    return "\n".join(parts)


def cmd_create_from_plan(plan_path: str) -> None:
    settings, client = require_settings()
    plan = load_json(Path(plan_path))
    validate_ai_plan(plan)
    created: dict[str, Any] = {"stories": []}

    for story in plan.get("stories", []):
        story_fields = build_story_fields(
            project_key=settings.jira_project_key,
            summary=story["summary"],
            description=_story_description(story),
            issue_type=settings.jira_default_issue_type_story,
            labels=list(dict.fromkeys(story.get("labels", []) + [settings.label_ai_drafted])),
        )
        created_story = client.create_issue(story_fields)
        story_entry = {"story": created_story, "tasks": []}

        for task in story.get("tasks", []):
            task_labels = list(
                dict.fromkeys(
                    task.get("labels", [])
                    + [settings.label_ai_drafted, settings.label_codex, settings.label_ready_for_codex]
                )
            )
            task_fields = build_task_fields(
                project_key=settings.jira_project_key,
                summary=task["summary"],
                description=_task_description(task),
                issue_type=settings.jira_default_issue_type_task,
                labels=task_labels,
                parent_key=None,
            )
            created_task = client.create_issue(task_fields)
            story_entry["tasks"].append(created_task)

        created["stories"].append(story_entry)

    print_json(created)


def cmd_draft_plan_from_requirement(
    epic_key: str,
    epic_summary: str,
    requirement_path: str,
    repo: str,
    workdir: str,
    labels: list[str] | None,
    use_codex: bool,
    timeout_seconds: int,
) -> None:
    requirement_text = Path(requirement_path).read_text(encoding="utf-8")
    runner = PlannerRunner(timeout_seconds=timeout_seconds)
    if use_codex:
        plan = runner.run_codex(epic_key, epic_summary, requirement_text, repo, workdir, labels)
    else:
        plan = runner.draft_plan(epic_key, epic_summary, requirement_text, repo, workdir, labels)
    validate_ai_plan(plan)
    print_json(plan)


def cmd_create_from_requirement(
    epic_key: str,
    epic_summary: str,
    requirement_path: str,
    repo: str,
    workdir: str,
    labels: list[str] | None,
    use_codex: bool,
    timeout_seconds: int,
) -> None:
    requirement_text = Path(requirement_path).read_text(encoding="utf-8")
    runner = PlannerRunner(timeout_seconds=timeout_seconds)
    if use_codex:
        plan = runner.run_codex(epic_key, epic_summary, requirement_text, repo, workdir, labels)
    else:
        plan = runner.draft_plan(epic_key, epic_summary, requirement_text, repo, workdir, labels)
    validate_ai_plan(plan)

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False, encoding="utf-8") as temp_plan:
        temp_plan.write(json.dumps(plan, ensure_ascii=False, indent=2))
        temp_plan_path = temp_plan.name
    try:
        cmd_create_from_plan(temp_plan_path)
    finally:
        Path(temp_plan_path).unlink(missing_ok=True)


def _replace_single_prefixed_line(description: str, prefix: str, replacement: str) -> tuple[str, str | None]:
    old_line = None
    updated_lines: list[str] = []
    replaced = False
    for line in description.splitlines():
        if line.strip().startswith(prefix):
            old_line = line
            updated_lines.append(replacement)
            replaced = True
        else:
            updated_lines.append(line)
    if not replaced:
        raise SystemExit(f"Issue description does not contain a '{prefix}' line")
    return "\n".join(updated_lines), old_line


def _replace_module_lines(description: str, modules: list[str]) -> str:
    lines = description.splitlines()
    updated_lines: list[str] = []
    in_technical_scope = False
    modules_written = False
    for line in lines:
        stripped = line.strip()
        if stripped == "Technical Scope":
            in_technical_scope = True
            updated_lines.append(line)
            continue
        if in_technical_scope and stripped == "":
            if not modules_written:
                for module in modules:
                    updated_lines.append(f"- Module: {module}")
                modules_written = True
            in_technical_scope = False
            updated_lines.append(line)
            continue
        if in_technical_scope and stripped.startswith("- Module:"):
            continue
        updated_lines.append(line)
    if not modules_written:
        raise SystemExit("Issue description does not contain a Technical Scope section")
    return "\n".join(updated_lines)


def _replace_test_command(description: str, test_command: str) -> str:
    lines = description.splitlines()
    updated_lines: list[str] = []
    replaced = False
    index = 0
    while index < len(lines):
        line = lines[index]
        updated_lines.append(line)
        if line.strip() == "Test Command":
            if index + 1 >= len(lines):
                raise SystemExit("Issue description Test Command section is incomplete")
            index += 1
            updated_lines.append(f"- {test_command}")
            replaced = True
            index += 1
            continue
        index += 1
    if not replaced:
        raise SystemExit("Issue description does not contain a Test Command section")
    return "\n".join(updated_lines)


def _update_task_scope(
    client: JiraClient,
    issue_key: str,
    repo: str | None,
    workdir: str | None,
    modules: list[str] | None,
    test_command: str | None,
) -> dict[str, Any]:
    issue = client.get_issue(issue_key)
    description = (issue.get("fields") or {}).get("description") or ""
    changes: dict[str, Any] = {}

    if repo:
        description, old_repo = _replace_single_prefixed_line(description, "- Repo:", f"- Repo: {repo}")
        changes["old_repo_line"] = old_repo
        changes["new_repo_line"] = f"- Repo: {repo}"
    if workdir:
        description, old_workdir = _replace_single_prefixed_line(description, "- Workdir:", f"- Workdir: {workdir}")
        changes["old_workdir_line"] = old_workdir
        changes["new_workdir_line"] = f"- Workdir: {workdir}"
    if modules is not None:
        description = _replace_module_lines(description, modules)
        changes["new_modules"] = modules
    if test_command:
        description = _replace_test_command(description, test_command)
        changes["new_test_command"] = test_command

    if not changes:
        raise SystemExit("No scope changes requested")

    client.update_issue_fields(issue_key, {"description": description})
    return {"issue_key": issue_key, "updated": True, **changes}


def cmd_set_workdir(issue_key: str, workdir: str) -> None:
    _, client = require_settings()
    print_json(_update_task_scope(client, issue_key, repo=None, workdir=workdir, modules=None, test_command=None))


def cmd_refine_task_scope(
    issue_key: str,
    repo: str | None,
    workdir: str | None,
    modules: list[str] | None,
    test_command: str | None,
) -> None:
    _, client = require_settings()
    print_json(_update_task_scope(client, issue_key, repo=repo, workdir=workdir, modules=modules, test_command=test_command))


def _select_suggested_updates(
    suggestion: dict[str, Any],
    only_fields: set[str] | None,
    exclude_fields: set[str] | None,
) -> dict[str, Any]:
    current = suggestion.get("current", {})
    suggested = suggestion.get("suggested", {})
    allowed_fields = {"repo", "workdir", "modules", "test_command"}
    only_fields = (only_fields or set()) & allowed_fields
    exclude_fields = (exclude_fields or set()) & allowed_fields

    def include(field: str) -> bool:
        if only_fields and field not in only_fields:
            return False
        if field in exclude_fields:
            return False
        return True

    return {
        "repo": suggested.get("repo") if include("repo") and suggested.get("repo") != current.get("repo") else None,
        "workdir": suggested.get("workdir") if include("workdir") and suggested.get("workdir") != current.get("workdir") else None,
        "modules": suggested.get("modules") if include("modules") and suggested.get("modules") != current.get("modules") else None,
        "test_command": suggested.get("test_command") if include("test_command") and suggested.get("test_command") != current.get("test_command") else None,
    }


def cmd_apply_task_fixes(issue_key: str, dry_run: bool, only_fields: list[str] | None, exclude_fields: list[str] | None) -> None:
    _, client = require_settings()
    issue = client.get_issue(issue_key)
    runner = CodexRunner()
    suggestion = runner.suggest_scope_fixes(issue)
    selected = _select_suggested_updates(suggestion, set(only_fields or []), set(exclude_fields or []))

    if not any(value is not None for value in selected.values()):
        print_json({
            "issue_key": issue_key,
            "updated": False,
            "reason": "No applicable fixes suggested for the selected fields",
            "suggestion": suggestion,
            "selected_updates": selected,
        })
        return

    if dry_run:
        print_json({
            "issue_key": issue_key,
            "updated": False,
            "dry_run": True,
            "selected_updates": selected,
            "suggestion": suggestion,
        })
        return

    result = _update_task_scope(
        client,
        issue_key,
        repo=selected["repo"],
        workdir=selected["workdir"],
        modules=selected["modules"],
        test_command=selected["test_command"],
    )
    result["applied_from_suggestion"] = suggestion
    result["selected_updates"] = selected
    print_json(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Jira + Codex prototype orchestrator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("plan-example", help="Print sample AI plan JSON")
    subparsers.add_parser("result-example", help="Print sample execution result JSON")
    subparsers.add_parser("check-config", help="Validate Jira configuration")
    subparsers.add_parser("check-jira", help="Validate Jira connectivity, auth, and project access")
    subparsers.add_parser("build-jql", help="Print ready-for-codex JQL")
    subparsers.add_parser("comment-example", help="Build sample Jira comment from execution result")

    validate_parser = subparsers.add_parser("validate", help="Validate a JSON file against a project schema")
    validate_parser.add_argument("kind", choices=["ai-plan", "execution-result"])
    validate_parser.add_argument("path")

    search_parser = subparsers.add_parser("search-ready", help="Search current sprint ready tasks")
    search_parser.add_argument("--limit", type=int, default=10)

    get_issue_parser = subparsers.add_parser("get-issue", help="Fetch a Jira issue by key")
    get_issue_parser.add_argument("issue_key")

    set_workdir_parser = subparsers.add_parser("set-workdir", help="Update the Workdir line in a Jira task description")
    set_workdir_parser.add_argument("issue_key")
    set_workdir_parser.add_argument("workdir")

    refine_scope_parser = subparsers.add_parser("refine-task-scope", help="Refine repo/workdir/module/test-command lines in a Jira task description")
    refine_scope_parser.add_argument("issue_key")
    refine_scope_parser.add_argument("--repo", default=None)
    refine_scope_parser.add_argument("--workdir", default=None)
    refine_scope_parser.add_argument("--module", action="append", dest="modules")
    refine_scope_parser.add_argument("--test-command", default=None)

    claim_parser = subparsers.add_parser("claim", help="Claim a task by moving it to 处理中")
    claim_parser.add_argument("issue_key")

    writeback_parser = subparsers.add_parser("writeback-example", help="Transition and comment using sample execution result")
    writeback_parser.add_argument("--issue-key", default=None)

    preflight_parser = subparsers.add_parser("preflight-task", help="Assess a Jira task for scope and environment readiness without running Codex")
    preflight_parser.add_argument("issue_key")
    preflight_parser.add_argument("--no-writeback", action="store_true", help="Skip Jira comment/status/label writeback")

    suggest_parser = subparsers.add_parser("suggest-task-fixes", help="Suggest workdir/module/test-command fixes for a Jira task")
    suggest_parser.add_argument("issue_key")

    apply_parser = subparsers.add_parser("apply-task-fixes", help="Apply suggested task fixes back into the Jira task description")
    apply_parser.add_argument("issue_key")
    apply_parser.add_argument("--dry-run", action="store_true", help="Preview the selected updates without writing to Jira")
    apply_parser.add_argument("--only", action="append", choices=["repo", "workdir", "modules", "test_command"], help="Only apply selected field types")
    apply_parser.add_argument("--exclude", action="append", choices=["repo", "workdir", "modules", "test_command"], help="Exclude selected field types from application")

    prepare_parser = subparsers.add_parser("prepare-task", help="Suggest, optionally apply, and preflight a Jira task in one command")
    prepare_parser.add_argument("issue_key")
    prepare_parser.add_argument("--auto-apply", action="store_true", help="Apply selected suggestions before running preflight")
    prepare_parser.add_argument("--only", action="append", choices=["repo", "workdir", "modules", "test_command"], help="Only select suggestions from these field types")
    prepare_parser.add_argument("--exclude", action="append", choices=["repo", "workdir", "modules", "test_command"], help="Exclude suggestions from these field types")
    prepare_parser.add_argument("--no-writeback", action="store_true", help="Skip Jira comment/status/label writeback during preflight")

    create_parser = subparsers.add_parser("create-from-plan", help="Create stories and tasks from a plan JSON file")
    create_parser.add_argument("plan_path")

    draft_requirement_parser = subparsers.add_parser("draft-plan-from-requirement", help="Generate an AI plan JSON from a requirement document")
    draft_requirement_parser.add_argument("epic_key")
    draft_requirement_parser.add_argument("epic_summary")
    draft_requirement_parser.add_argument("requirement_path")
    draft_requirement_parser.add_argument("--repo", required=True)
    draft_requirement_parser.add_argument("--workdir", required=True)
    draft_requirement_parser.add_argument("--label", action="append", dest="labels")
    draft_requirement_parser.add_argument("--use-codex", action="store_true", help="Use real Codex planning instead of deterministic draft mode")
    draft_requirement_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)

    create_requirement_parser = subparsers.add_parser("create-from-requirement", help="Generate a plan from a requirement document and create Jira issues")
    create_requirement_parser.add_argument("epic_key")
    create_requirement_parser.add_argument("epic_summary")
    create_requirement_parser.add_argument("requirement_path")
    create_requirement_parser.add_argument("--repo", required=True)
    create_requirement_parser.add_argument("--workdir", required=True)
    create_requirement_parser.add_argument("--label", action="append", dest="labels")
    create_requirement_parser.add_argument("--use-codex", action="store_true", help="Use real Codex planning instead of deterministic draft mode")
    create_requirement_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)

    run_parser = subparsers.add_parser("run-task", help="Claim, execute, and write back a Jira task")
    run_parser.add_argument("issue_key")
    run_parser.add_argument("--dry-run", action="store_true", help="Return a deterministic result without invoking Codex CLI")
    run_parser.add_argument("--no-claim", action="store_true", help="Skip moving the issue to running state")
    run_parser.add_argument("--no-writeback", action="store_true", help="Skip Jira comment/status/label writeback")
    run_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Execution timeout in seconds")

    run_next_parser = subparsers.add_parser("run-next", help="Run the next ready-for-codex Jira task")
    run_next_parser.add_argument("--dry-run", action="store_true", help="Return a deterministic result without invoking Codex CLI")
    run_next_parser.add_argument("--no-writeback", action="store_true", help="Skip Jira comment/status/label writeback")
    run_next_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Execution timeout in seconds")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "plan-example":
        cmd_plan_example()
        return
    if args.command == "result-example":
        cmd_result_example()
        return
    if args.command == "check-config":
        cmd_check_config()
        return
    if args.command == "check-jira":
        cmd_check_jira()
        return
    if args.command == "validate":
        cmd_validate(args.kind, args.path)
        return
    if args.command == "build-jql":
        cmd_build_jql()
        return
    if args.command == "comment-example":
        cmd_comment_from_example()
        return
    if args.command == "search-ready":
        cmd_search_ready(args.limit)
        return
    if args.command == "get-issue":
        cmd_get_issue(args.issue_key)
        return
    if args.command == "set-workdir":
        cmd_set_workdir(args.issue_key, args.workdir)
        return
    if args.command == "refine-task-scope":
        cmd_refine_task_scope(args.issue_key, args.repo, args.workdir, args.modules, args.test_command)
        return
    if args.command == "claim":
        cmd_claim(args.issue_key)
        return
    if args.command == "writeback-example":
        cmd_writeback_from_example(args.issue_key)
        return
    if args.command == "preflight-task":
        cmd_preflight_task(args.issue_key, args.no_writeback)
        return
    if args.command == "suggest-task-fixes":
        cmd_suggest_task_fixes(args.issue_key)
        return
    if args.command == "apply-task-fixes":
        cmd_apply_task_fixes(args.issue_key, args.dry_run, args.only, args.exclude)
        return
    if args.command == "prepare-task":
        cmd_prepare_task(args.issue_key, args.auto_apply, args.only, args.exclude, args.no_writeback)
        return
    if args.command == "create-from-plan":
        cmd_create_from_plan(args.plan_path)
        return
    if args.command == "draft-plan-from-requirement":
        cmd_draft_plan_from_requirement(
            args.epic_key,
            args.epic_summary,
            args.requirement_path,
            args.repo,
            args.workdir,
            args.labels,
            args.use_codex,
            args.timeout,
        )
        return
    if args.command == "create-from-requirement":
        cmd_create_from_requirement(
            args.epic_key,
            args.epic_summary,
            args.requirement_path,
            args.repo,
            args.workdir,
            args.labels,
            args.use_codex,
            args.timeout,
        )
        return
    if args.command == "run-task":
        cmd_run_task(args.issue_key, args.dry_run, args.no_claim, args.no_writeback, args.timeout)
        return
    if args.command == "run-next":
        cmd_run_next(args.dry_run, args.no_writeback, args.timeout)
        return

    parser.error("Unknown command")


if __name__ == "__main__":
    main()
