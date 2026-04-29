"""Minimal Jira REST client for the Jira + Codex prototype.

Supports Jira Server/Data Center style REST usage and can also work with
Cloud-style credentials when configured accordingly.
"""

from __future__ import annotations

import base64
import json
from typing import Any
from urllib import error, request

from config import Settings


class JiraClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.base_api_url = settings.jira_base_url.rstrip("/") + f"/rest/api/{settings.jira_api_version}"
        auth = f"{settings.jira_username}:{settings.jira_password}".encode("utf-8")
        self.auth_header = "Basic " + base64.b64encode(auth).decode("ascii")

    def get_issue(self, issue_key: str) -> dict[str, Any]:
        return self._request_json("GET", f"/issue/{issue_key}")

    def get_server_info(self) -> dict[str, Any]:
        return self._request_json("GET", "/serverInfo")

    def get_myself(self) -> dict[str, Any]:
        return self._request_json("GET", "/myself")

    def get_project(self, project_key: str) -> dict[str, Any]:
        return self._request_json("GET", f"/project/{project_key}")

    def search_issues(self, jql: str, fields: list[str] | None = None, max_results: int = 20) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "jql": jql,
            "maxResults": max_results,
        }
        if fields:
            payload["fields"] = fields
        return self._request_json("POST", "/search", payload)

    def create_issue(self, fields: dict[str, Any]) -> dict[str, Any]:
        return self._request_json("POST", "/issue", {"fields": fields})

    def add_comment(self, issue_key: str, comment_body: str) -> dict[str, Any]:
        payload = {"body": comment_body}
        return self._request_json("POST", f"/issue/{issue_key}/comment", payload)

    def transition_issue(self, issue_key: str, transition_id: str) -> dict[str, Any]:
        payload = {"transition": {"id": transition_id}}
        return self._request_json("POST", f"/issue/{issue_key}/transitions", payload)

    def list_transitions(self, issue_key: str) -> dict[str, Any]:
        return self._request_json("GET", f"/issue/{issue_key}/transitions")

    def update_issue_fields(self, issue_key: str, fields: dict[str, Any]) -> dict[str, Any]:
        return self._request_json("PUT", f"/issue/{issue_key}", {"fields": fields})

    def update_issue_labels(self, issue_key: str, add_labels: list[str] | None = None, remove_labels: list[str] | None = None) -> dict[str, Any]:
        operations: list[dict[str, Any]] = []
        for label in add_labels or []:
            operations.append({"add": label})
        for label in remove_labels or []:
            operations.append({"remove": label})
        if not operations:
            return {}
        return self._request_json("PUT", f"/issue/{issue_key}", {"update": {"labels": operations}})

    def find_transition_id_by_name(self, issue_key: str, target_status_name: str) -> str | None:
        data = self.list_transitions(issue_key)
        for item in data.get("transitions", []):
            to_block = item.get("to", {})
            if to_block.get("name") == target_status_name:
                return item.get("id")
        return None

    def claim_task(self, issue_key: str, in_progress_status: str) -> dict[str, Any]:
        transition_id = self.find_transition_id_by_name(issue_key, in_progress_status)
        if not transition_id:
            raise RuntimeError(f"No transition found for status: {in_progress_status}")
        return self.transition_issue(issue_key, transition_id)

    def _request_json(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = None
        headers = {
            "Authorization": self.auth_header,
            "Accept": "application/json",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = request.Request(
            url=self.base_api_url + path,
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with request.urlopen(req) as response:
                raw = response.read().decode("utf-8")
                if not raw.strip():
                    return {}
                return json.loads(raw)
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Jira API error {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Jira API connection error: {exc}") from exc


def build_story_fields(project_key: str, summary: str, description: str, issue_type: str, labels: list[str]) -> dict[str, Any]:
    return {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
        "labels": labels,
    }


def build_task_fields(
    project_key: str,
    summary: str,
    description: str,
    issue_type: str,
    labels: list[str],
    parent_key: str | None = None,
) -> dict[str, Any]:
    fields = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
        "labels": labels,
    }
    if parent_key:
        fields["parent"] = {"key": parent_key}
    return fields
