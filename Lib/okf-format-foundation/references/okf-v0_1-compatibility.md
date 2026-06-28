# OKF v0.1 Compatibility Boundary

## Purpose

Use this reference to distinguish the Open Knowledge Format v0.1 draft from the stricter, optional OKF Format Foundation profile.

Official announcement:

- [Introducing the Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/)

This pack does not reproduce or replace the authoritative specification. Verify the current specification and license before public redistribution or production adoption.

## Minimum OKF v0.1 Model

An OKF bundle is a directory tree of human-readable Markdown documents.

A normal concept document:

- is UTF-8 Markdown;
- starts with YAML frontmatter;
- has a non-empty `type` field;
- uses its bundle-relative file path, without `.md`, as its concept ID;
- may use Markdown links to other concepts;
- may include external citations.

Reserved names:

- `index.md` lists available concepts for progressive disclosure;
- `log.md` records dated updates.

The draft is deliberately permissive:

- type values are not centrally registered;
- unknown types and additional frontmatter fields should be tolerated;
- optional metadata may be absent;
- broken links do not make the bundle malformed;
- directory organization remains domain-defined.

## What OKF Does Not Establish

OKF conformance does not prove:

- factual truth;
- source authority;
- knowledge freshness;
- semantic completeness;
- legal or regulatory applicability;
- ontology quality;
- typed graph semantics;
- automatic enrichment or retrieval;
- readiness for a particular agent runtime.

The Foundation Profile adds provenance and workflow expectations, but those additions must not be represented as requirements of OKF v0.1 itself.

## Compatibility Policy for This Pack

Produce concepts that remain readable as ordinary OKF Markdown. Add Foundation metadata as producer-defined fields. Preserve unknown fields when editing. Treat validation findings beyond a missing frontmatter block or `type` as Foundation Profile results, not universal OKF failures.
