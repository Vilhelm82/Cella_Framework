# CCE-5 stage report v1.0

**Verdict:** `COMPLETE` for the two exact DBP corridors and the fundamental
groupoid they generate.

The indexed E-0003/E-0014/E-0022 material closes the analytic family in the
ordered basis

```text
Y=(K(m), E(m), Pi(m^2/(2m-1);m)).
```

The exact rational connection `Y'=M(m)Y` has singular ledger
`m=0,1/2,1,infinity`. Its third row is independently reconstructed from the
two-variable `Pi(n;m)` connection and the exact E-0022 elimination.

The former absolute-calibration gap is also closed. In relative coordinate
`u=x/m`, the moving branch section `q=1/m` crosses the primary contour exactly
once on each released polygon. On the upper route it crosses from below to
above and contributes `+B`; on the lower conjugate route it contributes `-B`.
The full ordered branch braid acts on compact cycles by

```text
upper: A -> A+2B, B -> B
lower: A -> A-2B, B -> B.
```

Therefore

```text
lambda_up   = +B_- = (0, 1)
lambda_down = -B_- = (0,-1).
```

The exact route-specific relative matrices in basis `(A,B,mu,delta_lateral)`
preserve the primitive boundary vector and restrict to mutually inverse
symplectic compact matrices. Their difference refines the previous quotient
statement to `2B-mu`, while their CPV half-sum has no compact correction.

On the fixed `E_128` trace curve, freezing the primitive real-projective-circle
cycle gives exact comparison coordinates `(a,b,c)=(1,0,0)`; the lower lateral
path has meridian coordinate `c+1=1`.

The upper/lower arrows and their inverses now compose in a common endpoint
basis. Arbitrary endpoint-composable words in `U,L,u,l` have exact compact
and relative transport matrices, typed source/target objects, deterministic
certificates, and inverse/composition laws. This closes the logical expansion
from two isolated calls to their generated groupoid.

The 61-assertion gate covers both corridors, exact connection identities,
branch crossing, symplectic/inverse laws, boundary preservation, compact
corrections, trace comparison, checkpoints, refusals, and hostile mutation.
The proof is geometric and exact; no near-integrality or fitted numerical
monodromy is used.

Production: `engine/src/cella/continuation/cce5.py` (`1cbbbdd2...7c05`). Gate:
`engine/tests/gate_continuation_cce5.py` (`e2e870ab...018b`). Released upper
and lower certificate digests are `64161d83...d9c7` and `da1ad62e...250a`.
The theorem note is `DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md`.

The whole regular `m`-plane is not yet claimed. It needs calibrated local
generators at `m=0,1/2,1,infinity`; the current basis is not logarithmic at
`m=1`, so naive residue exponentiation is insufficient.
