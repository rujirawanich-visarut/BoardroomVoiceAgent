---
name: okf-format-foundation
description: Convert web pages, documents, notes, transcripts, specifications, and human-provided knowledge into portable, diffable Open Knowledge Format (OKF) bundles. Use when an agent can read and write repository files and the user wants source-grounded knowledge extraction, three context-sensitive extraction lenses, an explicit human lens-selection checkpoint, provenance-aware Markdown concepts, or an OKF-compatible knowledge bundle that other humans and AI systems can read.
---

# OKF Format Foundation

Turn source material into portable human-and-agent-readable knowledge without hiding the perspective used to extract it.

The governing sequence is:

```text
Human Knowledge
-> three extraction lenses
-> human confirmation
-> source-grounded concepts
-> validated OKF bundle
```

Do not treat a lens as truth. A lens controls attention; it must not change what the source says.

## Load the Foundation Rules

Before proposing lenses, read:

- `references/okf-v0_1-compatibility.md` for the OKF v0.1 boundary;
- `references/lens-protocol.md` for lens generation and the user checkpoint;
- `references/foundation-profile.md` before writing concept files;
- `references/provenance-rules.md` when the source includes external claims, uncertain authorship, interpretation, or existing concepts.

## Workflow

### 1. Establish the source boundary

Inventory what was actually supplied or successfully retrieved:

- source title or working title;
- source type;
- source locator such as URL, repository path, or `user-provided text`;
- whether the source was read completely;
- access limitations, missing pages, images, tables, or attachments;
- language and likely audience;
- whether the source is primary, secondary, or human recollection when that can be determined.

If a URL cannot be accessed, ask the user to provide the page as text or a file. Never reconstruct the unavailable page from model memory.

### 2. Propose three extraction lenses

Unless the user already explicitly selected a lens and requested direct writing, propose exactly three meaningfully distinct lenses.

Lens 1 must be **Source Fidelity**. Generate Lens 2 and Lens 3 from the source using the model's own relevant capabilities. Suitable choices may be technical, operational, strategic, critical, governance, research, pedagogical, historical, legal, systems, or decision-oriented.

For every lens state:

- what it foregrounds;
- what it deliberately leaves secondary;
- likely concept types;
- interpretation level: low, medium, or high;
- the lens's main blind spot.

Do not create three cosmetic variations of the same summary.

### 3. Pause for human confirmation

Stop after presenting the lenses. Do not create or modify an OKF bundle until the user:

- chooses one lens;
- combines named lenses; or
- explicitly requests a new set of lenses.

Include the proposed target path in the same checkpoint. If the user supplied no path, propose:

```text
knowledge/<source-slug>/
```

The user may confirm lens and path in one response.

Skip this pause only when the user has already named the lens or explicitly requested direct Source Fidelity extraction and supplied or accepted a target path.

### 4. Design the concept split

After confirmation, decide whether the source should become one concept or a small group of concepts.

Prefer one concept when the source explains one coherent idea. Split only when concepts have distinct purposes, audiences, provenance, or lifecycle. Avoid fragmenting headings into separate files merely because the source has sections.

Before writing, briefly state the planned concepts and relationships.

### 5. Extract with epistemic separation

Preserve three boundaries:

1. **Source-supported knowledge** — directly supported by the supplied source.
2. **Interpretation through the selected lens** — reasoned implications, explicitly labeled.
3. **Limitations and open questions** — uncertainty, missing context, and claims requiring verification.

Do not silently add internal model knowledge. If external context is useful, place it in a separately labeled section with a real citation or omit it.

Synthesize rather than reproducing long passages. Preserve exact wording only when necessary for a definition, constraint, or short quotation.

### 6. Write the OKF bundle

Use the structure and frontmatter in `references/foundation-profile.md`. Use `assets/bundle-template/` as a structural starting point, not as content to copy blindly.

At minimum:

- create or update `index.md`;
- create concept Markdown files with YAML frontmatter;
- add standard Markdown links between related concepts;
- add `# Citations` entries;
- append a dated entry to `log.md`;
- preserve unknown frontmatter fields in existing concepts.

Never overwrite an existing concept silently. Read it first, preserve still-valid knowledge and metadata, describe the change, and log the update. If the new source conflicts with existing knowledge, show the conflict instead of choosing a winner without evidence.

### 7. Validate

Run the dependency-free validator when Python is available:

```bash
python scripts/validate_okf_bundle.py <bundle-path> --profile foundation
```

If Python is unavailable, perform the same checks manually:

- every non-reserved Markdown concept has frontmatter;
- every concept has a non-empty `type`;
- Foundation Profile metadata is present;
- timestamps are ISO 8601;
- internal links resolve or are disclosed as warnings;
- source-supported claims and interpretation remain separated;
- citations exist and were not invented;
- `index.md` and `log.md` reflect the current bundle.

Do not claim that structural validation proves factual correctness.

### 8. Report the result

Return:

- selected lens;
- bundle path;
- concepts created or updated;
- source limitations;
- validator result: PASS, WARNING, or ERROR;
- any conflicts or questions requiring human review.

## Direct-Mode Requests

Honor direct mode only when the user clearly supplies the lens or says to use Source Fidelity and write immediately. Direct mode removes the selection pause; it does not remove provenance, epistemic separation, validation, or write safety.

## Behavioral Guardrails

- Do not invent an inaccessible source.
- Do not present interpretation as source fact.
- Do not create citations that were not inspected or supplied.
- Do not equate OKF conformance with truth, freshness, authority, or completeness.
- Do not force a taxonomy when the source supports a generic concept.
- Do not turn every source into a knowledge graph; Markdown links are sufficient.
- Do not require platform-specific SDKs, databases, or cloud services.
- Do not silently overwrite, delete, or merge human knowledge.
- Do not describe AI-generated drafts as human-reviewed.
- Do not claim compatibility beyond the checks actually run.

## Portability

This file is the canonical behavioral prompt. Platforms with formal skill support may install the folder as a skill. Other file-capable AI platforms may be instructed:

```text
Read okf-format-foundation/SKILL.md completely and follow it for this task.
```

The core workflow must remain usable without `agents/openai.yaml`, external SDKs, network access, or the validator script.
