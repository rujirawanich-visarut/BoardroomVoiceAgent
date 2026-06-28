"""Execute demo.ipynb with the standard library and persist cell outputs.

The demo uses plain Python cells only, so capstone verification does not depend
on Jupyter tooling being installed in the local audit runtime.
"""

import contextlib
import io
import json
import traceback
from pathlib import Path


NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "demo.ipynb"


def main() -> None:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    namespace = {"__name__": "__main__"}
    execution_count = 0

    for cell_index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        execution_count += 1
        source = "".join(cell.get("source", []))
        stdout = io.StringIO()
        stderr = io.StringIO()
        cell["execution_count"] = execution_count
        cell["outputs"] = []
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(compile(source, f"demo.ipynb:cell-{cell_index}", "exec"), namespace)
        except Exception as exc:
            cell["outputs"].append(
                {
                    "output_type": "error",
                    "ename": type(exc).__name__,
                    "evalue": str(exc),
                    "traceback": traceback.format_exc().splitlines(),
                }
            )
            NOTEBOOK_PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
            raise

        if stdout.getvalue():
            cell["outputs"].append(
                {"output_type": "stream", "name": "stdout", "text": stdout.getvalue().splitlines(True)}
            )
        if stderr.getvalue():
            cell["outputs"].append(
                {"output_type": "stream", "name": "stderr", "text": stderr.getvalue().splitlines(True)}
            )

    NOTEBOOK_PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Executed {execution_count} code cells: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
