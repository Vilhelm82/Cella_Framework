# Preliminary shared-process Pathfinder benchmark: all 16 signed-contact projections

> **Superseded for performance claims.** Order-stratified analysis exposed shared-process cache contamination. The final cache-isolated report is `CONTACT_ORBIT_ISOLATED_BENCHMARK.md`.

**Workload:** recorded stage-2 corpus deliverable, all sixteen contact-image ideals  
**Host:** 1.25.11  
**Design:** 30 paired, order-balanced, fresh-process trials after two excluded warm-ups  
**Outliers removed:** none  
**Exact equivalence:** `exact-ideal-equality-all-16`  
**External certificate:** `independent-triangular-presentation-replay-closed`

## Marginal algorithm result

Model loading and process startup occur before both in-process timers. Pathfinder marginal total includes Python lowering, core analysis/selection, route lifting, direct wall construction, and independent triangular-ideal certificate replay.

| Measurement | Median | 95% bootstrap CI |
|---|---:|---:|
| Generic elimination | 0.033306s | — |
| Pathfinder including certificate | 0.019096s | — |
| Paired time saved | 0.014271s | [0.008855, 0.019517]s |
| Paired speedup | 1.799x | [1.406, 2.175]x |

Pathfinder was faster in **30/30** pairs; exact two-sided sign-test `p=1.86e-09`.

## Cold end-to-end result

These trials include Python wrapper/core work, M2 startup, model loading, execution, and Pathfinder certificate replay.

| Route | Median wall time | Median peak RSS |
|---|---:|---:|
| Generic elimination | 3.209450s | 358624 KiB |
| Wrapped Pathfinder | 3.187367s | 358620 KiB |

Cold median ratio: **1.0069x**. The marginal benchmark answers whether the route is computationally better; the cold benchmark answers whether one isolated invocation amortizes M2 startup.

## Interpretation

`The structural route is admitted and benchmarked as a genuine algorithmic improvement only if the paired median difference and its 95% interval are positive. Cold-start performance is reported separately and is not allowed to erase or fabricate the marginal result.`
