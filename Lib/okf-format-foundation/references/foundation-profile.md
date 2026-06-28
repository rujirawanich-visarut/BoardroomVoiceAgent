# OKF Format Foundation Profile v0.1

## Purpose

This profile adds provenance, human-selection, and lifecycle metadata while remaining readable as ordinary OKF Markdown. These fields are Foundation requirements, not universal OKF v0.1 requirements.

## Bundle Structure

```text
<bundle>/
├── index.md
├── log.md
└── concepts/
    └── <concept-slug>.md
```

Add subdirectories only when they improve navigation. Do not create an empty taxonomy in advance.

## Required Concept Frontmatter

```yaml
---
okf_version: "0.1"
type: Reference
title: Example Concept
description: One sentence describing the knowledge unit.
tags: [example]
timestamp: 2026-06-21T00:00:00Z
source_title: Example Source
source_type: web-page
source_locator: https://example.com/source
source_access: complete
extraction_lens: Source Fidelity
knowledge_status: draft
confidence: medium
human_confirmed_lens: true
generated_with_ai: true
---
```

Foundation-required fields:

- `okf_version`
- `type`
- `title`
- `description`
- `tags`
- `timestamp`
- `source_title`
- `source_type`
- `source_locator`
- `source_access`
- `extraction_lens`
- `knowledge_status`
- `confidence`
- `human_confirmed_lens`
- `generated_with_ai`

Use `source_locator: user-provided text` for knowledge supplied directly in conversation. Use a repository-relative path for local sources when portability permits. Do not invent a URL.

Recommended values:

- `source_access`: `complete`, `partial`, or `unverified`
- `knowledge_status`: `draft`, `reviewed`, `active`, or `retired`
- `confidence`: `high`, `medium`, or `low`

`human_confirmed_lens: true` means the human selected the extraction perspective. It does not mean the human reviewed every claim.

`generated_with_ai: true` discloses assistance. It does not identify a vendor and therefore remains portable.

## Concept Body

Use these sections when applicable:

```markdown
# Source-Supported Knowledge

# Interpretation Through the Selected Lens

# Limitations and Open Questions

# Related Concepts

# Citations
```

Omit an empty section rather than filling it with generic prose. Do not omit `# Limitations and Open Questions` when source access is partial or interpretation is material.

## Index

`index.md` should help a human or agent discover the bundle before opening every file:

```markdown
# Bundle Title

One-sentence purpose and source boundary.

## Concepts

- [Concept title](concepts/concept-slug.md) — one-sentence description.
```

## Log

`log.md` uses ISO dates, newest first:

```markdown
# Bundle Update Log

## 2026-06-21

- **Creation**: Added [Concept title](concepts/concept-slug.md) using the Source Fidelity lens.
```

## Concept Types

Prefer descriptive, ordinary language. Examples:

- `Reference`
- `Technical Specification`
- `Playbook`
- `Research Finding`
- `Strategic Interpretation`
- `Decision Pattern`
- `Metric Definition`
- `Process`

Do not force an existing type when a clearer new value is appropriate. OKF consumers should tolerate unknown types.

## Relationships

Use normal Markdown links and explain the relationship in prose. Do not imply typed graph semantics that the bundle does not encode.

## Canonical Source Policy

Choose one canonical representation. If JSON, HTML, or another index is needed, generate it from the Markdown concepts where practical. Do not maintain two manually edited sources of truth without an explicit reconciliation process.
