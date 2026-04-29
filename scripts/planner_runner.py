"""Requirement-to-plan runner for Jira intake workflows.

This runner converts a free-form requirement into an AI plan JSON compatible with
`schemas/ai-plan.schema.json`. It supports:
- a deterministic draft mode for local prototyping
- a Codex-backed mode using `codex exec` with schema-constrained output
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from schema_validate import validate_ai_plan


ROOT = Path(__file__).resolve().parents[1]
PLAN_PROMPT_PATH = ROOT / "prompts" / "epic_to_plan.prompt.md"
PLAN_SCHEMA_PATH = ROOT / "schemas" / "ai-plan.schema.json"
DEFAULT_CODEX_HOME = Path(os.getenv("CODEX_HOME", "/root/.codex"))
DEFAULT_CODEX_USER_HOME = Path(os.getenv("CODEX_USER_HOME", "/root"))


class PlannerRunner:
    def __init__(self, command: str | None = None, timeout_seconds: int = 1800) -> None:
        self.command = command or os.getenv("CODEX_COMMAND", "codex")
        self.timeout_seconds = timeout_seconds
        self.codex_home = Path(os.getenv("CODEX_HOME", str(DEFAULT_CODEX_HOME)))
        self.codex_user_home = Path(os.getenv("CODEX_USER_HOME", str(DEFAULT_CODEX_USER_HOME)))

    def build_prompt(
        self,
        epic_key: str,
        epic_summary: str,
        requirement_text: str,
        repo: str,
        workdir: str,
        labels: list[str] | None = None,
    ) -> str:
        system_prompt = PLAN_PROMPT_PATH.read_text(encoding="utf-8")
        payload = {
            "epic_key": epic_key,
            "epic_summary": epic_summary,
            "requirement_text": requirement_text,
            "repo": repo,
            "workdir": workdir,
            "labels": labels or [],
        }
        return "\n\n".join(
            [
                system_prompt,
                "Requirement Context:",
                json.dumps(payload, ensure_ascii=False, indent=2),
                "Output JSON only.",
            ]
        )

    def draft_plan(
        self,
        epic_key: str,
        epic_summary: str,
        requirement_text: str,
        repo: str,
        workdir: str,
        labels: list[str] | None = None,
    ) -> dict[str, Any]:
        task_summary = self._summarize_requirement(epic_summary, requirement_text)
        label_list = list(dict.fromkeys((labels or []) + ["ai-drafted"]))
        plan = {
            "epic_key": epic_key,
            "epic_summary": epic_summary,
            "stories": [
                {
                    "summary": f"围绕『{epic_summary}』完成首轮任务拆解",
                    "description": requirement_text.strip(),
                    "labels": label_list,
                    "acceptance_criteria": [
                        "需求被拆解为可独立执行的 Jira Task",
                        "每个 Task 都包含明确范围、验收标准和测试命令",
                    ],
                    "dependencies": [],
                    "risks": [
                        "当前为 AI draft，可能仍需人工补充业务约束",
                    ],
                    "tasks": [
                        {
                            "summary": task_summary,
                            "issue_type": "Task",
                            "labels": list(dict.fromkeys(label_list + ["codex"])),
                            "repo": repo,
                            "workdir": workdir,
                            "module_scope": ["TODO: refine module scope"],
                            "definition_of_done": [
                                "完成首轮实现或验证所需的最小代码变更",
                                "补充或确认可运行的测试命令",
                            ],
                            "acceptance_criteria": [
                                "任务范围与目标仓库匹配",
                                "能够通过 prepare-task / preflight-task 审查",
                            ],
                            "execution_hint": "先用 prepare-task 生成建议并修正任务 scope，再执行真正的 run-task。",
                            "test_command": "TODO: refine test command",
                            "risk_notes": [
                                "需要人工确认 module_scope 与 test_command",
                            ],
                            "ai_confidence": 0.55,
                        }
                    ],
                }
            ],
            "questions_for_human": [
                "是否有明确的目标模块或服务目录？",
                "是否有推荐的测试命令？",
            ],
        }
        validate_ai_plan(plan)
        return plan

    def run_codex(
        self,
        epic_key: str,
        epic_summary: str,
        requirement_text: str,
        repo: str,
        workdir: str,
        labels: list[str] | None = None,
        timeout_seconds: int | None = None,
    ) -> dict[str, Any]:
        prompt = self.build_prompt(epic_key, epic_summary, requirement_text, repo, workdir, labels)
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False, encoding="utf-8") as temp_output:
            output_path = temp_output.name

        command = [
            self.command,
            "exec",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "--output-schema",
            str(PLAN_SCHEMA_PATH),
            "--output-last-message",
            output_path,
            "-",
        ]

        env = os.environ.copy()
        env["CODEX_HOME"] = str(self.codex_home)
        env["HOME"] = str(self.codex_user_home)

        timeout_value = timeout_seconds or self.timeout_seconds
        process = subprocess.run(
            command,
            input=prompt,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_value,
            env=env,
        )
        if process.returncode != 0:
            raise RuntimeError(
                "Codex planning command failed: "
                f"exit={process.returncode}; stderr={process.stderr.strip() or '<empty>'}; "
                f"stdout={process.stdout.strip()[:1000] or '<empty>'}"
            )

        raw = Path(output_path).read_text(encoding="utf-8").strip()
        try:
            Path(output_path).unlink(missing_ok=True)
        except Exception:
            pass
        if not raw:
            raise RuntimeError("Codex planning output file was empty")

        plan = json.loads(raw)
        validate_ai_plan(plan)
        return plan

    def _summarize_requirement(self, epic_summary: str, requirement_text: str) -> str:
        text = requirement_text.strip().splitlines()[0] if requirement_text.strip() else epic_summary
        text = text.strip()
        if len(text) > 40:
            text = text[:40].rstrip() + "…"
        return f"基于需求草案落实：{text or epic_summary}"
