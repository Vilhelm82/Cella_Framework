# WARP Stage A Report — factorability decidability (CL-W1/W2/W3)

**Date:** 2026-06-14 (machine date). **Arm:** algebra (THE WARP) of
`the-shared-residual` (charter OPEN; geometry arm CLOSED + RATIFIED, HR138).
**Authority:** `Build_Docs/Agent_tasks/CAMPAIGN_BRIEF_algebra_arm_DRAFT.md` §3/§4 +
§10 RATIFIED 2026-06-14 (Will) + standing rules 1.8/1.9 + the manifest SPINE FENCE.
**Tier:** eval-tier (`src/lloyd_v4/evals/the_warp/`); no substrate edit, no promotion
(Rule 1.2). **Spine FENCED** — no spine claim, no cross-domain G-claim.

**Prereg:** FROZEN pre-emission, pin `b2790acf9c3482d04823d190f5d78fd0e8467d507c4ee4c1c43e4f6e165e6751`
(`stage_a/prereg.json`, `prereg_sha256.pin`); manifest dependency pin matches the
frozen Stage-0 manifest. **Records:** `stage_a/records/stage_a_records.jsonl`, sha256
`c540c1e0860406336e0639e015f0cf9cad9be7d1baa2c3da37583b9a28517c82`, **byte-stable ×2**.
Rule 1.8: `run_stage_a.GRADER_CLAUSES` byte-verbatim of the frozen `PMW_CLAUSES`
(drift gate live, tested). Covenant #7: the probe (`D_static`/`D_dynamic`) never
imports the referee; the commuted-tree truth + the one declared oracle are
runner-wired. Full suite exit 0.

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| **PMW.1** decidable core (CL-W1) | **PASS 6/6 — K-W1/K-W2 NEVER FIRED** | On every FX-W-A/C cell `D_static == D_dynamic == "factors"` (biconditional, zero false verdicts); the independent commuted-tree referee matched `D_dynamic.true_q` exactly in ℚ (factoring not self-certified). |
| **PMW.2** type property (CL-W2) | **PASS** | AST-seam clean (verdict path references no float-lane value / residue / exposure); `D_static` verdict point-invariant; UNDERFLOW-WITNESS-ULP (FXWC1) float lane reads `0.0` while the cell factors via `R_exact`-by-composition — factorability ≠ float-lane exactness. |
| **PMW.3** the Richardson wall (CL-W3) | **PASS 3/3 — K-W4 NOT FIRED** | On every FX-W-D cell `D_static` = `does_not_factor` and `D_dynamic` refuses typed (`transcendental_uninterpreted`); the one declared oracle call recovers factoring — the split coincides with on-branch expression-equality. Fixture split **[MEASURED]**; general semi-decidability **[ANALYTIC]** (Richardson 1968), never claimed measured. |
| **PMW.4** determinism | **PASS** | Records byte-stable ×2 (sha above). |

## Status moves (applied 2026-06-14, Will's GO)

- **CL-W1 → DEMONSTRATED** (PMW.1).
- **CL-W2 → DEMONSTRATED** (PMW.2).
- **CL-W3 → DEMONSTRATED** (PMW.3; split [MEASURED], semi-decidability [ANALYTIC]).

Recorded in `CLAIM_LEDGER.md` (append-only Status-moves log; prior NOT_YET_PROBED
rows preserved). No HR/glossary write — charter-level canonical record reserved.

## Defect chains

None. All predictions passed on first frozen run; no kill fired; no refute-row.

## Method notes (for audit)

- **Decidability shape** cites the in-family precedent `required_precision` (recon Q3,
  `precedent_confirmed`): a static structural predicate over a restricted finite
  lattice, decidable = YES — CL-W1 constructs and confirms its own biconditional.
- **`D_static`** lifts the `AtomKind` partition from `core.binding` only (recon Q2,
  `partial_wrap`), not the manifest-lineage walk; its verdict function `_factor_verdict`
  reads the operation type and recurses — the AST-seam proves it.
- **R15 (binding, §10.7):** `below_detection` in this lineage is
  `R_exact`-by-composition, not a `T_token` — the schema carries no `T_token` for it.

## Will's desk

Stage A clean. Next: **Stage B** — the carrier classifier over FX-W-E/F: **CL-W4**
(free-module additive reconstruction closes; [ANALYTIC]+confirm) and the **CL-W5
keystone** on ℙ¹(ℚ) (additive ill-defined → the foregone [ANALYTIC] half; the
[MEASURED] weight is whether the Möbius/PGL₂ action maps equal points to equal points
where addition cannot). K-W3 armed (refute-row-and-continue) — a named-boundary
refutation is a result. Prereg frozen before the battery.
