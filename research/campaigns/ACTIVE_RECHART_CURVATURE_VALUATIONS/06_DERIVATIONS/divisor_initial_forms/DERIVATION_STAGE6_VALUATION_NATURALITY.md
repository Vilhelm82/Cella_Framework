# Stage 6 derivation — valuation naturality on the role cover

**Proof obligations discharged:** PO-22, PO-23, PO-24, PO-25, PO-26 (hierarchy retained)
**Falsification gates:** `05_VERIFICATION_NEW/valuation_naturality/` — four gates
(6+6+7+2 checks), all exact, all passing. Gate 6 requirement met: every law below is read
from local germs; the global scalar-curvature rational function is never assembled.

---

## Part A — scoped to what the paper requires

### A.1 Pole-order naturality (PO-22)

Scalar curvature is a scalar: under any boundary-adapted rechart the divisor order of `R`
is invariant (Paper II Thm 6.1 mechanism). Verified exactly for the parity (`k=4`) and
generic (`k=3`) faces under the full unit change `z = (v0(y) + v1(y) z') z'` (gate Q1) and
under shears mixing transverse coordinates (Stage 5 gate V3).

### A.2 The principal coefficient is a weight-k conormal datum (PO-23)

With the plan's convention `z' = u(y) z + O(z^2)`:

```
R = c(y) z^-k + O(z^-k+1)   ==>   c'(y) = u(y)^k c(y),
```

and ONLY `u|_D` enters — the `O(z^2)` part of the rechart feeds strictly lower layers
(gates P1-P3, Q1). Equivalently: `c` is a section of `(N^* D)^{ox k}` (the k-th conormal
power); the paper should state it intrinsically so no silently fixed boundary coordinate
appears. The parity-breaking mechanism is exact: a quadratic rechart term `k2 z'^2`
produces the odd layer `4 m(m+5) k2 / (B c^5) z'^-3` (Prop 6.3 replayed symbolically,
gate P1) — parity preservation is an ODD-coordinate condition.

### A.3 Gauge-free packaging

The defining-function freedom is fully quotiented by proper distance (gate Q2):

```
parity face:   lim R d^2    = -m(m+5)/4
generic face:  lim R d^(3/2) = Theta A^(-1/4) / 2^(3/2),   Theta = sum P_a1/P_a0.
```

### A.4 Finite weighted-jet determination and transverse exclusion (PO-24, PO-25)

Independent replay (direct function-coefficient curvature via the directional-channel
engine — a different engine from the packaged Laurent-jet verifier):

- generic face, all eight coefficients arbitrary functions of `y`:
  `R = (P1/P0 + R1/R0)/A2 z^-3 + O(z^-2)`; the coefficient contains **no derivative of
  any coefficient function** and never sees `A3, P2, R2` (gate J1);
- reflection face: `R = -14/B z^-4 + O(z^-2)`, independent of `B4, C10, C20` and of the
  transverse amplitudes (gate J2);
- the packaged legacy verifier replays from the package with the shim path fixed
  (gate D — the Stage 0 audit flag is discharged, not just noted).

### A.5 Cancellation hierarchy (PO-26)

Retained as frozen (Paper II Thm 7.5) with the Stage 5 witnesses: drift balance drops
`3 -> 2` (typed, next-layer inspected), inverse-cancellation strata named, class-boundary
events separated. Nondegenerate stratum for the generic law: `Theta != 0` exactly.

---

## Part B — complementary expansion (use-case-agnostic)

### B.1 Valuation naturality across the ROLE cover

Combining with Stage 3: each presentation's metric `g^(rho)` is a class member near each
role-pair divisor, and pole order + weight-k principal coefficient are intrinsic data of
`(germ, divisor)` — hence comparable across presentations through the pair-form
dictionary. What may legitimately differ between `g^(rho)` and `g^(sigma)` is which pair
channels the assignment omits (`b_{rho sigma}` missing from both), i.e. the germ itself,
NOT the naturality laws. The complementary paper states this as: **valuation data descend
to the pair-form atlas; they are functors of the germ, and the germ is presentation-
indexed by a controlled rule.**

### B.2 Agnostic statement

For any diagonal-collapse constitutive law (thermodynamic, economic, chemical): the
blow-up rate of the curvature diagnostic at a boundary is chart-free, and its leading
amplitude transforms as a k-th power of the boundary reparametrization — so amplitudes
from different models are comparable only after fixing an intrinsic gauge (proper
distance) or quoting the conormal weight. This is the practical export of Stage 6.

### B.3 Boundaries

- Off-diagonal principal-coefficient FORMULAS (beyond order/weight laws and finite-jet
  dependence) require the weighted initial form of `(E, P, h)` — Stage 5 B; no closed
  off-diagonal coefficient table is claimed in the first paper.
- Codimension >= 2 naturality for the off-diagonal class: out of scope (retained diagonal
  Newton rules cover the diagonal corner case).
