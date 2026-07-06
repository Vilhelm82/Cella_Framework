# Arithmetic track — dual-constant close-off

**Date:** 2026-07-06 · **Scope:** paper-track material (LEADS fence applies — this
does not set engine queue priorities; next open engine task remains G1.2).
**Artifacts:** `stage3_certification_v2.py` + `stage3_report_v2.json` (this
directory; report byte-stable ×2, sha `c0d95b48bdcc6dc6`; 20/20 gates; no naive
`ellippi(n>1, m)` evaluation on any certified path).
**Provenance:** external drafts (report PDF + two script iterations, ChatGPT/Will)
reviewed, corrected, and certified in-session; original drafts remain in
`Reference_Material/` (untracked, reference-only).

## 1. Objects

The keystone total-curvature constant and its Galois companion, on the elliptic
curve `Y² = X³ − X² + X − 1 = (X−1)(X²+1)` (Δ = −256, j = 128 — both re-verified
by hand):

```
I_primary = -2^(7/4) [ (3+2√2)·Π(n; k²)  − (2+2√2)·K(k²)  ],  k² = (2−√2)/4, n  = (4−3√2)/8
I_dual    = -2^(7/4) [ (3−2√2)·Π(n′;k′²) − (2−2√2)·K(k′²) ],  k′² = (2+√2)/4, n′ = (4+3√2)/8 > 1
```

`I_primary` retrodicts the standing 50-digit value exactly. `I_dual` requires a
branch convention since n′ > 1; the certified Cauchy-principal-value is

```
I_dual_CPV = -3.98800108597455809771976225753908737969412185555236029134797282037438
             2044301620084374998184536780571825905599613640469999524934769838194516
             297015969913667980232572633733216813738631005097537291913139724257892149600355947
```

**Correction record:** the originating PDF's printed value is wrong from digit 40
(`…9694131413…` → certified `…9694121855…`). Root cause: mpmath's singular-path
`ellippi(n>1, m)` loses ~25 internal digits. A session error of ours is owned in the
same breath: an initial "reproduces" check compared two runs of the same singular
path and missed that they disagreed at digit 40 — reproduction of an artifact is
not certification of a value. Case law: **never certify from a singular-path
special-function evaluation; always two independent routes.**

## 2. PROVEN (Stage 1 — the residue theorem)

For `ω = P·dx/((1−n′x²)·y)` on `y² = (1−x²)(1−k′²x²)`, `P = −2^(7/4)(3−2√2)`,
pole `x₀ = 1/√n′`:

```
x₀² = 12√2−16 ;  1−x₀² = (3−2√2)² ;  1−k′²x₀² = 3−2√2 ;  n′·(3−2√2) = √2/8
Res_bare(+x₀) = −2^(1/4)(3+2√2) ;   P·Res_bare = 4   (exactly)
```

Hand derivation plus machine proof: `minimal_polynomial(P·Res_bare) = x − 4`
(sign carried; no branch ambiguity). Corollaries: one-sided continuation differs
from CPV by ±4πi; the two continuations differ by 8πi; residues at the four curve
points over ±x₀ cancel pairwise (gate G3b).

## 3. CERTIFIED (numerics, with scope)

- Two independent CPV routes — complex-contour and the regular interchange
  identity `PV Π(n′;m) = K(m) − Π(m/n′; m)` with `m/n′ = 2√2−2 < 1` — agree to
  `3.2e−136` at dps 270. The 220-digit pin above is two-route certified to that
  floor and single-route (regular path, dps-stable) beyond.
- The paper-ready **regular closed form** (no CPV, every parameter in (0,1)):

```
I_dual = -2^(7/4) [ K(k′²) − (3−2√2)·Π(2√2−2; k′²) ]
```

- Period controls, gated against independent Carlson-RF computation (exact to
  working precision): `ω₁ = 2^(7/4)·K(k²)`, `Im ω₂ = −2^(3/4)·K(k′²)`,
  `Re ω₂ = ω₁/2` (rhombic). The 2^(7/4) scale in both constants is the period
  normalization.

## 4. STRUCTURAL (the honest duality)

```
λ(1−λ) = 1/8 for both moduli  ⟹  j(Legendre curve) = 10976 for primary AND dual
Φ₂(128, 10976) = 0            ⟹  2-isogenous to the minimal j = 128 model
λ ↦ 1−λ is an isomorphism      ⟹  primary/dual Legendre curves are THE SAME curve;
                                   Galois conjugation acts as the period swap
```

The differential lives on the j = 10976 Legendre curve, not on the j = 128 model;
any bilinear-relation program must carry the index-2 isogeny bookkeeping.

## 5. REFUTED / UNSUPPORTED (from the originating report)

- **REFUTED as stated:** "primary + dual = the period lattice / complete
  topological basis." PSLQ over ℚ(2^(1/4)) at 100 dps (controls validated,
  coefficients ≤ 10⁶) finds no relation placing either constant in the span of
  {ω₁, Im ω₂}; both are third-kind-dominated (differentials with poles — where
  the 4π residue lives), and two real numbers cannot span a complex lattice.
- **UNSUPPORTED:** "curvature over the classically forbidden region /
  thermodynamic shadow" — no change of variables connects the conjugated
  Legendre parameters to a region of the DBP surface. The defensible statement
  is the period-swap mechanism of §4.

## 6. OPEN (if the paper wants more)

Stage 2 of the proof plan: normalize ω as a third-kind differential on the
λ-curve, Riemann bilinear relations with the Abel–Jacobi position of the pole
divisor, transfer through the 2-isogeny to the j = 128 model. Only a
module-level "companion" statement (third-kind periods + quasi-periods +
residues) can survive §5's refutation.

## 7. Safer theorem statement (agreed frame)

```
PROVEN:   the branch structure of I_dual — residue 4, offsets ±4πi / 8πi.
CERTIFIED: I_primary (retrodicted), I_dual_CPV (two-route), the regular form,
          the period identities, j/isogeny structure.
CANDIDATE: I_dual as a principal-value third-kind companion on the conjugate
          reduction (Stage 2 to make precise).
NOT CLAIMED: lattice completion.
```
