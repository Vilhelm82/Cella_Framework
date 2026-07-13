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
5. **Cancellation condition.** The theorem must give the exact locus where a vertex disappears
   (its coefficient vanishes). [NOTE, corrected 2026-07-07: an early draft mis-stated this as
   "the single-monomial toric germ is non-generic" — that was a labeling error (swapped x,y
   weights). With correct weights the single-monomial germ realises the polytope; raw weights
   and face data are equivalent inputs. The true condition is `A=0 / B=0`, below.]

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
criteria 1–4 verified for KN (from certified face data → the Test 9 wedge) and for synthetic
`(4,4)` and `(4,3)` corners (direct curvature). The corner order drops below both faces
(order-4/order-4 → order-2; order-4/order-3 → order-2).

**GENERAL VERTEX RULE — PROVEN** (`verification/pfc_test3_vertex_rule.py`, byte-stable ×2). As a
closed symbolic identity, for `g_i=h_i(s)x^{p_i}y^{q_i}u_i` the polar part of R is supported on
exactly `V_1=(−(p_1+2),−q_1)`, `V_2=(−p_2,−(q_2+2))`, `V_0=(−p_0,−q_0)` with EXPLICIT
coefficients `A(p_0,p_1,p_2)/(2h_1)`, `B(q_0,q_1,q_2)/(2h_2)`, and an s-jet `C_0`;
`A=−p_0²+p_0p_1−p_0p_2+2p_0+p_1p_2−p_2²+2p_2`. Criterion 1 (reduction to face data) holds because
`p_x=p_1+2`, `r_y=−q_1`, etc.; criterion 5 (cancellation) is exactly `A=0 / B=0` (or degenerate
s-jet), plus `V_0` polar iff `p_0>0` or `q_0>0`. Unit factors leave the vertices/order fixed, so
the rule holds for generic germs, not just monomials.

**OPEN (campaign body):**
- **Codimension ≥ 3** corners (Newton polytope in `ℝ^k`, `k≥3`).
- **Front-face coefficient classification** — the facet-sum "projective" coefficient as a
  function of the balanced-direction data (the KN mixed term `M` is the `k=2` instance).
