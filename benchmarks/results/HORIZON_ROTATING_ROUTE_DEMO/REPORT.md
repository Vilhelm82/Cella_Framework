# Horizon-rotating Pathfinder route demo

**Module:** `horizon_rotating` (content hash `705b7e556790`)
**Source:** `tools/wreath_engine/examples/horizon_rotating.json`
**Delivery mode:** `certified`
**Base group:** S5 (order 120), cover degree 5

## Routes planned from the module, executed end-to-end

| # | Route family | Executor | Wall time | Certificate |
|---|---|---|---:|---|
| 1 | `signed_contact_orbit_projection` | macaulay2 | 3.2556 s | closed |
| 2 | `kummer_finite_extension_primeness` | macaulay2 | 3.1733 s | closed |
| 3 | `rotating_three_channel_wreath_closure` | native (no M2) | 0.000519 s | f2_rank discharged in-core; group obligations external |

**Total wall time:** 6.4305 s
**M2 certificate replay:** all_closed

## Reference

Wreath-engine verify job `job_20260711T033436_b19195`: **961.3 s**,
53 gates, certified.

Routes cover the 16 contact walls, the delta_private primeness, and the rotating wreath-closure claim. The verify job's per-channel charpoly and structural gates are NOT covered by these routes.

## Artifacts in this directory

- `route1_contact_orbit.m2` / `.out.txt` — the emitted M2 script and its full transcript
- `route2_iz_primeness.m2` / `.out.txt` — the Kummer primeness route and its transcript
- `route3_wreath_closure.route.json` — the native wreath-closure `ComputationalRoute` (canonical serialization)
- `SUMMARY.json` — machine-readable per-route timings, certificate status, and coverage
