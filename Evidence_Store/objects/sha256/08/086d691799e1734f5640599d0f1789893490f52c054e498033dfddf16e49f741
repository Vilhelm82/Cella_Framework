# Phase A / Phase 0 — Frozen Pre-registration (substrate-invariant-search)

**Status:** ❌ SUPERSEDED (never signed, never run as a verdict generator), 2026-06-07. Resolved by
`Build_Docs/Reports/substrate_invariant_search/phase_a_closeout.md`. The leave-one-fixture-out search
instrument specified below was proved unnecessary before freeze: the candidate relation `S2 == G2` is
an analytic **identity** (chain rule on `base_operand = y²`), so its verdict cell cannot fail and is
not a test; and the univariate-κ cells fail by structure, but their failure does **not** license the
D.5 `H_zero_jet_only` conclusion (S2≡G2 is multivariate). Only a thin FD-metrology receipt and the
binade seam carried empirical content; both are delivered in the closeout. This document survives as the
record of a search we proved we did not need to run. Do not build the instrument.

**Original status (historical):** ⏳ AWAITING SIGN-OFF. Once signed, this artifact is **frozen**
(CAMPAIGN_DISCIPLINE rule 1.1): no post-hoc edits to thresholds, formulas, or hypotheses — a result
that does not fit gets a new *versioned* prereg, never a quiet rewrite.
**Authority:** `substrate_invariant_search_successor_authority_2026_06_07.md` (R1).
**Build spec:** `substrate_invariant_search_phase_a_jet_order_spec.md`.
**Date:** 2026-06-07. **Layer:** `src/lloyd_v4/evals/substrate_invariant_search_phase_a.py` (eval-only).

---

## A. Three design decisions requiring your sign-off (read first)

These deviate from / sharpen the spec because the data forces them. Approve or amend before freeze.

1. **The universality test is bidirectional 2-fold, not 3-fold leave-one-out.** The geometry table has
   only **two** varying-κ fixtures (Schwarzschild, pure_algebraic); SR is constant-κ. So the test is:
   fit `C=f(T)` on Schwarzschild → predict pure_algebraic, and fit on pure_algebraic → predict
   Schwarzschild. **Honest consequence:** a PASS on n=2 fixtures is *"consistent across the two fixtures
   we have,"* NOT *"universal."* A FAIL is a clean fixture-bound verdict. Real universality needs a 3rd
   varying-κ fixture — `cbrt_four_form` exists elsewhere in the campaign (task029c) but is NOT in this
   geometry table. **Decision: run the 2-fold now as a strong filter, and flag cbrt-table generation as
   the Phase-B upgrade if 2-fold PASSes?** (My recommendation: yes — a 2-fold FAIL kills the hypothesis
   cheaply; only a 2-fold PASS earns the cost of a 3rd fixture.)
2. **The verdict is restricted to the κ-overlap region [0.18, 1.89].** Outside it (Schwarzschild's
   0.0024–0.18 and 1.89–3.83) prediction is extrapolation, reported separately, **not** part of the
   verdict. Overlap computed at runtime as `[max(min κ_i), min(max κ_i)]` over the two fixtures; the
   y''-target variant uses the analogous y'' overlap.
3. **Noise-floor / shuffle-gate are split (sharpening the spec's single `max(...)`).** As literally
   written, `noise_floor = max(SR_residual, shuffle_P95)` makes the shuffle pass by construction (it is
   one of the maxed terms), so the shuffle could never "FAIL the universality test." I split them: the
   **floor** is the SR-slice residual (instrument irreducible error); the **shuffle is a separate gate**
   that must sit *well above* the floor (proving the test can fail). Exact numbers in §C/§D.

---

## B. Frozen inputs, channels, targets

- **Input:** `Build_Docs/Reports/mcg_geometry_first/phase_1_geometry_table.json` (sha256 recorded at
  run; expected prefix `6502e942…`). Columns used: `fixture`, `natural_function_value` (y),
  `J_value` (y'), `hessian_value` (y''), `principal_curvature` (κ), `stability_status`,
  `near_degenerate_flag`.
- **Rows in verdict:** `fixture ∈ {schwarzschild_four_form, pure_algebraic_four_form}` (varying-κ),
  `stability_status == "stable"`, `near_degenerate_flag == False`, κ ∈ overlap (§A.2). SR rows used only
  for the floor/control. `*_anchor` rows excluded entirely.
- **Substrate channels** `C` (FD jet ladder on `F(t)=log₂|base_operand(t)|`, central differences,
  mirroring `mcg_geometry_first_geometry`'s `RELATIVE_STEP_LADDER` + its stability gate):
  - `S0 = F` (0-jet, magnitude) — **NEGATIVE CONTROL, pre-registered to FAIL** (§D.4).
  - `S2 = d²F/dt²` (raw 2-jet), `S2_s = d²F/ds²` (arc-length 2-jet) — **the candidates.**
  - `S1_s = dF/ds` reported for completeness, not a verdict channel.
- **Geometric targets** `T`: `κ` (principal_curvature), `y''` (hessian_value).
- **Metrology check (not a verdict):** FD `S2` must match the closed form
  `G2 = (2/ln2)(y''/y − (y'/y)²)` to **relative 1e-3** on stable rows; rows failing are reclassified
  unstable and excluded. (Declared metrology, not hidden magic.)

---

## C. The monotone fit and the noise floor (exact)

- **Fit `C=f(T)`:** bin `T` into `K` equal-count bins over the training fixture's overlap rows; take the
  **median C per bin**; enforce monotonicity by pool-adjacent-violators (PAV) on the bin medians;
  predict by linear interpolation between bin centers, clamped at the endpoints. **K_start = 6.**
  Pure-stdlib (no sklearn, no symbolic backend). DOF knob = K (see §D shuffle reduction).
- **Normalization (dimensionless error):** `norm_err = |C_pred − C_true| / DR(C)`, where
  `DR(C) = P97.5(C) − P2.5(C)` over the pooled verdict rows (per channel). All errors below are
  `norm_err`.
- **SR-slice floor (per channel):** `SR_floor(C) = P95( |C − median(C on SR)| ) / DR(C)` over stable SR
  rows. (On constant κ a perfect κ-tracker is flat; its residual wander = irreducible position leakage.)
- **noise_floor(C) = max( SR_floor(C), 0.02 ).** The 0.02 (2% of dynamic range) is a floor-on-the-floor
  for FD/round-off realism, so a near-zero `SR_floor` can't make PASS unfalsifiably easy.

---

## D. Hypotheses, verdict thresholds, gates (exact, frozen)

**Pre-registered expectation (the NULL):** `H_zero_jet_only` — only `S0` (magnitude) is shared;
`S2_s` is fixture-bound or noise. I expect the null to be *hard to reject*. `H_jet_geometry` is the
alternative: a substrate jet is a universal function of a geometric jet across the two fixtures.

**D.1 Phase-0 shuffle-null gate (MUST hold before ANY §D.3 verdict is read).**
Permute the (coordinate ↔ fingerprint) pairing within each varying-κ fixture, recompute the jets, run
the 2-fold fit; record the worst-fold P95 `norm_err`. **N = 200 permutations, seed = 20260607.**
`shuffle_err = median over permutations of (worst-fold P95 norm_err)`.
**Gate:** `shuffle_err ≥ 5 × noise_floor(C)` for the candidate channel `C = S2_s`.
- If the gate **fails** (chance predicts too well → fit over-flexible), halve K (6 → 3 → 2) and retry.
  Record the final K. If it still fails at **K = 2** (linear), the instrument is **VOID** — report and
  STOP; no hypothesis verdict is issued.

**D.2 Route-identity gate (MUST hold).** The four algebraic forms of `base_operand` agree per coordinate
to relative **1e-12** (already a closed dyadic identity `1 − x_term`); if any disagree, the fingerprint
is route-contaminated and the phase is VOID.

**D.3 Universality verdict (per channel `C ∈ {S2, S2_s}`, per target `T ∈ {κ, y''}`):**
- **PASS (consistent-across-the-two-fixtures):** **both** folds have P95 `norm_err ≤ 2 × noise_floor(C)`,
  within the κ-overlap.
- **FAIL (fixture-bound):** **either** fold has P95 `norm_err > 2 × noise_floor(C)`.
- (No middle verdict. The `2×` is the only slack and is frozen here.)

**D.4 S0 negative control (instrument-validity check).** `S0` vs `κ` **must FAIL** §D.3 (reproducing
Phase H's 0/5 — a 0-jet cannot be cross-fixture-universal against a 2-jet). **If S0 PASSES, the
instrument is broken → VOID, STOP.**

**D.5 Native-combination finding (§4.3 discovery output).** Report the PASS/FAIL matrix over the 4
(C,T) cells. Interpretations, pre-committed:
- `S2_s`↔`κ` PASS ⟹ substrate carries Euclidean curvature directly.
- `S2_s`↔`κ` FAIL **and** `S2_s`↔`y''` PASS ⟹ **the substrate's native invariant is operand
  log-acceleration; κ is its continuum shadow** through the `(1+y'²)^{3/2}` Jacobian the bits never
  compute. (The §A-flagged "interesting" outcome; the better V4-native rebuild story.)
- all candidate cells FAIL ⟹ `H_zero_jet_only` holds → write the clean negative; pivot to the seam.

**D.6 Seam (always reported, never a loss).** The κ resolution at which the lattice channel `Δ²B`
(discrete 2nd difference of `floor(log₂|base_operand|)`) goes flat / aliases — the measurable binade
granularity where "the algebraic handle is lost." Reported regardless of D.3.

---

## E. Output contract (frozen)

`Build_Docs/Reports/substrate_invariant_search/phase_a_substrate_jet_curvature.json`, byte-stable
(`json.dumps(..., indent=2, sort_keys=True)`). Top-level keys: `audit_name`, `phase`, `campaign`,
`authority`, `preregistry` (this file), `input_sha256` (geometry table + this prereg + spec),
`overlap_region`, `noise_floor` (per channel), `shuffle_gate` (shuffle_err, K_final, pass/fail),
`route_identity_gate`, `s0_negative_control` (must be FAIL), `verdict_matrix` (4 cells, §D.3),
`native_combination` (§D.5), `seam_resolution` (§D.6), `per_row` (S0,S1,S1_s,S2,S2_s,ΔB,Δ²B,y,y',y'',κ,
G2,S2_fd_vs_anchor_residual,fixture,stable,in_overlap), `console_log`, `timestamps`. Stability/
near-degenerate/out-of-overlap rows segregated under separate keys, excluded from the verdict.

---

## F. Sign-off checklist (CAMPAIGN_DISCIPLINE §9)

- [ ] §A design decisions approved (2-fold scope; overlap restriction; floor/shuffle split).
- [ ] §C K_start, normalization, floor formula approved.
- [ ] §D thresholds (`2× floor` PASS; `5× floor` shuffle gate; N=200/seed) approved.
- [ ] V3-isolated, no symbolic backend, byte-stable JSON, input sha256 — confirmed in build.
- [ ] Build order locked: route-identity gate → S2-vs-anchor metrology → shuffle gate (must FAIL) →
      S0 negative control (must FAIL) → only then read the §D.3 verdict matrix.

*Nothing in §B–§E moves once you sign §F. A surprise gets a versioned prereg, not an edit.*
