# Shape of the Quiet — Phase 2 Wiring Addendum (pre-registered, committed BEFORE any sweep)

The frozen manifest (pin `9a1d7ec6…`) anticipated exactly this addendum: details that
could only be pinned against live tool probes and code-level signatures. Everything
below is fixed BEFORE the first sweep execution and is not tuned afterwards. The
manifest itself is untouched (the freeze gate enforces that).

## I2 — V3 oracle, pinned fields (probes 2026-06-10)

- **F1(a) comparator:** `lv3_diagnose` → `K_G` (the single principal curvature for the
  1D-in-2D surface). Validity: `trust == 1.0` and empty `refusal_reasons`. `F_val`,
  `gradient_magnitude`, `pathology` recorded verbatim per rung.
- **F1(b): the V3 MCP surface exposes NO Hessian-eigenvalue diagnostic.** Probe:
  `lv3_observe_full` on `1 - 2*M/r - z*z` at r=10, full-tree key scan for
  eig/hess/spectr/lambda → empty; only `diagnostic.metadata.principal_curvatures`
  (2 values, n=3) exists. Pinned consequence: per rung, I2 records
  `refusal_kind = "oracle_quantity_unavailable"` for the −2-eigenvalue quantity;
  `K_G`, `principal_curvatures`, `trust` recorded verbatim as NEIGHBOUR data, never
  scored against −2. (First-class result: V3-via-MCP cannot read the form-borne
  invariant directly.)
- **F2 (ζ/J₀/Ai):** `refusal_kind = "oracle_inexpressible"` per rung (compiler
  allowlist probe in the manifest).
- **F2c (sin):** per-rung `lv3_branch_classify`, `equation = "sin(x) - y"`,
  `branch_point = {"x": "x", "y": 0.0}`, `sweep_index = 0`, `boundary_value = x0`,
  `approach_range = [x0 + 16*d_k, x0 + d_k]`, `n_points = 10` (schema minimum).
  Comparator field = `alpha`. Validity: `stability == "stable"`. Full response
  recorded verbatim.

## I3 — V4 typed probe, pinned constructions

- **F1(a):** `reconstruct_kappa_from_substrate("schwarzschild_four_form", r_k)` from
  the committed Phase A fd-metrology module (HR129), with its declared plateau gate
  and `fd_operand_variation` guard: guard value > 0.5 ⇒ rung recorded as typed
  `fd_unresolved` refusal (the Phase A boundary-row convention), never an estimate.
- **F1(b):** central second difference of F along z at the operating point:
  `H_zz ≈ (F(z+h) − 2·F(z) + F(z−h)) / h²` with `h = 2**(floor(log2|z|) − 6)`
  (exact power of two, 6 bits below z's binade). Rationale: the z-block is exactly
  quadratic, so truncation error is identically zero; the rounding budget is
  ~2⁻⁴⁰ ≪ tol 1e-9. Refusal when z == 0 (horizon rung). `typed_ulp` grain of z and
  of F recorded per rung.
- **F2 / F2c (σ1):** transfer-law estimator: at window points d_j = d_k·2^j (j=0..4),
  `typed_finite_difference(g=|f(x0+·)|, f=d_j, delta_f=d_j/16)`; collection →
  `typed_log_log_slope`; **σ1 = slope + 1** (exact identity for power laws,
  T ~ |αc|·f^(α−1), glossary transfer law). Method gap vs the direct estimator is
  inside the pre-registered 0.01 tol (ledger retest B ≤ 0.0033). Typed statuses
  recorded; SLOPE status ≠ OBSERVED ⇒ typed refusal for the rung.
- **F2/F2c I3 channel rule (exponent quantities — the manifest ratio rule is for
  value-like quantities; this pins the exponent mapping):**
  - `phenomenon`: SLOPE_OBSERVED ∧ all 5 transfer cells TRANSFER_OBSERVED ∧
    slope `standard_error` ≤ tol (0.01)
  - `substrate`: ≥3 transfer cells cancellation-dominated / non-finite, or slope
    degenerate by zero variance (the window reads lattice, not function)
  - `format_precision_pinned`: any window |f| < 2⁻¹⁰²¹ (c2-theorem scope-gate floor)
  - `ambiguous`: everything else
  - **AMENDMENT (pre-execution, 2026-06-10, before any sweep ran):** the originally
    drafted `phenomenon` gate included `r² ≥ 0.99`. Live smoke on the sin zero showed
    that gate is shape-inappropriate: for σ1 ≈ 1 the transfer is nearly CONSTANT, so
    the log-log fit's r² is structurally low (0.70 on a reading good to 4e-5) — r²
    measures variance explained, which vanishes as the slope flattens. Replaced by
    the slope `standard_error ≤ tol` gate BEFORE first execution. `cancellation_grade
    = 1 − r²` (glossary) remains a screen for full-sweep power-law fits, not
    near-flat transfers. No sweep data existed when this was amended.
- **F1 I3 channel rule (value quantities, manifest literal):** signal_ratio =
  |reading| / (max ulp(operand values touched by the FD)/2), thresholds 1e3 / 1;
  `format_precision_pinned` when |base_operand| < 1e-4 (glossary E-unsafe), which on
  F1's ladder means δ-deep rungs — exactly ruling 3's regime, arbiter referees.

## I1 — naive float64, pinned operation order

- **F1(a):** `z = math.sqrt(1-2/r); zp = (1/r**2)/z; zpp = (-2/r**3)/z - (1/r**4)/z**3;
  kappa = abs(zpp)/(1+zp*zp)**1.5` — evaluated at (r_k, on-the-fly z), no guards.
- **F1(b):** `numpy.linalg.eigvalsh` of the float64 3×3 Hessian
  `[[-4M/r³, 0, 2/r²], [0, −2, 0], [2/r², 0, 0]]`; comparator = eigenvalue nearest −2.
- **F2/F2c:** `numpy.polyfit(log10 d_eff, log10|f|, 1)[0]` over the 5 window points;
  validity = all |f| finite and nonzero. Evaluators: ζ `complex(mpmath.zeta(0.5+1j·x))`
  → float64 (manifest caveat); J₀ `scipy.special.j0`; Ai `scipy.special.airy(x)[0]`;
  sin `math.sin`.

## Arbiter — pinned procedures

- **F1(a):** κ closed form in mpmath at the exact binary r_k; dps 50, +10 escalation
  until successive values agree within tol/10 (manifest).
- **F1(b):** `mpmath.eigsy` of the exact Hessian at exact binary (r_k, z_k, M=1);
  comparator = eigenvalue nearest −2 (analytically exactly −2: the decoupled z-block).
- **F2/F2c:** exact OLS slope of (ln d, ln|f|) at the exact binary window points,
  mpmath values, dps escalation as above; refined-locus annotation: zeros recomputed
  via `mpmath.zetazero / besseljzero / airyaizero / k·pi`, and σ1 against the true
  locus recorded as annotation (not the scored comparator).
- **Ground classification (manifest rule):** Δq_ulp computed by shifting the rung's
  primary input by exactly 1 ulp (F1: r_k; F2: the anchor x_k = fl64(x0)+d-window
  shifted by 1 ulp of x0) and recomputing q_true.

## AMENDMENT 2 (pre-execution, 2026-06-10, before any recorded sweep)

The thin smoke slice (no campaign records written) exposed an estimator-method
offset: I3's transfer-route σ1 responds to window curvature at exactly 2× the
direct window slope (derivation: for |f| = c·d·(1+a·d), direct ≈ 1 + a·d̄ while
transfer T = |f'| gives 1 + 2a·d̄; confirmed numerically on J₀ zero 1 at k=2:
direct 0.9881, transfer-route 0.9740). This is a DEFINITIONAL property of the
pre-registered estimator, not substrate noise — grading I3 against the direct
quantity would charge the typed instrument a definitional offset and corrupt the
depth measurement the campaign exists to make.

Pinned resolution (dual arbiter, both recorded per rung — ruling 3 satisfied):
- `arbiter.value` (σ1_direct_true) stays the manifest quantity — comparator for
  I1 and I2, and the basis of the ground classification. UNCHANGED.
- `arbiter.transfer_estimator_true`: the EXACT-arithmetic value of I3's own
  pre-registered estimator — mpmath function values at the SAME binary sample
  points the typed primitive touches (x1 = fl64(x0+d_j), x2 = fl64(x0 + fl64(d_j
  + fl64(d_j/16)))), same forward-difference quotient, same OLS, σ1 = slope + 1.
  This is I3's trustworthiness comparator: departure from it isolates substrate
  contamination of the reading from the estimator's definitional curvature
  response.
- I3 records BOTH signed errors (`error` vs its own ideal; `error_vs_direct` vs
  the manifest quantity). The figure and report disclose the dual grading.
- I1's ideal is already σ1_direct_true (identical definition, same points), so
  I1's grading is unchanged and symmetric.

## Source audit (Acceptance Criterion 7), pinned command

`PYTHONPATH=src python -m pytest tests/test_source_purity.py` (substrate gate) AND
`grep -nE "math\.(log|log2|exp|sin|cos)" src/lloyd_v4/evals/shape_of_the_quiet_sweep.py`
must show raw transcendental use ONLY inside the I1 instrument functions (whose whole
point is to be naive) and the pre-registered Phase A extractor calls — never in I3's
reading path beyond those modules, and never in the comparison/attribution layer.
