"""Emit the deterministic CCE-1 six-certificate inventory in one process."""

from __future__ import annotations

import json

from cella.continuation import continue_certified, released_request
from cella.continuation.canonical import canonical_digest
from cella.continuation.model import CertifiedResult
from cella.continuation.pathfinder import ADMITTED_REQUESTS


records = []
certificates = []
for target, bits in ADMITTED_REQUESTS:
    result = continue_certified(released_request(target, bits))
    if not isinstance(result, CertifiedResult):
        raise RuntimeError(f"released request refused: {target}/{bits}: {result!r}")
    record = {
        "target": target,
        "bits": bits,
        "plan_digest": result.plan.plan_digest,
        "route_digest": result.route_certificate.route_digest,
        "evaluation_digest": result.evaluation_certificate.evaluation_digest,
        "legacy_digest": result.route_certificate.legacy_certificate_digest,
    }
    records.append(record)
    certificates.append(result.evaluation_certificate)
    print(json.dumps(record, sort_keys=True, separators=(",", ":")), flush=True)

print(json.dumps({
    "bundle_sha256": canonical_digest(certificates),
    "records": records,
}, sort_keys=True, separators=(",", ":")), flush=True)
