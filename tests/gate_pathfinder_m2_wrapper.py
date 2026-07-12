"""Boundary gate for the external M2 Pathfinder wrapper."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools" / "pathfinder_m2"))

from cella.pathfinder import plan_request
from cella_pathfinder_m2 import M2ContactOrbitTask, M2ContactProjectionTask, lower_task, plan_and_lift
from cella_pathfinder_m2.wrapper import M2WrapperRefusal


FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


def task(**changes: object) -> M2ContactProjectionTask:
    values: dict[str, object] = {
        "request_id": "m2-even-contact-delta-slice-a-v1",
        "model_path": ROOT / "docs" / "files" / "horizon_wreath_inertia_model.m2",
        "slice_assignments": (("N1", 4), ("N2", 8), ("N3", 12), ("N4", 20)),
    }
    values.update(changes)
    return M2ContactProjectionTask(**values)  # type: ignore[arg-type]


host_task = task()
request = lower_task(host_task)
check("wrapper lowering preserves the model path", dict(request.external_binding)["model_path"] == str(host_task.model_path))
check("wrapper lowering preserves host object identities", dict(request.external_binding)["contact_component"] == "Ceven")

planning = plan_request(request)
check("route selection occurs in Pathfinder core", planning.route is not None and planning.route.route_family == "contact_restriction")
# PF-PLAN-002 evolution: generic_elimination is now a REGISTERED comparison
# candidate.  The structural route must win the ordered comparison and the
# generic candidate must receive an explicit rejection record instead of
# silently vanishing (updated 2026-07-12 when the provider registry landed).
check(
    "registered generic candidate loses the comparison with a recorded reason",
    any(r.route_family == "generic_elimination" for r in planning.rejected_alternatives)
    or planning.pareto_frontier == ("contact_restriction",),
)

lifted = plan_and_lift(host_task)
check("lifted object contains a route, not a final result", lifted.route_family == "contact_restriction")
check("lifted M2 avoids generic elimination", "saturate(" not in lifted.script and "eliminate(" not in lifted.script)
check("lifted M2 retains the doubled J node", "J^2" in lifted.script and "assert(J % structuralBase != 0)" in lifted.script)
check("certificate obligations cross the boundary", "multiplicity-retention" in lifted.certificate_obligation_ids)

with tempfile.TemporaryDirectory(prefix="pathfinder-m2-gate-") as temporary:
    script_path = Path(temporary) / "route.m2"
    script_path.write_text(lifted.script)
    completed = subprocess.run(
        ["M2", "--script", str(script_path)],
        capture_output=True,
        text=True,
        check=False,
    )
check("M2 executes the lifted route", completed.returncode == 0)
check("M2 emits the exact base-image presentation", "matrix {{N1-4, N2-8, N3-12, N4-20, M-11, J^2}}" in completed.stdout)
check("external M2 certificate replay closes", "PATHFINDER_M2_CERTIFICATE=CLOSED" in completed.stdout)

# Odd contact: the structural route refuses; the core may now admit the
# registered generic_elimination candidate instead — but the contact-task
# bindings carry no generator/ring declarations, so the wrapper must refuse
# to lift it loudly rather than execute any fallback (updated 2026-07-12).
try:
    plan_and_lift(task(sign_product=-1))
except M2WrapperRefusal as exc:
    refused = (
        "no_admissible_route" in str(exc)
        or "generic elimination requires" in str(exc)
        or "no M2 lifting contract" in str(exc)
    )
else:
    refused = False
check("wrapper surfaces refusal without fallback execution", refused)

orbit_task = M2ContactOrbitTask(
    request_id="m2-all-signed-contact-walls-v1",
    model_path=ROOT / "docs" / "files" / "horizon_wreath_inertia_model.m2",
)
orbit_lifted = plan_and_lift(orbit_task)
check("complete contact orbit selects the structural orbit route", orbit_lifted.route_family == "signed_contact_orbit_projection")
check("contact-orbit wrapper emits no generic elimination", "eliminate(" not in orbit_lifted.script)
with tempfile.TemporaryDirectory(prefix="pathfinder-m2-orbit-gate-") as temporary:
    script_path = Path(temporary) / "orbit.m2"
    script_path.write_text(orbit_lifted.script)
    orbit_completed = subprocess.run(
        ["M2", "--script", str(script_path)],
        capture_output=True,
        text=True,
        check=False,
    )
check("M2 executes the complete structural contact orbit", orbit_completed.returncode == 0)
check("structural orbit emits sixteen wall ideals", orbit_completed.stdout.count("matrix {{") == 16)
check("contact-orbit triangular certificate closes", "PATHFINDER_M2_CERTIFICATE=CLOSED" in orbit_completed.stdout)


print()
if FAILS:
    print(f"GATE PATHFINDER M2 WRAPPER: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER M2 WRAPPER: CLOSED")
