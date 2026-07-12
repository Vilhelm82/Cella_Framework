"""Gate the reusable native-period MCP adapters and their refusal boundary."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.mcp_server import (
    TOOL_GROUPS,
    call_dbp_certificate_verify,
    call_dbp_landen_trace_verify,
    call_dbp_relative_period,
    call_dbp_release_receipt,
    call_legendre_ke_enclose,
    call_legendre_pinning,
)


FAILS = []


def check(label, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}")
    if not condition:
        FAILS.append(label)


evaluated = call_dbp_relative_period("primary", 48)
certificate = evaluated["value"]["certificate_record"]
check(
    "N1 fixed DBP evaluator is MCP-callable with its canonical certificate",
    evaluated["ok"]
    and evaluated["value"]["target"] == "primary"
    and evaluated["value"]["dyadic_bracket"]["rounded_value_bits"] == 48
    and certificate["schema_id"]
    == "cella.dbp.native_relative_period_evaluator.certificate",
)

replayed = call_dbp_certificate_verify(certificate)
check(
    "N2 emitted certificate replays through a separate MCP operation",
    replayed["ok"] and replayed["value"]["accepted"] is True,
)

tampered = dict(certificate)
tampered["source_ledger"] = dict(tampered["source_ledger"])
tampered["source_ledger"]["sheet"] = "wrong"
refused = call_dbp_certificate_verify(tampered)
check(
    "N3 source-ledger tampering remains a typed refusal",
    not refused["ok"]
    and refused["refusal"]["token"] == "route_identity_failed"
    and refused["refusal"]["stage"] == "source_ledger",
)

k_value = call_legendre_ke_enclose("K", "1/4", 48)
e_value = call_legendre_ke_enclose(
    "E", {"type": "QSqrt", "a": "1/2", "b": "-1/4", "r": "2"}, 48
)
check(
    "N4 rational and QSqrt Legendre parameters retain native K/E certificates",
    k_value["ok"]
    and e_value["ok"]
    and k_value["value"]["atom"] == "K"
    and e_value["value"]["parameter"]["type"] == "QSqrt"
    and e_value["value"]["pinning_register"]["contains"] is True,
)

pin = call_legendre_pinning("1/4", 48)
outside = call_legendre_ke_enclose("K", "1", 48)
check(
    "N5 complementary pinning closes and the m=1 boundary refuses",
    pin["ok"]
    and pin["value"]["contains"] is True
    and not outside["ok"]
    and outside["refusal"]["token"] == "domain_separation_failed",
)

trace = call_dbp_landen_trace_verify()
check(
    "N6 Landen trace verifier runs all exact gates in clean child processes",
    trace["ok"]
    and trace["value"]["passed"] is True
    and trace["value"]["exact_gate_count"] > 40
    and "surface" in trace["value"]["scope_boundary"],
)

receipt = call_dbp_release_receipt()
check(
    "N7 stored release evidence is hash-pinned and honestly marked non-current",
    receipt["ok"]
    and receipt["value"]["verdict"] == "PASS"
    and receipt["value"]["stored_receipt_only"] is True
    and len(receipt["value"]["report_sha256"]) == 64,
)

expected = {
    "cella_dbp_relative_period",
    "cella_dbp_certificate_verify",
    "cella_legendre_ke_enclose",
    "cella_legendre_pinning",
    "cella_dbp_landen_trace_verify",
    "cella_dbp_release_receipt",
}
check(
    "N8 every native-period adapter is exposed through the arithmetic profile",
    expected <= set(TOOL_GROUPS["arithmetic"]),
)

print()
if FAILS:
    print(f"GATE MCP NATIVE PERIODS: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP NATIVE PERIODS: CLOSED — native DBP and Legendre work is reusable through MCP.")
