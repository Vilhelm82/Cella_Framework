# PFC-4 PREREG — the corner-valuation theorem

**Frozen 2026-07-07.** Opening the frontier campaign of PFC: read the leading curvature order
of a multi-face reflection corner off the local germ, without a global scalar expansion.

## The question

At a codimension-`k` corner where `k` boundary faces meet, and along an approach path scaling
each vanishing coordinate as `x_j ~ ρ_j ε^{a_j}`, the scalar curvature blows up as
`R ~ ε^{−m(a)}`. **What is `m(a)`, from the germ alone?**

## The claim (codim-2, the opening target)

Two faces `{x=0}`, `{y=0}` meet with single-face orders `p_x, p_y` and corner-residue weights
`r_x, r_y` (the power with which each face's leading curvature coefficient vanishes/blows
approaching the corner). Then `R` near the corner has a **polar Newton polytope** with two
vertices

    v_x = (−p_x, r_y),   v_y = (r_x, −p_y),

and the order along `x=ρ ε^{a_x}, y=ε^{a_y}` is the **support function**

    m(a) = max_v ( −⟨a, v⟩ ) = max( p_x a_x − r_y a_y,  p_y a_y − r_x a_x ).

## Acceptance criteria (what counts as proof)

1. **Reduction to face data.** The corner order depends only on `(p_x,p_y,r_x,r_y)`, i.e. on the
   two single-face PFC laws (order + residue weight), NOT on the full metric.
2. **Support-function duality.** `m(a)` is piecewise linear (a Newton polygon); each edge is one
   face's contribution; the vertex is the balanced direction.
3. **Milder-corner phenomenon.** `min_a m(a)` can be strictly below `min(p_x,p_y)`.
4. **Front-face coefficient.** At a facet-parallel (balanced) direction the whole facet is
   optimal, so the leading coefficient is a facet sum (a genuine mixed term neither face sees).
5. **Genericity condition.** The correct input is the face data; a pure single-monomial
   ("toric") metric is non-generic and yields a milder (wrong) wedge — the theorem must say when
   the generic polytope applies (no accidental cancellation).

## Method

- Support-function machinery: exact convex geometry (support function of a 2-vertex polytope).
- KN instance: vertices from **certified** face data (`lead7_test6` residues `C_Ω~Q²`, `C_Φ~J²`;
  order-4 from the `−m(m+5)/B` law at `m=2`), compared to the `lead7_test9` direct-curvature
  wedge `max(4a−2,4−2a)`.
- Synthetic instances: hand-built diagonal metrics with controllable corners, exact-partial
  curvature, wedge read off directly, vertices recovered, pole-depths matched to the measured
  single-face orders. Use `(4,4)` and `(4,3)` corners to show the rule is not KN-specific.

## Status

**OPENING RESULT — DONE** (`verification/pfc_test2_corner_valuation.py`, byte-stable ×2):
criteria 1–5 verified for KN (from certified face data → the Test 9 wedge) and for synthetic
`(4,4)` and `(4,3)` corners (direct curvature); the toric non-genericity is exhibited. The
corner order drops below both faces (order-4/order-4 → order-2; order-4/order-3 → order-2).

**OPEN (campaign body):**
- **General proof** of the vertex rule `v = (residue-weight, −face-order)` for arbitrary
  diagonal inverse-channel germs (not case-by-case), with the precise **cancellation condition**
  under which the generic polytope holds (the toric counterexample shows it can fail).
- **Codimension ≥ 3** corners (Newton polytope in `ℝ^k`, `k≥3`).
- **Front-face coefficient classification** — the facet-sum "projective" coefficient as a
  function of the balanced-direction data (the KN mixed term `M` is the `k=2` instance).
