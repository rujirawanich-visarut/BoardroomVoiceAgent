# Provenance and Write-Safety Rules

## Source Inventory

Record what the agent actually inspected. Distinguish:

- complete source;
- partial source;
- source referenced but unavailable;
- human recollection or conversation;
- external context introduced after extraction.

Do not upgrade a secondary summary to a primary source.

## Claim Boundaries

Place statements in the correct epistemic category:

### Source-supported

The supplied source directly supports the statement. Paraphrase faithfully and cite the source.

### Interpretation

The statement follows from a selected lens but is not explicitly stated. Label it as interpretation and explain the basis.

### Open question

The source does not support a conclusion or contains a conflict. Preserve the uncertainty.

### External context

The agent introduces separately inspected material. Label it and cite it independently. Never imply it came from the original source.

## Confidence

Confidence refers to support for the extracted concept, not the model's general confidence.

- `high`: directly supported, source access complete, and little interpretation required.
- `medium`: supported but includes synthesis, ambiguity, or incomplete context.
- `low`: partial access, weak attribution, material conflict, or interpretation dominates.

## Existing Knowledge

Before editing an existing concept:

1. Read the full file.
2. Preserve unknown metadata.
3. Compare the new source with existing claims.
4. Keep both claims visible when they conflict.
5. Update timestamp and status honestly.
6. Record the change in `log.md`.

Never silently delete human annotations or replace a reviewed concept with an AI draft.

## Citations

- Cite inspected sources only.
- Use stable repository-relative links when the source is stored in the bundle.
- Use direct external URLs when appropriate.
- Do not cite a search-results page as the authority.
- Do not fabricate author, date, title, page number, or URL.
- If citation metadata is incomplete, say so.

## Copyright and Sensitive Material

Synthesize rather than reproducing long copyrighted passages. Preserve only short quotations needed for definitions or exact constraints.

Do not copy secrets, personal data, credentials, confidential operational details, or restricted source material into a portable bundle without explicit authorization. Portability increases the consequence of accidental disclosure.

## Human Checkpoints

Human lens confirmation authorizes a perspective, not factual approval. Keep `knowledge_status: draft` until a human or defined review process confirms the content.

If the user requests an authoritative, legal, medical, financial, compliance, or safety concept, require appropriate primary-source or expert review rather than elevating model synthesis to authority.
