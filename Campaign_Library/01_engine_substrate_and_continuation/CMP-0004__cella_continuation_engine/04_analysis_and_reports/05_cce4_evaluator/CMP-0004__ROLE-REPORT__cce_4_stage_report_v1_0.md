# CCE-4 stage report v1.0

**Verdict:** COMPLETE for `primary` and `dual_cpv` at every exact integer
precision `target_bits >= 16`. The historical 192/256/384 set is retained as
the recertification matrix, not as a scope ceiling.

The stage was executed at base commit `50683b971399236abe413cafcf2c56c5b1b9228c` inside the pre-existing dirty worktree. Production adds `cce4.py` and public exports; the legacy native evaluator and schema 1.1 were not edited. The finite `KernelSpec` grammar contains exactly `INPUT_AFFINE`, `ADD`, `SCALE_Q`, `MUL`, `SQRT`, and `DIV`, and only two immutable programs. It is an envelope around the exact certified recurrence evaluator, not an arbitrary DAG parser.

Each certificate binds its canonical spec, normalization, nested CCE-2 route digests, nested CCE-3 selected-class certificate, PF-0/live Pathfinder identity, exact panel/disk schedule, analytic/tail and fixed-DAG accounts, dual polar reduction, exact dyadic bracket, achieved width, and replay digest. The primary normalization preserves the `-2*pi` enclosure distinction. The dual certificate records `runtime_cpv=false` and polar-kernel CPV exactly zero.

`engine/tests/gate_continuation_cce4.py` passed 73 assertions, including a
non-matrix 64-bit certification and replay. The arbitrary-program expansion
was investigated but is not admitted: the six coefficient recurrences exist,
while generic compositional complex-disk branch/denominator witnesses and a
program-derived Cauchy tail theorem do not yet exist. Relaxing the sealed-spec
comparison alone would execute the wrong fixed legacy kernel.

The clean full release took 223.82 seconds and 26,232 KiB peak RSS. Primary/192 was 10.045268 seconds cold; its warmed envelope replay was 0.050778 seconds and is explicitly not a cold evaluator speedup.

Changed stage files are `engine/src/cella/continuation/cce4.py`, `engine/src/cella/continuation/__init__.py`, `engine/tests/gate_continuation_cce4.py`, the standalone verifier, schema, bundle, refusal matrix, dependency report, benchmark, gap ledger, and this report. CCE-5 through CCE-8 were then audited in dependency order. The separate evaluator-campaign `pathfinder_m1_scout.py` was not used because this stage binds the primary `engine/src/cella/pathfinder/` implementation.
