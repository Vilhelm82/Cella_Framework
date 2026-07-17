# CCE-1 isolated benchmark report v1.0

**Date:** 2026-07-14  
**Host scope:** this checkout and host; timings are characterization, not a portability claim.

Each target was measured in its own fresh Python process at 192 requested bits.
The first call is cold end-to-end evaluation. Nine subsequent calls measure the
cached marginal envelope path, and 25 independent certificate replays measure
verifier cost. The clock was `time.perf_counter_ns`.

| Target | Cold end-to-end | Cached marginal median | Verifier median |
|---|---:|---:|---:|
| primary | 9,979.733 ms | 3.789 ms | 2.701 ms |
| dual_cpv | 16,331.862 ms | 3.565 ms | 2.721 ms |

The cold and marginal figures are intentionally not combined into one speedup
claim. The marginal path benefits from the legacy evaluator's in-process exact
recurrence cache; the cold result includes the actual certified computation.

Harness: `engine/benchmarks/benchmark_continuation_cce1.py`.
