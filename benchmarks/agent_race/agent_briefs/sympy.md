# SymPy Agent Brief

You must write a competitive solver script for the problem paper using only Python standard library and SymPy.

Allowed imports:
- `json`, `time`, `math`, `decimal`, `fractions`, `pathlib`, `sys`
- `sympy`

Disallowed:
- Cella modules
- mpmath directly
- python-flint or other interval/ball libraries
- reading `answer_key.json`
- reading other engines' submissions or reports

Basic Python filler is allowed in every case. Filler means standard-library parsing, orchestration, timing, formatting, small arithmetic glue, or a hand-coded replacement for a missing SymPy primitive. Native means work done by SymPy APIs.

Your script must emit a JSON report with `engine`, `cases`, and one record per `case_id`. Each case record must include `case_id`, `status`, `answer`, `elapsed_ms`, `native_ms`, `filler_ms`, `native_steps`, `filler_steps`, and `method`. Add `working_precision` when relevant.

Design the solution to be as competitive as possible on both accuracy and runtime. Use exact symbolic operations, rational arithmetic, simplification, limits, matrix operations, or residue/complex tools where they are the native SymPy route.
