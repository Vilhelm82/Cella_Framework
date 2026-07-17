> **RETIRED 2026-05-25**
>
> This authority document was scoped without consulting parallel V4 work that contained foundational tools for the campaign's stated goal (substrate-derived K_G observable for L3 promotion). Specifically: `transfer_function_exponent_family_v4.tex` (the α-1 transfer law, proven), the BACL theorem as a prediction engine (not just a catalogued observable), α as a per-probe local observable, `typed_log_log_slope` and `typed_finite_difference` primitives, and the relationship machinery between these quantities.
>
> Phases A through I were executed under that constrained toolkit. Their results document the behavior of the constrained instrument that was operative under this authority's scope; they are not citable as substrate-physics findings about the campaign's actual subject matter. The "cross-fixture ceiling is mathematical, structural" verdict in the Phase F amendment is correct *for value-space observables under the constrained toolkit*; it is not a general structural claim about the substrate.
>
> Yesterday's cross-fixture log-log slope agreement at branch (Schw 0.9962, PA 1.0000, |Δ|=0.0038 at N=5) is the surprise that revealed the toolkit limitation. It is not a result of this authority's campaign; it is the evidence that motivated this authority's retirement.
>
> **Successor authority:** `substrate_invariant_search_2026_05_26.md` (pending; opens with the proper toolkit at §1 as required reading + foundational tools).
>
> **Campaign goal remains open:** substrate-derived K_G observable. Phase E Path A failed under this authority. Phase E Path B (BACL + α + log-log slope construction) was not attempted because the toolkit needed to attempt it was not on the menu.
>
> **Do not cite phase results from this authority as substrate-physics findings.** See `Reports/substrate_invariant_search/README.md` for the disposition of phase artifacts.
>
> ---

# Substrate Invariant Search Campaign

**Date:** 2026-05-23
**Audience:** Claude Code / Codex-style repo implementation agent
**Mode:** Discovery + synthesis campaign. Catalogue, characterise, fuse, then demonstrate.
**Scope:** V4 eval-layer + one substrate primitive addition (V4-native K_G in Phase E). Plan-mode + axiom-check required for Phase E. No other Layer 0/1 modifications.

---

## 0. Purpose

This campaign hunts the substrate-derived geometric invariant that V4 needs in order to operate as a **substrate probe** rather than a residual-based diagnostic.

The framing comes from the substrate-as-probe thesis articulated 2026-05-23:

> Residual-based solvers (Newton, secant, fixed-point) iterate on a quantity that's the output of the same arithmetic substrate they're trying to navigate. When `|F(x)|` drops below the noise floor, the solver cannot distinguish "I found the root" from "I hit BACL grain." Convergence criteria are substrate-substrate convolutions: asking the noise whether the noise is small. The alternative is to expose enough substrate primitives that the phenomenon can be read *from* the substrate fingerprint, the way NASA reframed turbulence from noise to diagnostic medium, or the way the V4 barcode framing reads surface identity from finite-precision residual structure.

Operationally, the campaign asks: **does there exist a low-dimensional substrate-derived scalar (or vector) that carries point-level geometric content of a constraint surface, is computable from inputs alone, is invariant under route choice and format, and can replace residual-based termination in a defined failure-mode demonstration?**

If yes, the campaign produces it and demonstrates it.
If no, the campaign records why — which combination of substrate primitives is insufficient, and what additional substrate work would be required.

---

## 1. Fixed context carried forward

Established by prior V4 work. Do not relitigate.

### 1.1 BACL is proven

`bacl_invariant_audit/`, `bacl_subnormal_audit/`, `bacl_multi_format_audit/`. For `a, b ∈ F⁺` with `ulp(a) ≥ ulp(b)`, `a − b = j · ulp(b)` for integer `j ∈ ℤ`. ~31,000 records across float16/32/64 normal+subnormal. Zero violations. Multi-format BACL holds.

BACL provides the substrate's intrinsic lattice unit at any operand pair. **This is the strongest established substrate invariant ingredient.**

### 1.2 Conjecture C / c2 lattice theorem proven within scope

`conjecture_c_proof_audit/` (definition-grounded Amendment II), `c2_lattice_substrate_derivation/`, `c2_theorem_scope_gate/`. For float64 normal range (`f ≥ 2^−1021`), the sqrt-square chain preserves binade-floor. Identifies a closed structural property for that chain.

### 1.3 MCG geometry-first campaign delivered (1D scope)

`mcg_geometry_first/phase_0` through `phase_2h`. M = BACL, C = `E := log2(|base_operand|)` operationally validated as 1D C-extractor (Phase 2g `cdef1_operational_extractor_validated_1d`), G empirically absent in 1D, V3 diagnostic bridge built (Phase 2h, oracle agreement).

Threshold cluster: `log2 ∈ [−0.949, −0.750]`, spread 0.198, corresponding to `|base_operand| ∈ [0.518, 0.594]` — near the Sterbenz boundary at `|base_operand| ~ 0.5`. **Cross-fixture substrate-recognisable threshold.**

### 1.4 Fingerprint atlas barcode framing validated

`substrate_fingerprint_atlas_phase_delta/`. 6-slot fingerprint uniquely identifies all 6 campaign fixtures. Perturbed SR (probe window `{0.80, 0.82, 0.84}`) vs canonical SR (`{0.83, 0.85, 0.87}`) at **distance 0.0** — byte-identical fingerprint under window perturbation. Fixture-level invariance demonstrated.

### 1.5 Blowup-exponent universal

`blowup_exponent_v4_audit/`. `σ1 = 1.000 ± 0.000` across 15 simple zeros of `ζ`, `J₀`, `Ai`. Linearisation-order signature is structurally universal — H1-equivalent across very different transcendental functions. **Strong candidate for a regularity-class invariant.**

### 1.6 V3 isolation discipline (CLAUDE.md §4)

V3 / lv3 is a confirmation oracle, never a design source. Cross-pipeline comparison at the smoke-test fixture level (`v3_calibration_fixtures/`, 2026-05-23) is reference data, not design input.

### 1.7 The substrate primitives V4 currently exposes

- **BACL grain** `ulp(b)` at an operand pair — substrate-level intrinsic granularity
- **E := log2(|base_operand|)** — substrate image of distance-to-singular-surface (1D, `1 − x_term` form)
- **F1_to_F2 phase signature** — algebraic-path-dependent BACL-lattice readback (MCG)
- **Hardened dual-arm probe** — operational discipline for independent reads with path/operand separation telemetry (`hardened_dual_arm_probe/`)
- **Fingerprint atlas slots** — empirical substrate observables that distinguish surfaces (Phase δ)
- **Path-dependent cancellation** — algebraic-form asymmetry between silent and BACL-residual-carrying routes

V4 does **not** currently expose a native K_G primitive. Phase E adds it.

---

## 2. Campaign thesis

The unified invariant exists if and only if there is a substrate-derived scalar (or vector) `I(F, x)` satisfying:

```text
(P1) input-derivable:  I computable from (F, x) alone, no iteration on F(x_k)
(P2) geometric:         I carries point-level geometric content of F = 0
(P3) route-invariant:   I unchanged under algebraically-equivalent rewrites of F
(P4) format-invariant:  I scales lawfully across float16/32/64
(P5) discriminating:    I distinguishes substrate-attribution from phenomenon
```

Properties P1–P5 are the falsifiability criteria.

The strategy is bottom-up: catalogue the candidate ingredients already in the corpus (Phase A), compute them on a common probe set (Phase B), find the irreducible basis (Phase C), test transformation-invariance (Phase D), add the missing K_G ingredient (Phase E), synthesise (Phase F), demonstrate against Newton in a defined failure mode (Phase G).

If at Phase F no combination satisfies P1–P5, the campaign records the gap and surfaces what additional substrate work would be required.

---

## 3. Phase structure

Each phase is a separate pre-registered deliverable. Phases land in order; later phases may revise but must cite prior ones via sha256 chain. Standard V4 campaign discipline: pre-registries binding pre-measurement; byte-stable artefacts; sha256 provenance; no scope creep.

### Phase A — Invariant candidate catalogue (audit-only)

**Purpose:** Formal statement of every substrate-invariant candidate currently in the V4 corpus. Per candidate: definition, mathematical form, substrate-derivation chain, current verification status, scope-of-applicability, identified gaps.

**Discipline:** Audit-only. No new measurements. References prior reports; does not recompute.

**Output:** `Build_Docs/Reports/substrate_invariant_search/phase_a_candidate_catalogue.json` + `.md`.

**Candidates expected (non-exhaustive):**
- BACL lattice grain `ulp(b)` (proven)
- E := log2(|base_operand|) (1D-validated)
- Sterbenz cluster threshold
- σ1 universal linearisation exponent
- Fingerprint atlas distance metric
- Null-tangent alignment `|cos θ| = 1.0000` universal
- V3's −2 eigenvalue (untested V4-native)
- F3 calibration ≡ 0.0 exact (algebraic-path invariant)
- Doubling-ladder rung index
- Two-form asymmetry under path cancellation
- c2 lattice theorem's binade-floor preservation

### Phase B — Common probe set evaluation

**Purpose:** Compute every applicable Phase A candidate at a common set of probe points across SR / Schwarzschild / pure_algebraic + at least one geometry-anchor multi-D fixture. Build per-point invariant vectors.

**Discipline:** Pre-register the probe set + computation method per candidate. Byte-stable artefact.

**Output:** `phase_b_invariant_vector_table.json` + `.md`.

### Phase C — Irreducible basis analysis

**Purpose:** Identify which candidates are correlated (redundant) and which are orthogonal (genuinely independent). Estimate the intrinsic dimensionality of the candidate vector. Report the irreducible basis.

**Discipline:** Pairwise correlations + dimensionality estimation via PCA-equivalent. Pre-register tests; no candidate elimination without explicit rationale.

**Output:** `phase_c_irreducible_basis.json` + `.md`.

### Phase D — Transformation-invariance audit

**Purpose:** For each candidate in the irreducible basis, test invariance under:
- Algebraically-equivalent route rewrites (route-invariance, P3)
- Format change float32 ↔ float64 (format-invariance, P4)
- Reparameterisation of the constraint (e.g., `r → 1/u` for Schwarzschild)

Candidates failing transformation-invariance are demoted; candidates passing become invariant-synthesis ingredients.

**Discipline:** Per-transformation pre-registered acceptance criterion.

**Output:** `phase_d_transformation_invariance_audit.json` + `.md`.

### Phase E — V4-native K_G primitive (substrate addition)

**Purpose:** Implement Gaussian curvature `K_G(F, x)` as a V4 substrate primitive, derived from BACL / E / fingerprint primitives rather than imported via bordered-determinant arithmetic. The current campaign cannot proceed to synthesis without this — Phase 2h surfaced the gap; the substrate probe needs its own K_G to be the substrate-derived analogue.

**Discipline:** Substrate-touching. Plan mode + `/v4-axiom-check` required. Axiom 4, 8, 11, 12 reviewed pre-edit. No named-math imports as substrate (Axiom 11) — K_G must be derived via the synthesis protocol from substrate primitives, not asserted from differential-geometry literature.

**Output:** `src/lloyd_v4/primitives/kg_primitive.py` + tests + pre-edit plan in `Build_Docs/Reports/substrate_invariant_search/phase_e_plan.md` + per-axiom rationale.

### Phase F — Invariant synthesis

**Purpose:** Combine the surviving Phase D candidates + Phase E K_G into a candidate substrate invariant `I(F, x)`. Verify P1–P5 against the synthesis target.

**Discipline:** Pre-registered synthesis form. If no form satisfies P1–P5, record the gap and freeze the campaign at this phase (do not force-fit).

**Output:** `phase_f_invariant_synthesis.json` + `.md` + `src/lloyd_v4/evals/substrate_invariant.py`.

### Phase G — Failure-mode demonstration

**Purpose:** Pick a known-pathological case where Newton's method fails (root multiplicity ≥ 2, near-singular Jacobian, ill-conditioned at noise floor). Show that:
- Newton produces spurious convergence or fails to terminate
- The Phase F substrate invariant reads the geometry correctly without iteration

If the demonstration succeeds: substrate-as-probe thesis has empirical proof-of-concept.
If it fails: record which property (P1–P5) of the invariant breaks under pathological geometry, and what's needed to close the gap.

**Discipline:** Pre-register the pathological case. Pre-register Newton's failure mode. Compare against Newton's actual behaviour on the same case, not against a strawman.

**Output:** `phase_g_failure_mode_demo.json` + `.md` + reproducible script.

---

## 4. Non-goals

- **Not** a retire-Newton-everywhere claim. The Phase G demonstration is for a defined failure mode, not a general-purpose replacement.
- **Not** a publication campaign. The work is internal probe-maturation. Publication-defensibility framing is excluded per existing V4 working discipline.
- **Not** a substrate refactor. Phase E adds one primitive (K_G). No other Layer 0/1 changes.
- **Not** V3 reimplementation. lv3 is confirmation oracle only.
- **Not** an MCG continuation. Multi-D MCG questions (MD_Q1–MD_Q4 from Phase 2h) are parked; this campaign may consume them as input but does not pursue them.
- **Not** a literature audit. The "BACL folklore-likely" web search is a separate parked deliverable.

---

## 5. Falsifiability gates per phase

| Phase | Gate | Failure response |
|---|---|---|
| A | Every named candidate in §1.7 + this §3 list documented with definition + status | Add missing candidate or close gap |
| B | Per-point invariant vectors computed without iteration on F(x) | If iteration required, candidate violates P1; mark and proceed |
| C | Irreducible basis has cardinality ≥ 2 (otherwise no fusion needed) and ≤ ~6 (otherwise no useful synthesis) | Outside this range, re-examine candidate set |
| D | At least one basis element survives all three transformation tests | If none survive, record and freeze; substrate invariant doesn't exist in current scope |
| E | V4-native K_G computable on canonical fixtures, byte-stable, axiom-clean | If derivation requires named-math import, freeze; this is a substrate-primitive gap |
| F | Synthesised `I` satisfies P1–P5 | If not, record which property breaks and freeze |
| G | Newton fails on chosen case AND `I` reads correct geometry | If `I` also fails, record what additional substrate it would need |

The campaign's overall falsifiability is at Phase F. If Phase F freezes, the substrate-as-probe thesis is not refuted but is shown to be substrate-incomplete in the current scope — and the campaign produces the specific list of what's missing.

---

## 6. Discipline

Follows existing V4 campaign discipline (`Build_Docs/CAMPAIGN_DISCIPLINE.md`):

- **Pre-registries binding pre-measurement.** Pre-measurement amendments allowed only if explicitly flagged before data is admitted.
- **Byte-stable artefacts.** Every JSON output must rerun byte-identical (`json.dumps(..., indent=2, sort_keys=True)`).
- **sha256 chain.** Each phase artefact records sha256 of its sources.
- **Forbidden language scan.** No "discovered," "confirmed," "proves" language without negation context.
- **V3 isolation.** Per CLAUDE.md §4. Confirmation oracle use allowed in separate non-primary artifacts.
- **Substrate boundary.** Phase E is the only substrate-touching phase. All others are eval-layer.

Each phase post-completion: provide interpretive analysis per user's standing direction.

---

## 7. References

- D⊕S=P substrate-as-probe thesis (this session, 2026-05-23)
- `Build_Docs/PROBE_READINESS.md` — scoreboard tracking V3 calibration attribution
- `Build_Docs/Reports/bacl_invariant_audit/closeout.md` — BACL proof
- `Build_Docs/Reports/conjecture_c_proof_audit/closeout.md` — Conjecture C definition-grounded proof
- `Build_Docs/Reports/c2_lattice_substrate_derivation/closeout.md` — c2 lattice theorem
- `Build_Docs/Reports/mcg_geometry_first/phase_2h_v3_bridge.md` — V3 diagnostic bridge artifact
- `Build_Docs/Reports/substrate_fingerprint_atlas_phase_delta/closeout.md` — barcode framing validated
- `Build_Docs/Reports/blowup_exponent_v4_audit/closeout.md` — σ1 universal
- `Build_Docs/Reports/hardened_dual_arm_probe/closeout.md` — operational discipline for independent reads
- `Build_Docs/where_i_got_stuck.md` — original substrate observations
- `Build_Docs/Architecture/AXIOMS.md` — 12 axioms (Axiom 11 especially relevant for Phase E)
- `Build_Docs/Architecture/DUAL_ARM_PROBE_PRINCIPLES.md`
- `Build_Docs/Architecture/REFERENCE_HYGIENE.md`
- `CLAUDE.md` §4 — V3 isolation discipline
- `Build_Docs/CAMPAIGN_DISCIPLINE.md` — V4-wide campaign methodology

---

## 8. Status

**Active. Phase A pre-registry to be drafted as the next deliverable.**

Phase A spec: `Build_Docs/Agent_tasks/substrate_invariant_search_phase_a_catalogue.md`.
