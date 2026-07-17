# STAGE 3b.3 — MINIATURE MODEL — STAGE REPORT (S-2026-07-05b)
**Authority:** PREREG_3B3 (frozen pre-battery, pin `9ddb235b`). **Records:**
grades ×2 identical (`m33_mb_grade_x2.sha`), reads ×2
(`m33_reads_x2.sha`); raw RUR box-only, sha banked. **Envelope:** msolve
~3 min vs 1800 s. **Defect chains: ZERO.** One design defect in ink (below).

## Verdicts
| id | verdict | reading |
|---|---|---|
| MP.0 | PASS (procedure) | M-0 and M-A recorded **DEGENERATE** (msolve dim > 0, grader refused by design); M-B dim 0, ideal_deg 192, grades ×2 |
| MP.1, MP.2a–c | NOT GRADABLE | n=3 rungs are structurally impossible — design defect caught by the dim gate, mechanism identified: perp() puts all slate vectors in g^⊥ and dim Λ²(g^⊥) = C(n−1,2) = 1 at n=3, so every Cayley product lies in the 1-parameter SO(2)_g; ≥2-parameter tie systems are positive-dimensional by construction. Smallest honest chassis analogue = n=4 with 3 params (M-B is critically sized: group dim 3 = #params) |
| MP.3a | **HOLDS** | lead(w) perfect square at n=4 — the D-borne square-lead law SURVIVES at miniature scale |
| MP.3b | **HOLDS** | class(lead·const) trivial, sign + ⟹ **N(D1·D2) = +□ at n=4** — the norm law survives |
| MP.3c | **FAILS** | spectrum [1, 3, 92, 96] — the even Galois split does NOT survive; 352+352 is chassis/scale-specific |

## M4 — mechanism memo (the stage's deliverable)
1. **The laws separate.** At n=4 the norm law (+□) and lead-square law hold
   while the even split is gone ⟹ the norm law does NOT need the even
   split. Two phenomena that were entangled at n=5 are now decoupled; the
   mechanism hunt should target the norm law alone.
2. **A rational tie point exists at n=4** (deg-1 factor): θ = 8281/102860164
   = (91/10142)², so at that point **D1·D2 = (10142/91)² — a literal
   rational square, pointwise**. (Unsurprising that a witness exists below
   the Part-III threshold n≤4; its VALUE being a perfect square is the
   lead.)
3. **Pointwise-h refuted off the rational component, exactly as at n=5:**
   f(z²) is irreducible over the deg-3, deg-92, deg-96 components (reads
   ×2) — θ is not a square in any nontrivial component field. The n=4
   miniature reproduces the n=5 structure: norm-level identity WITHOUT a
   pointwise mechanism.
4. **The ι-swap candidate is DAMAGED:** the nontrivial const classes sit in
   the deg-92/96 pair and are EQUAL (cancelling in the product) — but
   factors of different degrees cannot be exchanged by an involution. The
   shared-class structure therefore is NOT (here) an orbit swap; it points
   at a norm-residue/corestriction mechanism (the Stage-3a "ker
   corestriction" reading) as the primary suspect. The HUNT_ADDENDUM §5
   ι-candidate survives only in weakened form (quadratic-extension symmetry
   of the pair without a variety involution).
5. **The phenomenon is now model-tractable:** 192 points, 3 variables, n=4,
   with an explicit rational point on the variety. Next probes armed (desk;
   not started): (a) extract (t1,t2,t3) at the rational point via RUR
   parametrization — what geometric configuration ties there; (b) symbolic
   3-var elimination on the miniature (the formula-level view A3 asked
   for); (c) miniature Frobenius statistics on the 92/96 pair (Galois-group
   constraints without the n=5 cost); (d) norm-residue mechanism test:
   corestriction kernel structure on the miniature components.

## Ladder economics
n=5 chassis: deg-704 systems, ~12 min/job, formula opaque. n=4 miniature:
deg-192, ~3 min, symbolically approachable, phenomenon intact minus the
even split. The miniature does its job.

*GROUNDED — Will, S-2026-07-05b ("Accept 3b.3 close"). Design-defect row
(n=3 rungs) and all verdicts above carried by byte-stable ×2 artifacts in
records/. §M4 next-fork remains on the desk, unruled.*
