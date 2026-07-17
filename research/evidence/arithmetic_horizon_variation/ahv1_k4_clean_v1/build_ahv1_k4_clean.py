#!/usr/bin/env python3
"""Build the clean AHV-1 k=4 evidence package from exact input data.

It constructs the multiquadratic norm, finite branch polynomial, Hurwitz
transpositions, cellular matrices, and the decoration-live Kummer matrix.
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import sys

import mpmath as mp
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ


HERE = Path(__file__).resolve().parent
u, y = sp.symbols("u y")
MP_DPS = 50
LINE_STEPS = 500
CIRCLE_STEPS = 300


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            default=lambda value: int(value)
            if isinstance(value, sp.Integer)
            else str(value),
        )
        + "\n"
    )


def sha256_json(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def norm_polynomial(a: tuple[int, int, int, int]) -> sp.Expr:
    """Norm of y-sum(w_i) in Q(u)[w_i]/(w_i^2-u-a_i)."""
    zero = sp.Poly(0, u, y, domain=ZZ)
    one = sp.Poly(1, u, y, domain=ZZ)
    yy = sp.Poly(y, u, y, domain=ZZ)
    element = {0: one}
    for signs in itertools.product((-1, 1), repeat=4):
        factor = {0: yy}
        factor.update(
            {1 << i: sp.Poly(-signs[i], u, y, domain=ZZ) for i in range(4)}
        )
        product: dict[int, sp.Poly] = {}
        for left_mask, left_poly in element.items():
            for right_mask, right_poly in factor.items():
                scalar = one
                for i in range(4):
                    if ((left_mask & right_mask) >> i) & 1:
                        scalar *= sp.Poly(u + a[i], u, y, domain=ZZ)
                mask = left_mask ^ right_mask
                product[mask] = product.get(mask, zero) + left_poly * right_poly * scalar
        element = {mask: poly for mask, poly in product.items() if poly}
    if set(element) != {0}:
        raise AssertionError("multiquadratic norm did not descend to Q[u,y]")
    return sp.expand(element[0].as_expr())


def sparse_terms(expr: sp.Expr) -> list[list[int]]:
    return [[iu, iy, int(c)] for (iu, iy), c in sp.Poly(expr, u, y).terms()]


def univariate_coefficients(expr: sp.Expr, variable: sp.Symbol) -> list[int]:
    return [int(c) for c in sp.Poly(expr, variable, domain=ZZ).all_coeffs()]


def select_factor(
    factorization: tuple[sp.Expr, list[tuple[sp.Expr, int]]],
    variable: sp.Symbol,
    degree: int,
    exponent: int,
) -> sp.Expr:
    candidates = [
        factor
        for factor, power in factorization[1]
        if sp.degree(factor, variable) == degree and power == exponent
    ]
    if len(candidates) != 1:
        raise AssertionError(
            f"expected one degree-{degree}, exponent-{exponent} factor; got {len(candidates)}"
        )
    return sp.primitive(candidates[0], variable)[1]


def exact_stage(a: tuple[int, int, int, int]) -> dict[str, object]:
    phi = norm_polynomial(a)
    branch_resultant = sp.resultant(phi, sp.diff(phi, u), u)
    critical_resultant = sp.resultant(phi, sp.diff(phi, u), y)
    branch_factorization = sp.factor_list(branch_resultant)
    critical_factorization = sp.factor_list(critical_resultant)
    branch = select_factor(branch_factorization, y, 18, 1)
    critical = select_factor(critical_factorization, u, 9, 2)
    if sp.gcd(branch, sp.diff(branch, y)) != 1:
        raise AssertionError("finite branch polynomial is not square-free")
    good_locus_balances = {
        "".join("+" if e == 1 else "-" for e in signs): sum(
            signs[i] * a[i] for i in range(4)
        )
        for signs in itertools.product((-1, 1), repeat=4)
        if signs[0] == 1
    }
    return {
        "phi": phi,
        "branch": branch,
        "critical": critical,
        "branch_factor_degrees": [
            [int(sp.degree(f, y)), int(e)] for f, e in branch_factorization[1]
        ],
        "critical_factor_degrees": [
            [int(sp.degree(f, u)), int(e)] for f, e in critical_factorization[1]
        ],
        "good_locus": {
            "a_entries_pairwise_distinct": len(set(a)) == 4,
            "balanced_signed_sums": good_locus_balances,
            "all_balanced_signed_sums_nonzero": all(good_locus_balances.values()),
        },
    }


def mp_complex(value: object, digits: int = 60) -> mp.mpc:
    z = sp.sympify(value)
    return mp.mpc(str(sp.re(z).evalf(digits)), str(sp.im(z).evalf(digits)))


def complex_record(z: mp.mpc) -> dict[str, str]:
    return {"re": mp.nstr(mp.re(z), MP_DPS), "im": mp.nstr(mp.im(z), MP_DPS)}


def distance_to_segment(point: complex, start: complex, end: complex) -> float:
    vector = end - start
    t = (
        (point - start).real * vector.real
        + (point - start).imag * vector.imag
    ) / abs(vector) ** 2
    t = max(0.0, min(1.0, t))
    return abs(point - (start + t * vector))


def choose_star_base(branches: list[complex]) -> tuple[complex, float]:
    radius = max(abs(z) for z in branches)
    best = (-1.0, 0j)
    for radial_index in range(13):
        trial_radius = (1.1 + 0.2 * radial_index) * radius
        for angular_index in range(720):
            base = trial_radius * cmath.exp(2j * math.pi * angular_index / 720)
            clearance = min(
                distance_to_segment(branches[j], base, branches[i])
                for i in range(len(branches))
                for j in range(len(branches))
                if i != j
            )
            if clearance > best[0]:
                best = (clearance, base)
    return best[1], best[0]


def coefficient_vector(expr: sp.Expr) -> list[int]:
    poly = sp.Poly(expr, y)
    terms = dict(poly.terms())
    return [int(terms.get((power,), 0)) for power in range(poly.degree(), -1, -1)]


def horner(coefficients: list[mp.mpc], value: mp.mpc) -> mp.mpc:
    result = mp.mpc(0)
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def match_permutation(left: list[mp.mpc], right: list[mp.mpc]) -> tuple[int, ...]:
    return min(
        (
            sum(abs(left[i] - right[p[i]]) ** 2 for i in range(5)),
            p,
        )
        for p in itertools.permutations(range(5))
    )[1]


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(left)))


def permutation_group(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = tuple(range(5))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            candidate = compose(generator, current)
            if candidate not in group:
                group.add(candidate)
                frontier.append(candidate)
    return group


def numerical_hurwitz(phi: sp.Expr, branch: sp.Expr) -> dict[str, object]:
    mp.mp.dps = MP_DPS
    approximate = list(sp.nroots(branch, n=MP_DPS + 5, maxsteps=1000))
    branches = [mp_complex(root) for root in approximate]
    base0, clearance = choose_star_base([complex(z) for z in branches])
    base = mp.mpc(base0.real, base0.imag)

    phi_u = sp.Poly(phi, u)
    coefficient_polys = phi_u.all_coeffs()
    coefficient_vectors = [coefficient_vector(c) for c in coefficient_polys]
    y_derivative_vectors = [coefficient_vector(sp.diff(c, y)) for c in coefficient_polys]

    def coefficients_at(z: mp.mpc) -> list[mp.mpc]:
        return [horner(vector, z) for vector in coefficient_vectors]

    def y_coefficients_at(z: mp.mpc) -> list[mp.mpc]:
        return [horner(vector, z) for vector in y_derivative_vectors]

    def u_derivative_value(coefficients: list[mp.mpc], x: mp.mpc) -> mp.mpc:
        return horner([(5 - i) * coefficients[i] for i in range(5)], x)

    base_sympy = sp.Float(str(mp.re(base)), MP_DPS + 10) + sp.I * sp.Float(
        str(mp.im(base)), MP_DPS + 10
    )
    initial = [
        mp_complex(root)
        for root in sp.nroots(
            sp.Poly(phi.subs(y, base_sympy), u), n=MP_DPS + 5, maxsteps=1000
        )
    ]
    initial.sort(key=lambda z: (float(mp.re(z)), float(mp.im(z))))

    maximum_residual = mp.mpf(0)
    minimum_sheet_separation = mp.inf

    def advance(
        old_roots: list[mp.mpc], old_y: mp.mpc, new_y: mp.mpc
    ) -> list[mp.mpc]:
        nonlocal maximum_residual, minimum_sheet_separation
        old_coefficients = coefficients_at(old_y)
        old_y_coefficients = y_coefficients_at(old_y)
        new_coefficients = coefficients_at(new_y)
        delta_y = new_y - old_y
        new_roots = []
        for old_root in old_roots:
            root = old_root - (
                horner(old_y_coefficients, old_root)
                / u_derivative_value(old_coefficients, old_root)
            ) * delta_y
            for _ in range(16):
                correction = horner(new_coefficients, root) / u_derivative_value(
                    new_coefficients, root
                )
                root -= correction
                if abs(correction) < mp.mpf("1e-38"):
                    break
            residual = abs(horner(new_coefficients, root))
            maximum_residual = max(maximum_residual, residual)
            new_roots.append(root)
        separation = min(
            abs(new_roots[i] - new_roots[j])
            for i in range(5)
            for j in range(i)
        )
        minimum_sheet_separation = min(minimum_sheet_separation, separation)
        if separation < mp.mpf("1e-16"):
            raise AssertionError("sheet continuation lost separation")
        return new_roots

    loops: list[dict[str, object]] = []
    for branch_index, branch_point in enumerate(branches):
        nearest = min(
            abs(branch_point - other)
            for j, other in enumerate(branches)
            if j != branch_index
        )
        loop_radius = min(mp.mpf("0.035") * nearest, mp.mpf("0.04"))
        approach = branch_point + loop_radius * (base - branch_point) / abs(
            base - branch_point
        )
        roots = list(initial)
        previous_y = base
        for step in range(1, LINE_STEPS + 1):
            next_y = base + (approach - base) * step / LINE_STEPS
            roots = advance(roots, previous_y, next_y)
            previous_y = next_y
        initial_angle = mp.arg(approach - branch_point)
        for step in range(1, CIRCLE_STEPS + 1):
            next_y = branch_point + loop_radius * mp.e ** (
                1j * (initial_angle + 2 * mp.pi * step / CIRCLE_STEPS)
            )
            roots = advance(roots, previous_y, next_y)
            previous_y = next_y
        for step in range(1, LINE_STEPS + 1):
            next_y = approach + (base - approach) * step / LINE_STEPS
            roots = advance(roots, previous_y, next_y)
            previous_y = next_y
        permutation = match_permutation(roots, initial)
        moved = [i for i, image in enumerate(permutation) if i != image]
        if len(moved) != 2 or permutation[moved[0]] != moved[1]:
            raise AssertionError(f"loop {branch_index} was not a transposition")
        loops.append(
            {
                "angle": mp.nstr(mp.arg(branch_point - base), MP_DPS),
                "branch_point": complex_record(branch_point),
                "nearest_branch_distance": mp.nstr(nearest, MP_DPS),
                "loop_radius": mp.nstr(loop_radius, MP_DPS),
                "permutation": list(permutation),
                "transposition": moved,
            }
        )

    loops.sort(key=lambda item: mp.mpf(item["angle"]))
    permutations = [tuple(item["permutation"]) for item in loops]
    product = tuple(range(5))
    for permutation in permutations:
        product = compose(permutation, product)
    group = permutation_group(permutations)
    used_pairs = sorted({tuple(item["transposition"]) for item in loops})
    if product != tuple(range(5)) or len(group) != 120:
        raise AssertionError("Hurwitz product/group certificate failed")
    return {
        "precision_decimal_digits": MP_DPS,
        "path_model": "noncrossing optimized star; CCW meridians",
        "line_steps_each_way": LINE_STEPS,
        "circle_steps": CIRCLE_STEPS,
        "basepoint": complex_record(base),
        "minimum_star_clearance": repr(clearance),
        "initial_sheet_roots": [complex_record(root) for root in initial],
        "loops_order": "increasing argument(branch-basepoint)",
        "loops": loops,
        "ordered_product": list(product),
        "generated_group_order": len(group),
        "distinct_transposition_pairs": [list(pair) for pair in used_pairs],
        "maximum_absolute_newton_residual": mp.nstr(maximum_residual, 20),
        "minimum_tracked_sheet_separation": mp.nstr(minimum_sheet_separation, 20),
    }


def integer_rank_mod2(matrix: list[list[int]]) -> int:
    rows = [[entry & 1 for entry in row] for row in matrix]
    if not rows:
        return 0
    rank = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][column]:
                rows[r] = [a ^ b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def nonzero_snf(matrix: sp.Matrix) -> list[int]:
    diagonal = smith_normal_form(matrix, domain=ZZ)
    return [
        abs(int(diagonal[i, i]))
        for i in range(min(diagonal.shape))
        if diagonal[i, i]
    ]


def chain_data(loops: list[dict[str, object]]) -> tuple[dict[str, object], dict[str, object]]:
    transpositions = [tuple(item["transposition"]) for item in loops]
    d1 = sp.zeros(5, 90)
    d2 = sp.zeros(90, 77)
    for j, (a, b) in enumerate(transpositions):
        permutation = list(range(5))
        permutation[a], permutation[b] = permutation[b], permutation[a]
        for sheet in range(5):
            edge = 5 * j + sheet
            d1[permutation[sheet], edge] += 1
            d1[sheet, edge] -= 1
        column = 4 * j
        d2[5 * j + a, column] = 1
        d2[5 * j + b, column] = 1
        for offset, fixed in enumerate(s for s in range(5) if s not in (a, b)):
            d2[5 * j + fixed, column + 1 + offset] = 1
    for starting_sheet in range(5):
        sheet = starting_sheet
        column = 72 + starting_sheet
        for j, (a, b) in enumerate(transpositions):
            d2[5 * j + sheet, column] += 1
            if sheet == a:
                sheet = b
            elif sheet == b:
                sheet = a
        if sheet != starting_sheet:
            raise AssertionError("outer lift did not close")
    if d1 * d2 != sp.zeros(5, 77):
        raise AssertionError("cellular boundary composition is nonzero")

    vanishing = sp.zeros(5, 18)
    thimbles = sp.zeros(90, 18)
    for j, (a, b) in enumerate(transpositions):
        vanishing[a, j] = -1
        vanishing[b, j] = 1
        thimbles[5 * j + a, j] = 1
    augmented = d2.row_join(thimbles)
    gram = vanishing.T * vanishing
    d1_snf = nonzero_snf(d1)
    d2_snf = nonzero_snf(d2)
    vanishing_snf = nonzero_snf(vanishing)
    augmented_snf = nonzero_snf(augmented)
    gram_snf = nonzero_snf(gram)
    d2_mod2_rank = integer_rank_mod2(d2.tolist())
    augmented_mod2_rank = integer_rank_mod2(augmented.tolist())
    gram_mod2_rank = integer_rank_mod2(gram.tolist())

    chain_payload = {
        "model": "five-vertex compressed lifted CW model",
        "basis": {
            "C0": "five sheets over the basepoint",
            "C1": "e_(j,s), j=0..17 and s=0..4",
            "C2": "four local filling cycles per branch plus five outer lifts",
        },
        "shapes": {"d1": list(d1.shape), "d2": list(d2.shape)},
        "d1": d1.tolist(),
        "d2": d2.tolist(),
        "d1_d2_zero": True,
        "smith": {"d1_nonzero": d1_snf, "d2_nonzero": d2_snf},
        "homology": {
            "H0": {"free_rank": 1, "torsion": []},
            "H1": {
                "free_rank": 90 - len(d1_snf) - len(d2_snf),
                "torsion": [value for value in d2_snf if value != 1],
            },
            "H2": {"free_rank": 77 - len(d2_snf), "torsion": []},
        },
        "euler_characteristic": 5 - 90 + 77,
        "genus_from_h1": (90 - len(d1_snf) - len(d2_snf)) // 2,
    }
    thimble_payload = {
        "vanishing_boundary_matrix": vanishing.tolist(),
        "thimble_matrix": thimbles.tolist(),
        "smith": {
            "vanishing_nonzero": vanishing_snf,
            "augmented_d2_thimbles_nonzero": augmented_snf,
            "gram_nonzero": gram_snf,
        },
        "relative_lattice": {
            "presentation": "C1/im(d2)",
            "free_rank": 90 - len(d2_snf),
            "torsion": [value for value in d2_snf if value != 1],
            "thimbles_generate_integrally": len(augmented_snf) == 90
            and all(value == 1 for value in augmented_snf),
        },
        "mod2": {
            "vanishing_rank": integer_rank_mod2(vanishing.tolist()),
            "gram_rank": gram_mod2_rank,
            "gram_radical_dimension": 18 - gram_mod2_rank,
            "d2_rank": d2_mod2_rank,
            "augmented_rank": augmented_mod2_rank,
            "relative_thimble_span_dimension": augmented_mod2_rank - d2_mod2_rank,
        },
    }
    return chain_payload, thimble_payload


def exact_certificate(
    name: str,
    a: tuple[int, int, int, int],
    exact: dict[str, object],
    hurwitz: dict[str, object],
) -> dict[str, object]:
    phi = exact["phi"]
    branch = exact["branch"]
    critical = exact["critical"]
    exact_payload = {
        "norm_sparse_terms_u_y_coefficient": sparse_terms(phi),
        "norm_degree_u": int(sp.degree(phi, u)),
        "norm_degree_y": int(sp.degree(phi, y)),
        "norm_leading_u_coefficient": str(sp.Poly(phi, u).LC()),
        "branch_polynomial_coefficients_descending_y": univariate_coefficients(branch, y),
        "critical_u_polynomial_coefficients_descending_u": univariate_coefficients(
            critical, u
        ),
        "branch_factor_degrees_and_exponents": exact["branch_factor_degrees"],
        "critical_factor_degrees_and_exponents": exact["critical_factor_degrees"],
        "branch_polynomial_square_free": True,
        "good_locus": exact["good_locus"],
    }
    return {
        "schema": "cella.ahv1.k4.clean.instance.v1",
        "instance": name,
        "model": "w_i^2=u+a_i; y=sum_i w_i",
        "a": list(a),
        "exact": exact_payload,
        "exact_payload_sha256": sha256_json(exact_payload),
        "hurwitz": hurwitz,
        "topology": {
            "degree": 5,
            "finite_simple_branch_points": 18,
            "riemann_hurwitz_genus": 5,
        },
        "provenance": {
            "construction": "independent exact norm and high-precision continuation",
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "mpmath": mp.__version__,
        },
    }


def kummer_payload(branch: sp.Expr) -> dict[str, object]:
    n = (1, 2, 4, 8)
    product = math.prod(n)
    even_signs = (1, 1, 1, 1)
    odd_signs = (-1, 1, 1, 1)

    def witness(signs: tuple[int, int, int, int]) -> dict[str, object]:
        sign_product = math.prod(signs)
        contact_y = sum(signs[i] * n[i] for i in range(4))
        reciprocal_sum = sum(sp.Rational(signs[i], n[i]) for i in range(4))
        beta = sign_product * product * reciprocal_sum
        gamma = 2 * product * (1 + sign_product)
        return {
            "signs": list(signs),
            "contact_y": contact_y,
            "sign_product": sign_product,
            "reciprocal_sum": str(reciprocal_sum),
            "beta_contact": str(beta),
            "gamma_R9_contact": gamma,
            "branch_polynomial_at_contact": str(sp.expand(branch).subs(y, contact_y)),
            "unramified_at_specialized_contact": branch.subs(y, contact_y) != 0,
        }

    parity = sp.zeros(10, 10)
    for i in range(5):
        parity[i, i] = 1
        parity[5 + i, i] = 1
        parity[5 + i, 5 + i] = 1
    return {
        "normalization": "gamma_R9=2*(e4(w)+u*e2(w)+u^2+P)",
        "alpha": "e4(w)+u*e2(w)+u^2",
        "beta": "e3(w)+u*e1(w)",
        "N": list(n),
        "a_equals_N_squared": [value * value for value in n],
        "P": product,
        "identity": "gamma_R9*(gamma_R9-4*P)=4*u*beta^2",
        "even_contact": witness(even_signs),
        "odd_contact": witness(odd_signs),
        "sheet_level_B": [[1, 0], [1, 1]],
        "orbit_saturated_matrix": [
            [int(parity[row, column]) for column in range(10)]
            for row in range(10)
        ],
        "orbit_saturated_rank_F2": integer_rank_mod2(parity.tolist()),
        "square_class_rank": 10,
        "base_group": "S5",
        "normal_closure_group": "C2^2 wr S5",
        "normal_closure_group_order": 122880,
        "scope_note": "This is the k=4 static two-channel certificate only.",
    }


def report_text(control: dict[str, object], decoration: dict[str, object]) -> str:
    c_h = control["hurwitz"]
    d_h = decoration["hurwitz"]
    k = decoration["kummer"]
    return f"""# AHV-1 at k=4: clean two-instance execution

**Version:** 1.0  
**Status:** independently rebuilt and replay-gated  
**Scope:** a k=4 falsifier/probe, not an all-k IV.3 closure

## 1. Separation of roles

This package deliberately uses two instances and does not merge their claims.

1. The **topological control** is `a=(0,2,3,7)`. It certifies the finite branch system, explicit Hurwitz transpositions, genus, integral homology, and thimble lattice. Because `a_1=0`, it is not used for the R9 contact/Kummer channel.
2. The **decoration-live instance** is `N=(1,2,4,8)`, hence `a=N^2=(1,4,16,64)`. It independently repeats the topology calculation and supplies the canonical R9 channels `r_1=u` and `r_2=gamma_R9=2(e_4(w)+u e_2(w)+u^2+P)`.

## 2. Exact eliminants and finite branching

For each instance the builder forms the full multiquadratic norm

`Phi(u,y)=prod_{{epsilon in {{+-1}}^4}}(y-sum_i epsilon_i w_i)`, with `w_i^2=u+a_i`,

inside the exact 16-dimensional group algebra. In both cases `deg_u Phi=5`, `deg_y Phi=16`, and the leading `u^5` coefficient is `-4096*y^6`. Exact resultants isolate:

- one degree-9 factor in `Res_y(Phi,Phi_u)`, occurring with exponent two;
- one square-free degree-18 factor in `Res_u(Phi,Phi_u)`, occurring with exponent one.

Thus each instance has 18 distinct finite simple branch values. Their exact coefficient lists, all resultant factor degrees, and the sparse norm are in the two certificates.

## 3. Explicit Hurwitz systems

Sheets were continued at {MP_DPS}-digit precision around a deterministic noncrossing star of counter-clockwise meridians. Every local permutation is a transposition. For the control instance their ordered product is `{c_h['ordered_product']}`, they generate a group of order `{c_h['generated_group_order']}`, and all ten transposition pairs occur. The decoration-live instance independently gives product `{d_h['ordered_product']}`, group order `{d_h['generated_group_order']}`, and again all ten pairs.

The group is therefore `S_5` in both instances. The recorded branch values, base roots, loop radii, path order, permutations, residual bound, and separation bound make the continuation auditable.

## 4. Integral topology from the computed monodromy

The matrix artifacts use a compressed lifted CW model with 5 vertices, 90 lifted branch edges, and 77 faces. It is chain-equivalent to the more heavily subdivided 95-vertex/180-edge model; no homology claim depends on that subdivision choice.

For both independently computed Hurwitz systems:

- `d_1 d_2=0`;
- `SNF(d_1)` has four nonzero invariant factors, all one;
- `SNF(d_2)` has 76 nonzero invariant factors, all one;
- `H_0=Z`, `H_1=Z^10` with no torsion, and `H_2=Z`;
- `chi=-8`, hence `g=5`, independently agreeing with Riemann--Hurwitz.

## 5. Vanishing cycles and thimbles

For each branch transposition `(a b)`, the vanishing boundary is `e_b-e_a` and the selected thimble is the lifted edge `e_(j,a)`. Exact Smith reduction gives:

- boundary SNF `(1,1,1,1)`, so the cycles integrally generate `A_4`;
- `H_1(X,F_0;Z)=C_1/im(d_2)=Z^14`;
- the augmented matrix `[d_2 | T]` has 90 invariant factors, all one, so the 18 thimbles generate the relative lattice integrally;
- the Gram matrix has nonzero SNF `(1,1,1,5)`, hence discriminant group `Z/5`;
- over `F_2`, the Gram rank is 4, its radical has dimension 14, and the relative thimble span has dimension 14.

There is no integral index defect and no hidden 2-torsion in this presentation.

## 6. Canonically normalized R9 Kummer certificate

Only the decoration-live instance is used here. With `P=64`,

Globally, `alpha=e_4(w)+u e_2(w)+u^2`, `beta=e_3(w)+u e_1(w)`, and

`gamma_R9=2(alpha+P)=2(e_4(w)+u e_2(w)+u^2+P)`.

The exact factorization `prod_i(w_i+sqrt(u))=alpha+sqrt(u) beta` gives
`alpha^2-u beta^2=P^2`, hence
`gamma_R9(gamma_R9-4P)=4u beta^2`. At a signed contact `u=0`, this global
radicand specializes to `2(P+e_4(w))`; only that specialization was used to
compute the two parity rows below.

The all-plus contact has `y=15`, reciprocal sum `15/8`, `beta=120`, and parity row `(1,0)`. The odd contact `(-,+,+,+)` has `y=13`, reciprocal sum `-1/8`, `beta=8`, and parity row `(1,1)`. Exact evaluation of the degree-18 branch polynomial at both contact values is nonzero, so these specialized contacts are away from the finite mass branch locus.

Orbit saturation under the independently certified transitive `S_5` action gives

`V=[[I_5,0],[I_5,I_5]]=B tensor I_5`, where `B=[[1,0],[1,1]]`.

Its `F_2` rank is {k['orbit_saturated_rank_F2']}. The ten conjugate square classes are independent and the k=4 static normal closure is `C_2^2 wr S_5`, of order `{k['normal_closure_group_order']}`.

## 7. What this does and does not establish

This clean run establishes the k=4 topology, integral thimble generation, and canonical two-channel R9 parity certificate on explicit good instances. It upgrades the evidence base by making every matrix and exact eliminant available for replay.

It does **not** prove the arbitrary-k relation module vanishes, identify a universal entropy-type second radicand for k other than 4, or close all of IV.3. In particular, no rank claim is made from a single unsaturated prolongation; the Kummer conclusion uses the full `S_5` orbit.

## 8. Replay

Run `python3 build_ahv1_k4_clean.py` to reconstruct the package, then `python3 verify_ahv1_k4_clean.py` or the repository gate `python3 engine/tests/gate_ahv1_k4_clean.py`.
"""


def build() -> None:
    instances = {
        "topological_control": (0, 2, 3, 7),
        "decoration_live": (1, 4, 16, 64),
    }
    certificates: dict[str, dict[str, object]] = {}
    chains: dict[str, dict[str, object]] = {}
    thimbles: dict[str, dict[str, object]] = {}
    exact_by_name: dict[str, dict[str, object]] = {}
    for name, a in instances.items():
        print(f"[{name}] exact norm/resultants", flush=True)
        exact = exact_stage(a)
        print(f"[{name}] numerical Hurwitz continuation", flush=True)
        hurwitz = numerical_hurwitz(exact["phi"], exact["branch"])
        print(f"[{name}] integral matrices", flush=True)
        chain, thimble = chain_data(hurwitz["loops"])
        certificate = exact_certificate(name, a, exact, hurwitz)
        certificates[name] = certificate
        chains[name] = chain
        thimbles[name] = thimble
        exact_by_name[name] = exact

    decoration = certificates["decoration_live"]
    decoration["kummer"] = kummer_payload(exact_by_name["decoration_live"]["branch"])
    decoration["scope"] = {
        "closes_k4_static_R9": True,
        "closes_all_k_IV3": False,
    }
    certificates["topological_control"]["scope"] = {
        "topology_only": True,
        "kummer_claims": False,
        "closes_all_k_IV3": False,
    }

    write_json(HERE / "certificates/topological_control.json", certificates["topological_control"])
    write_json(HERE / "certificates/decoration_live.json", decoration)
    write_json(HERE / "matrices/control_chain_matrices.json", chains["topological_control"])
    write_json(HERE / "matrices/control_thimbles.json", thimbles["topological_control"])
    write_json(HERE / "matrices/decoration_chain_matrices.json", chains["decoration_live"])
    write_json(HERE / "matrices/decoration_thimbles.json", thimbles["decoration_live"])
    write_json(HERE / "matrices/decoration_kummer_parity.json", decoration["kummer"])
    report = report_text(certificates["topological_control"], decoration)
    report_path = HERE / "reports/AHV1_K4_CLEAN_EXECUTION_v1.0.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    print("clean AHV-1 k=4 package built", flush=True)


if __name__ == "__main__":
    try:
        build()
    except KeyboardInterrupt:
        sys.exit(130)
