# Transfer Function Exponent Family — v5 Independent Work Bundle

**Created**: 2026-05-30  
**Purpose**: Self-contained package for updating `transfer_function_exponent_family_v4.tex` to v5 and continuing related R&D **independently** of the full V4 engine codebase.

This bundle contains only the artifacts, reports, and planning documents needed for the paper revision work. It respects the scope decisions made on 2026-05-30:
- GR critical exponents work (whitepaper, ISCO/Kerr recoveries, 45/16 derivation) is **excluded** (no-go for the current v5 paper update).
- Focus is on grounding the existing claims using the dedicated V4 campaign artifacts.

## Contents

### SOURCE_PAPER/
- `transfer_function_exponent_family_v4.tex` — the May 14 2026 baseline paper (616 lines)

### PLANNING/
- `transfer_function_exponent_family_v4_to_v5_artifact_mapping.md` — authoritative claim-to-artifact inventory (the user's detailed list + cross-checks). This is the source of truth for what evidence exists for every claim.
- `transfer_function_exponent_family_v4_to_v5_revision_plan.md` — detailed section-by-section delta plan. **Read this first** before editing the paper.

### PROVENANCE/
- `HISTORICAL_RECORD.md` — canonical result index with the explicit "SUPERSEDED" flags on the v4.tex claims (cross-fixture universality, Theorem 3 labeling, precision-scaling presentation).
- Key `_audit/` synthesis files (03, 04, 05, 09, 13) that provide the attack-surface analysis and later reconciliation.

### REPORTS/
Curated subset of the most important evidence directories (7 MB total):
- `task017c_multi_precision_theorem2/` + summary — precision-scaling separation (Theorem 2 / b_k) — the R²=1.0 regular-region result and the three partial sub-claims.
- `task024b/`, `task027/`, `task028/`, `task029c/` — the four original fixtures with full campaign outputs.
- `bacl_invariant_audit/`, `bacl_multi_format_audit/`, `bacl_subnormal_audit/` — the BACL invariant (proven).
- `c2_lattice_substrate_derivation/`, `c2_lattice_sharpness_audit/`, `c2_theorem_scope_gate/` — the substrate-derived c2 integer-lattice theorem (this is the big one that turns empirical observations into derived results).
- `conjecture_c_proof_audit/` — required for the n=2 clean case.
- `task031_sterbenz_audit/`, `task030_refinery_mvp/`, `task032_cross_fixture_refinery_audit/` — Sterbenz + sub-lattice alignment / refinery findings.
- `task029_path_basis_rank_clustering/`, `task029b_methodology_refinement/` — path-basis rank work.
- `task035_sweep_signature_probe/`, `task036_alpha_probe_sweep_signature_companion/` — the orthogonal same-precision diagnostic (relevant for self-reference discussion).
- `task023_iterated_logarithm_discovery/` — the V3 material for the one real remaining gap (non-algebraic retest).

### SCRATCH/
Minimal set of scripts that demonstrate direct measurement of the transfer law / α-1 (the ones explicitly listed in the mapping for Theorem 1):
- `transfer_function_slope_test.py`
- `local_slope_field.py`
- `sqrt_alpha_probe.py`, `radical_family_alpha_probe.py`, `cbrt_alpha_probe.py`, `cbrt_alpha_probe_mpmath_oracle.py`

### CONTEXT/
- `V4_GLOSSARY.md` (full) — definitions and cross-references.
- `CAMPAIGN_DISCIPLINE.md`, `LIVE_CAMPAIGNS_LEDGER.md` (selected sections) — process context.

## How to Use This Bundle for Independent Work

1. **Start here**: Read `PLANNING/transfer_function_exponent_family_v4_to_v5_revision_plan.md` completely.
2. Use `PLANNING/transfer_function_exponent_family_v4_to_v5_artifact_mapping.md` as the living table of what evidence backs every claim in the paper.
3. The `HISTORICAL_RECORD.md` (PROVENANCE/) tells you exactly which statements in the v4.tex are flagged as over-reaching.
4. When you edit the paper, every changed claim should get a citation to one of the `REPORTS/` subdirectories (e.g. `Reports/c2_lattice_substrate_derivation/closeout.md`).
5. The two genuine gaps (finite-window-bias harness and iterated-log V4 retest) are documented as still open — do not claim progress on them.

## What Is Deliberately Excluded
- All GR critical phenomena work (whitepaper, ISCO/Kerr/Choptuik scripts, 45/16 derivation, etc.) — per explicit scope decision 2026-05-30.
- The full V4 source code (`src/`, `tests/`, most of `scratch/`).
- The entire uncurated `Build_Docs/Reports/` (hundreds of files). Only the paper-relevant campaigns are included.
- Any large binary artifacts or full campaign raw data beyond what is in the selected report dirs.

This bundle is designed so you can reason about, edit, and reason about the mathematical/empirical claims in the paper without needing the live V4 engine running.

## Recommended Next Actions (when working independently)
- Produce v5.tex using the revision plan as checklist.
- Consider adding a short "Provenance" appendix in v5 that points back to the mapping document.
- If you discover new supporting evidence or close one of the two real gaps while working, document it in the same style as the existing report directories so it can be merged back later.

