# ARITH-I Stage B — the r=3 exactness VERDICT (T-B / T-C resolved)

**Date:** 2026-07-06. **PREREG** `32f2fb3a`. **Certificate:**
`reports/arithmetic_track/arith_i_stageB_verdict.py` (`843a7689`, 3/3, byte-stable ×2).
Refs: `OPEN_B1_RESOLVED.md` (surface + density from calc log v8 / standing results
v1.1). Paper-track fence: no engine priority changed.

## Verdict

**The order-3 pure-coupling channel density `κ_{3;3,0} = −e_3(P Hc P)/q^{5/2}` is NOT
EXACT on the canonical n=4 surface.** Concretely, on `F = Σy_i² + Σ_{i<j}y_iy_j − c`:

```
∫_S κ_{3;3,0} dA  =  −2π²/(5c)   ( = −2π²/5 at c=1 )   ≠ 0
∫_S K_GK dA       =  2π² = vol(S³)                     (control, machinery-validated)
ratio  ∫κ / ∫K_GK =  −1/(5c)      ( −1/5 at c=1, −1/10 at c=2 — confirmed )
```

## The structural key — the surface is a COMPACT ELLIPSOID

The canonical n=4 quadratic form `M=(I+J)/2` has eigenvalues `5/2, ½, ½, ½` —
**positive definite**. So (unlike the n=3 keystone, a non-compact hyperboloid) the
n=4 surface is an **ellipsoid: a compact connected oriented 3-manifold** (≅ S³). On a
compact oriented `M^m`, a top-form `ω` is **exact ⟺ ∫_M ω = 0**. The verdict is then
immediate and rigorous: `∫_S κ_{3;3,0} dA = −3.948… ≠ 0` ⟹ not exact. (The `2π²`
Gauss–Kronecker control validates the area element + integration to ~1e-4, so the
nonzero value is not a numerical artifact of a true zero.)

This is exactly the "species change" **CALC-24 Part A** predicted: *"for n≥4 the
surface is (n−1)-dimensional and the invariant changes species (Gauss–Kronecker /
Chern–Gauss–Bonnet); the elliptic handle is bonded to the 3-role / 2-surface
geometry."*

## Resolution of T-B / T-C — a THIRD outcome, beyond the BRIEF's binary

The BRIEF staked a dichotomy: **C1** (higher Cohn-Vossen — the density is exact / end
data) vs **C2** (the r≥3 constants are transcendental interior periods of the double
cover). Both are premised on the **non-compact 2-surface (n=3)** picture. On the
canonical n≥4 surface neither holds:

- **C1 FALSE** — `∫κ ≠ 0`, the density is not exact; there is no Cohn-Vossen "end
  data" because the compact ellipsoid has no ends.
- **C2 is NOT the character** — the value `−2π²/5` is a **rational multiple of
  vol(S³)**, a **π²-rational**, not an elliptic/transcendental period.

The honest resolution: **the r=3 channel constant is a π²-rational** (topological
species — a rational multiple of the Gauss-map degree `vol(S³)`), determined by the
compact geometry. The "higher Cohn-Vossen vs interior period" question dissolves once
the surface is recognized as a compact ellipsoid. This is a genuine finding, and it
supersedes the addendum-A5 framing that treated the r≥3 grid as a continuation of the
n=3 elliptic period.

## Kills

**K-3** (primitive found AND bump moves the constant → contradiction): **NOT
triggered** — non-exactness was established directly by the compact-integral criterion
(`∫≠0`), no primitive was claimed, no contradiction. K-1/K-2/K-4 belong to Stage A
(all clean / K-2 closed).

## Staked conjecture (not proven — banked as the next thread)

`∫_S κ_{r;r,0} dA / ∫_S K_GK dA = −1/(n+1)` for general n (n=4 → −1/5). The `−1/5`
matched −0.2000000 to 7 digits at two resolutions; the general-n law is a numeric
conjecture, and the exact value `−2π²/(5c)` is EMPIRICAL (7-digit ratio) — a symbolic
proof (via the §I.3b Johnson-operator closed form, or a direct S₄-symmetry reduction
of the ellipsoid integral) is the clean follow-up.

## Prior-art obligation (owed before any external "theorem" claim)

The finding is "the coupling-channel curvature integral on the canonical symmetric
ellipsoid is a rational multiple of vol(S³)" — before framing this as novel, sweep:
total absolute curvature (Chern–Lashof), Gauss–Kronecker integrals of symmetric
quadrics, and Willmore-type functionals. The novelty candidate is the *channel*
(off-diagonal-Hessian) density specifically, not the full Gauss–Kronecker (which is
the classical `vol(S³)`).

## Status

**T-B RESOLVED (r=3 not exact; π²-rational, not a period). Stage B CLOSED.** ARITH-I
campaign: Stage A COMPLETE (family-tier closed form, K-2 closed), Stage B CLOSED (r=3
verdict). Remaining threads (open, banked): the `−1/(n+1)` conjecture + a symbolic
proof of `−2π²/5`; the prior-art sweep. LEAD-8 verdict: the r=3 channel constant is a
topological π²-rational, resolving the higher-Cohn-Vossen question in the negative and
reframing the transcendence vein (it lives on the non-compact n=3 side, not n≥4).
