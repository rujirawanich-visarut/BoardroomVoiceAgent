import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any


SCHEMA_FILES = {
    "EvidenceSchema": Path(__file__).parent / "schemas" / "evidence_schema.json",
}


class StructuredResponseError(ValueError):
    def __init__(self, stage: str, message: str):
        super().__init__(message)
        self.stage = stage


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise StructuredResponseError("parse", f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_non_standard_constant(value: str) -> None:
    raise StructuredResponseError("parse", f"Non-standard JSON constant: {value}")


@lru_cache(maxsize=None)
def _schema(schema_name: str) -> dict:
    schema_path = SCHEMA_FILES.get(schema_name)
    if schema_path is None:
        raise StructuredResponseError("configuration", f"Unknown schema: {schema_name}")
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _resolve_ref(root_schema: dict, reference: str) -> dict:
    if not reference.startswith("#/"):
        raise StructuredResponseError("configuration", f"Unsupported schema reference: {reference}")
    node: Any = root_schema
    for part in reference[2:].split("/"):
        if not isinstance(node, dict) or part not in node:
            raise StructuredResponseError("configuration", f"Invalid schema reference: {reference}")
        node = node[part]
    if not isinstance(node, dict):
        raise StructuredResponseError("configuration", f"Schema reference is not an object: {reference}")
    return node


def _validate_node(value: Any, schema: dict, root_schema: dict, path: str) -> None:
    if "$ref" in schema:
        _validate_node(value, _resolve_ref(root_schema, schema["$ref"]), root_schema, path)
        return

    expected_type = schema.get("type")
    type_matches = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "boolean": isinstance(value, bool),
    }
    if expected_type in type_matches and not type_matches[expected_type]:
        raise StructuredResponseError("schema", f"{path}: expected {expected_type}")

    if expected_type == "object":
        required = schema.get("required", [])
        for field_name in required:
            if field_name not in value:
                raise StructuredResponseError("schema", f"{path}: missing required field '{field_name}'")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise StructuredResponseError("schema", f"{path}: unknown field '{unknown[0]}'")
        for field_name, field_value in value.items():
            if field_name in properties:
                _validate_node(field_value, properties[field_name], root_schema, f"{path}.{field_name}")

    elif expected_type == "array":
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                _validate_node(item, item_schema, root_schema, f"{path}[{index}]")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                raise StructuredResponseError("schema", f"{path}: array items must be unique")

    elif expected_type == "string":
        if len(value) < schema.get("minLength", 0):
            raise StructuredResponseError("schema", f"{path}: string is shorter than minLength")
        pattern = schema.get("pattern")
        if pattern and re.search(pattern, value) is None:
            raise StructuredResponseError("schema", f"{path}: string does not match required pattern")


def parse_and_validate_structured_response(raw_response: str, schema_name: str) -> dict:
    """Parse one strict JSON object and validate it against the named schema."""
    if not isinstance(raw_response, str):
        raise StructuredResponseError("parse", "Model response must cross the boundary as a JSON string.")

    try:
        parsed = json.loads(
            raw_response,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_non_standard_constant,
        )
    except StructuredResponseError:
        raise
    except json.JSONDecodeError as exc:
        raise StructuredResponseError(
            "parse",
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
        ) from exc

    if not isinstance(parsed, dict):
        raise StructuredResponseError("parse", "Model response root must be a JSON object.")

    root_schema = _schema(schema_name)
    _validate_node(parsed, root_schema, root_schema, "$")
    return parsed
