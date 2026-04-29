"""Lightweight schema validation helpers.

This validator intentionally supports only the subset of JSON Schema needed by
this prototype: type, required, enum, minimum, maximum, items, properties, and
$defs + local $ref.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
AI_PLAN_SCHEMA = "ai-plan.schema.json"
EXECUTION_RESULT_SCHEMA = "execution-result.schema.json"


class SchemaValidationError(ValueError):
    pass


def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMAS_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


def validate_with_schema_name(data: Any, schema_name: str) -> None:
    schema = load_schema(schema_name)
    validate(data, schema)


def validate_ai_plan(data: Any) -> None:
    validate_with_schema_name(data, AI_PLAN_SCHEMA)


def validate_execution_result(data: Any) -> None:
    validate_with_schema_name(data, EXECUTION_RESULT_SCHEMA)


def validate(data: Any, schema: dict[str, Any], root_schema: dict[str, Any] | None = None, path: str = "$") -> None:
    root = root_schema or schema

    if "$ref" in schema:
        target = _resolve_ref(root, schema["$ref"])
        validate(data, target, root, path)
        return

    expected_type = schema.get("type")
    if expected_type:
        _validate_type(data, expected_type, path)

    if "enum" in schema and data not in schema["enum"]:
        raise SchemaValidationError(f"{path}: expected one of {schema['enum']}, got {data!r}")

    if isinstance(data, (int, float)):
        if "minimum" in schema and data < schema["minimum"]:
            raise SchemaValidationError(f"{path}: expected >= {schema['minimum']}, got {data}")
        if "maximum" in schema and data > schema["maximum"]:
            raise SchemaValidationError(f"{path}: expected <= {schema['maximum']}, got {data}")

    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            raise SchemaValidationError(f"{path}: expected minLength {schema['minLength']}, got {len(data)}")

    if isinstance(data, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in data:
                raise SchemaValidationError(f"{path}: missing required field {key!r}")
        properties = schema.get("properties", {})
        for key, value in data.items():
            if key in properties:
                validate(value, properties[key], root, f"{path}.{key}")

    if isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            raise SchemaValidationError(f"{path}: expected at least {schema['minItems']} items, got {len(data)}")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(data):
                validate(item, item_schema, root, f"{path}[{index}]")


def _resolve_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise SchemaValidationError(f"Unsupported ref: {ref}")
    current: Any = root_schema
    for part in ref[2:].split("/"):
        current = current[part]
    if not isinstance(current, dict):
        raise SchemaValidationError(f"Invalid ref target: {ref}")
    return current


def _validate_type(data: Any, expected_type: str, path: str) -> None:
    ok = False
    if expected_type == "object":
        ok = isinstance(data, dict)
    elif expected_type == "array":
        ok = isinstance(data, list)
    elif expected_type == "string":
        ok = isinstance(data, str)
    elif expected_type == "number":
        ok = isinstance(data, (int, float)) and not isinstance(data, bool)
    elif expected_type == "integer":
        ok = isinstance(data, int) and not isinstance(data, bool)
    elif expected_type == "boolean":
        ok = isinstance(data, bool)
    elif expected_type == "null":
        ok = data is None
    else:
        raise SchemaValidationError(f"Unsupported schema type: {expected_type}")

    if not ok:
        raise SchemaValidationError(f"{path}: expected {expected_type}, got {type(data).__name__}")
