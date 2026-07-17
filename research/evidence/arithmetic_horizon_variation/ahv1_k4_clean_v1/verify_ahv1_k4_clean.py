#!/usr/bin/env python3
"""Independent verifier for the clean AHV-1 k=4 evidence package."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import mpmath as mp
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ


HERE = Path(__file__).resolve().parent
u, y = sp.symbols("u y")


def load(path: str) -> object:
    return json.loads((HERE / path).read_text())


def digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def resultant_norm(a: list[int]) -> sp.Expr:
    """Independent iterated-resultant construction of the norm."""
    w = sp.symbols("w0:4")
    result = y - sum(w)
    for i in range(4):
        result = sp.resultant(result, w[i] ** 2 - u - a[i], w[i])
        result = sp.expand(result)
    return result


def terms(expr: sp.Expr) -> list[list[int]]:
    return [[iu, iy, int(c)] for (iu, iy), c in sp.Poly(expr, u, y).terms()]


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(left)))


def generated_group(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
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


def rank_mod2(matrix: list[list[int]]) -> int:
    rows = [[value & 1 for value in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0]) if rows else 0):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][column]:
                rows[r] = [a ^ b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def snf_nonzero(matrix: sp.Matrix) -> list[int]:
    normal = smith_normal_form(matrix, domain=ZZ)
    return [
        abs(int(normal[i, i]))
        for i in range(min(normal.shape))
        if normal[i, i]
    ]


def rebuild_matrices(loops: list[dict[str, object]]) -> tuple[sp.Matrix, ...]:
    d1 = sp.zeros(5, 90)
    d2 = sp.zeros(90, 77)
    vanishing = sp.zeros(5, 18)
    thimbles = sp.zeros(90, 18)
    pairs = [tuple(loop["transposition"]) for loop in loops]
    for j, (a, b) in enumerate(pairs):
        permutation = list(range(5))
        permutation[a], permutation[b] = b, a
        for sheet in range(5):
            d1[permutation[sheet], 5 * j + sheet] += 1
            d1[sheet, 5 * j + sheet] -= 1
        d2[5 * j + a, 4 * j] = 1
        d2[5 * j + b, 4 * j] = 1
        for offset, fixed in enumerate(s for s in range(5) if s not in (a, b)):
            d2[5 * j + fixed, 4 * j + 1 + offset] = 1
        vanishing[a, j] = -1
        vanishing[b, j] = 1
        thimbles[5 * j + a, j] = 1
    for start in range(5):
        sheet = start
        for j, (a, b) in enumerate(pairs):
            d2[5 * j + sheet, 72 + start] += 1
            if sheet == a:
                sheet = b
            elif sheet == b:
                sheet = a
        assert sheet == start
    return d1, d2, vanishing, thimbles


def verify_instance(
    certificate_path: str,
    chain_path: str,
    thimble_path: str,
) -> tuple[dict[str, object], sp.Expr]:
    certificate = load(certificate_path)
    chain = load(chain_path)
    thimble = load(thimble_path)
    exact = certificate["exact"]
    assert digest(exact) == certificate["exact_payload_sha256"]

    phi = resultant_norm(certificate["a"])
    assert terms(phi) == exact["norm_sparse_terms_u_y_coefficient"]
    assert sp.degree(phi, u) == 5 and sp.degree(phi, y) == 16
    assert str(sp.Poly(phi, u).LC()) == "-4096*y**6"

    branch_resultant = sp.resultant(phi, sp.diff(phi, u), u)
    critical_resultant = sp.resultant(phi, sp.diff(phi, u), y)
    branch_factors = sp.factor_list(branch_resultant)[1]
    critical_factors = sp.factor_list(critical_resultant)[1]
    assert [[sp.degree(f, y), e] for f, e in branch_factors] == exact[
        "branch_factor_degrees_and_exponents"
    ]
    assert [[sp.degree(f, u), e] for f, e in critical_factors] == exact[
        "critical_factor_degrees_and_exponents"
    ]
    branch = next(f for f, e in branch_factors if sp.degree(f, y) == 18 and e == 1)
    branch = sp.primitive(branch, y)[1]
    critical = next(f for f, e in critical_factors if sp.degree(f, u) == 9 and e == 2)
    critical = sp.primitive(critical, u)[1]
    assert [int(c) for c in sp.Poly(branch, y).all_coeffs()] == exact[
        "branch_polynomial_coefficients_descending_y"
    ]
    assert [int(c) for c in sp.Poly(critical, u).all_coeffs()] == exact[
        "critical_u_polynomial_coefficients_descending_u"
    ]
    assert sp.gcd(branch, sp.diff(branch, y)) == 1
    assert exact["good_locus"]["a_entries_pairwise_distinct"]
    assert exact["good_locus"]["all_balanced_signed_sums_nonzero"]

    hurwitz = certificate["hurwitz"]
    loops = hurwitz["loops"]
    assert len(loops) == 18
    assert [mp.mpf(loop["angle"]) for loop in loops] == sorted(
        mp.mpf(loop["angle"]) for loop in loops
    )
    permutations = [tuple(loop["permutation"]) for loop in loops]
    for loop, permutation in zip(loops, permutations):
        moved = [i for i, image in enumerate(permutation) if i != image]
        assert len(moved) == 2 and permutation[moved[0]] == moved[1]
        assert moved == loop["transposition"]
    product = tuple(range(5))
    for permutation in permutations:
        product = compose(permutation, product)
    assert list(product) == hurwitz["ordered_product"] == [0, 1, 2, 3, 4]
    assert len(generated_group(permutations)) == hurwitz["generated_group_order"] == 120
    assert len({tuple(loop["transposition"]) for loop in loops}) == 10

    mp.mp.dps = 60
    branch_coefficients = [mp.mpf(c) for c in sp.Poly(branch, y).all_coeffs()]
    branch_points = [
        mp.mpc(loop["branch_point"]["re"], loop["branch_point"]["im"])
        for loop in loops
    ]
    for point in branch_points:
        value = mp.mpc(0)
        for coefficient in branch_coefficients:
            value = value * point + coefficient
        scale = max(mp.mpf(1), abs(point) ** 18) * max(abs(c) for c in branch_coefficients)
        assert abs(value) / scale < mp.mpf("1e-45")
    assert min(
        abs(branch_points[i] - branch_points[j])
        for i in range(18)
        for j in range(i)
    ) > mp.mpf("1e-20")

    d1, d2, vanishing, thimbles = rebuild_matrices(loops)
    assert d1.tolist() == chain["d1"]
    assert d2.tolist() == chain["d2"]
    assert d1 * d2 == sp.zeros(5, 77)
    assert snf_nonzero(d1) == chain["smith"]["d1_nonzero"] == [1] * 4
    assert snf_nonzero(d2) == chain["smith"]["d2_nonzero"] == [1] * 76
    assert chain["homology"]["H0"] == {"free_rank": 1, "torsion": []}
    assert chain["homology"]["H1"] == {"free_rank": 10, "torsion": []}
    assert chain["homology"]["H2"] == {"free_rank": 1, "torsion": []}
    assert chain["euler_characteristic"] == -8 and chain["genus_from_h1"] == 5

    assert vanishing.tolist() == thimble["vanishing_boundary_matrix"]
    assert thimbles.tolist() == thimble["thimble_matrix"]
    augmented = d2.row_join(thimbles)
    gram = vanishing.T * vanishing
    assert snf_nonzero(vanishing) == thimble["smith"]["vanishing_nonzero"] == [1] * 4
    assert snf_nonzero(augmented) == thimble["smith"][
        "augmented_d2_thimbles_nonzero"
    ] == [1] * 90
    assert snf_nonzero(gram) == thimble["smith"]["gram_nonzero"] == [1, 1, 1, 5]
    assert thimble["relative_lattice"] == {
        "free_rank": 14,
        "presentation": "C1/im(d2)",
        "thimbles_generate_integrally": True,
        "torsion": [],
    }
    assert thimble["mod2"] == {
        "augmented_rank": 90,
        "d2_rank": 76,
        "gram_radical_dimension": 14,
        "gram_rank": 4,
        "relative_thimble_span_dimension": 14,
        "vanishing_rank": 4,
    }
    assert rank_mod2(gram.tolist()) == 4
    return certificate, branch


def verify() -> None:
    control, _ = verify_instance(
        "certificates/topological_control.json",
        "matrices/control_chain_matrices.json",
        "matrices/control_thimbles.json",
    )
    decoration, branch = verify_instance(
        "certificates/decoration_live.json",
        "matrices/decoration_chain_matrices.json",
        "matrices/decoration_thimbles.json",
    )
    assert control["a"] == [0, 2, 3, 7]
    assert control["scope"] == {
        "closes_all_k_IV3": False,
        "kummer_claims": False,
        "topology_only": True,
    }
    assert decoration["a"] == [1, 4, 16, 64]
    assert decoration["scope"] == {
        "closes_all_k_IV3": False,
        "closes_k4_static_R9": True,
    }

    kummer = decoration["kummer"]
    assert kummer == load("matrices/decoration_kummer_parity.json")
    assert kummer["normalization"] == "gamma_R9=2*(P+e4(w))"
    assert kummer["N"] == [1, 2, 4, 8]
    assert kummer["a_equals_N_squared"] == decoration["a"]
    assert kummer["P"] == 64
    assert kummer["sheet_level_B"] == [[1, 0], [1, 1]]
    assert kummer["even_contact"]["reciprocal_sum"] == "15/8"
    assert kummer["even_contact"]["beta_contact"] == "120"
    assert kummer["odd_contact"]["reciprocal_sum"] == "-1/8"
    assert kummer["odd_contact"]["beta_contact"] == "8"
    for contact in (kummer["even_contact"], kummer["odd_contact"]):
        assert branch.subs(y, contact["contact_y"]) != 0
        assert contact["unramified_at_specialized_contact"]
    parity = kummer["orbit_saturated_matrix"]
    assert parity == (
        sp.eye(5).row_join(sp.zeros(5)).col_join(sp.eye(5).row_join(sp.eye(5)))
    ).tolist()
    assert rank_mod2(parity) == kummer["orbit_saturated_rank_F2"] == 10
    assert kummer["normal_closure_group"] == "C2^2 wr S5"
    assert kummer["normal_closure_group_order"] == 122880

    report = (HERE / "reports/AHV1_K4_CLEAN_EXECUTION_v1.0.md").read_text()
    assert "does **not** prove the arbitrary-k relation module vanishes" in report
    assert "gamma_R9=2(P+e_4(w))" in report
    assert "gamma=P+e_4(w)" not in report
    print("PASS: clean AHV-1 k=4 exact, Hurwitz, lattice, and Kummer certificates")


if __name__ == "__main__":
    verify()
