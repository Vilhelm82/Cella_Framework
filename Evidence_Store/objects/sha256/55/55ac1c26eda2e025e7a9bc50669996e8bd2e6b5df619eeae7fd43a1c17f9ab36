#!/usr/bin/env python3
"""Direct post-CCE-8 mathematical replay (historical filename retained)."""

from fractions import Fraction as F
from pathlib import Path
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "engine/src").is_dir())
sys.path.insert(0, str(ROOT / "engine/src"))

from cella.continuation.cce8 import (
    FiniteRoleJet, act_finite_role_jet, finite_role_group_laws,
    truncate_finite_role_jet,
)
from cella.continuation.r3_ac_fold import ac_fold_root_interval, hostile_ac_fold_parameters
passed = 0


def check(label, condition):
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


jet = FiniteRoleJet(7, (
    (1,0,F(-3,2)), (0,1,F(-1,2)), (2,0,F(-13,8)), (1,1,F(-5,4)), (0,2,F(-1,8)),
    (3,0,F(2,7)), (2,1,F(-3,11)), (1,2,F(5,13)), (0,3,F(7,17)),
    (4,0,F(1,19)), (2,2,F(-2,23)), (0,4,F(3,29)),
    (5,0,F(2,31)), (3,2,F(-3,37)), (1,5,F(5,41)), (0,7,F(-7,43)),
))
left = truncate_finite_role_jet(act_finite_role_jet(jet, "sttst"), 4)
right = act_finite_role_jet(truncate_finite_role_jet(jet, 4), "sttst")
check("finite tower naturality", left == right)
check("finite role group laws", all(valid for _law, valid in finite_role_group_laws(jet)))

parameters = hostile_ac_fold_parameters()
high = ac_fold_root_interval(parameters, "high")
low = ac_fold_root_interval(parameters, "low")
check("R3 discriminant positive", parameters.discriminant > 0)
check("R3 high interval", high[0] > 3 and high[1] < 4)
check("R3 low interval", low[0] > 0 and low[1] < 1)
check("R3 roots separated", low[1] < high[0])

print(f"Post-CCE-8 direct mathematical replay: {passed} assertions passed")
