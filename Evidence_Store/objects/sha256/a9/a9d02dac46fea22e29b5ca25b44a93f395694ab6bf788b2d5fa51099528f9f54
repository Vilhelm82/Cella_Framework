# P-F3 HUNT ADDENDUM v2.2 — CHECK CORRECTION (supersedes v2.1's HB.1' only)
**Status: FROZEN at commit. Date 2026-07-03.**

## Correction (in ink)
v2.1's HB.1' asserted "the saturated system verifiably vanishes at the identity." **That premise was false as written:** the slice families evaluate at parameter (0,0,0) to the pinned base rotation `cayley(u1⊥,v1⊥)·cayley(u2⊥,v2⊥)`, which is not the identity, and the tie functions do not vanish there generically. The v2.1 runtime check fired correctly against a wrong specification (banked: run halted at slice 0, X=0, no records). The Cayley-factor diagnosis, the saturation repair, and its rational-point-preservation proof are untouched by this correction.

## HB.1'' (supersedes HB.1'; all other clauses, kills, caps, blob discipline carry unchanged)
HB.1'': after the pinned K=6, D=15 interpolation with fresh-point self-check, each tie polynomial is exactly divided by the Cayley denominators D1(t1) and D2(t2,t3) to maximal powers with zero remainder required at every step and the division multiplicities (a1_X, a2_X) recorded; saturation is verified at three fresh rational points by the exact identity P_sat(p) * D1(p)^a1_X * D2(p)^a2_X == P_raw(p); the saturated system is handed to msolve with integer-cleared coefficients; D1 and D2 are bounded below by 1 on the reals, so no rational point is removed.

## depends_on additions
| artifact | pin |
|---|---|
| HUNT_ADDENDUM_v2_1.md (parent, defect record) | 2deabfc84dd874c4 |
| HUNT_ADDENDUM_v2.md (grandparent) | 70ed8967e1f06b24 |

frozen: true · version: 2.2 · author: Claude-container · authority: route-(b) continuation, S-2026-07-03
