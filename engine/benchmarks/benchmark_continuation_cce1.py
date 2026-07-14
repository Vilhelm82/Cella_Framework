"""Isolated CCE-1 cold, marginal, and verifier timing harness.

Run once per target in a fresh Python process.  The first continuation call is
the cold end-to-end sample; subsequent calls measure the marginal cached path.
"""

from __future__ import annotations

import json
from statistics import median
import sys
from time import perf_counter_ns

from cella.continuation import (
    continue_certified,
    released_request,
    verify_continuation_certificate,
)
from cella.continuation.model import CertifiedResult


def elapsed_ms(callable_):
    start = perf_counter_ns()
    value = callable_()
    return value, (perf_counter_ns() - start) / 1_000_000


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"primary", "dual_cpv"}:
        raise SystemExit("usage: benchmark_continuation_cce1.py primary|dual_cpv")
    target = sys.argv[1]
    request = released_request(target, 192)

    result, cold_ms = elapsed_ms(lambda: continue_certified(request))
    if not isinstance(result, CertifiedResult):
        raise RuntimeError(f"cold run did not certify: {result!r}")

    marginal_ms = []
    for _ in range(9):
        repeated, sample_ms = elapsed_ms(lambda: continue_certified(request))
        if not isinstance(repeated, CertifiedResult):
            raise RuntimeError(f"marginal run did not certify: {repeated!r}")
        if repeated.evaluation_certificate.evaluation_digest != result.evaluation_certificate.evaluation_digest:
            raise RuntimeError("marginal run changed the evaluation digest")
        marginal_ms.append(sample_ms)

    verifier_ms = []
    for _ in range(25):
        report, sample_ms = elapsed_ms(
            lambda: verify_continuation_certificate(result.evaluation_certificate)
        )
        if not report.valid:
            raise RuntimeError(f"verifier rejected canonical result: {report!r}")
        verifier_ms.append(sample_ms)

    print(json.dumps({
        "schema_id": "cella.continuation.cce1_benchmark_sample",
        "schema_version": "1.0",
        "target": target,
        "requested_bits": 192,
        "process_isolation": "fresh process for this target",
        "clock": "time.perf_counter_ns",
        "cold_end_to_end_ms": cold_ms,
        "marginal_cached_median_ms": median(marginal_ms),
        "marginal_cached_samples_ms": marginal_ms,
        "verifier_median_ms": median(verifier_ms),
        "verifier_samples_ms": verifier_ms,
        "route_digest": result.route_certificate.route_digest,
        "evaluation_digest": result.evaluation_certificate.evaluation_digest,
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
