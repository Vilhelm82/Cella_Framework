"""Gate the agent-authored benchmark race protocol.

Run:  PYTHONPATH=src python tests/gate_agent_race_protocol.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BENCH = ROOT / "benchmarks" / "agent_race"

FAILS: list[str] = []


def check(name: str, ok: bool) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


paper_path = BENCH / "problem_paper.md"
answer_key_path = BENCH / "answer_key.json"
judge_path = BENCH / "judge.py"
brief_paths = {
    "sympy": BENCH / "agent_briefs" / "sympy.md",
    "mpmath": BENCH / "agent_briefs" / "mpmath.md",
    "flint_arb": BENCH / "agent_briefs" / "flint_arb.md",
    "cella": BENCH / "agent_briefs" / "cella.md",
}

check(
    "AR1 protocol artifact paths exist",
    paper_path.exists()
    and answer_key_path.exists()
    and judge_path.exists()
    and all(path.exists() for path in brief_paths.values())
    and (BENCH / "submissions").is_dir()
    and (BENCH / "reports").is_dir(),
)

answer_key = {}
if answer_key_path.exists():
    try:
        answer_key = json.loads(answer_key_path.read_text(encoding="utf-8"))
    except Exception:
        answer_key = {}

check(
    "AR2 answer key is only case id to answer string",
    bool(answer_key)
    and all(isinstance(k, str) and k.startswith("P") for k in answer_key)
    and all(isinstance(v, str) for v in answer_key.values())
    and all(not isinstance(v, dict) for v in answer_key.values()),
)

paper_text = paper_path.read_text(encoding="utf-8") if paper_path.exists() else ""
check(
    "AR3 paper is neutral and contains all answer-key case ids",
    bool(answer_key)
    and all(case_id in paper_text for case_id in answer_key)
    and "Cella" not in paper_text
    and "Pathfinder" not in paper_text
    and "SymPy" not in paper_text
    and "mpmath" not in paper_text
    and "Arb" not in paper_text,
)

brief_text = "\n".join(path.read_text(encoding="utf-8") for path in brief_paths.values() if path.exists())
check(
    "AR4 engine briefs constrain tools and require competitive solver reports",
    all(name in brief_text for name in ("SymPy", "mpmath", "python-flint", "Cella"))
    and "case_id" in brief_text
    and "elapsed_ms" in brief_text
    and "native_ms" in brief_text
    and "filler_ms" in brief_text
    and "filler" in brief_text
    and "answer" in brief_text
    and "status" in brief_text,
)

if judge_path.exists() and answer_key:
    with tempfile.TemporaryDirectory() as tmp:
        report_path = Path(tmp) / "sample-report.json"
        judged_path = Path(tmp) / "judged.json"
        report_path.write_text(
            json.dumps(
                {
                    "engine": "sample",
                    "cases": [
                        {
                            "case_id": "P001",
                            "status": "pass",
                            "answer": answer_key.get("P001", ""),
                            "elapsed_ms": 1.0,
                            "native_ms": 0.75,
                            "filler_ms": 0.25,
                            "native_steps": ["sample native operation"],
                            "filler_steps": ["sample Python formatting"],
                        },
                        {
                            "case_id": "P002",
                            "status": "pass",
                            "answer": "wrong",
                            "elapsed_ms": 1.0,
                            "native_ms": 0.2,
                            "filler_ms": 0.8,
                            "native_steps": ["sample native operation"],
                            "filler_steps": ["sample Python fallback"],
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [sys.executable, str(judge_path), "--report", str(report_path), "--output", str(judged_path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        judged = json.loads(judged_path.read_text(encoding="utf-8")) if judged_path.exists() else {}
else:
    completed = None
    judged = {}

check(
    "AR5 judge compares reports to the minimal answer key",
    completed is not None
    and completed.returncode == 0
    and judged.get("summary", {}).get("correct") == 1
    and judged.get("summary", {}).get("incorrect") == 1,
)

check(
    "AR6 judge report preserves timing and method fields from solver report",
    bool(judged.get("cases"))
    and "elapsed_ms" in judged["cases"][0]
    and "native_ms" in judged["cases"][0]
    and "filler_ms" in judged["cases"][0]
    and "filler_percent" in judged["cases"][0]
    and "answer" in judged["cases"][0]
    and "expected" not in judged["cases"][0],
)

check(
    "AR7 judge summarizes native versus Python filler timing",
    judged.get("summary", {}).get("native_ms") == 0.95
    and judged.get("summary", {}).get("filler_ms") == 1.05
    and judged.get("summary", {}).get("filler_percent") == 52.5
    and judged.get("summary", {}).get("instrumentation_missing") == 0,
)

print()
if FAILS:
    print(f"GATE AGENT RACE PROTOCOL: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE AGENT RACE PROTOCOL: CLOSED - blind problem paper, minimal key, and judge protocol are ready.")
sys.exit(0)
