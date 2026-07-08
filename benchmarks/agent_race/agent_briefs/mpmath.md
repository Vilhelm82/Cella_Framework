# mpmath Agent Brief

You must write a competitive solver script for the problem paper using only Python standard library and mpmath.

Allowed imports:
- `json`, `time`, `math`, `decimal`, `fractions`, `pathlib`, `sys`
- `mpmath`

Disallowed:
- Cella modules
- SymPy
- python-flint or other interval/ball libraries
- reading `answer_key.json`
- reading other engines' submissions or reports

Basic Python filler is allowed in every case. Filler means standard-library parsing, orchestration, timing, formatting, small arithmetic glue, or a hand-coded replacement for a missing mpmath primitive. Native means work done by mpmath APIs.

Your script must emit a JSON report with `engine`, `cases`, and one record per `case_id`. Each case record must include `case_id`, `status`, `answer`, `elapsed_ms`, `native_ms`, `filler_ms`, `native_steps`, `filler_steps`, and `method`. Add `working_precision` when relevant.

Design the solution to be as competitive as possible on both accuracy and runtime. Use high-precision arithmetic, stable reformulations you derive, numerical linear algebra, contour quadrature, and direct limiting arguments only when you can encode them using the allowed tools.
