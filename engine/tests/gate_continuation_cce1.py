"""CCE-1 compatibility, envelope, verifier and checkpoint gate."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation import (
    InsufficientProofBudget,
    UnsupportedRequest,
    continue_certified,
    released_request,
    resume_continuation,
    verify_continuation_certificate,
)
from cella.continuation.canonical import canonical_json_bytes
from cella.continuation.checkpoint import make_checkpoint, verify_checkpoint
from cella.continuation.model import ProofBudget
from cella.continuation.pathfinder import ADMITTED_REQUESTS, construct_plan
from cella.native_periods import evaluate_dbp_relative_period


passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


request = released_request("primary", 192)
direct = evaluate_dbp_relative_period("primary", 192)
first = continue_certified(request)
second = continue_certified(request)
check("CCE-1 returns CertifiedResult", type(first).__name__ == "CertifiedResult")
check("legacy digest remains recertified", first.route_certificate.legacy_certificate_digest == direct.certificate_digest == "a2ee898068f07889de338866a97d86d221758f40dbaf80cebeaa8b7ad83fadde")
check("nested legacy bytes are unchanged", first.evaluation_certificate.legacy_certificate_json.encode() == canonical_json_bytes(direct.certificate_record))
check("same-process envelope bytes are deterministic", canonical_json_bytes(first) == canonical_json_bytes(second))

report = verify_continuation_certificate(first.evaluation_certificate)
check("independent envelope verifier accepts canonical result", report.valid and report.code == "verified")
check("verifier replays all CCE-1 obligations", len(report.checked_obligations) == 11)

for target, bits in ADMITTED_REQUESTS:
    plan = construct_plan(released_request(target, bits))
    check(f"plan exists for {target}/{bits}", type(plan).__name__ == "PathfinderPlan")

small = replace(request, proof_budget=ProofBudget(31, 87, 281))
small_outcome = continue_certified(small)
check("valid but inadequate schedule is not invalid", isinstance(small_outcome, InsufficientProofBudget))
check("adequacy refusal is stable", small_outcome.refusal.code == "proof_budget_exhausted")

unsupported = continue_certified(replace(request, requested_bits=191))
check("request outside PF-0 scope refuses", isinstance(unsupported, UnsupportedRequest))
check("unsupported precision has stable code", unsupported.refusal.code == "unsupported_path")

legacy_record = json.loads(first.evaluation_certificate.legacy_certificate_json)
legacy_record["account_ledger"]["closed"] = False
tampered_legacy = replace(
    first.evaluation_certificate,
    legacy_certificate_json=json.dumps(legacy_record, sort_keys=True, separators=(",", ":")),
)
check("tampered nested legacy account is rejected", not verify_continuation_certificate(tampered_legacy).valid)

tampered_plan = replace(first.plan, plan_digest="0" * 64)
tampered_route = replace(first.route_certificate, pathfinder_plan=tampered_plan)
tampered_evaluation = replace(first.evaluation_certificate, route_certificate=tampered_route)
check("tampered Pathfinder plan is rejected", not verify_continuation_certificate(tampered_evaluation).valid)

tampered_pf0 = replace(first.route_certificate, pf0_confirmation_digest="0" * 64)
check("tampered PF-0 report link is rejected", not verify_continuation_certificate(
    replace(first.evaluation_certificate, route_certificate=tampered_pf0)
).valid)

checkpoint = make_checkpoint(request, first.plan, first.route_certificate.route_digest)
check("checkpoint verifies", verify_checkpoint(checkpoint, request, first.plan).valid)
check("checkpoint digest tampering is rejected", not verify_checkpoint(
    replace(checkpoint, checkpoint_digest="0" * 64), request, first.plan
).valid)
wrong_path_request = replace(request, exact_path_digest="0" * 64)
check("checkpoint path mismatch is rejected", not verify_checkpoint(
    checkpoint, wrong_path_request, first.plan
).valid)
resume_bad = resume_continuation(replace(checkpoint, checkpoint_digest="0" * 64), request)
check("public resume returns typed checkpoint refusal", isinstance(resume_bad, UnsupportedRequest) and resume_bad.refusal.code == "checkpoint_chain_invalid")

native_source = "\n".join(
    path.read_text()
    for path in (Path(__file__).resolve().parent.parent / "src/cella/native_periods").glob("*.py")
)
check("legacy evaluator remains continuation- and Pathfinder-free", "cella.continuation" not in native_source and "cella.pathfinder" not in native_source)

print(f"CCE-1 compatibility and certificate envelope: {passed} assertions passed")
