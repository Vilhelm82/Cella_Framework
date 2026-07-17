# CCE-2 stage report v1.0

**Verdict:** PROVED (curve-level exact corridor scope)  
**Date:** 2026-07-14  
**Base and current HEAD:** `50683b971399236abe413cafcf2c56c5b1b9228c`  
**Worktree identity:** dirty overlay on the recorded base; unrelated pre-existing
deletions and Paper III work were preserved and excluded from this stage.

## Result

CCE-2 installs two exact seven-segment Q(i) corridor representatives based at
`sigma=1`.  The upper square is counterclockwise with word `a_+` and windings
`(0,1,0)` about `(0,+i,-i)`.  The lower is its complex conjugate, clockwise,
with word `a_-^(-1)` and windings `(0,0,-1)`.  Their explicit vertices are the
ordered pairs in `DBP_EXACT_CORRIDOR_MANIFEST_v1.0.json`.

Every one of the 21 segment/puncture minima for each path is recomputed in
exact rational arithmetic.  A radius-`1/8` base tube has lower distances
`3/8` from zero and the enclosed branch point and `7/8` from the other branch.
The lift certificate uses 29 rational radius-`1/4` charts and 28 strict overlap
witnesses.  Odd deck parity sends the `+sqrt(2)` isolator to the `-sqrt(2)`
isolator without floating-point or nearest-root selection.

The curve divisor reduction supplies route/tube bounds for `rho`, `rho+/-1`,
`m`, `n`, `c`, `x_p`, and `y_p^2`.  The exact return-stem argument works on
`0<h<=1`: the upper has `Im(m)<0` and selects `delta_-^up`; the lower has
`Im(m)>0` and selects `delta_-^down`.  The unresolved compact corrections
remain explicitly in `Z[A]+Z[B]`.

## Authority and orientation resolution

- Stage 3: `research/paper/Theorems/DBP/technical_supplements/DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1.md`, SHA-256 `bdaabb1a1015f7b6b3055321b422a3b6d84053c808d2e3669ea646ff3de82670`.
- Paper III: `research/paper/Theorems/DBP/DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md`, SHA-256 `c5d790829434f848057529ef77ff855e3bc4d9f582e1d766dc2f273b4c76aeb6`.
- CCE-2 gap input: SHA-256 `29a7b7351910ee401b57fbd75112ce613394f90993239f44edc0f0b678f57894`.

Stage 3 specifies the upper half-plane generator and the analogous conjugate
lower construction, but does not spell out a polygon orientation.  CCE-2 uses
the permitted exact-replacement route: the lower is fixed as the conjugate
clockwise word `a_-^(-1)`.  Its orientation is retained in the certificate,
while quotient transport is unchanged up to the explicitly unresolved compact
Picard--Lefschetz correction.  Winding parity alone is never used as corridor
identity evidence.

## Production binding and deterministic digests

- theorem: `bfb0dc4c4678803cc46e791cbe60e87736ea41ce14db157e8fb1726e28b671fe`
- divisor reduction: `cf893db1c6c2718a614dfdf519e220cbb3b7312aff62130c608ddd7598c1c93a`
- lateral calibration: `f94cb784d7218e3fa2f03c024a4921457b1d517ddfa022c81a90865c4dec5143`
- upper/lower route manifests: `63e19e63181d9573590d2ff4825787c95f4ecc1b99da8d510df370b7ccfaa62d`, `6216ca406c364cf382baabb7f6ea112ed095ce2393ac9d63f06636d5157565b5`
- upper/lower clearance certificates: `c4c9fae572cd9ca02ffdc493389c738731a961df9e7593b0be72382bf8e2240a`, `9cf591af652d6c9e7e5609f8641ef00b78c6c8e7434d8d2be0ae6291fbff0217`
- live 52-file Pathfinder closure: `1c887a5bfe2605e085d84176e592f0823184d70526b378fb53d05ce6fdcdc195`
- live DBP provider: `0a91a1a5e50988758c0ce7221bd285ccf047eaa3ea1e6e61027938e14efc5ced`
- upper/lower route certificates: `9cef4fce941d3f11bdd460562a6eb39b5d6925c06bc42ba90cf20d768e5bad06`, `2853d3fbfe78c9a64ad34cac144736b8658d2e7c4a37f0b53815ed6721e09f82`
- two-certificate bundle: `b2fc82f6705cfe25070a641f4678f2caf94c35e36a11bc1023a9fd9a4f56605c`

Two clean Python processes reproduced the same CCE-2 bundle digest.  PF-0's
confirmation report remains bound as
`304fccce5ed1206f23969952634d10b250d8d4d7a7a955971afa8018c2372008`.
CCE-1 retains its historical PF-0 closure binding; CCE-2 independently binds
the expanded live closure.

## Changed production and verification sources

- `engine/src/cella/continuation/corridors.py`
- `engine/src/cella/continuation/model.py`
- `engine/src/cella/continuation/pathfinder.py`
- `engine/src/cella/continuation/api.py`
- `engine/src/cella/continuation/__init__.py`
- `engine/src/cella/pathfinder/recognize/dbp_native.py`
- `engine/tests/gate_continuation_cce2.py`
- the three campaign verifier programs and required theorem/JSON/report artifacts

## Gates and legacy locks

- 37/37 engine test programs passed.
- DBP native evaluator: 1,591 assertions passed.
- PF-0: 58 assertions passed.
- CCE-1: 24 assertions passed.
- CCE-2: 31 assertions passed.
- stand-alone corridor verifiers: 47 assertions passed.
- legacy schema-1.1 bundle unchanged:
  `aa97101da7ae03f127adf4dc7940128fbdc8ee425a21c2ef88b828c76afd2989`.
- CCE-1 six-envelope bundle unchanged:
  `c04ba9200de47bd5fc68e84e9c932ab63e5ea9eb41981b6bba3144272b7f84a3`.

## Recorded events and scope

No stop ceremony was performed. The prior mistaken primary-path pointer to
`research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/pathfinder_m1_scout.py`
was not read, imported, executed, or used as CCE-2 evidence; production has
zero references to it. The file remains a valid scout in its own campaign.
Work was routed through the primary typed Pathfinder provider and its 52-file
source closure. Paper III was not edited; a separate
insertion note is supplied for review.

This stage certifies the base tube, unique path lifts, and the curve family
with marked endpoints and third-kind poles.  It does not certify a global
single-valued sheet over an odd-winding tube and does not certify a surface
sweep.  Remaining obligations are enumerated in `CCE_2_GAP_LEDGER_v1.0.md`.
