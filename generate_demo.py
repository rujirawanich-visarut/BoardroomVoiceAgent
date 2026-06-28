import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 0. Project Overview\n",
    "\n",
    "BoardroomVoiceAgent converts messy executive pre-reads into decision-grade spoken briefings.\n",
    "It demonstrates Semantic Backpressure, Human Accountability Lock, structured validation, and Boardroom Voice Agent skills."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Prepare Custom Executive Pre-read\n",
    "\n",
    "This is not a canned sample. Here we define a complex, real-world Thai executive pre-read involving AI Agent adoption, productivity claims, and missing governance controls. We save it to `sample_inputs/custom_pre_read.md`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from pathlib import Path\n",
    "import os\n",
    "\n",
    "os.makedirs('sample_inputs', exist_ok=True)\n",
    "os.makedirs('sample_outputs', exist_ok=True)\n",
    "os.makedirs('logs', exist_ok=True)\n",
    "\n",
    "custom_input_text = \"\"\"คือเรื่องนี้ผมก็ไม่แน่ใจว่าจะต้องตัดสินใจยังไงนะครับ แต่ตอนนี้ทีมอยากให้ scale AI Agent ไปใช้ใน operation หลายทีมเร็ว ๆ เพราะ pilot ที่ลองกับ shift report กับ maintenance troubleshooting เหมือนจะช่วยลดเวลางาน manual ได้จริง บางคนบอกว่าประหยัดเวลาได้เยอะมากแต่ก็ยังไม่มี baseline ชัด ๆ ว่าก่อนหน้านี้ใช้เวลากี่ชั่วโมง แล้วหลังใช้ agent ลดไปเท่าไหร่แน่ ๆ แล้วฝั่ง operations ก็อยากได้เร็วเพราะคนหน้างานบ่นว่าหา SOP กับ incident เก่า ๆ ยากมาก แต่ฝั่ง risk กับ compliance ยังเหมือนจะไม่สบายใจเพราะยังไม่รู้ว่าเวลาที่ agent ให้คำแนะนำผิดใครเป็นคนรับผิดชอบ บาง use case แค่ search knowledge ก็น่าจะปลอดภัย แต่บาง use case เหมือน agent เริ่ม suggest action หรือ recommend next step แล้ว ซึ่งผมก็ไม่แน่ใจว่าตรงนี้ถือเป็น decision support หรือเริ่มเป็น autonomy แล้วหรือยัง อีกอย่าง data access ก็ยังไม่เคลียร์ บางทีมอยากให้ agent อ่าน maintenance log, production data, SOP, RCA, email summary รวม ๆ กัน แต่ยังไม่มีใครบอกชัดว่า data ไหน confidential data ไหนใช้ได้ data ไหนต้องขอ approval ก่อน แล้ว Digital team ก็บอกว่า platform พร้อมระดับหนึ่งแต่ยังไม่ได้มี governance framework เต็ม ส่วน HR ก็บอกว่าถ้าจะให้คน adopt จริงต้อง train พร้อม use case ไม่งั้นเรียนแล้วก็ไม่ได้ใช้ แต่ถ้ารอ governance ครบหมดก็อาจช้าเกินไปเพราะ business อยากเห็น productivity impact ปีนี้แล้ว CFO ก็ถามว่าจะวัด benefit ยังไงเพราะตอนนี้มีแต่คำว่า productivity improvement แต่ยังไม่มีตัวเลขที่ audit ได้ บางคนเสนอให้ scale ไปก่อนเฉพาะ low-risk use case เช่น knowledge retrieval กับ summary แต่บางคนก็บอกว่าถ้าทำแค่นั้น value อาจไม่พอ justify budget ส่วนทีม plant หนึ่งบอกว่าอยากลอง agent ที่ช่วย troubleshoot abnormal condition แต่ผมกลัวว่าถ้า context ไม่ครบแล้ว agent ตอบมั่นใจเกินไปจะเสี่ยงมาก ยังไม่มี halt rule ชัด ๆ ว่าเมื่อไหร่ agent ต้องหยุดและถาม engineer หรือ supervisor แล้วเรื่อง approval gate ก็ยังงง ๆ ว่าใคร approve agent ใหม่ ใคร monitor output ใคร update knowledge base ถ้า SOP เปลี่ยน แล้วถ้า agent ใช้ข้อมูลเก่าใครรับผิดชอบ สรุปคือผมรู้สึกว่ามันมี value จริง แต่ก็มี governance gap เยอะ แล้วตอนประชุม MC รอบหน้าเหมือนต้องขอ direction ว่าจะไปต่อยังไง จะอนุมัติ scale เลยไหม จะให้ทำ targeted pilot ก่อน หรือจะให้หยุดรอ governance แต่ถ้าหยุดหมดก็อาจเสีย momentum และคนก็จะกลับไปทำ manual เหมือนเดิม ผมอยากให้ช่วยสรุปให้ผู้บริหารฟังแบบไม่ต้องยาวมาก แต่ต้องเห็น trade-off ว่าจะเอา speed หรือ control หรือมีทางกลางที่ไม่หลอกตัวเองเกินไป และถ้าข้อมูลยังไม่พอก็ควรบอกด้วยว่าอะไรที่ยังขาดก่อนตัดสินใจจริง\"\"\"\n",
    "\n",
    "Path('sample_inputs/custom_pre_read.md').write_text(custom_input_text, encoding='utf-8')\n",
    "print(\"Custom pre-read saved to sample_inputs/custom_pre_read.md\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Run BoardroomVoiceAgent\n",
    "\n",
    "Run the primary offline pipeline command. This will classify decision gravity, extract the evidence chain, pass through minimal boardroom quality gates, and generate the final TTS-ready briefing."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import subprocess\n",
    "\n",
    "cmd = [\n",
    "    \"python\", \"app.py\", \n",
    "    \"--input\", \"sample_inputs/custom_pre_read.md\", \n",
    "    \"--output\", \"sample_outputs/final_submission_custom_mock_llm.md\", \n",
    "    \"--mock-llm\", \"--trace\", \"--strict\"\n",
    "]\n",
    "\n",
    "result = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, \"PYTHONIOENCODING\": \"utf-8\"})\n",
    "\n",
    "# Clean up output for presentation\n",
    "output = result.stdout.replace('\\n[!]', '[!]')\n",
    "\n",
    "print(output)\n",
    "if result.stderr:\n",
    "    print(\"Errors:\", result.stderr)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. View Generated Briefing and Trace\n",
    "\n",
    "Display the final generated decision-grade briefing and the key reviewer fields from the trace log."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "from IPython.display import Markdown, display\n",
    "\n",
    "# Display generated briefing\n",
    "display(Markdown(\"### Generated Briefing\"))\n",
    "display(Markdown(Path(\"sample_outputs/final_submission_custom_mock_llm.md\").read_text(encoding=\"utf-8\")))\n",
    "\n",
    "# Display trace summary\n",
    "trace_file = Path('logs/run_trace_latest.json')\n",
    "if trace_file.exists():\n",
    "    trace = json.loads(trace_file.read_text(encoding='utf-8'))\n",
    "    trace_summary = {\n",
    "        'decision_gravity': trace.get('decision_gravity'),\n",
    "        'composition_route': trace.get('composition_route'),\n",
    "        'decision_boundary': trace.get('decision_boundary'),\n",
    "        'pipeline_outcome': trace.get('pipeline_outcome'),\n",
    "        'semantic_backpressure': trace.get('semantic_backpressure', {}).get('triggered', False),\n",
    "        'quality_gate_outcomes': trace.get('gate_outcomes', {}),\n",
    "        'evaluation_result': trace.get('evaluation_result')\n",
    "    }\n",
    "    print(\"\\n--- Trace Summary ---\")\n",
    "    print(json.dumps(trace_summary, indent=2))\n",
    "else:\n",
    "    # Fallback to markdown trace\n",
    "    md_trace = Path('logs/run_trace_latest.md')\n",
    "    if md_trace.exists():\n",
    "        print(\"\\n--- Trace Summary ---\")\n",
    "        print(md_trace.read_text(encoding='utf-8'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Appendix: Additional Context & Tests\n",
    "\n",
    "The cells below are optional and show deterministic fallback mode, security evaluation corpus, source-faithfulness, and the full test suite."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Run full test suite including security evaluations\n",
    "result_tests = subprocess.run([\"python\", \"test_runner.py\"], capture_output=True, text=True)\n",
    "print(result_tests.stdout)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open("demo.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print("demo.ipynb regenerated successfully using json.")
