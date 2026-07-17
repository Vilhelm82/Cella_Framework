# CCE-4 benchmark report v1.0

The clean-process full-release replay took **223.82 s** and **26,232 KiB** peak RSS. It reconstructed and verified all six certificates, created and checked checkpoints, resumed them, and compared the canonical bundle.

A separate primary/192 measurement took **10.045268 s cold** and **0.050778 s warm** in one process. The warm number measures only marginal CCE-4 envelope/class replay after the native certified recurrence cache is populated. It is not a cold evaluator speedup and must not be advertised as one. Both executions produced certificate digest `279037e9...2c0e`.

Command:

```text
/usr/bin/time -f 'elapsed_seconds=%e max_rss_kb=%M' env PYTHONPATH=engine/src python research/campaigns/CELLA_CONTINUATION_ENGINE/05_cce4_evaluator/verify_cce4_bounded_evaluation.py
```
