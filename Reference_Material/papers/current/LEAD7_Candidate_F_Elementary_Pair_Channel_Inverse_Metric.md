# LEAD-7 Candidate F — Elementary Pair-Channel Inverse Metric

**Purpose:** Handoff note for Claude Code after Candidate D failed the full Kerr-Newman boundary-curvature test.

**Core verdict:** Candidate D's failure is informative. It shows that a valid `n = 3` DBP complementarity metric must preserve elementary pair-channel zeros. Aggregating channels by a positive norm before inversion is too coarse.

---

## 1. What Candidate D taught us

Candidate D failed for a precise structural reason.

Candidate D aggregates individual pair couplings first:

```text
C_i = sum of Λ_i,pair^2 / q_i^2
```

and then inverts:

```text
g_ii = 1 / C_i
```

This destroys channel-zero information. If one pair coupling goes to zero at a reflection-fixed face, but another pair coupling in the same output chart stays nonzero or diverges, the sum hides the zero. The metric component may still collapse, but the curvature does not see the reflection singularity.

This matches the Candidate D report: the metric saw the extremal boundary but failed to make the intrinsic curvature diverge on the two reflection-fixed faces:

```text
Ω = 0
Φ_e = 0
```

The successful `n = 2` DBP metric is not just a boundary-collapsing metric. Its curvature must reproduce the complementarity law:

```text
GTD-II curvature:
order-2 poles on transition / Davies loci
finite on role boundaries

DBP curvature:
finite on transition / Davies loci
order-3 poles on generic role boundaries
order-4 poles at reflection-fixed role boundaries
```

Candidate D failing exactly at the reflection-fixed faces indicates that norm aggregation erased the channel-zero mechanism responsible for the order-4 pole.

---

## 2. Do not repair Candidate B as a pullback metric

Candidate B failed for a structural reason too.

Candidate B was:

```text
g_B = (dO)^T (dO)
```

Near a role boundary, the relevant channel or carrier component typically behaves like:

```text
O_or_κ ~ t^(-2)
```

Then:

```text
dO_or_dκ ~ t^(-3)
```

So the pullback metric behaves like:

```text
g_B ~ t^(-6)
```

That is the wrong valuation class. The paper metric instead uses inverse channel values, so the collapsing component behaves like:

```text
g_A ~ t^2
```

This difference explains why Candidate B produced an extremal pole around order 8 and missed Schwarzschild. The pullback metric measures sensitivity of the feature map. The DBP metric measures inverse channel accessibility.

Bank this lesson:

```text
Carrier faithfulness is not enough to define the DBP metric.

The metric must preserve the inverse-channel valuation law.
```

---

## 3. Candidate F — inverse-before-sum pair-channel metric

The next candidate should not be another pullback metric.

The next candidate should keep the paper's inverse-channel mechanism but avoid Candidate D's zero-blind aggregation.

Call it:

```text
Candidate F:
elementary pair-channel inverse metric
```

For each output charge:

```text
E_i = f_i(M, E_j, E_k)
```

there are three input-pair couplings:

```text
Λ_i,{M,j}
Λ_i,{M,k}
Λ_i,{j,k}
```

Define the positive elementary channel strengths:

```text
C_i,{a,b} = Λ_i,{a,b}^2 / q_i^2
```

with:

```text
q_i = 1 + |∇f_i|^2
```

Candidate D did:

```text
g_D,ii = 1 / ( C_i,{M,j} + C_i,{M,k} + t*C_i,{j,k} )
```

Candidate F instead does:

```text
g_F,ii =
    w_MQ / C_i,{M,j}
  + w_MQ / C_i,{M,k}
  + w_QQ / C_i,{j,k}
```

or, with one relative weight:

```text
g_F,ii =
    1 / C_i,{M,j}
  + 1 / C_i,{M,k}
  + u / C_i,{j,k}
```

Since:

```text
1 / C_i,{a,b} = q_i^2 / Λ_i,{a,b}^2
```

this is:

```text
g_F,ii = q_i^2 * [
    1 / Λ_i,{M,j}^2
  + 1 / Λ_i,{M,k}^2
  + u / Λ_i,{j,k}^2
]
```

Use the first test case:

```text
u = 1
```

This gives the simplest Frobenius-dual version.

---

## 4. Why Candidate F is the right next test

Candidate F reduces exactly to the paper metric at `n = 2`.

At `n = 2`, each output chart has only one off-diagonal pair coupling, so Candidate F becomes:

```text
g_F,ii = 1 / C_i
```

which is exactly the channel-inverse metric:

```text
g_DBP = -h^(-1)
```

It also preserves the thing Candidate D erased:

```text
individual channel zeros
```

At a reflection-fixed boundary, the order-4 divergence is tied to a symmetry-forced cross-derivative vanishing. Candidate D sums squared channels, so a zero channel can be masked. Candidate F inverts each elementary channel separately, so a zero elementary channel gives:

```text
1 / C_i,{a,b} -> infinity
```

This is the direct mathematical repair:

```text
Do not invert the norm of the channels.

Invert the elementary channel values first, then assemble.
```

---

## 5. Expected behavior of Candidate F

Candidate F should be tested against these expectations.

```text
n = 2 reduction:
exactly reproduces Candidate A / paper metric.
```

```text
extremal T = 0:
R diverges, expected generic order 3.
```

```text
Ω = 0:
R diverges, expected reflection-fixed order 4.
```

```text
Φ_e = 0:
R diverges, expected reflection-fixed order 4.
```

```text
Davies D3:
R finite.
```

```text
Kerr limit Q -> 0:
reduces cleanly to the n = 2 Kerr channel-inverse metric.
```

If Candidate F passes, it gives a stronger result than Candidate D:

```text
The correct n = 3 lift is not output-norm inverse.

It is elementary pair-channel inverse geometry.

The reflection-fixed order law forces preservation of individual channel zeros.
```

---

## 6. The theorem hiding in Candidate D's failure

Candidate D's failure suggests a theorem-shaped negative result.

```text
No norm-before-inversion diagonal metric can reproduce the full n = 3
reflection-boundary complementarity law whenever the reflection singularity is
carried by an individual channel zero masked by another nonzero channel in the
same output chart.
```

Simpler version:

```text
Reflection-fixed pole order requires zero-sensitive channel assembly.

Positive norm aggregation is zero-blind.

Therefore Candidate D(t)-type metrics cannot be the n = 3 DBP metric.
```

This remains useful even if Candidate F fails. It turns Candidate D's failure into a clean selection rule.

---

## 7. Candidate E — full pair-channel tensor, if F fails

Candidate E should stay on the bench, but do not open it before Candidate F.

Candidate E is:

```text
Candidate E:
pair-channel incidence tensor
```

Define:

```text
g_E =
Σ_i Σ_{a<b in inputs(i)}
    W_i,{a,b} * θ_i,{a,b} ⊗ θ_i,{a,b}
```

with either inverse-channel weights:

```text
W_i,{a,b} = 1 / C_i,{a,b}
```

or direct-channel weights:

```text
W_i,{a,b} = C_i,{a,b}
```

depending on whether the channel should collapse or pole in that direction.

The key unresolved choice is the incidence one-form:

```text
θ_i,{M,j}
```

and:

```text
θ_i,{j,k}
```

The charge-charge pair should probably not be assigned only to:

```text
dE_i
```

It should likely carry an incidence form such as:

```text
dE_j - dE_k
```

A first testable Candidate E version:

```text
θ_i,{M,j} = dE_i
```

```text
θ_i,{M,k} = dE_i
```

```text
θ_i,{j,k} = dE_j - dE_k
```

But only open Candidate E if Candidate F fails.

---

## 8. Watch for spurious interior poles

Candidate F may be too sensitive.

Because it inverts each elementary channel separately, it will blow up wherever any elementary channel vanishes:

```text
Λ_i,{a,b} = 0
```

This could introduce interior singularities.

That is not automatically bad. It may mean those are real channel-isotropy strata. But for the GTD complementarity metric, spurious interior curvature poles would be a failure unless they coincide with known role, Davies, or phase strata.

So Candidate F must include this gate:

```text
Interior-pole scan:
factor or sample all Λ_i,{a,b}=0 loci inside the physical KN wedge.

If R[g_F] has interior singularities away from Davies/role strata:
    Candidate F fails as the complementarity metric,
    but identifies channel-isotropy singularities for LEAD-2.
```

---

## 9. Optional systematic family — power-mean assembly

If Candidate F is close but not exact, use a controlled family rather than opening an infinite metric zoo.

Define:

```text
g_i^(α) = [ Σ_p w_p * C_i,p^α ]^(-1/α)
```

Special cases:

```text
α = 1:
Candidate D, norm-before-inversion.
```

```text
α -> -1:
harmonic assembly, zero-sensitive.
```

```text
direct reciprocal sum:
Candidate F, strongest zero-sensitive version.
```

This family can test whether the successful exponent is selected by the reflection law.

Use only if Candidate F is close but not exact.

---

## 10. Test ladder for Candidate F

Run these tests in order.

```text
Test F0:
Implement Candidate F with u = 1.

Check n = 2:
must equal paper Candidate A exactly.
```

```text
Test F1:
Run Kerr-Newman boundaries.

Targets:
T = 0      R pole order 3
Ω = 0      R pole order 4
Φ_e = 0    R pole order 4
D3         R finite
```

```text
Test F2:
Run Kretschmann.

Target:
K diverges at all role boundaries,
finite on D3.
```

```text
Test F3:
Interior singularity scan.

Target:
no unapproved curvature poles in the physical wedge.
```

```text
Test F4:
Q -> 0 Kerr reduction.

Target:
recovers the n = 2 metric or conformal class strongly enough to preserve
the exact pole coefficients.
```

```text
Test F5:
If F works, try weight u.

Question:
is u = 1 forced, or does every positive u work?
If every u works, find the canonical selector.
```

---

## 11. Recommended LEAD-7 brief update

Replace Candidate B as primary with:

```text
CANDIDATE F — elementary pair-channel inverse metric [PRIMARY NEXT]

For each output charge Ei, compute every elementary off-diagonal coupling channel
in that output chart. Invert each elementary channel strength before assembling.

This is the direct n = 3 generalization of the paper's inverse-channel metric.
It preserves the role-boundary valuation law and reduces exactly to the n = 2
metric. Its risk is spurious interior poles from elementary channel zeros.
```

Reclassify Candidate B:

```text
CANDIDATE B — carrier-pullback information metric [REFUTED for paper lift]

Fails n = 2 pole-order retrodiction:
extremal order ~8, Schwarzschild no pole.

Useful as a separate sensitivity geometry, not as the DBP complementarity metric.
```

Reclassify Candidate C:

```text
CANDIDATE C — three-channel pullback [BENCH]

Complementary but wrong extremal order.
May be a distinct geometry, not the paper metric.
```

Reclassify Candidate D:

```text
CANDIDATE D(t) — output-channel norm inverse [REFUTED for full n = 3 complementarity]

Passes n = 2 reduction and extremal n = 3 divergence.
Fails reflection-fixed faces Ω = 0 and Φ_e = 0 for all tested t.

Useful as evidence that norm-before-inversion aggregation is zero-blind.
```

---

## 12. Bottom line

There may still be a better metric worth investigating.

The best next candidate is:

```text
Candidate F:
elementary pair-channel inverse metric
```

It is better than Candidate D because it preserves individual channel zeros, which are exactly what reflection-fixed order-4 poles seem to require.

The deeper alternative is:

```text
Candidate E:
full pair-channel incidence tensor
```

but do not jump there until Candidate F fails.

Most importantly, Candidate D's failure gives a new theorem-shaped criterion:

```text
A valid n = 3 DBP complementarity metric must be zero-sensitive at the
elementary pair-channel level.

Aggregating channels by a positive norm before inversion is too coarse.
```

That is the insight to carry forward.

