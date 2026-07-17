# STAGE B REPORT — the fold-edge mechanism (closed forms derived and certified)
**Date:** 2026-07-02 · **Governing:** MECH_PREDECL pin `c413c3f85ce7ff11` (targets frozen pre-script) · **Verification:** `stage_B/mech_verify.py` on the banked 40-digit folds, run ×2 in-directory, identical sha `9d51015735132846` · **Substrate:** [CONTAINER] analysis of [BOX]-certified data.

## The derivation [PROVEN, continuum leading order]
From rest, velocity terms vanish and `M(θ)·θ̈ = −∇V`. With `M = [[2,cΔ],[cΔ,1]]`,
`∇V = (2g sinθ1, g sinθ2)`, and `φ := θ2 − π`, the second row at `φ = 0` gives the drive
```
A(theta1) = theta2_dd |_{phi=0} = -g*sin(2*theta1)/(2 - cos^2(theta1))
```
From rest, `φ(t) = φ0 + (t²/2)·A(θ1(0)) + O(t⁴)`; the flip condition `φ(T)=0` with
`u ≈ −φ/2` gives `u0 = (T²/4)·A(θ1) + O(T⁴)`, so the tongue edge is the extremum of A.
Setting `dA/dθ1 = 0` with `x = cos2θ1` and `2−cos²θ1 = (3−x)/2` collapses to
`x(3−x) = 1−x²`, i.e. **`cos(2θ1*) = 1/3` exactly**, where `|A| = g·(2√2/3)/(4/3) = g/√2`.
```
u*(T) = g*T^2/(4*sqrt(2)) + O(T^4)          theta1*(T->0) = -arccos(1/3)/2
grid:  4000*u*(k) -> (6.25/sqrt(2))*k^2 = 4.419417382...*k^2
```
Sign check: the +u edge needs A > 0, i.e. sin2θ1 < 0 — the negative extremal angle, as
measured. (θ1 near −π also solves cos2θ1 = 1/3; the measured branch is the interior one.)

## Verification (targets frozen in MECH_PREDECL before the script existed)
| clause | result |
|---|---|
| M1 leading constant | extrapolated 4.41980 vs 4.41942, diff 3.8e−4, band 3e−3 — **PASS** |
| M2 extremal angle | extrapolated −0.6154985 vs −0.6154797, **diff 1.9e−5**, band 1e−3 — **PASS** |
| M3 drift sign | b = −0.00268 < 0 — **PASS** |
| M4 out-of-fit k=6,7 | residuals −0.0075 / −0.046, small and growing — reported, no verdict per predecl |

## Supersessions (registry-20 row filed)
"Leading behavior ≈ (9/2)k² [EMPIRICAL]" (STAGEB_rung2.md, STAGEB_ladder.md) is
**SUPERSEDED**: 4.5 was a third floors-level artifact; the true leading constant is
6.25/√2 [PROVEN + CERTIFIED-numeric]. The k² *scaling* statements stand.

## Standing after this report
Tongue-edge law: leading order CLOSED — constant and angle in closed form, mechanism
named, verified against independent 40-digit data under frozen targets.
OPEN: the T⁴ coefficient (same expansion, next order — θ1-motion and linear-in-φ
instability enter there); the discrete fixed-h admixture (the 3.8e−4 M1 gap sits inside
the frozen h² band; deriving it is the sharp next test); fold-locus ↔ branch-12.

## Process note
The banking commit `55d7911` preceded this file due to a broken shell chain (its message
overclaims its content by exactly this report); this commit completes it. No result is
affected — the verification sha and all clause verdicts are unchanged.
