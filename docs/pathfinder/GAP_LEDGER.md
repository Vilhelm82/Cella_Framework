# Pathfinder gap ledger

**Date:** 2026-07-12
**Scope rule:** an entry appears here only when the supplied corpus genuinely
lacks the mathematical derivation or required native method.  Nothing in this
ledger is deferred implementable work; every family whose mathematics the
corpus supplies is implemented and registered (39 families live).

| # | Missing capability | Exact missing native method | Source location of the gap |
|---|---|---|---|
| 1 | Newton-wedge front-face coefficient on facet-parallel approach directions | Projective front-face coefficient classification when a direction collects an entire polytope facet (neither single-face law resolves it) | `paper/pfc_normal_forms.tex` §Higher-codimension corners — stated OPEN in the corpus; `newton_wedge_corner` records it as an exceptional branch |
| 2 | Codimension ≥ 3 corner laws (Newton polytope in R^k, k ≥ 3) | k-dimensional polar-vertex rule and support-function classification beyond two parity variables | `paper/pfc_normal_forms.tex` §corners ("codim ≥3 … remain OPEN"); contract scope of `newton_wedge_corner` is codim 2 |
| 3 | Closure monodromy over F(J) (rotating closure, R9/R13 front) | A theorem promoting the generic augmented wreath closure to the rotated function-field closure; the corpus explicitly forbids the promotion | `docs/files/ROTATING_KUMMER_RANK_JUMP_LEMMA_REPORT_2026-07-10.md` §7.5 "Do not promote closure monodromy"; recorded as a refusal stratum in `rotating_kummer_rank_jump` |
| 4 | Non-coprime directive self-glue coupling (gcd(m_D, k) > 1 layer towers) | The iterated intermediate wreath structure for non-coprime coupled trinomials ("richer intermediate iterated wreath — not worked out") | `Reference_Material/papers/current/self_glue_monodromy.txt` §12; `self_glue_exponent_gcd` covers the gcd law C_d wr S_{m/d} only |
| 5 | Nonemptiness of higher-codimension collision strata | A compactified discriminant scheme fixing which optional colored partitions are realized; the intrinsic inertia classification (Thm 13.1) is complete without it | `docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md` §1, §14; refusal stratum `poset_node_outside_declared_open` in `lazy_realization_poset` |
| 6 | Transcendental real-constant pins (elliptic third-kind CPV values) | Native certified real evaluation (interval/exact-real) of complete elliptic integrals; only the exact algebraic sub-gates (λ(1−λ)=1/8, residue = 4, Φ₂(128,10976)=0) are natively scoutable | `Reference_Material/papers/current/DBP_Curvature_Constants_Corrected_Formulation.md` (a certified-constants ledger, not a route theorem); Module R obligation in `CELLA_ARCHITECTURE_v1.3.md` §28 |
| 7 | Carrier-required curvature classification for n ≥ 5 | The general-(n,r) loss-shape carrier decomposition; the corpus certifies the shape-operator identity as MEASURED only for n=3, r=1,2 and supplies carrier forms only to n=4 | `Reference_Material/papers/current/Three_Channel_KG_New_Math_Extension.md` §5–6; `canonical_invariant_reduction` emits the general-r route with the identity as an external obligation |
| 8 | Wild / residue-characteristic-two inertia | Non-tame local inertia classification (the corpus classification is tame with residue characteristic ≠ 2 throughout) | `docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md` §3 hypotheses; `CELLA_ARCHITECTURE_v1.3.md` §28 research obligation; refusal `wild_or_residue_characteristic_two` in `branch_inertia_stratification` |

Every entry above is carried in the corresponding provider contract as an
explicit exceptional branch or refusal stratum, so the boundary is visible at
route-selection time rather than silently absorbed.
