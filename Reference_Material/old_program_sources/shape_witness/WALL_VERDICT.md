# WALL_VERDICT — E1 FLAGSHIP STAGE 0 WALL_SCOUT (THE ENGINE Stage C)
**Date:** 2026-07-03 · **Prereg:** `WALL_SCOUT_PREDECL.md`, pin `b8d6c404131e7db7` (FROZEN pre-battery, commit `5003086`) · **Battery:** `wall_scout.py` (engine_harness's first consumer: clause_gate + pin_gate fired on every invocation) · **Records:** `wall_scout_records/` (container ×2 + box ×2, full stdout).

## The measured wall (MC.3 verdict)
**INCLUDED(n=6). INCLUDED(n=7). No wall anywhere in the scouted range.**
n-budget for the flagship = **{5, 6, 7} at full tier** — n=7 sheds its "scout-tier" caveat. Worst measured op: OP3 at n=7 = **2.235 s wall / 58.0 MB RSS** on the primary substrate, against the envelope 1200 s / 8192 MB — a **537× time margin and 141× memory margin**. B3's ladder constraint "and the wall scout permits the cost" is satisfied vacuously through the scouted range; the binding constraint on any degree climb is now purely the insufficiency-certification side.

| (op, n) | container max wall (s) | container max RSS (MB) | box max wall (s) | verdict |
|---|---|---|---|---|
| OP1, 6 | 0.121 | 53.2 | 0.052 | fits |
| OP2, 6 | 0.343 | 55.1 | 0.153 | fits |
| OP3, 6 | 0.781 | 56.0 | 0.296 | fits |
| OP1, 7 | 0.468 | 56.3 | 0.189 | fits |
| OP2, 7 | 0.571 | 57.6 | 0.229 | fits |
| OP3, 7 | 2.235 | 58.0 | 0.835 | fits |

## Clause grades (all green; kills armed, none fired)
- **MC.1 PASS** — RECORDS_SHA256 `c7dab7eb0e48d8a7` on both container runs AND both box runs. **Bonus [OBSERVED]:** the blob is byte-identical *across substrates* — four agreeing runs on two machines (the probe-2 cross-instantiation pattern, again).
- **MC.2/MC.3 PASS** — envelope comparison above; primary substrate authoritative.
- **MC.4 PASS** — box secondary banked; ~2.7× faster; no threshold authority, as frozen.
- **MC.5 PASS** — witness_battery re-certified via harness immediately pre-scout (PA.1 PASS, `39bed5552c805f4d` ×2).
- **MC.6 PASS** — frozen numbers RECORDED: Molien graded invariant counts on the pair module = **a₁=1, a₂=3, a₃=8 at BOTH n=6 and n=7**. Grading of P-F1 (a₂=3 expected) belongs to flagship Stage A; noted: the recorded numbers equal the CL-F1 mechanism's demand.
- **MC.7 PASS** — projector gates green at both n: ranks (1,5,9) and (1,6,14) = (1, n−1, n(n−3)/2) exactly; idempotency; partition of identity.

## Observations banked (labels calibrated; no claims graded here)
1. **a₃ = 8 at both n=6 and n=7** [OBSERVED, exact Molien] — the degree-3 invariant budget is n-stable across the scouted range. Suggestive for CL-F4 (n-uniform closed forms); representation-stability flavor. Observation only.
2. **J_rank = 7 (full) at both n** [OBSERVED at the pinned generic fixture] — the degree-≤2 detector suite (Ê₁..Ê₄, m2_triv, m2_std, m2_shape) has locally independent components at a generic point at n=6,7. Single-fixture evidence; no genericity claim.
3. Cost scaling OP3 n=6→7 ≈ 2.9× on ~1.9× subset count — comfortably polynomial in the scouted range. n=8,9 look reachable on these margins [OBSERVED extrapolation, out of frozen scope].

## Status moves (per predecl §7 + PA-1)
- **WALL_VERDICT banked; flagship Stage 0's B2 duty DISCHARGED.** Auto-filed per the PA-1 measurement class (predecl frozen+pinned pre-battery `5003086`; clauses embedded and gate-verified at runtime; calibration control green; byte-stable ×2 per substrate; records banked; kills armed, un-fired).
- Umbrella **Stage C: CLOSED**. Flagship Stage 0 state: DF freezes live in the frozen brief (`3b3fca42`), fixtures pinned (predecl §3), calibration control green (MC.5), Molien counts recorded (MC.6), wall measured (this verdict). **Per the brief's Stage-0 gate, what remains is Will's Go** — the ladder (B3) and stop-rule (B4) stay armed; nothing here pre-commits a degree climb.

## Will's desk
Flagship **Stage A** on your word: CL-F1 proof (quadratic basis, cheap PROVEN target), CL-F2 sweep ×2, and the P-F3 witness hunt (the all-m2-tied pair). Stage B (umbrella: L3 stratum classifier) remains queued and independent.
