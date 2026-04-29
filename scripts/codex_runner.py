"""Codex CLI runner for Jira task execution.

The runner builds a self-contained prompt from a Jira issue and can either:
- return a deterministic dry-run execution result; or
- invoke Codex CLI non-interactively and parse a structured JSON result.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any
from difflib import get_close_matches


ROOT = Path(__file__).resolve().parents[1]
TASK_PROMPT_PATH = ROOT / "prompts" / "task_execution.prompt.md"
EXECUTION_SCHEMA_PATH = ROOT / "schemas" / "execution-result.schema.json"
DEFAULT_CODEX_HOME = Path(os.getenv("CODEX_HOME", "/root/.codex"))
DEFAULT_CODEX_USER_HOME = Path(os.getenv("CODEX_USER_HOME", "/root"))


class CodexRunner:
    def __init__(self, command: str | None = None, timeout_seconds: int = 1800) -> None:
        self.command = command or os.getenv("CODEX_COMMAND", "codex")
        self.timeout_seconds = timeout_seconds
        self.codex_home = Path(os.getenv("CODEX_HOME", str(DEFAULT_CODEX_HOME)))
        self.codex_user_home = Path(os.getenv("CODEX_USER_HOME", str(DEFAULT_CODEX_USER_HOME)))

    def build_task_context(self, issue: dict[str, Any]) -> dict[str, Any]:
        fields = issue.get("fields", {})
        description = fields.get("description") or ""
        test_command = self._extract_section_value(description, "Test Command")
        resolved_test_command = self._resolve_command_for_environment(test_command)
        return {
            "issue_key": issue.get("key", ""),
            "summary": fields.get("summary", ""),
            "description": description,
            "status": (fields.get("status") or {}).get("name", ""),
            "labels": fields.get("labels", []),
            "issue_type": (fields.get("issuetype") or {}).get("name", ""),
            "repo": self._extract_prefixed_value(description, "- Repo:"),
            "workdir": self._extract_prefixed_value(description, "- Workdir:"),
            "module_scope": self._extract_prefixed_values(description, "- Module:"),
            "test_command": test_command,
            "resolved_test_command": resolved_test_command,
        }

    def build_prompt(self, issue: dict[str, Any]) -> str:
        context = self.build_task_context(issue)
        system_prompt = TASK_PROMPT_PATH.read_text(encoding="utf-8")
        return "\n\n".join(
            [
                system_prompt,
                "Task Context:",
                json.dumps(context, ensure_ascii=False, indent=2),
                "Output JSON only.",
            ]
        )

    def dry_run(self, issue: dict[str, Any]) -> dict[str, Any]:
        context = self.build_task_context(issue)
        return {
            "issue_key": context["issue_key"],
            "result": "human_review",
            "summary": [
                "Dry-run execution completed",
                "No repository changes were made",
            ],
            "files_touched": [],
            "test_results": [
                {
                    "command": context.get("resolved_test_command") or context.get("test_command") or "dry-run",
                    "status": "skipped",
                }
            ],
            "risks": [
                "This is a dry-run result and does not include real code execution",
            ],
            "blockers": [],
            "artifacts": {
                "commit_link": "",
                "pr_link": "",
            },
        }

    def assess(self, issue: dict[str, Any]) -> dict[str, Any]:
        context = self.build_task_context(issue)
        preflight_error = self._preflight_context_error(context)
        resolved_test_command = context.get("resolved_test_command") or context.get("test_command") or ""
        if preflight_error:
            return {
                "issue_key": context["issue_key"],
                "result": "blocked",
                "summary": [
                    "Task preflight assessment found execution blockers",
                    "Codex execution was not started",
                ],
                "files_touched": [],
                "test_results": [
                    {
                        "command": resolved_test_command or "preflight",
                        "status": "skipped",
                    }
                ],
                "risks": [
                    "Task definition or environment must be corrected before execution",
                ],
                "blockers": [preflight_error],
                "artifacts": {
                    "commit_link": "",
                    "pr_link": "",
                },
            }

        summary = [
            "Task preflight assessment passed basic repository and environment checks",
            "Codex execution may proceed with the declared scope",
        ]
        risks = [
            "Preflight only validates declared scope and command availability, not business correctness",
        ]
        return {
            "issue_key": context["issue_key"],
            "result": "human_review",
            "summary": summary,
            "files_touched": [],
            "test_results": [
                {
                    "command": resolved_test_command or "preflight",
                    "status": "skipped",
                }
            ],
            "risks": risks,
            "blockers": [],
            "artifacts": {
                "commit_link": "",
                "pr_link": "",
            },
        }

    def suggest_scope_fixes(self, issue: dict[str, Any]) -> dict[str, Any]:
        context = self.build_task_context(issue)
        workdir_value = (context.get("workdir") or "").strip()
        workdir = Path(workdir_value) if workdir_value else None
        declared_modules = context.get("module_scope") or []
        suggested_modules: list[str] = []
        module_notes: list[str] = []

        if workdir and workdir.exists() and workdir.is_dir():
            suggested_modules, module_notes = self._suggest_modules(workdir, declared_modules)

        suggested_workdir = workdir_value
        workdir_note = "Declared workdir is usable"
        if not workdir_value:
            workdir_note = "Task is missing Workdir; no automatic workdir candidate found"
        elif not workdir or not workdir.exists():
            workdir_note = "Declared Workdir does not exist"
        elif not workdir.is_dir():
            workdir_note = "Declared Workdir is not a directory"

        resolved_test_command = context.get("resolved_test_command") or ""
        suggested_test_command = resolved_test_command or context.get("test_command") or ""
        test_command_note = self._test_command_suggestion_note(context.get("test_command") or "")

        return {
            "issue_key": context["issue_key"],
            "current": {
                "repo": context.get("repo") or "",
                "workdir": workdir_value,
                "modules": declared_modules,
                "test_command": context.get("test_command") or "",
            },
            "suggested": {
                "repo": context.get("repo") or "",
                "workdir": suggested_workdir,
                "modules": suggested_modules,
                "test_command": suggested_test_command,
            },
            "notes": {
                "workdir": workdir_note,
                "modules": module_notes,
                "test_command": test_command_note,
            },
        }

    def run(self, issue: dict[str, Any], dry_run: bool = False, timeout_seconds: int | None = None) -> dict[str, Any]:
        if dry_run:
            return self.dry_run(issue)

        context = self.build_task_context(issue)
        workdir = context.get("workdir") or ""
        preflight_error = self._preflight_context_error(context)
        if preflight_error:
            return self._blocked_result(issue, preflight_error)

        prompt = self.build_prompt(issue)
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False, encoding="utf-8") as temp_output:
            output_path = temp_output.name

        command = [self.command, "exec", "--skip-git-repo-check", "--sandbox", "workspace-write"]
        if workdir:
            command.extend(["-C", workdir])
        command.extend([
            "--output-schema",
            str(EXECUTION_SCHEMA_PATH),
            "--output-last-message",
            output_path,
            "-",
        ])

        env = os.environ.copy()
        env["CODEX_HOME"] = str(self.codex_home)
        env["HOME"] = str(self.codex_user_home)

        timeout_value = timeout_seconds or self.timeout_seconds

        try:
            process = subprocess.run(
                command,
                input=prompt,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_value,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return self._blocked_result(issue, f"Codex execution timed out after {timeout_value} seconds")
        except Exception as exc:
            return self._blocked_result(issue, f"Failed to start Codex CLI: {exc}")

        if process.returncode != 0:
            return self._blocked_result(
                issue,
                "Codex command failed: "
                f"exit={process.returncode}; stderr={process.stderr.strip() or '<empty>'}; "
                f"stdout={process.stdout.strip()[:1000] or '<empty>'}; "
                f"CODEX_HOME={self.codex_home}; HOME={self.codex_user_home}; "
                f"WORKDIR={workdir or '<none>'}",
            )

        try:
            raw = Path(output_path).read_text(encoding="utf-8").strip()
        except Exception as exc:
            return self._blocked_result(issue, f"Failed to read Codex output file: {exc}")
        finally:
            try:
                Path(output_path).unlink(missing_ok=True)
            except Exception:
                pass

        if not raw:
            return self._blocked_result(issue, "Codex output file was empty")

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            snippet = raw[:1000]
            return self._blocked_result(issue, f"Failed to parse Codex JSON output: {exc}; output={snippet}")

    def _blocked_result(self, issue: dict[str, Any], reason: str) -> dict[str, Any]:
        issue_key = issue.get("key", "")
        return {
            "issue_key": issue_key,
            "result": "blocked",
            "summary": ["Codex execution did not complete successfully"],
            "files_touched": [],
            "test_results": [],
            "risks": [],
            "blockers": [reason],
            "artifacts": {
                "commit_link": "",
                "pr_link": "",
            },
        }

    def _preflight_context_error(self, context: dict[str, Any]) -> str | None:
        workdir_value = (context.get("workdir") or "").strip()
        if not workdir_value:
            return "Task description is missing Workdir"

        workdir = Path(workdir_value)
        if not workdir.exists():
            return f"Task Workdir does not exist: {workdir_value}"
        if not workdir.is_dir():
            return f"Task Workdir is not a directory: {workdir_value}"

        missing_modules = self._find_missing_modules(workdir, context.get("module_scope") or [])
        if missing_modules:
            missing_display = ", ".join(missing_modules)
            return (
                "Task modules do not exist under Workdir: "
                f"{missing_display}; workdir={workdir_value}"
            )

        test_command = (context.get("test_command") or "").strip()
        command_error = self._preflight_test_command_error(test_command)
        if command_error:
            return command_error
        return None

    def _preflight_test_command_error(self, test_command: str) -> str | None:
        if not test_command:
            return None

        resolved = self._resolve_command_for_environment(test_command)
        if not resolved:
            first_token = test_command.split()[0]
            if first_token == "pnpm" and shutil.which("corepack"):
                return (
                    "Task test command requires pnpm, but pnpm is not available and corepack could not prepare it; "
                    "this environment likely lacks working network/proxy access for corepack package bootstrap"
                )
            return f"Task test command executable is not available in PATH: {first_token}"
        return None

    def _resolve_command_for_environment(self, command: str) -> str:
        command = command.strip()
        if not command:
            return ""

        parts = command.split(maxsplit=1)
        executable = parts[0]
        remainder = parts[1] if len(parts) > 1 else ""

        if shutil.which(executable):
            return command

        if executable == "pnpm" and shutil.which("corepack"):
            if self._corepack_can_prepare_pnpm():
                return f"corepack pnpm {remainder}".strip()
            return ""

        return ""

    def _corepack_can_prepare_pnpm(self) -> bool:
        try:
            process = subprocess.run(
                ["corepack", "pnpm", "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=20,
            )
        except Exception:
            return False
        return process.returncode == 0

    def _find_missing_modules(self, workdir: Path, module_scope: list[str]) -> list[str]:
        missing: list[str] = []
        for raw_module in module_scope:
            module = raw_module.strip()
            if not module:
                continue
            candidate = workdir / module
            if not candidate.exists():
                missing.append(module)
        return missing

    def _suggest_modules(self, workdir: Path, module_scope: list[str]) -> tuple[list[str], list[str]]:
        suggestions: list[str] = []
        notes: list[str] = []
        existing_relative_paths = [str(path.relative_to(workdir)) for path in workdir.rglob("*") if path.is_file()]

        for raw_module in module_scope:
            module = raw_module.strip()
            if not module:
                continue
            candidate = workdir / module
            if candidate.exists():
                suggestions.append(module)
                notes.append(f"Module exists: {module}")
                continue

            module_path = Path(module)
            module_name = module_path.name
            module_suffix = module_path.suffix
            parent_tail = "/".join(module_path.parts[-3:-1]) if len(module_path.parts) >= 3 else ""

            exact_name_matches = [
                path for path in existing_relative_paths
                if Path(path).name == module_name and (not module_suffix or Path(path).suffix == module_suffix)
            ]
            if exact_name_matches:
                selected = exact_name_matches[0]
                suggestions.append(selected)
                notes.append(f"Module '{module}' not found; suggested exact filename match '{selected}'")
                continue

            filtered_candidates = [
                path for path in existing_relative_paths
                if (not module_suffix or Path(path).suffix == module_suffix)
                and (not parent_tail or parent_tail in path)
            ]
            close_matches = get_close_matches(module_name, [Path(path).name for path in filtered_candidates], n=1, cutoff=0.8)
            if close_matches:
                matched_name = close_matches[0]
                matched_path = next((path for path in filtered_candidates if Path(path).name == matched_name), matched_name)
                suggestions.append(matched_path)
                notes.append(f"Module '{module}' not found; suggested similar file '{matched_path}'")
                continue

            notes.append(f"No local module suggestion found for '{module}'")

        return suggestions, notes

    def _test_command_suggestion_note(self, test_command: str) -> str:
        if not test_command:
            return "Task is missing Test Command"
        resolved = self._resolve_command_for_environment(test_command)
        if resolved and resolved == test_command:
            return "Declared test command is directly executable"
        if resolved:
            return f"Declared test command is executable after environment adaptation: {resolved}"
        first_token = test_command.split()[0]
        if first_token == "pnpm" and shutil.which("corepack"):
            return "pnpm is unavailable and corepack fallback is currently not usable in this environment"
        return f"Executable '{first_token}' is unavailable in PATH"

    def _extract_prefixed_value(self, text: str, prefix: str) -> str:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(prefix):
                return stripped[len(prefix):].strip()
        return ""

    def _extract_prefixed_values(self, text: str, prefix: str) -> list[str]:
        values: list[str] = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(prefix):
                values.append(stripped[len(prefix):].strip())
        return values

    def _extract_section_value(self, text: str, section_name: str) -> str:
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.strip() == section_name and index + 1 < len(lines):
                next_line = lines[index + 1].strip()
                if next_line.startswith("- "):
                    return next_line[2:].strip()
        return ""
