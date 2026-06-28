#!/usr/bin/env python3
"""Validate an OKF v0.1-style bundle and the optional Foundation Profile.

This validator is dependency-free and intentionally narrow. It checks only the
top-level YAML subset and Markdown conventions used by OKF Format Foundation.
It is not a general-purpose YAML parser and does not evaluate factual truth.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


RESERVED_NAMES = {"index.md", "log.md"}
FOUNDATION_REQUIRED = (
    "okf_version",
    "type",
    "title",
    "description",
    "tags",
    "timestamp",
    "source_title",
    "source_type",
    "source_locator",
    "source_access",
    "extraction_lens",
    "knowledge_status",
    "confidence",
    "human_confirmed_lens",
    "generated_with_ai",
)
VALID_SOURCE_ACCESS = {"complete", "partial", "unverified"}
VALID_KNOWLEDGE_STATUS = {"draft", "reviewed", "active", "retired"}
VALID_CONFIDENCE = {"high", "medium", "low"}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
DATE_HEADING_RE = re.compile(r"^##\s+\d{4}-\d{2}-\d{2}\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Finding:
    severity: str
    path: Path
    message: str


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, str], str, list[Finding]]:
    findings: list[Finding] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, [Finding("ERROR", path, "missing YAML frontmatter")]

    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return {}, text, [Finding("ERROR", path, "frontmatter has no closing delimiter")]

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:closing], start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[:1].isspace():
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            findings.append(
                Finding("WARNING", path, f"line {line_number}: unsupported top-level YAML syntax")
            )
            continue
        key, raw_value = match.groups()
        if key in metadata:
            findings.append(Finding("ERROR", path, f"duplicate frontmatter key: {key}"))
            continue
        metadata[key] = raw_value.strip().strip('"').strip("'")

    body = "\n".join(lines[closing + 1 :])
    return metadata, body, findings


def validate_timestamp(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_concept(path: Path, profile: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [Finding("ERROR", path, "file is not valid UTF-8")]

    metadata, body, parsed = parse_frontmatter(text, path)
    findings.extend(parsed)
    if any(f.severity == "ERROR" and "frontmatter" in f.message for f in parsed):
        return findings

    if not metadata.get("type", "").strip():
        findings.append(Finding("ERROR", path, "missing or empty required OKF field: type"))

    if profile == "foundation":
        for field in FOUNDATION_REQUIRED:
            if field == "type":
                continue
            if not metadata.get(field, "").strip():
                findings.append(Finding("ERROR", path, f"missing or empty Foundation field: {field}"))

        timestamp = metadata.get("timestamp", "")
        if timestamp and not validate_timestamp(timestamp):
            findings.append(Finding("ERROR", path, "timestamp is not valid ISO 8601"))

        source_access = metadata.get("source_access", "").lower()
        if source_access and source_access not in VALID_SOURCE_ACCESS:
            findings.append(
                Finding("ERROR", path, f"source_access must be one of {sorted(VALID_SOURCE_ACCESS)}")
            )

        status = metadata.get("knowledge_status", "").lower()
        if status and status not in VALID_KNOWLEDGE_STATUS:
            findings.append(
                Finding("ERROR", path, f"knowledge_status must be one of {sorted(VALID_KNOWLEDGE_STATUS)}")
            )

        confidence = metadata.get("confidence", "").lower()
        if confidence and confidence not in VALID_CONFIDENCE:
            findings.append(
                Finding("ERROR", path, f"confidence must be one of {sorted(VALID_CONFIDENCE)}")
            )

        for boolean_field in ("human_confirmed_lens", "generated_with_ai"):
            value = metadata.get(boolean_field, "").lower()
            if value and value not in {"true", "false"}:
                findings.append(Finding("ERROR", path, f"{boolean_field} must be true or false"))

        if "# Source-Supported Knowledge" not in body:
            findings.append(Finding("WARNING", path, "missing Source-Supported Knowledge section"))
        if "# Citations" not in body:
            findings.append(Finding("WARNING", path, "missing Citations section"))
        if metadata.get("source_access", "").lower() in {"partial", "unverified"} and "# Limitations and Open Questions" not in body:
            findings.append(
                Finding("WARNING", path, "partial or unverified source lacks Limitations and Open Questions")
            )

    return findings


def iter_markdown_files(bundle: Path) -> Iterable[Path]:
    return sorted(path for path in bundle.rglob("*.md") if path.is_file())


def resolve_link(bundle: Path, source: Path, target: str) -> Path | None:
    target = target.strip().split(maxsplit=1)[0].strip("<>")
    target = unquote(target.split("#", 1)[0])
    if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None
    if target.startswith("/"):
        return bundle / target.lstrip("/")
    return source.parent / target


def validate_links(bundle: Path, markdown_files: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            resolved = resolve_link(bundle, path, raw_target)
            if resolved is None:
                continue
            if not resolved.exists():
                findings.append(Finding("WARNING", path, f"broken internal link: {raw_target}"))
    return findings


def validate_reserved_files(bundle: Path, profile: str) -> list[Finding]:
    findings: list[Finding] = []
    index = bundle / "index.md"
    log = bundle / "log.md"

    if profile == "foundation":
        if not index.exists():
            findings.append(Finding("ERROR", index, "Foundation bundle requires index.md"))
        if not log.exists():
            findings.append(Finding("ERROR", log, "Foundation bundle requires log.md"))

    if index.exists():
        text = index.read_text(encoding="utf-8")
        if not re.search(r"^#\s+\S", text, re.MULTILINE):
            findings.append(Finding("WARNING", index, "index.md has no top-level heading"))

    if log.exists():
        text = log.read_text(encoding="utf-8")
        if not DATE_HEADING_RE.search(text):
            findings.append(Finding("WARNING", log, "log.md has no ISO date heading"))

    return findings


def validate_bundle(bundle: Path, profile: str) -> list[Finding]:
    if not bundle.exists():
        return [Finding("ERROR", bundle, "bundle path does not exist")]
    if not bundle.is_dir():
        return [Finding("ERROR", bundle, "bundle path is not a directory")]

    markdown_files = list(iter_markdown_files(bundle))
    concept_files = [path for path in markdown_files if path.name not in RESERVED_NAMES]
    findings = validate_reserved_files(bundle, profile)

    if not concept_files:
        findings.append(Finding("ERROR", bundle, "bundle contains no concept Markdown files"))
    for path in concept_files:
        findings.extend(validate_concept(path, profile))
    findings.extend(validate_links(bundle, markdown_files))
    return findings


def relative_display(path: Path, bundle: Path) -> str:
    try:
        return str(path.relative_to(bundle)) or "."
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an OKF-style bundle. This does not assess factual correctness."
    )
    parser.add_argument("bundle", type=Path, help="Path to the bundle root")
    parser.add_argument(
        "--profile",
        choices=("okf", "foundation"),
        default="foundation",
        help="Validation level (default: foundation)",
    )
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    findings = validate_bundle(bundle, args.profile)

    order = {"ERROR": 0, "WARNING": 1}
    for finding in sorted(findings, key=lambda item: (order[item.severity], str(item.path), item.message)):
        print(f"[{finding.severity}] {relative_display(finding.path, bundle)}: {finding.message}")

    errors = sum(f.severity == "ERROR" for f in findings)
    warnings = sum(f.severity == "WARNING" for f in findings)
    concepts = sum(
        path.name not in RESERVED_NAMES for path in iter_markdown_files(bundle)
    ) if bundle.is_dir() else 0

    if errors:
        outcome = "ERROR"
    elif warnings:
        outcome = "WARNING"
    else:
        outcome = "PASS"

    print(f"Outcome: {outcome} | Concepts: {concepts} | Errors: {errors} | Warnings: {warnings}")
    print("Structural validation does not prove factual correctness, authority, or freshness.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
