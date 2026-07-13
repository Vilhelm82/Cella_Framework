# ARITH-I Stage B — session 1 note (r=3 exactness: setup, r=2 primitive, the gate)

**Date:** 2026-07-06. **PREREG:** `32f2fb3a` (Stage-B section; the fabricated
"two sessions" stop condition is VOID — `CORRECTION_2026-07-06_fabricated_stop_
condition.md`). **Script:** `reports/arithmetic_track/arith_i_stageB_s1.py`
(`6ed1232a`, 5/5 ×2). Paper-track fence: no engine priority changed.

## The question (T-B / addendum A5)

Is the order-r pure-coupling channel density
`κ_{r;r,0} = (−1)^r e_r(P Hc P)/q^((r+2)/2)` (`Hc = offdiag(H)`, `P = I − gg^T/q`,
`q = |∇F|²`) **exact** (= d of an algebraic form) on the quadric? r=2 YES is
Gauss–Bonnet; r=3 is the discriminator — YES → a "higher Cohn-Vossen" theorem for
channel densities; NO → the r≥3 grid constants are interior periods.

Definition re-derived (the engine's numerator tower, `src/cella/sensors.py`:
`κ_r=(−1)^r e_r(P Hc P)/q^(r/2)`, `r=2..n−1`; the integrable-density normalization
adds `1/q` per addendum A4 → `q^((r+2)/2)`). The depth theorem (portfolio Part IV)
names `κ_{r;r,0}` as "the r×r coupling minor", realizing Specht `S^(n−r,r)` for
`n≥2r`.

## What closed this session

**SBB-1 — the r=3 density needs n≥4 (proven, structural).** `P` projects out the
1-D gradient, so `rank(P Hc P) ≤ n−1`; at n=3 that is ≤2, hence **every 3×3 minor
vanishes and `e_3(P Hc P) ≡ 0` identically on the n=3 keystone** (verified
symbolically). The r=3 exactness question is therefore *not* a question about the
keystone surface — it lives on the n≥4 member (Specht-full at n≥2r=6). `e_2` stays
the live coupling channel at n=3 (`kc`). This is a structural fact, not a modeling
choice, and it reframes the campaign's r≥3 arm as inherently higher-n.

**SBB-2 — the r=2 explicit primitive (exact).** On the n=3 keystone the
Gauss–Bonnet primitive is the Gauss-map pullback of the sphere's area-form
primitive:

```
η = −N₃ (N₁ dN₂ − N₂ dN₁)/(N₁² + N₂²),     N = ∇F/|∇F|  (the Gauss map),
dη = K_G dA    exactly on the surface
```

verified at 8 exact rational points (exact algebraic zero); the pre-substitution
residual factors as `6(P/P − 1)`, i.e. `= 0` on `P² = 3−D²−DS`. **Only singularity:
`N₁=N₂=0`** — the Gauss map at the poles, i.e. the asymptotic/umbilic directions,
exactly where the end contribution `−2L` (Stage A) localizes. This is the explicit
"Gauss–Bonnet 1-form" the Stage-A handoff owed, it validates the exactness
*mechanism* constructively (beyond the abstract Gauss–Bonnet guarantee), and it is
the **template for the r=3 ansatz** (Route-1 machinery demonstrated at r=2).

**SBB-3 — the r=3 density is a real object.** On a sample n=4 quadric with rank-3
coupling, `e_3(P Hc P)` is a nonzero finite rational function of position
(sample value 21/31), so `q^(5/2)`-normalized it is a well-defined integrable
density — the r=3 test is about a genuine object, not the vacuous n=3 zero.

## The gate (honest OPEN, routed — not guessed)

**The specific ARITH-I n=4 (and n=6) quadric family is not fixed by the surviving
[CONTAINER] material, and the exactness answer depends on it.** The n=3 keystone
`F=D²+DS+P²−3` came from the DBP construction; its n-general form is not recorded as
a formula (the depth-theorem scripts `f1_*.py` are CONFIRMED ABSENT — reference
README audit), and the depth-theorem construction in the standing results gives the
Specht realization but not the surface's defining quadratic form. Per the standing
discipline (do not run a derivation on a guessed definition — the "elegant algebra
lies" rule), the family is **named as the gating sub-task**, not assumed:

> **OPEN B-1 — pin the ARITH-I r=3 surface.** Decide/derive the n=4 and n=6 quadric
> family on which `κ_{3;3,0}` is integrated. Options: (a) the DBP construction's
> n-general form, if Will holds the source; (b) the depth-theorem canonical family
> (reconstruct CALC-31..35's surface from scratch, re-verifying the Specht
> realization as the calibration anchor); (c) coordinate with LEAD-1 / a GRID_I
> prereg if that campaign fixes the grid surface. The choice is load-bearing (it can
> change YES/NO), so it is Will's call / a derivation gate, not a default.

Once B-1 is pinned, the r=3 verdict runs as prereg'd: **Route 1** (ansatz primitive
`ω` with `q`-power denominators, `dω = density` → linear algebra — the SBB-2 η is
the r=2 proof-of-method) and **Route 2** (compact bump deformation leaving the
family; if `∫ κ_{3;3,0}` moves, exactness is dead), K-3 armed (primitive found AND
bump moves ⟹ HALT).

## Ledger

r=2 primitive: exhibited, exact. Structural n≥4 requirement: proven. r=3 density:
real, computable. r=3 verdict: **gated on OPEN B-1** (family pin). No kill fired
(K-3 belongs to the verdict run). Nothing guessed.
