# CL-F4 — n-UNIFORMITY OF THE DEGREE-≤3 INVARIANT LAYER
**Status: PROVEN (derivation) + CERTIFIED at the (d,n) grid ×2 (records
`d3a0cfff`, PREREG_F4 pin `63dfe44a`). GROUNDED — Will, S-2026-07-05b
("ratify, go 3b.3").**

## Theorem (correspondence + stabilization, all n, all d)
Degree-d monomials on the pair module V_n = ℚ^{pairs} correspond to
multisets of d edges = d-edge multigraphs on n labeled vertices; the S_n
action permutes vertices, so invariant-monomial orbits = isomorphism
classes of d-edge multigraphs with ≤ n non-isolated vertices, and the
orbit sums (one per class) are a basis of the degree-d invariants. Hence:
```
a_d(n) = #{ d-edge multigraph iso classes with support ≤ n }
a_d(n) = a_d(2d)  for all n ≥ 2d      (a d-edge multigraph has ≤ 2d
                                        non-isolated vertices)
```
*Proof.* Orbit sums of a permutation action are a basis of the invariants
(disjoint supports); the support bound is immediate; for n ≥ 2d every iso
class is realizable and distinct classes stay distinct (any isomorphism of
supports extends to S_n). ∎

## The degree-≤3 table (CERTIFIED ×2, both computation paths, n = 3..8)
```
a₁(n) = 1                        n ≥ 2
a₂(n) = 3   (n ≥ 4);   a₂(3) = 2      [missing type: 2-matching]
a₃(n) = 8   (n ≥ 6);   a₃(5) = 7 ; a₃(4) = 6 ; a₃(3) = 3
```
The stable degree-3 basis, n-uniform (with vertex supports):
triple edge (2); double+adjacent (3); triangle (3); double+disjoint (4);
path P₄ (4); star K₁,₃ (4); adjacent-pair+disjoint (5); 3-matching (6).
**Boundary mechanism (closes the F3 datum):** a₃(5) = 7 because exactly
the 3-matching needs 6 vertices; a₃(4) = 6 loses also the support-5 type;
a₃(3) = 3 keeps only supports ≤ 3. The "a₃ n-stability" observed at
n = 6,7 (WALL_VERDICT) is the theorem's 2d-threshold: stability begins at
n = 2·3 = 6, provably for all larger n.

## Consequences banked
- CL-F4's staked target met: Molien counts closed-form in n (piecewise-
  stable with proven thresholds), invariant bases n-uniform (the multigraph
  orbit-sum families, defined identically at every n).
- F3's separation result now carries n-uniform meaning: the 1+3+7
  functions used at n=5 are the n=5 specialization of the stable 1+3+8
  family (minus the 3-matching, absent at n=5).
- Build note (ink): one instrument defect — rep_utils.conjugacy_classes
  returns (cycle_type, size) pairs, misread on first invocation; caught by
  traceback before any verdict; fixed, reran clean.

*Nothing canonical until Will signs.*
