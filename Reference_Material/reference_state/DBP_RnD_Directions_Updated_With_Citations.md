# DBP R&D Directions — Updated Standing-Results Version

**Date:** 2026-07-06  
**Purpose:** Reproduce and update the earlier `DBP_RnD_Directions_Exact_Role_Channel_Geometry.md` brief using the newer standing-results dashboard and the GTD/DBP comparison context.  
**Status:** Working R&D brief. It is a prioritisation and campaign-design document, not a proof document.

---

## Source discipline

This version treats the standing-results dashboard as the current state record. The dashboard explicitly says it is “STATE, not history,” and gives the source-of-truth order as:

```text
persistent evals > standing-results dashboard > calc log > ephemeral scripts
```

So this brief retires or downgrades older directions where the dashboard supersedes them.[^SR-state]

A second discipline also matters: prior labels such as `accepted`, `ratified`, `proven`, and `certified` are not evidence by themselves. Anything load-bearing in a new repo, paper theorem, or engine layer still needs in-repo re-verification: fresh code or fresh derivation, exact arithmetic where applicable, and byte-stability for computational claims.[^AD-reverify]

Citation keys used below:

```text
[SR]        DBP STANDING RESULTS.md, 2026-07-01
[GTD]       gtd vs dbp.pdf, June 28 2026 draft
[LEADS]     LEADS.md, 2026-07-06
[REVIEW]    REVIEW_Exact_Role_Channel_Geometry.md, 2026-07-06
[LEVER]     LEVER_AUDIT.md, 2026-07-06
[ADMIT]     ADMISSIONS.md, 2026-07-06
```

---

## Executive assessment

The previous version was directionally right, but its centre of gravity was slightly stale. You are not at:

```text
Maybe DBP has a scalar-blindness thesis to prove.
```

You are at:

```text
Exact Role-Channel Geometry now has several backbone theorems settled;
the live novelty is in the remaining interiors, singular boundaries, topology,
and the n = 3 thermodynamic lift.
```

The best global framing remains:

```text
active output-role re-solving
+ exact rational finite-jet transport
+ channel-resolved invariant fibres
+ gauge-normal carriers
+ typed singular strata
```

But the corrected thesis is sharper than the old one:

```text
Single scalars are always lossy.
The full scalar tower resolves shape only up through n <= 4.
For n >= 5, carrier-level structure is forced by dimension.
```

That is stronger and cleaner than a broad “scalars are blind” slogan. The standing results give the dimension threshold explicitly: with `n−1` scalar invariants and shape dimension `n(n−3)/2`, the full scalar spectrum resolves shape iff `n <= 4`; a single scalar such as `j`, `K_G`, or one channel aliases shape at every `n`.[^SR-dim]

The headline research move should therefore be:

```text
Stop proving that scalar summaries can fail.
Start exploiting the exact carrier/threshold theorems to find what only the channel geometry sees.
```

---

## What is now settled or retired

### 1. Broad scalar-blindness as a theorem target is retired

Do not pitch the next work as if scalar blindness is still an open thesis. It is now corrected into a precise dimension theorem:

```text
full sigma_r spectrum resolves shape iff n <= 4
single scalar aliases shape at every n
n >= 5 requires carrier-level structure by dimension
```

The old statement “scalars are blind to shape, need monodromy” is explicitly corrected in the standing-results dashboard. It remains true only for a single scalar, or for the full scalar tower once `n >= 5`.[^SR-retired-scalars]

**Updated use:** cite scalar incompleteness as a proven background theorem, then move on to what the carrier makes computable.

---

### 2. The carrier theorem is done, not a direction

The central carrier theorem is settled for all `n >= 3`:

```text
Im(L) ≅ M^(n−2,2)
     = C[role-pairs]
     = triv ⊕ std(n−1,1) ⊕ S^(n−2,2)
```

The dashboard states this as proven for all `n`, with load-bearing steps computer-verified for `n = 4..9`.[^SR-carrier]

The gauge-normal form is also standing:

```text
O_ij = H_ij - g_i H_jj/(2g_j) - g_j H_ii/(2g_i)
Λ_{k,{j,l}} = O_jk + O_kl - O_jl
```

This means the carrier is not just another feature vector; it is the gauge-invariant Hessian quotient at order 2.[^SR-gauge]

**Updated use:** build from `O`, do not re-argue for it.

---

### 3. The pure-coupling depth theorem is done

The order-axis depth theorem is complete:

```text
For all r >= 2 and n >= 2r,
κ_{r;r,0} realizes S^(n−r,r).
```

The standing results mark this theorem as proven, complete, and with no gaps.[^SR-depth]

**Updated use:** the open problem is no longer the pure-coupling column. It is the mixed-bidegree interior:

```text
κ_{r;p,q}
minimal p required to reach depth r
other depth-r irreps
full-density surjectivity
```

---

### 4. The two-state scalar-loss demonstration is no longer a theorem target

The GTD/DBP paper contains a Kerr-Newman two-state demonstration where `R` and `A_c` agree to about `10^-13`, while the carrier `O` and rank-one channels separate the states.[^GTD-two-state]

That is still a strong physics-facing illustration. But mathematically, it is now less important than the standing exact witness at `n = 4`, where two different Hessians have identical magnitude vector `(C) = (6, 33, 33, 54)` but different carrier data, with isotypic norms recorded.[^SR-twostate]

**Updated use:** keep the Kerr-Newman two-state example as narrative evidence. Do not spend R&D effort “promoting” it to a theorem; the stronger exact theorem already exists.

---

### 5. The same-`S3` question is closed

Do not keep the “are the role `S3` and monodromy `S3` the same?” question alive. The standing results close it:

```text
role S3 != monodromy S3
verdict: no_canonical_comparison_map
```

The monodromy `S3` acts on root sheets of a stage-2 trinomial, with no canonical bijection to the three roles.[^SR-sameS3]

**Updated use:** any monodromy work should now be framed as local-carrier versus global-cover ambiguity, not as comparison of two `S3`s.

---

### 6. The symmetric-wreath claim is corrected

The old product-cover statement using a symmetric wreath is superseded. The standing result is cyclic:

```text
product cover = C_mP wr C_mP
order = m_P^(m_P+1)
```

The dashboard explicitly says this corrects the original `Sym(m_P) wr Sym(m_P)` version and answers the `S3 wr S3` question: no, the product side stays cyclic.[^SR-wreath]

**Updated use:** quote the cyclic wreath law, not the old symmetric one.

---

### 7. The arithmetic track is more mature than the old brief implied

The total-curvature arithmetic track is not a vague “place-limit trap” anymore. The standing results give:

```text
j = 128 exactly
non-CM elliptic period
three independent numerical routes to 60 digits
closed form in elliptic integrals
j(s) monotone coupling landscape
```

The dashboard states that `j = 128` is rational, non-CM, not a class-number-1 CM value, and not reducible to the usual clean `π`, `Γ(1/3)`, or `Γ(1/4)` forms.[^SR-arithmetic]

**Updated use:** this is probably a write-up track now, not an exploratory R&D track.

---

### 8. `D_static` must remain open

The previous brief already warned this, and the review confirms it: `D_static` reverted to open. It should be kept as a re-derivation target, not carried as a citable settled result.[^REVIEW-dstatic]

**Updated use:** mention it only under carrier-choice / computational-currency research, with the word “re-derived” nailed to its forehead.

---

## Updated core thesis

The research programme should now be framed as:

```text
Exact Role-Channel Geometry:
A finite-jet and curvature-account theory of how local structure changes
when the output role of an implicit relation is actively changed.
```

The distinctive combination is still:

```text
active role re-solving
exact rational finite-jet transport
channel-resolved invariant fibres
faithful gauge-normal carrier O
typed singular strata
```

But the pitch should emphasize the standing backbone:

```text
carrier theorem: done
shape-loss theorem: done
dimension threshold: done
pure-coupling depth theorem: done
parity law: done
n = 2 GTD/DBP complementarity: done
n = 3 DBP metric/complementarity lift: open
mixed-grid interior: open
role-singularity classification: open
channel topology: open
```

The new sentence worth making true is:

```text
Once scalar and carrier backbones are settled, the remaining dark corners are the
places where topology, singularity, mixed degree, and thermodynamic boundary structure
force new channel data.
```

---

## Highest-value live directions

### 1. The `n = 3` DBP metric and complementarity lift

**Status:** Open.  
**Priority:** Highest physics-facing priority.  
**Why it matters:** The GTD/DBP paper establishes the channel-inverse metric and complementarity for `n = 2`, but explicitly leaves the `n = 3` lift open.

For `n = 2`, the DBP metric is:

```text
g_DBP = -h^(-1)
h = Σ_i κ_{c,i} dE_i ⊗ dE_i
```

The paper reports that this metric is positive-definite on the Kerr wedge, singular on the role boundaries, and that its curvature detects boundaries where conventional GTD-II is blind.[^GTD-metric]

The complementarity law is already verified across Kerr, Reissner-Nordström, and van der Waals: GTD-II carries an order-2 pole on the instability/transition locus, while DBP carries order-3 poles on generic role boundaries and order-4 poles where a boundary is reflection-fixed.[^GTD-complement]

But for `n = 3`, the paper says each output chart carries several off-diagonal couplings rather than one, so the channel form `h` must be generalized before the construction transfers; whether complementarity survives against the Kerr-Newman Davies surface is the natural next test.[^GTD-n3-open]

#### Is this a matrix extension or a structural obstruction?

My read: it is **not merely a computation sprint**, but there is no known obstruction yet. It is a derivation campaign with a finite test space.

The likely raw material is not the raw Hessian and not a hand-selected diagonal list of channels. It should be the gauge-invariant role-pair carrier:

```text
O_ij = H_ij - g_i H_jj/(2g_j) - g_j H_ii/(2g_i)
```

because `O` is already the gauge-normal carrier of the order-2 coupling data.[^SR-gauge]

The hard part is canonicity. There are many bilinear or quadratic forms one could build from the role-pair carrier. The winning `h_3` needs to satisfy:

```text
1. reduce exactly to the n = 2 channel-inverse construction
2. be S3-symmetric on the three charge roles
3. factor through O or directional normal-curvature objects, not raw H
4. have controlled sign / definiteness on the physical Kerr-Newman wedge
5. degenerate or blow up on the physical role-boundary divisors:
   T = 0, Ω = 0, Φ_e = 0
6. be testable against the n = 3 Davies surface D3
```

#### Suggested campaign: `N3_COMPLEMENTARITY_I`

Stage A — Derivation screen:

```text
enumerate natural S3-equivariant bilinear forms on O
apply n = 2 reduction constraint
apply gauge-invariance constraint
apply boundary-order constraint
keep only minimal surviving candidates
```

Stage B — Exact Kerr-Newman screen:

```text
compute candidate h_3 on Kerr-Newman
check positivity / signature in the physical wedge
check singular set against:
  Davies D3
  extremal T = 0
  Ω = 0
  Φ_e = 0
```

Stage C — Complementarity test:

```text
GTD-II R: double pole on D3, finite on extremal
DBP R[h_3]: finite on D3, divergent on role boundaries
record pole orders and leading coefficients where possible
```

Stage D — Obstruction handling:

```text
if no candidate survives canonicity + positivity + boundary behaviour,
write the obstruction theorem instead of pretending the metric exists.
```

This is the most immediate “paper-quality” open problem because it naturally extends the GTD/DBP comparison and gives a concrete pass/fail result.

---

### 2. Channel topology / coupling-graph classification

**Status:** Open.  
**Priority:** Best pure-math novelty candidate after the standing carrier/depth backbone.  
**Why it matters:** This is a genuinely structural question not already closed by the standing theorems.

The LEADS document frames it as classifying channel spectra by Hessian coupling-graph topology:

```text
no edge
single edge
chain
triangle
star
bipartite
complete
```

The triangle decomposition already gives adjacent combinatorial machinery, so the problem is newly tractable.[^LEADS-topology]

#### Goal

Prove one of two theorem shapes:

```text
positive theorem:
  graph topology class determines a channel-signature family under stated hypotheses

negative theorem:
  distinct graph classes can be channel-isospectral, with exact counterexamples
```

Either result is useful. A positive theorem becomes combinatorial differential geometry of local coupling. A negative theorem becomes a sharp blindness theorem.

#### Suggested campaign: `TOPOLOGY_I`

```text
n = 4, 5
representative graph classes
exact rational g,H samples per class
compute channel spectra and gauge-rigid/null directions
classify injectivity / non-injectivity
publish exact counterexample pairs if injectivity fails
```

This is the cleanest place to discover a new “channel topology” language.

---

### 3. Mixed bidegree grid `κ_{r;p,q}`

**Status:** Open interior; edges mapped.  
**Priority:** Best higher-order pure-math theorem candidate.  
**Why it matters:** The pure-coupling column is done, but the mixed interior is where a new recurrence/signature/minimal-depth theorem could live.

The LEADS file says the grid has three mapped edges:

```text
pure-coupling column: depth theorem, all r, n >= 2r
r = 2 row: triangle / shadow law
normalization boundary: parity law
```

The unmapped region is the mixed-bidegree interior, and the minimal coupling degree `p` required to reach depth `r` remains open.[^LEADS-grid]

#### Candidate theorem shapes

```text
Pascal-type recurrence across (p,q)
forced-vanishing law
Lorentzian-to-higher-signature law
minimal-depth threshold in p
mixed bidegree detects other depth-r irreps
```

#### Suggested campaign: `GRID_I`

```text
extract exact grids at n = 4, 5
orders r = 2, 3
use two-variable Vandermonde extraction
publish coefficient tables
stake one conjecture before widening the sweep
```

This is still one of the best places to find something genuinely new, but it is no longer the only backbone: the depth theorem already gives the pure-coupling spine.

---

### 4. Role singularity atlas

**Status:** Vocabulary exists; theorem open.  
**Priority:** Deep conceptual dark corner and likely bridge to physics.  
**Why it matters:** The engine can refuse at degeneracies. It cannot yet read them.

The review says the active role-jet groupoid is done at order 2 for `n = 3`, but the singular-strata classification theorem is still open. Tokens such as `ROLE_CHART_UNAVAILABLE` and `CHANNEL_ISOTROPIC` are named and witnessed, but the theorem connecting chart failure to characteristic channel/orbit behaviour across the boundary is not done.[^REVIEW-singular]

The LEADS file names the relevant failures:

```text
a = 0 / b = 0
Δ_n = 0
det S = 0
κ_i = κ_j
tangent contact
cone apex
```

and asks whether each stratum type has a characteristic channel signature.[^LEADS-singular]

#### Suggested campaign: `SINGULARITY_I`

```text
one-parameter exact-Q families crossing each stratum
left/right channel accounts
blow-up rates
rank drops
role-orbit stabilizers
refusal-token transitions
```

The theorem shape should be:

```text
role non-solvability is not an exception;
it is typed geometric information.
```

This is where the project can talk about folds, caustics, horizons, phase boundaries, and critical points without overclaiming.

---

### 5. Symbolic RN and van der Waals coefficients

**Status:** Open as paper-hardening.  
**Priority:** High tractability; strengthens physics narrative.  
**Why it matters:** The GTD/DBP paper has symbolic Kerr leading coefficients, while the order-law transfer to RN and van der Waals is computer-verified. Closing the symbolic coefficients would make the universality claim harder to swat.

The paper states that for Kerr, both pole orders and leading coefficients are in closed form, while the transfer of the order law to Reissner-Nordström and van der Waals remains computer-verified.[^GTD-complement]

#### Suggested campaign: `RN_VDW_SYMBOLIC_I`

```text
derive leading Laurent coefficients for RN extremal and Q = 0 boundaries
derive leading Laurent coefficient for vdW role boundary
confirm order 3 generic / order 4 reflection-fixed split
write a compact symbolic table beside the Kerr coefficients
```

This is not the deepest research direction, but it is probably the fastest paper-strengthening win.

---

### 6. Arithmetic track write-up

**Status:** Strong enough to write.  
**Priority:** Paper track, not main engine R&D.  
**Why it matters:** The non-CM total-curvature result is clean, unusual, and already highly structured.

Standing results already give:

```text
∫∫ K_G dA = -5.010490702660418...
j = 128 exactly
non-CM elliptic period
closed form in elliptic integrals
j(s) monotone landscape
CM ladder structure
j = 128 aliasing triple resolved by branch configuration
```

The important strategic distinction: this is probably publishable as an arithmetic/geometry note, but it is less central to the engine than the carrier, topology, singularity, and complementarity lines.[^SR-arithmetic]

#### Suggested output

```text
short paper:
  total DBP curvature as a non-CM elliptic period
  coupling/shear parameter j(s)
  CM limits and non-CM keystone
  aliasing triple: scalar/group blind, branch configuration resolves
```

Do not let this eat the main R&D queue. It is a jewel-box paper, not the engine room.

---

### 7. Odd sector / `Qsqrt` diagnostics

**Status:** Open and newly unblocked.  
**Priority:** High-upside adversarial theorem.  
**Why it matters:** The even scalar tower is rational. The odd sector lives in `Q(√q)` and may detect bending-sensitive extrinsic structure invisible to the even tier.

LEADS says `QSqrt` is now implemented and gate-certified, so odd-order invariants are exactly computable in the engine. The proposed discriminating test is a bending family that holds all even invariants fixed while the odd tier separates what the even tier cannot.[^LEADS-odd]

#### Suggested campaign: `ODD_I`

```text
construct or import a bending family
fix even invariants
compute σ1 or σ3 exactly in Q(√q)
prove the odd tier separates the family
```

The theorem shape is pleasingly sharp:

```text
even invariants are blind;
odd channel density sees.
```

---

### 8. Order-3 transport and groupoid proper

**Status:** Open.  
**Priority:** Foundation-hardening.  
**Why it matters:** Order-2 active role action is certified. Third-order formulas exist as paper raw material, but nothing at order 3 is certified in-repo; the genuine local groupoid of output charts is still untouched.[^LEADS-order3]

#### Suggested campaign: `TRANSPORT_III`

```text
re-derive third-order recharting law
certify at keystone and generic rational jets
check whether order-2 attribution theorem survives one order up
record whether cross-term closure survives
```

If it closes, the phrase `active role-jet groupoid` becomes earned. If it fails, the obstruction is the theorem.

---

### 9. Codimension `>= 2` constraint systems

**Status:** Open.  
**Priority:** Engine / applied unlock, but wider than the current DBP paper sequence.  
**Why it matters:** Real sensor networks are systems, not single hypersurfaces.

The lever audit ranks codimension `>= 2` constraint systems as the top “engine soon” R&D priority because nothing currently covers systems of constraints.[^LEVER-codim]

#### Suggested campaign: `CODIM2_I`

```text
two constraints in R^4
exact rational data
compare:
  separate channel accounts then intersect
  intersect then channelize
look for non-commutation or induced holonomy
```

This is probably not where to start if the immediate goal is the GTD/DBP paper sequence, but it is a serious next engine-frontier problem.

---

### 10. Global completeness of the low-degree invariant set

**Status:** Open.  
**Priority:** Credibility spine.  
**Why it matters:** Local certification is not global completeness.

The lever audit places global completeness of the low-degree invariant set as a major “engine soon” priority: the local tier is certified, but the global completeness theorem is open.[^LEVER-codim]

The target theorem:

```text
Within a declared regular locus and degree/order bound,
the invariant set separates exactly the equivalence classes it claims to separate,
and the blindness set is complete.
```

This is boring until it wins. Then it becomes the sentence everybody cites.

---

### 11. `D_static` re-derived

**Status:** Open / reverted.  
**Priority:** Computational sibling direction.  
**Why it matters:** If re-derived cleanly, it could answer whether recoverability/factorability is decidable from an operation-DAG before execution.

LEADS says `D_static` is open again and should be re-derived over Layer-0 observation-map chains, proving the biconditional on the rational-op class with an independent referee and locating the transcendental wall.[^LEADS-dstatic]

#### Suggested campaign: `DSTATIC_REDERIVE_I`

```text
define predicate over observation-map chains
prove rational-op biconditional
independent referee
explicit transcendental wall
no inherited WARP status
```

This remains interesting, but it should not outrank the live DBP mathematics.

---

### 12. Global monodromy / cycle-type reserve

**Status:** Specific old questions closed; broader isthmus open.  
**Priority:** Pure-math / global ambiguity reserve.  
**Why it matters:** It is the project’s main global mathematics, but it is no longer the next practical R&D target.

Retired:

```text
same role S3 vs monodromy S3?    closed: no canonical comparison
Sym wreath product?              corrected: cyclic wreath
```

Still open:

```text
local carrier ↔ global cover ambiguity
residue near role boundary ↔ monodromy cycle type
branch-typed inversion / ambiguity typing
```

The GTD/DBP paper itself says the earlier conjecture `holonomy = A_c` cannot hold literally because `A_c` is continuous while monodromy is discrete; the honest bridge would relate `A_c`’s residue near a boundary to monodromy cycle type.[^GTD-n3-open]

So: keep it alive, but stop letting it masquerade as the main road. This is a side passage with interesting carvings.

---

## Revised priority board

### If the goal is the next physics-facing paper

1. **`n = 3` DBP metric / complementarity lift**  
   Highest impact and genuinely open.

2. **Symbolic RN and van der Waals coefficients**  
   Fastest strengthening of the existing complementarity law.

3. **Role singularity atlas, boundary-specialized slice**  
   Gives the physical boundary story a clean typed-stratum basis.

4. **Kerr-Newman scalar/carrier narrative cleanup**  
   Keep the two-state demo as illustration, not theorem target.

### If the goal is pure mathematical novelty

1. **Channel topology classification**  
   Best new structural language candidate.

2. **Mixed `κ_{r;p,q}` grid**  
   Best higher-order theorem candidate.

3. **Odd-sector bending diagnostic**  
   Best adversarial separation theorem.

4. **Role singularity atlas**  
   Deepest geometric dark corner.

### If the goal is engine / Cella architecture

1. **Codimension `>= 2` systems**  
   Largest applied unlock.

2. **Global completeness of invariant set**  
   Credibility spine.

3. **Order-3 transport / groupoid proper**  
   Foundation-hardening.

4. **`D_static` re-derived**  
   Computational-currency sibling, but not DBP-first.

### If the goal is quick publishable output

1. **Arithmetic track write-up**  
   Non-CM elliptic period / `j = 128` / `j(s)` landscape.

2. **Symbolic RN/vdW coefficients note**  
   Table-driven, strengthens GTD/DBP.

3. **Kerr-Newman two-state demo as narrative appendix**  
   Useful, but do not oversell it as the theorem.

---

## Retired / do-not-reopen list

```text
1. “Prove scalar blindness” as broad thesis
   → corrected by dimension threshold.

2. “Promote two-state demo to theorem”
   → exact n=4 witness and dimension theorem already do the job.

3. “Are role S3 and monodromy S3 the same?”
   → closed: no canonical comparison map.

4. “Product cover is symmetric wreath”
   → corrected: cyclic wreath.

5. “Pure-coupling depth theorem is partial”
   → complete for all r >= 2, n >= 2r.

6. “Carrier theorem is still a direction”
   → done; build from O.

7. “D_static is settled”
   → reverted/open; only re-derive fresh.
```

The taxidermy shelf is getting crowded. Useful, dramatic, and absolutely not worth feeding.

---

## Near-term campaign slate

### `N3_COMPLEMENTARITY_I`

```text
Goal:
  derive and test the n = 3 DBP channel form h_3.

Hard pass/fail:
  h_3 reduces to n = 2 construction;
  h_3 is S3-symmetric and gauge-invariant;
  h_3 has controlled sign on Kerr-Newman;
  R[h_3] is finite on D3 and singular on role boundaries,
  or the obstruction is certified.
```

### `TOPOLOGY_I`

```text
Goal:
  classify spectra by coupling-graph topology at n = 4,5.

Hard pass/fail:
  topology predicts channel signature, or exact isospectral counterexamples exist.
```

### `GRID_I`

```text
Goal:
  extract mixed κ_{r;p,q} grid for n = 4,5 and r = 2,3.

Hard pass/fail:
  recurrence/signature/vanishing/minimal-depth conjecture survives,
  or obstruction table is published.
```

### `SINGULARITY_I`

```text
Goal:
  classify channel/orbit behaviour across role singular strata.

Hard pass/fail:
  each stratum has a characteristic signature,
  or exact counterexamples show which strata are not readable.
```

### `RN_VDW_SYMBOLIC_I`

```text
Goal:
  derive symbolic leading coefficients for RN and vdW DBP curvature poles.

Hard pass/fail:
  symbolic coefficients agree with verified slopes,
  or the order-law table gets corrected.
```

### `ODD_I`

```text
Goal:
  test whether σ_odd in Q(√q) separates an even-invariant-blind family.

Hard pass/fail:
  odd sector separates what even sector cannot,
  or the claimed diagnostic layer is weakened.
```

### `TRANSPORT_III`

```text
Goal:
  certify third-order role transport and decide whether attribution survives.

Hard pass/fail:
  order-3 closure supports groupoid formalization,
  or obstruction is recorded.
```

---

## Closing synthesis

The updated programme is less speculative and more dangerous in the good way.

The old brief said:

```text
Scalar invariants may be correct while the channel fibre contains the explanation.
```

The updated version says:

```text
The carrier and scalar-threshold theorems are now standing.
The next discoveries should come from the mixed interior, graph topology,
role singularities, odd-sector separation, and the n = 3 thermodynamic lift.
```

The cleanest immediate bet is the `n = 3` complementarity lift. The cleanest pure-math bet is channel topology. The deepest dark corner is role singularities. The most theorem-shaped higher-order target is the mixed grid. And the arithmetic track is sitting there polished enough to glare at you from across the room.

Make the next campaign small enough to kill. That is where this work seems to get its best manners.

---

## Source notes

[^SR-state]: **[SR]** `DBP STANDING RESULTS.md`, “How to read this”: current-state dashboard, source-of-truth order, certification substrates, and tier definitions.

[^AD-reverify]: **[ADMIT]** `ADMISSIONS.md`, “THE RE-VERIFICATION RULE”: origin-document statuses are claims rather than evidence; load-bearing prior results must be re-proven inside the current repo.

[^SR-dim]: **[SR]** Part III, “DIMENSION THRESHOLD (scalars vs shape)”: `n−1 >= n(n−3)/2` iff `n <= 4`; single scalar aliases at every `n`.

[^SR-retired-scalars]: **[SR]** Part VII, “SUPERSEDED / REFUTED”: old “scalars blind to shape, need monodromy” framing corrected by the dimension threshold.

[^SR-carrier]: **[SR]** Part I.1, “Central theorem — the carrier is the role-pair module”: `Im(L) ≅ M^(n−2,2)` for all `n >= 3`.

[^SR-gauge]: **[SR]** Part I.3, “Gauge-normal form — the carrier IS the gauge-invariant Hessian quotient”: definition of `O_ij` and `Λ_{k,{j,l}}`.

[^SR-depth]: **[SR]** Part IV, “THE (r,n)-PLANE DEPTH THEOREM”: `κ_{r;r,0}` realizes `S^(n−r,r)` for all `r >= 2`, `n >= 2r`.

[^GTD-two-state]: **[GTD]** §5.3, “Two states, one R, one Ac, two carriers”: Kerr-Newman two-state demonstration with `R` and `A_c` matching while carrier `O` separates.

[^SR-twostate]: **[SR]** Part I.6, “Finite two-state witness for the (2,2) shape”: exact `n = 4` pair with identical magnitude vector but different carrier components.

[^SR-sameS3]: **[SR]** Part I.5, “The resolvent S3 is a role-QUOTIENT, not independent”: role `S3` and monodromy `S3` are distinct; verdict `no_canonical_comparison_map`.

[^SR-wreath]: **[SR]** Part V.4, “Self-glue monodromy wreath law”: product cover is cyclic wreath `C_mP wr C_mP`, not symmetric wreath.

[^SR-arithmetic]: **[SR]** Part V.1–V.3, “TRANSCENDENCE / ARITHMETIC LANDSCAPE”: non-CM total curvature with `j = 128`, `j(s)` landscape, CM ladder, and aliasing triple resolved by branch configuration.

[^REVIEW-dstatic]: **[REVIEW]** “Caveat on one item you cited”: `D_static` reverted to open and should be treated as re-derivation target.

[^GTD-metric]: **[GTD]** §6.1–§6.2, “The channel-inverse metric” and “The curvature scalar, and where it diverges”: `g_DBP = -h^-1`, boundary singularities, and Kerr leading coefficients.

[^GTD-complement]: **[GTD]** §6.3, “The complementarity is universal”: GTD order-2 transition poles; DBP order-3 generic boundary poles and order-4 reflection-fixed poles across Kerr, RN, and vdW.

[^GTD-n3-open]: **[GTD]** §6.5, “What remains open”: holonomy/cycle-type bridge and the `n = 3` lift requiring generalization of `h` because each output chart has several off-diagonal couplings.

[^LEADS-topology]: **[LEADS]** LEAD-3, “Channel topology (coupling-graph classification)”: graph classes and discriminating test for spectra / gauge-rigid directions.

[^LEADS-grid]: **[LEADS]** LEAD-1, “The `κ_{r;p,q}` grid at n >= 4”: mapped edges, unmapped mixed interior, and exact extraction plan.

[^REVIEW-singular]: **[REVIEW]** “The five linked results,” item 2: singular-strata vocabulary done; classification theorem open.

[^LEADS-singular]: **[LEADS]** LEAD-2, “Role singularities”: algebraic failures to connect with channel/orbit behaviour across boundaries.

[^LEADS-odd]: **[LEADS]** LEAD-4, “The odd sector: √q diagnostics”: `QSqrt` unblocks exact odd-order invariant computation; bending-family discriminating test.

[^LEADS-order3]: **[LEADS]** LEAD-5, “Order-3 transport and the role groupoid proper”: order-3 formulas not certified; groupoid proper untouched.

[^LEVER-codim]: **[LEVER]** Tier 2, “engine soon”: codimension `>= 2` constraint systems and global completeness as high-priority engine R&D.

[^LEADS-dstatic]: **[LEADS]** LEAD-6, “D_static re-derived”: open/reverted; predicate to be defined fresh over Layer-0 observation-map chains.
