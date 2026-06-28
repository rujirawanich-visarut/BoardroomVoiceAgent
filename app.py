import argparse
import sys
from src.ingestion import DocumentIngestionAgent
from src.decision_gravity import DecisionGravityClassifier
from src.evidence_chain import EvidenceExtractor
from src.semantic_backpressure import SemanticBackpressureDetector
from src.boardroom_narrator import BoardroomVoiceAgentSkill
from src.evaluation import Evaluator
from src.llm_interface import LLMInterface
from src.tracing import TraceLogger

def main():
    parser = argparse.ArgumentParser(description="BoardroomVoiceAgent Wave 2")
    parser.add_argument("--input", type=str, default="sample_inputs/ai_agent_adoption_pre_read.md", help="Path to input markdown file")
    parser.add_argument("--output", type=str, default="sample_outputs/decision_grade_audio_briefing.md", help="Path to output markdown file")
    parser.add_argument("--use-llm", action="store_true", help="Enable LLM reasoning")
    parser.add_argument("--llm-provider", type=str, default=None, help="LLM Provider")
    parser.add_argument("--mock-llm", action="store_true", help="Use mock LLM for testing")
    parser.add_argument("--trace", action="store_true", help="Generate run trace log")
    parser.add_argument("--strict", action="store_true", help="Strict mode for validations")
    args = parser.parse_args()

    print(f"Reading input from: {args.input}")
    
    # Setup tracing and LLM
    tracer = TraceLogger() if args.trace else None
    if tracer:
        tracer.update(input_file=args.input, llm_enabled=args.use_llm or args.mock_llm)
        if args.mock_llm:
            tracer.update(llm_mode="Mock")
        elif args.use_llm:
            tracer.update(llm_mode="Provider")

    llm_interface = LLMInterface(use_llm=args.use_llm, mock_llm=args.mock_llm, provider=args.llm_provider)

    try:
        # 1. Ingestion
        ingestion = DocumentIngestionAgent()
        context = ingestion.ingest(args.input)
        
        # 2. Decision Gravity Classification
        gravity_classifier = DecisionGravityClassifier()
        gravity_result = gravity_classifier.classify(context)
        print(f"Decision Gravity: {gravity_result.gravity} (Triggers: {gravity_result.triggers})")
        if tracer:
            tracer.update(decision_gravity=gravity_result.gravity, triggers=gravity_result.triggers)
        
        # 3. Evidence Extraction
        extractor = EvidenceExtractor(llm_interface=llm_interface, tracer=tracer)
        evidence = extractor.extract(context)
        
        # 4. Semantic Backpressure
        backpressure_detector = SemanticBackpressureDetector()
        backpressure = backpressure_detector.detect(context, evidence)
        
        if tracer:
            tracer.update(backpressure_status=backpressure.triggered, rule_triggered=backpressure.rule_triggered)

        if backpressure.triggered:
            print("\n[!] SEMANTIC BACKPRESSURE TRIGGERED")
            print(f"Severity: {backpressure.severity}, Rule: {backpressure.rule_triggered}")
            for r in backpressure.reasons:
                print(f"Reason: {r}")
                
        # 5. Boardroom Narration
        narrator = BoardroomVoiceAgentSkill()
        brief = narrator.generate_brief(evidence, backpressure, gravity_result.gravity)
        
        # 6. Evaluation
        print("\n--- Running Evaluation ---")
        evaluator = Evaluator()
        passed = evaluator.evaluate(
            brief,
            context.raw_text,
            args.trace,
            args.mock_llm or args.use_llm,
            gravity_result.gravity,
        )
        if tracer:
            tracer.update(
                evaluation_result="PASSED" if passed else "FAILED",
                quality_gate_outcomes=evidence.gate_outcomes,
                gate_protocol_outcome=evaluator.protocol_outcome,
                composition_route=evaluator.composition_route,
                decision_boundary=evaluator.decision_boundary,
                pipeline_outcome=evaluator.pipeline_outcome,
            )
            trace_paths = tracer.write_trace()
        
        # Generate output markdown
        output_title = (
            "Boardroom Voice Agent — Semantic Backpressure Brief"
            if backpressure.triggered
            else "Boardroom Voice Agent — Decision-Grade Pre-read Brief"
        )
        output_md = f"""# {output_title}

## Prior Update
{brief.prior_update}

## Evidence → Insight → Conclusion → Choice
**Evidence:** {brief.evidence_chain.evidence}
**Insight:** {brief.evidence_chain.insight}
**Conclusion:** {brief.evidence_chain.conclusion}
**Choice:** {brief.evidence_chain.choice}

## TTS Script
{brief.tts_script}

## Clean-Read Version
{brief.clean_read}

## Meeting Room Question
{brief.meeting_room_question}

## One-Line Decision Cue
{brief.one_line_decision_cue}

## Rhythm Rationale
{brief.rhythm_rationale}
"""
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_md)
            
        print(f"\nBrief successfully generated at: {args.output}")
        if tracer:
            print(f"Run trace generated at: {tracer.output_path}")
            print(f"Per-run trace generated at: {trace_paths['artifact_json']}")
        if args.strict and not passed:
            sys.exit(1)
        
    except Exception as e:
        print(f"Error executing pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
