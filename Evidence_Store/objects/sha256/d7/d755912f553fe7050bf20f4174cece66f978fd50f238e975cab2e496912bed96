# STAGE B REPORT — the second-order fold law (closed forms, no free parameters)
**Date:** 2026-07-02 · **Governing:** T4_PREDECL pin `a4e70c973004ff3b` (targets frozen pre-script; hand-candidate G≈−12.8 pre-registered as expected casualty) · **Derivation+grading:** `stage_B/t4_derive.py`, ×2 identical sha `baf480805a5eb895` · **Substrate:** [CONTAINER] symbolic, graded against [BOX] 40-digit folds.

## The law [PROVEN, continuum through T⁴ — the script is the derivation certificate]
```
u*(T)  = (g/(4*sqrt(2)))*T^2 + (g^2*(sqrt(3) - 2*sqrt(2))/64)*T^4 + O(T^6)
theta1*(T) = -acos(1/3)/2 - (g*(5*sqrt(2) + 3*sqrt(3))/36)*T^2 + O(T^4)
```
Route: exact Lagrangian → exact EOM (CAS-solved, zero hand algebra) → from-rest even
Taylor `θ(t) = θ0 + (t²/2)F + (t⁴/24)(F_θ·F + F_vv[F,F])` → series solve of the flip
condition → extremization. Closed forms extracted by PSLQ and verified:
`16G + 50√2 − 25√3 = 0` (residual 2.5e−29), `18d₂ + 25√2 + 15√3 = 0` (residual 0.0),
with the g-scaling (G ∝ g², d₂ ∝ g) confirming the dimensional structure.

## Grading (targets = banked coefficients, frozen first)
| clause | predicted | banked | diff | band | verdict |
|---|---|---|---|---|---|
| P-T4a (u k⁴ coeff) | −0.00267670 | −0.00267804 | **1.3e−6** | 4.0e−4 | **PASS** |
| P-T4b (θ1 k² coeff) | −0.00212973 | −0.00213212 | **2.4e−6** | 4.3e−4 | **PASS** |

Both residuals sit at the k⁶-truncation scale — the error itself is behaving as the
theory predicts. The hand-expansion candidate (G≈−12.8) died as pre-registered; the
CAS pipeline supersedes hand algebra for all future orders.

## What this closes / opens
CLOSED: the tongue-edge law through second order; the θ1*-drift mechanism; the "form
unidentified" verdict from the fold report (r(k) was the mixed footprint of a clean
even-T series — the earlier no-poly-fits puzzle dissolves: fits in k missed the
extremal-angle drift coupling).
OPEN: T⁶ (same pipeline, one more order — would predict the M4 residuals with no
freedom); the discrete-h² admixture (the surviving ~5e−4 relative gap); modular tower;
fold-locus ↔ branch-12.
