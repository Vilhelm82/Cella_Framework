#!/usr/bin/env python3
"""Exact R3 AC-fold native realization, functor, and hostile-fixture gate."""

from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation.canonical import canonical_json_bytes
from cella.continuation.model import Refusal
from cella.continuation.r3_ac_fold import (
    ACFoldObject,
    ACFoldParameters,
    CertifiedACFoldResult,
    ac_fold_route,
    compose_ac_fold_routes,
    continue_ac_fold_certified,
    hostile_ac_fold_parameters,
    reduce_ac_fold_morphism,
    reverse_ac_fold_route,
    verify_ac_fold_certificate,
)
from cella.continuation.selected_skeleton import compose_skeleton_morphisms


passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


params = hostile_ac_fold_parameters()
check("precommitted discriminant is twelve", params.discriminant == 12)
check("precommitted polynomial is v2-4v+1", (params.linear_coefficient, params.constant_coefficient) == (-4, 1))

high = ACFoldObject.build(params, "high")
identity = ac_fold_route(high, 0)
one_loop = ac_fold_route(high, 1)
two_loops = ac_fold_route(high, 2)
check("identity fixes high sheet", identity.target == high)
check("one loop swaps sheets", one_loop.target.sheet == "low")
check("two loops fix sheet", two_loops.target == high)

reverse = reverse_ac_fold_route(one_loop)
check("reversal negates winding", reverse.winding == -1)
check("route followed by reverse is identity", compose_ac_fold_routes(one_loop, reverse).target == high)
check("route winding composes additively", compose_ac_fold_routes(one_loop, ac_fold_route(one_loop.target, 3)).winding == 4)

first = continue_ac_fold_certified(one_loop)
second = continue_ac_fold_certified(one_loop)
check("native result certifies", isinstance(first, CertifiedACFoldResult))
check("native result deterministic", canonical_json_bytes(first) == canonical_json_bytes(second))
if isinstance(first, CertifiedACFoldResult):
    cert = first.certificate
    check("certificate independently replays", verify_ac_fold_certificate(cert) is True)
    check("high root lies in precommitted interval", cert.high_root_interval[0] > 3 and cert.high_root_interval[1] < 4)
    check("low root lies in precommitted interval", cert.low_root_interval[0] > 0 and cert.low_root_interval[1] < 1)
    check("root brackets disjoint", cert.low_root_interval[1] < cert.high_root_interval[0])
    check("adapter preserves source sheet", cert.skeleton_source.selected_branch == "high")
    check("adapter preserves target sheet", cert.skeleton_target.selected_branch == "low")
    check("adapter records odd monodromy", cert.skeleton_morphism.monodromy_parity == 1)
    check("no existing arm oracle", dict(cert.dependency_ledger)["existing_arm_oracle"] == "none")
    check("sheet mutation rejects", isinstance(verify_ac_fold_certificate(replace(cert, route=replace(cert.route, target=high))), Refusal))
    check("interval mutation rejects", isinstance(verify_ac_fold_certificate(replace(cert, high_root_interval=(Fraction(3), Fraction(4)))), Refusal))
    check("discriminant mutation rejects", isinstance(verify_ac_fold_certificate(replace(cert, discriminant=13)), Refusal))
    check("dependency mutation rejects", isinstance(verify_ac_fold_certificate(replace(cert, dependency_ledger=(("existing_arm_oracle", "cce8"),))), Refusal))

native_composite = compose_ac_fold_routes(one_loop, ac_fold_route(one_loop.target, 1))
skeleton_composite = compose_skeleton_morphisms(reduce_ac_fold_morphism(one_loop), reduce_ac_fold_morphism(ac_fold_route(one_loop.target, 1)))
check("reduction preserves composition parity", reduce_ac_fold_morphism(native_composite).monodromy_parity == skeleton_composite.monodromy_parity)
check("reduction is full onto C2 parity", {reduce_ac_fold_morphism(ac_fold_route(high, n)).monodromy_parity for n in (0, 1)} == {0, 1})
check("reduction kernel is nontrivial 2Z", reduce_ac_fold_morphism(two_loops).monodromy_parity == 0 and two_loops.winding != 0)

# P=1,Q=0,X=1,E=sqrt(2) is not rational, so use P=0,Q=1/4,X=1,E=1:
# Delta=1-1=0 exactly.
wall = ACFoldParameters(Fraction(0), Fraction(1, 4), Fraction(1), Fraction(1))
wall_result = continue_ac_fold_certified(ac_fold_route(ACFoldObject.build(wall, "high"), 0))
check("fold wall is typed", isinstance(wall_result, Refusal) and wall_result.code == "OutsideStrictChamber")

negative = ACFoldParameters(Fraction(1), Fraction(0), Fraction(1), Fraction(1))
negative_result = continue_ac_fold_certified(ac_fold_route(ACFoldObject.build(negative, "high"), 0))
check("negative discriminant is typed", isinstance(negative_result, Refusal) and negative_result.code == "OutsideStrictChamber")

source = Path(__file__).resolve().parents[1].joinpath("src/cella/continuation/r3_ac_fold.py").read_text()
check("R3 does not import existing continuation arms", all(token not in source for token in ("from .cce5", "from .cce7", "from .cce8", "native_periods", "horizon")))
check("R3 verifier uses no external CAS", all(token not in source for token in ("import sympy", "import sage", "subprocess")))

print(f"R3 exact AC-fold realization gate: {passed} assertions passed")
