# ARITH-I Stage B — session 2 note (r=2 channel exactness resolved; machinery + normalization validated)

**Date:** 2026-07-06. **PREREG:** `32f2fb3a` (Stage-B; the fabricated stop condition
is VOID). **Script:** `reports/arithmetic_track/arith_i_stageB_s2.py` (`3c18c25e`,
4/4 ×2). Builds on Stage B s1 (`6ed1232a`). Paper-track fence: no engine priority.

## What this session settled (all on the n=3 keystone — family-free)

**SBC-1 — the channel density's structure (exact).** The r=2 pure-coupling channel
density is the full Gaussian curvature weighted by height²:

```
kc = e_2(P Hc P)/q = −4P²/q² = (P²/3)·K_G ,     K_G = −12/q².
```

So `kc` is **not** constant-proportional to `K_G` — its exactness is a genuine
question, not inherited from Gauss–Bonnet.

**SBC-2 — the ansatz machinery is validated (control).** The Route-1 linear-algebra
ansatz recovers the known Gauss–Bonnet primitive of `K_G` at minimal degree,
`η_K = −2P(S dD − D dS)/(√q·w)`, `w=(2D+S)²+D²`, `dη_K = K_G dA` exactly. This is the
Gauss-map pullback of the S² area-form primitive (session-1 SBB-2), re-derived by the
exact machinery Route 1 uses at r=3.

**SBC-3 — the normalization is load-bearing (the key subtlety).** In the surface
chart, `kc·dA = −2P/q^{3/2} dD dS` in the **σ**-normalization (`q^{r/2}`), and
`−2P/q^{5/2} dD dS` in the **grid** normalization (`q^{(r+2)/2}`).
- σ channel (`−2P/q^{3/2}`): **no algebraic primitive** in the tested class
  (deg ≤ 4 over `√q·w`, and over `√q·w²`) — not exact *(search result, not a
  non-existence proof)*.
- grid channel (`−2P/q^{5/2}`): **EXACT** (SBC-4).

The A5/BRIEF exactness question uses the **grid** normalization (`q^{5/2}` at r=3), so
the EXACT case is the one that matters — and it **reproduces A5's premise** that "the
r=2 constant is end data because the density is exact." The earlier session-2 (Stage
A) refutations of naive weight forms were about a different object; here the object is
the channel density and the finding is positive in the correct normalization.

**SBC-4 — the r=2 grid-channel primitive (exact, explicit, verified).**

```
η_c = a/(q^{3/2} w) dD + b/(q^{3/2} w) dS,
a = (2P/9)(3DS² + 30D + S³ + 9S),
b = (2P/9)(−3D²S − DS² + 15D + 6S),          dη_c = grid r=2 channel density (exact).
```

## Consequence for r=3

The r=2 channel density **is exact in the grid normalization**, with an explicit
algebraic primitive — so (i) the r≥3 premise is live (not trivially decided), (ii) the
ansatz machinery and the normalization are validated end-to-end, and (iii) `H°` is
confirmed to be the **off-diagonal channel Hessian `Hc`** (the numerator-tower /
depth-theorem lineage), *not* the full Hessian — so r=3 is the genuine *channel*
question, not the trivial Gauss–Kronecker one (which is automatically exact).

## The remaining gate (unchanged, singular)

**OPEN B-1** — the specific ARITH-I n=4/n=6 quadric family. It is the *only* thing
between here and the r=3 verdict: the machinery is validated, the normalization pinned,
the density defined, `H°` fixed. Once the family is chosen (DBP n-general form if the
source is held / reconstruct the depth-theorem canonical family / coordinate LEAD-1),
the r=3 verdict runs immediately: build `η` by the SBC-4 ansatz on the n=4 surface
(dim-3 → a 2-form primitive), K-3 armed with the bump corroboration. A natural next
step that does **not** require pinning the family: run the r=3 ansatz on several
natural n=4 quadrics and test whether the exact/not verdict is family-robust.

## Ledger

r=2 channel: EXACT (grid), explicit primitive, verified. Machinery + normalization:
validated. `H° = Hc` (offdiag): confirmed. r=3 verdict: gated on OPEN B-1 only.
Nothing guessed.
