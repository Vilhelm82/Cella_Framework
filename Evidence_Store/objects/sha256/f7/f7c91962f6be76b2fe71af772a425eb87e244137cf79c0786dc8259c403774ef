#!/usr/bin/env python3
"""Exact lift-chain, deck-parity and return-stem lateral verifier."""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "engine/src").is_dir())
sys.path.insert(0, str(ROOT / "engine/src"))

from cella.continuation.corridors import (  # noqa: E402
    CORRIDORS, INITIAL_ROOT_ISOLATOR, PUNCTURES, TERMINAL_ROOT_ISOLATOR,
    lift_disk_chain,
)

passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


check("initial isolator selects +sqrt2", INITIAL_ROOT_ISOLATOR.isolating_rectangle[:2] == (F(1), F(2)))
check("terminal isolator selects -sqrt2", TERMINAL_ROOT_ISOLATOR.isolating_rectangle[:2] == (F(-2), F(-1)))
for name, manifest in CORRIDORS.items():
    charts, overlaps = lift_disk_chain(manifest)
    check(f"{name} ordered chart count", len(charts) == 29)
    check(f"{name} ordered overlap count", len(overlaps) == 28)
    check(f"{name} charts avoid branch locus", all((chart.center - point).norm_squared() > chart.radius ** 2 for chart in charts for _, point in PUNCTURES))
    check(f"{name} strict overlap witnesses", all((w.common_point - charts[w.left_chart].center).norm_squared() < charts[w.left_chart].radius ** 2 and (w.common_point - charts[w.right_chart].center).norm_squared() < charts[w.right_chart].radius ** 2 for w in overlaps))
    check(f"{name} odd branch parity", sum(value for point, value in manifest.windings if point in {"plus_i", "minus_i"}) % 2 == 1)
    check(f"{name} terminal sheet", manifest.terminal_sheet == "rho=-sqrt(2)")
check("upper exact h0", F(1) == 1)
check("upper return sign selects up", CORRIDORS["upper"].selected_target_quotient_class.startswith("[delta_-^up]"))
check("lower return sign selects down", CORRIDORS["lower"].selected_target_quotient_class.startswith("[delta_-^down]"))
check("compact corrections retained", all("Z[A]+Z[B]" in m.unresolved_compact_correction for m in CORRIDORS.values()))
print(f"DBP corridor lift and lateral class: {passed} assertions passed")
