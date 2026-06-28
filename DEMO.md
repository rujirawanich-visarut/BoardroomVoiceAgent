# BoardroomVoiceAgent Demo Walkthrough

## 1. Install check

```bash
python -m pip install -r requirements.txt
```

The offline CLI has no third-party runtime dependencies.

## 2. Run the full evaluation

```bash
python test_runner.py
```

Expected result: every integration scenario reports **7/7 Structural Contract Checks** and **3/3 Minimal Boardroom Quality Gates**. The suite also reports **8/8 security scenarios** and **5/5 source-faithfulness scenarios**, in addition to deterministic execution, valid and invalid MockLLM paths, the custom AI-governance pre-read, and unrelated routing probes.

## 3. Run the custom AI-governance briefing

```bash
python app.py --input sample_inputs/custom_pre_read.md --output sample_outputs/final_submission_custom_mock_llm.md --mock-llm --trace --strict
```

Expected indicators:

- Decision Gravity: High
- Semantic Backpressure: triggered for accountability/governance gaps
- Three paths preserved: fast scale, delayed scale, targeted governed pilots
- Quality gates: 3/3
- Pipeline outcome: BACKPRESSURE

## 4. Verify unrelated inputs do not become AI-governance briefs

```bash
python app.py --input sample_inputs/warehouse_productivity_update.md --output sample_outputs/warehouse_productivity_update_briefing.md --mock-llm --trace --strict
python app.py --input sample_inputs/office_lease_decision.md --output sample_outputs/office_lease_decision_briefing.md --mock-llm --trace --strict
```

The warehouse result is informational. The office result frames continuity versus relocation economics. Neither may introduce AI accountability evidence.

## 5. Notebook

Open `demo.ipynb`. The committed notebook contains six executed code cells with no errors. It discovers the project root, uses `sys.executable`, verifies dependencies, runs the full evaluation, generates the custom briefing, reads the latest and per-run trace, and executes reviewer assertions.

Local standard-library execution without Jupyter tooling:

```bash
python scripts/execute_demo_notebook.py
```

For Kaggle, attach the complete repository as notebook input. The notebook locates the attached files and copies them to `/kaggle/working/BoardroomVoiceAgent` before writing outputs.

Reviewer evidence is indexed in `SUBMISSION_EVIDENCE.md`.
