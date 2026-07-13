"""Extended M2 integration gate: non-contact fixtures through the wrapper.

Covers handoff test requirement 7 (M2 integration beyond the contact route):
1. generic_elimination — the PF-PLAN-002 comparison candidate on a small ideal,
   checked for exact equivalence against a direct M2 baseline.
2. kummer_finite_extension_primeness — the rotating IZ primeness fixture
   (preferred fixture #2 of the build handoff), route-only plus certified.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools" / "pathfinder_m2"))

from cella.pathfinder import plan_request
from cella_pathfinder_m2 import (
    M2DifferenceIdealPrimenessTask,
    M2GenericEliminationTask,
    lower_generic_elimination_task,
    plan_and_lift,
)

FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


def run_m2(script: str, name: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix=f"pathfinder-m2-{name}-") as temporary:
        script_path = Path(temporary) / f"{name}.m2"
        script_path.write_text(script)
        return subprocess.run(
            ["M2", "--script", str(script_path)],
            capture_output=True,
            text=True,
            check=False,
        )


# --- fixture 1: generic elimination ----------------------------------------
elimination_task = M2GenericEliminationTask(
    request_id="m2-generic-elimination-twisted-cubic-v1",
    variables=("t", "x", "y", "z"),
    weights=(1, 1, 1, 1),
    generators=("x - t**2", "y - t**3", "z - t**4"),
    eliminate_variables=("t",),
)
planning = plan_request(lower_generic_elimination_task(elimination_task))
check(
    "generic elimination route is selected by the core",
    planning.route is not None and planning.route.route_family == "generic_elimination",
)

lifted = plan_and_lift(elimination_task)
check("elimination lift translates ** into M2 powers", "t^2" in lifted.script and "**" not in lifted.script)
check("elimination lift eliminates the declared variable", "eliminate(workingIdeal, {t})" in lifted.script)

completed = run_m2(lifted.script, "generic-elimination")
check("M2 executes the generic elimination route", completed.returncode == 0)
check(
    "elimination certificate replay closes",
    "PATHFINDER_M2_CERTIFICATE=CLOSED" in completed.stdout,
)

baseline_script = """S = QQ[t, x, y, z];
baseline = trim eliminate(ideal(x - t^2, y - t^3, z - t^4), {t});
print "PATHFINDER_M2_BASELINE_BEGIN";
print toString gens baseline;
print "PATHFINDER_M2_BASELINE_END";
"""
baseline = run_m2(baseline_script, "elimination-baseline")
check("baseline elimination executes", baseline.returncode == 0)


def extract(block: str, begin: str, end: str) -> str:
    return block.split(begin, 1)[1].split(end, 1)[0].strip()


route_generators = extract(completed.stdout, "PATHFINDER_M2_RESULT_BEGIN", "PATHFINDER_M2_RESULT_END")
baseline_generators = extract(baseline.stdout, "PATHFINDER_M2_BASELINE_BEGIN", "PATHFINDER_M2_BASELINE_END")
check(
    "route and baseline produce the exact same eliminated ideal",
    sorted(route_generators.replace(" ", "").strip("matrix{}").split(","))
    == sorted(baseline_generators.replace(" ", "").strip("matrix{}").split(",")),
)

route_only = plan_and_lift(elimination_task, certified=False)
check(
    "route-only elimination lift omits certified delivery",
    "PATHFINDER_M2_CERTIFICATE" not in route_only.script,
)

# --- fixture 2: rotating IZ primeness (Kummer P4 route) ---------------------
primeness_task = M2DifferenceIdealPrimenessTask(
    request_id="m2-rotating-iz-primeness-v1",
    model_path=REPO_ROOT / "docs" / "files" / "horizon_wreath_inertia_model.m2",
)
primeness_lift = plan_and_lift(primeness_task, certified=False)
check(
    "IZ primeness selects the Kummer finite-extension route",
    primeness_lift.route_family == "kummer_finite_extension_primeness",
)
check(
    "primeness route-only script avoids generic decomposition",
    "primaryDecomposition" not in primeness_lift.script
    and "minimalPrimes" not in primeness_lift.script,
)
primeness_run = run_m2(primeness_lift.script, "iz-primeness-route-only")
check("M2 executes the primeness route (route-only)", primeness_run.returncode == 0)
check(
    "primeness route emits the difference-ideal presentation",
    "PATHFINDER_M2_RESULT_BEGIN" in primeness_run.stdout,
)

certified_lift = plan_and_lift(primeness_task, certified=True)
check(
    "certified primeness lift carries the squarefree gcd replay",
    "gcd(radicandPoly, radicandDerivative) == 1" in certified_lift.script,
)
check(
    "certified primeness lift replays the Thm 16.1 codim/degree data",
    "codim IZ == 6" in certified_lift.script and "degree IZ == 64" in certified_lift.script,
)
certified_run = run_m2(certified_lift.script, "iz-primeness-certified")
check("M2 executes the certified primeness route", certified_run.returncode == 0)
check(
    "primeness certificate replay closes",
    "PATHFINDER_M2_CERTIFICATE=CLOSED" in certified_run.stdout,
)


print()
if FAILS:
    print(f"GATE PATHFINDER M2 EXTENDED: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER M2 EXTENDED: CLOSED")
