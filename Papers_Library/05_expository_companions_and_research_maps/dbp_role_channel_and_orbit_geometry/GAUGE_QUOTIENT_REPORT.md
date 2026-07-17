# GAUGE QUOTIENT REPORT — Campaign D (CL-D5)

## Question

Campaign A found 5298 reduced-tower classes holding distinct channel carriers, but left the gauge status unresolved: were those distinctions real geometry or defining-function gauge bookkeeping? Campaign D answers it exactly.

## Method

Over the **frozen Campaign A n=3 bound** — `g ∈ {(1,1,1), (1,2,3), (2,-1,1)}`, symmetric Hessian entries in `{-2,-1,0,1,2}`, zero Hessian skipped — group jets by `(q, reduced_tower)` and keep one representative per distinct direct carrier. For each separation class:

1. **gauge-classify** the representative pair with the exact same-`g` solver (`a = (Δg − (gᵀΔg/2q)·g)/q`, then verify);
2. compute **RoleChSpec** for every representative.

Because RoleChSpec is gauge-invariant, gauge-equivalent jets share a RoleChSpec, so a class with **≥ 2 distinct RoleChSpec fingerprints** contains a genuinely non-gauge-equivalent geometry pair — a **surviving** role-channel separation.

## Result

| count | value |
|---|---|
| candidate_pairs_total | 5298 |
| candidate_pairs_gauge_equivalent | 3057 |
| candidate_pairs_gauge_not_equivalent | 2241 |
| candidate_pairs_gauge_not_comparable | 0 |
| candidate_pairs_rolechspec_equal | 3057 |
| candidate_pairs_rolechspec_different | 2241 |
| **surviving_role_channel_separation_groups** | **3381** |

**Verdict: PASS_WITH_WITNESS.** Classification is complete and exact: 0 not-comparable (all same-`g`), 0 undecided, no KC-D5 violation.

### The exact identity that validates the invariant

For the representative pairs, **gauge-equivalent ⟺ RoleChSpec-equal**:

```
gauge_equivalent (3057) == rolechspec_equal      (3057)
gauge_not_equivalent (2241) == rolechspec_different (2241)
```

This is not assumed — it is measured. RoleChSpec is empirically *exactly* the same-gradient gauge invariant on this bound: it collapses every gauge-equivalent pair and separates every gauge-distinct one.

### Representative surviving witness

```
g  = (1,1,1)
H1 = [-2,-2,-2; -2,-2,-2; -2,-2,-1]
H2 = [-2,-2,-2; -2,-1,-1; -2,-1,-1]
reduced_tower(H1) == reduced_tower(H2) == (-2, 0)     (same reduced curvature)
gauge_status = GAUGE_NOT_EQUIVALENT                    (no a solves H2-H1 = g a^T + a g^T)
RoleChSpec(H1) != RoleChSpec(H2)                       (different active role carrier)
```

20 surviving witnesses are recorded in `summary.json → quotient_search.witnesses`.

## Required scientific wording

> Within the frozen Campaign A n=3 bound, at least one channel-carrier separation survives passive exclusion and exact same-gradient gauge quotienting after active graph-normalized role recharting.

In fact 3381 of 5298 separation classes survive. The remaining 1917 classes collapse entirely — **all** their representatives share a single RoleChSpec — so those separations were gauge-residual, the carrier difference being defining-function bookkeeping correctly quotiented away by RoleChSpec.

(Note: the per-class survival count, 3381, exceeds the rep-pair `rolechspec_different` count, 2241, because survival inspects *every* representative in a class, whereas the rep-pair columns inspect only the two lexicographically-first carriers. A class whose first two reps share a RoleChSpec can still survive on a third.)

Campaign D is eval-tier only; it does not promote anything to substrate and does not prove a full role-channel theory outside this frozen bound.
