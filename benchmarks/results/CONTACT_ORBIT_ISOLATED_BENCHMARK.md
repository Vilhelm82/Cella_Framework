# Pathfinder benchmark: 16 signed-contact projections, cache-isolated

**Workload:** recorded stage-2 corpus deliverable  
**Host:** 1.25.11  
**Design:** 30 paired trials; each route in a separate fresh M2 process; order alternated  
**Warm-up:** one excluded process per route  
**Outliers removed:** none  
**Exact baseline result:** `closed`  
**Independent Pathfinder certificate:** `closed`

## Marginal route cost

Internal M2 elapsed timings exclude process startup and model loading. Pathfinder total includes wrapper lowering, core recognition/selection, route lifting, direct wall construction, and independent triangular-presentation replay.

| Measurement | Median | 95% paired-bootstrap interval |
|---|---:|---:|
| Generic elimination | 0.032088s | — |
| Pathfinder including certificate | 0.015502s | — |
| Time saved | 0.015954s | [0.015429, 0.016489]s |
| Speedup | 2.014x | [1.996, 2.068]x |

Pathfinder was faster in **30/30** isolated pairs; exact two-sided sign-test `p=1.86e-09`.

## Cold end-to-end cost

Cold totals include separate M2 startup/model loading. Pathfinder also includes its Python wrapper/core overhead and external certificate replay.

| Measurement | Generic | Pathfinder |
|---|---:|---:|
| Median wall time | 3.354238s | 3.310936s |
| Median peak RSS | 358406 KiB | 358484 KiB |

Cold paired median speedup: **1.0088x**, 95% interval [1.0059, 1.0146]x. Pathfinder was faster cold in **24/30** pairs.

## Order-stratified check

| Stratum | Pairs | Marginal median speedup | Cold median speedup |
|---|---:|---:|---:|
| Baseline process first | 15 | 2.062x | 1.0083x |
| Pathfinder process first | 15 | 2.005x | 1.0093x |

The separate-process design prevents one route from populating Gröbner caches used by the other. Order strata remain visible to expose thermal or system-drift effects.
