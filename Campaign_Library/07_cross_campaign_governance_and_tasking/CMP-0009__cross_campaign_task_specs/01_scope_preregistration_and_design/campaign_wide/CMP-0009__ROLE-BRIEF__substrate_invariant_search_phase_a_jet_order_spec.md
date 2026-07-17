# Phase A — Substrate-Jet Curvature Test (build spec)

**Campaign:** substrate_invariant_search (successor authority — write R1 first, this is its first phase)
**Layer:** `src/lloyd_v4/evals/substrate_invariant_search_phase_a.py` — eval only, no substrate modification.
**Discipline:** V3-isolated (no `lv3`), no symbolic backend (FD-only, mirroring `mcg_geometry_first_geometry`),
byte-stable JSON (`sort_keys=True`), sha256 of every input artifact, pre-registered before first run.

---

## 0. Why this phase exists (the corrected diagnosis)

Phases A–H tested **0-jet** substrate observables against a **2-jet** geometric quantity.

- The headline observable `E = log₂|base_operand|`. In every fixture `base_operand = 1 − x_term = y²`,
  so `E = 2·log₂ y` — a pure function of the operand magnitude `y`. The 0-jet.
- Every other candidate (`ulp_spread_log2`, `log2_min_ulp`, `signed_asymmetry`, …) is `ulp()`/`log2()`
  of operand values at a single coordinate. `ulp(v)` depends only on the binade of `|v|`. All 0-jet.
- The target `principal_curvature` (the campaign's "K_G") `= |y''| / (1+y'²)^{3/2}` — a 2-jet quantity.

Consequences, both forced and non-informative about geometry:
- Within-fixture `ρ(E, κ) = −1.0000` is the **coordinate tautology** (both monotone in `t`).
- Cross-fixture `0/5` at matched κ is a **jet-order mismatch**, not absence of geometry.

**This phase samples the missing jet orders** by differentiating the substrate fingerprint along the
coordinate, then tests whether a substrate jet is a *universal function* of the geometric jet across
fixtures. The within-fixture rank test is retired; functional universality replaces it.

---

## 1. Inputs

- `Build_Docs/Reports/mcg_geometry_first/phase_1_geometry_table.json` (411 rows). Per primary-fixture row
  it already carries the geometric jet: `natural_function_value` (`y`), `J_value` (`y'`),
  `hessian_value` (`y''`), `principal_curvature` (`κ`), plus the FD ladder and `stability_status`.
- Primary fixtures only: `sr_four_form`, `schwarzschild_four_form`, `pure_algebraic_four_form`.
  `geometry_anchor` rows excluded from all headlines (existing pooling rule).
- Rows with `stability_status != "stable"` or `near_degenerate_flag == True` are **excluded from the
  universality verdict** and reported separately (they are domain-boundary artifacts, not signal).

---

## 2. The substrate fingerprint and its jet ladder

### 2.1 Smooth channel (the continuous test)

Define the fingerprint as a *closed-form function of the coordinate*, so it can be FD-laddered exactly
the way the geometry module ladders `y` — evaluate at `t ± h`, central-difference, same
`RELATIVE_STEP_LADDER`, same stability gate.

```
F(t) = log2(|base_operand(t)|),   base_operand(t) = 1 − x_term(t)
       x_term:  β²  (SR) | 2/r (Schw) | x (pure_alg)
```

Compute three substrate channels at each grid point via the FD ladder on `F`:

```
S0(t) = F(t)            # 0-jet  — equals the existing E. Magnitude.
S1(t) = dF/dt           # 1-jet  — operand log-velocity.
S2(t) = d²F/dt²         # 2-jet  — operand log-acceleration. Carries y''.
```

Closed-form anchor (validation label only, not used as substrate input):
`S2 = (2/ln2)·(y''/y − (y'/y)²)`. Verify the FD `S2` matches this to ladder tolerance per row; record
the residual. (This is the "declared metrology, not hidden magic" check the geometry module already does.)

### 2.2 Arc-length reparametrization (the invariance step — mandatory)

`S1, S2` in raw `t` are coordinate-dependent and will not be invariant across fixtures that parametrize
differently. Reparametrize by intrinsic arc length of the graph:

```
ds/dt = sqrt(1 + (y')²) = sqrt(1 + J_value²)
S1_s = dF/ds  = S1 / (ds/dt)
S2_s = d²F/ds² = (S2 − S1·(d²s/dt²)/(ds/dt)) / (ds/dt)²
```

where `d²s/dt² = y'·y'' / sqrt(1+y'²) = J_value·hessian_value / sqrt(1+J_value²)`. Compute `S1_s, S2_s`
per row. **Report both raw-t and arc-length channels.** The arc-length channel is the invariant
candidate; the raw-t channel is the diagnostic that shows how much of the cross-fixture story is
parametrization.

### 2.3 Lattice channel (the discrete / seam characterization)

The `ulp`-based observables jump at binade boundaries — those jumps are not noise, they are the
substrate's native resolution. Build the discrete second difference of the binade-quantized magnitude:

```
B(t)  = floor(log2(|base_operand(t)|))      # binade index of the operand
ΔB, Δ²B over the actual coordinate grid     # discrete (lattice) curvature analog
```

Do **not** smooth this. Report `Δ²B` alongside `S2_s`. Its role is §5.

---

## 3. Geometric target columns (from the existing table)

Per row, carry: `y = natural_function_value`, `y' = J_value`, `y'' = hessian_value`, `κ = principal_curvature`.
Also derive the geometric log-acceleration anchor `G2 = (2/ln2)·(y''/y − (y'/y)²)` for the direct
identity check (this is what `S2` *should* equal; the interesting test is §4, not this identity).

---

## 4. The universality test (replaces rank correlation)

For each candidate substrate channel `C ∈ {S2, S2_s}` and each geometric target `T ∈ {κ, y''}`:

### 4.1 Leave-one-fixture-out functional fit (the headline)

1. Fit a monotone 1-D map `C = f(T)` on the pooled rows of **two** fixtures (isotonic or low-order
   spline — no transcendence import; a piecewise-linear monotone fit is fine and substrate-legal).
2. Predict `C` on the **held-out third** fixture from its `T`.
3. Report median and 95th-percentile relative prediction error, per held-out fixture, all three folds.

**Verdict thresholds (pre-register exact numbers before running):**
- `PASS` (universal): all three folds predict within the **instrument noise floor** (set in §6 from the
  Phase-0 null), i.e. the map is fixture-agnostic.
- `FAIL` (fixture-bound): any fold exceeds the floor by the pre-registered margin.

This is immune to the coordinate tautology: two monotone functions of `t` always rank-correlate ±1, but
they need not obey the *same* `C = f(T)` law. The shared law is the content; the rank is not.

### 4.2 Matched-invariant agreement (the corrected version of the old test)

Bin rows by `T` (the geometric quantity), `≥ 10` rows/bin. Within each bin, compute the cross-fixture
spread of `C`. The old Phase-H test did this with `C = E` (0-jet) vs `T = κ` (2-jet) and got 0/5. Re-run
it with `C = S2_s` (2-jet) vs `T = κ`. Report the spread distribution; `PASS` if within the noise floor.

### 4.3 Which combination is native (the discovery output)

If `S2_s` vs `κ` does **not** collapse but `S2_s` vs `y''` (or `S2_s` vs `G2`) **does**, that is the
finding: the substrate's native invariant is the **log-acceleration of the operand**, not Euclidean
curvature κ — and κ is its cousin via the `(1+y'²)^{3/2}` Jacobian the substrate never sees. Report the
specific universal combination explicitly; it is the V4-native curvature observable.

---

## 5. Hypotheses (pre-register the null)

- **H_jet_geometry:** some substrate jet (`S2_s`, or a declared combination) is a universal function of
  a geometric jet across fixtures (§4.1 PASS). ⟹ the substrate carries a differential-geometric invariant.
- **H_zero_jet_only (NULL — pre-register as expected):** only `S0` (magnitude) is shared; `S2_s` is
  fixture-bound or noise. ⟹ the substrate carries operand magnitude, not curvature. Write the clean
  negative and pivot to §5-seam.
- **Seam characterization (always reported, never a loss):** the coordinate resolution at which the
  lattice channel `Δ²B` can no longer resolve `κ` — i.e. where the binade-quantized second difference
  goes flat or aliases. That resolution floor is the precise, *measurable* location where "the algebraic
  handle is lost": not in transcendence, but at the binade granularity of the substrate's own jet.

---

## 6. Controls and the Phase-0 instrument gate (build BEFORE any hypothesis run)

1. **SR constant-κ slice.** SR's κ is ~constant. If `S2_s` tracks κ, `S2_s` is ~constant on SR; if it
   varies with coordinate there, it is still partly position-encoding. Quantify the residual variation;
   it sets part of the noise floor.
2. **Pure-noise control.** Randomly permute the (coordinate ↔ fingerprint) pairing within each fixture
   and re-run §4.1. The universality test **must FAIL** on shuffled data. If it passes, the fit is
   over-flexible — reduce the map's degrees of freedom until the shuffle fails. This is the
   `wrong_clean_emit` guard: an instrument that confirms a permuted null is ringing on noise.
3. **Route-identity control.** Confirm the fingerprint is route-invariant (the four algebraic forms agree
   at each coordinate) before trusting any jet built from it. If forms disagree, the fingerprint is
   route-contaminated and §4 is void.
4. **Noise floor.** Define it as `max(SR-slice residual, shuffle-null 95th-percentile error)`. All §4
   verdicts are relative to this single declared floor. No per-test fudge.

Phase 0 is direction-agnostic: it earns a trustworthy instrument and a defined null before any
hypothesis runs. Gate it with `wrong_clean_emit` exactly as the spine campaign does.

---

## 7. Output / report contract

- Write to `Build_Docs/Reports/substrate_invariant_search/phase_a_substrate_jet_curvature.json`,
  byte-stable (`json.dumps(..., indent=2, sort_keys=True)`).
- Top-level: `audit_name`, `phase`, `campaign`, `authority` (the R1 successor doc), `preregistry` path,
  input sha256s (`phase_1_geometry_table.json` and this spec), `noise_floor`, the per-channel/per-target
  verdict table (§4.1, §4.2), the native-combination finding (§4.3), the seam resolution floor (§5),
  and the full per-row jet table (`S0,S1,S2,S1_s,S2_s,ΔB,Δ²B,y,y',y'',κ,G2,S2_fd_vs_anchor_residual`).
- Stability/near-degenerate rows segregated under a separate key, excluded from the verdict.
- Capture full stdout to a `console_log` field in the report dict (TeeStream pattern), with timestamp
  and every numerical verdict in the dict — nothing that matters lives only in the console.

---

## 8. Why this is the V4-native curvature extractor (the mission tie-in)

The end goal is rebuilding V3 on V4 substrate. V3's curvature/conditioning diagnostics are computational
quantities — they must be recoverable from substrate behavior, not imported. This phase delivers exactly
that: a validated map **(substrate jet) → (geometric quantity)**, cross-fixture. Two outcomes, both
useful:

- If `S2_s` is universal against `κ`: the substrate carries curvature directly; V3's curvature extractor
  rebuilds as "second arc-length derivative of operand log-magnitude." Done.
- If the universal combination is `S2_s` vs `y''`/`G2` instead: the substrate's native curvature is the
  operand log-acceleration, and continuum κ is its image under a Jacobian the bits don't see. V3's
  diagnostics get re-expressed in the substrate's *own* invariant — which is the whole point of a
  V4-native rebuild rather than a κ wrapper (and the Axiom-11/12-clean form: derive the invariant from
  substrate primitives, then show where standard κ is its continuum shadow).

The binade resolution floor (§5) tells the rebuild where the extractor's honest precision ends — the
typed refusal boundary for the curvature observable, in the same spirit as the P2 budget seam.

---

## 9. Pre-registration checklist (sign before first run)

- [ ] R1 successor authority written; this phase cites it.
- [ ] Exact §4 verdict thresholds and the §6 noise-floor formula committed in the preregistry doc.
- [ ] Phase-0 controls (1–4) built and the shuffle-null confirmed to FAIL the universality test.
- [ ] `S2` FD-vs-anchor residual check wired (metrology, not hidden).
- [ ] Stability/near-degenerate segregation in place.
- [ ] No `lv3`, no symbolic backend, byte-stable JSON, input sha256s recorded.
