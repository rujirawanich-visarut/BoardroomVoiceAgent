import json
import os
import re
import time
import uuid

class TraceLogger:
    def __init__(self, output_path: str = "logs/run_trace_latest.md"):
        self.output_path = output_path
        self.run_id = f"{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{uuid.uuid4().hex[:8]}"
        self.trace = {
            "run_id": self.run_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "input_file": "",
            "decision_gravity": "",
            "triggers": [],
            "llm_enabled": False,
            "llm_mode": "",
            "llm_invoked": False,
            "llm_parse_passed": False,
            "llm_schema_validation_passed": False,
            "llm_validation_error_type": "",
            "llm_validation_passed": False,
            "fallback_used": False,
            "fallback_reason": "",
            "backpressure_status": False,
            "rule_triggered": "",
            "composition_route": "PASS",
            "decision_boundary": "CLEAR",
            "pipeline_outcome": "PASS",
            "evaluation_result": "Pending"
        }

    def update(self, **kwargs):
        for k, v in kwargs.items():
            self.trace[k] = v

    def _markdown(self):
        md_content = f"# BoardroomVoiceAgent Run Trace\n\n"
        md_content += f"**Run ID:** {self.trace.get('run_id', self.run_id)}\n"
        md_content += f"**Timestamp:** {self.trace['timestamp']}\n"
        md_content += f"**Input File:** {self.trace.get('input_file', '')}\n"
        md_content += f"**Decision Gravity:** {self.trace.get('decision_gravity', '')}\n"
        md_content += f"**Triggers:** {self.trace.get('triggers', [])}\n"
        md_content += f"**LLM Enabled:** {self.trace.get('llm_enabled', False)}\n"
        md_content += f"**LLM Mode:** {self.trace.get('llm_mode', 'N/A')}\n"
        md_content += f"**LLM Invoked:** {self.trace.get('llm_invoked', False)}\n"
        md_content += f"**LLM Parse Passed:** {self.trace.get('llm_parse_passed', False)}\n"
        md_content += f"**LLM Schema Validation Passed:** {self.trace.get('llm_schema_validation_passed', False)}\n"
        md_content += f"**LLM Validation Error Type:** {self.trace.get('llm_validation_error_type', '')}\n"
        md_content += f"**LLM Validation Passed:** {self.trace.get('llm_validation_passed', False)}\n"
        md_content += f"**Fallback Used:** {self.trace.get('fallback_used', False)}\n"
        md_content += f"**Fallback Reason:** {self.trace.get('fallback_reason', '')}\n"
        md_content += f"**Backpressure Status:** {self.trace.get('backpressure_status', False)}\n"
        md_content += f"**Rule Triggered:** {self.trace.get('rule_triggered', '')}\n"
        md_content += f"**Composition Route:** {self.trace.get('composition_route', 'PASS')}\n"
        md_content += f"**Decision Boundary:** {self.trace.get('decision_boundary', 'CLEAR')}\n"
        md_content += f"**Pipeline Outcome:** {self.trace.get('pipeline_outcome', 'PASS')}\n"
        md_content += f"**Quality Gate Outcomes:** {self.trace.get('quality_gate_outcomes', {})}\n"
        md_content += f"**Gate Protocol Outcome:** {self.trace.get('gate_protocol_outcome', 'PASS')}\n"
        md_content += f"**Evaluation Result:** {self.trace.get('evaluation_result', 'N/A')}\n"
        md_content += f"**Per-Run Trace JSON:** {self.trace.get('trace_artifact_json', '')}\n"
        return md_content

    def write_trace(self):
        latest_directory = os.path.dirname(self.output_path) or "."
        os.makedirs(latest_directory, exist_ok=True)

        input_name = os.path.splitext(os.path.basename(self.trace.get("input_file", "run")))[0]
        safe_input_name = re.sub(r"[^a-zA-Z0-9_-]+", "-", input_name).strip("-") or "run"
        runs_directory = os.path.join(latest_directory, "runs")
        os.makedirs(runs_directory, exist_ok=True)
        artifact_base = os.path.join(runs_directory, f"{self.run_id}-{safe_input_name}")
        artifact_md = artifact_base + ".md"
        artifact_json = artifact_base + ".json"
        latest_json = os.path.splitext(self.output_path)[0] + ".json"

        self.trace["trace_artifact_markdown"] = artifact_md.replace("\\", "/")
        self.trace["trace_artifact_json"] = artifact_json.replace("\\", "/")
        markdown = self._markdown()

        for path, content in (
            (artifact_md, markdown),
            (self.output_path, markdown),
        ):
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(content)
        for path in (artifact_json, latest_json):
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(self.trace, handle, indent=2)

        return {
            "latest_markdown": self.output_path,
            "latest_json": latest_json,
            "artifact_markdown": artifact_md,
            "artifact_json": artifact_json,
        }
