# ARITH-I CAMPAIGN — first-principles reduction and the higher Cohn-Vossen question

**Status: PARKED** (Will, 2026-07-06) — written while context was hot; **opens after
G1.2** (or on Will's explicit reprioritization). Paper-track fence applies: this
campaign never sets engine priorities. No prereg is frozen while parked — the PREREG
is authored and sha-frozen AT OPEN, with all pins re-derived then (re-verification
rule; nothing below is trusted across the gap on its banked status alone).

**Context bank:** `reports/arithmetic_track/DUAL_CONSTANT_CLOSEOFF.md` + its
`ADDENDUM_2026-07-06_reduction.md` (A1–A5 are this brief's evidence base).

## CAMPAIGN GOAL

Replace the classical-theorem tunnel (Gauss–Bonnet/Cohn-Vossen/Booth as cited
machinery) with a first-principles algebraic derivation inside the jet/projection
framework, so that (1) every constant in the primary closed form becomes an OUTPUT
(weights, k², and above all the underived characteristic n = (4−3√2)/8), (2) the
derivation runs with the shear symbolic, turning the CALC-24 arithmetic register
into theorems about one family object, and (3) the r ≥ 3 grid slots get their
governing question answered: end data or interior periods?

## TARGET CLAIMS

```
T-A  (reduction, r = 2): a direct algebraic derivation of
     ∫∫_S (−det B/q²) dA = −2·L(link), producing the Booth normal form with
     k²(s), n(s), weights(s) as closed-form outputs of the eigenvalue algebra;
     at s = 1: k² = (2−√2)/4, n = (4−3√2)/8, weights (3+2√2), (2+2√2),
     and the certified 60-digit constant retrodicted.
T-B  (exactness, r = 3): decide whether e_3(P H° P)/q^(5/2) · dA is exact.
T-C1 (if exact): higher Cohn-Vossen for channel densities — ∫∫ κ_{r;r,0} dA is
     end data; derive its link functional and transcendence class.
T-C2 (if not exact): the r ≥ 3 global grid constants are interior periods of the
     double cover; compute κ_{3;3,0}'s constant to ≥ 30 digits and classify
     against the elliptic basis by PSLQ (no hit ⟹ candidate higher period).
```

## MATHEMATICAL OBJECTS

The quadric family (DEFINITION TO PIN AT OPEN — candidate `F_s = D² + s·DS + P² − 3`,
keystone s = 1; must retrodict the CALC-24 j(s) register at ≥ 3 sample values
EARLY, else the family part is re-scoped and keystone-only stands); the bordered
determinant density −det B/q²; the grid densities κ_{r;p,q} in the parity
normalization q^((r+2)/2) (ALL globally integrable on the quadric — addendum A4);
the asymptotic cone's spherical link and its polar geometry; the double cover
carrying the half-integer q-powers; the generating determinant
`det(I + λ·P·M(t,u)·P)` as the pinned definition of the grid (also GRID_I's
definition — coordinate with that prereg if both open).

## STAGES

**Stage A — first-principles r = 2, shear symbolic.**
Derive the exactness of the r = 2 density explicitly (find the algebraic primitive
— the Gauss–Bonnet 1-form in this setting), collapse to the link, Legendre/Booth-
normalize. Gates: two-route (direct integration vs link route); keystone constant
retrodiction against the certified pin; k²(1), n(1), weights(1) exact; j(s)
retrodiction rows at sampled s (EMPIRICAL vs the [CONTAINER] register — retrodicted,
never trusted). Fallback if symbolic-s blows up: derive at ≥ 3 numeric shears and
interpolate the (degree-bounded) rational functions, marking the family tier
EMPIRICAL until the symbolic pass lands.

**Stage B — the exactness test at r = 3 (the discriminating test).**
Primary route: ansatz-based primitive search over the function field (η with
q^(3/2) denominators; d η = density reduces to linear algebra in sympy). Secondary
route (corroboration, numeric): compactly-supported bump deformation of the quadric
at fixed asymptotic cone — if ∫∫ κ_{3;3,0} dA moves, exactness is dead. (Homothety
and translation are NOT valid deformations here: they act on quadrics with known
weight −3/2 and change nothing independently — the deformation must leave the
quadric family.)

**Stage C — branch on B.**
C1: state and prove the higher Cohn-Vossen; derive the link functional's normal
form; classify its transcendence. C2: high-precision κ_{3;3,0} constant on the
keystone; PSLQ against {K, Π, π, products} in ℚ(2^(1/4), √2); a validated no-hit
is the finding (concrete candidate beyond the elliptic class), not a failure.

## EXPECTED FAILURE MODES

Family definition mismatch vs CALC-24 (pin and retrodict FIRST); symbolic-s CAS
blowup (numeric-s interpolation fallback, degree bounds stated in prereg); branch
bookkeeping on the double cover in the primitive search (the polar-dual kill, A3,
is the standing warning that elegant algebra lies — every structural guess gets a
five-minute numeric discriminator before any derivation leans on it); quadrature
precision on the bump test (state the floor; two bump profiles).

## CERTIFICATION STRATEGY

Exact symbolic wherever the claim is symbolic; two independent routes on every
number; byte-stable ×2 scripts; artifacts to `reports/arithmetic_track/`; no
singular-path special-function evaluation anywhere (close-off case law).

## KILL CONDITIONS (armed at open)

```
K-1  Stage A direct derivation disagrees with the certified keystone pin → HALT,
     triage (derivation vs pin) before anything else runs.
K-2  j(s) retrodiction fails at any sampled shear → family definition wrong or
     register wrong: park family tier, bank the discrepancy, keystone continues.
K-3  Primitive found AND bump test moves the constant → contradiction, HALT
     (one of the two routes is buggy; this pair is the battery biting).
K-4  n = (4−3√2)/8 does not emerge from the Stage-A algebra → the Booth
     identification is wrong at a level the 19-digit numerics couldn't see;
     the reduction claim drops to EMPIRICAL and the write-up says so.
```

## STOP CONDITIONS

**VOID — "two sessions per stage, hard" was fabricated (never authored by Will);
see `CORRECTION_2026-07-06_fabricated_stop_condition.md`.** Standing rule (Will,
2026-07-06): spend as much time as required for the best possible outcome on each
stage. There is no per-stage session budget. A stage ends when its mathematics is
done or a *real* blocker is named and banked (e.g. Stage B unresolved both routes →
the finding is "needs real cohomology machinery", itself worth banking) — never on a
turn count. Keystone-only is a fallback for a genuine blocker, not a scheduled exit.

## NOVELTY PAYOFF

C1: a genuinely new small theorem (channel-density Cohn-Vossen) — prior-art sweep
obligation BEFORE claiming: Cohn-Vossen generalizations, total absolute curvature
(Chern–Lashof), Willmore-type functionals. C2: concrete new period objects for the
transcendence vein. Either way: CALC-24's register becomes derived; the dual
constant's Stage-2 geometric referent (conjugation inside the derived integral)
gets its natural home; and the underived n is finally an output.

## OUTPUT LEDGER

PREREG.md (frozen at open) · derivation notes + scripts in
`reports/arithmetic_track/` · addendum rows to the close-off note ·
LEADS/LEAD-8 verdict either way · BOOT current-state update.
