"""Gate the improved Cella Pathfinder spec.

Run baseline/limit capture:
  python tests/gate_mcp_pathfinder_improved_spec.py --report docs/superpowers/reports/2026-07-08-pathfinder-spec-battery-baseline.json

Run improved regression:
  python tests/gate_mcp_pathfinder_improved_spec.py --expect-improved --report docs/superpowers/reports/2026-07-08-pathfinder-spec-battery-improved.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


EXPECT_IMPROVED = "--expect-improved" in sys.argv
REPORT_PATH = None
if "--report" in sys.argv:
    idx = sys.argv.index("--report")
    try:
        REPORT_PATH = Path(sys.argv[idx + 1])
    except IndexError:
        print("GATE MCP PATHFINDER IMPROVED SPEC: OPEN - --report needs a path")
        sys.exit(2)

FAILS: list[str] = []
LIMITS: list[str] = []
RESULTS: list[dict] = []


def _record(status: str, name: str, detail: str = "") -> None:
    label = {"pass": "PASS", "fail": "FAIL", "limit": "LIMIT"}[status]
    suffix = f" - {detail}" if detail else ""
    print(f"[{label}] {name}{suffix}")
    RESULTS.append({"name": name, "status": status, "detail": detail})
    if status == "fail":
        FAILS.append(name)
    elif status == "limit":
        LIMITS.append(name)


def check(name: str, ok: bool, detail: str = "") -> None:
    _record("pass" if ok else "fail", name, detail if not ok else "")


def improved(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        _record("pass", name)
    elif EXPECT_IMPROVED:
        _record("fail", name, detail)
    else:
        _record("limit", name, detail)


try:
    from cella.mcp_server import (
        call_diag_germ_classifier,
        call_route_plan,
        call_rewrite_candidates,
    )
except Exception as exc:
    print(f"GATE MCP PATHFINDER IMPROVED SPEC: OPEN - import failed: {exc}")
    sys.exit(1)


SWEEP = {"variable": "eps", "low": "1e-12", "high": "1e-4"}


def route(**kwargs):
    try:
        return call_route_plan(expression="eps", sweep=SWEEP, **kwargs)
    except TypeError as exc:
        return {
            "ok": False,
            "exception_type": "TypeError",
            "error": str(exc),
            "value": {},
        }


base = call_route_plan(expression="(1 + eps) - 1", sweep=SWEEP)
check(
    "BAT1 existing arithmetic route planner still detects rewrite-needed cancellation",
    base["ok"]
    and base["value"]["decision"] == "rewrite_candidate_needed"
    and "cella_rewrite_candidates" in base["value"]["next_tools"],
)

offset = call_rewrite_candidates(expression="(1 + eps) - 1", sweep=SWEEP)
check(
    "BAT2 existing rewrite generator still exposes constant-offset collapse",
    offset["ok"]
    and any(c["family"] == "constant_offset_collapse" and c["expression"] == "eps" for c in offset["value"]["candidates"]),
)

primitive = call_diag_germ_classifier(
    coordinate="x",
    native={"leading": "B", "power": "2", "parity": "even"},
    transverse=[
        {"leading": "A1", "power": "-2", "parity": "even"},
        {"leading": "A2", "power": "-2", "parity": "even"},
    ],
)
check(
    "BAT3 existing campaign primitive classifies the parity-fixed local law",
    primitive["ok"]
    and primitive["value"]["kind"] == "parity_fixed"
    and primitive["value"]["coefficient_text"] == "-14/(B)",
)

stage_c = route(
    domain="dbp",
    geometry={
        "case": "stage_c_pin_move",
        "pin_move_predicate": "whole_vector",
    },
)
overlay = stage_c.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT4 Pathfinder accepts a declared DBP domain and returns a geometry overlay",
    stage_c.get("ok") is True and overlay.get("authority") == "c001_eval",
    stage_c.get("error", "geometry_overlay missing"),
)
improved(
    "BAT5 Stage C pin/move routes through delta_kappa_c, not whole-vector predicates",
    overlay.get("channel_predicate") == "delta_kappa_c"
    and "whole_vector_predicate_superseded" in overlay.get("warnings", []),
    str(overlay),
)

regular = route(domain="dbp", geometry={"regularity_g": ["0", "1", "2"]})
regular_overlay = regular.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT6 single g_i=0 with q!=0 is regular rather than refused",
    regular_overlay.get("regularity_status") == "regular"
    and regular_overlay.get("regularity", {}).get("q") == "5",
    str(regular_overlay),
)

singular = route(domain="dbp", geometry={"regularity_g": ["0", "0", "0"]})
singular_overlay = singular.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT7 q=g^Tg=0 is the true DBP singular refusal locus",
    singular_overlay.get("regularity_status") == "q_zero_singular"
    and singular_overlay.get("regularity", {}).get("q") == "0",
    str(singular_overlay),
)

quantity = route(domain="dbp", geometry={"quantity": "kappa_squared"})
quantity_overlay = quantity.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT8 Pathfinder distinguishes K_G^2 from channel-norm square",
    "squared_total_KG" in quantity_overlay.get("quantity_definitions", {})
    and "channel_norm_sq" in quantity_overlay.get("quantity_definitions", {})
    and "ambiguous_kappa_squared" in quantity_overlay.get("warnings", []),
    str(quantity_overlay),
)

shape = route(domain="dbp", geometry={"n": 5})
shape_overlay = shape.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT9 n=5 scalar-spectrum shape routing requires carrier/witness machinery",
    shape_overlay.get("shape_resolution") == "carrier_required"
    and "cella_role_pair_loss_diagnostic" in shape_overlay.get("next_tools", []),
    str(shape_overlay),
)

reflection = route(
    domain="inverse_channel_metric",
    geometry={"metric_case": "reflection_face", "m": 2, "B": "B"},
)
reflection_overlay = reflection.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT10 reflection faces route to parity_fixed order-4 local law",
    reflection_overlay.get("local_germ_kind") == "parity_fixed"
    and reflection_overlay.get("local_law", {}).get("order") == "4"
    and reflection_overlay.get("local_law", {}).get("coefficient_text") == "-14/(B)",
    str(reflection_overlay),
)

extremal = route(domain="inverse_channel_metric", geometry={"metric_case": "extremal_face"})
extremal_overlay = extremal.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT11 extremal face routes to generic_quadratic order-3 local law",
    extremal_overlay.get("local_germ_kind") == "generic_quadratic"
    and extremal_overlay.get("local_law", {}).get("order") == "3",
    str(extremal_overlay),
)

corner = route(domain="inverse_channel_metric", geometry={"metric_case": "double_reflection_corner"})
corner_overlay = corner.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT12 double reflection corner routes to Newton-wedge analysis",
    corner_overlay.get("local_germ_kind") == "corner_newton_wedge"
    and "cella_corner_frontface" in corner_overlay.get("next_tools", []),
    str(corner_overlay),
)

metric = route(domain="inverse_channel_metric", geometry={"metric_case": "kn_metric"})
metric_overlay = metric.get("value", {}).get("geometry_overlay", {})
improved(
    "BAT13 KN metric route selects mass-role inverse-sum u=0 and preserves graph normalization",
    metric_overlay.get("metric_assembly") == "mass_role_inverse_sum_u0"
    and metric_overlay.get("role_role_policy") == "omit_as_channel_isotropy_diagnostic"
    and metric_overlay.get("graph_normalization_required") is True,
    str(metric_overlay),
)

summary = {
    "mode": "expect_improved" if EXPECT_IMPROVED else "baseline_limits_allowed",
    "pass_count": sum(1 for r in RESULTS if r["status"] == "pass"),
    "limit_count": len(LIMITS),
    "fail_count": len(FAILS),
    "results": RESULTS,
}
if REPORT_PATH is not None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nreport: {REPORT_PATH}")

print()
if FAILS:
    print(f"GATE MCP PATHFINDER IMPROVED SPEC: OPEN ({len(FAILS)} failing, {len(LIMITS)} limits)")
    sys.exit(1)
if LIMITS:
    print(f"GATE MCP PATHFINDER IMPROVED SPEC: BASELINE LIMITS RECORDED ({len(LIMITS)} limits)")
    sys.exit(0)
print("GATE MCP PATHFINDER IMPROVED SPEC: CLOSED - improved Pathfinder spec battery passes.")
sys.exit(0)
