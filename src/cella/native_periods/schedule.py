"""Independent admission of the untrusted compile-time M1 schedule."""

from __future__ import annotations

import json
from importlib.resources import files


EXPECTED_OBLIGATIONS = (
    "exact_domain_separation", "panel_differentiability_radius",
    "fixed_dag_account_closure", "algebraic_recurrence_cauchy_remainder",
)


def admitted_m1_schedule(kernel_id: str) -> dict:
    raw = json.loads(files(__package__).joinpath("m1_schedule.json").read_text())
    if raw.get("schema") != "cella.dbp.native_periods.static_schedule.v1":
        raise ValueError("schedule schema mismatch")
    if raw.get("kernel_form") != "factored" or raw.get("rule") != "certified_taylor_interval_jet":
        raise ValueError("unadmitted kernel form or quadrature rule")
    panels = raw.get("panels")
    if panels not in (16, 32, 64, 128) or panels & (panels-1):
        raise ValueError("schedule bounds failed")
    if tuple(raw.get("obligations", ())) != EXPECTED_OBLIGATIONS:
        raise ValueError("schedule obligations incomplete")
    # Domain and real differentiability radius are independently re-proved by
    # the interval jet on every panel.  Account closure and the remainder
    # theorem are checked when those jets execute; this admission is not proof.
    segments = raw.get("kernel_schedules", {}).get(kernel_id)
    if not isinstance(segments, list):
        raise ValueError("kernel schedule missing")
    expanded = []
    for segment in segments:
        first, last = segment.get("first_panel"), segment.get("last_panel")
        order, guard, radius = segment.get("order"), segment.get("guard_bits"), segment.get("radius_multiplier")
        if not (isinstance(first, int) and isinstance(last, int) and 0 <= first <= last < panels):
            raise ValueError("invalid panel segment")
        if order not in range(24, 129) or guard < 64 or radius not in (2, 3, 4, 6, 8):
            raise ValueError("unadmitted panel parameters")
        expanded.extend({"panel": i, "order": order, "guard_bits": guard,
                         "radius_multiplier": radius} for i in range(first, last+1))
    if [x["panel"] for x in expanded] != list(range(panels)):
        raise ValueError("panel schedule is not an exact partition")
    return {"panels": panels, "panel_schedules": expanded}
