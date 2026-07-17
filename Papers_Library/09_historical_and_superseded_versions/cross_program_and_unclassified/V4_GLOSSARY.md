# V4 Glossary & Concept Index

**Purpose:** A consult-anytime reference for what exists in V4 — concepts, primitives, theorems, observables, mechanisms. Each entry is short by design: one-line summary + status + path to the primary source. Read it mid-session whenever you need to check you haven't drifted or misremembered.

**Last updated:** 2026-05-26

---

## How to use this file

- **Mid-session lookup:** use the alphabetical jump-list below if you know the term.
- **Browsing / orientation:** use the categorical sections (§1–§13).
- **Confused between two things:** check §13 "Things commonly confused."
- **Status legend:** *Proven* = derived from axioms with empirical verification. *Empirical* = large-N observed, no derivation yet. *Partial* = working but scope-limited or research-grade. *Open* = not yet addressed. *Retired* = considered and dropped.
- **Don't bloat this file.** Each entry is one line + source. For depth, follow the cited path.

---

## Alphabetical jump-list

A: [α (alpha)](#alpha-exponent) · [AlphaProbe](#alphaprobe) · [Axioms 1–12](#1-axioms-the-12-operational-digest)
B: [BACL](#bacl-binade-aligned-cancellation-lattice) · [b_k](#b_k-arithmetic-path-conditioning-amplitude) · [BranchFingerprint](#branchfingerprint) · [Blowup exponent (σ₁)](#blowup-exponent-σ₁)
C: [Calibrated primitive](#calibrated-primitive) · [Campaign discipline](#campaign-discipline) · [Cancellation_dominated](#cancellation_dominated-status) · [`cancellation_grade`](#cancellation_grade) · [C-extractor (E)](#e--log_2basebackslashoperand-c-extractor) · [Conjecture C](#conjecture-c) · [c2 lattice theorem](#c2-lattice-theorem) · [c2 scope gate](#c2-theorem-scope-gate) · [Comb / doubled comb](#comb--doubled-comb--half-grid)
D: [Decision-law](#decision-law-l3-refinery-mvp) · [`directional_alpha_probe`](#directional_alpha_probe-task-018) · [`drop_rate`](#drop_rate) · [Dual-arm probe](#dual-arm-probe-hardened-v1) · [Dual-arm 6-condition rule](#dual-arm-6-condition-resolution-rule)
E: [E (log₂(|base_operand|))](#e--log_2basebackslashoperand-c-extractor) · [`equation_refinery`](#equation_refinery-task-007) · [`exact_quadratic_projection`](#exact_quadratic_projection)
F: [F1 / F2 / F3 / F4](#f1--f2--f3--f4-four-form-battery) · [F5+ candidates](#f5-candidates) · [F1 ∥ F2 polarity coupling](#f1--f2-grid-stable-parallel-polarity-coupling) · [Fixtures (four-form)](#7-fixtures) · [Fold-readback probe](#fold-readback-probe-v10v11-superseded) · [Format_precision_pinned](#format_precision_pinned-attribution)
G: [Gap_resolved](#gap_resolved-dual-arm-verdict) · [G (geometric content)](#g-geometric-content) · [Geometry-first reframe](#geometry-first-reframe)
H: [Hard cell](#hard-cell--zero-offset-hard-cell) · [Hardened dual-arm probe V1](#dual-arm-probe-hardened-v1) · [Half-grid](#comb--doubled-comb--half-grid)
I: [Identity zero vs below-LoD](#axiom-6-zero-must-be-measured-or-proven)
J: [JetBundle](#jetbundle--scalar_alpha_jet_bundle)
K: [K_G](#k_g-canonical-gaussian-curvature) · [K_q](#k_q-proxy-calibration)
L: [Layer architecture](#3-layer-architecture) · [Lattice grain (integer / non-integer / empty)](#lattice-grain) · [Lifted singularity](#lifted-singularity-construction)
M: [MCG decomposition](#mcg-decomposition--r--m-oplus-c-oplus-g) · [M (substrate-mandated)](#m-substrate-mandated) · [`max_integer_residual`](#burden-vector-components)
N: [Noise floor (`b_k`)](#b_k-noise-floor-l2-metrology)
O: [Observability rule F4 (e_f < e_x)](#observability-rule-f4-e_f--e_x) · [Offset guard](#operand-offset-guard) · [Operand offset / path separation](#operand-offset--path-separation)
P: [Path separation](#operand-offset--path-separation) · [Polarity coupling](#f1--f2-grid-stable-parallel-polarity-coupling) · [`ProjectionBranch`](#projectionbranch) · [`projective_ratio`](#projective_ratio) · [Precision-scaling separation (Theorem 3)](#precision-scaling-separation-theorem-3) · [`propagated_window_error`](#propagated_window_error)
Q: [Q1–Q6 (original questions)](#original-questions-q1q6-status)
R: [Reference hygiene](#reference-hygiene-v3--vera) · [Refinery MVP (Task 030)](#decision-law-l3-refinery-mvp) · [Route / route bank](#route--route-bank) · [`RefineryStatus`](#refinerystatus-8-strata)
S: [Sterbenz boundary](#sterbenz-boundary) · [Sterbenz lemma](#sterbenz-lemma) · [`StatusTransitionRule`](#status-families-10) · [Status families](#status-families-10) · [`StratifiedQuadraticRoots`](#stratified_quadratic_roots) · [Sub-lattice alignment](#sub-lattice-alignment-task-031) · [Substrate fingerprint atlas](#substrate-fingerprint-atlas-closed-absorbed) · [substrate-invariant-search](#substrate-invariant-search-active) · [substrate-as-probe StructuredReading](#substrate-as-probe-structuredreading-4-channel) · [`sweep_signature_probe`](#sweep_signature_probe-task-035) · [`SweepSignatureStatus`](#sweepsignaturestatus) · [`SweepSignatureValue`](#sweepsignaturevalue) · [companion call pattern](#companion-call-pattern-task-036-canonical-example) · [companion_sweep_signature_* fields](#companion_sweep_signature_observation--_status--_trace_id)
T: [Transfer law (Theorem 1)](#transfer-law-robust-branch-theorem-1) · [Transfer-function-exponent-family](#transfer-function-exponent-family) · [`typed_finite_difference`](#typed_finite_difference-task-015) · [`typed_log_log_slope`](#typed_log_log_slope-task-016) · [TypedResult](#typedresult) · [Two-form partition](#two-form-partition)
U: [`ulp_spread_log2`](#ulp_spread_log2)
V: [V3 reference rule (Axiom 10)](#axiom-10-v3-is-reference-evidence-only) · [Vera unification](#vera-strip-and-replicate-protocol)
W: [`wrong_clean_emit_count`](#wrong_clean_emit_count-master-audit-metric)

---

## 1. Axioms (the 12, operational digest)

Authoritative: [Architecture/AXIOMS.md](Architecture/AXIOMS.md). One-line paraphrases (not citations).

1. **Geometry precedes scalarization** — typed objects first; scalars only when D/S/V/C/Pr/Pt permit.
2. **Degeneracy is a stratum** — not a failure or exception.
3. **No hidden guard rails** — every rescue, clamp, tolerance is declared.
4. **Validity is multi-field** — defined / finite / selectable / advanceable / observable / policy-accepted are distinct.
5. **Numerical representation is a path** — precision, backend, expression-path are observation metadata, not the object.
6. **Zero must be measured or proven** — `identity_zero ≠ below_limit_of_detection ≠ indeterminate ≠ detected_nonzero`.
7. **Proxy observables require calibration** — `K_q` etc.
8. **Typed results compose by protocols** — producer + consumer + accepted-status-set explicit.
9. **Type-system failures are real failures** — false type stickers worse than untyped failure.
10. **V3 is reference evidence only** — no imports, calls, adapters, bridges.
11. **Epistemic Stance Only** — no `math` / `numpy.special` / `mpmath` as substrate; no hardcoded constants; named theorems are domain articulations, not substrate.
12. **Self-Derivation** — every layer derives from parent layers via registered transitions.

---

## 2. Theorems and Proven Lemmas

### BACL (Binade-Aligned Cancellation Lattice)
For positive floats `a, b` with `ulp(a) ≥ ulp(b)`, `a − b = j · ulp(b)` for integer `j`. **Status:** *Proven* from IEEE 754 binade-spacing (5-line proof). Unified across float16, float32, float64, normal + subnormal. 31,000+ records, zero violations.
See: [Reports/bacl_invariant_audit/](Reports/bacl_invariant_audit/), [Reports/bacl_multi_format_audit/](Reports/bacl_multi_format_audit/), [Reports/bacl_subnormal_audit/](Reports/bacl_subnormal_audit/).

### Conjecture C
For `f ∈ [2^k, 2^(k+1))` in float64 normal range and `R = round(sqrt(f))`, `round(R · R) ≥ 2^k`. **Status:** *Proven* for sqrt in float64 normal range. 220,444 checks, zero violations. **Frozen open:** C_subnormal, C_3, C_4, C_5.
See: [Reports/conjecture_c_proof_audit/](Reports/conjecture_c_proof_audit/).

### c2 lattice theorem
c2 routing `round(V_2 + (x_term − 1))` produces integer-multiples of `ulp(f_float)` in float64 normal range. Sqrt-specific corollary: `|j| ≤ 1`. **Status:** *Proven* conditional on Conjecture C. 90,000 records, zero violations.
See: [Reports/c2_lattice_substrate_derivation/](Reports/c2_lattice_substrate_derivation/), [Reports/c2_lattice_sharpness_audit/](Reports/c2_lattice_sharpness_audit/).

### c2 theorem scope gate
All 14 V4 campaign grids keep `min(f_float) ≥ 968 binades above 2^(−1021)`. Methodology discipline: future fixtures must pass this gate or supply separate subnormal verification.
See: [Reports/c2_theorem_scope_gate/](Reports/c2_theorem_scope_gate/).

### Transfer law (robust branch, Theorem 1)
`T_{δf}(f) ∼ |αc| f^(α−1) L(f)` as `f → 0+`, given controlled branch expansion with `δf/f → 0`. Limiting log-log slope is `α − 1`. **Status:** *Proven* (chain rule + controlled asymptotics). V4 synthetic validation slope error ~1e-11 across α ∈ {0.5, 1.5, 2.0, 3.0}.
See: [transfer_function_exponent_family_v4.tex](transfer_function_exponent_family_v4.tex) Thm 1, §3, §6.

### Precision-scaling separation (Theorem 3)
`C_{p,k} = a + u_p b_k` where `a` is path-invariant geometric amplitude and `b_k` is path-dependent conditioning amplitude. Identifiable by multi-precision linear fit. **Status:** *Proven*; empirically validated R²=1.0 across all four fixtures × paths in the regular region. **Open:** three sub-claims (cbrt F1 intercept at sub-precision-floor; F1/F2 slope distinguishability; Sterbenz-region b_k structure).
See: [transfer_function_exponent_family_v4.tex](transfer_function_exponent_family_v4.tex) Thm 3 + §6; Task 017c.

### Sterbenz lemma (classical, restated for V4 context)
For IEEE 754 floats `a, b` same precision with `a/2 ≤ b ≤ 2a`, `a − b` is computed exactly. Predicts the **Sterbenz boundary** in V4 fixtures.
See: [transfer_function_exponent_family_v4.tex](transfer_function_exponent_family_v4.tex) §7.

### Cross-fixture invariance (Theorem 4 in paper)
Five classification-level invariants preserved across Schwarzschild, SR, pure_algebraic, cbrt: F3 silence, F2 non-integer lattice, F4 integer lattice, F1 ∥ F2 grid-stable polarity coupling, Sterbenz directional bias. **Status:** *Empirical invariance statement*, not a derived theorem.
See: [transfer_function_exponent_family_v4.tex](transfer_function_exponent_family_v4.tex) §6 Thm 4; Tasks 028, 029c.

### Lifted singularity structural invariants
For K simultaneous constraints F_joint = ΣF_i² − X²: rank K+1, signature (K positive, 1 negative), H_XX = −2. **Status:** *Structural* (true by construction); the **empirical** finding is null-tangent alignment with family tangent at `|cos θ| = 1.0000` across 6 fixtures + Kerr spin 0.1–0.99.
See: [Reports/lifted_singularity_v4_audit/](Reports/lifted_singularity_v4_audit/).

### Blowup exponent (σ₁)
At linearization order, `σ₁ = 1.000` universally across 15 simple zeros of ζ, J₀, Ai. **Status:** *Empirical* structural sanity check. Higher-order signatures (σ₃, σ₄) inconclusive at audit depth.
See: [Reports/blowup_exponent_v4_audit/](Reports/blowup_exponent_v4_audit/).

---

## 3. Layer Architecture

Authoritative: [Architecture/LAYER_MANIFEST.md](Architecture/LAYER_MANIFEST.md), [Architecture/layer_manifest.json](Architecture/layer_manifest.json).

| Layer | Holds | Status |
|---|---|---|
| **L0 Core** | `TypedResult`, `Status` (46 statuses / 10 families), `Provenance`, `Protocol`, `StatusTransitionRule` | Complete |
| **L1 Primitives** | 10 primitives (see §4) | Complete |
| **L1.5 Projection** | `exact_quadratic_projection`, `ProjectionBranch`, branch selection | Complete |
| **L2 Metrology / Branch** | `b_k` noise floor, `K_q` proxy, limit-of-detection, `BranchFingerprint`, transfer observables | Complete; **operationally authoritative** |
| **L3a Refinery / History** | `equation_refinery`, `snapshot_typed_result`, `RefineryStatus`, `StatusTrace` | Partial; **not authoritative** |
| **L3b Solver** | `TypedProjectionSolver`, `SolverPolicy`, `SolverStatus` | Partial; **not authoritative** |

L3 promotion gates: see [LIVE_CAMPAIGNS_LEDGER.md → `layer-3-promotion`](LIVE_CAMPAIGNS_LEDGER.md#layer-3-promotion).

---

## 4. Primitives (by layer)

### L1 calibrated primitives (10)

#### `projective_ratio`
`ProjectiveRatio(n, d)` with 6 strata (finite_ratio, signed_zero, infinite_direction, indeterminate, refusal, invalid). Scalarization enforces typed refusal for non-finite strata. **Source:** Task 001.

#### `stratified_quadratic_roots`
`StratifiedQuadraticRoots(a, b, c)` with 6 root strata. Branch-selected via `select_quadratic_root()`. **Source:** Task 002.

#### `typed_collection`
Boundary primitive for typed sequences. **Source:** Task 010-Sub-A.

#### `typed_value`
Boundary primitive for raw single values. **Source:** Task 010-Sub-B.

#### `typed_finite_difference` (Task 015)
Computes `T_{δf}(f) = |Δ_{δf}g(f) / δf|` as typed observation. 5 strata: `transfer_observed`, `transfer_cancellation_dominated`, `transfer_non_finite`, `transfer_domain_refused`, `transfer_delta_indeterminate`.

#### `typed_log_log_slope` (Task 016)
Fits log-log slope of typed transfer collection. Returns slope as typed observable with provenance lineage to constituent transfer observations.

#### `directional_alpha_probe` (Task 018)
Samples grid, measures α via log-log slope. 9 strata covering regular integer / fractional branch / singularity / model ambiguity / cancellation / domain refusal / non-finite / indeterminate. Added in Task 023b: `alpha_zero_boundary`, `alpha_unstable_window`.

#### `sweep_signature_probe` (Task 035)
Composes `typed_finite_difference` and `typed_log_log_slope` into a low-sensitivity sweep screening signature. Emits `SweepSignatureValue` with `cancellation_grade`, `drop_rate`, transfer counts, and a nested slope observation.

#### `scalar_alpha_jet_bundle` (Task 019)
Shifts `g` to `g_local(h) = g(x0+h) − g(x0)`, delegates to `directional_alpha_probe`. **Asymmetry:** local additive construction tends to zero as `h → 0+` when `f(x0)` finite; negative-α at branch requires `singular_alpha_jet_bundle` instead.

#### `singular_alpha_jet_bundle` (Task 021)
Sibling probe to `scalar_alpha_jet_bundle` for singular-direct case (`g_singular(h) = f(x0+h)` without subtraction). Observes singular region where `|f(x0+h)|` blows up.

### L1.5 projection

#### `exact_quadratic_projection`
Consumes typed root-state, enforces protocol, emits projection evidence. Source root-state, branch, selected root, projection status (transverse / tangent_contact / linear / no_real_root / identity / no_solution / selection_refused). **Source:** Task 003, rebuilt Task 010.

#### `ProjectionBranch`
Typed branch object (positive / negative / unique) replacing raw-string flags. **Source:** Task 010 rebuild.

### L2 metrology / branch

#### `b_k` noise floor (L2 metrology)
Declared / estimated / classified. Strata: detection / below_limit / indeterminate. **Source:** Task 004.
**Distinct from** `b_k` arithmetic-path conditioning amplitude in Theorem 3.

#### `K_q` proxy calibration
Proxy evidence via `ProjectiveRatio` scalarization. Required by Axiom 7. **Source:** Task 004.

#### `BranchFingerprint`
Transfer-flow slope comparison, model-residual bands, `K_q` slope stability. **Evidence only**; does not classify domain branch. **Source:** Task 006.

### L3 (partial, non-authoritative)

#### `equation_refinery` (Task 007)
Compares snapshots componentwise. 8 `RefineryStatus` strata: slag (lower / upper / internal / identity), indeterminate, refusal, comparison-refused, protocol-refused.

#### `RefineryStatus` (8 strata)
See above.

#### `StatusTrace` / `HistoryEvent` (Task 008)
Compact status-transition recording across TypedResult chain.

#### `TypedProjectionSolver` (Task 009)
Domain consumer. 11 `SolverStatus` strata. **Not authoritative** — reference-only until L3 promotion gates close.

---

## 5. Status Families (10)

Authoritative: [Architecture/STATUS_CALCULUS.md](Architecture/STATUS_CALCULUS.md).

46 statuses across 10 families. Named `StatusTransitionRule` registry maps between families. Key strata:

- `transfer_observed`, `transfer_cancellation_dominated` (L1 transfer)
- `alpha_regular_integer`, `alpha_fractional_branch`, `alpha_negative_singularity`, `alpha_cancellation_dominated`, `alpha_insufficient_data`, `alpha_domain_refused`, `alpha_zero_boundary`, `alpha_unstable_window` (AlphaProbe)
- `sweep_signature_clean`, `sweep_signature_cancellation_dominated`, `sweep_signature_high_drop_rate`, `sweep_signature_degenerate_input` (SweepSignature)
- `slope_observed` (log-log slope)
- `RefineryStatus.*` (L3a)
- `SolverStatus.*` (L3b)

Detail and transition map in `STATUS_CALCULUS.md`.

---

## 6. Active Campaigns (see ledger)

Cross-reference only. Authoritative status: [LIVE_CAMPAIGNS_LEDGER.md](LIVE_CAMPAIGNS_LEDGER.md).

- `substrate-invariant-search` (active)
- `alpha-minus-one-exhaustion` (active, behind on phases)
- `hardened-dual-arm-probe` (V1 complete; v11 control-silence fix pending)
- `layer-3-promotion` (gates 2 + 3 open)
- `vera-unification` (most replications in design status)
- `paper-hardening` (active)

---

## 7. Fixtures

The four-form battery is evaluated on these fixtures. Each has its own Sterbenz boundary at the canonical native variable.

| Fixture | Form | Sweep | Sterbenz boundary | Radical | Source |
|---|---|---|---|---|---|
| Schwarzschild radial | `f = 1 − 2/r` | `r ∈ [2.005, 10.0]`, 137 points | `r = 4.0` | sqrt | Task 024b |
| SR time dilation | `f = 1 − β²` | `β ∈ [0.01, 0.9999]`, 137 points | `β = 1/√2` | sqrt | Task 027 |
| Pure algebraic | `f = 1 − x` | `x ∈ [0.01, 0.99]`, 137 points | `x = 0.5` | sqrt | Task 028 |
| Cube-root algebraic | `f = 1 − x`, n=3 | `x ∈ [0.01, 0.99]`, 137 points | `x = 0.5` | cbrt | Task 029c |
| Sphere multi-D | unit sphere | probe-based | n/a | n/a | substrate_invariant_search Phases B–E |
| Lifted singularity (Morris-Thorne, Kerr ISCO etc.) | K simultaneous constraints + F_joint | varies | n/a | n/a | [Reports/lifted_singularity_v4_audit/](Reports/lifted_singularity_v4_audit/) |

---

## 8. Key Observables and Forms

### F1 / F2 / F3 / F4 (four-form battery)

Algebraically zero on the constraint surface by construction. Non-zero values are arithmetic-path residuals.

- `F1 := R² − f_direct` (direct ratio precomputed) — F1 form
- `F2 := R² − 1 + x_term` (split addition; `x_term = 2/r, β², x`) — F2 form, the workhorse
- `F3 := R − √f_direct` (same path twice; calibration zero) — **identically zero everywhere**
- `F4 := R − √f_alt` (alternative factored routing) — F4 form

Cross-fixture status: see Theorem 4 in paper. Lattice classifications:
- F1: depolarized lattice
- F2: **non-integer lattice grain** (half-level in Schw/SR; quarter-integer in PA/cbrt)
- F3: identity silence
- F4: **integer lattice character**

### F5+ candidates
Path-basis rewrite candidates that survive single-linkage clustering at cut=0.10 outside the F1–F4 clusters. **Universal across radical degrees:** `P_compound_split`, `P_sign_c`. **Fixture-specific:** `P_distrib_sqrt_mul` (sqrt only), `P_compound_zero` (SR only), `P_factor_b` (PA only), `P_distrib_mul` (SR only), `P_sign_a` (SR only). **Retired as artifact:** `P_scaled_2`, `P_scaled_half` (Decimal ROUND_HALF_EVEN artifacts).
See: Tasks 029, 029b, 029c.

### F1 ∥ F2 grid-stable parallel polarity coupling
Where both F1 and F2 fire on the same cell, their signs agree with 100% frequency across all four perturbation grids tested per fixture. p < 1e-10. **Status:** *Empirical*, universal across 4 fixtures.
See: Tasks 026c-prime, 028, 029c.

### K_G (canonical Gaussian curvature)
2-variable case: `K_G = det(H_b_3x3) / |∇F|³`. 3-variable case: `K_G = −det(H_b_4x4) / |∇F|⁴`. Sign convention matches V3 oracle. **Status:** *Eval-layer only* in V4 (imported from Goldman 2005); substrate-derivation (Phase E Path A) failed. Sphere sanity check: max deviation 2.22e-16 (1 ulp).
See: substrate_invariant_search Phase E.

### E = log₂(|base_operand|) (C-extractor)
Operationally validated 1D C-extractor. Threshold cluster at Sterbenz boundary. **Status:** *Empirical, operationally validated 1D*. **Phase H finding:** E is K_G's within-fixture rank cousin at Spearman ρ = −1.0000 in Schwarzschild and pure_algebraic; fixture-bound (relationship breaks across fixtures at matched K_G). E **fails T2 format-invariance** at near-singular coordinates (when |base_operand| approaches float32 precision floor).
See: mcg_geometry_first Phase 2g; substrate_invariant_search Phase H.

### `ulp_spread_log2`
`log2(max_ulp / min_ulp)` across operand chain. Reforms BACL from constant to discriminating. **Status:** First element of irreducible substrate-invariant basis. Survives all three transformations in Phase D audit.
See: substrate_invariant_search Phase C, D.

### two-form partition
Algebraic-form structural invariant (silent vs residual-carrying per route). Third element of irreducible substrate-invariant basis. Survives all three transformations.
See: substrate_invariant_search Phase C, D.

### `b_k` (arithmetic-path conditioning amplitude)
Path-dependent slope in Theorem 3's `C_{p,k} = a + u_p b_k`. Identifiable by multi-precision linear fit. **In Sterbenz region: larger upper-CI than in regular region across all four fixtures** (paper §6 table) — Q5 remains hardest in the boundary regime.
**Distinct from** `b_k` noise floor in L2 metrology (same letter, different concept).
See: Task 017c; paper §6.

### `a` (path-invariant geometric amplitude)
Intercept in `C_{p,k} = a + u_p b_k`. The geometric component separable from `b_k` by precision-scaling.

### `T_{δf}` (transfer observable)
`T_{δf}(f) = |Δ_{δf}g(f) / δf|`. The observable being fitted in V4 direct validation (no `|λ_max|` proxy needed). Limit `T_{δf}(f) ∼ |αc| f^(α−1) L(f)`.
See: `typed_finite_difference` primitive; paper §4.

### `cancellation_grade`
Task 035 sweep-screening signal `1 - r_squared`, where `r_squared` comes from the composed `LogLogSlopeObservation`. High values indicate that a full-sweep power-law fit is poor enough to be treated as cancellation-dominated under `CANCELLATION_GRADE_THRESHOLD`.
See: `sweep_signature_probe`.

### `drop_rate`
Task 035 sweep-screening signal: fraction of transfer cells that did not emit `transfer_observed` (`transfer_cancellation_dominated`, `transfer_non_finite`, `transfer_domain_refused`, or `transfer_delta_indeterminate`). High values emit `sweep_signature_high_drop_rate` under `DROP_RATE_THRESHOLD`.
See: `sweep_signature_probe`.

### blowup exponent (σ₁)
At linearization order, σ₁ = 1.000 universally. See §2.

### BACL grain (`max_ulp / 2`)
Substrate-mandated noise floor predicted from operand chain. Used in substrate-as-probe `signal_ratio = |K_G| / bacl_predicted_noise_floor`.

### lattice grain
The spacing of the residual lattice. Three classifications: `lattice_integer`, `non_integer_lattice` (half-level or quarter-integer), `lattice_empty`. Per-fixture, per-form characterisation. F2: non-integer. F4: integer. F1/F3: empty in calibration-zero cases.

### `max_integer_residual`
Maximum integer residual (in ulp units) across the sweep. Burden vector component used in refinery Pareto comparison.

---

## 9. Probes and Instruments

### AlphaProbe (Task 018, `directional_alpha_probe`)
The primary V4 instrument for measuring `α` at a probe point. Composes finite-difference + log-log slope + typed-stratum classifier. Recovers α to ~1e-10 precision on clean cases; refuses cleanly on cancellation-dominated data.

### SweepSignatureValue
Structured Task 035 primitive value containing `cancellation_grade`, `drop_rate`, the nested `LogLogSlopeObservation`, transfer-count cells, and the expression path. It is observable-level screening evidence, not a refinery campaign aggregate.
See: `sweep_signature_probe`.

### companion call pattern (Task 036 canonical example)
One primitive (the caller) optionally invokes a sibling primitive at the same layer and attaches the typed result as informational fields (never mutating the caller's primary status or validity). The callee's trace ID is recorded in the caller's provenance parents. Consumers compose the pair; no `StatusTransitionRule` or combined enum is introduced. Task 036 (`directional_alpha_probe` + `sweep_signature_probe`) is the reference implementation. The three attached fields are `companion_sweep_signature_observation`, `companion_sweep_signature_status`, `companion_sweep_signature_trace_id`.

### companion_sweep_signature_observation / _status / _trace_id
Optional fields on `AlphaProbeObservation` (populated only when `directional_alpha_probe(..., companion_sweep_signature=True)`). Carry the full `SweepSignatureValue`, its `SweepSignatureStatus`, and the companion's provenance trace ID. All three are jointly None or jointly populated (enforced in `__post_init__`). Informational only; do not affect `AlphaProbeStatus` or scalarization. Enables consumers to distinguish formulation-burdened vs structurally-unstable interpretations of `alpha_unstable_window`.

### JetBundle (`scalar_alpha_jet_bundle`)
Composes directional alpha and derivative evidence for a point. See L1 primitives §4. Asymmetry: negative-α requires `singular_alpha_jet_bundle` instead.

### Fold-readback probe v10 / v11 (SUPERSEDED)
Precursor to hardened dual-arm probe. v10 verified machinery (operands hardcoded identical); v11 demonstrated genuine path separation (F2 wide / F4 microscope). **Closed; superseded by hardened V1.**
See: [Reports/foldreadback_probe0_v10_active_dualarm/](Reports/foldreadback_probe0_v10_active_dualarm/), [Reports/foldreadback_probe0_v11_genuine_separation/](Reports/foldreadback_probe0_v11_genuine_separation/).

### Dual-arm probe (hardened V1)
V4's production instrument for discriminating whether ARM-N reads genuinely new data vs numerically-collapsed restatement of ARM-W. Construction-time gates + run-time per-record `hardened_status`. 16 `gap_resolved` records on F2/F4 SR fixture. **Status:** V1 complete; v11 control-silence fix pending for advancement.
See: [Reports/hardened_dual_arm_probe/](Reports/hardened_dual_arm_probe/), [Architecture/DUAL_ARM_PROBE_PRINCIPLES.md](Architecture/DUAL_ARM_PROBE_PRINCIPLES.md).

### Dual-arm 6-condition resolution rule
An ARM-W gap is *resolved* by ARM-N iff **all six** hold: (1) ARM-W declares warning/below-floor/core-gap; (2) ARM-N activated by ARM-W falloff telemetry (not self-activated); (3) ARM-N produces valid reads inside the interval by ARM-N's own instrument law; (4) **real float64 path/operand separation** from ARM-W (non-zero offset level); (5) ARM-N read **not** selected by target-aware residual minimization; (6) handoff stable under partition and guard checks. Missing any one blocks `gap_resolved`.
See: [Architecture/DUAL_ARM_PROBE_PRINCIPLES.md](Architecture/DUAL_ARM_PROBE_PRINCIPLES.md).

### substrate-as-probe StructuredReading (4-channel)
4-channel composite instrument from substrate_invariant_search Phase F. Channels: (1) `ulp_spread_log2`, (2) `E_log2_base_operand`, (3) `two_form_partition`, (4) `K_G` (eval-layer). Decision rule attributes each probe to `phenomenon` / `substrate` / `ambiguous` / `format_precision_pinned` via `signal_ratio = |K_G| / bacl_predicted_noise_floor`. **Status:** Proof-of-concept (Phase G 3/4 matches); decision-rule thresholds are magic numbers, research-grade.
See: substrate_invariant_search Phase F, G.

### Substrate fingerprint atlas (CLOSED; absorbed)
12-slot fingerprint vector across 6 fixtures × 2 routes for fixture identification. Phase β redesign achieved complete discrimination (all 15 pairs distinguishable). **Closed**; partially absorbed into substrate-invariant-search.
See: [Reports/substrate_fingerprint_atlas/](Reports/substrate_fingerprint_atlas/), [Reports/substrate_fingerprint_atlas_phase_beta/](Reports/substrate_fingerprint_atlas_phase_beta/).

---

## 10. Mechanisms and Phenomena

### Sterbenz boundary
The operand value where `R^n ≥ 1/2` makes the first subtraction `R^n − 1` Sterbenz-exact. Fixture-specific: Schw `r=4.0`; SR `β=1/√2`; PA `x=0.5`; cbrt `x=0.5`. Predicts directional density bias in F2 firings — confirmed in all four fixtures. **One identified mechanism contributing to `b_k`**, not the whole.
See: paper §7; Tasks 028, 029c.

### Sub-lattice alignment (Task 031)
**V4-native discovery.** The Sterbenz-blessed arithmetic form `(R·R) − 1 + x` is **not** the minimum-burden representation of `R^n − 1 + x ≡ 0` in the Sterbenz-applicable region. The reassociated form `(R·R) + (x − 1)` dominates on lattice burden (integer lattice vs non-integer; max_integer_residual 0 vs 0.25) while tying on `b_k`. Operation-level exactness and chain-level optimization are **different criteria measuring different observables**. **Universal across 4 fixtures × 2 radical degrees** ([cross-fixture audit](Reports/task032_cross_fixture_refinery_audit/)).
See: [Reports/task031_sterbenz_audit_summary.md](Reports/task031_sterbenz_audit_summary.md); paper §8.

### MCG decomposition (`R = M ⊕ C ⊕ G`)
Decomposes observable residue into **M** (substrate-mandated, proven via BACL), **C** (conditioning amplification, operationally validated as `E = log₂(|base_operand|)`), **G** (geometric content if it exists). **G empirically absent in 1D scope** (three refutations in MCG Phase 2h). If G exists, it lies in multi-D regimes or reformulated observables.
See: [Reports/mcg_geometry_first/](Reports/mcg_geometry_first/) phase 0 M contract through phase 2h.

### M (substrate-mandated)
The BACL-proven integer-ulp lattice. The "predictable noise floor" of any constraint surface computation.

### G (geometric content)
**Empirically absent in 1D scope.** What remains after M and C are accounted for; either zero or below the discrimination threshold in 1D. May exist in multi-D — open.

### Geometry-first reframe
The reformulation that converted residue-first MCG (failed, killswitch HALT) into geometry-first: start from constraint geometry, propose candidate geometric invariants, ask whether BACL-filtered readback shadows them.
See: [Reports/mcg_gate_3_killswitch/](Reports/mcg_gate_3_killswitch/) closeout §6–7.

### Transfer-function exponent family
The cross-fixture invariant identified in [2026_05_25 cross-fixture closure](Reports/substrate_invariant_search/2026_05_25_cross_fixture_closure_via_transfer_function.md): the local asymptotic log-log slope of E versus singular-distance coordinate, evaluated at the branch point. Both Schwarzschild and pure_algebraic share branch exponent α=1; slopes converge to 1. Empirical agreement |Δ|=0.0038 at N=5.

### Routing-composition signature
Substrate-as-probe phenomenon where mathematically-identical compositions of the same operation produce bit-level operand differences (0 to ~4 ULPs depending on pair) that propagate through the V4 α-recovery chain with amplification ≈10⁶. Worked example: f^(1/6) across Python `**(1/6)`, `cbrt(sqrt(f))`, `sqrt(cbrt(f))`, `exp(log(f)/6)`, `numpy.power(f, 1/6)` — R1 ≡ R3 ≡ R5 bit-identical, R2 differs 1 ULP, R4 differs ~4 ULPs; resulting V4 α biases span −5.31e-11 to −1.37e-11. **Status:** *Empirical* (single n=6 dig, 2026-05-26). Refines the IEEE-mandate taxonomy: bit-identity within the implementation-free class is empirically possible when implementations dispatch through the same libm; the variation that matters is *compositional*, not merely implementational. **Implication for substrate-as-probe:** routing-diversity tests are most informative when they vary the composition, not the call site.
See: [Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md](Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md) §3.

### Negative-α BACL-favourable regime
Observation that the negative-α regime probed by `singular_alpha_jet_bundle` is empirically cleaner than the positive-α radical family (10⁻¹³ floor vs 10⁻¹¹ floor). Mechanism: for negative α, |g(h)| → ∞ as h → 0+; the finite-difference subtraction operates on two large numbers in the same binade where BACL gives bit-exact cancellation. For positive α, |g(f)| → 0 and the subtraction enters precision-floor territory. The substrate behaviour is opposite-signed between regimes. **Status:** *Empirical* (2026-05-26, 4 power-law observables).
See: [Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md](Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md) §4.

### Lifted singularity construction
For K simultaneous constraints F_i=0, lifted via `F_joint = ΣF_i² − X²`. Hessian has rank K+1, signature (K positive, 1 negative), H_XX = −2 — all **by construction**. The empirical finding is null-tangent alignment.
See: §2 above; [Reports/lifted_singularity_v4_audit/](Reports/lifted_singularity_v4_audit/).

### Observability rule F4 (`e_f < e_x`)
A measurement is observable iff operand `f` has lost binade information relative to its parameter `x`. **DO NOT extend** — below the rule there is no structured signal, only rounding noise.
**Distinct from** F4 *form* in the four-form battery (same letter, different concept).
See: [Reports/observability_rule_audit_F4/](Reports/observability_rule_audit_F4/).

### Comb / doubled comb / half-grid
A target observational outcome: residual phase `F/ulp(f) == 0.5`. Doubled sampling density. **May 16 cluster** searched for natural half-combs; result was *conditional* (Schw `f_binade_-1` 20/20 with hard-cell pair, but does not survive perturbation, does not transfer to other fixtures). Mostly negative results.
See: [Reports/f1_f2_natural_phase/](Reports/f1_f2_natural_phase/) and ~14 sibling May 16 reports.

### Hard cell / zero-offset hard cell
A coordinate where all direct + companion q-routes collapse to identical values — no operand offset available to lever half-phase separation. Index 130 on perturbed Schwarzschild `f_binade_-1` is the canonical example. **Resolved diagnostically by rounded-transcendental routes (violates Axiom 11)**; no clean-substrate resolution.
See: [Reports/hard_cell_q_source_exhaustion_search/](Reports/hard_cell_q_source_exhaustion_search/), [Reports/zero_offset_transcendental_q_source_search/](Reports/zero_offset_transcendental_q_source_search/).

### Operand offset / path separation
Real float64 difference between two routes' computed operand values. Necessary (not sufficient) for ARM-N independent reading. When zero, routes are numerically collapsed despite being algebraically distinct.

### Operand-offset guard
**Exact predictor** (precision 1.0, recall 1.0 on tested scope) of route-bank half-phase success. Rule: "direct is half-phase OR any companion route differs from direct by a nonzero float64."
See: [Reports/route_bank_offset_guard_audit/](Reports/route_bank_offset_guard_audit/).

### Route / route bank
A *route* is an arithmetic expression path used to compute intermediate values, especially the cancellation operand `q`. A *route bank* is a finite collection of candidate routes (e.g., `{cbrt_power, direct_2_over_r, sqrt_ratio_squared}`).

### Decision-law (L3 refinery MVP)
Task 030 produced the eval-layer F1-vs-F2 decision MVP for pure_algebraic. 8-dimensional burden vector + Pareto comparison. Reads committed JSONs; does not rerun campaigns. **Not authoritative L3** — feeds `layer-3-promotion` campaign.
See: [Reports/task030_refinery_mvp/](Reports/task030_refinery_mvp/).

### Burden vector components
8 dimensions: `b_k` point estimate + CI bounds, `lattice_class`, `max_integer_residual`, `polarity_class`, `calibration_zero_preserved`, `operation_chain_depth`. Used in Pareto comparison.

### `propagated_window_error`
V4-honest substrate-declared uncertainty. The audit framework uses `observed − ground_truth > propagated_window_error` as the "wrong" criterion, NOT naive `standard_error`. Worked example: task024b F4 appears 13.9σ off by naive audit but within `propagated_window_error` — different verdict.
See: [V4_AUDIT_FRAMEWORK.md](V4_AUDIT_FRAMEWORK.md).

---

## 11. Status / Verdict Vocabulary

### `gap_resolved` (dual-arm verdict)
ARM-N has met all 6 conditions of the resolution rule. First positive verdict in V4 satisfying full operational discipline. 16 records on F2/F4 SR fixture.

### `armN_zero_path_separation`
Underpromotion: ARM-N active but condition 4 (real path separation) fails.

### `phenomenon` / `substrate` / `ambiguous` / `format_precision_pinned` (substrate-as-probe attributions)
Output categories of the 4-channel StructuredReading decision rule. **Phenomenon** = signal_ratio > 1e3, clean signal. **Substrate** = signal_ratio ≤ 1, residual at or below noise floor. **Ambiguous** = middle regime. **Format_precision_pinned** = E in unsafe range (|base_operand| < ~10⁻⁴), format-precision artefacts dominate.

### `alpha_zero_boundary` / `alpha_unstable_window`
AlphaProbe statuses added Task 023b. Boundary: observed alpha near zero. Unstable: nested-window span exceeds materiality.

### `SweepSignatureStatus`
Task 035 status family with seven strata: clean, cancellation-dominated, high-drop-rate, degenerate-input, insufficient-data, nonfinite, and domain-refused. Default consumers accept only `sweep_signature_clean`.
See: `sweep_signature_probe`; [Architecture/STATUS_CALCULUS.md](Architecture/STATUS_CALCULUS.md).

### `alpha_regular_integer` (caller-gated)
Fires only when the caller provides `declared_alpha_band` or matching `declared_alpha_models`. With `declared_alpha_band=None` and `declared_alpha_models=()` (agnostic mode), the classifier routes every positive observed_α — including bit-clean integer cases (x, x², x³ recovered to ~10⁻¹²) — to `alpha_fractional_branch`. The calculus refuses to round to integer without an explicit caller-supplied tolerance. **Calibration fact:** every FRACTIONAL_BRANCH reading in V4 campaign history is an agnostic-mode classification, not a verified non-integer; consumers wanting to act on the integer-vs-fractional distinction must set the band parameter. **Status:** *Mechanism characterised* (2026-05-26).
See: `_classify_alpha` in `src/lloyd_v4/primitives/directional_alpha_probe.py`; [Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md](Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md) §5.4.

### Window-averaged α (vs asymptotic α)
For observables with non-power-law subleading terms (log corrections, products of powers, etc.), `directional_alpha_probe` reports the *window-averaged* slope, not the asymptotic limit. Worked example: f(x) = x·log(x) at x₀=0 recovers α=0.9013 across the standard 12-point sweep, despite asymptotic α → 1. For pure power-law observables (no subleading terms), window/asymptote collapses. **Status:** *Calibration fact* (2026-05-26). Downstream consumers reading α from log-modulated observables must treat it as a sweep-window measurement, not an asymptote.
See: [Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md](Reports/substrate_invariant_search/2026_05_26_alpha_recovery_exploratory_findings.md) §5.5.

### `cancellation_dominated` (status)
Observability stratum across multiple primitives indicating the result is dominated by floating-point cancellation, not structured signal.

### `advanceable` / `selectable` / `defined` / `finite` / `observable` / `policy_accepted`
Multi-field validity (per Axiom 4). These are distinct boolean fields, not one universal validity flag.

### `wrong_clean_emit_count` (master audit metric)
Decomposed into `wrong_family_clean_emit`, `wrong_off_family_clean_emit`, `wrong_boundary_clean_emit`, `wrong_refusal_failure`. Tracked per campaign per phase. High-confidence emit criteria: `refusal=None`, `protocol=ok`, `validity.selectable=True`, stable-status indicator True.
See: [V4_AUDIT_FRAMEWORK.md](V4_AUDIT_FRAMEWORK.md).

### Campaign verdict vocabulary
`proof_of_concept_achieved`, `partial_sharpening`, `chain_property_universal`, `HALT terminal`, `methodology_refinement_complete`, etc. Each campaign closeout uses one. Refer to source closeouts for usage.

---

## 12. Discipline Frameworks

### Campaign discipline
7 cross-cutting rules: pre-registration binding; no substrate promotion within campaign; `wrong_clean_emit_count` master metric; surprise ledger; cross-campaign reference palette; time-boxed phases; fork discipline.
See: [CAMPAIGN_DISCIPLINE.md](CAMPAIGN_DISCIPLINE.md).

### V4 audit framework
Operational spec for `wrong_clean_emit_count`. High-confidence criteria + V4-honest wrong criterion via `propagated_window_error`.
See: [V4_AUDIT_FRAMEWORK.md](V4_AUDIT_FRAMEWORK.md).

### Reference hygiene (V3 + Vera)
Axiom 10 (V3 reference-only): no imports/calls/adapters/bridges. `mcp__lloyd_v3__lv3_*` tools are confirmation oracles only. **Extends to AI workflow** — reading V3 docstrings/test expectations can spoil V4 emergence.
See: [Architecture/V3_REFERENCE_LEDGER.md](Architecture/V3_REFERENCE_LEDGER.md), [Architecture/REFERENCE_HYGIENE.md](Architecture/REFERENCE_HYGIENE.md).

### Vera strip-and-replicate protocol
Strip Vera vocabulary → identify substantive observation → design V4-native test → run → compare → cite Vera as independent source. **Depth A** = cite as corroboration. **Depth B′** = replicate before admission. **Depth C** structurally impossible.
See: [Architecture/VERA_REFERENCE_LEDGER.md](Architecture/VERA_REFERENCE_LEDGER.md), [vera_v4_unification_dossier.md](../../Docs/vera_v4_unification_dossier.md).

### Live campaigns ledger
What's in flight right now. Prevents restart of active campaigns under new names.
See: [LIVE_CAMPAIGNS_LEDGER.md](LIVE_CAMPAIGNS_LEDGER.md).

### Pre-edit axiom check
`/v4-axiom-check` slash command walks any substrate-touching diff through the 12 axioms. Mandatory before edits in `src/lloyd_v4/core/`, `primitives/`, `projection/`, `metrology/`, `branch/`, or `Build_Docs/Architecture/`.

### Plan mode for substrate work
Before any substrate edit, enter plan mode and produce an explicit plan naming the axioms the edit touches and how the edit honours them.

### Byte-stable outputs
Campaign JSON outputs are byte-stable. Regenerate and diff before claiming a change.

---

## 13. Things commonly confused

| Sound similar | Are actually different |
|---|---|
| `b_k` noise floor (L2 metrology) | `b_k` arithmetic-path conditioning amplitude (Theorem 3). **Same letter, different concept.** |
| F4 form (`R − √f_alt`, four-form battery) | Observability rule F4 (`e_f < e_x`). **Same letter, different concept.** |
| BACL (proven IEEE 754 invariant) | c2 lattice theorem (conditional on Conjecture C; specific to c2 routing) |
| MCG `mcg-discovery` campaign | MCG `mcg-geometry-first` campaign | mcg-discovery is SUPERSEDED; geometry-first then merged into substrate-invariant-search |
| Refinery MVP (Task 030, eval-layer instance) | `layer-3-promotion` campaign (the broader promotion effort the MVP feeds into) |
| `K_q` (proxy calibration, Axiom 7) | K_G (canonical Gaussian curvature, Phase E) — different K |
| `Conditioning` carrier (`core/conditioning.py`, L0) | "conditioning primitive" in `SUBSTRATE_CONSTRUCTION.md §9` — the carrier is a typed dataclass holding status + diagnostic; the §9 "conditioning primitive" is the L1 IEEE 754 lattice-geometry primitive (embodied by `typed_ulp` and any siblings that expose binade/lattice spacing). **Same word, different layer, different concept.** When SUBSTRATE_CONSTRUCTION refers to "the conditioning primitive" it means the lattice-geometry primitive, not the L0 carrier. |
| `scalar_alpha_jet_bundle` | `singular_alpha_jet_bundle` — sibling primitives for regular vs singular regions; one is not a fix for the other |
| Sub-lattice alignment (Task 031 discovery) | Sterbenz boundary mechanism (paper §7) — both contribute to `b_k`; not the same mechanism |
| `M` (substrate-mandated, MCG term) | M as in mass / Schwarzschild parameter — context disambiguates |
| Substrate fingerprint atlas (closed) | substrate-invariant-search (active) — the atlas was partially absorbed into the search |
| Phase 3B of alpha-minus-one-exhaustion (six fixture classes, pre-registered) | Phase G of substrate-invariant-search (4 pathological probes) — NOT the same thing |
| AlphaProbe primitive (`directional_alpha_probe`) | α (alpha exponent, the mathematical quantity being measured) |
| α (alpha exponent) | `a` (path-invariant geometric amplitude in Theorem 3) — same Greek/Latin letter, different concept |
| Layer 3 (refinery / decision-law / solver) | L3a (refinery / history) and L3b (solver) — subdivisions |
| Agnostic-mode `alpha_fractional_branch` (no declared band) | Declared-mode `alpha_fractional_branch` (with band; observed outside any integer envelope) — same status name, different semantic: agnostic skips the integer test entirely, declared has run the test and concluded non-integer |
| Window-averaged α from `directional_alpha_probe` | Asymptotic α at the branch point — for log-modulated observables these differ; for pure power laws they coincide |
| Routing-composition signature (substrate-as-probe at the α chain, 2026-05-26) | BACL grain (substrate-as-probe at the per-operation lattice) — BACL is per-operation; routing-composition is per-decomposition; both real, different scales |
| `SweepSignature` | `BurdenVector` vs `SlagVector` — all carry "is this rewrite worth taking" evidence, but `SweepSignature` is a primitives-layer observable-level statistical sweep signature, `BurdenVector` is an evals/refinery_mvp per-(fixture, path) campaign aggregation, and `SlagVector` is a refinery-layer typed-result snapshot diff |

### Original questions Q1–Q6 status

See [LIVE_CAMPAIGNS_LEDGER.md → Open questions](LIVE_CAMPAIGNS_LEDGER.md#open-questions--current-status) for current status. Most-confused: Q5 is **solved in the regular region** but `b_k` is **larger in the Sterbenz region** — the apparatus is louder where the user first noticed the phenomenon. Q6 is **addressed via dual-arm probe** (discrimination) but **not solved** (resolution below noise floor).

---

## Update protocol

This file changes when:
1. A new primitive, status family, theorem, or proven lemma is added.
2. A concept is renamed or scoped.
3. A status changes (e.g., "open" → "proven", "active" → "closed").
4. A confused-pair surfaces in practice (add to §13).

This file does **not** change for:
- Per-task results (those live in `Reports/`)
- In-progress campaign updates (those go to [LIVE_CAMPAIGNS_LEDGER.md](LIVE_CAMPAIGNS_LEDGER.md))
- Narrative or synthesis (those go to `Docs/`)

Keep entries tight. One line + status + source. If you find yourself writing a paragraph, that paragraph belongs in a report, not here.
