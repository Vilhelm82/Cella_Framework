# Codex handoff — Exact DBP corridor representatives and positive clearance v1.0

**Campaign:** CCE-2R — Exact Corridors  
**Date:** 2026-07-14  
**Status:** executable proof-and-build handoff  
**Target:** close the first unproved obligation blocking CCE-2  
**Repository:** Cella  
**Primary output:** exact upper/lower DBP route manifests with positive exact clearance and lateral-class calibration

---

## 0. Assignment

Derive, prove, encode, and certify explicit representatives for the two DBP
shear-cover corridors used in Paper III. The output must close the current CCE-2
gap without inserting a path under the informal label “standard path.”

The required result is a pair of exact piecewise-rational base paths, their
uniquely continued lifts to the DBP shear cover, exact positive clearance from
every curve-level singular divisor, and a proof that they select the established
upper and lower lateral classes.

The campaign must produce one of two outcomes:

```text
PROVED
  Exact route representatives, clearance constants, cover lifts, corridor
  identification, and pole-side calibration are all certified.

BLOCKED
  A precise mathematical obligation remains. Report the exact missing lemma,
  divisor equation, or orientation convention. Do not install a provisional
  route into CCE-2.
```

Do not weaken the theorem to numerical sampling. Do not infer a route from its
endpoint sheet alone. Do not use the stale evaluator-campaign Pathfinder scout.

---

## 1. Frozen starting state

Treat the completed CCE work as immutable input:

```text
CCE-0                         complete
PF-0                          complete against live typed Pathfinder
CCE-1                         complete
engine test programs          36 passed
DBP evaluator assertions      1,591
PF-0 assertions               58
CCE-1 assertions              24
```

The canonical six-envelope CCE-1 bundle digest is:

```text
c04ba9200de47bd5fc68e84e9c932ab63e5ea9eb41981b6bba3144272b7f84a3
```

The live Pathfinder closure is the production implementation under:

```text
engine/src/cella/pathfinder/
```

Resolve its exact module inventory from the PF-0 report and production tests.
The production closure is reported as 52 source files and must remain
certificate-bound.

The following file is historical/regression material only:

```text
research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/
  pathfinder_m1_scout.py
```

It must have zero production references before and after this campaign.

Read first:

```text
research/campaigns/CELLA_CONTINUATION_ENGINE/
  CCE_CONTINUATION_ENGINE_FINAL_REPORT_v0.2.md
  CCE_CONTINUATION_ENGINE_FINAL_REPORT_v0.2.json
  CCE_1_STAGE_REPORT_v1.0.md
  PATHFINDER_BEHAVIOR_CONFIRMATION_REPORT_v1.0.md
  PATHFINDER_BEHAVIOR_CONFIRMATION_REPORT_v1.0.json
  CCE_2_ROUTE_SPECIFICATION_GAP_v1.0.md

the current continuation-engine request, state, certificate and verifier code
the live DBP Pathfinder provider and its tests
DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md, Sections 7D–7F
DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1.md
DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1.md
SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md
DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md
```

If the gap report imposes a stronger route contract than this handoff, retain
the stronger requirement and document the difference.

---

## 2. Exact geometric setting

Work on the shear cover:

```text
U_tilde^o = {
    (sigma,rho) in C^2 :
    rho^2 = 1 + sigma^2,
    sigma != 0,
    rho != 0
}.
```

The distinguished endpoints are:

```text
u_+ = (1,+sqrt(2))
u_- = (1,-sqrt(2)).
```

The derived parameters are:

```text
c = (rho - 1)/(rho + 1)
m = (rho - 1)/(2*rho)
n = -m^2/(1 - 2*m).
```

The deck involution is:

```text
tau(sigma,rho) = (sigma,-rho)

c o tau = c^(-1)
m o tau = 1-m
n o tau = 1-n.
```

The elliptic fibre and relative group are:

```text
C_u       : y^2 = x(x-1)(x-m(u))
C_u^o     : C_u minus {P_u^+,P_u^-}
Q_0       : (0,0)
Q_m       : (m,0)
H_Z(u)    : H_1(C_u^o,{Q_0,Q_m};Z).
```

Use a marked basis equivalent to:

```text
(A, B, mu, delta)
```

with compact lattice:

```text
Lambda_ell = Z*A + Z*B.
```

The target transport statements are:

```text
G_up[delta_+]   = [delta_-^up]
G_down[delta_+] = [delta_-^down]
```

in:

```text
H_Z(u_-)/Lambda_ell(u_-).
```

The established lateral relation is:

```text
delta_-^up - delta_-^down = -mu_-.
```

Do not set the unresolved compact corrections to zero:

```text
G_up(delta_+)   = delta_-^up   + lambda_up
G_down(delta_+) = delta_-^down + lambda_down

lambda_up, lambda_down in Lambda_ell(u_-).
```

---

## 3. Exact candidate base paths

Use the following rational polygonal representatives as the primary candidates.
Every coordinate lies in `Q(i)`.

### 3.1 Upper candidate

Define the ordered vertices:

```text
U_0 =  1
U_1 =  1/2 + i
U_2 =  1/2 + 3i/2
U_3 = -1/2 + 3i/2
U_4 = -1/2 + i/2
U_5 =  1/2 + i/2
U_6 =  1/2 + i
U_7 =  1.
```

For `j=0,...,6`, parameterize the segment exactly by:

```text
gamma_up,j(t) = U_j + t*(U_(j+1)-U_j),
0 <= t <= 1.
```

The ordered path is:

```text
gamma_up
  = [U_0,U_1]
  * [U_1,U_2]
  * [U_2,U_3]
  * [U_3,U_4]
  * [U_4,U_5]
  * [U_5,U_6]
  * [U_6,U_7].
```

It consists of a stem from `1` to `1/2+i`, one counterclockwise square about
`+i`, and the reverse stem.

The expected free-group and winding data are:

```text
word(gamma_up)          = a_+
wind_(+i)(gamma_up)     = +1
wind_(-i)(gamma_up)     = 0
wind_0(gamma_up)        = 0.
```

### 3.2 Lower candidate

Take the complex-conjugate ordered vertices:

```text
D_0 =  1
D_1 =  1/2 - i
D_2 =  1/2 - 3i/2
D_3 = -1/2 - 3i/2
D_4 = -1/2 - i/2
D_5 =  1/2 - i/2
D_6 =  1/2 - i
D_7 =  1.
```

Define:

```text
gamma_down,j(t) = D_j + t*(D_(j+1)-D_j),
0 <= t <= 1,
```

and concatenate the seven ordered segments.

For the conjugate orientation shown above, the expected data are:

```text
word(gamma_down)        = a_-^(-1)
wind_(-i)(gamma_down)   = -1
wind_(+i)(gamma_down)   = 0
wind_0(gamma_down)      = 0.
```

### 3.3 Orientation gate

Do not assume that the lower Stage-3 corridor uses `a_-^(-1)` merely because it
is the conjugate of the upper path. Compare the candidate with the actual
Stage-3 orientation convention.

If Stage 3 requires `a_-` rather than `a_-^(-1)`, reverse only the lower square
traversal while retaining the lower stem and reverse stem. Record the selected
orientation in the theorem, route manifest, fixtures, and certificate.

The stem determines the endpoint pole-side approach. Reversing the small square
does not alter the return-stem side, but it may alter compact-period data. The
orientation must therefore be fixed explicitly even though CCE-2 currently
works modulo `A/B` periods.

### 3.4 Exact path representation

Store every complex rational coordinate as an ordered pair of reduced rational
numbers:

```text
sigma = (Re_num/Re_den) + i*(Im_num/Im_den).
```

Do not use decimal coordinates. Canonicalize segment order, orientation,
concatenation, and path reversal before hashing.

---

## 4. The theorem to prove

Produce a theorem with the following content.

```text
THEOREM — Exact DBP corridors and positive clearance

There exist explicit piecewise-Q(i)-affine paths gamma_up and gamma_down,
based at sigma=1, whose unique lifts ell_up and ell_down to U_tilde^o
starting at u_+ satisfy:

1. Endpoint lift

   ell_up(0) = ell_down(0) = u_+,
   ell_up(1) = ell_down(1) = u_-.

2. Exact route words

   gamma_up represents the Stage-3 upper generator about +i;
   gamma_down represents the Stage-3 lower generator about -i,
   with its orientation stated explicitly.

3. Positive exact curve-level clearance

   There are explicit rational constants eta_j > 0 such that both lifted
   paths remain eta_j-clear of every curve discriminant, pole collision,
   endpoint collision, and denominator divisor in the CCE-2 manifest.

4. Admissible isotopy

   Each candidate is connected to its corresponding Stage-3 corridor by
   an isotopy through paths satisfying the same clearance conditions.

5. Lateral calibration

   ell_up selects delta_-^up and ell_down selects delta_-^down.

6. Quotient transport

   G_up[delta_+]   = [delta_-^up],
   G_down[delta_+] = [delta_-^down]

   modulo Lambda_ell = Z[A]+Z[B].
```

The theorem must distinguish exact path identity, homotopy class, cover sheet,
pole-side selection, and quotient homology class. None of these may be inferred
from another without proof.

---

## 5. Exact base-plane clearance

For a rational segment:

```text
z(t) = z_0 + t*d,
0 <= t <= 1,
```

and a point `a`, compute:

```text
Delta_a(t)
  = |z(t)-a|^2
  = A*t^2 + B*t + C,

A,B,C in Q.
```

The exact minimum occurs at an endpoint or at:

```text
t_* = -B/(2*A)
```

when `0 <= t_* <= 1`. Evaluate every candidate exactly. Do not replace this
finite rational calculation with floating sampling.

For the displayed candidates, certify at least the following conservative
bounds.

### Upper path

```text
|sigma|       >= 1/2
|sigma-i|     >= 1/2
|sigma+i|     >= 1
|sigma|       <= 2.
```

### Lower path

```text
|sigma|       >= 1/2
|sigma+i|     >= 1/2
|sigma-i|     >= 1
|sigma|       <= 2.
```

These are deliberately conservative. Store the exact segment minima in the
certificate, even if the theorem publishes simpler rational lower bounds.

Verify winding by an exact polygon-index or ray-crossing algorithm over
`Q(i)`. Winding numbers alone are not sufficient for homotopy in the
three-punctured plane. Also record the reduced word in:

```text
pi_1(C minus {0,+i,-i}, 1).
```

---

## 6. Lift to the shear cover

Use:

```text
rho^2 = (sigma-i)*(sigma+i).
```

The path avoids both branch points, so the initial root `rho(0)=+sqrt(2)` has a
unique analytic continuation along every segment.

The endpoint deck parity is:

```text
rho(1)
  = (-1)^(wind_(+i)(gamma)+wind_(-i)(gamma))*rho(0).
```

Both candidates wind oddly about exactly one branch point. Therefore:

```text
rho(1) = -sqrt(2).
```

Certify the lift segment by segment using the live Pathfinder DBP provider and
the CCE algebraic isolator. Each overlap must identify exactly one continuation
root. The route certificate must include:

```text
initial root isolator
ordered segment endpoints
ordered overlap witnesses
deck parity
terminal root isolator
proof that terminal rho = -sqrt(2)
```

From the base bounds:

```text
|1+sigma^2|
  = |sigma-i|*|sigma+i|
  >= 1/2.
```

Hence:

```text
|rho|^2 >= 1/2,
|rho|   >= 1/sqrt(2) > 1/2.
```

Also:

```text
|rho|^2 = |1+sigma^2| <= 1+|sigma|^2 <= 5,
|rho| <= sqrt(5) < 3.
```

These give a simple exact annular enclosure for every lifted segment:

```text
1/2 < |rho| < 3.
```

---

## 7. Derived-parameter clearance

Use the exact identities:

```text
(rho-1)*(rho+1) = sigma^2,

m       = (rho-1)/(2*rho),
1-m     = (rho+1)/(2*rho),
1-2m    = 1/rho,

n       = -(rho-1)^2/(4*rho),
1-n     =  (rho+1)^2/(4*rho),

c       = (rho-1)/(rho+1).
```

Since:

```text
|sigma|^2 >= 1/4
```

and:

```text
|rho+1| < 4,
|rho-1| < 4,
```

the product identity implies:

```text
|rho-1| > 1/16,
|rho+1| > 1/16.
```

For a non-strict published rational bound, certify and use:

```text
|rho-1| >= 1/32,
|rho+1| >= 1/32.
```

Consequently one may use the conservative route-level bounds:

```text
|m|       >= 1/192
|1-m|     >= 1/192
|1-2m|    >= 1/3

|n|       >= 1/12288
|1-n|     >= 1/12288

|c|       >= 1/128
|1/c|     >= 1/128.
```

Codex must verify every displayed constant from the exact inequalities before
publishing it. Tighter constants may replace these, but weaker unproved numbers
may not.

The zero/infinity equivalences are:

```text
m = 0       <=> rho = 1  <=> sigma = 0
m = 1       <=> rho = -1 <=> sigma = 0
n = 0       <=> rho = 1  <=> sigma = 0
n = 1       <=> rho = -1 <=> sigma = 0
rho = 0     <=> sigma in {+i,-i}.
```

Prove these identities symbolically and use them to reduce the divisor ledger.

---

## 8. Third-kind pole and endpoint separation

The pole lies over:

```text
x_p = m/n = 2 - 1/m.
```

Reduce it to the cover coordinate:

```text
x_p       = -2/(rho-1)
x_p - 1   = -(rho+1)/(rho-1)
x_p - m   = -(rho+1)^2/(2*rho*(rho-1)).
```

The squared pole height is:

```text
y_p^2
  = x_p*(x_p-1)*(x_p-m)
  = -(rho+1)^3/(rho*(rho-1)^3).
```

Therefore the two pole points remain distinct and avoid `Q_0`, `Q_m`, and the
elliptic branch points whenever:

```text
rho != 0,
rho != 1,
rho != -1.
```

Using the conservative route bounds, certify explicit separation such as:

```text
|x_p|       >= 1/2
|x_p-1|     >= 1/128
|x_p-m|     >= 1/24576
|y_p^2|     >= 1/6291456.
```

These constants follow from:

```text
1/2 < |rho| < 3,
1/32 <= |rho-1|,
1/32 <= |rho+1|,
|rho-1| < 4,
|rho+1| < 4.
```

Verify the arithmetic exactly. The certificate should retain the sharper value
obtained on each segment.

---

## 9. Positive tube, not merely a positive path

CCE needs a stable corridor, not only pointwise nonvanishing on one path.

Construct a base-plane tube of exact radius:

```text
r_tube = 1/8
```

around each polygonal candidate, or select a smaller dyadic radius if required
by the live provider.

By the path-point clearance bounds, every point in the upper tube satisfies:

```text
|sigma|       >= 3/8
|sigma-i|     >= 3/8
|sigma+i|     >= 7/8.
```

The lower tube satisfies the conjugate bounds. Also:

```text
|sigma| <= 17/8 < 3.
```

Thus throughout either tube:

```text
|rho|^2
  = |sigma-i|*|sigma+i|
  >= 21/64,

|rho| > 1/2,
|rho| < 4.
```

Furthermore:

```text
|rho-1|*|rho+1|
  = |sigma|^2
  >= 9/64.
```

Since `|rho±1|<5`, a conservative tube bound is:

```text
|rho-1| >= 1/64,
|rho+1| >= 1/64.
```

This yields tube-level bounds:

```text
|m|       >= 1/512
|1-m|     >= 1/512
|1-2m|    >= 1/4

|n|       >= 1/65536
|1-n|     >= 1/65536.
```

For the poles, one may conservatively target:

```text
|x_p|       >= 2/5
|x_p-1|     >= 1/320
|x_p-m|     >= 1/163840
|y_p^2|     >= 1/131072000.
```

All constants must be checked exactly. If `r_tube=1/8` fails an additional
divisor from the authoritative CCE-2 manifest, shrink the tube dyadically and
record the first accepted radius. Do not alter the central path merely to make a
weak numerical check pass.

The tube certificate must state whether it certifies:

```text
the base sigma-plane tube,
its unique lifted cover tube,
the curve family over that tube,
or an additional surface-sweep domain.
```

Do not conflate these scopes.

---

## 10. Admissible isotopy and corridor identity

Matching endpoint sheets and winding numbers is not sufficient to identify a
path in a three-punctured plane. Its fundamental group is nonabelian.

Prove corridor identity by one of:

```text
1. an explicit isotopy between the polygon and the Stage-3 route inside the
   certified admissible tube;

2. an exact reduced-word calculation in
   pi_1(C minus {0,+i,-i},1), together with a proof that the Stage-3 route has
   the same word;

3. replacement of the previously informal Stage-3 route by the exact polygon,
   accompanied by a theorem that the Stage-3 proof depends only on the stated
   admissible corridor class and pole-side calibration.
```

The proof must not use only the abelian winding vector.

Record:

```text
basepoint
stem
small-loop orientation
reduced free-group word
lifted endpoint
isotopy domain
divisors excluded throughout the isotopy
```

---

## 11. Pole-side calibration

The upper and lower labels must be derived from the return stems.

Let `h>0` approach zero on the final upper return segment. Then:

```text
sigma_up(h)
  = 1 + h*(-1/2+i).
```

On the terminal negative sheet:

```text
rho = -sqrt(1+sigma^2),
d rho/d sigma at u_- = -1/sqrt(2),
d m/d rho at u_-     = 1/4.
```

Therefore:

```text
rho_up(h)
  = -sqrt(2)
    + h*(1/(2*sqrt(2)) - i/sqrt(2))
    + O(h^2),

m_up(h)
  = m_-
    + h*(1/(8*sqrt(2)) - i/(4*sqrt(2)))
    + O(h^2).
```

Hence for sufficiently small positive `h`:

```text
Im(m_up(h)) < 0.
```

For the lower return segment:

```text
sigma_down(h)
  = 1 + h*(-1/2-i),

m_down(h)
  = m_-
    + h*(1/(8*sqrt(2)) + i/(4*sqrt(2)))
    + O(h^2),

Im(m_down(h)) > 0.
```

Use an exact Taylor remainder or algebraic interval argument to produce a
specific rational `h_0>0` for which these signs hold on:

```text
0 < h <= h_0.
```

Then invoke the established local pole-side theorem:

```text
upper parameter approach from Im(m)<0 selects delta_-^up;
lower parameter approach from Im(m)>0 selects delta_-^down.
```

Confirm the sign convention against the authoritative Stage-3 theorem before
freezing it. If the paper uses the opposite naming convention, preserve the
paper and adjust the route labels consistently; do not silently flip one layer.

The local pole coordinate may also be checked through:

```text
u_p = 1/n = (2m-1)/m^2,

d u_p/dm
  = 2*(1-m)/m^3.
```

At the dual endpoint the derivative is positive real, so the sign of the
parameter approach transfers to the pole approach under the established local
coordinate convention.

---

## 12. Curve-level versus surface-level clearance

CCE-2 is a curve-route and relative-class stage. Its mandatory clearance ledger
must include every divisor used by:

```text
the shear cover,
the elliptic fibre,
the marked endpoints,
the third-kind poles,
the relative local system,
the selected observable requested at CCE-2.
```

The surface theorem additionally mentions:

```text
v = 1/c,
v = 1/c^2,
the norm discriminant,
the surface polar divisor,
the swept-boundary collision locus.
```

Handle these according to the actual CCE-2 contract:

```text
If CCE-2 requests only curve transport:
  prove the curve corridor theorem now;
  record surface clearance as a CCE-6 obligation;
  do not claim a surface-route certificate.

If the current CCE-2 manifest already requests a surface observable:
  derive the complete surface divisor equations;
  add exact clearance over the path-times-fibre domain;
  keep CCE-2 blocked until that stronger lemma is proved.
```

Do not infer full surface clearance from nonvanishing of `sigma`, `rho`, `m`, or
`n` alone.

---

## 13. Live Pathfinder integration

Use the narrow DBP provider already added to the production typed Pathfinder.
Do not create a second planner and do not route through the stale scout.

The provider request must contain exact data:

```text
family_id
family_manifest_digest
route_id
ordered Q(i) vertices
segment orientations
initial sheet isolator
expected free-group word
expected deck parity
required divisor manifest
requested tube radius
requested proof budget
coefficient ring
selected relative class
```

The live provider should return a valid plan or a typed unsupported result under
the PF-0 contract. Distinguish validity from adequacy:

```text
ValidPlan
  exact path and clearance obligations are within the provider's admitted
  domain;

InsufficientProofBudget
  the valid plan cannot reach a requested analytic width under the supplied
  budget;

UnsupportedRequest
  the route, divisor family, field, or operation lies outside the confirmed
  provider domain.
```

The route theorem is a mathematical input to the provider. Pathfinder must not
manufacture the missing isotopy or pole-side theorem from route labels.

Bind the final plan to:

```text
PF-0 confirmation-report digest
52-file production Pathfinder closure digest
DBP provider source digest
route-manifest digest
divisor-manifest digest
clearance-theorem digest
```

---

## 14. Implementation stages

### Stage R0 — Preflight and scope lock

```text
read the CCE-2 gap report and authoritative route theorems
inventory the live Pathfinder provider and CCE route types
confirm zero production references to pathfinder_m1_scout.py
record the CCE-1 six-envelope digest
enumerate every divisor currently required by CCE-2
separate curve-level and surface-level obligations
```

Gate:

```text
No code changes until the exact divisor manifest and route theorem target are
written into the campaign report.
```

### Stage R1 — Exact route manifests

```text
encode the upper and lower rational vertex sequences
canonicalize segment order and orientation
compute exact polygon words and winding data
resolve the lower orientation against Stage 3
generate canonical route digests
```

Gate:

```text
Every vertex is Q(i), every segment is exact, and the free-group word—not only
the winding vector—is recorded.
```

### Stage R2 — Base clearance and cover lift

```text
compute exact segment-point distance minima
prove the displayed base clearance constants
continue the selected rho root through every segment
prove unique overlap matching
prove terminal rho = -sqrt(2)
certify the base tube and lifted tube
```

Gate:

```text
No sampled clearance values and no nearest-root sheet choices appear in the
certificate.
```

### Stage R3 — Derived parameters and pole separation

```text
prove the rho/m/n/c identities
derive route- and tube-level rational lower bounds
reduce all pole collisions to rho, rho-1, and rho+1 nonvanishing
prove exact pole/end-point separation
close the curve divisor ledger
```

Gate:

```text
Every required denominator and collision polynomial has a positive exact lower
bound over the certified tube.
```

### Stage R4 — Corridor identity and lateral calibration

```text
prove explicit isotopy or exact free-group-word agreement with Stage 3
derive the upper and lower return-stem expansions
prove exact signs for 0<h<=h_0
apply the local pole-side theorem
identify delta_-^up and delta_-^down
```

Gate:

```text
The route labels follow from the geometry. No target-name or fixture-based
selection is admitted.
```

### Stage R5 — CCE-2 implementation and certification

```text
install the proved manifests in the live DBP provider
run continue_certified on upper and lower routes
emit route certificates and deterministic digests
verify path composition, reversal, endpoint lift, clearance and class typing
add hostile tamper tests
run all engine and campaign gates in clean processes
```

Gate:

```text
CCE-2 closes only when both routes replay independently and the exact theorem
artifact is source-bound into their certificates.
```

---

## 15. Mandatory exact tests

### Route representation

```text
all vertex coordinates are reduced Q(i)
segment concatenation closes exactly at sigma=1
upper and lower paths are conjugate before any required orientation adjustment
path reversal is exact
route canonicalization is deterministic
route digests are clean-process stable
```

### Fundamental-group data

```text
upper reduced word matches the Stage-3 upper generator
lower reduced word matches the Stage-3 lower generator
windings about 0,+i,-i are exact
wrong square orientation is detected
winding-only substitution does not satisfy the corridor-identity gate
```

### Base and tube clearance

```text
exact rational minimum for every segment/point pair
positive path clearance from 0,+i,-i
positive tube clearance from 0,+i,-i
tampered vertex crossing a divisor is rejected
oversized tube is rejected
accepted dyadic tube radius is deterministic
```

### Cover lift

```text
initial rho = +sqrt(2)
unique root match on every segment overlap
odd branch-point parity
terminal rho = -sqrt(2)
wrong initial sheet is rejected
tampered terminal sheet is rejected
```

### Derived parameters

```text
m,1-m,1-2m,n,1-n,c and 1/c remain defined
displayed symbolic identities replay exactly
every published lower bound is re-derived exactly
tampered bound fails verification
```

### Poles and marked endpoints

```text
x_p identities replay exactly
y_p^2 identity replays exactly
P^+ and P^- remain distinct
poles avoid Q_0,Q_m and the elliptic branch points
pole-collision tampering is rejected
```

### Lateral calibration

```text
upper return stem has Im(m)<0 near u_-
lower return stem has Im(m)>0 near u_-
an exact h_0 and remainder bound are recorded
upper route selects delta_-^up
lower route selects delta_-^down
the meridian relation remains unchanged
```

### Regression and trust boundary

```text
all 36 engine test programs pass
all 1,591 DBP evaluator assertions pass
all 58 PF-0 assertions pass
all 24 CCE-1 assertions pass
six schema-1.1 evaluator locks remain unchanged
CCE-1 six-envelope bundle remains unchanged
production Pathfinder closure remains source-bound
pathfinder_m1_scout.py has zero production references
no external CAS or floating scout enters certificate evidence
```

---

## 16. Hostile refusal cases

Add stable cases for:

```text
route_vertex_not_exact
route_not_closed
wrong_free_group_word
wrong_branch_winding
wrong_lower_orientation
path_hits_sigma_zero
path_hits_branch_point
tube_hits_divisor
tube_radius_not_certified
branch_overlap_not_unique
terminal_sheet_mismatch
derived_parameter_clearance_failed
pole_endpoint_collision
pole_pair_collision
stage3_corridor_identity_unproved
pole_side_ambiguous
route_theorem_digest_mismatch
divisor_manifest_digest_mismatch
stale_pathfinder_source_reference
surface_scope_requested_without_surface_clearance
```

Every refusal must identify the exact failed obligation. Do not return a
replacement path automatically after a theorem-identity failure. A route search
may propose another exact candidate, but it must restart the relevant proof
gates.

---

## 17. Required deliverables

Produce all of the following in:

```text
research/campaigns/CELLA_CONTINUATION_ENGINE/
```

### Mathematical artifacts

```text
DBP_EXACT_CORRIDOR_POSITIVE_CLEARANCE_THEOREM_v1.0.md
DBP_EXACT_CORRIDOR_DIVISOR_REDUCTION_v1.0.md
DBP_CORRIDOR_LATERAL_CALIBRATION_v1.0.md
```

### Machine-readable artifacts

```text
DBP_EXACT_CORRIDOR_MANIFEST_v1.0.json
DBP_EXACT_CORRIDOR_CLEARANCE_CERTIFICATES_v1.0.json
DBP_EXACT_CORRIDOR_ROUTE_DIGESTS_v1.0.json
```

### Verification

```text
verify_dbp_exact_corridor_paths.py
verify_dbp_corridor_clearance.py
verify_dbp_corridor_lift_and_lateral_class.py
```

### CCE integration reports

```text
CCE_2_STAGE_REPORT_v1.0.md
CCE_2_STAGE_REPORT_v1.0.json
CCE_2_GAP_LEDGER_v1.0.md
```

The stage report must record:

```text
base commit and final worktree identity
all source files changed
authoritative theorem sources
exact selected path vertices and orientation
free-group words and windings
route and tube clearance constants
cover lift endpoint proofs
pole-side calibration
route, provider, theorem and certificate digests
assertion totals
clean-process replay result
legacy certificate locks
remaining curve and surface gaps
```

Do not edit Paper III automatically. If the theorem succeeds, prepare a separate
paper-update patch or insertion note for user review.

---

## 18. Completion criteria

CCE-2R and CCE-2 are complete only when:

```text
1. gamma_up and gamma_down are explicit Q(i)-polygonal paths.

2. Their exact free-group words and orientations match the authoritative
   Stage-3 corridor conventions.

3. Their lifts beginning at u_+ terminate at u_-.

4. Every curve-level divisor in the CCE-2 manifest has a positive rational
   clearance bound over a certified positive-radius tube.

5. The third-kind poles remain distinct and avoid both marked endpoints.

6. The return-stem geometry proves the upper and lower lateral selections.

7. The quotient transports agree with Theorem 7F.1 without setting unknown
   A/B corrections to zero.

8. The live production Pathfinder provider constructs the plans in the same
   continue_certified operation.

9. Both route certificates replay deterministically and are bound to the exact
   route theorem, divisor manifest, live provider, and PF-0 closure.

10. Every prior evaluator, PF-0, and CCE-1 gate remains clean.

11. No production reference to pathfinder_m1_scout.py exists.

12. Any unproved surface-level clearance is explicitly retained for CCE-6 and
    is not reported as a CCE-2 result.
```

---

## 19. Immediate execution order

Begin in this order:

```text
1. Read CCE_2_ROUTE_SPECIFICATION_GAP_v1.0.md and list the exact required
   divisor manifest.

2. Verify the seven-segment upper and lower candidate paths symbolically.

3. Resolve the lower-loop orientation against the Stage-3 convention.

4. Compute exact point-clearance minima and certify the proposed 1/8 tubes.

5. Prove the rho/m/n/c divisor reductions and pole-separation identities.

6. Certify the lifted paths and terminal sheet through the live Pathfinder and
   CCE isolator.

7. Prove admissible corridor identity using an explicit isotopy or reduced
   free-group word—not winding alone.

8. Prove the return-stem signs and lateral calibration with an exact remainder
   bound.

9. Freeze the mathematical theorem and machine-readable route manifests.

10. Integrate them into CCE-2, regenerate only the new route certificates, and
    rerun every frozen legacy gate.
```

The governing rule is:

```text
An exact loop is not yet the DBP corridor.

The corridor is the exact loop
+ its lifted sheet
+ its positive divisor clearance
+ its admissible isotopy class
+ its pole-side calibration
+ its typed relative-homology action.
```

