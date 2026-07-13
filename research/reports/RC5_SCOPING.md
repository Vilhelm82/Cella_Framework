# RC-5 SCOPING SPIKE — the n=2 GTD/DBP spine, priced for LEAD-7

**Date:** 2026-07-06 · bounded side task approved by Will · NOT a certificate — a
scoping report. Nothing here is citable as verified; it enumerates what RC-5 must
re-verify and demonstrates feasibility at one fixture.
**Source:** `Reference_Material/gtd_vs_dbp.pdf` (2026-06-28 draft, 15 pp) — origin
currency; its own certainty tiers are quoted below and are claims, not evidence.

## 1. The claims RC-5 must re-verify (LEAD-7's load-bearing set)

| # | Claim (paper ref) | Origin tier |
|---|---|---|
| 1 | Kerr Christodoulou relation M(S,J) = sqrt(S/4π + πJ²/S); wedge 0 ≤ J ≤ S/2π | [literature] |
| 2 | Davies quartic 48π⁴J⁴+24π²J²S²−S⁴ = 0 ⟺ J²/M⁴ = 2√3−3 | [computer-verified] |
| 3 | GTD-II Kerr: g^II = ω·diag(−M_SS, M_JJ), ω = M/2; den K = S·(Davies)²; extremal factor absent (blindness) | [computer-verified] |
| 4 | DBP channels Λ_P = B, Λ_D = (Ab−aB)/a, Λ_S = (Ca−bB)/b; κ_c,i = −Λ_i²/q₀²; A_c three forms + telescoping | [symbolic]/[computer-verified] — already partially in-repo via RC-4 |
| 5 | Davies reconciliation Λ_D/Λ_P = −1; Λ_S/Λ_P = −(1+√3) | [symbolic] |
| 6 | Role-boundary = chart-singularity: a=0 ⟺ S=2πJ (extremal); b=0 ⟺ J=0 (Schwarzschild) | [symbolic] |
| 7 | DBP metric g^DBP = −h⁻¹, h = Σ κ_c,i dE^i⊗dE^i: exists, Riemannian in the wedge, det ∝ (S−2πJ)² extremal, component pole Schwarzschild | [computer-verified] |
| 8 | RADICAL CANCELLATION: every Λ_i carries the single factor √(M²), so g^DBP and R[g^DBP] are RATIONAL in (S,J,π) | [symbolic] — the tower keystone |
| 9 | Pole orders + leading coefficients: extremal order 3, C_ext = 2(8J+1)/(π(4J+1)³); Schwarzschild order 4, C_sch = −96πS/(16πS+1)²; R finite ≈ −0.043 on Davies | [symbolic] orders/coeffs; [computer-verified] values |
| 10 | Complementarity transfer to RN and vdW (orders 2/3/4 law) | [computer-verified] only — symbolic coefficients OPEN (paper track row) |

**DO-NOT-CITE flags found at origin:** eq. (28), the factored closed form of the KN
den R, is marked **[pending verification run]** in the paper itself; the Mahanta
modified-metric reading (m_sg = 0) is marked **[literature: confirm vs. source]**.
Neither may enter RC-5 as an input.

## 2. Tower verdict (the spike's question)

**π is units, not structure:** S = 2πσ makes Christodoulou fully rational —
`M² = (σ²+J²)/(2σ)`, polynomial constraint `2σM² − σ² − J² = 0`. Wedge J ≤ σ,
extremal σ = J, Davies 3J⁴+6J²σ²−σ⁴ = 0.

**Fixture demonstration (run 2026-07-06, exact ℚ end to end, no sympy, no float):**
at the interior rational point (σ,J) = (8,6), M = 5/2 (Davies factor 13616 ≠ 0):

```
jet:      a = 7/160,  b = 3/20,  A = 851/64000,  B = -171/8000,  C = 2/125
channels: kP = -7485696/17193765625,  kD = -230400/53919649,  kS = -6400/9903609
          q0 = 1049/1024,   A_c = 1605546817971022856192/57493557717514472900390625
metric:   h negative-definite, g^DBP positive-definite at the point (Result 4, fixture tier)
K[g^DBP]  = 406831198804171398850922570883255602113
            / 2367687477818631736432646387701278480000000        (exact rational)
```

Method: truncated bivariate Taylor jets over ℚ (degree 6) around the fixture —
series sqrt/reciprocal by Newton over Fractions, Brioschi curvature from series
coefficients. **The whole pipeline through the curvature scalar closes in ℚ at
rational-M fixtures; at general rational (σ,J) it closes in ℚ(√d), d = M², one
radical, field-closed.** No A-003 displacement: the tower holds.

## 3. The frame subtlety (found by the spike; RC-5 must respect it)

The rescale S = 2πσ is a coordinate change of the extensive frame, and the DBP
channels are frame quantities — so rescaled-frame numbers are a different gauge of
the construction, NOT retrodictions of the paper's π-frame coefficients (claim 9's
C_ext, C_sch carry explicit π). RC-5 therefore splits:

- **Structure tier (exact ℚ, rescaled frame):** existence, definiteness, boundary
  degeneration orders, complementarity/disjointness — frame-robust claims.
- **Retrodiction tier (exact ℚ(π), original frame):** the pinned coefficients,
  verbatim, with π an indeterminate in the rational function field ℚ(π)(S,J) —
  exact throughout given claim 8, which is itself re-proven first.

## 4. Route and price

The spike's truncated-jet-over-ℚ machinery generalizes directly to one-parameter
boundary approaches (exact Laurent order extraction at S → 2πJ and J → 0) — pole
orders WITHOUT full symbolic curvature, sidestepping the CAS blowup the spike hit
with naive sympy. Estimated cost of RC-5 proper: **1–2 sessions** (structure tier
~half, retrodiction tier + boundary Laurent ~one).

**LEAD-7 pricing conclusion:** no tower obstruction, no blocked prerequisite;
LEAD-7 is now tractability-competitive with LEAD-1. The choice between them is a
novelty-axis choice (pure-math grid originality vs physics-facing complementarity
lift), not a feasibility one.

## 5. Files

Spike computations were session-local (throwaway scripts, method recorded above);
per the re-verification rule nothing becomes citable until RC-5 exists as
`verification/recert_gtd_dbp_n2.py` with byte-stable ×2 output.
