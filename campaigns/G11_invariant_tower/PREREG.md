# G1.1 PREREG — frozen before implementation

All pins derived 2026-07-06 from the definition below via TWO independent exact
routes (principal-minor sums and Faddeev–LeVerrier char poly on A, asserted equal on
every corpus row), with geometric sanity confirmed on spheres/cylinder and two
retrodictions against standing certificates (gate_03's σ₁² = 72/343; RC-1's saddle
K_G = −1/9). Frozen before any implementation code. Pins are immutable; failures are
findings, triaged never edited mid-run.

## Definition (fixes the convention — the sign IS part of the pin)

```
A     = P H P ,  P = I - g g^T / q ,  q = g.g          (exact, rational)
c_r   = e_r(A)  (sum of r x r principal minors; A g = 0 kills e_n)
sigma_r = (-1)^r c_r / q^(r/2) ,   r = 1 .. n-1        (shape operator S = -(1/sqrt q) A|_tangent)
```

Parity typing (the parity law, enforced at the type level):
```
even r : sigma_r = c_r / q^(r/2)              -> Fraction
odd  r : sigma_r = b*sqrt(q), b = -c_r / q^((r+1)/2)
         b == 0 or q a rational square        -> Fraction (exactly rational)
         else                                 -> QSqrt(0, b, q)   (radicand q, one sqrt per context)
```

Gauge invariance mechanism (staked, tested at P4): P annihilates g, so
`P (g a^T + a g^T) P = 0` — A is IDENTICALLY gauge-invariant, hence the whole tower.

## P1 — corpus pins (retrodicted through the API)

```
keystone   F = x1^2+x1x2+x3^2-3     @ (1,1,1)   g=(3,1,2)    q=14
           sigma = ( QSqrt(0,-6/49,14),  -3/49 )
sphere3    F = x^2+y^2+z^2-14       @ (1,2,3)   g=(2,4,6)    q=56
           sigma = ( QSqrt(0,-1/14,56),  1/14 )
cylinder   F = x^2+y^2-5            @ (1,2,7)   g=(2,4,0)    q=20
           sigma = ( QSqrt(0,-1/10,20),  0 )
saddle     F = x3-x1x2              @ (1,1,1)   g=(-1,-1,1)  q=3
           sigma = ( QSqrt(0,-2/9,3),   -1/9 )      [sigma2 cross-route: RC-1 K_G pin]
ellipsoid  F = x^2+2y^2+3z^2-6      @ (1,1,1)   g=(2,4,6)    q=56
           sigma = ( QSqrt(0,-6/49,56),  9/49 )
monkey     F = x3-x1^3+3x1x2^2      @ (0,0,0)   g=(0,0,1)    q=1 (square)
           sigma = ( 0, 0 )                          [odd value rational by square q]
sphere4    F = x1^2+..+x4^2-30      @ (1,2,3,4) g=(2,4,6,8)  q=120
           sigma = ( QSqrt(0,-1/20,120),  1/10,  QSqrt(0,-1/1800,120) )
```

Retrodictions banked in this derivation: keystone sigma1^2 = 72/343 (gate_03 pin,
sign now fixed NEGATIVE by the convention above); saddle sigma2 = -1/9 = RC-1's
pinned K_G for the same fixture.

## P2 — parity typing rows

Every corpus row: even slots are Fraction; odd slots are QSqrt with radicand exactly
q — except monkey (q = 1, square: rational by theorem, Fraction) and any zero odd
value. Type checks are part of the battery, not just value checks.

## P3 — cross-route (K-1 armed): sigma2 == labeled channel sum

For every n=3 corpus row with all gradient components nonzero (keystone, sphere3,
saddle, ellipsoid): `sigma_tower[1] == kc + kint + ks` from
`channels_n3_crosscheck`, plus the labeled triples pinned:
```
keystone  (kc,kint,ks) = (-1/49, -3/49, 1/49)
sphere3   (0, 0, 1/14)      [pure self]
saddle    (-1/9, 0, 0)      [pure coupling]
ellipsoid (0, 0, 9/49)      [pure self]
```
ASYMMETRY ROW (pinned deliberately): cylinder and monkey have a zero gradient
component — the TOWER computes (invariants need no chart; regularity is g != 0
only) while carrier/cross-check refuse ROLE_CHART_UNAVAILABLE on the same block.
Chart conditions and regularity conditions are different strata; the battery pins
both behaviours on one fixture.

## P4 — gauge invariance (K-3 armed)

Full tower exactly invariant under H -> H + g a^T + a g^T on every corpus row, gauge
rows: n=3 (1,0,0),(0,1,0),(1,-2,3),(-1/2,5,1); n=4 (1,0,0,0),(1/3,-2,5,7).

## P5 — purity wiring

```
U1  R-epoch through Account leaves the whole tower fixed (keystone, a=(1,-2,3))
U2  M-defect E01=E10=1 on keystone moves the tower; PINNED WITNESS:
    sigma' = ( QSqrt(0,-9/98,14), -9/49 )
U3  M-corrected reconstruction recovers the base tower exactly
```

## P6 — refusal rows

```
R1  block len 2                  -> CODIM_UNSUPPORTED
R2  g = (0,0,0)                  -> SINGULAR_GRADIENT
R3  float in jet                 -> TypeError
(component-zero g does NOT refuse the tower: P3 asymmetry row)
```

## P7 — certificates

C1 tower certificate: tier string present ("orders 1..n-1; parity-typed"), QSqrt
value flows through canon; C2 refusal certificate (R1) plain; C3 double-run law.

## P8 — mutants (each MUST FAIL its target)

```
M1  SIGN-FLIP: S = +(1/sqrt q) A  (sigma_odd negated, sigma_even unchanged).
    Must FAIL every odd pin with nonzero value; must PASS even pins —
    demonstrating the sign is pinned by convention, detectable only in the
    odd sector (exactly why the odd sector is a diagnostic layer, LEAD-4).
M2  NORMALIZATION: q^r in place of q^(r/2)-scheme. Must FAIL nonzero pins.
M3  RADICAND-CONTEXT: odd sigma emitted as QSqrt(0, b, 4q) (wrong context,
    non-square). Must FAIL pins — one sqrt per context is a pinned identity,
    not a formatting choice.
```

## Kills

K-1 cross-route mismatch (P3) -> route split, HALT, triage sigma machinery vs
channel formula. K-2 parity violation on any row -> parity law misread, HALT.
K-3 gauge sweep failure -> transport misread, HALT.

## Verdict rule

Close only if: P1-P7 all pass, P8 mutants all bite, full gate suite (zero..04, 10,
11) green x2, gate_11 stdout byte-stable x2.
