"""CCE-8 exact finite-order role-cover, boundary, tamper and checkpoint gate."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation.canonical import canonical_json_bytes
from cella.continuation.cce8 import (
    CCE8FiniteRequest, CCE8Request, CertifiedFiniteRoleCoverResult,
    CertifiedRoleCoverResult, FiniteRoleJet, RoleBoundaryEvent,
    act_finite_role_jet, classify_role_boundary,
    continue_finite_role_cover_certified, continue_role_cover_certified,
    finite_jet_from_order2, finite_role_group_laws, make_cce8_checkpoint,
    finite_tower_naturality, truncate_finite_role_jet,
    released_cce8_request, resume_cce8, verify_cce8_certificate,
    verify_cce8_checkpoint, verify_cce8_finite_certificate,
    verify_finite_tower_naturality,
)
from cella.continuation.model import Refusal


passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


results = {}
for word in ("e", "s", "t", "ss", "tt", "ststst", "st"):
    request = released_cce8_request(word, "P")
    first = continue_role_cover_certified(request)
    second = continue_role_cover_certified(request)
    check(f"{word} certifies", isinstance(first, CertifiedRoleCoverResult))
    check(f"{word} deterministic", canonical_json_bytes(first) == canonical_json_bytes(second))
    if isinstance(first, CertifiedRoleCoverResult):
        check(f"{word} verifies", verify_cce8_certificate(first.certificate) is True)
        results[word] = first

check("s2 identity", results["ss"].certificate.terminal_state.jet == results["e"].certificate.terminal_state.jet)
check("t2 identity", results["tt"].certificate.terminal_state.jet == results["e"].certificate.terminal_state.jet)
check("st3 identity", results["ststst"].certificate.terminal_state.jet == results["e"].certificate.terminal_state.jet)
check("t transports P role to D chart slot", results["t"].certificate.terminal_state.selected_chart_label == "D")
check("s leaves P role in P chart slot", results["s"].certificate.terminal_state.selected_chart_label == "P")
check("channel account permutes", dict(results["st"].certificate.channel_account_ledger)["terminal_kappa_digest"] == dict(results["st"].certificate.channel_account_ledger)["permuted_initial_kappa_digest"])
check("stable theorem ids", results["e"].certificate.theorem_ids[0].startswith("RC-I.1"))

higher_jet = FiniteRoleJet(
    4,
    (
        (1, 0, Fraction(-3, 2)), (0, 1, Fraction(-1, 2)),
        (2, 0, Fraction(-13, 8)), (1, 1, Fraction(-5, 4)), (0, 2, Fraction(-1, 8)),
        (3, 0, Fraction(2, 7)), (2, 1, Fraction(-3, 11)),
        (1, 2, Fraction(5, 13)), (0, 3, Fraction(7, 17)),
        (4, 0, Fraction(1, 19)), (2, 2, Fraction(-2, 23)), (0, 4, Fraction(3, 29)),
    ),
)
check("finite order-4 exact S3 laws", all(value for _, value in finite_role_group_laws(higher_jet)))
finite_request = CCE8FiniteRequest("paper-i-order4-st", higher_jet, "st", "P")
finite_first = continue_finite_role_cover_certified(finite_request)
finite_second = continue_finite_role_cover_certified(finite_request)
check("order-4 role cover certifies", isinstance(finite_first, CertifiedFiniteRoleCoverResult))
check("order-4 deterministic", canonical_json_bytes(finite_first) == canonical_json_bytes(finite_second))
if isinstance(finite_first, CertifiedFiniteRoleCoverResult):
    check("order-4 certificate verifies", verify_cce8_finite_certificate(finite_first.certificate) is True)
    check("order-4 is retained", finite_first.certificate.terminal_state.jet.order == 4)
    check("higher coefficients actively transform", finite_first.certificate.terminal_state.jet.coefficients != higher_jet.coefficients)
    check("finite channel projection permutes", finite_first.certificate.terminal_state.order2_channel_state.kappa_channels == tuple(
        finite_first.certificate.initial_state.order2_channel_state.kappa_channels[("P", "D", "S").index(label)]
        for label in finite_first.certificate.terminal_state.role_labels
    ))

order2_finite = finite_jet_from_order2(released_cce8_request("e").jet)
check("finite t agrees with released order-2 formula", act_finite_role_jet(order2_finite, "t").order2_jet() == results["t"].certificate.terminal_state.jet)
check("finite s agrees with released order-2 formula", act_finite_role_jet(order2_finite, "s").order2_jet() == results["s"].certificate.terminal_state.jet)

order7_jet = FiniteRoleJet(
    7,
    higher_jet.coefficients + (
        (5, 0, Fraction(2, 31)), (3, 2, Fraction(-3, 37)),
        (1, 5, Fraction(5, 41)), (0, 7, Fraction(-7, 43)),
    ),
)
for target_order in (2, 3, 4, 5, 6):
    tower = finite_tower_naturality(order7_jet, target_order, "sttst")
    check(f"order-7 to order-{target_order} tower commutes", tower.act_then_truncate_digest == tower.truncate_then_act_digest)
    check(f"order-7 to order-{target_order} tower verifies", verify_finite_tower_naturality(order7_jet, tower) is True)
check("tower truncation drops only high terms", truncate_finite_role_jet(order7_jet, 4) == higher_jet)
tower = finite_tower_naturality(order7_jet, 4, "st")
check("tower witness tamper rejects", isinstance(verify_finite_tower_naturality(order7_jet, replace(tower, target_order=3)), Refusal))

chart_boundary = classify_role_boundary((Fraction(0), Fraction(1), Fraction(1), Fraction(1), Fraction(1)))
check("chart boundary is typed", isinstance(chart_boundary, RoleBoundaryEvent) and chart_boundary.unavailable_output_roles == ("D",))
check("chart boundary is not regular", not chart_boundary.regular_active_role_locus and "active_chart_failure:a=0" in chart_boundary.stratum_types)
isotropy_boundary = classify_role_boundary((Fraction(2), Fraction(2), Fraction(2), Fraction(0), Fraction(2)))
check("channel-isotropy boundary is typed", isotropy_boundary.vanishing_channel_numerators == ("Lambda_P",))
check("isotropy keeps charts but loses faithfulness", not isotropy_boundary.unavailable_output_roles and not isotropy_boundary.regular_active_role_locus)
regular_event = classify_role_boundary(released_cce8_request("e").jet)
check("regular role locus classifies", regular_event.regular_active_role_locus and regular_event.stratum_types == ("regular_active_role_locus",))

singular = CCE8Request("singular", (Fraction(0), Fraction(1), Fraction(1), Fraction(1), Fraction(1)), "t", "P")
outcome = continue_role_cover_certified(singular)
check("missing chart refuses", isinstance(outcome, Refusal) and outcome.code == "RechartDomainViolation")
isotropic = CCE8Request("isotropic", (Fraction(2), Fraction(2), Fraction(2), Fraction(0), Fraction(2)), "s", "P")
outcome = continue_role_cover_certified(isotropic)
check("role divisor refuses", isinstance(outcome, Refusal) and outcome.code == "RoleDivisorCrossing")
wrong_scope = replace(released_cce8_request(), requested_scope="paper_v_cross_adapter_closure")
outcome = continue_role_cover_certified(wrong_scope)
check("Paper V escalation refuses", isinstance(outcome, Refusal) and outcome.code == "StageDependencyUnavailable")

cert = results["st"].certificate
check("role permutation tamper rejects", isinstance(verify_cce8_certificate(replace(cert, role_permutation=(("P", "P"),))), Refusal))
check("selection tamper rejects", isinstance(verify_cce8_certificate(replace(cert, selection_ledger=(("selected_geometric_role", "S"),))), Refusal))
check("source tamper rejects", isinstance(verify_cce8_certificate(replace(cert, source_ledger=(("paper_i", "0" * 64),))), Refusal))

checkpoint = make_cce8_checkpoint(results["st"])
check("checkpoint verifies", verify_cce8_checkpoint(checkpoint, results["st"]))
resumed = resume_cce8(checkpoint, results["st"].request)
check("resume certifies", isinstance(resumed, CertifiedRoleCoverResult) and resumed.certificate.previous_checkpoint_digest == checkpoint.checkpoint_digest)
check("checkpoint mutation rejects", not verify_cce8_checkpoint(replace(checkpoint, checkpoint_digest="0" * 64), results["st"]))

source = Path(__file__).resolve().parents[1].joinpath("src/cella/continuation/cce8.py").read_text()
check("campaign-local scout is separate from production", "pathfinder_m1_scout.py" not in source)
check("no external CAS", all(token not in source for token in ("import sympy", "import sage", "subprocess")))

print(f"CCE-8 exact finite-order role-cover gate: {passed} assertions passed")
