# DBP Paper Ensemble Architecture

## Canonical paper boundaries, theorem ownership, and remaining gates, v1.0

**Date:** 2026-07-14  
**Status:** architecture frozen; component theorems remain governed by their
individual proof ledgers  
**Purpose:** prevent the current theorem ensemble from becoming one circular
mega-paper or a collection of overlapping micro-papers

---

## 0. Architectural decision

The programme should be organized as four component papers, one eventual
capstone, and one internal parent ledger.

```text
Paper I   Role-cover foundations
Paper II  Kerr--Newman inverse-channel realization
Paper III DBP elliptic curvature and transport
Paper IV  Galois horizon cover

Paper V   Selected quotient groupoids: equivalence, closure,
          and independent realizations
          [held until the remaining gates are proved]

Internal  Unified theorem spine / master dependency ledger
```

The decisive editorial rules are:

```text
1. Merge Landen--Trace and Native Relative-Period Route.
2. Absorb Surface-to-Link and Surface-Cycle Stages 1--3 into the same
   elliptic paper, with detailed calculations retained as appendices or
   proof dossiers.
3. Keep Galois Horizon Cover mathematically independent.
4. Keep the local role-cover foundation separate from its Kerr--Newman
   metric realization.
5. Do not publish the categorical capstone until equivalence, closure,
   and an independently sourced third realization are proved.
6. The unified spine is a ledger, not a sixth proof source.
```

---

## 1. Dependency architecture

```text
Paper I: Role-cover foundations
             |
             v
Paper II: Kerr--Newman selected metric realization

Paper III: DBP elliptic curvature transport      [standalone proof branch]

Paper IV: Galois horizon cover                    [standalone proof branch]

Paper I + Paper II + Paper III + Paper IV
             |
             | plus equivalence + closure + independent R3
             v
Paper V: Selected quotient groupoids
```

Paper III and Paper IV may cite Paper I for motivation and terminology, but
their mathematical proofs must not depend on the conjectural capstone.

---

## 2. Paper I

### Active Recharting of Framed Constraint Hypersurfaces

### Role Covers and Curvature-Channel Quotients

This is the abstract local foundation.

### Theorem payload

1. regular output-chart cover and active partial role action;
2. Active Recharting Orbit Theorem;
3. rational finite-jet action and the value-plus-jet carrier;
4. bordered-minor channel polynomial;
5. exact reduction from channel accounts to elementary extrinsic curvature;
6. defining-function gauge transport and the zero-sum account fibre;
7. Gaussian three-channel specialization;
8. RoleChSpec orbit separation and faithfulness at the proved jet order;
9. stabilizer, role-divisor, and reflection-stratum structure;
10. local curvature-valuation and parity-fixed boundary normal forms.

### Exclusions

Paper I should contain no load-bearing Kerr--Newman calculation, horizon
arithmetic, or elliptic-period proof. Those are realizations of its local
language, not part of the foundational theorem.

### Material absorbed or retired

```text
ABSORB
  active/passive recharting correction
  invariant reduction and gauge-transport theorem
  role-jet and carrier-faithfulness theorems
  local curvature valuation results

SUPPLEMENT
  three-channel implementation and verification documents

RETIRE AS HISTORICAL
  superseded campaign summaries and duplicate theorem notes
```

---

## 3. Paper II

### Inverse-Channel Geometry of Kerr--Newman Thermodynamics

### Selection and Boundary Curvature

This is the first detailed selected realization of Paper I.

### Theorem payload

1. mass-coordinate coupling zeros are exactly the role divisors;
2. weighted inverse-channel metric family;
3. uniqueness of the admissible family member;
4. positivity and interior regularity on the outer wedge;
5. regularity across the Davies surface;
6. generic order-three curvature collapse;
7. reflection-fixed order-four normal form and coefficient;
8. Schwarzschild Newton-wedge and corner behaviour;
9. open-stratum `3/4/4` complementarity theorem.

### Remaining symbolic gates owned by Paper II

```text
KN-G1  interior zero-exclusion / existence theorem
KN-G2  exact six-factor metric audit
KN-G3  nonremovable scalar-curvature pole theorem
KN-G4  extremal Sturm or exact noncancellation theorem
KN-G5  reflection residues
KN-G6  corner coefficients and specialization maps
```

Paper II depends on Paper I and must not repeat its abstract orbit or channel
proofs.

---

## 4. Paper III

### Curvature Periods of the DBP Quadric

### Landen Trace, Relative Surface Cycles, and Picard--Lefschetz Transport

This is one consolidated elliptic paper. Splitting its arithmetic, topology,
surface geometry, and native evaluator would duplicate every normalization
and create circular citations.

### Canonical internal order

1. DBP shear quadric and curvature form;
2. global primitive and family-wide surface-to-link theorem;
3. keystone metric quotient and Legendre reduction;
4. complementary Galois channels;
5. degree-two isogenies and common trace differential;
6. trace/anti-trace decomposition;
7. exact logarithmic anti differential and anti-periods;
8. primary and dual trace-path formulas;
9. pole-free native finite-interval compilation;
10. dual metric-quartic boundary chain;
11. Borel--Moore surface lift;
12. integral Picard--Lefschetz transport;
13. Native Transport and Scalar-Extension Separation Theorem;
14. exact-certificate interface.

### Central coefficient theorem

```text
integral lateral transport       exists over Z
CPV meridian midpoint            first exists over Q
Galois phase normalization       first exists over C
```

### Canonical source absorption

```text
MAIN SOURCE
  DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1

MERGE INTO MAIN BODY
  DBP_NATIVE_RELATIVE_PERIOD_ROUTE_THEOREM_v1.0
  DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0
  Native Transport and Scalar-Extension Separation Theorem

DETAILED APPENDICES / PROOF DOSSIERS
  DBP_DUAL_SURFACE_CYCLE_STAGE1_v0.1
  DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1
  DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1

INTERNAL AUDIT ONLY
  DUAL_CONSTANT_CLOSEOFF.md
  stage3_report_v2.json
  arith_i_stageA*.py
  Archive.zip

COMPUTATIONAL SUPPLEMENT
  verify_dbp_landen_trace_theorem_v1_1.py
  verify_dbp_native_relative_period_route.py
  verify_dbp_dual_surface_cycle_stage1.py
  verify_dbp_dual_surface_cycle_stage2.py
  verify_dbp_dual_surface_cycle_stage3.py
```

The Stage 1--3 reports are not three papers. Their theorem statements appear
once in Paper III; their full coordinate, convergence, residue, and lattice
arguments remain available as appendices or a technical supplement.

### Closed results that must not be reopened

```text
EP-C1  primary surface-to-link reduction
EP-C2  metric quartic--Legendre isomorphism
EP-C3  degree-two isogenies and common E_128 trace differential
EP-C4  exact logarithmic closure of the anti differential
EP-C5  exact primary and dual anti-periods
EP-C6  residue four and lateral/CPV bookkeeping
EP-C7  dual boundary chain and Borel--Moore surface lift
EP-C8  path-specific integral Picard--Lefschetz classes modulo A/B periods
EP-C9  CPV midpoint rational but nonintegral
EP-C10 boundary obstruction to absorbing i into an integral class
EP-C11 pole-free native evaluator for the two DBP claims
```

The following are also settled negatively:

```text
NO  primary plus dual form a complete period lattice
NO  the normalized dual class is an integral class modulo compact periods
NO  a second real or classically forbidden DBP surface region has been found
```

---

## 5. Paper IV

### Galois Theory of the Horizon Cover

### Monodromy, Kummer Towers, and Physical Root Selection

This remains a separate global algebraic paper.

### Theorem payload

1. Kerr--Newman horizon pair as a quadratic Galois cover;
2. entropy/temperature grading and the Galois-odd covariant;
3. mass-fibre norm and the `k`-ellipse degree law;
4. symmetric monodromy and four-charge `S_5` obstruction;
5. entropy non-radical theorem;
6. signed walls and physical chamber;
7. normalization--reflection descent;
8. definite-pencil and first-exit physical-root selection;
9. Kummer modules and static wreath closure;
10. degree-20 crown and rotating rank jump;
11. inertia and realization-poset theorem.

Paper IV must have no load-bearing dependence on Paper III. Their comparison
belongs only in the capstone.

---

## 6. Paper V

### Selected Quotient Groupoids

### Equivalence, Closure, and Independent Realizations

This is the eventual capstone. It must not be promoted from conjecture to
theorem until all three gates below are complete.

The common language should be groupoidal because the component symmetries are
different kinds of objects:

```text
role recharting
  -> partial rational / etale groupoid

horizon continuation
  -> covering and monodromy groupoid

elliptic continuation
  -> fundamental groupoid acting on a relative-homology local system
```

A provisional coefficient-typed selected quotient object is

```text
O_R = (
    base B,
    carrier X_R,
    groupoid G => X_R,
    quotient q: X_R -> |G|,
    admissible chamber C,
    selected section s,
    stratified wall W,
    boundary/stabilizer labels nu
)
```

where `R` is one of `Z`, `Q`, or `C` when coefficient type matters.

This is provisional until the data-minimization theorem is proved.

---

## 7. Remaining Gate E: equivalence

### 7.1 What equivalence must not mean

The raw local and global carriers cannot be declared strictly equivalent
without proof. Their generic fibres have different types:

```text
local channel account fibre
  = positive-dimensional affine fibre ker(Sigma_r)

global horizon/root fibre
  = generically finite discrete fibre
```

This dimensional mismatch is evidence against equivalence of the full
structured carriers.

### 7.2 Correct theorem target

```text
THEOREM E — Common Quotient--Selection Skeleton and Strict
             Non-Equivalence of Full Carriers

1. The full local and global structured carriers are not equivalent.

2. Explicit reduction functors send them to a common selected
   quotient skeleton.

3. Those reduced presentations are equivalent in the selected quotient
   category.

4. The reduction is maximal: restoring the discarded account-fibre or
   root-label data destroys the equivalence.
```

Presentation equivalence should be formulated as Morita equivalence of the
relevant groupoids while preserving:

```text
quotient
admissible chamber
selected section
stabilizer / inertia type
wall incidence
boundary normal-form label
```

Before claiming equivalence, the proof must compare:

```text
generic fibre type and dimension
automorphism and isotropy groups
monodromy
wall-incidence posets
branch-divisor codimension
selected-section topology
boundary specialization
```

If full faithfulness or essential surjectivity fails, the correct result is a
common functor, reflection, or adjunction rather than an equivalence.

### 7.3 Separate elliptic equivalence theorem

Paper III also leaves a sharp internal path-comparison problem. On

```text
E^o = E_128 minus {P,-P}
D   = {Q=(1,0), O}
H   = H_1(E^o,D;Z)
```

fix an integral basis

```text
H = <A, B, mu, Gamma_+>.
```

The lateral dual trace paths have unique expansions

```text
[Gamma_-^up]
  = [Gamma_+] + a[A] + b[B] + c[mu]

[Gamma_-^down]
  = [Gamma_+] + a[A] + b[B] + (c+1)[mu]
```

up to the chosen meridian sign. The exact integers `(a,b,c)` are not yet
known. Their determination gives the correct module-level equivalence:

```text
[Gamma_-^CPV]
  = [Gamma_+] + a[A] + b[B] + (c+1/2)[mu].
```

This is a Relative Trace-Path Equivalence Theorem. It is not a claim that the
two numerical constants are scalar algebraic multiples of one another.

This internal elliptic theorem may be completed in Paper III or a short
technical sequel, but it is logically distinct from the capstone equivalence
gate.

---

## 8. Remaining Gate C: closure

Here closure means categorical closure, not logarithmic closure, Galois normal
closure, or completion of a two-period lattice.

### Theorem target

```text
THEOREM C — Coefficient-Typed Selected Quotient Closure

For each admissible coefficient ring R, selected quotient objects and
native morphisms form a category and are closed, under explicit hypotheses,
under:

    identities and composition
    invariant-open restriction
    chamber restriction
    admissible base change
    quotient by a normal symmetry subgroupoid
    quotient by a saturated sub-local system
    transverse or compatible fibre product
    boundary specialization to typed wall strata

Selected sections remain branch-free on chamber interiors, while
stabilizer, inertia, wall, and valuation data specialize functorially
at boundaries.
```

The substantive proof obligation is preservation of selection and typed wall
data. Associativity of ordinary map composition is not the difficult part.

### Scalar-extension ladder

The elliptic theorem supplies the first strict coefficient example:

```text
SQG_Z  ->  SQG_Q  ->  SQG_C

integral lateral class      in SQG_Z
CPV midpoint                in SQG_Q but not SQG_Z
i-normalized class          in SQG_C but not SQG_Z
```

Scalar extension is a functor. It is not an equivalence and need not admit
descent.

### Elliptic closure below the capstone

A family-level elliptic closure theorem would compute

```text
rho:
pi_1(parameter base)
    -> Aut(H_1(E^o,D;Z))
```

on a complete basis `(A,B,mu,delta)`, prove equivariance of the surface lift,
and show that the DBP relative periods form an affine torsor over

```text
Z period_A + Z period_B + Z residue_period.
```

The current Stage-3 theorem determines the lateral coset and residue column,
not the complete `A/B` monodromy matrices.

---

## 9. Remaining Gate R3: independent third realization

The elliptic transport system is a valuable derived realization with native
data:

```text
carrier       = integral relative-homology local system
symmetry      = deck / Gauss--Manin / Picard--Lefschetz action
quotient      = class modulo compact periods
selection     = oriented upper or lower branch corridor
wall data     = discriminant, vanishing cycles, and pole meridian
Q-layer       = CPV midpoint
C-layer       = Galois phase normalization
```

It should appear in the capstone exposition. Under a strong independence
criterion, however, it is derived from the DBP quadric through link quotient,
elliptic isomorphism, isogeny, and surface lift. It should therefore not be
used by itself to discharge the independent-third gate.

### Independence criterion

A realization qualifies as independent only if:

```text
R3-1  its source equations are not a base change, quotient, isogeny,
      or reparameterization of an existing realization;

R3-2  its symmetry and wall structure are derived independently;

R3-3  its selection rule has an independent mathematical or physical origin;

R3-4  it realizes every required datum and a nontrivial native morphism;

R3-5  it has an interior branch-avoidance theorem and typed boundary form;

R3-6  it produces at least one prediction not inserted into the axioms;

R3-7  membership is proved without using the conjectural capstone theorem.
```

### Recommended candidate

The cleanest exact candidate is the lossless two-bus AC power-flow fold cover.
With slack magnitude `E`, reactance `X`, active power `P`, reactive power `Q`,
and squared load-bus magnitude `v`, its algebraic cover is

```text
v^2 + (2 Q X - E^2) v + X^2(P^2 + Q^2) = 0.
```

Its discriminant is

```text
Delta = (E^2 - 2 Q X)^2 - 4 X^2(P^2 + Q^2)
      = E^4 - 4 E^2 Q X - 4 P^2 X^2.
```

The realization data are independently sourced:

```text
carrier       = the two voltage sheets
symmetry      = C2 sheet exchange
quotient      = polynomial coefficients / discriminant data
chamber       = Delta > 0 with positive voltage
selection     = high-voltage branch continued from no load
wall          = Delta = 0 saddle-node voltage collapse
boundary type = square-root fold
```

At no load, the roots are

```text
v = E^2, 0,
```

so the physical section is selected independently by continuation from
`v=E^2`. This system is algebraically exact, has a genuine physical selection
rule, and is not derived from the DBP or horizon carriers.

It should begin as an R3 theorem dossier. It becomes a standalone companion
paper only if the family extension, wall stratification, or predictions grow
beyond what Paper V can carry cleanly.

---

## 10. Work order

The most efficient proof order is:

```text
1. Consolidate Paper III without duplicating the Stage reports.

2. Formalize the native-morphism theorem in Paper III.

3. Define the selected quotient category and its coefficient typing.

4. Prove the closure theorem with exact hypotheses.

5. Prove strict non-equivalence of full carriers and equivalence of the
   reduced quotient--selection skeleton.

6. Derive and certify the independent R3 realization.

7. Promote the capstone conjecture to a theorem.
```

The internal elliptic path-equivalence calculation may run alongside steps
3--6 because it does not control the logical validity of Papers I--IV.

---

## 11. Unified spine policy

Rename the unified spine internally as the **Master Theorem Ledger**. It must
record, but not re-prove, each result.

Use stable theorem families:

```text
RC-*   role-cover foundations
KN-*   Kerr--Newman inverse-channel realization
EP-*   elliptic periods, cycles, and transport
HC-*   horizon-cover arithmetic and selection
SQG-*  selected quotient groupoid framework
R3-*   independent third realization
```

Each ledger entry should contain:

```text
canonical theorem statement
owner paper and theorem number
proof status
dependencies
coefficient ring
verification artifacts
unresolved gates
notation collisions
superseded source list
```

The spine must never be cited as the proof source and must never allow the
capstone conjecture to prove one of its component realizations.

---

## 12. Release boundary

```text
RELEASE-INDEPENDENT
  Paper I, once its own theorem ledger is clean
  Paper II, once its remaining symbolic gates close
  Paper III, after consolidation and native-morphism formalization
  Paper IV, under its own proof and certificate ledger

HOLD
  Paper V

PAPER V RELEASE GATES
  SQG-E   equivalence / strict non-equivalence theorem
  SQG-C   categorical closure theorem
  R3      independently sourced third realization
```

This architecture lets every established mathematical body stand on its own
while preserving a precise route to the stronger ensemble theorem.
