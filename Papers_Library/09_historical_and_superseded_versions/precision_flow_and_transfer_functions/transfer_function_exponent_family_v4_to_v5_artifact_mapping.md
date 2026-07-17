# Transfer Function Exponent Family v4 → v5 Artifact Mapping

**Purpose**: Source of truth for the v5 revision. Nearly every corrective or strengthening change the paper needs already has a dedicated, citable artifact (report directory + closeout/summary, or scratch script + results). This is a **citation + reframing + integration** task, not new research.

**Date of this mapping**: 2026-05-30  
**Source paper**: `Build_Docs/transfer_function_exponent_family_v4.tex` (2026-05-14)  
**Primary authority for supersessions**: `HISTORICAL_RECORD.md` (entries under "Superseded" + paper-hardening notes)  
**User-provided inventory** (2026-05-30 message) used as the canonical list; cross-checked against actual directories.

---

## Items with Dedicated Artifacts (Ready to Cite)

### 1. Theorem 1 — transfer law / α−1 / log-log slope (robust branch transfer + pure algebraic corollary)

**Existing artifacts**:
- `scratch/transfer_function_slope_test.py`
- `scratch/local_slope_field.py`
- `scratch/sqrt_alpha_probe.py`
- `scratch/radical_family_alpha_probe.py`
- `scratch/cbrt_alpha_probe.py`
- `scratch/cbrt_alpha_probe_mpmath_oracle.py` (oracle cross-checks)
- Reports:
  - `Reports/substrate_invariant_search/` (multiple phases, especially the 2026-05-25 slope-field closure via transfer function)
  - `Reports/task025_path_law_discovery/`
  - `Reports/task035_sweep_signature_probe/` (new Layer-1 primitive that composes typed_finite_difference + typed_log_log_slope)
  - `Reports/task036_alpha_probe_sweep_signature_companion/` (joint evidence pattern; used in GR critical exponent recoveries)

**Status in v4.tex**: Already the strongest part of the paper (controlled expansion, finite-difference transfer, limiting log-log slope = α−1). V5 primarily needs better provenance citations + explicit note that V4 typed primitives now measure this directly (no more |λ_max| proxy dependency for primary validation path).

**GR application note**: The whitepaper (`scratch/whitepaper_gr_critical_exponents_v1.md`) + ISCO/Kerr scripts recover known physical exponents (0.5 for Schwarzschild ISCO saddle-node, 1/3 for Kerr prograde ISCO, 1/2 for photon sphere, linear for retrograde) using exactly these primitives. The 45/16 coefficient for retrograde was first measured empirically, then analytically derived.

---

### 2. Precision-scaling separation / b_k / R²=1.0 (user labeled "Theorem 3"; corresponds to paper's Theorem 2 + related discussion)

**Primary artifact**:
- `Reports/task017c_multi_precision_theorem2/` (f5_plus_supplementary.json, headline_classification.md, pre_registration.md, precision_aggregate.json)
- `Reports/task017c_summary.md` (top-level in Reports/)
- Predecessor: `Reports/task017b_multi_precision_instrument_model/`

**Exact status to carry forward** (from task017c + HISTORICAL_RECORD):
- Regular-region linear-in-u_p model C_{p,k} = a + u_p b_k fits at R² = 1.0 across all four fixtures and load-bearing paths (core validation).
- F3 calibration zero at every precision.
- Three sub-claims remain partial/open (as correctly noted in v4.tex §self-reference):
  1. cbrt F1 intercept CI excludes zero only at magnitude below available oracle floor → geometric component identifiable only as bounded-above.
  2. F1/F2 slope distinguishability failed with the available 3–4 distinct u_p values per fixture (CIs overlap).
  3. Over-strong pre-registered prediction that b_k should vanish inside Sterbenz-exact half-space was not supported; inverted observation (Sterbenz-region b_k upper bounds larger than regular-region in every fixture) + reframing is substantive.

**V5 action**: Quote the exact partial status from task017c_summary / headline_classification rather than the stronger "empirically validated" phrasing currently in the paper. Cite the task017c directory as the authoritative empirical instantiation.

---

### 3. Cross-fixture invariance (4 fixtures, 2 radical degrees; paper's Theorem 3 / "chain-property")

**Per-fixture dedicated reports** (user's list):
- `Reports/task024b_schwarzschild_four_form/` (Schwarzschild radial; includes v3_reference_overlay)
- `Reports/task027_sr_four_form_cross_fixture/` (special-relativistic time dilation)
- `Reports/task028_conditional_masks_joint_lattice_pure_algebraic/` (physics-stripped pure-algebraic control)
- `Reports/task029c_cbrt_four_form_battery/` (cube-root algebraic control; cbrt_polarity_grid_*.json, cbrt_precision_overlap_table.csv, etc.)

**Synthesis / audit**:
- `Reports/_audit/03_four-form-battery-cross-fixture-invariance.md`

**Additional related**:
- `Reports/task032_cross_fixture_refinery_audit/` (extends the invariance to quartic; lattice grain discrimination)
- `Reports/task033_schwarzschild_cbrt_transformed_n3/`
- `Reports/task034_schwarzschild_quartic_transformed_n4/`

**Critical update for v5** (per HISTORICAL_RECORD supersession flags):
- The v4.tex presents this as "Theorem 3" with language of derivation / "in general" / strengthens to "controlled-branch radical chains in general".
- Record status: empirical regularity / classification-level observation across the four fixtures. The 0.5/0.25 (and integer vs non-integer) grain values are artifacts of the two rounding grids (F1 vs F2 families), not a deep universal.
- The actual derivation of the lattice structure arrived later (see next item).

**V5 action**: Relabel or re-scope the statement to "Cross-fixture classification invariants observed across four fixtures spanning two radical degrees (Tasks 024b/027/028/029c + audit 03)". Move the "derivation" claim to the new substrate-derivation section below. Keep the five invariants (F3 silence, F1∥F2 polarity, F2 non-integer grain, F4 integer lattice, Sterbenz directional bias) as the observed pattern, with explicit citation to the per-fixture reports.

---

### 4. Substrate derivation of the lattice structure (what Open Challenge #2 in the paper called a "forward task")

This is the single largest corrective strengthening.

**Core derivation artifacts**:
- `Reports/bacl_invariant_audit/` (+ `bacl_multi_format_audit/`, `bacl_subnormal_audit/`) — BACL invariant (a−b = j·ulp(b) for ulp(a)≥ulp(b)), proven across normal + subnormal, float16/32/64.
- `Reports/c2_lattice_substrate_derivation/` (+ closeout.md, artifact.json) — c2 integer-lattice universality as 3–5 line corollary of BACL + Sterbenz + IEEE 754 binade spacing. 0 violations on ~25k measurements.
- `Reports/c2_lattice_sharpness_audit/`
- `Reports/c2_theorem_scope_gate/` — explicit scope (normal range f_float ≥ 2^-1021; n=2 clean, n=3 route-dependent looseness, n≥4 needs further C_n).
- Scratch: `bacl_invariant_audit.py`, `bacl_*.py` (4 scripts), `c2_lattice_*.py` (4 scripts including `c2_theorem_scope_gate.py`, `c2_lattice_binade_danger_zone.py`).
- Audit synthesis: `Reports/_audit/09_bacl-substrate-invariant-and-hardened-probe.md`

**Conjecture C (correctly-rounded sqrt preserves binade floor under canonical squaring; required for the n=2 clean case)**:
- `Reports/conjecture_c_proof_audit/` (+ closeout.md)
- `scratch/conjecture_c_definition_grounded.py`, `conjecture_c_proof_audit.py`

**Scope + n-dependence clarification** (directly addresses "in general" over-reach):
- `Reports/c2_theorem_scope_gate/`
- `Reports/task033_schwarzschild_cbrt_transformed_n3/` (n=3 looseness, value-level boundary still at x=0.5)
- `Reports/task034_schwarzschild_quartic_transformed_n4/` (transformed row converges to identity floor at n≥3)
- `Reports/task032_quartic_lattice_grain_discrimination/`

**V5 action**:
- Add a short new subsection "Substrate derivation of the c2 lattice invariants" (or equivalent).
- Cite the BACL + c2 closeouts as the operation-level mechanism that was previously a forward task.
- Explicitly state that the 0.5/0.25 grain pattern and integer vs non-integer distinction are now derived (with scope gates) rather than purely empirical cross-fixture observations.
- Retire or heavily qualify the old "Theorem 3" universality language per the HISTORICAL_RECORD supersession notes.
- Note route-dependence for n=3 (np.cbrt max |j|=7 vs pow(1/3) max=2) as a V4-native fingerprint result.

---

### 5. Sterbenz boundary as a concrete b_k component

**Artifacts**:
- `Reports/task031_sterbenz_audit/` (+ summary)
- `Reports/_audit/05_refinery-sterbenz-lattice-grain-and-curvature-pivot.md`

**V5 action**: The v4.tex already treats this well (Observation, not full b_k). Update citations to the task031 directory and note that the value-level boundary identification extends across radical degrees (confirmed in task029c cube-root at the same x=0.5 location).

---

### 6. Sub-lattice alignment / refinery audit (V4-native discovery that operation-level exactness ≠ macroscopic lattice burden)

**Artifacts**:
- `Reports/task030_refinery_mvp/`
- `Reports/task032_cross_fixture_refinery_audit/` (the six-candidate Pareto audit extended to cross-fixture; c2 dominates c1 on lattice class in all 4 fixtures)
- `scratch/cross_fixture_refinery_audit.py`

**V5 action**: Already strong in the paper (Observation 2). Add citation to task032_cross_fixture_refinery_audit closeout for the four-fixture universality of the sub-lattice alignment finding.

---

### 7. Path-basis rank / multi-component structure of b_k (Open Challenge #7)

**Artifacts**:
- `Reports/task029_path_basis_rank_clustering/`
- `Reports/task029b_methodology_refinement/`

**V5 action**: Update the open-challenges section to reflect the methodology refinement and any rank closure achieved. The full operation-graph annotation deriving the five invariants from per-operation rounding remains forward (as the paper already states).

---

## The Two Genuine Gaps (Correctly Flagged in the Paper as Forward Tasks)

These have **no dedicated V4 artifact** (user's explicit statement; cross-checked):

1. **Finite-window bias V4 fitting harness** (Proposition "Two-term finite-window bias" + Open Challenge #6)
   - The mathematical bias formula exists in the paper.
   - No V4 typed harness that applies nested-window s(f) = s_∞ + B f^ρ fitting across the typed transfer observations and reports α = s_∞ + 1 with bias estimate.
   - Remains a real, correctly documented gap.

2. **Non-algebraic / iterated-logarithm V4 retest under the automatic stability diagnostic** (Open Challenge #5)
   - V3 discovery exists: `Reports/task023_iterated_logarithm_discovery/` (discovery_report.md, observations_data.json, discovery_script.py) + task023_summary.md + task023b_summary.md.
   - No V4 retest using typed_log_log_slope + the automatic threshold rule (Diagnostic Rule in the paper: model comparison among M_A algebraic, M_L logarithmic/slow variation, M_E essential) + information criteria on nested windows.
   - Remains a real, correctly documented gap. (The V3 result can still be cited as historical independent evidence.)

**V5 action**: Keep these two items in the "Open challenges" section, with explicit "no V4 artifact yet" language and pointers to the V3 task023 material for the iterated-log case. Do not claim progress that does not exist.

---

## Additional Post-v4 Strengthening (Not in the Original Open Challenges List)

These are high-value results that exercise the exact machinery the paper describes and should be considered for inclusion:

- **Sweep signature probe as orthogonal same-precision diagnostic** (`Reports/task035_sweep_signature_probe/`, `task036_alpha_probe_sweep_signature_companion/`, Arc 13 audit `_audit/13_...md`): Joint (alpha + sweep) verdict distinguishes formulation-burdened cases from structurally-unstable but clean ones. Directly advances the self-reference problem beyond multi-precision u_p scaling alone. Used in the GR recoveries.

- **Cross-fixture slope-space invariant** (`Reports/substrate_invariant_search/2026_05_25_cross_fixture_closure_via_transfer_function.md`): Local log-log slope of E at the branch converges to the predicted α value across fixtures (Δ=0.0038 at N=5 for α=1 cases) where value-space observables showed a ceiling. Direct manifestation of Theorem 1 on the diagnostic instrument itself. (Campaign authority later retired for toolkit reasons; the finding is preserved.)

- **GR critical exponents recovery** (`scratch/whitepaper_gr_critical_exponents_v1.md` + supporting ISCO/Kerr/Choptuik scripts + result JSONs + `kerr_retrograde_45_over_16_derivation.md`):
  - Recovers Schwarzschild ISCO α = 0.500014 ± 6.3×10^{-6}.
  - Kerr prograde ISCO α = 1/3 to 4 significant figures on deep grids.
  - Photon sphere + horizon α = 1/2.
  - Retrograde ISCO linear with leading coefficient exactly 45/16 (empirically measured first, then derived analytically via exact cancellation of fractional-power terms in the BPT retrograde combination).
  - All results produced with the V4 typed primitives (directional_alpha_probe ± sweep_signature companion) on real geodesic observables, with explicit formulation-burden vs genuine-structure separation.
  - This is the strongest external validation + application of the framework since the v4 draft.

**Decision required**: Whether (and at what depth) to add a short "Applications to general-relativistic critical phenomena" section or paragraph citing the whitepaper + derivation. This is the most dramatic "I have since made progress that strengthens" result.

---

## Recommended v5 Revision Priorities (in order)

1. **Corrective reframing (highest credibility impact)**: Apply the HISTORICAL_RECORD supersession flags + the user's map above to Thm 3 (cross-fixture), the "in general" language, and the precision-separation status. Add the BACL + c2 derivation subsection. This directly addresses the "latent drift risk" called out in the audits.

2. **Citation hygiene**: Every major claim gets at least one precise pointer to the report directory or closeout.md listed above. Remove or qualify any phrasing that presents empirical observations as derived theorems.

3. **Integrate the two new orthogonal axes** (multi-precision from task017c + same-precision sweep signature from task035/036) into the self-reference discussion.

4. **GR applications** (scope decision): Add as new high-visibility content if desired. Even a 1–2 paragraph + table version is a major strengthening.

5. **Open challenges update**: Mark the two real gaps as still open (with pointers to V3 task023 for the iterated-log case). Note progress on the lattice derivation (was Open Challenge #2, now closed via BACL+c2), refinery (task032), path-basis (029b), etc.

6. **Version / date / provenance note**: Bump to v5, update date, add a short "Changes since v4" section or appendix that points to this mapping document.

---

## Next Concrete Steps

- Review this mapping for accuracy / completeness.
- Decision on GR whitepaper inclusion + desired depth.
- I will then produce either:
  - A detailed v5 delta plan (section-by-section edit list with exact new wording + citation insertions), or
  - Direct search/replace + new section drafts against the .tex (with the mapping as the controlling document).

This structure keeps the revision disciplined, traceable to real artifacts, and resistant to future drift. The paper will read as "the empirical claims of v4 have been grounded in subsequent substrate derivations, with the framework now demonstrated on real GR critical phenomena."

Let me know corrections to the mapping or the inclusion decision and I'll proceed.