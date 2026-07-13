# ARITH-I PREREG — first-principles reduction + the higher Cohn-Vossen question

**Frozen at open (2026-07-06).** Lean prereg: predictions, retrodiction targets, and
falsification gates, authored before Stage-A derivation code. Origin/[CONTAINER] values
are targets to reproduce in-repo, never evidence (re-verification rule). A gate firing
is a finding, not a failure. Paper-track fence: this campaign sets no engine priorities.

**Open-pin re-verification (done before this freeze):**
`verification/arith_i_open_pins.py`, 15/15, byte-stable ×2, pin
`a2ef103d8f436fe1a2728fe10887574a4b67a4beb5efebd549a8f884aae77d9c`. Re-derived fresh:
family self-check at s=1, `det B = 4(D²+DS+P²)` (⟹ det B ≡ 12 on F=0), K_G = −3/49 at
q = 14, cone eigenvalues (1±√2)/2 & 1, `a²_max = k² = (2−√2)/4`, the keystone constant
by two independent routes (closed form vs direct link arc length, agree < 1e-60), and
the CALC-24 register self-consistency at four sample shears. Nothing below is trusted on
its banked status; the pins above are what bears load.

## FAMILY DEFINITION — pinned at open (K-2 tests it)

```
F_s = D² + s·D·S + P² − 3 ,        keystone s = 1.
```

The symbol `s` is asserted to be the SAME shear as the CALC-24 register `j(s)`; that
identification is the content of K-2. Re-derived general-s consequence (from the open
pins, [CONTAINER]-free, this repo): the bordered-Hessian determinant is

```
det B = 4·s²·(D² + s·D·S + P²)    ⟹    det B ≡ 12·s²  on F_s = 0
     ⟹  K_G = −det B/q² = −12·s²/q² ,   q = |∇F_s|² .
```

At s = 1 this is the certified keystone `K_G = −12/q²`. If the Stage-A derivation of the
link reduction produces a different det B or a different K_G(s), the family definition
is wrong and K-2 fires before any transcendence claim runs.

## P-A — reduction at r = 2, shear symbolic (T-A)

**Claim.** A direct algebraic derivation (no Gauss–Bonnet/Cohn-Vossen/Booth cited as a
black box) of

```
∫∫_S (−det B/q²) dA = −2·L(link) ,   L = arc length of the spherical conic
                                     {u ∈ S²: D² + s·DS + P² = 0}
```

with `k²(s)`, `n(s)`, and the two Booth weights emerging as **closed-form outputs** of
the cone eigenvalue algebra — the algebraic primitive (the Gauss–Bonnet 1-form in this
setting) exhibited explicitly, not invoked.

**Retrodiction targets at s = 1 (from the open pins — reproduce, don't cite):**

```
k²(1) = (2−√2)/4        n(1) = (4−3√2)/8        weights (3+2√2), (2+2√2)
keystone constant = −5.010490702660418769050021160526777648057…  (two routes)
eigenvalues of the coupled block: (1±√2)/2 and 1 ;  a²_max = k² exactly
```

**Gates.** K-1 (below): direct derivation disagrees with the certified keystone pin.
K-4 (below): `n = (4−3√2)/8` does not emerge from the algebra.

**Fallback (declared now).** If symbolic-s CAS blows up: derive at ≥ 3 numeric shears
`s ∈ {1/2, 1, 2}` (all avoiding the register singularities s = 0, 1/√3) and interpolate
the rational functions `k²(s)`, `n(s)`, weights, with degree bounds **numerator and
denominator ≤ 6 in s** (the register `j(s)` sits at degree 6/6; the eigenvalue algebra
is lower). A fit needing degree > 6 is itself a finding (family mis-scoped). Family
tier is marked EMPIRICAL until the symbolic pass lands; keystone stays exact.

## P-B — the exactness test at r = 3 (the discriminator, T-B)

**Claim.** A decision, by two independent routes that bite as a pair (K-3), of whether

```
e₃(P·H°·P) / q^(5/2) · dA     is exact (= d of an algebraic 1-form) on the quadric.
```

**Route 1 (primary, symbolic).** Ansatz primitive `η` with `q^(3/2)` denominators over
the function field; `dη = density` reduces to linear algebra in sympy. Ansatz space and
its dimension declared in the Stage-B note before solving; an empty solution set with
the space documented is the NO verdict for that route.

**Route 2 (corroboration, numeric).** Compactly-supported bump deformation of the
quadric at fixed asymptotic cone; if `∫∫ κ_{3;3,0} dA` moves, exactness is dead.
Declared now: homothety and translation are NOT admissible deformations (they act on
quadrics at known weight −3/2 and change nothing independently) — the bump must leave
the quadric family. **Two bump profiles** (compact C^∞ and compact polynomial-spline);
**quadrature precision floor: 25 digits** (mp.dps ≥ 40, adaptive), the reported move
must exceed 1e-20 to count as nonzero.

## P-C — branch on B (T-C1 / T-C2)

- **C1 (if exact).** State and prove the higher Cohn-Vossen for channel densities;
  derive the link functional's normal form; classify its transcendence.
  **Prior-art sweep is an obligation before any theorem claim:** Cohn-Vossen
  generalizations, total absolute curvature (Chern–Lashof), Willmore-type functionals.
- **C2 (if not exact).** High-precision `κ_{3;3,0}` constant on the keystone to ≥ 30
  digits; PSLQ against {K, Π, π, products} in ℚ(2^(1/4), √2) with validated controls;
  a validated no-hit is the finding (concrete candidate beyond the elliptic class), not
  a failure.

## KILL CONDITIONS (armed at open)

```
K-1  Stage-A direct derivation disagrees with the certified keystone pin
     (constant −5.0104907…, or K_G(1,1,1) = −3/49) → HALT; triage derivation
     vs pin before anything else runs.
K-2  j(s) retrodiction fails at any sampled shear (family F_s does not reproduce
     the CALC-24 register j(s) = (1728s⁶−1728s⁴+576s²−64)/(s⁶+2s⁴+s²)) → family
     definition wrong or register wrong: park family tier, bank the discrepancy,
     KEYSTONE (s = 1) continues.
K-3  Primitive found (Route 1 = exact) AND bump test moves the constant
     (Route 2 = not exact) → contradiction, HALT; one route is buggy (this pair
     is the battery biting).
K-4  n = (4−3√2)/8 does not emerge from the Stage-A algebra → the Booth
     identification is wrong below the 19-digit numeric floor; the reduction
     claim drops to EMPIRICAL and the write-up says so.
```

## STOP CONDITIONS

Two sessions per stage, hard. Stage-A overrun → close keystone-only (n derived,
constants as outputs) and park the family tier with the blocker named. Stage-B
unresolved both routes → park with the ansatz space documented exhausted; the finding
is then "needs real cohomology machinery", itself worth banking.

## METHOD

Fresh code, exact symbolic where the claim is symbolic, exact ℚ / ℚ(√d) numbers, two
independent routes on every number, byte-stable ×2 scripts, artifacts to
`reports/arithmetic_track/`. **No singular-path special-function evaluation on any
certified path** (close-off case law: `ellippi(n>1, m)` loses ~25 digits — the P4 open
pin uses only the regular n = (4−3√2)/8 < 1 form). Every structural guess gets a
five-minute numeric discriminator before a derivation leans on it (A3 polar-dual
refutation is the standing warning). Reuse the certified bank (RC-1 `K_G = −det B/q²`;
the open-pin re-derivations); import nothing else.

## OUTPUT LEDGER

This PREREG (frozen) · derivation notes + byte-stable scripts in
`reports/arithmetic_track/` · addendum rows to `DUAL_CONSTANT_CLOSEOFF.md` ·
`LEADS.md` LEAD-8 verdict either way · `BOOT.md` current-state update · `ADMISSIONS`
touched only if a result becomes load-bearing for the engine (default: paper-track,
no admission).
