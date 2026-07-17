# P-F3 HUNT ADDENDUM v2.3 — CURVE-SLICING EXTRACTION (extends v2.2; DIM_POSITIVE handling)
**Status: FROZEN at commit, pre-patch. Date 2026-07-03.**

## Finding that forces this (banked: v2.2 records sha 468a661d ×2)
All eight saturated slice systems are **dimension 1** (msolve-certified curves). Dimension count `3 + dim(T) − 6 = 1` implies the tie locus T is 4-dimensional in the sampled region — one above the identity-point rank-3 count — flagged as a mechanism question (see diagnostics below). Operationally: every slice already carries a curve of tie points; the hunt reduces to finding one rational point on one curve.

## HB.6 (new clause; HB.1''–HB.5 carry unchanged)
HB.6: for any slice whose saturated system is msolve-certified positive-dimensional, the runner intersects it with the pinned blind hyperplane schedule [t3 = 1, t3 = 1/2, t1 + t2 + t3 = 1, t1 - t2 = 1/3] in that order, solves each 0-dimensional result with msolve under the same 600-second cap, extracts rational points exactly per HB.3 semantics, certifies every candidate with the unchanged exact pipeline, and banks per-plane point sets canonically; the schedule was pinned before any curve was examined.

## Mechanism diagnostics (recorded, deterministic, blob-safe)
- D-1: division multiplicities (a1_X, a2_X) per slice enter the blob (observability repair).
- D-2: exact rank of the two-Cayley parametrization's three tangent vectors at the pinned rational point (t1,t2,t3) = (1/3, 1/5, 1/7) on slice 0 (rank 2 ⟹ the +1 dimension is a parametrization artifact; rank 3 ⟹ the tie locus is genuinely 4-dimensional there).
- D-3: disc(charpoly(H_fixture)) ≠ 0 recorded exactly (rules the H-stabilizer mechanism in or out).

## depends_on additions
| artifact | pin |
|---|---|
| HUNT_ADDENDUM_v2_2.md (parent) | a9d02dac46fea22e |
| v2.2 records sha (both runs) | 468a661d499c9353 |

frozen: true · version: 2.3 · author: Claude-container · authority: route-(b) continuation, S-2026-07-03
