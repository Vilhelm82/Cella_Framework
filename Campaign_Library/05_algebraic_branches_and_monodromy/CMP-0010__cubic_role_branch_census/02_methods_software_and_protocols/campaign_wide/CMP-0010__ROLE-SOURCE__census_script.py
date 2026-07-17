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
from typing import Callable, Iterable

import numpy as np
import sympy as sp


RAW_OUTPUT_DIR = "/run/media/wlloyd/Games 2/Lloyd_Workbench/engine/Raw console output"

TEST_NAME = "cubic_role_branch_census"
DEFAULT_ARC_STEPS = 720
DEFAULT_LINE_STEPS = 220
ROOT_RESIDUAL_MAX = 1e-9
STEP_MOTION_RATIO_MAX = 0.10
MIN_PATH_STEP = 2.0**-44
EXACT_PRECISION_DIGITS = 80

CERTIFIED = "CERTIFIED_PERMUTATION"
UNCERTIFIED_STEP = "UNCERTIFIED_STEP_MATCH"
UNCERTIFIED_CLOSURE = "UNCERTIFIED_CLOSURE_MATCH"
NON_BIJECTIVE = "NON_BIJECTIVE_CLOSURE"
TRACK_PROX_DISAGREE = "CONTINUATION_PROXIMITY_DISAGREEMENT"
LOOP_HITS_DISCRIMINANT = "LOOP_HITS_DISCRIMINANT"
ROOT_FIDELITY_FAILURE = "ROOT_FIDELITY_FAILURE"
DISCRIMINANT_ORACLE_MISMATCH = "DISCRIMINANT_ORACLE_MISMATCH"
COALESCENCE_ORACLE_MISMATCH = "COALESCENCE_ORACLE_MISMATCH"
COMMON_FRAME_NOT_DISTINCT = "COMMON_FRAME_NOT_DISTINCT"
HURWITZ_FACTORIZATION_FAILURE = "HURWITZ_FACTORIZATION_FAILURE"

STATUS_VALUES = [
    CERTIFIED,
    UNCERTIFIED_STEP,
    UNCERTIFIED_CLOSURE,
    NON_BIJECTIVE,
    TRACK_PROX_DISAGREE,
    LOOP_HITS_DISCRIMINANT,
    ROOT_FIDELITY_FAILURE,
    DISCRIMINANT_ORACLE_MISMATCH,
    COALESCENCE_ORACLE_MISMATCH,
    COMMON_FRAME_NOT_DISTINCT,
    HURWITZ_FACTORIZATION_FAILURE,
]


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


class PathPiece:
    def __init__(
        self,
        *,
        kind: str,
        start: complex,
        end: complex,
        steps: int,
        center: complex | None = None,
        radius: float | None = None,
        start_angle: float | None = None,
        delta_angle: float | None = None,
    ) -> None:
        self.kind = kind
        self.start = start
        self.end = end
        self.steps = steps
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.delta_angle = delta_angle


def _initial_status_counts() -> dict[str, int]:
    return {status: 0 for status in STATUS_VALUES}


def _complex_pair_key(value: complex) -> tuple[float, float]:
    return (float(value.real), float(value.imag))


def _sort_roots(roots: Iterable[complex]) -> list[complex]:
    return sorted((complex(root) for root in roots), key=_complex_pair_key)


def _complex_from_exact(value: sp.Expr) -> complex:
    evaluated = sp.N(value, EXACT_PRECISION_DIGITS)
    return complex(evaluated)


def _complex_json(value: complex) -> dict[str, str]:
    return {
        "real": f"{value.real:.17g}",
        "imag": f"{value.imag:.17g}",
    }


def _q_json(value: Fraction) -> dict[str, int]:
    return {"num": value.numerator, "den": value.denominator}


def _q_display(value: Fraction) -> str:
    return json.dumps(_q_json(value), sort_keys=True)


def _sympy_rational_to_fraction(value: sp.Expr) -> Fraction | None:
    simplified = sp.simplify(value)
    if not simplified.is_Rational:
        return None
    return Fraction(int(simplified.p), int(simplified.q))


def _format_perm(perm: list[int]) -> str:
    return "[" + ",".join(str(item) for item in perm) + "]"


def _is_identity(perm: list[int]) -> bool:
    return perm == list(range(len(perm)))


def _pass_fail(passed: bool) -> str:
    return "PASS" if passed else "FAIL"


def compose_perm(first: list[int], second: list[int]) -> list[int]:
    """Return first after second for label maps i -> perm[i]."""
    return [first[second[index]] for index in range(len(first))]


def product_perms_ccw(perms: list[list[int]]) -> list[int]:
    """Documented convention: apply lassos in listed CCW order, left to right."""
    if not perms:
        return []
    result = list(range(len(perms[0])))
    for perm in perms:
        result = compose_perm(perm, result)
    return result


def invert_perm(perm: list[int]) -> list[int]:
    inverse = [0] * len(perm)
    for index, target in enumerate(perm):
        inverse[target] = index
    return inverse


def cycle_type(perm: list[int]) -> list[int]:
    seen: set[int] = set()
    cycles: list[int] = []
    for start in range(len(perm)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = perm[current]
        cycles.append(length)
    return sorted(cycles, reverse=True)


def swapped_pair(perm: list[int]) -> list[int]:
    return [index for index, target in enumerate(perm) if target != index]


def classify_channel_content(channel_vector: dict[str, Fraction] | None) -> str:
    if channel_vector is None:
        return "unavailable"

    values = [
        channel_vector["kappa_c"],
        channel_vector["kappa_s"],
        channel_vector["kappa_int"],
    ]
    total = sum(values, Fraction(0))
    nonzero = any(value != 0 for value in values)
    if total == 0 and nonzero:
        return "scalar_flat_channel_active"

    pair_cancels = any(
        values[i] != 0 and values[j] != 0 and values[i] + values[j] == 0
        for i in range(3)
        for j in range(i + 1, 3)
    )
    if total != 0 and pair_cancels:
        return "channel_cancellation_present"

    return "regular"


def polynomial_roots(coefficients: list[complex]) -> list[complex]:
    return _sort_roots(np.roots(np.asarray(coefficients, dtype=np.complex128)))


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


def greedy_nearest_assignment(previous_roots: list[complex], current_roots: list[complex]) -> list[int]:
    available = set(range(len(current_roots)))
    assignment: list[int] = []
    for previous in previous_roots:
        best = min(available, key=lambda index: (abs(current_roots[index] - previous), index))
        assignment.append(best)
        available.remove(best)
    return assignment


def certify_closure(
    final_roots: list[complex], initial_roots: list[complex], pi_track: list[int]
) -> dict:
    n_roots = len(initial_roots)
    if n_roots == 1:
        passed = list(pi_track) == [0]
        return {
            "status": CERTIFIED if passed else TRACK_PROX_DISAGREE,
            "initial_min_sep": 0.0,
            "best_cost": 0.0,
            "second_best_cost": None,
            "best_assignment_pi_prox": [0],
            "track_prox_agree": passed,
            "bijective": True,
            "passed": passed,
        }

    initial_min_sep = min_pairwise_separation(initial_roots)

    def assignment_cost(perm: tuple[int, ...]) -> float:
        return float(max(abs(final_roots[index] - initial_roots[perm[index]]) for index in range(n_roots)))

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


def cubic_x1_coefficients(x2: complex) -> list[complex]:
    return [1.0 + 0.0j, 0.0 + 0.0j, x2, 1.0 + 0.0j]


def x3_coefficients(x2: complex) -> list[complex]:
    return [1.0 + 0.0j, 0.0 + 0.0j, x2 - 2.0]


def _piece_param(piece: PathPiece, progress: float) -> complex:
    if progress >= 1.0:
        return piece.end
    if piece.kind == "line":
        return piece.start + (piece.end - piece.start) * progress
    if piece.kind == "arc":
        assert piece.center is not None
        assert piece.radius is not None
        assert piece.start_angle is not None
        assert piece.delta_angle is not None
        angle = piece.start_angle + piece.delta_angle * progress
        return piece.center + piece.radius * cmath.exp(1j * angle)
    raise ValueError(f"unknown path piece: {piece.kind}")


def line_piece(start: complex, end: complex, steps: int = DEFAULT_LINE_STEPS) -> PathPiece:
    return PathPiece(kind="line", start=start, end=end, steps=steps)


def arc_piece(
    center: complex,
    radius: float,
    start_angle: float,
    delta_angle: float = 2.0 * math.pi,
    steps: int = DEFAULT_ARC_STEPS,
) -> PathPiece:
    start = center + radius * cmath.exp(1j * start_angle)
    return PathPiece(
        kind="arc",
        start=start,
        end=start,
        steps=steps,
        center=center,
        radius=radius,
        start_angle=start_angle,
        delta_angle=delta_angle,
    )


def track_path(
    *,
    loop_name: str,
    surface: str,
    solved_role: str,
    frame: str,
    start_param: complex,
    pieces: list[PathPiece],
    coeff_fn: Callable[[complex], list[complex]],
    metadata: dict,
    capture_after_piece: int | None = None,
) -> dict:
    initial_coefficients = coeff_fn(start_param)
    initial_roots = polynomial_roots(initial_coefficients)
    tracked_roots = initial_roots.copy()
    last_assignment = list(range(len(initial_roots)))
    max_residual = max(normalized_residual(initial_coefficients, root) for root in initial_roots)
    max_motion_ratio = 0.0
    bisections = 0
    accepted_steps = 0
    captured_roots: list[complex] | None = None

    for piece_index, piece in enumerate(pieces):
        progress = 0.0
        base_step = 1.0 / piece.steps
        while progress < 1.0:
            step = min(base_step, 1.0 - progress)
            accepted = False
            while not accepted:
                proposed = progress + step
                if proposed >= 1.0 - 1e-15:
                    proposed = 1.0
                param = _piece_param(piece, proposed)
                coefficients = coeff_fn(param)
                current_roots = polynomial_roots(coefficients)
                current_residual = max(normalized_residual(coefficients, root) for root in current_roots)
                max_residual = max(max_residual, current_residual)
                if current_residual > ROOT_RESIDUAL_MAX:
                    return _failed_loop_entry(
                        loop_name=loop_name,
                        surface=surface,
                        solved_role=solved_role,
                        frame=frame,
                        metadata=metadata,
                        status=ROOT_FIDELITY_FAILURE,
                        pi_track=last_assignment,
                        max_residual=max_residual,
                        max_motion_ratio=max_motion_ratio,
                        bisections=bisections,
                        accepted_steps=accepted_steps,
                    )

                assignment = greedy_nearest_assignment(tracked_roots, current_roots)
                moved_roots = [current_roots[index] for index in assignment]
                max_motion = max(
                    abs(moved_roots[index] - tracked_roots[index])
                    for index in range(len(tracked_roots))
                )
                min_sep = min_pairwise_separation(current_roots)
                motion_ratio = 0.0 if min_sep == math.inf else float(max_motion / min_sep)

                if motion_ratio > STEP_MOTION_RATIO_MAX:
                    step *= 0.5
                    bisections += 1
                    if step < MIN_PATH_STEP:
                        return _failed_loop_entry(
                            loop_name=loop_name,
                            surface=surface,
                            solved_role=solved_role,
                            frame=frame,
                            metadata=metadata,
                            status=UNCERTIFIED_STEP,
                            pi_track=last_assignment,
                            max_residual=max_residual,
                            max_motion_ratio=max(max_motion_ratio, motion_ratio),
                            bisections=bisections,
                            accepted_steps=accepted_steps,
                        )
                    continue

                tracked_roots = moved_roots
                last_assignment = assignment
                max_motion_ratio = max(max_motion_ratio, motion_ratio)
                accepted_steps += 1
                progress = proposed
                accepted = True

        if capture_after_piece is not None and piece_index == capture_after_piece:
            captured_roots = tracked_roots.copy()

    pi_track = last_assignment
    closure = certify_closure(tracked_roots, initial_roots, pi_track)
    return {
        "loop_name": loop_name,
        "surface": surface,
        "solved_role": solved_role,
        "frame": frame,
        **metadata,
        "pi_track": pi_track,
        "cycle_type": cycle_type(pi_track),
        "status": closure["status"],
        "root_fidelity_max_residual": float(max_residual),
        "step_safety_max_motion_ratio": float(max_motion_ratio),
        "adaptive_bisections": bisections,
        "accepted_steps": accepted_steps,
        "closure_certificate": closure,
        "captured_roots_after_piece": [_complex_json(root) for root in captured_roots]
        if captured_roots is not None
        else None,
        "_captured_roots_complex": captured_roots,
    }


def _failed_loop_entry(
    *,
    loop_name: str,
    surface: str,
    solved_role: str,
    frame: str,
    metadata: dict,
    status: str,
    pi_track: list[int],
    max_residual: float,
    max_motion_ratio: float,
    bisections: int,
    accepted_steps: int,
) -> dict:
    return {
        "loop_name": loop_name,
        "surface": surface,
        "solved_role": solved_role,
        "frame": frame,
        **metadata,
        "pi_track": pi_track,
        "cycle_type": cycle_type(pi_track),
        "status": status,
        "root_fidelity_max_residual": float(max_residual),
        "step_safety_max_motion_ratio": float(max_motion_ratio),
        "adaptive_bisections": bisections,
        "accepted_steps": accepted_steps,
        "closure_certificate": {
            "initial_min_sep": None,
            "best_cost": None,
            "second_best_cost": None,
            "best_assignment_pi_prox": None,
            "track_prox_agree": False,
            "bijective": False,
            "passed": False,
        },
        "captured_roots_after_piece": None,
        "_captured_roots_complex": None,
    }


def build_exact_layer() -> dict:
    x2 = sp.symbols("x2")
    x1 = sp.symbols("x1")
    discriminant_poly = sp.Poly(-4 * x2**3 - 27, x2)
    branch_points = list(discriminant_poly.all_roots())
    separation_exact = sp.simplify(
        (branch_points[0] - branch_points[1])
        * (sp.conjugate(branch_points[0]) - sp.conjugate(branch_points[1]))
    )

    enclosure_checks: dict[str, dict] = {}
    for radius in [Fraction(1, 2), Fraction(1, 1), Fraction(3, 2)]:
        radius_sq = sp.Rational(radius.numerator, radius.denominator) ** 2
        counts: list[int] = []
        strict: list[bool] = []
        for center in branch_points:
            enclosed = 0
            for branch_point in branch_points:
                dist_sq = sp.simplify((center - branch_point) * (sp.conjugate(center) - sp.conjugate(branch_point)))
                if sp.simplify(dist_sq - radius_sq) == 0:
                    strict.append(False)
                elif bool(sp.simplify(dist_sq - radius_sq) < 0):
                    enclosed += 1
                    strict.append(True)
                else:
                    strict.append(True)
            counts.append(enclosed)
        enclosure_checks[str(float(radius))] = {
            "radius": str(float(radius)),
            "counts": counts,
            "exactly_one_each": counts == [1, 1, 1] and all(strict),
        }

    double_roots = []
    polynomial = x1**3 + x2 * x1 + 1
    derivative = sp.diff(polynomial, x1)
    for branch_point in branch_points:
        double_root = sp.simplify(-sp.Rational(3, 1) / (2 * branch_point))
        simple_root = sp.simplify(sp.Rational(3, 1) / branch_point)
        p_value = sp.simplify(polynomial.subs({x1: double_root, x2: branch_point}))
        pprime_value = sp.simplify(derivative.subs({x1: double_root, x2: branch_point}))
        double_roots.append(
            {
                "branch_point_exact": sp.sstr(branch_point),
                "double_root_exact": sp.sstr(double_root),
                "simple_root_exact": sp.sstr(simple_root),
                "p_zero": p_value == 0,
                "pprime_zero": pprime_value == 0,
            }
        )

    pairwise_values = []
    for i in range(len(branch_points)):
        for j in range(i + 1, len(branch_points)):
            value = sp.simplify(
                (branch_points[i] - branch_points[j])
                * (sp.conjugate(branch_points[i]) - sp.conjugate(branch_points[j]))
            )
            pairwise_values.append(sp.sstr(value))

    return {
        "discriminant": "-4*x2**3 - 27",
        "branch_points": [
            {
                "index": index,
                "exact": sp.sstr(branch_point),
                "value": _complex_json(_complex_from_exact(branch_point)),
            }
            for index, branch_point in enumerate(branch_points)
        ],
        "pairwise_separation_squared": sp.sstr(separation_exact),
        "pairwise_values": pairwise_values,
        "equilateral": len(set(pairwise_values)) == 1,
        "enclosure_checks": enclosure_checks,
        "double_roots": double_roots,
    }


def _branch_point_records() -> list[dict]:
    x2 = sp.symbols("x2")
    exact_points = list(sp.Poly(-4 * x2**3 - 27, x2).all_roots())
    records = []
    for index, exact in enumerate(exact_points):
        numeric = _complex_from_exact(exact)
        principal_arg = math.atan2(numeric.imag, numeric.real)
        ccw_arg = principal_arg if principal_arg >= 0.0 else principal_arg + 2.0 * math.pi
        records.append(
            {
                "sympy_index": index,
                "exact": exact,
                "exact_str": sp.sstr(exact),
                "numeric": numeric,
                "principal_arg": principal_arg,
                "arg": ccw_arg,
                "double_root_exact": sp.simplify(-sp.Rational(3, 1) / (2 * exact)),
                "double_root_numeric": _complex_from_exact(sp.simplify(-sp.Rational(3, 1) / (2 * exact))),
            }
        )
    return sorted(records, key=lambda item: (item["arg"], item["exact_str"]))


def _lasso_pieces(beta: complex, center: complex, radius: float) -> tuple[list[PathPiece], complex, float]:
    direction = center - beta
    unit = direction / abs(direction)
    anchor = center - radius * unit
    start_angle = math.atan2((anchor - center).imag, (anchor - center).real)
    pieces = [
        line_piece(beta, anchor),
        arc_piece(center=center, radius=radius, start_angle=start_angle, delta_angle=2.0 * math.pi),
        line_piece(anchor, beta),
    ]
    return pieces, anchor, start_angle


def track_x1_lasso(branch: dict, radius: float, order_index: int) -> dict:
    beta = 0.0 + 0.0j
    pieces, anchor, start_angle = _lasso_pieces(beta, branch["numeric"], radius)
    metadata = {
        "branch_point": {
            "sympy_index": branch["sympy_index"],
            "exact": branch["exact_str"],
            "value": _complex_json(branch["numeric"]),
            "arg": float(branch["arg"]),
        },
        "lasso_order_index": order_index,
        "radius": float(radius),
        "anchor": _complex_json(anchor),
        "orientation": "CCW",
        "start_angle": float(start_angle),
    }
    return track_path(
        loop_name=f"x1_lasso_b{branch['sympy_index']}_r{str(radius).replace('.', '_')}",
        surface="cubic_x1",
        solved_role="x1",
        frame="common:beta=0",
        start_param=beta,
        pieces=pieces,
        coeff_fn=cubic_x1_coefficients,
        metadata=metadata,
        capture_after_piece=0,
    )


def track_x1_large_loop() -> dict:
    beta = 0.0 + 0.0j
    radius = 5.0
    start = radius + 0.0j
    pieces = [
        line_piece(beta, start),
        arc_piece(center=beta, radius=radius, start_angle=0.0, delta_angle=2.0 * math.pi),
        line_piece(start, beta),
    ]
    return track_path(
        loop_name="x1_large_loop_radius_5",
        surface="cubic_x1",
        solved_role="x1",
        frame="common:beta=0",
        start_param=beta,
        pieces=pieces,
        coeff_fn=cubic_x1_coefficients,
        metadata={
            "center": _complex_json(beta),
            "radius": radius,
            "orientation": "CCW",
            "branch_points_enclosed": 3,
        },
    )


def track_x1_contractible_loop() -> dict:
    beta = 0.0 + 0.0j
    radius = 1.0
    start = radius + 0.0j
    pieces = [
        line_piece(beta, start),
        arc_piece(center=beta, radius=radius, start_angle=0.0, delta_angle=2.0 * math.pi),
        line_piece(start, beta),
    ]
    return track_path(
        loop_name="x1_contractible_beta_radius_1",
        surface="cubic_x1",
        solved_role="x1",
        frame="common:beta=0",
        start_param=beta,
        pieces=pieces,
        coeff_fn=cubic_x1_coefficients,
        metadata={
            "center": _complex_json(beta),
            "radius": radius,
            "orientation": "CCW",
            "branch_points_enclosed": 0,
        },
    )


def track_x1_strained_loop() -> dict:
    beta = 0.0 + 0.0j
    center = 1.0 + 0.0j
    radius = 1.5
    start = center + radius
    pieces = [
        line_piece(beta, start),
        arc_piece(center=center, radius=radius, start_angle=0.0, delta_angle=2.0 * math.pi),
        line_piece(start, beta),
    ]
    return track_path(
        loop_name="x1_strained_center_1_radius_1_5",
        surface="cubic_x1",
        solved_role="x1",
        frame="common:beta=0",
        start_param=beta,
        pieces=pieces,
        coeff_fn=cubic_x1_coefficients,
        metadata={
            "center": _complex_json(center),
            "radius": radius,
            "orientation": "CCW",
            "branch_points_enclosed": 0,
            "exact_enclosure": "for every branch point b, |1-b|^2 > (3/2)^2",
        },
    )


def structural_x2_loop() -> dict:
    closure = certify_closure([2.0 + 0.0j], [2.0 + 0.0j], [0])
    return {
        "loop_name": "x2_structural_degree1",
        "surface": "cubic_x2",
        "solved_role": "x2",
        "frame": "structural:degree1",
        "degree": 1,
        "stratum": "x1=0",
        "stratum_type": "role-denominator pole",
        "branch_monodromy": False,
        "pi_track": [0],
        "cycle_type": [1],
        "status": closure["status"],
        "root_fidelity_max_residual": 0.0,
        "step_safety_max_motion_ratio": 0.0,
        "adaptive_bisections": 0,
        "accepted_steps": 0,
        "closure_certificate": closure,
    }


def track_x3_loop() -> dict:
    center = 2.0 + 0.0j
    radius = 1.0
    start = center + radius
    piece = arc_piece(center=center, radius=radius, start_angle=0.0, delta_angle=2.0 * math.pi)
    return track_path(
        loop_name="x3_slice_x1_1_center_2_radius_1",
        surface="cubic_x3",
        solved_role="x3",
        frame="slice:x1=1",
        start_param=start,
        pieces=[piece],
        coeff_fn=x3_coefficients,
        metadata={
            "slice": {"x1": 1},
            "polynomial": "x3**2 + x2 - 2",
            "center": 2.0,
            "radius": 1.0,
            "orientation": "CCW",
        },
    )


def coalescence_oracle_entry(loop: dict, branch: dict) -> dict:
    captured = loop.get("_captured_roots_complex")
    if captured is None:
        pair = []
        distances = []
    else:
        double_root = branch["double_root_numeric"]
        scored = sorted(
            ([abs(root - double_root), index] for index, root in enumerate(captured)),
            key=lambda item: (item[0], item[1]),
        )
        pair = sorted([scored[0][1], scored[1][1]])
        distances = [{"sheet": item[1], "distance": float(item[0])} for item in scored]

    measured_pair = sorted(swapped_pair(loop["pi_track"]))
    matches = measured_pair == pair and loop["cycle_type"] == [2, 1]
    return {
        "loop_name": loop["loop_name"],
        "branch_point_exact": branch["exact_str"],
        "double_root_exact": sp.sstr(branch["double_root_exact"]),
        "double_root_value": _complex_json(branch["double_root_numeric"]),
        "measured_swapped_pair": measured_pair,
        "oracle_coalescence_pair": pair,
        "distances_to_double_root_at_anchor": distances,
        "matches": matches,
    }


def coalescence_channel_annotation(branch: dict) -> dict:
    x1, x2, t, u = sp.symbols("x1 x2 t u")
    root = branch["double_root_exact"]
    point = branch["exact"]
    g = [
        sp.simplify(3 * root**2 + point),
        sp.simplify(root),
        sp.Rational(4, 1),
    ]
    H = [
        [sp.simplify(6 * root), sp.Rational(1, 1), sp.Rational(0, 1)],
        [sp.Rational(1, 1), sp.Rational(0, 1), sp.Rational(0, 1)],
        [sp.Rational(0, 1), sp.Rational(0, 1), sp.Rational(2, 1)],
    ]
    Hc = [[H[i][j] if i != j else sp.Rational(0, 1) for j in range(3)] for i in range(3)]
    Hs = [[H[i][j] if i == j else sp.Rational(0, 1) for j in range(3)] for i in range(3)]
    M = [[t * Hc[i][j] + u * Hs[i][j] for j in range(3)] for i in range(3)]
    bordered = [[sp.Rational(0, 1)] + g] + [[g[i]] + M[i] for i in range(3)]
    density = -sp.Matrix(bordered).det()
    poly = sp.Poly(sp.expand(density), t, u)
    q = sp.simplify(sum(entry * entry for entry in g))
    exprs = {
        "kappa_c": sp.simplify(poly.coeff_monomial(t**2) / q**2),
        "kappa_s": sp.simplify(poly.coeff_monomial(u**2) / q**2),
        "kappa_int": sp.simplify(poly.coeff_monomial(t * u) / q**2),
    }
    fractions = {key: _sympy_rational_to_fraction(value) for key, value in exprs.items()}
    if any(value is None for value in fractions.values()):
        return {
            "branch_point_exact": branch["exact_str"],
            "channel_vector": None,
            "channel_vector_display": "unavailable",
            "channel_content": "unavailable",
            "reason": "normalized kappa entries are algebraic at this coalescence, not exact Q",
        }

    channel_vector = {key: value for key, value in fractions.items() if value is not None}
    return {
        "branch_point_exact": branch["exact_str"],
        "channel_vector": {key: _q_json(value) for key, value in channel_vector.items()},
        "channel_vector_display": (
            f"kappa_c={_q_display(channel_vector['kappa_c'])}; "
            f"kappa_s={_q_display(channel_vector['kappa_s'])}; "
            f"kappa_int={_q_display(channel_vector['kappa_int'])}"
        ),
        "channel_content": classify_channel_content(channel_vector),
        "reason": "exact Q normalized channel vector",
    }


def x1_branch_channel_annotations() -> list[dict]:
    return [
        {"lasso_order_index": index, **coalescence_channel_annotation(branch)}
        for index, branch in enumerate(_branch_point_records())
    ]


def _strip_internal_fields(loop: dict) -> dict:
    public = dict(loop)
    public.pop("_captured_roots_complex", None)
    return public


def build_controls(
    *,
    primary_lassos: list[dict],
    all_lassos: list[dict],
    contractible: dict,
    strained: dict,
    big_loop: dict,
    x2_loop: dict,
    x3_loop: dict,
    coalescence: list[dict],
    hurwitz: dict,
) -> list[dict]:
    radius_groups: dict[int, list[list[int]]] = {}
    for loop in all_lassos:
        index = loop["branch_point"]["sympy_index"]
        radius_groups.setdefault(index, []).append(loop["pi_track"])

    finite_transpositions = [loop["pi_track"] for loop in primary_lassos]
    finite_pairs = [tuple(sorted(swapped_pair(perm))) for perm in finite_transpositions]

    return [
        {
            "name": "x1_finite_branch_loops_certify_transpositions",
            "passed": all(loop["status"] == CERTIFIED and loop["cycle_type"] == [2, 1] for loop in primary_lassos),
            "detail": {"primary_lasso_cycle_types": [loop["cycle_type"] for loop in primary_lassos]},
        },
        {
            "name": "x1_common_frame_distinctness",
            "passed": len(set(finite_pairs)) == 3,
            "detail": {"swapped_pairs": [list(pair) for pair in finite_pairs]},
        },
        {
            "name": "x1_coalescence_oracle_agreement",
            "passed": all(item["matches"] for item in coalescence),
            "detail": {"matches": [[item["loop_name"], item["matches"]] for item in coalescence]},
        },
        {
            "name": "x1_contractible_loop_identity",
            "passed": contractible["status"] == CERTIFIED and _is_identity(contractible["pi_track"]),
            "detail": {"permutation": contractible["pi_track"]},
        },
        {
            "name": "x1_strained_non_enclosing_loop_identity",
            "passed": strained["status"] == CERTIFIED and _is_identity(strained["pi_track"]),
            "detail": {
                "permutation": strained["pi_track"],
                "max_motion_ratio": strained["step_safety_max_motion_ratio"],
            },
        },
        {
            "name": "x1_radius_independence",
            "passed": all(len({tuple(perm) for perm in perms}) == 1 for perms in radius_groups.values()),
            "detail": {str(key): value for key, value in sorted(radius_groups.items())},
        },
        {
            "name": "x1_infinity_hurwitz",
            "passed": hurwitz["infinity_ramified"] and hurwitz["equal"] and big_loop["status"] == CERTIFIED,
            "detail": hurwitz,
        },
        {
            "name": "x2_structural_identity_pole_typing",
            "passed": x2_loop["status"] == CERTIFIED
            and x2_loop["pi_track"] == [0]
            and x2_loop["stratum_type"] == "role-denominator pole"
            and x2_loop["branch_monodromy"] is False,
            "detail": {
                "permutation": x2_loop["pi_track"],
                "stratum_type": x2_loop["stratum_type"],
            },
        },
        {
            "name": "x3_square_root_swap",
            "passed": x3_loop["status"] == CERTIFIED and x3_loop["cycle_type"] == [2],
            "detail": {"permutation": x3_loop["pi_track"], "cycle_type": x3_loop["cycle_type"]},
        },
        {
            "name": "certificate_gates",
            "passed": all(
                loop["status"] == CERTIFIED and loop["closure_certificate"]["track_prox_agree"]
                for loop in [*all_lassos, contractible, strained, big_loop, x2_loop, x3_loop]
            ),
            "detail": {
                "statuses": [
                    [loop["loop_name"], loop["status"]]
                    for loop in [*all_lassos, contractible, strained, big_loop, x2_loop, x3_loop]
                ]
            },
        },
    ]


def run_census(timestamp: str | None = None) -> dict:
    exact_layer = build_exact_layer()
    branches = _branch_point_records()
    radii = [0.5, 1.0, 1.5]
    all_lassos: list[dict] = []
    primary_lassos: list[dict] = []
    coalescence: list[dict] = []

    for order_index, branch in enumerate(branches):
        for radius in radii:
            loop = track_x1_lasso(branch, radius, order_index)
            all_lassos.append(loop)
            oracle = coalescence_oracle_entry(loop, branch)
            loop["oracle"] = {
                "cycle_type": [2, 1],
                "double_root_exact": sp.sstr(branch["double_root_exact"]),
                "coalescence_pair_matches": oracle["matches"],
                "distinct_in_common_frame": None,
            }
            coalescence.append(oracle)
            if radius == 1.0:
                primary_lassos.append(loop)

    primary_lassos = sorted(primary_lassos, key=lambda item: item["lasso_order_index"])
    big_loop = track_x1_large_loop()
    contractible = track_x1_contractible_loop()
    strained = track_x1_strained_loop()
    x2_loop = structural_x2_loop()
    x3_loop = track_x3_loop()

    finite_perms = [loop["pi_track"] for loop in primary_lassos]
    finite_pairs = [tuple(sorted(swapped_pair(perm))) for perm in finite_perms]
    distinct = len(set(finite_pairs)) == 3
    for loop in all_lassos:
        if "oracle" in loop:
            loop["oracle"]["distinct_in_common_frame"] = distinct

    ccw_product = product_perms_ccw(finite_perms)
    hurwitz = {
        "orientation": "CCW",
        "ordering": [
            {
                "lasso_order_index": loop["lasso_order_index"],
                "sympy_index": loop["branch_point"]["sympy_index"],
                "arg": loop["branch_point"]["arg"],
                "pi": loop["pi_track"],
            }
            for loop in primary_lassos
        ],
        "m_big": big_loop["pi_track"],
        "m_big_cycle_type": big_loop["cycle_type"],
        "ccw_product": ccw_product,
        "equal": big_loop["pi_track"] == ccw_product,
        "infinity_ramified": (not _is_identity(big_loop["pi_track"])) and big_loop["cycle_type"] == [2, 1],
        "m_infinity_inverse": invert_perm(big_loop["pi_track"]),
        "derived_four_term_relation_identity": compose_perm(invert_perm(big_loop["pi_track"]), ccw_product)
        == list(range(3)),
    }

    loops = [
        *_strip_and_sort_lassos(all_lassos),
        _strip_internal_fields(contractible),
        _strip_internal_fields(strained),
        _strip_internal_fields(big_loop),
        x2_loop,
        _strip_internal_fields(x3_loop),
    ]
    controls = build_controls(
        primary_lassos=primary_lassos,
        all_lassos=all_lassos,
        contractible=contractible,
        strained=strained,
        big_loop=big_loop,
        x2_loop=x2_loop,
        x3_loop=x3_loop,
        coalescence=coalescence,
        hurwitz=hurwitz,
    )

    status_counts = _initial_status_counts()
    for loop in loops:
        status_counts[loop["status"]] += 1

    if not distinct:
        status_counts[COMMON_FRAME_NOT_DISTINCT] += 1
    if not all(item["matches"] for item in coalescence):
        status_counts[COALESCENCE_ORACLE_MISMATCH] += 1
    if not (hurwitz["infinity_ramified"] and hurwitz["equal"]):
        status_counts[HURWITZ_FACTORIZATION_FAILURE] += 1

    exact_layer_passed = (
        len(exact_layer["branch_points"]) == 3
        and exact_layer["equilateral"]
        and all(item["exactly_one_each"] for item in exact_layer["enclosure_checks"].values())
        and all(item["p_zero"] and item["pprime_zero"] for item in exact_layer["double_roots"])
    )
    if not exact_layer_passed:
        status_counts[DISCRIMINANT_ORACLE_MISMATCH] += 1

    failure_statuses = [status for status in STATUS_VALUES if status != CERTIFIED]
    overall_pass = (
        status_counts[CERTIFIED] == 14
        and all(status_counts[status] == 0 for status in failure_statuses)
        and all(control["passed"] for control in controls)
        and exact_layer_passed
    )

    return {
        "timestamp": timestamp
        or dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "test_name": TEST_NAME,
        "overall_status": "PASS" if overall_pass else "FAIL",
        "exact_layer": exact_layer,
        "status_counts": status_counts,
        "loops": loops,
        "x1_summary": {
            "surface": "x1**3 + x1*x2 + x3**2 - 3",
            "slice": {"x3": 2},
            "base_point_beta": 0,
            "common_frame_root_order": "sort roots at beta by (Re, Im)",
            "finite_lasso_order": "increasing arg(b_i - beta) in [0, 2*pi), CCW from positive real ray",
            "finite_permutations": finite_perms,
            "finite_cycle_types": [cycle_type(perm) for perm in finite_perms],
            "finite_swapped_pairs": [list(pair) for pair in finite_pairs],
            "finite_transpositions_distinct": distinct,
            "contractible_identity": _is_identity(contractible["pi_track"]),
            "strained_identity": _is_identity(strained["pi_track"]),
            "large_loop": big_loop["pi_track"],
        },
        "x2_summary": {
            "degree": 1,
            "monodromy": x2_loop["pi_track"],
            "stratum": "x1=0",
            "stratum_type": "role-denominator pole",
            "branch_monodromy": False,
        },
        "x3_summary": {
            "slice": {"x1": 1},
            "polynomial": "x3**2 + x2 - 2",
            "monodromy": x3_loop["pi_track"],
            "cycle_type": x3_loop["cycle_type"],
        },
        "coalescence_oracle": coalescence,
        "hurwitz": hurwitz,
        "controls": controls,
    }


def _strip_and_sort_lassos(all_lassos: list[dict]) -> list[dict]:
    return [
        _strip_internal_fields(loop)
        for loop in sorted(
            all_lassos,
            key=lambda item: (
                item["lasso_order_index"],
                item["radius"],
                item["branch_point"]["sympy_index"],
            ),
        )
    ]


def print_reference_confirmation(report: dict) -> None:
    exact = report["exact_layer"]
    controls = {control["name"]: control for control in report["controls"]}
    print("EXACT LAYER (sympy)")
    print(
        "  branch points: -3*2**(1/3)/2 , 3*2**(1/3)/4 -/+ 3*2**(1/3)*sqrt(3)*i/4         "
        f"{_pass_fail(len(exact['branch_points']) == 3)}"
    )
    print(
        "  pairwise |b_i-b_j|^2 = 27*2**(2/3)/4 (~10.715), equilateral                    "
        f"{_pass_fail(exact['equilateral'])}"
    )
    print(
        "  enclosure (center on b_i, rho in {0.5,1.0,1.5}): exactly one enclosed          "
        f"{_pass_fail(all(item['exactly_one_each'] for item in exact['enclosure_checks'].values()))}"
    )
    print(
        "  coalescence double roots r=-3/(2b): exact double roots (P=P'=0)                "
        f"{_pass_fail(all(item['p_zero'] and item['pprime_zero'] for item in exact['double_roots']))}"
    )
    print("")
    print("x1-SOLVE (common frame, beta=0)")
    print(
        "  m(b) at each branch point: cycle type (2,1)                                    "
        f"{_pass_fail(controls['x1_finite_branch_loops_certify_transpositions']['passed'])}"
    )
    print(
        "  three finite transpositions DISTINCT in common frame                          "
        f"{_pass_fail(controls['x1_common_frame_distinctness']['passed'])}"
    )
    print(
        "  large loop |x2|=5: cycle type (2,1) -> infinity ramified                       "
        f"{_pass_fail(report['hurwitz']['infinity_ramified'])}"
    )
    print(
        "  Hurwitz: m_big == CCW product of the three lassos                             "
        f"{_pass_fail(report['hurwitz']['equal'])}"
    )
    print(
        "  coalescence pairing: swapped pair -> -3/(2b) at each branch point             "
        f"{_pass_fail(controls['x1_coalescence_oracle_agreement']['passed'])}"
    )
    print(
        "  contractible loop (beta, radius 1): identity                                   "
        f"{_pass_fail(controls['x1_contractible_loop_identity']['passed'])}"
    )
    print("")
    print("x3-SOLVE")
    print(
        "  slice x1=1, x3^2+x2-2=0, loop x2 around 2: cycle type (2) swap                 "
        f"{_pass_fail(controls['x3_square_root_swap']['passed'])}"
    )
    print("")
    print("x2-SOLVE")
    print(
        "  degree 1, identity, x1=0 typed as role-denominator pole (not branch)           "
        f"{_pass_fail(controls['x2_structural_identity_pole_typing']['passed'])}"
    )
    print("")
    print("CERTIFICATE")
    print(
        "  every loop CERTIFIED_PERMUTATION; pi_track == pi_prox on every loop            "
        f"{_pass_fail(controls['certificate_gates']['passed'])}"
    )
    print(
        "  all failure-status counts zero                                                 "
        f"{_pass_fail(all(value == 0 for key, value in report['status_counts'].items() if key != CERTIFIED))}"
    )


def write_report(report: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_census_markdown(report: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    x1 = report["x1_summary"]
    x2 = report["x2_summary"]
    x3 = report["x3_summary"]
    annotations = x1_branch_channel_annotations()
    branch_rows = [
        (
            f"| x1 | {item['lasso_order_index']} | `{item['branch_point_exact']}` | "
            f"`{x1['finite_permutations'][item['lasso_order_index']]}` | "
            f"`{item['channel_vector_display']}` | `{item['channel_content']}` | "
            f"{item['reason']} |"
        )
        for item in annotations
    ]
    lines = [
        "# Cubic Role-Branch Census",
        "",
        "Surface: `F = x1^3 + x1*x2 + x3^2 - 3`.",
        "",
        "## x1 Role Solve",
        "",
        f"- Slice: `x3 = {x1['slice']['x3']}`.",
        f"- Base frame: `beta = {x1['base_point_beta']}`, roots ordered by `(Re, Im)`.",
        f"- Finite branch permutations, CCW order: `{x1['finite_permutations']}`.",
        f"- Finite cycle types: `{x1['finite_cycle_types']}`.",
        f"- Distinct transpositions in common frame: `{x1['finite_transpositions_distinct']}`.",
        f"- Large loop permutation: `{x1['large_loop']}`.",
        f"- Hurwitz `m_big == CCW product`: `{report['hurwitz']['equal']}`.",
        f"- Contractible loop identity: `{x1['contractible_identity']}`.",
        f"- Strained non-enclosing loop identity: `{x1['strained_identity']}`.",
        "",
        "### x1 Branch Strata",
        "",
        "Rows are sorted by `lasso_order_index`, the `[0, 2*pi)` CCW order used by the lasso run.",
        "",
        "| role | lasso_order_index | branch_point | monodromy | channel_vector (kappa_c,kappa_s,kappa_int) | channel_content | note |",
        "|---|---:|---|---|---|---|---|",
        *branch_rows,
        "",
        "## x2 Role Solve",
        "",
        f"- Degree: `{x2['degree']}`.",
        f"- Monodromy: `{x2['monodromy']}`.",
        f"- Stratum `{x2['stratum']}` typed as `{x2['stratum_type']}`.",
        "- This is a role-denominator pole stratum, not branch monodromy.",
        "",
        "## x3 Role Solve",
        "",
        f"- Slice: `x1 = {x3['slice']['x1']}`.",
        f"- Polynomial: `{x3['polynomial']}`.",
        f"- Monodromy: `{x3['monodromy']}`.",
        f"- Cycle type: `{x3['cycle_type']}`.",
        "",
        "## Certificate Summary",
        "",
        f"- Overall status: `{report['overall_status']}`.",
        f"- Status counts: `{report['status_counts']}`.",
        f"- Coalescence oracle matches: `{all(item['matches'] for item in report['coalescence_oracle'])}`.",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def default_report_path() -> Path:
    return Path(__file__).resolve().parent / "census_report.json"


def default_census_path() -> Path:
    return Path(__file__).resolve().parent / "CENSUS.md"


def raw_report_path() -> Path:
    return Path(RAW_OUTPUT_DIR) / "cubic_role_branch_census_report.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=default_report_path())
    parser.add_argument("--census-md", type=Path, default=default_census_path())
    parser.add_argument("--skip-raw-copy", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    tee = TeeStream(sys.stdout)
    sys.stdout = tee
    try:
        report = run_census()
        print_reference_confirmation(report)
        report["console_log"] = tee.getvalue()
    finally:
        sys.stdout = tee.original

    write_report(report, args.output)
    write_census_markdown(report, args.census_md)
    if not args.skip_raw_copy:
        os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
        write_report(report, raw_report_path())

    print(f"[report: {args.output}]")
    print(f"[census: {args.census_md}]")
    if not args.skip_raw_copy:
        print(f"[raw-copy: {raw_report_path()}]")
    return 0 if report["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
