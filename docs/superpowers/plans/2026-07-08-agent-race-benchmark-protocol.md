# Agent Race Benchmark Protocol Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a benchmark protocol where agents read a neutral problem paper, produce engine-constrained solver scripts, and are judged only against a minimal case-id answer key while reporting native-vs-Python-filler effort.

**Architecture:** The protocol lives under `benchmarks/agent_race/`. The problem paper is human-readable and engine-neutral; `answer_key.json` contains only `{case_id: answer}`; `judge.py` compares submitted JSON reports to the paper's declared comparison policy without solving cases. Solver reports must split `native_ms` and `filler_ms` so primitive gaps are measured rather than treated as automatic failures.

**Tech Stack:** Python stdlib JSON/Fraction/decimal/complex parsing, Markdown/JSON artifacts, existing Cella repo gate-script style.

---

### Task 1: Protocol Artifacts

**Files:**
- Create: `benchmarks/agent_race/problem_paper.md`
- Create: `benchmarks/agent_race/answer_key.json`
- Create: `benchmarks/agent_race/agent_briefs/sympy.md`
- Create: `benchmarks/agent_race/agent_briefs/mpmath.md`
- Create: `benchmarks/agent_race/agent_briefs/flint_arb.md`
- Create: `benchmarks/agent_race/agent_briefs/cella.md`
- Create: `benchmarks/agent_race/submissions/.gitkeep`
- Create: `benchmarks/agent_race/reports/.gitkeep`

- [ ] **Step 1: Write the failing gate expectations**

Create `tests/gate_agent_race_protocol.py` requiring the paper, minimal answer key, engine briefs, empty submissions/reports folders, and no method/provenance metadata in the answer key.

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python tests/gate_agent_race_protocol.py`
Expected: FAIL because the artifacts do not exist.

- [ ] **Step 3: Write minimal protocol artifacts**

Add a neutral first paper with exact, numeric, algebraic, matrix, branch, local-geometry, and contour-style cases. Keep answers in `answer_key.json` as strings only.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python tests/gate_agent_race_protocol.py`
Expected: PASS for artifact structure and answer-key minimalism.

### Task 2: Judge

**Files:**
- Create: `benchmarks/agent_race/judge.py`
- Modify: `tests/gate_agent_race_protocol.py`

- [ ] **Step 1: Extend the failing gate for judge behavior**

Require `judge.py` to accept a report JSON, compare answers against `answer_key.json`, preserve native/filler timing fields, summarize filler percentage, and write a judged report without solving any problem.

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python tests/gate_agent_race_protocol.py`
Expected: FAIL because `judge.py` does not exist.

- [ ] **Step 3: Implement minimal judge**

Implement exact string/rational/decimal/complex comparison modes keyed by case id from static judge policy. Reject missing answers, wrong answers, malformed reports, and non-string answer-key values.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python tests/gate_agent_race_protocol.py`
Expected: PASS.

### Task 3: Verification

**Files:**
- Test: `tests/gate_agent_race_protocol.py`
- Test: existing package gates

- [ ] **Step 1: Run protocol gate**

Run: `PYTHONPATH=src python tests/gate_agent_race_protocol.py`
Expected: PASS.

- [ ] **Step 2: Compile judge**

Run: `python -m py_compile benchmarks/agent_race/judge.py tests/gate_agent_race_protocol.py`
Expected: exit 0.

- [ ] **Step 3: Run package smoke gates**

Run: `PYTHONPATH=src python tests/gate_mcp.py` and `PYTHONPATH=src python tests/gate_mcp_pathfinder.py`
Expected: PASS.
