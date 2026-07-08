# Flint/Arb Agent Brief

You must write a competitive solver script for the problem paper using only Python standard library and python-flint.

Allowed imports:
- `json`, `time`, `math`, `fractions`, `pathlib`, `sys`
- `flint`

Disallowed:
- Cella modules
- SymPy
- mpmath
- reading `answer_key.json`
- reading other engines' submissions or reports

Basic Python filler is allowed in every case. Filler means standard-library parsing, orchestration, timing, formatting, small arithmetic glue, or a hand-coded replacement for a missing python-flint primitive. Native means work done by python-flint, FLINT, Arb, or Acb APIs.

Your script must emit a JSON report with `engine`, `cases`, and one record per `case_id`. Each case record must include `case_id`, `status`, `answer`, `elapsed_ms`, `native_ms`, `filler_ms`, `native_steps`, `filler_steps`, and `method`. Add `working_precision` when relevant.

Design the solution to be as competitive as possible on both accuracy and runtime. Use exact FLINT rational/polynomial/matrix facilities where appropriate and Arb/Acb ball arithmetic where a high-precision enclosure is the native route.
