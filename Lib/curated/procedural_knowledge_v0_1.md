# BoardroomVoiceAgent Procedural Knowledge v0.1

> Status: REVIEWED EXPERIMENTAL  
> Runtime integration: NONE  
> Purpose: Provide reusable reasoning guidance without supplying case facts or making the executive decision.

## 1. Knowledge Boundary

This artifact is a reasoning aid, not an authority source.

It may help the agent:

- distinguish an informational update from a decision or commitment request;
- identify the evidence categories normally needed to frame a decision;
- preserve source-stated options and expose material trade-offs;
- ask sharper accountability, governance, and safety questions;
- distinguish normal uncertainty from a decision-integrity blocker;
- render decision logic as calm, speakable executive narration.

It must not:

- add facts, options, risks, thresholds, owners, or legal duties absent from the source;
- convert a pattern resemblance into a factual conclusion;
- select or recommend the final strategic pathway;
- treat every uncertainty as Semantic Backpressure;
- override `AGENTS.md`, the Human Accountability Lock, or deterministic fallback;
- be described as active runtime behavior until integration and evaluation evidence exist.

Source material remains the evidence layer. This pack only supplies procedural structure.

## 2. Three Knowledge Types

### 2.1 Procedural knowledge — how to reason

Procedural knowledge governs the sequence of interpretation:

1. Detect intent before extracting a decision.
2. Separate source evidence from interpretation.
3. Identify whether a real decision or commitment is requested.
4. Preserve every material source-stated option.
5. Identify the old business belief, not a risk phrase, as the prior assumption.
6. Distinguish ordinary uncertainty from missing evidence that blocks the requested commitment.
7. Frame the trade-off without choosing for the accountable forum.
8. Convert the result into one-idea-per-line spoken narration.

### 2.2 Pattern knowledge — what decision structures recur

Pattern knowledge describes recurring decision structures such as capital phasing, margin versus volume, supply resilience, or AI governance. A pattern is a hypothesis about structure, not a claim about the current case.

Pattern use is permitted only when source anchors support the match. When no pattern is well supported, the agent must remain generic rather than force a match.

### 2.3 Case knowledge — what is true here

Case knowledge comes only from the current pre-read or an explicitly supplied authoritative source. Pattern libraries and research notes are never case evidence.

The agent must be able to answer:

```text
Which source phrase supports this case-specific statement?
```

If no source phrase supports it, the statement must be removed, marked as a question, or treated as unsupported extraction.

## 3. Intent and Outcome Routing

Intent classification precedes pattern matching.

### PASS

Use PASS when:

- the material is informational and asks for no decision or commitment; or
- a real decision is requested and the source supports a coherent decision frame.

PASS does not mean the source is perfect. It means the requested output can be composed faithfully without inventing critical content.

### REPAIR

Use REPAIR only when deterministic composition can fix presentation defects without changing meaning, for example:

- a risk phrase occupies the prior-assumption field but the source contains a valid old business belief;
- source-stated options were dropped or collapsed;
- a meeting question mechanically joins missing-evidence labels;
- narration contains raw field concatenation or overlong lines.

REPAIR must not fabricate evidence, commission external analysis, resolve a legal ambiguity, or assign an owner.

### FALLBACK

Use FALLBACK when model, schema, extraction, or composition output is invalid and deterministic recovery is required, for example:

- required structured fields cannot be parsed;
- the extracted roles contradict the source and cannot be repaired from source anchors;
- an unsupported decision structure was imposed on ambiguous material;
- the selected pattern has no defensible source anchors.

FALLBACK is a composition route, not a risk judgment.

### BACKPRESSURE

Use BACKPRESSURE only when both conditions are true:

1. A real decision or commitment is requested now; and
2. critical evidence, accountability, governance, compliance, financial, or safety boundaries needed for that commitment are missing or contradictory.

Normal uncertainty alone is not BACKPRESSURE. A pattern match alone is not BACKPRESSURE. Unsupported extraction should normally route to FALLBACK unless the source independently establishes a genuine decision-integrity boundary.

## 4. Semantic Composition Protocol

### 4.1 Prior Update

The prior assumption must be an old business belief that once guided action.

Good prior roles include:

- a demand, value, cost, operating-model, risk, timing, or capability belief;
- an explicit earlier plan or management thesis;
- a belief implied by the source's contrast between what was expected and what is now observed.

Do not use these as a prior assumption unless the source explicitly states that they were believed previously:

- a risk label;
- a missing-evidence statement;
- an unclear-accountability phrase;
- a governance gap;
- a halt rule;
- the narrator's conclusion.

If no old belief is supported, say that the prior assumption is not explicit. Do not invent one.

### 4.2 Evidence to Choice

Compose in this order:

```text
Evidence: What does the source establish?
Insight: What decision-relevant meaning follows from that evidence?
Conclusion: What can and cannot be supported now?
Choice: What source-grounded decision structure must the accountable forum face?
```

Each step must be traceable to the source or clearly framed as interpretation.

### 4.3 Option Preservation

When the source contains Option A, B, and C—or otherwise names several material paths—the output must preserve the major paths. Do not collapse a tertiary decision into a binary for rhetorical neatness.

The agent may compress wording but must preserve:

- the distinct action in each option;
- the material risk or sacrifice each option carries;
- any source-stated sequencing or reversibility differences.

The agent must not invent a middle path merely to create a compromise. A phased or bounded option is valid only when supplied by the source or directly implied by an explicitly requested evidence-gathering step.

### 4.4 Evidence Sufficiency

Evaluate evidence relative to the requested scope of commitment, not against an imaginary standard of completeness.

Useful evidence categories include:

- strategic fit and decision criteria;
- financial baseline and value range;
- customer, market, or demand evidence;
- operational feasibility and capacity;
- risk, safety, compliance, and data boundaries;
- accountability, approval, monitoring, and halt ownership;
- implementation readiness, dependencies, and reversibility;
- alternatives and consequences of delay.

Not every case requires every category. The question is whether an absent category is critical to the commitment being requested.

### 4.5 Agency and Accountability

Distinguish:

- **Evaluative agency:** the system summarizes, compares, detects, or recommends for human review.
- **Operative agency:** the system executes, authorizes, changes a state, or materially influences an outcome without an effective human checkpoint.

Greater operative agency generally requires clearer authority, monitoring, escalation, and halt boundaries. This is a question framework, not a universal legal rule.

Do not assign accountability from a pattern. Ask who is authorized, who monitors, who can halt, and who owns remediation when the source does not say.

### 4.6 Implicit Recommendation and Automation Bias

A script can make a de facto recommendation even without saying “recommend” when it:

- gives one option vivid benefits and describes alternatives only as losses;
- removes viable source options;
- states one path as inevitable;
- uses a decision cue that instructs executives to approve, authorize, or choose;
- labels one option “safe” without source support.

When only one viable option remains after faithful evidence analysis, state why the other options are unsupported and keep the final choice with the accountable forum.

## 5. Pattern Use Protocol

Pattern matching follows, never precedes, source extraction.

For any proposed pattern match:

1. Record at least two independent source anchors.
2. Check for a stronger competing pattern.
3. Treat the match as low confidence when the source is sparse or ambiguous.
4. Use the pattern to propose questions and evidence categories—not facts.
5. Preserve source language when it conflicts with the pattern vocabulary.
6. Do not activate BACKPRESSURE merely because the pattern is normally high risk.

If no defensible match exists, use a neutral decision frame.

## 6. Spoken Decision Coherence

The spoken artifact should carry one principal idea per line.

Required qualities:

- concise sentences suitable for listening once;
- explicit bridges between evidence, meaning, and decision;
- no raw concatenation of field labels or missing-evidence lists;
- no awkward Thai-English joins created by templates;
- source-stated terms may remain bilingual when they are natural to the audience;
- `[PAUSE 3.0s]` only after a material trade-off, severe contradiction, irreversible implication, safety boundary, governance boundary, or explicit decision question.

The Meeting Room Question should ask what the accountable forum must resolve. It should not be a list of missing fields disguised as a question.

The One-Line Decision Cue should combine the conclusion and trade-off. It must be memorable but non-prescriptive.

## 7. Provenance and Confidence

Every pattern or procedural rule should carry:

- its research provenance;
- its review status;
- jurisdictional scope where relevant;
- a confidence statement;
- prohibited inferences;
- a note when an external authoritative source has not been verified.

Legal, regulatory, accounting, tax, safety, and fiduciary claims require authoritative, jurisdiction-specific verification before production use. The research artifacts in `Lib/` are discovery inputs, not legal or professional advice.

## 8. Emergent Knowledge Lifecycle

Creative candidate knowledge is welcome, but it must move through a visible lifecycle:

```text
CANDIDATE -> REVIEWED -> ACTIVE -> RETIRED
```

- **CANDIDATE:** interesting structure found in research or observed behavior.
- **REVIEWED:** internally coherent, bounded, and suitable for controlled evaluation.
- **ACTIVE:** explicitly integrated into runtime and supported by tests and documentation.
- **RETIRED:** removed from active use but retained for provenance.

No item in this v0.1 pack is ACTIVE.

## 9. Intentionally Excluded Claims

The following are not adopted as procedural truth:

- unverified universal numerical thresholds;
- unverified jurisdiction-specific penalties or duties;
- claims that a named mathematical distance proves executive reasoning quality;
- automatic ERP, market, legal, or operational data retrieval not implemented by the project;
- the claim that a pattern library is exhaustive;
- any cue that tells the board which option to approve;
- any claim that these artifacts constitute a confidential or blind holdout set.

## 10. Activation Checklist

Before any part of this pack is wired into runtime:

```text
[ ] Source-grounding behavior is tested.
[ ] Informational material still routes PASS/CLEAR.
[ ] Unsupported extraction routes FALLBACK, not automatic BACKPRESSURE.
[ ] Backpressure still requires a real decision plus a critical missing boundary.
[ ] Source-stated options are preserved.
[ ] No pattern injects case facts or final recommendations.
[ ] Mixed-language narration remains natural and speakable.
[ ] Existing deterministic fallback still passes.
[ ] Documentation names the integration honestly.
```
