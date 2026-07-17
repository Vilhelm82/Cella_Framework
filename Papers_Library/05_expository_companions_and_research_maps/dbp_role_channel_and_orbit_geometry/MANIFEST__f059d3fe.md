# MANIFEST — Campaign H: RoleChSpec Symbolic Proof Extraction

**Campaign id:** `campaign_h_rolechspec_symbolic_proof_extraction`
**Tier:** eval-tier / proof-extraction only. No substrate promotion. Does not change Campaign A/D/E/F/G artifacts. **Campaign type: symbolic theorem extraction.**
**Discipline:** exact symbolic algebra (**SymPy 1.14.0** + `fractions`); no float / no tolerance / no NumPy in any verdict path; RoleChSpec recomputed (no cached Campaign G labels); deterministic, two-run byte-identical (same SymPy version).

## Pre-registration
- [`PREREG.md`](PREREG.md) — recorded before any generated report. States the theorem target, the gauge-normal form, and the proof found (r=1 linear recovery, rank 3, minor `16 g2⁴(g1²+g3²)` nonzero on the regular Q-locus).

## Code (eval / proof-extraction package)
`src/lloyd_v4/evals/rolechspec_symbolic_proof_extraction/`

| module | role |
|---|---|
| `symbols.py` | symbolic `g`, `H`, `O` |
| `gauge_normal_form.py` | `G_g`, `a_i = H_ii/(2 g_i)`, `H_perp`, obstruction, `gauge_image_rank` (Lemma H1) |
| `rolechspec_symbolic.py` | symbolic rechart + channel vectors (r=1,2) per role (Lemma H2/H3) |
| `injectivity_ideal.py` | r=1 coefficient matrix, rank, recovery minor, `nonzero_on_regular_Q`, certificate (Lemma H4) |
| `exceptional_locus.py` | typed exceptional strata; sum-of-squares definiteness over Q (CL-H5) |
| `verify_against_campaign_g.py` | symbolic↔Campaign-D bridge + iff retrodiction (CL-H6) |
| `char_boundary.py` | char-≠2 single-minor cert (CL-H8) + char-2 gauge-rank collapse (CL-H9) |
| `raw_chart_rolechspec.py` | raw chart-level RoleChSpec (full `H`, pre-gauge-normal); char-2 atlas, phantom `g gᵀ`, faithfulness resolution (CL-H10) |
| `run_campaign_h.py` | assemble proof, grade CL-H1…H10, byte-stable emit, verify |
| `mutants.py` | 10 symbolic/proof mutants (§10) |

Reuses the Campaign D RoleChSpec engine (recomputation) for the retrodiction bridge only.

## Tests
`tests/test_campaign_h_*.py` — gauge_normal_form, symbolic_rolechspec, injectivity_checks, exceptional_locus, retrodict_campaign_g, mutants, byte_stability. **All pass.**

## Artifacts (this directory)
`records.jsonl` (per-role closed formulas + lemma certificates), `summary.json` (CL-H1…H7 + Theorem H), `sha256.txt`, and the reports `GAUGE_NORMAL_FORM_PROOF.md`, `SYMBOLIC_ROLECHSPEC_FORMULAS.md`, `INJECTIVITY_IDEAL_REPORT.md`, `EXCEPTIONAL_LOCUS_REPORT.md`, `CAMPAIGN_G_RETRODICTION.md`, `MUTATION_REPORT.md`, `CLAIM_LEDGER.md`.

## Reproduce
```bash
python -m lloyd_v4.evals.rolechspec_symbolic_proof_extraction.run_campaign_h \
    --out results/rolechspec_symbolic_proof_extraction
```
`run_campaign_h.verify(dir)` rebuilds and checks byte-identity. Byte-stability holds for the pinned SymPy version (1.14.0).

## Result (headline)
Status **PASS**, no kill fired. **Theorem H PROVED (symbolic, regular Q-locus):** RoleChSpec is a faithful invariant of `Sym_3(Q)/Im(G_g)`, via the gauge-normal form and an explicit linear recovery of `O` from the `r=1` channels, with no exceptional stratum beyond regularity over Q. The finite-tested Campaign G theorem is upgraded to a symbolic theorem candidate.

## Characteristic-0 strengthening (additive — CL-H8 / CL-H9; `char_boundary.py`, `CHAR2_BOUNDARY_REPORT.md`)
An independent audit sharpened the ceiling from "over Q" to **char ≠ 2**: the coupling-rows minor `det(0,2,4) = 32/(g1 g2 g3)` is a unit-numerator certificate of rank 3 on the regular locus over any field where 2 is invertible (**CL-H8**), so the two-Gröbner saturation is vacuous. char 2 is a **derived** wall (**CL-H9**): the gauge `G_g(a)_ii = 2 g_i a_i` is diagonal-blind, `Im(G_g)` drops 3→2, and the quotient is `k⁴` not the `k³` carrier `O`. CL-H4/CL-H5 (the over-Q headline) are unchanged.

## Characteristic-2 faithfulness (additive — CL-H10; `raw_chart_rolechspec.py`, `RAW_CHART_ROLECHSPEC_REPORT.md`)
The char-2 faithfulness analog flagged OPEN in CL-H9 is **resolved** by the **raw chart-level RoleChSpec** (the channel engine on the full Hessian `H`, before the gauge-normal substitution — denominators are `g`-monomials, no `1/(2g)`, so it is defined in char 2 and equals the gauge-normal object over char ≠ 2). In char 2 it is invariant under the diagonal-blind gauge **and** under the rank-one **phantom** `g gᵀ` (= `G_g(g/2)` over ℚ, outside the char-2 gauge image). The blind spot is **exactly** `⟨g gᵀ⟩` (1-dim, finite-enumeration certified): the naive 4-dim `{H11,H22,H33,ell}` analog **fails by one dimension**, and RoleChSpec is **faithful on the corrected 3-dim quotient** `Sym₃/(Im G_g ⊕ ⟨g gᵀ⟩)` — the **same dimension (3)** as the char ≠ 2 carrier `O`. `K-H9` armed (mutation-checked live). PENDING Will's sign-off. Tests: `tests/test_campaign_h_raw_chart_rolechspec.py` (16, all pass).
