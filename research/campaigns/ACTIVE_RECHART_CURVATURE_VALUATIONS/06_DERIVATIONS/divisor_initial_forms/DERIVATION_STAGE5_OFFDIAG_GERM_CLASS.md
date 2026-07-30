# Stage 5 derivation — the framed monomial-unit germ class

**Proof obligations discharged:** PO-18, PO-19, PO-20 (one-divisor scope), PO-21
**Falsification gates:** `05_VERIFICATION_NEW/off_diagonal_germs/` — four gates, all exact,
all passing (plus the shared exact-curvature harness `curvlib.py`, validated on the unit
two-sphere, flat space, and the pure parity models).

---

## Part A — scoped to what the paper requires

### A.1 The class and its closure (PO-18)

`g = E^T diag(z^{p_i} h_i) E` near the smooth divisor `D = {z = 0}`, with `E` smooth
invertible up to `D` and `h_i` smooth nonvanishing on `D`.

**Closure theorem.** Under any boundary-adapted rechart `z = u(z',y') z'` (`u|_D != 0`),
`y = psi(z',y')`, the pullback is again a class member with the SAME exponent vector:

```
g' = E'^T diag(z'^{p_i} h'_i) E',    E' = (E o phi) J,    h'_i = (h_i o phi) u^{p_i} x unit,
```

`J` the rechart Jacobian. Proof is a two-line factorization (`z^{p_i} = u^{p_i} z'^{p_i}`,
congruence by `J`); gate W1 verifies the exact matrix identity plus unit/invertibility at
the divisor. The class therefore contains every smooth off-diagonal rechart pullback of the
diagonal normal forms — the plan's minimum requirement — with no enlargement needed
(decision gate of plan §Stage 5 resolved: the class is closed; no patching).

### A.2 Determinant and inverse valuations (PO-19)

- **Determinant rigidity:** `det g = z^{sum p_i} (det E)^2 prod h_i` exactly (gates W2/I1).
  Inside the class the determinant valuation NEVER shifts; a shift requires `det E|_D = 0`,
  i.e. leaving the class. Falsification item 4 in its determinant form is therefore a
  **class-boundary event**, typed, not an interior surprise.
- **Inverse law:** `ord_z (g^{-1})_{ij} >= -max_k p_k`, with equality on the named
  noncancellation stratum `E^{-1}_{i k*} E^{-1}_{j k*}|_D != 0` (`k*` the maximal
  exponent index). Off the stratum the valuation JUMPS (exact witness, gate I3:
  an entry jumps from the naive `-4` to `0` while `det` stays rigid at `+5`).

### A.3 Curvature initial data (PO-20, one divisor)

- Universal finite bound: `ord_z R >= 2(min p - max p) - 2` (each curvature term carries
  at most two inverse factors, two derivatives, one metric factor); random exact members
  confirm (gate V1).
- The leading term is finite-jet data: perturbing `E` and `h` at `z^5` changes nothing in
  the leading order or coefficient (gate W3) — the germ-level seed of PO-24.
- `E = I` reduces to the diagonal calculus exactly: generic collapse gives order 3 with
  coefficient `(1/A2)(P1/P0)` (gate V2).
- **Honest scoping datum:** off-diagonal members do NOT inherit the diagonal Newton
  vertices. Gate V1 exhibits members with `p = (3,-2)` whose curvature order is `-2` or
  even `0`, far from the diagonal vertex `-(p_0+2)`. All leading-term claims for the
  off-diagonal class must go through the weighted initial form, never through the exponent
  matrix alone (this repeats, off-diagonally, Paper II's Consequence 7.8).

### A.4 Named degeneracy strata (PO-21)

| stratum | algebraic condition | effect (witnessed) |
|---|---|---|
| class boundary | `det E|_D = 0` | determinant valuation shifts |
| unit failure | some `h_i|_D = 0` | exponent vector ill-defined |
| inverse cancellation | minor zeros of `E^{-1}|_D` at the extreme exponent | inverse valuation jump (I3) |
| drift balance | `sum_alpha P_{alpha,1}/P_{alpha,0} = 0` | order drops 3 -> 2 (X1/X3) |
| frame activity | `E` z-dependent with no diffeo origin | curvature created from flat core (X2) |

Each is a typed stratum with an equation, not an exception policy.

---

## Part B — complementary expansion (use-case-agnostic)

### B.1 What the class really is

The datum `(E, P, h)` is a smooth frame `E` for a z-graded quadratic form. The class is
the orbit of diagonal monomial germs under the two groups that act in applications:
boundary-adapted diffeos (geometry-preserving) and smooth frame dressings
(geometry-CHANGING — gate X2). Keeping these separate is the load-bearing distinction:
closure (A.1) concerns the first group; the valuation laws (A.2, A.3) are statements about
a FIXED member, uniform over the second.

### B.2 Direct-sum comparison (plan task "compare with weighted symmetric-matrix germs")

A general weighted symmetric germ `g_{ij} = z^{w_ij} u_{ij}` need not factor as
`E^T D E` with smooth invertible `E`; conversely every class member is a weighted
symmetric germ with `w_ij >= min(p)` and unit structure controlled by two smooth objects
only. The class is the correct middle ground: strictly larger than recharted diagonals
(X2), strictly smaller than arbitrary weighted germs — and it is the LARGEST subclass on
which the determinant valuation is rigid (A.2), which is exactly what the valuation
theorems consume. This is the mathematical cause for choosing it, stated as the plan
demands.

### B.3 Boundaries

- Normal crossings (several divisors) for the off-diagonal class: OUT of the first paper;
  the diagonal codimension-k theory stays available as the retained appendix.
- Real-analytic vs smooth: all gates run on polynomial data; smooth flat perturbations are
  covered only through the first finite nonzero jet (same wall as Paper II Cor 3.3).
