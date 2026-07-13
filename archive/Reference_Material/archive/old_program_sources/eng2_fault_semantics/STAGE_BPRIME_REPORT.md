# STAGE B′ — DIRECTION-LAW PROBE — STAGE REPORT (S-2026-07-05b)
**Authority:** PREREG_BPRIME (frozen pre-battery; final pin after the
pre-battery pin-completeness fix: see freeze_pins_bprime.sha256).
**Records:** `68698bf2…` byte-stable ×2. **Envelope:** 7.3 s vs 1200 s.
**Defect chains: NONE.** One pre-battery instrument defect caught by the
pin gate itself (pinfile relative-path depth error → REFUSE_MISMATCH →
pinfile regenerated before any run; gate worked as designed).

## Verdicts — ALL PASS
| id | verdict | note |
|---|---|---|
| PBp.0 | **PASS** | regression: all six Stage-B shadows reproduced exactly; projector gates n=4,5,6 |
| PBp.1 | **PASS** | both identities SYMBOLIC in g at n=4 (sympy cancel ≡ 0) |
| PBp.1b | **PASS** | same at n=5 (envelope non-issue: 7 s total) |
| PBp.2 | **PASS** | direction (−(n−2):2:n) at 9/9 fresh g-fixtures, exact ℚ |
| PBp.3a | **PASS** | s(g) symmetric + homogeneous deg 6−2n, symbolic, n=4 and 5 |
| referee | agree | symbolic zeros ⟺ numeric zeros at all fresh fixtures |

## The theorem candidate this stage assembled (status per clause)
```
shadow( Q_ν^{W-prod}(g) )  =  s(g) · [ (n−2)·I − A_1 ]
A_1 = Johnson J(n,2) adjacency;  spectrum (−(n−2), 2, n) on (triv, std, shape)
s(g) = e_3(g²) / ( C(n,3) · e_n(g²) )        [g² = (g_1²,…,g_n²)]
```
- Direction law: **CERTIFIED** — symbolic n=4,5; multi-g exact numeric n=6.
- Scalar closed form: **CERTIFIED at n=4,5** (the recorded factored
  polynomials ARE e_3(g²) and C(n,3)·e_n(g²) verbatim); general-n form
  FORMULATED (Level 4), proof owed.
- n=3 miracle EXPLAINED [STRUCTURAL]: s ≡ e_3/e_3 = 1 at n=3 — constant
  coefficients were the collapse of the scalar, not a separate accident;
  I.3a = the n=3 member with A_1 = J−I.
- General-n statement: FORMULATED; symbolic-in-n proof = next derivation
  step (no battery required; e_2 trace expansion + Johnson-scheme algebra).

## Residual measurements (PBp.4, record-only, banked)
R(g) = Q_ν − s·Q_univ is FULL RANK at every fixture (6/6, 10/10, 15/15) —
not a low-rank correction. Block structure: P_triv R P_triv ≡ 0 at all 15
fixtures; at n=4 additionally P_shape R P_shape = 0 and the triv↔shape
intertwiners vanish (support: ts/st, ss, ssh/shs only); at n=5,6 all blocks
except tt are active. The completion object is concentrated in std-anchored
blocks at n=4 and spreads at n≥5 — input for the covariant-completion
design, no claim staked.

## Will's desk (stage close)
1. Accept B′ verdicts (direction law CERTIFIED; ledger + dashboard deltas
   PROPOSED).
2. Next fork: (a) **derivation step** — general-n symbolic proof of the
   shadow law + scalar form (no battery; turns CERTIFIED-at-fixtures into
   PROVEN-for-all-n) [RECOMMENDED — cheapest path to the theorem];
   (b) covariant-completion probe for R(g) (new freeze);
   (c) return to flagship queue (CL-F3) with the law banked as-is.
3. CL-ENG2 remains gated (needs the full bridge or a ratio-law route
   through the certified shadow law — design question for (a)'s output).
