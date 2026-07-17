<!--
STAGE D ledger close block. Written into stage_d/ by the stage-runner; the
merge-packager APPENDS this to the shared results/three_channel_kg/CLAIM_LEDGER.md
(append-only). The stage-runner does NOT edit the shared ledger.
-->

## Stage D close — frame honesty (CL-c7, PARTIAL by design) — 2026-06-23

**Prereg pin:** `ae399cb1d4fe5cd37afc615cdb2c5e4e2e2246e1ee9b6542d3484f73930e118a`
**Records sha256:** `0aceffdd3133713a0985381e347b958c730e012c2e0958e48f045c355a87238d` (12 records; byte-stable over two runs)
**Suite:** exit 0 · **Predictions:** 9/9 PASS · **Defect-chain:** 0

| Claim | Prior status | Stage-D verdict | New status (proposed) |
|---|---|---|---|
| CL-c7 | NOT_YET_PROBED (PARTIAL by design) | provable frame-honesty core graded on the frozen F12 pin (R3): F12a channels MOVE `(−1/49,1/49,−3/49)→(−961/30625,2713/30625,−3627/30625)` while `K_G=σ₂=−3/49` INVARIANT (frame-relativity / R2); F12b signed permutation FIXES channels and `K_G` invariant (`S₃⋉{±}` at n=3); K7 NOT fired; completeness left OPEN | **PARTIAL** (NOT DEMONSTRATED) |
| CL-c3c-ii | NOT_YET_PROBED (OPEN — blocked on `{σ_r}`-completeness / L1) | recorded OPEN; NOT closed by Stage D; K-soft raised as a non-refuting FLAG | **OPEN** (no move) |

**Kills:** K7 (frame-undeclared, refute) — **NOT FIRED** (recharts legitimate/orthogonal, `σ₂` held
invariant under both F12a/F12b). K-soft (completeness) — **non-refuting FLAG** raised
("completeness unestablished"; no in-scope refuting witness manufactured; does not refute, does not
fail a prediction).

**Dispositions encoded:** R2 (channels frame-relative in the supplied DBP frame; only the sum `K_G`
intrinsic) · R3 (F12 pin CLOSED; exact-ℚ tuples from FIXTURES.md used verbatim).

**Scope/fences:** eval-tier only; no substrate promotion; nothing canonical until Will signs off.
PARTIAL by design — the `{σ_r}`-completeness / L1 question (CL-c3c-ii) stays OPEN as a successor.

*Authority: frozen objects under `results/three_channel_kg/` verified vs `freeze_pins_sha256.json`;
bench imported read-only and pinned in `stage_d/prereg.json` `depends_on`. Covenant loop; prereg
frozen pre-emission; clauses embedded verbatim + gated; two-run byte-stability; mutation guards prove
a lying engine is caught.*
