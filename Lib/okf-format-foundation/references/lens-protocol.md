# Extraction Lens Protocol

## Principle

A lens is a disclosed attention policy. It determines which source-supported relationships are foregrounded; it does not grant permission to alter or supplement the source.

## Lens Set

Propose exactly three lenses unless the user already selected one.

### Lens 1 — Source Fidelity

Always include this lens.

Foreground:

- definitions;
- claims and evidence;
- specifications and constraints;
- stated relationships;
- uncertainty and citations.

Keep interpretation low. Its common blind spot is that it may preserve facts without making their practical or strategic significance vivid.

### Lens 2 — Context-Selected Practical Lens

Select the most useful practical capability for the source, such as:

- technical implementation;
- operating procedure;
- governance and accountability;
- research method;
- legal or compliance questions;
- teaching and learning;
- stakeholder communication.

### Lens 3 — Context-Selected Interpretive Lens

Select a genuinely different perspective, such as:

- strategic implications;
- critical analysis;
- systems relationships;
- innovation opportunities;
- risks and assumptions;
- decision architecture;
- historical change.

Do not default to “strategic” when the source makes another lens more useful.

## Lens Card Format

Use this compact structure:

```markdown
### Lens 1 — <name>

- Foregrounds: ...
- Leaves secondary: ...
- Likely concepts: ...
- Interpretation level: Low | Medium | High
- Main blind spot: ...
```

After all three cards, write:

```text
Choose 1, 2, or 3; combine named lenses; or ask for three different lenses.
Proposed bundle path: knowledge/<source-slug>/
I will not write files until you confirm the lens and path.
```

## Quality Checks

The lens set is acceptable only when:

- all three could produce materially different concept bodies;
- Lens 1 provides a low-interpretation anchor;
- the practical and interpretive lenses fit the actual source;
- each blind spot is candid and specific;
- none of the labels presupposes a desired conclusion.

## Combining Lenses

When the user combines lenses, do not blend their claims invisibly. Preserve sections or frontmatter that identify the role of each lens.

Example:

```yaml
extraction_lens: "Source Fidelity + Strategic Adoption"
```

Use the lower-confidence rating when the interpretive lens introduces material uncertainty.

## Example — Article Introducing a Data Format

Possible lenses:

1. **Specification and Source Fidelity** — structure, required fields, conformance, non-goals.
2. **Knowledge Operations** — producer/consumer workflow, lifecycle, version control, maintenance.
3. **Strategic Adoption** — organizational value, constraints, readiness, and overclaiming risks.

The third lens may be insightful, but it must label claims that go beyond the specification as interpretation.
