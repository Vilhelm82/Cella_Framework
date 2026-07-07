# LEAD-7 Test 3 — Candidate F (elementary pair-channel inverse) at n=3, Kerr-Newman

**Date:** 2026-07-07. Certificate: `verification/lead7_test3_candF_n3.py`. Origin:
`Reference_Material/LEAD7_Candidate_F_Elementary_Pair_Channel_Inverse_Metric.md` (claims,
re-derived in-repo). Builds on Test 2 (`reports/LEAD7_test2_candD_n3.md`): Candidate D
(sum-before-invert) reproduced complementarity on only 1 of 3 role boundaries. Curvature
machinery (3D Ricci scalar `R` + Kretschmann `K`, exact partials) validated in Test 2 on
flat ℝ³ (→0) and the round 3-sphere (→6/a²).

## The two aggregation orders

Both candidates use the same elementary channels
`C_{i,{a,b}} = Λ_{i,{a,b}}²/q_i²` (two **mass-charge** pairs `{M,j},{M,k}`, one
**charge-charge** pair `{j,k}` per output chart), but assemble them oppositely:

```
D:  g_ii = 1 / ( C_{M,j} + C_{M,k} + t·C_{j,k} )         sum-then-invert  (zero-blind)
F:  g_ii = 1/C_{M,j} + 1/C_{M,k} + u/C_{j,k}             invert-then-sum  (zero-sensitive)
    = q_i²·[ 1/Λ²_{M,j} + 1/Λ²_{M,k} + u/Λ²_{j,k} ]
```

The doc's diagnosis (confirmed here): D's sum hides a channel *zero* — if one pair coupling
vanishes on a reflection-fixed face while another stays finite, `C` stays finite and the
curvature never sees the singularity. F inverts each channel first, so a vanishing channel
forces a metric pole.

## Results

### T3-1 — reduction to A at n=2 (remove Q as a charge)
The n=2 reduction means the 2-charge Kerr system (S,J): the entropy chart is `f_S(M,J)`
with a **single** mass-charge pair `{M,J}` and no charge-charge pair, so the F recipe gives
`g = q²/Λ²_{M,J} =` the paper metric A, `u` irrelevant (symbolic). Constraint (1) holds.

**Caveat (a genuine F subtlety, not present for D):** this is *not* the same as setting
`Q=0` in the 3-charge metric. In the 3-charge KN metric, `Q→0` is the **Φ_e=0 role
boundary**, where `Λ_{Se,{M,Q}} ∝ Q → 0` makes F's `1/Λ²` term *diverge* (correctly — see
T3-2). D reduces cleanly in both senses because it sums-then-inverts; F distinguishes them
because it inverts-then-sums. Both F behaviors are correct: reduce to A when Q is not a
charge, diverge on the Φ_e=0 boundary when Q is a charge whose value → 0.

### T3-2 — F(u=1) FIXES D's boundary failure, with the correct order law
Exact-partial `R` approaching each physical role boundary:

| boundary | Candidate D (Test 2) | **Candidate F (u=1)** | order |
|---|---|---|---|
| extremal T=0 | diverges | **diverges** | **3** (generic) |
| Ω=0 (J→0) | *finite* ✗ | **diverges** (R: 3e4→3e12→3e20) | **4** (reflection-fixed) |
| Φ_e=0 (Q→0) | *finite* ✗ | **diverges** (R: 5e2→5e10→5e18) | **4** (reflection-fixed) |

The orders read off cleanly: `R` grows ×10⁸ per 100× decrease in J (and Q) ⟹ order **4**
on both reflection-fixed faces; order **3** on extremal. This is exactly the paper's
complementarity law — order-3 generic, order-4 reflection-fixed — realized at n=3. The
mechanism: in the entropy chart `Λ_{Se,{M,J}} ∝ J·(2M²−Q²)·disc^{−3/2}` vanishes *on* J=0,
so F's `1/Λ²` term poles there. D summed it away.

### T3-3 — but F(u=1) FAILS the §8 interior gate
Invert-before-sum on the **charge-charge** term is too sharp. The Q-chart charge-charge
coupling `Λ_{Q,{Se,J}}` has an **interior zero** at `(M=2, J=0.826, Q=1.6988)` —
disc/M⁴=0.236, far from every boundary — and F(u=1) poles there:

```
Λ_cc → 0:   R = −0.004 → −0.158 → −14.6 → −1453   (order-2 pole, K~Λ⁻⁴)
```

This locus is **not** Davies: the Davies surface (M_SS=0) at that (M,J) is at Q=1.656, a
distinct curve. So F(u=1) has a spurious interior curvature pole on a channel-isotropy
stratum — the doc's §8 disqualifying condition (the stratum itself is a LEAD-2 object).

### T3-4 — F(u=0) reproduces the FULL complementarity AND is interior-clean
The interior pole comes entirely from the charge-charge term; the boundary divergences come
entirely from the mass-charge terms. Dropping the charge-charge term (**u=0**, mass-charge
only) keeps every boundary divergence and removes the interior pole:

| check | F(u=0) |
|---|---|
| n=2 reduction → paper metric A | ✓ |
| extremal T=0 | R diverges, **order 3** |
| Ω=0 (J→0) | R diverges, **order 4** |
| Φ_e=0 (Q→0) | R diverges, **order 4** |
| Davies D3 (M_SS=0, at (2,1.2,1.566)) | R = −0.0012, **finite** |
| interior scan (M∈{1.5,2,3}, ~1300 pts) | clean; max\|R\| at the smallest-J grid point (Ω=0 tail), not interior |
| the point that killed u=1 (2,0.826,1.699) | R = −0.0036, **finite** |

The mass-charge couplings vanish only on the role boundaries
(`Λ_{Se,{M,J}} ∝ J`, `Λ_{Se,{M,Q}} ∝ Q`, and the J/Q-chart analogues), never on an interior
curve (verified by direct zero-hunts: the smallest interior mass-charge coupling, 0.007, is
a benign local min near the extremal edge, not a zero).

### T3-5 — u=0 is uniquely selected
Near a charge-charge zero `Λ_{j,k}→0`, the `u/Λ²_{j,k}` term dominates:
- `u > 0` → `g_ii → +∞`: the spurious interior pole (T3-3).
- `u < 0` → `g_ii → −∞`: metric becomes indefinite (positive-definiteness lost).
- `u = 0` → finite and positive.

So **u=0 is the unique member of the F(u) family that is both interior-clean and
positive-definite**, and it retains every boundary divergence (all in the mass-charge
sector). Demonstrated numerically: near the zero, `g_QQ(u=+½) > 10⁶` while `g_QQ(u=−½) < 0`.

## Verdict

**Strong numerical (EMPIRICAL) evidence that the n=3 DBP complementarity metric is the
mass-charge inverse-channel metric**

```
g_DBP,ii = q_i² · Σ_{ρ = mass-charge pairs of chart i} 1/Λ_{i,ρ}²      (Candidate F, u=0)
```

It reduces exactly to the paper's `g^DBP = −h⁻¹` at n=2, and at n=3 Kerr-Newman it
reproduces the full complementarity law — curvature divergence of order 3 on the generic
role boundary (extremal T=0) and order 4 on the two reflection-fixed boundaries (Ω=0,
Φ_e=0), finite on the Davies surface — with **no spurious interior singularities**. The
charge-charge couplings, whose interior zeros wrecked F(u=1), are exactly the
channel-isotropy strata that belong to LEAD-2, not to the complementarity metric.

This resolves LEAD-7's central question (does a canonical n=3 DBP metric exist?) in the
affirmative, at the numerical tier, and identifies the construction:

- **not** the diagonal norm-inverse (Candidate D — zero-blind, misses reflection faces),
- **not** the carrier pullback (Candidate B — wrong valuation class),
- **but** the elementary **mass-charge** inverse-channel sum.

Banked selection rule (from the D and F(u=1) failures together):

> The n=3 DBP complementarity metric must be **zero-sensitive at the elementary
> mass-charge channel level** (invert each mass-charge coupling before summing) and must
> **exclude the charge-charge couplings** (whose zeros are interior isotropy strata, not
> role boundaries). Norm-before-inversion (D) is too coarse; inverting the charge-charge
> channels too (F, u>0) is too sharp. u=0 is forced.

## Next (to lift from EMPIRICAL → certified)

1. **Prove** `Λ_{i,{M,j}} = 0 ⟺` the role divisor of chart i (that the mass-charge channel
   zeros are *exactly* the role boundaries T=0/Ω=0/Φ_e=0, no others) — this upgrades the
   interior-cleanliness from a finite scan to a theorem.
2. **Exact pole coefficients** at each boundary (retrodiction tier), matching the paper's
   pinned `C_ext`, `C_sch` structure in the π-frame — the analogue of the n=2 RC-5
   retrodiction tier, now for KN.
3. Characterize the charge-charge zero locus as a LEAD-2 channel-isotropy stratum
   (hand-off to LEAD-2).
