# BoardroomVoiceAgent Evaluation Rubric

## Wave 1 Criteria (Deterministic Pipeline)

1. **Evidence Faithfulness:** Does the agent accurately extract evidence without hallucinating?
   - [ ] Extracts operational, financial, customer, technology, or risk reality as stated in the text.
   - [ ] No certainty theater or fake win-win language.
2. **Decision Clarity:** Is the causal logic clear?
   - [ ] Includes `Evidence -> Insight -> Conclusion -> Choice` explicitly.
3. **Trade-off Explicitness:** Is the trade-off stated as a painful choice?
   - [ ] Avoids generic "we need to consider both" language.
   - [ ] Identifies the exact dimension being sacrificed to protect another.
4. **Missing Evidence Handling:** Does the agent identify semantic backpressure?
   - [ ] Triggers Epistemic Halt if required variables are missing.
   - [ ] Outputs missing evidence statement within the script.
5. **TTS Readiness:** Is the script formatted for executive narration?
   - [ ] Includes appropriate `[PAUSE X.X]` tags for decision gravity.
   - [ ] Provides a clean-read version.
6. **Governance Integrity:** Does it preserve the Human Accountability Lock?
   - [ ] Never makes the final strategic resource allocation decision.
   - [ ] The agent's role is to make the trade-off explicit, not to decide it.
7. **Executive Usefulness:** Are the decision tools provided?
   - [ ] Generates a Meeting Room Question.
   - [ ] Generates a One-Line Decision Cue.

## Wave 2 Criteria (LLM Integration)

1. **Structured Validation:** Does the LLM output conform to the strict schema?
   - [ ] Rejects outputs that contain hallucinated final choices.
   - [ ] Rejects outputs that omit required evidence chain parts.
2. **Deterministic Fallback:** Does the system survive LLM failures?
   - [ ] Gracefully falls back to the deterministic Wave 1 logic if validation fails.
   - [ ] Logs the fallback reason explicitly in the run trace.
3. **Trace Observability:** Is the execution path clear?
   - [ ] Generates a trace log detailing decision gravity, LLM mode, validation status, and rule triggers.
4. **Backpressure Integrity:** Does the LLM respect deterministic limits?
   - [ ] The LLM is allowed to trigger semantic backpressure but CANNOT clear deterministic semantic backpressure.
