# CLAIM LEDGER — Campaign H: RoleChSpec Symbolic Proof Extraction

Eval-tier / proof-extraction. Graded by `run_campaign_h.py`; byte-stability checked by `run_campaign_h.verify`. Machine-readable mirror: `summary.json → claims`. Nothing canonical until Will signs off.

| Claim | Statement | Verdict | Evidence |
|---|---|---|---|
| **CL-H1** | `Sym_3(Q)/Im(G_g) ≅ Q^3` via `H ↦ O_g(H)` | **PASS** | `H_perp` diagonal = 0; off-diagonals = obstruction; `gauge_image_rank = 3`; obstruction Jacobian rank 3 |
| **CL-H2** | `RoleChSpec_g(H) = RoleChSpec_g(H_perp)` | **PASS** | every chart channel component invariant under `H_perp + G_g(b)` (symbolic) |
| **CL-H3** | closed RoleChSpec formulas in `(g, O)` for all roles | **PASS** | Product/Directive/Substrate charts as exact rational functions; `κ_int = 0`; r1 linear, r2 quadratic |
| **CL-H4** | RoleChSpec equality forces `O = O'` (saturated) | **PASS** | r=1 coefficient matrix rank 3; minor numerator `16 g2⁴(g1²+g3²)`; `O` recovered linearly → injective |
| **CL-H5** | every denominator/singularity component typed | **PASS** | minor numerator factors `16·g2⁴·(g1²+g3²)`; sum-of-squares definite over Q; no stratum beyond regularity |
| **CL-H6** | Campaign G retrodiction | **PASS** | symbolic formulas match Campaign D; 180 sampled pairs, 0 faithfulness / 0 gauge-invariance counterexamples |
| **CL-H7** | mutation controls | **PASS** | 10 symbolic/proof mutants all caught |
| **CL-H8** | injectivity holds on the regular locus over any **characteristic-0** field (and more — any field where 2 is invertible) | **PASS** | explicit single-minor certificate: the coupling-rows minor `det(0,2,4) = 32/(g1 g2 g3)`, numerator the unit `32 = 2⁵`; rank 3 over **char ≠ 2**. (The two-Gröbner saturation is *vacuous* — the minor-numerator ideal is already `⟨1⟩`; this explicit minor is the sharper certificate.) Kill **K-H7** |
| **CL-H9** | char ≠ 2 is a **derived structural wall**, not a margin | **PASS** | in char 2 the gauge `G_g(a)_ii = 2 g_i a_i` is diagonal-blind; the off-diagonal gauge map `[[g2,g1,0],[g3,0,g1],[0,g3,g2]]` has `det = −2 g1 g2 g3` (= 0 in char 2), rank 3→2 (surviving 2×2 minor `−g1 g3`); `Im(G_g)` drops 3→2, quotient `k⁴` not the `k³` carrier `O`; new char-2 invariants `{H11, H22, H33, ell = g3 O12 + g2 O13 + g1 O23}`. ~~Open analog~~ **now RESOLVED by CL-H10** (the derived-wall facts of CL-H9 are unchanged). Kill **K-H8** |
| **CL-H10** | char-2 faithfulness **RESOLVED** via the raw chart-level RoleChSpec | **PASS** | the raw channels (full Hessian, before the gauge-normal substitution) are char-2-defined (`g`-monomial denominators, no `1/(2g)`) and equal the gauge-normal object over char ≠ 2 (CL-H2). In char 2 they are invariant under the diagonal-blind gauge AND under the rank-one **phantom** `g gᵀ` (= `G_g(g/2)` over ℚ, but outside the collapsed char-2 gauge image — its diagonal `g_i²` is unreachable by the diagonal-blind gauge). The blind spot is **exactly** `⟨g gᵀ⟩` (1-dim, finite-enumeration certified, controls visible): the naive 4-dim `{H11,H22,H33,ell}` analog **fails by one dimension**, and RoleChSpec is **faithful on the corrected 3-dim quotient** `Sym₃/(Im G_g ⊕ ⟨g gᵀ⟩)` — the same dimension (3) as the char ≠ 2 carrier `O`. Kill **K-H9** |

## Kill conditions — all armed, none fired

| Kill | Fires when | Status |
|---|---|---|
| K-H1 | normal form fails (diagonal not killed / obstruction mismatch) | silent |
| K-H2 | RoleChSpec depends on gauge diagonal after normalisation | silent |
| K-H3 | injectivity fails generically (regular `O ≠ O'` with equal RoleChSpec) | silent |
| K-H4 | exceptional locus untyped (silent denominator discard) | silent |
| K-H5 | Campaign G retrodiction contradicted | silent |
| K-H6 | float/tolerance leakage in the verdict path | silent |
| K-H7 | the coupling-rows minor is anything other than a nonzero constant over `g1 g2 g3` (char-≠2 certificate fails) | silent |
| K-H8 | the off-diagonal gauge map determinant ≠ `−2 g1 g2 g3`, or a regular-locus 2×2 minor of it vanishes (char-2 collapse facts fail) | silent |
| K-H9 | the phantom `g gᵀ` is visible to the raw RoleChSpec in char 2, or the char-2 blind spot is not exactly the 1-dim `⟨g gᵀ⟩`, or the corrected 3-dim quotient is not faithful (char-2 faithfulness resolution fails) | silent |

**Kills fired: NONE.** Status **PASS** — **Theorem H PROVED (symbolic, regular Q-locus); sharpened to char ≠ 2 (CL-H8), with char 2 a derived wall (CL-H9); the char-2 faithfulness analog is now RESOLVED (CL-H10): faithful on the 3-dim quotient `Sym₃/(Im G_g ⊕ ⟨g gᵀ⟩)`, with the naive 4-dim analog failing by the 1-dim phantom `⟨g gᵀ⟩`.**

> `K-H9` is mutation-checked live: replacing the phantom direction with a genuinely visible perturbation fires `K-H9` and flips CL-H10 → FAIL, status → FAIL.

> Note on IDs: the original audit request named "CL-H6 / K-H6", but those IDs are already taken (Campaign G retrodiction / float-leakage). To stay additive (instruction #4), the char-0 strengthening and the char-2 wall are recorded at the next free IDs **CL-H8 (K-H7)** and **CL-H9 (K-H8)**; the char-2 faithfulness resolution is the next free **CL-H10 (K-H9)**. CL-H4 / CL-H5 (the over-Q headline) are unchanged.

## Theorem H (best outcome)

> For regular `g` and `H1, H2 ∈ Sym_3(Q)`: `RoleChSpec_g(H1) = RoleChSpec_g(H2)  ⟺  O_g(H2 − H1) = 0`. Pass to the gauge-normal representative `H_perp = H − G_g(a)`, `a_i = H_ii/(2 g_i)` (Lemma H1); RoleChSpec depends only on `H_perp` (Lemma H2); its `r=1` channels are linear forms in `O` of rank 3 with a g-only nonzero minor (Lemma H4), so `O` is recovered linearly → injective. Over Q the minor numerator `16 g2⁴(g1²+g3²)` is nonzero on `g1 g2 g3 ≠ 0`, so there is **no exceptional stratum beyond regularity**.

This upgrades the A→D→E→F→G result from a **finite-tested theorem** to a **symbolic theorem candidate on the regular Q-locus**, with the exceptional strata explicitly typed (here: none beyond regularity over Q).

## Discipline
Exact symbolic algebra (SymPy 1.14.0 + `fractions`); no float / tolerance in any verdict; RoleChSpec recomputed (no cached Campaign G labels); eval-tier / proof-extraction only; no substrate modified; two runs byte-identical. **PENDING Will's sign-off.**
