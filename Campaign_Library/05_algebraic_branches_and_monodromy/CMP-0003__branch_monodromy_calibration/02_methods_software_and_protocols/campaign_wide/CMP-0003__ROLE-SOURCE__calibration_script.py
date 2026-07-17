#!/usr/bin/env python3
from __future__ import annotations

import argparse
import cmath
import datetime as dt
import io
import json
import math
import os
import sys
from fractions import Fraction
from itertools import permutations
from pathlib import Path
from typing import Iterable

import numpy as np


RAW_OUTPUT_DIR = "/run/media/wlloyd/Games 2/Lloyd_Workbench/engine/Raw console output"

TEST_NAME = "branch_monodromy_calibration_v2"
DEFAULT_N_STEPS = 4000
ROOT_RESIDUAL_MAX = 1e-9
STEP_MOTION_RATIO_MAX = 0.10
MIN_ANGULAR_STEP = 2.0 * math.pi * 2.0**-44

CERTIFIED = "CERTIFIED_PERMUTATION"
UNCERTIFIED_STEP = "UNCERTIFIED_STEP_MATCH"
UNCERTIFIED_CLOSURE = "UNCERTIFIED_CLOSURE_MATCH"
NON_BIJECTIVE = "NON_BIJECTIVE_CLOSURE"
TRACK_PROX_DISAGREE = "CONTINUATION_PROXIMITY_DISAGREEMENT"
LOOP_HITS_DISCRIMINANT = "LOOP_HITS_DISCRIMINANT"
ROOT_FIDELITY_FAILURE = "ROOT_FIDELITY_FAILURE"
ORACLE_MISMATCH = "DISCRIMINANT_ORACLE_MISMATCH"

STATUS_VALUES = [
    CERTIFIED,
    UNCERTIFIED_STEP,
    UNCERTIFIED_CLOSURE,
    NON_BIJECTIVE,
    TRACK_PROX_DISAGREE,
    LOOP_HITS_DISCRIMINANT,
    ROOT_FIDELITY_FAILURE,
    ORACLE_MISMATCH,
]

IDENTITY_1 = [0]
IDENTITY_2 = [0, 1]
SWAP_2 = [1, 0]


class TeeStream:
    def __init__(self, original):
        self.original = original
        self._buffer = io.StringIO()

    def write(self, text: str) -> int:
        self._buffer.write(text)
        return self.original.write(text)

    def flush(self) -> None:
        self.original.flush()

    def getvalue(self) -> str:
        return self._buffer.getvalue()


def _fraction(value: int | float | str | Fraction) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(str(value))


def _complex_pair_key(value: complex) -> tuple[float, float]:
    return (float(value.real), float(value.imag))


def _sort_roots(roots: Iterable[complex]) -> list[complex]:
    return sorted((complex(root) for root in roots), key=_complex_pair_key)


def _format_perm(perm: list[int]) -> str:
    return "[" + ",".join(str(item) for item in perm) + "]"


def _is_identity(perm: list[int]) -> bool:
    return perm == list(range(len(perm)))


def _monodromy_word(perm: list[int]) -> str:
    return "identity" if _is_identity(perm) else _format_perm(perm)


def _compose_perm(first: list[int], second: list[int]) -> list[int]:
    return [first[second[index]] for index in range(len(first))]


def _initial_status_counts() -> dict[str, int]:
    return {status: 0 for status in STATUS_VALUES}


def polynomial_roots(coefficients: list[complex]) -> list[complex]:
    roots = np.roots(np.asarray(coefficients, dtype=np.complex128))
    return _sort_roots(roots)


def normalized_residual(coefficients: list[complex], root: complex) -> float:
    degree = len(coefficients) - 1
    value = 0.0j
    for coefficient in coefficients:
        value = value * root + coefficient

    scale = max(1.0, abs(root))
    denominator = 0.0
    for index, coefficient in enumerate(coefficients):
        power = degree - index
        denominator += abs(coefficient) * scale**power

    if denominator == 0.0:
        return math.inf
    return float(abs(value) / denominator)


def min_pairwise_separation(roots: list[complex]) -> float:
    if len(roots) <= 1:
        return math.inf
    return float(
        min(abs(roots[i] - roots[j]) for i in range(len(roots)) for j in range(i + 1, len(roots)))
    )


def greedy_nearest_assignment(
    previous_roots: list[complex], current_roots: list[complex]
) -> list[int]:
    available = set(range(len(current_roots)))
    assignment: list[int] = []
    for previous in previous_roots:
        best = min(
            available,
            key=lambda index: (abs(current_roots[index] - previous), index),
        )
        assignment.append(best)
        available.remove(best)
    return assignment


def keystone_coefficients(x2: complex, fixed_x3: complex = 2.0, mu: complex = 1.0) -> list[complex]:
    constant = fixed_x3 * fixed_x3 - 3.0
    return [mu, mu * x2, mu * constant]


def keystone_oracle(center: int | float | str | Fraction, radius: int | float | str | Fraction) -> dict:
    center_q = _fraction(center)
    radius_q = _fraction(radius)
    branch_points = [Fraction(-2), Fraction(2)]
    winding_count = 0

    for branch_point in branch_points:
        distance = abs(center_q - branch_point)
        if distance == radius_q:
            return {
                "status": LOOP_HITS_DISCRIMINANT,
                "w_delta": None,
                "oracle_monodromy": None,
                "branch_points": [-2, 2],
            }
        if distance < radius_q:
            winding_count += 1

    return {
        "status": "OK",
        "w_delta": winding_count,
        "oracle_monodromy": SWAP_2 if winding_count % 2 else IDENTITY_2,
        "branch_points": [-2, 2],
    }


def certify_closure(
    final_roots: list[complex], initial_roots: list[complex], pi_track: list[int]
) -> dict:
    n_roots = len(initial_roots)
    if n_roots == 1:
        return {
            "status": CERTIFIED,
            "initial_min_sep": 0.0,
            "best_cost": 0.0,
            "second_best_cost": None,
            "best_assignment_pi_prox": IDENTITY_1.copy(),
            "track_prox_agree": list(pi_track) == IDENTITY_1,
            "bijective": True,
            "passed": list(pi_track) == IDENTITY_1,
        }

    initial_min_sep = min_pairwise_separation(initial_roots)

    def assignment_cost(perm: tuple[int, ...]) -> float:
        return float(
            max(abs(final_roots[index] - initial_roots[perm[index]]) for index in range(n_roots))
        )

    scored = sorted(
        ([assignment_cost(perm), list(perm)] for perm in permutations(range(n_roots))),
        key=lambda item: (item[0], item[1]),
    )
    best_cost, pi_prox = scored[0]
    second_best_cost = scored[1][0]

    bijective = len(set(pi_prox)) == n_roots
    unique_sep = (best_cost <= 0.05 * initial_min_sep) and (
        (second_best_cost - best_cost) >= 0.25 * initial_min_sep
    )
    agree = list(pi_track) == pi_prox

    if not bijective:
        status = NON_BIJECTIVE
        passed = False
    elif not unique_sep:
        status = UNCERTIFIED_CLOSURE
        passed = False
    elif not agree:
        status = TRACK_PROX_DISAGREE
        passed = False
    else:
        status = CERTIFIED
        passed = True

    return {
        "status": status,
        "initial_min_sep": float(initial_min_sep),
        "best_cost": float(best_cost),
        "second_best_cost": float(second_best_cost),
        "best_assignment_pi_prox": pi_prox,
        "track_prox_agree": agree,
        "bijective": bijective,
        "passed": passed,
    }


def structural_multiplication_loop() -> dict:
    closure = certify_closure([1.0 + 0.0j], [1.0 + 0.0j], IDENTITY_1)
    return {
        "loop_name": "multiplication_degree1",
        "surface": "multiplication",
        "solved_role": "D",
        "fixed_params": {"S": 2},
        "loop_param": "P",
        "center": 5.0,
        "radius": 1.0,
        "n_steps": 0,
        "pi_track": IDENTITY_1.copy(),
        "status": closure["status"],
        "monodromy": "identity",
        "branch_locus": "empty",
        "root_fidelity_max_residual": 0.0,
        "step_safety_max_motion_ratio": 0.0,
        "closure_certificate": closure,
        "discriminant_oracle": {"applies": False},
    }


def _failure_loop_entry(
    *,
    loop_name: str,
    center: int | float,
    radius: int | float,
    n_steps: int,
    status: str,
    pi_track: list[int],
    max_residual: float,
    max_motion_ratio: float,
    closure_certificate: dict | None,
    oracle: dict | None,
) -> dict:
    return {
        "loop_name": loop_name,
        "surface": "keystone",
        "solved_role": "x1",
        "fixed_params": {"x3": 2},
        "center": center,
        "radius": radius,
        "n_steps": n_steps,
        "pi_track": pi_track,
        "status": status,
        "root_fidelity_max_residual": float(max_residual),
        "step_safety_max_motion_ratio": float(max_motion_ratio),
        "closure_certificate": closure_certificate
        or {
            "initial_min_sep": None,
            "best_cost": None,
            "second_best_cost": None,
            "best_assignment_pi_prox": None,
            "track_prox_agree": False,
            "bijective": False,
            "passed": False,
        },
        "discriminant_oracle": oracle or {"applies": True},
    }


def track_keystone_loop(
    *,
    loop_name: str,
    center: int | float,
    radius: int | float,
    n_steps: int = DEFAULT_N_STEPS,
    fixed_x3: float = 2.0,
    mu: float = 1.0,
) -> dict:
    start_param = complex(float(center) + float(radius), 0.0)
    initial_coefficients = keystone_coefficients(start_param, fixed_x3=fixed_x3, mu=mu)
    initial_roots = polynomial_roots(initial_coefficients)
    path_roots = initial_roots.copy()
    last_assignment = list(range(len(initial_roots)))

    max_residual = max(normalized_residual(initial_coefficients, root) for root in initial_roots)
    max_motion_ratio = 0.0
    theta = 0.0
    base_step = 2.0 * math.pi / n_steps

    while theta < 2.0 * math.pi:
        step = min(base_step, 2.0 * math.pi - theta)
        accepted = False

        while not accepted:
            proposed_theta = theta + step
            if proposed_theta >= 2.0 * math.pi - 1e-15:
                proposed_theta = 2.0 * math.pi
                x2 = start_param
            else:
                x2 = complex(center) + float(radius) * cmath.exp(1.0j * proposed_theta)

            coefficients = keystone_coefficients(x2, fixed_x3=fixed_x3, mu=mu)
            current_roots = polynomial_roots(coefficients)
            current_max_residual = max(
                normalized_residual(coefficients, root) for root in current_roots
            )
            max_residual = max(max_residual, current_max_residual)

            if current_max_residual > ROOT_RESIDUAL_MAX:
                oracle = _oracle_report(center, radius, IDENTITY_2, applies=True)
                return _failure_loop_entry(
                    loop_name=loop_name,
                    center=center,
                    radius=radius,
                    n_steps=n_steps,
                    status=ROOT_FIDELITY_FAILURE,
                    pi_track=last_assignment,
                    max_residual=max_residual,
                    max_motion_ratio=max_motion_ratio,
                    closure_certificate=None,
                    oracle=oracle,
                )

            assignment = greedy_nearest_assignment(path_roots, current_roots)
            moved_roots = [current_roots[index] for index in assignment]
            max_motion = max(
                abs(moved_roots[index] - path_roots[index])
                for index in range(len(path_roots))
            )
            min_sep = min_pairwise_separation(current_roots)
            motion_ratio = float(max_motion / min_sep)

            if motion_ratio > STEP_MOTION_RATIO_MAX:
                step *= 0.5
                if step < MIN_ANGULAR_STEP:
                    oracle = _oracle_report(center, radius, IDENTITY_2, applies=True)
                    return _failure_loop_entry(
                        loop_name=loop_name,
                        center=center,
                        radius=radius,
                        n_steps=n_steps,
                        status=UNCERTIFIED_STEP,
                        pi_track=last_assignment,
                        max_residual=max_residual,
                        max_motion_ratio=max(max_motion_ratio, motion_ratio),
                        closure_certificate=None,
                        oracle=oracle,
                    )
                continue

            path_roots = moved_roots
            last_assignment = assignment
            max_motion_ratio = max(max_motion_ratio, motion_ratio)
            theta = proposed_theta
            accepted = True

    pi_track = last_assignment
    closure = certify_closure(path_roots, initial_roots, pi_track)
    status = closure["status"]
    oracle = _oracle_report(center, radius, pi_track, applies=True)

    if oracle["status"] == LOOP_HITS_DISCRIMINANT:
        status = LOOP_HITS_DISCRIMINANT
    elif status == CERTIFIED and not oracle["tracker_matches_oracle"]:
        status = ORACLE_MISMATCH

    return {
        "loop_name": loop_name,
        "surface": "keystone",
        "solved_role": "x1",
        "fixed_params": {"x3": 2},
        "center": center,
        "radius": radius,
        "n_steps": n_steps,
        "pi_track": pi_track,
        "status": status,
        "root_fidelity_max_residual": float(max_residual),
        "step_safety_max_motion_ratio": float(max_motion_ratio),
        "closure_certificate": closure,
        "discriminant_oracle": oracle,
    }


def _oracle_report(
    center: int | float,
    radius: int | float,
    tracker_monodromy: list[int],
    *,
    applies: bool,
) -> dict:
    if not applies:
        return {"applies": False}

    oracle = keystone_oracle(center, radius)
    oracle_monodromy = oracle["oracle_monodromy"]
    return {
        "applies": True,
        "status": oracle["status"],
        "branch_points": oracle["branch_points"],
        "w_delta": oracle["w_delta"],
        "oracle_monodromy": oracle_monodromy,
        "tracker_matches_oracle": oracle_monodromy == tracker_monodromy,
    }


def _control(name: str, passed: bool, detail: dict) -> dict:
    return {"name": name, "passed": bool(passed), "detail": detail}


def build_controls(loops: list[dict]) -> list[dict]:
    by_name = {entry["loop_name"]: entry for entry in loops}
    plus_radii = [
        by_name["keystone_plus_r0_5"]["pi_track"],
        by_name["keystone_plus_r1_0"]["pi_track"],
        by_name["keystone_plus_r1_5"]["pi_track"],
    ]
    plus = by_name["keystone_plus_r1_0"]["pi_track"]
    minus = by_name["keystone_minus_r1_0"]["pi_track"]
    composed = _compose_perm(plus, minus)

    keystone_loops = [entry for entry in loops if entry["surface"] == "keystone"]
    non_structural = [entry for entry in loops if entry["surface"] != "multiplication"]

    return [
        _control(
            "radius_independence",
            plus_radii[0] == plus_radii[1] == plus_radii[2],
            {"plus_radius_permutations": plus_radii},
        ),
        _control(
            "contractible_loop_identity",
            by_name["keystone_contractible_10_r1_0"]["pi_track"] == IDENTITY_2,
            {"permutation": by_name["keystone_contractible_10_r1_0"]["pi_track"]},
        ),
        _control(
            "composition_closure",
            composed == IDENTITY_2,
            {"m_plus": plus, "m_minus": minus, "composition": composed},
        ),
        _control(
            "gauge_invariance",
            by_name["keystone_gauge_2_5_plus_r1_0"]["pi_track"] == plus,
            {
                "ungauged": plus,
                "gauged_mu_2_5": by_name["keystone_gauge_2_5_plus_r1_0"]["pi_track"],
            },
        ),
        _control(
            "certified_closure",
            all(
                entry["status"] == CERTIFIED and entry["closure_certificate"]["passed"]
                for entry in non_structural
            ),
            {
                "non_structural_statuses": [
                    [entry["loop_name"], entry["status"]] for entry in non_structural
                ]
            },
        ),
        _control(
            "discriminant_oracle_agreement",
            all(entry["discriminant_oracle"]["tracker_matches_oracle"] for entry in keystone_loops),
            {
                "keystone_oracle_matches": [
                    [
                        entry["loop_name"],
                        entry["discriminant_oracle"]["tracker_matches_oracle"],
                    ]
                    for entry in keystone_loops
                ]
            },
        ),
        _control(
            "strained_contractible_loop_identity",
            by_name["keystone_strained_4_r1_0"]["pi_track"] == IDENTITY_2,
            {"permutation": by_name["keystone_strained_4_r1_0"]["pi_track"]},
        ),
    ]


def run_calibration(timestamp: str | None = None) -> dict:
    loops = [
        structural_multiplication_loop(),
        track_keystone_loop(loop_name="keystone_plus_r0_5", center=2, radius=0.5),
        track_keystone_loop(loop_name="keystone_plus_r1_0", center=2, radius=1.0),
        track_keystone_loop(loop_name="keystone_plus_r1_5", center=2, radius=1.5),
        track_keystone_loop(loop_name="keystone_minus_r1_0", center=-2, radius=1.0),
        track_keystone_loop(loop_name="keystone_contractible_10_r1_0", center=10, radius=1.0),
        track_keystone_loop(loop_name="keystone_strained_4_r1_0", center=4, radius=1.0),
        track_keystone_loop(
            loop_name="keystone_gauge_2_5_plus_r1_0",
            center=2,
            radius=1.0,
            mu=2.5,
        ),
    ]

    status_counts = _initial_status_counts()
    for entry in loops:
        status_counts[entry["status"]] += 1

    controls = build_controls(loops)
    failure_statuses = [status for status in STATUS_VALUES if status != CERTIFIED]
    overall_pass = (
        status_counts[CERTIFIED] == len(loops)
        and all(status_counts[status] == 0 for status in failure_statuses)
        and all(control["passed"] for control in controls)
    )

    return {
        "timestamp": timestamp or dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "test_name": TEST_NAME,
        "overall_status": "PASS" if overall_pass else "FAIL",
        "status_counts": status_counts,
        "loops": loops,
        "controls": controls,
    }


def print_reference_confirmation(report: dict) -> None:
    loops = {entry["loop_name"]: entry for entry in report["loops"]}
    controls = {entry["name"]: entry for entry in report["controls"]}

    mult = loops["multiplication_degree1"]
    print("[1] Multiplication  P=D*S, solve for D")
    print(
        "    loop param P around 5.0: monodromy = "
        f"{mult['monodromy']}                       (predicted: identity)   "
        f"{_pass_fail(mult['pi_track'] == IDENTITY_1 and mult['status'] == CERTIFIED)}"
    )
    print(
        "    degree 1 in solved var -> empty discriminant, oracle n/a                                     "
        f"{_pass_fail(mult['branch_locus'] == 'empty' and not mult['discriminant_oracle']['applies'])}"
    )
    print("")
    print("[2] Keystone  F=x1^2+x1*x2+x3^2-3, solve for x1, fix x3=2")

    for loop_name, label in [
        ("keystone_plus_r0_5", "    loop x2 around +2, radius=0.5:"),
        ("keystone_plus_r1_0", "    loop x2 around +2, radius=1.0:"),
        ("keystone_plus_r1_5", "    loop x2 around +2, radius=1.5:"),
        ("keystone_minus_r1_0", "    loop x2 around -2, radius=1.0:"),
    ]:
        entry = loops[loop_name]
        prox = entry["closure_certificate"]["best_assignment_pi_prox"]
        oracle = entry["discriminant_oracle"]["oracle_monodromy"]
        print(
            f"{label} track={_format_perm(entry['pi_track'])}  "
            f"prox={_format_perm(prox)}  oracle={_format_perm(oracle)}                         "
            f"{_pass_fail(entry['status'] == CERTIFIED)}"
        )

    contractible = loops["keystone_contractible_10_r1_0"]
    strained = loops["keystone_strained_4_r1_0"]
    print(
        "    contractible loop x2 around 10, radius=1.0: track="
        f"{_monodromy_word(contractible['pi_track'])} prox="
        f"{_monodromy_word(contractible['closure_certificate']['best_assignment_pi_prox'])} "
        f"oracle={_monodromy_word(contractible['discriminant_oracle']['oracle_monodromy'])}     "
        f"{_pass_fail(contractible['status'] == CERTIFIED and contractible['pi_track'] == IDENTITY_2)}"
    )
    print(
        "    strained loop x2 around 4, radius=1.0:      track="
        f"{_monodromy_word(strained['pi_track'])} prox="
        f"{_monodromy_word(strained['closure_certificate']['best_assignment_pi_prox'])} "
        f"oracle={_monodromy_word(strained['discriminant_oracle']['oracle_monodromy'])}     "
        f"{_pass_fail(strained['status'] == CERTIFIED and strained['pi_track'] == IDENTITY_2)}"
    )
    print(
        "    closure  m(+2) ∘ m(-2) = "
        f"{_monodromy_word(controls['composition_closure']['detail']['composition'])}"
        "                                   (predicted: identity)   "
        f"{_pass_fail(controls['composition_closure']['passed'])}"
    )
    gauged = loops["keystone_gauge_2_5_plus_r1_0"]
    print(
        "    gauge  F -> 2.5*F, loop +2 radius 1: monodromy = "
        f"{_format_perm(gauged['pi_track'])}              (must equal ungauged)    "
        f"{_pass_fail(controls['gauge_invariance']['passed'])}"
    )
    print(
        "    every keystone tracker permutation equals oracle permutation                                 "
        f"{_pass_fail(controls['discriminant_oracle_agreement']['passed'])}"
    )
    print(
        "    every keystone loop: pi_track == pi_prox                                                     "
        f"{_pass_fail(_all_track_prox_agree(report))}"
    )
    print(
        "    every reported monodromy has status CERTIFIED_PERMUTATION                                    "
        f"{_pass_fail(all(entry['status'] == CERTIFIED for entry in report['loops']))}"
    )


def _all_track_prox_agree(report: dict) -> bool:
    return all(
        entry["closure_certificate"]["track_prox_agree"]
        for entry in report["loops"]
        if entry["surface"] == "keystone"
    )


def _pass_fail(passed: bool) -> str:
    return "PASS" if passed else "FAIL"


def write_report(report: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")


def default_report_path() -> Path:
    return Path(__file__).resolve().parent / "calibration_report.json"


def raw_report_path() -> Path:
    return Path(RAW_OUTPUT_DIR) / "branch_monodromy_calibration_report.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=default_report_path(),
        help="report path; defaults to the deliverable calibration_report.json",
    )
    parser.add_argument(
        "--skip-raw-copy",
        action="store_true",
        help="do not mirror the report into RAW_OUTPUT_DIR",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    tee = TeeStream(sys.stdout)
    sys.stdout = tee
    try:
        report = run_calibration()
        print_reference_confirmation(report)
        report["console_log"] = tee.getvalue()
    finally:
        sys.stdout = tee.original

    write_report(report, args.output)
    if not args.skip_raw_copy:
        os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
        write_report(report, raw_report_path())

    print(f"[report: {args.output}]")
    if not args.skip_raw_copy:
        print(f"[raw-copy: {raw_report_path()}]")
    return 0 if report["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
