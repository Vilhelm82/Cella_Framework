# π-ROTATION BOUNDARY CHASSIS — STAGE 0 PREDECL (S-2026-07-05)
**Status: FROZEN pre-battery (pin = sha at freeze commit). Authorization: PA-5
desk item 2, Will "accept defaults" S-2026-07-05. Runs BOX-PARALLEL to Stage B.**
**Prior-wins audit: the boundary chassis was designed-not-built in
HANDOFF_S2026-07-03 §fork(1); no boundary-family computation exists in the
corpus; no struck object used.**

## Object
Witness hunt (P-F3) continuation on the CHART BOUNDARY: the two-Cayley
sweep proved the interior obstruction is D-borne (SPLIT_PROBE, 9/9); the
boundary {angle-π rotations} is where the Cayley denominators — and hence
the obstruction's carrier — degenerate. Family (pilot slice, fixture (g,H)
n=5, all vectors = perp'd SLATES[0] data, deterministic):
```
A(t1,t2,t3) = cay(pu1 + t1·pe, pv1) · R_plane(p, q)
p = pu2 + t2·pe ,  q = pv2 + t3·pv1
R_plane = I − 2·M·adj(MᵀM)·Mᵀ / G2 ,  M = [p q] ,
G2 = |p|²|q|² − ⟨p,q⟩²   (Gram determinant — NOT of 1+(...) form;
                          the boundary family's only denominator besides D1)
```
Both factors fix g and are orthogonal ⟹ conjugation family ⟹ σ/Ê-ties free;
tie system = the three m2 ties, as on the interior chassis.

## Clauses / predictions (frozen)
| id | statement | class | prediction |
|---|---|---|---|
| PI.1 | AᵀA = I and A·g = g EXACTLY at every evaluation point | must | HOLDS (asserted inline; failure = K-PI1) |
| PI.2 | honest Rabinowitsch (y·D1·G2 − 1) tie ideal is 0-dimensional | sanity | HOLDS [PLAUSIBLE] |
| PI.3 | ideal degree | measurement | ≠ 704 [moderate]; record the number (GG = 88 = 2³·11 numerology flag on file — the interior degree's 11 may trace to Gram(g)) |
| PI.4 | interior square-lead law in its two-Cayley form | discriminating | does NOT persist unchanged [moderate] — the D-borne structure is halved/altered; record lead(w) square-class and factor spectrum via banked tools |
| PI.5 | rational tie points on the pilot slice | THE HUNT | NO prediction frozen. Screen (zero-root primes) + exact factorization (linear-factor cert), banked tools. ANY rational point ⟹ armed clause: exact witness verification (reconstruct point, verify ties in ℚ, then ORBIT-DISTINCTNESS exactly) BEFORE any witness language |

## Kills / envelope
K-PI1: any PI.1 assert or interpolation self-check failure ⟹ build defect,
HALT, audit. Grid job 1800 s / 8 GB; msolve 3600 s / 8 GB; exceed = datum.
Grid: D = 19 (degree ≤ 18/var), clearing K = 8, self-check ×3 random points
(inherited defenses from build_polys).

## Deliverables
`pi_stage0.py` (banked), `/tmp/pirot_s0.ms` + RUR + screen/factor grades ×2,
records under `campaigns/pi_rotation/records/`, ledger + carry rows per PA-4.
frozen: true · author: Claude-box · S-2026-07-05
