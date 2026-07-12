# First M2 Pathfinder benchmark report

**Benchmark:** `m2-even-contact-delta-slice-a-v1`  
**Host:** 1.25.11  
**Trials:** one excluded warm-up plus 7 cold processes per route  
**Result equivalence:** `exact-generator-equivalence`  
**Certificate:** `external-replay-closed`  
**Release timing gate:** `OPEN`

## Result

Both paths returned the canonical generators:

```text
['J^2', 'M-11', 'N1-4', 'N2-8', 'N3-12', 'N4-20']
```

The structural route retained `J^2`; external replay also verified that `J` is not in the resulting ideal.

## Wall-clock measurements

| Route | Minimum | Median | Maximum | Peak RSS median |
|---|---:|---:|---:|---:|
| Generic saturation/elimination | 3.193912s | 3.221196s | 3.246451s | 358388 KiB |
| Wrapped Pathfinder structural route | 3.183676s | 3.236631s | 3.246762s | 358416 KiB |

Median speedup ratio `T_baseline / T_pathfinder`: **0.995231x**.

Pathfinder total time includes lowering, core analysis/selection, route lifting, M2 process startup and model loading, selected-route execution, and external certificate replay. M2 execution and certificate CPU telemetry are recorded separately in the JSON report; the complete combined host-process wall time is used in `T_total`.

## Gate decision

`Correctness passed, but the wrapped Pathfinder median is not below baseline; no speedup is claimed.`

No fabricated duration estimate participates in route selection. These are measurements taken after exact route admission and replay.
