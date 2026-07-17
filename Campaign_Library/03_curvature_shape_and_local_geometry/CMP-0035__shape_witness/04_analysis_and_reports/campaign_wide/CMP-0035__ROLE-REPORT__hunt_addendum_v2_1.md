# P-F3 HUNT ADDENDUM v2.1 — SATURATION AMENDMENT (supersedes HB.1 only)
**Status: FROZEN at commit, pre-runner-patch. Date 2026-07-03. Authority: continuation of Will's route-(b) ruling; construction defect discovered and repaired in ink.**

## Defect (banked, v2 records sha 468a661d499c9353 ×2)
v2 as frozen handed msolve the interpolated polynomials `τ_X · D1⁶ · D2⁶`. The clearing power K=6 overshoots the true denominator power, so all three polynomials share residual factors of the Cayley denominators — the solved variety contains the complex hypersurfaces `D1=0 ∪ D2=0`, hence DIM_POSITIVE on all eight slices (v2 outcome MIXED). Retro-diagnosis: v1's lex-Gröbner walls were the same poison — degenerate inputs with fat common factors, not hard 0-dimensional systems.

## Soundness of the repair [PROVEN]
`D1(t1) = 1 + Gram(U1(t1), v1)` and `D2(t2,t3) = 1 + Gram(U2(t2,t3), v2)`; Gram determinants are non-negative on ℝ, so `D1, D2 ≥ 1` at every real (hence every rational) point. Exactly dividing the tie polynomials by maximal powers of D1 and D2 therefore removes **no rational point** of the tie variety. The identity `(0,0,0)` lies on the tie variety and must survive division (runtime check).

## HB.1' (supersedes HB.1; all other clauses, kills, caps, and blob discipline carry unchanged)
HB.1': after the pinned K=6, D=15 interpolation with fresh-point self-check, each tie polynomial is exactly divided by the Cayley denominators D1(t1) and D2(t2,t3) to maximal powers with zero remainder required at every step, the saturated system verifiably vanishes at the identity, and it is handed to msolve with integer-cleared coefficients; D1 and D2 are bounded below by 1 on the reals, so no rational point is removed.

## depends_on additions
| artifact | pin |
|---|---|
| HUNT_ADDENDUM_v2.md (parent) | 70ed8967e1f06b24 |
| hunt_v2_msolve.py (pre-patch, produced the v2 records) | (see repo history, commit ab329cb) |
| v2 records sha (both runs) | 468a661d499c9353 |

frozen: true · version: 2.1 · author: Claude-container · authority: route-(b) continuation, S-2026-07-03
