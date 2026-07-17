# Transfer-Function Paper — Claim Revalidation Ledger

**Date:** 2026-05-31
**Purpose:** Re-validate *every* claim in `transfer_function_exponent_family_v4.tex` + the V5 prose `.md` against the most current results/scratch artifacts, by **running code** (not reading closeouts), before compiling a new air-tight paper. Per CLAUDE.md §3 (Record integrity): a claim is "proven/measured" only when a reproducible run stands behind it; inference is tagged as inference.
**Method:** 7 adversarial validation sub-agents (clusters A–F), each required to reproduce headline numbers from running code, with independent oracles (exact `Fraction` / `mpmath`) where feasible. New verification scripts under `scratch/_revalidation/cluster*/`; no existing artifact modified.

**Verdict legend:** VERIFIED (reproduced) · PARTIAL (core holds, sub-claim open) · GAP (needs retest) · REFUTED (claim does not hold) · CONVENTION-ARTIFACT (true but mislabelled).

---

## 1. Verdict summary

| # | Claim | Status | Paper label allowed |
|---|---|---|---|
| A1 | BACL invariant `a−b = j·ulp(b)` | **VERIFIED** (31k records + 50k independent, 0 viol) | **proven** (scope: f16/f32/f64 normal+subnormal; f128 deferred) |
| A2 | Conjecture C (no-binade-drop, sqrt normal) | **VERIFIED** (220,444 + 383,045 independent, 0 viol) | **proven** (scope: float64 normal, n=2, RN-even; C_subnormal open) |
| A3 | c2 integer-lattice; n=2 \|j\|≤1 | **VERIFIED** (90k records 0 viol; n=2 \|j\|≤1 robust) | **proven** for n=2, f≥2⁻¹⁰²¹ |
| A3′ | c2 n=3 route-rank "np.cbrt \|j\|max=7 vs pow=2" | **PARTIAL / grid-conditioned** | observation only — *7 is not a bound* (see §3) |
| B1 | Transfer law (Thm 1) synthetic slope = α−1 ~1e-11 | **VERIFIED** (bit-identical via real V4 primitives) | **verified, eval-layer** (law itself proven by chain rule) |
| B2 | Cross-fixture local slope of E → α=1 (Schw .9962/PA 1.0) | **VERIFIED numbers; OPEN LEAD** (raw `math.log2`, not typed) | open lead (re-run gap T8-b) |
| C1 | Precision-scaling `C_{p,k}=a+u_p·b_k`, R²=1.0 regular region | **VERIFIED** (R²=1.0 all 16 rows; independent OLS 1.0/8dp on 12 load-bearing) | verified, eval-layer |
| C2a | cbrt F1 intercept CI excludes 0 below oracle floor | **PARTIAL** (CI [5.1e-21, 5.8e-17], < u_p) | open sub-claim |
| C2b | F1/F2/F4 slope distinguishability | **REFUTED/GAP** (CIs overlap near 0, all 4 fixtures) | "not separable with 3–6 precisions" |
| C2c | b_k vanishes inside Sterbenz half-space | **REFUTED** (all 4 F2 Sterbenz CIs exclude 0) | refuted/reframed |
| C3 | F2 Sterbenz-region b_k CI-upper > regular (table) | **VERIFIED** (8/8 values match .tex to 3dp) | verified, eval-layer |
| D1 | F3 silence (≡0 every cell/precision) | **VERIFIED** | observation |
| D2 | F2 grain "0.5 Schw/SR vs 0.25 PA/cbrt" | **CONVENTION-ARTIFACT** (integer-snap vs half-snap; same half-integer lattice in all 4) | restate: "half-integer lattice in all four" |
| D3 | F4 integer lattice (residual 0) | **VERIFIED** (float64; f32 silent) | observation |
| D4 | F1 ∥ F2 polarity coupling 100% | **VERIFIED** (exact 100%); "p<1e-10" NOT in artifacts | observation; recompute p (task026c-prime had p=3.1e-5) |
| D5 | Sterbenz directional density bias table | **VERIFIED** (count-for-count, 4 fixtures) | observation; note strength varies, direction robust |
| D* | "Cross-fixture invariance" as a **Theorem** | **MISNOMER** | **relabel Observation** (the .tex itself concedes L415) |
| E1 | Sterbenz boundaries r=4 / β=1/√2 / x=0.5 / x=0.5 | **VERIFIED** (exact) | derived |
| E2 | Sub-lattice alignment: c2 dominates c1 (Task 031) | **VERIFIED** (42/42 tests; sole frontier; b_k CI-tie 0.732 vs 0.640) | verified, eval-layer |
| E3 | Cross-fixture c2-dominates-c1-on-lattice (all 4) | **VERIFIED**; but task032 *strong* prediction FALSE (c1 irregular, not ¼-int, in SR/PA/cbrt) | weaker claim only |
| Fa1 | Phase 2A: F1 boundary = instrument artifact | **VERIFIED** (SR 0.74291→0.34492 w/o f128; F1≡0 at collapse cells, mpmath 3000-bit) | verified, eval-layer; "dominating term" REFUTED |
| Fa2 | Thm 4.1.1 subnormal sqrt identity V₂≡f | **VERIFIED in scope** (0 counterexamples / 95.4M, block-exhaustive at both seams; NOT full 4.5e15 enum) | "verified exhaustively at seams + sampled; analytic half-ULP argument" — *not* "mathematically guaranteed" |
| Fa3 | Subnormal cbrt combinatorics {−4..1}, excursions {−7..+3} | **VERIFIED** (99.09% in {−4..1} my sample vs 98.7% claimed; set exact; numpy.cbrt 27/64 not-CR; CR-cbrt→{−1,0,1} 100%) | verified, eval-layer (sample-dependent %) |
| Fb1 | Phase 2C nested-window diagnostic | **PARTIAL** (E rejected ΔAIC=1749 ✓; C s∞=1.25 ✓; fragile ≥3 ✓ qualit.) | see refutations below |
| Fb1d | "off-grid algebraic exponents MIS-REJECTED" | **REFUTED** (still classified algebraic; only s∞ accuracy degrades) | drop claim |
| Fb1′ | sandbox drift table {3:2.14, 5:3.91, 6:4.62} | **STALE/WRONG** (actual {3:2.45, 5:3.80, 6:4.45}) | use corrected numbers |
| Fb1″ | "0/9 false-accepts" | **scope-limited** (holds for C/D/E; adversarial P-probe finds 2/9: P2,P3) | state honestly |
| Fb2 | log²/√x·log degeneracy O(1/t) | **VERIFIED math**; "proven topological degeneracy" OVERSTATED | "verified observation, eval-layer" |
| Fb3 | W(k) info-loss form | **INCONSISTENCY CONFIRMED**; corrected single form below | use corrected form |
| Fb4 | Parity-trap (V_n=1 one-sided ½-ulp) | **VERIFIED** (V<1 side ∈{−½,0,½}, 5075/10000 at ±½; V>1 side ∈{−1,0,1}, 0 at ½) | verified, eval-layer |
| Fb5 | Payload route-inversion crossover | **VERIFIED** (all 4 fixtures; grid-density-stable ⇒ lattice property, not precision-scaling) | verified, eval-layer (apparatus/lattice-burden) |

---

## 2. The locked trio — safe to label "proven"

BACL, Conjecture C, c2 (n=2) reproduce with **0 violations** under both re-run and independent zero-import exact-rational oracles. These are the **only** claims that keep the word "proven" in the new paper, each with the scope its closeout already carries:
- **BACL:** float16/32/64, normal + subnormal; float128 deferred (x86 80-bit extended, not IEEE binary128).
- **Conjecture C:** float64 normal range, n=2 sqrt, round-to-nearest-even; `C_subnormal` frozen open.
- **c2 lattice theorem:** n=2 only, f_float ≥ 2⁻¹⁰²¹; stated as integer-lattice + |j|≤1.

## 3. Corrections the new paper MUST carry (the air-tight checklist)

1. **c2 n≥3 route-rank is grid-conditioned, not a bound.** "np.cbrt max|j|=7" reproduces only on the audit's exact hybrid grid; plain `linspace` gives 8, denser gives 11 (pow(1/3): 2→5). State the *direction* (np.cbrt rank ≫ pow rank) as robust; do **not** state 7 as a bound.
2. **F2 grain is half-integer in all four fixtures.** The "0.5 vs 0.25" split is an artifact of integer-snap vs half-snap residual conventions in two classifier implementations. Restate the invariant as "F2 sits on a non-integer (half-integer) lattice in every fixture"; footnote the 0.5/0.25 as convention.
3. **Cross-fixture invariance is an Observation, not a Theorem.** Relabel; the .tex already concedes "empirical-invariance statement, not a derived theorem" (L415).
4. **F1∥F2 polarity "p<1e-10" is not in any artifact.** Either recompute and cite, or use the task026c-prime reference-grid value p=3.1e-5. Substantive reproducible claim = exact 100% sign agreement where both fire.
5. **Sterbenz directional bias: direction robust, strength varies** (cbrt "above" density 0.485 not strongly suppressed). State as empirical regularity, not sharp law.
6. **Thm 4.1.1 (subnormal sqrt identity):** state "verified exhaustively at both seams + densely sampled (95.4M, 0 counterexamples) with a sound analytic half-ULP argument," **not** "mathematically guaranteed." Not a full enumeration of all ~4.5×10¹⁵ subnormals.
7. **cbrt combinatorics %:** use reproduced 99.09% in {−4..1} (sample-dependent) with the exact set {−7..+3}; note numpy.cbrt is not correctly-rounded (27/64 on the original grid) and a correctly-rounded cbrt tightens the spread to {−1,0,1}.
8. **W(k) corrected single form:** `W(k) = min(53, −⌊α·k + log₂|c|⌋)` (graded floor). The competing forms `min(53, 53+αk+C)` and `min(53, 53−k)` are **wrong** (wrong sign on k / flat-pinned at 53).
9. **log²/√x·log degeneracy:** "verified observation, eval-layer," not "proven topological degeneracy." It is a finite-range failure of this specific AIC/BIC harness (P2 is gate-marginal, drift 1.99 vs gate 2.0).
10. **Nested-window diagnostic:** keep n_windows≥3 pin; use corrected drift table `{2:1.05→STABLE, 3:2.45→UNSTABLE, 4:3.08→UNSTABLE}`; **drop** "off-grid algebraic exponents mis-rejected" (REFUTED — classification still accepts algebraic, only s∞ accuracy degrades); state "0/9 false-accepts" is scope-limited to C/D/E (adversarial P-probe finds 2/9).
11. **task032 strong prediction was FALSE** (`strong_prediction_held: false`): c1 is "irregular," not half/quarter-integer, in SR/PA/cbrt (only Schwarzschild is quarter-integer). Carry only the weaker "c2 dominates c1 on lattice class in all four."
12. **"proven" provenance sweep:** reserve "proven" for the trio only (Correction #2 list above). Demote "mathematically guaranteed" / "bounded consequence" / "proven topological degeneracy" → "verified observation, eval-layer."

## 4. Gaps to retest (feed Task #8)

| Gap | Why | Handoff ref |
|---|---|---|
| **F2 Sterbenz-region b_k in exact rationals** | The real open Q5 sub-claim (C2c refuted the vanishing prediction; F2 is the load-bearing path; Task A only ran F1). Carry residuals as `Fraction` to escape the float128 floor. | §3.2 |
| **Cross-fixture α→1 slope, typed + pre-registered** | B2 verified the numbers but on raw `math.log2`. A typed-primitive, audit-framework re-run converts the "open lead" into a citable result = substrate-invariant-search Phase A. | §2.1 / §3 |
| **F1−F2 common-mode rejection** | Confirms F1/F2 share R² so F1−F2 cancels the sqrt round-off, isolating operand-assembly path difference; supports the observable-structure section. | §3.5 |
| (forward, not paper-blocking) exact-forward M⊕C / G-presence; observable sufficiency map | substrate-invariant-search Gate 2 frontier; paper states them open. | §3.1 / §3.4 |

## 5. Infrastructure bugs found (mechanical, fix under Task #8/#10)

- `tests/test_task024b_schwarzschild_four_form.py:13` — stale import `AlphaWindowStabilityStatus` from `lloyd_v4.primitives`; relocated to `lloyd_v4.observers` under GAP-009. Blocks collection. One-line fix. (Campaign itself intact.)
- `tests/test_task017c_multi_precision_theorem2.py` — 2 tests fail on `FileNotFoundError` for the removed `Docs/transfer_function_exponent_family_v3.tex`; stale-path infra, no computed result affected.
- `scratch/sandbox_summary_report.md` drift table is stale (see Correction #10).
- **FIXED 2026-05-31 (mechanical):** `tests/test_task024b_...py:13` import repointed `primitives`→`observers`; `tests/test_task017c_...py:20` `THEOREM_SOURCE` repointed from removed `Docs/.../v3.tex` to `Build_Docs/transfer_function_exponent_family_v4.tex`.

---

## 6. Gap retests (Task #8 — eval-layer, research-grade; orchestrator verdicts)

Scripts under `scratch/_revalidation/retest{A,B,C}/`. Each passed its retrodiction gate. Verdicts below are the orchestrator's (not delegated).

### Retest A — F2 Sterbenz-region b_k in exact rationals (handoff §3.2; the real open Q5 sub-claim)
- **Gate:** PASS (Sterbenz boundary x=0.5 + F2 half-integer grain reproduced).
- **Escaped the degeneracy:** YES — 97% of Sterbenz cells yield ≥2 distinct nonzero residuals under exact `Fraction` arithmetic. The Phase-2A degeneracy was **F1-near-singularity (x→1)**, a *different region* from F2 Sterbenz (x≤0.5); it does not transfer.
- **Measurement:** F2 **Sterbenz b_k = 0.720** (R²=1.0) vs **regular b_k = 0.400** (R²=1.0), ratio **1.80** (larger, not vanishing).
- **VERDICT:** the old "b_k vanishes inside the Sterbenz half-space" prediction is **REFUTED by exact measurement** (consistent with C2c). **Caveat (load-bearing):** `b_k` here is the **ULP rounding-floor coefficient** (residual/u_p ∈ {0,±1}, ~50/50 parity sign, ~59% exactly zero ⇒ RMS ∝ u_p by construction), **not** an emergent substrate boundary. Paper statement: "On F2 in the Sterbenz region, C=a+u_p·b_k holds with R²=1.0 and identifiable nonzero b_k≈0.72 (≈1.8× regular); b_k measures the rounding-floor coefficient, so this refutes the vanishing prediction but does **not** establish a substrate boundary." The open sub-claim is thereby given a clean, honest statement (not closed as substrate).

### Retest B — Cross-fixture α→1 slope via TYPED primitives (handoff §2.1/§3; substrate-invariant-search Phase A)
- **Gate:** PASS (raw `math.log2` baseline reproduced: Schw 0.9962 / PA 1.0000 at N=5).
- **Typed (`typed_log_log_slope` OLS):** Schw **0.99669**, PA **1.00000**, |Δ| **0.00331** at N=5 (N=10: 0.99577/1.0; N=20: 0.99411/1.0). Method-gap vs raw ≤ **0.0014**, estimator-level (OLS-over-window vs central-difference), not data-level. All `SLOPE_OBSERVED`, R²≈1.0.
- **VERDICT:** convergence **survives the typed instrument** → promote from "open lead" to **verified eval-layer observation, citable as substrate-invariant-search Phase A** (measurement-robustness across 2 fixtures; does NOT by itself assert α=1 is a substrate invariant — Gate-2 stays open; SR + wider sweep is forward work).

### Retest C — F1−F2 common-mode rejection (handoff §3.5)
- **Gate:** PASS (F3≡0 all fixtures; Schw bit-matches committed `v3_reference_overlay.csv`).
- **Measurement:** F1/F2 share the **bit-identical R² operand** (confirmed in `src/lloyd_v4/evals/*_four_form.py` AND via `.hex()` equality), all 4 fixtures. `F1−F2 = (1−x_term) − f_direct`. In exact reals R² cancels exactly (R-independent); **in float64 the cancellation is exact at ~40–45% of cells and sub-ULP (≤1.11e-16) elsewhere** — R-independence holds to ~1–2 ULP, **not bit-exact**. F4 uses a distinct operand (f_alt≠f_direct) ⇒ F4 round-off is form-specific where the routing yields a distinct float64 operand (majority for Schw; large minority for SR/PA/cbrt).
- **VERDICT:** common-mode structure **confirmed** with the precision that the float cancellation is "**to ≤1 ULP**," not "exactly." Supports the observable-structure section (F1≡F4 at substrate-signature level per HR95; sqrt fractional part as a form-invariant common-mode carrier).
