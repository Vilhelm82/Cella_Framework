# LEAD-7 — carrier-pullback metric probe (Kerr n=2)

> **SUPERSEDED by the pole-order check (`LEAD7_pole_orders.md`, 2026-07-07).** The
> metric-divergence shown below is NECESSARY but NOT SUFFICIENT: the *curvature* R[g] of
> this pullback metric diverges order ~8 on extremal (not 3) and does NOT diverge on
> Schwarzschild — it FAILS the DBP complementarity/pole-order law. Candidate B is out.
> Kept as the record of the weaker check that misled the first recommendation.

**Date:** 2026-07-07. Probe (numerical, EMPIRICAL tier) substantiating the
carrier-pullback metric as a better DBP metric candidate than the paper's diagonal
`g^DBP=−h⁻¹` (Will's flag). Not a certificate — a design-decision probe. Origin:
`Reference_Material/gtd_vs_dbp.pdf` (claims, not evidence).

## The candidate

```
g_ab = Σ_{ρ∈{P,D,S}} (∂ κ_c^ρ/∂E^a)(∂ κ_c^ρ/∂E^b)  = (dO)ᵀ(dO),   E=(σ,J),
```
the pullback of the flat metric on carrier-space via the faithful carrier
`O=(κ_c^P,κ_c^D,κ_c^S)`. Channels from the role-channel calculus (Λ_P=B,
Λ_D=(Ab−aB)/a, Λ_S=(Ca−bB)/b; κ_c^ρ=−Λ_ρ²/q₀²) on Christodoulou M(σ,J).

## Result — the DBP complementarity holds, from the canonical construction

| location | g₀₀ | verdict |
|---|---|---|
| fixture (σ,J)=(8,6) | 0.0307, det 1.36e−7 | finite, positive (pos-def) |
| near extremal (6.01,6) | 6.51e9 | diverging |
| nearer extremal (6.0001,6) | 5.91e21 | **→ ∞ on σ=J (extremal)** |
| near Schwarzschild (8,0.01) | 3.80e6 | diverging |
| nearer Schwarzschild (8,0.0001) | 1.48e11 | **→ ∞ on J=0 (Schwarzschild)** |
| Davies (σ=15.2548,J=6) | 6.93e−5, det 1.61e−10 | **finite** |

So `(dO)ᵀ(dO)` **diverges on both physical role boundaries and is finite on Davies** —
exactly the DBP side of the complementarity law (Result 6), reproduced by a metric that
(unlike the diagonal `g^DBP`) is canonical, factors through O, is S₃-equivariant, and
generalizes to n=3 with no coupling-arrangement ambiguity.

## Mechanism (why it works)

On the extremal boundary `a=M_σ→0`, `Λ_D=(Ab−aB)/a → ∞`, so `κ_c^D → ∞` and its
gradient blows up ⟹ `g` diverges. On Schwarzschild `b=M_J→0`, `Λ_S=(Ca−bB)/b → ∞`
similarly. On Davies `M_σσ=0` (i.e. `A=0`), the Λ's are finite (A enters linearly, no
`1/A`), so `g` is finite. The divergence loci are the isotropy/chart-singularity loci
of the carrier — constraint (5) is automatic, not imposed.

## Caveats / next

- EMPIRICAL (finite-difference, 30-dps). The exact pole ORDERS (paper: order-3 generic,
  order-4 reflection-fixed) are NOT yet checked for this candidate — Stage-0 work
  (does `(dO)ᵀ(dO)` reproduce the paper's order law, or a different one?).
- Definiteness proven only pointwise; the wedge-wide statement is Stage-A.
- The head-to-head vs the diagonal `g^DBP` (which pole orders each gives) is the
  discriminator (LEAD-7 K-3).
