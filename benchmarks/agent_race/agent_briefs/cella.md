# Cella Agent Brief

You must write a competitive solver script for the problem paper using only Python standard library and the local Cella package.

Allowed imports:
- `json`, `time`, `math`, `fractions`, `decimal`, `pathlib`, `sys`
- modules under `cella`

Disallowed:
- SymPy as a direct solver except where a Cella API internally uses it
- mpmath as a direct solver except where a Cella API internally uses it
- python-flint as a direct solver except where a Cella API internally uses it
- reading `answer_key.json`
- reading other engines' submissions or reports

Basic Python filler is allowed in every case. Filler means standard-library parsing, orchestration, timing, formatting, small arithmetic glue, or a hand-coded replacement for a missing Cella primitive. Native means work done by Cella APIs.

Your script must emit a JSON report with `engine`, `cases`, and one record per `case_id`. Each case record must include `case_id`, `status`, `answer`, `elapsed_ms`, `native_ms`, `filler_ms`, `native_steps`, `filler_steps`, and `method`. Add `working_precision` when relevant.

Design the solution to be as competitive as possible on both accuracy and runtime. You are expected to use Cella Pathfinder and related Cella tools to identify cleaner routes, exact symbolic carriers, local geometry shortcuts, arithmetic rewrites, and exact rational paths before doing brute-force computation.

High filler use is not a benchmark failure. It is a primitive-gap measurement for the Cella build queue: record the gap plainly in `filler_steps` rather than hiding it behind a clever answer string.
