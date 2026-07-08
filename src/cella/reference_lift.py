"""Reference_Material lifts promoted into exact Cella tools.

The functions here are not imports of the origin scripts. They are small,
stdlib-only exact reconstructions of the reusable primitives those scripts and
briefs were converging on.
"""

from __future__ import annotations

from collections import deque
from fractions import Fraction
from itertools import combinations
from math import comb, factorial, gcd


def _q(x) -> Fraction:
    if isinstance(x, bool):
        raise TypeError("booleans are not exact rationals")
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x.strip())
    raise TypeError(f"expected exact integer or rational string, got {type(x).__name__}")


def _vec(xs) -> tuple[Fraction, ...]:
    return tuple(_q(x) for x in xs)


def _mat(rows) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(_q(x) for x in row) for row in rows)


def _det(M) -> Fraction:
    n = len(M)
    if n == 0:
        return Fraction(1)
    if n == 1:
        return M[0][0]
    total = Fraction(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * _det(minor)
    return total


def _fmt_key(items) -> str:
    return ",".join(str(i) for i in items)


def _solve_square(A, b) -> tuple[Fraction, ...]:
    detA = _det(A)
    if detA == 0:
        raise ZeroDivisionError("linear recovery matrix is singular")
    out = []
    n = len(A)
    for col in range(n):
        M = [list(row) for row in A]
        for i in range(n):
            M[i][col] = b[i]
        out.append(_det(tuple(tuple(row) for row in M)) / detA)
    return tuple(out)


def _channel_components(g, H) -> dict:
    g = _vec(g)
    H = _mat(H)
    if len(g) != 3 or len(H) != 3 or any(len(row) != 3 for row in H):
        raise ValueError("three-channel referee requires a 3-vector and 3x3 Hessian")
    q = sum(x * x for x in g)
    if q == 0:
        raise ValueError("singular gradient: q=0")
    g1, g2, g3 = g
    H11, H22, H33 = H[0][0], H[1][1], H[2][2]
    H12, H13, H23 = H[0][1], H[0][2], H[1][2]
    Delta_c = (
        g1 * g1 * H23 * H23
        + g2 * g2 * H13 * H13
        + g3 * g3 * H12 * H12
        - 2 * g1 * g2 * H13 * H23
        - 2 * g1 * g3 * H12 * H23
        - 2 * g2 * g3 * H12 * H13
    )
    Delta_s = -(
        g1 * g1 * H22 * H33
        + g2 * g2 * H11 * H33
        + g3 * g3 * H11 * H22
    )
    Delta_m = 2 * (
        g1 * g2 * H12 * H33
        + g1 * g3 * H13 * H22
        + g2 * g3 * H11 * H23
    )
    bordered = _det(((0, g1, g2, g3), (g1, *H[0]), (g2, *H[1]), (g3, *H[2])))
    delta_sum = Delta_c + Delta_s + Delta_m
    den = q * q
    kappa_c = -Delta_c / den
    kappa_s = -Delta_s / den
    kappa_int = -Delta_m / den
    K_G = kappa_c + kappa_s + kappa_int

    # The classic kappa_s trap: naively mirroring the traceless coupling
    # formula onto H_s drops trace terms. It must disagree on the keystone.
    Hs = ((H11, 0, 0), (0, H22, 0), (0, 0, H33))
    Hs2 = tuple(
        tuple(sum(Hs[i][k] * Hs[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )
    g_Hs2_g = sum(g[i] * Hs2[i][j] * g[j] for i in range(3) for j in range(3))
    tr_Hs2 = Hs2[0][0] + Hs2[1][1] + Hs2[2][2]
    mirror_self = (2 * g_Hs2_g - q * tr_Hs2) / (2 * den)

    return {
        "q": q,
        "deltas": {
            "Delta_c": Delta_c,
            "Delta_s": Delta_s,
            "Delta_m": Delta_m,
        },
        "bordered_det": bordered,
        "delta_sum": delta_sum,
        "bordered_matches_partition": bordered == delta_sum,
        "channels": {
            "K_G": K_G,
            "kappa_c": kappa_c,
            "kappa_s": kappa_s,
            "kappa_int": kappa_int,
        },
        "mutation_traps": {
            "mirror_self_formula_caught": mirror_self != kappa_s,
            "drop_interaction_caught": kappa_int != 0 and (kappa_c + kappa_s) != K_G,
            "sign_blind_scalar_caught": K_G < 0,
        },
    }


def three_channel_referee(gradient, hessian) -> dict:
    """Exact n=3 channel referee with determinant partition metadata."""
    out = _channel_components(gradient, hessian)
    out["method"] = "three_channel_bordered_partition"
    return out


def gauge_channel_transport(gradient, hessian, gauge) -> dict:
    """Gauge action H -> H + g a^T + a g^T and exact channel movement."""
    g = _vec(gradient)
    H = _mat(hessian)
    a = _vec(gauge)
    if len(g) != 3 or len(a) != 3:
        raise ValueError("gauge-channel transport is n=3")
    moved_H = tuple(
        tuple(H[i][j] + g[i] * a[j] + a[i] * g[j] for j in range(3))
        for i in range(3)
    )
    base = _channel_components(g, H)
    moved = _channel_components(g, moved_H)
    delta_channels = {
        key: moved["channels"][key] - base["channels"][key]
        for key in ("kappa_c", "kappa_s", "kappa_int")
    }
    delta_channels["K_G"] = moved["channels"]["K_G"] - base["channels"]["K_G"]
    delta_channels["sum_channels"] = (
        delta_channels["kappa_c"]
        + delta_channels["kappa_s"]
        + delta_channels["kappa_int"]
    )

    offdiag = {(0, 1): H[0][1], (0, 2): H[0][2], (1, 2): H[1][2]}
    nonzero_edges = [edge for edge, value in offdiag.items() if value != 0]
    single_edge = None
    q2 = base["q"] * base["q"]
    if len(nonzero_edges) == 1:
        i, j = nonzero_edges[0]
        k = ({0, 1, 2} - {i, j}).pop()
        h = offdiag[(i, j)]
        single_edge = {
            "edge": (i, j),
            "endpoint_axes": (i, j),
            "opposite_axis": k,
            "endpoint_delta_kappa_c_per_t": Fraction(0),
            "opposite_delta_kappa_c_per_t": 4 * g[i] * g[j] * g[k] * h / q2,
        }

    edge_vector = (
        g[0] * H[1][2],
        g[1] * H[0][2],
        g[2] * H[0][1],
    )
    return {
        "base": base,
        "moved": moved,
        "gauge": a,
        "moved_hessian": moved_H,
        "delta": delta_channels,
        "K_invariant": delta_channels["K_G"] == 0,
        "zero_sum_channel_shift": delta_channels["sum_channels"] == 0,
        "coupling_edge_vector": edge_vector,
        "single_edge": single_edge,
    }


def _s1(j):
    a, b = j
    return (b, a)


def _t1(j):
    a, b = j
    return (1 / a, -b / a)


def _s2(j):
    a, b, A, B, C = j
    return (b, a, C, B, A)


def _t2(j):
    a, b, A, B, C = j
    return (
        1 / a,
        -b / a,
        -A / a**3,
        (A * b - a * B) / a**3,
        (-A * b * b + 2 * a * b * B - a * a * C) / a**3,
    )


def _s3(j):
    a, b, A, B, C, E, F, G, H = j
    return (b, a, C, B, A, H, G, F, E)


def _t3(j):
    a, b, A, B, C, E, F, G, H = j
    return (
        1 / a,
        -b / a,
        -A / a**3,
        (A * b - a * B) / a**3,
        (-A * b * b + 2 * a * b * B - a * a * C) / a**3,
        (3 * A * A - a * E) / a**5,
        (-3 * A * A * b + 3 * a * A * B + a * b * E - a * a * F) / a**5,
        (
            3 * A * A * b * b
            - 6 * a * A * B * b
            + a * a * A * C
            + 2 * a * a * B * B
            - a * b * b * E
            + 2 * a * a * b * F
            - a**3 * G
        )
        / a**5,
        (
            -3 * A * A * b**3
            + 9 * a * A * B * b * b
            - 3 * a * a * A * C * b
            - 6 * a * a * B * B * b
            + 3 * a**3 * B * C
            + a * b**3 * E
            - 3 * a * a * b * b * F
            + 3 * a**3 * b * G
            - a**4 * H
        )
        / a**5,
    )


def _first_projective_invariants(a: Fraction, b: Fraction) -> dict:
    e1 = 1 - a - b
    e2 = a * b - a - b
    e3 = a * b
    return {
        "I1": e1 * e2 / e3,
        "I2": e1**3 / e3,
        "Delta_n": (a - b) ** 2 * (a + 1) ** 2 * (b + 1) ** 2,
    }


def _exponent_orbit(m: Fraction, n: Fraction) -> tuple[tuple[Fraction, Fraction], ...]:
    return (
        (m, n),
        (n, m),
        (1 / m, -n / m),
        (-n / m, 1 / m),
        (-m / n, 1 / n),
        (1 / n, -m / n),
    )


def role_jet_orbit(order: int, jet, exponents=None) -> dict:
    """Exact active role-jet S3 orbit through order 3."""
    order = int(order)
    j = _vec(jet)
    expected_len = {1: 2, 2: 5, 3: 9}.get(order)
    if expected_len is None:
        raise ValueError("role-jet order must be 1, 2, or 3")
    if len(j) != expected_len:
        raise ValueError(f"order {order} role jet expects {expected_len} entries")
    s, t = {1: (_s1, _t1), 2: (_s2, _t2), 3: (_s3, _t3)}[order]
    st = lambda x: s(t(x))
    laws = {
        "s2": s(s(j)) == j,
        "t2": t(t(j)) == j,
        "st3": st(st(st(j))) == j,
    }

    seen: dict[tuple[Fraction, ...], str] = {j: "e"}
    queue = deque([j])
    while queue:
        cur = queue.popleft()
        for label, fn in (("s", s), ("t", t)):
            nxt = fn(cur)
            if nxt not in seen:
                seen[nxt] = seen[cur] + label
                queue.append(nxt)

    out = {
        "order": order,
        "input_jet": j,
        "orbit_size": len(seen),
        "orbit": [{"word": word, "jet": state} for state, word in seen.items()],
        "group_laws": laws,
        "first_projective_invariants": _first_projective_invariants(j[0], j[1]),
    }
    if exponents is not None:
        m, n = _vec(exponents)
        eorb = _exponent_orbit(m, n)
        out["exponent_orbit"] = eorb
        out["degree_spectrum"] = tuple(sorted(alpha + beta for alpha, beta in eorb))
    return out


def _graph_channels(alpha, beta, L, M, N) -> dict:
    q = 1 + alpha * alpha + beta * beta
    kappa_c = -M * M / (q * q)
    kappa_s = L * N / (q * q)
    kappa_int = Fraction(0)
    return {
        "K_G": kappa_c + kappa_s + kappa_int,
        "kappa_c": kappa_c,
        "kappa_s": kappa_s,
        "kappa_int": kappa_int,
    }


def curvature_orbit_spectrum(graph_jet) -> dict:
    """Six active ordered graph charts, collapsed to three output spectra."""
    a, b, A, B, C = _vec(graph_jet)
    charts = []

    def add(name, alpha, beta, L, M, N):
        charts.append({
            "name": name,
            "alpha": alpha,
            "beta": beta,
            "L": L,
            "M": M,
            "N": N,
            "spectrum": _graph_channels(alpha, beta, L, M, N),
        })

    add("P|D,S", a, b, A, B, C)
    add("P|S,D", b, a, C, B, A)

    alpha, beta = 1 / a, -b / a
    L = -A / a**3
    M = (A * b - a * B) / a**3
    N = (-A * b * b + 2 * a * b * B - a * a * C) / a**3
    add("D|P,S", alpha, beta, L, M, N)
    add("D|S,P", beta, alpha, N, M, L)

    alpha, beta = -a / b, 1 / b
    L = (-C * a * a + 2 * a * b * B - b * b * A) / b**3
    M = (C * a - b * B) / b**3
    N = -C / b**3
    add("S|D,P", alpha, beta, L, M, N)
    add("S|P,D", beta, alpha, N, M, L)

    output_spectra = {"P": charts[0]["spectrum"], "D": charts[2]["spectrum"], "S": charts[4]["spectrum"]}
    unique = {tuple(spec.items()) for spec in output_spectra.values()}
    totals = tuple(sorted({chart["spectrum"]["K_G"] for chart in charts}))
    return {
        "charts": charts,
        "output_spectra": output_spectra,
        "unique_output_spectrum_count": len(unique),
        "total_curvature_values": totals,
        "six_ordered_charts_collapse_to_three": charts[0]["spectrum"] == charts[1]["spectrum"]
        and charts[2]["spectrum"] == charts[3]["spectrum"]
        and charts[4]["spectrum"] == charts[5]["spectrum"],
    }


def _carrier_o_n3(g, H) -> tuple[Fraction, Fraction, Fraction]:
    return (
        H[0][1] - g[0] * H[1][1] / (2 * g[1]) - g[1] * H[0][0] / (2 * g[0]),
        H[0][2] - g[0] * H[2][2] / (2 * g[2]) - g[2] * H[0][0] / (2 * g[0]),
        H[1][2] - g[1] * H[2][2] / (2 * g[2]) - g[2] * H[1][1] / (2 * g[1]),
    )


def _hperp_from_o(O):
    O12, O13, O23 = O
    return ((0, O12, O13), (O12, 0, O23), (O13, O23, 0))


def _role_graph_densities(g, O, output_index: int) -> dict:
    H = _hperp_from_o(O)
    inputs = tuple(i for i in range(3) if i != output_index)
    i, j, k = inputs[0], inputs[1], output_index
    alpha = -g[i] / g[k]
    beta = -g[j] / g[k]
    L = -(H[i][i] + 2 * H[i][k] * alpha + H[k][k] * alpha * alpha) / g[k]
    M = -(H[i][j] + H[i][k] * beta + H[j][k] * alpha + H[k][k] * alpha * beta) / g[k]
    N = -(H[j][j] + 2 * H[j][k] * beta + H[k][k] * beta * beta) / g[k]
    q_chart = 1 + alpha * alpha + beta * beta
    return {
        "output_index": k,
        "input_indices": inputs,
        "q_chart": q_chart,
        "slopes": {"alpha": alpha, "beta": beta},
        "second": {"L": L, "M": M, "N": N},
        "r1": {
            "kappa_c_hat": -2 * alpha * beta * M,
            "kappa_s_hat": L * (1 + beta * beta) + N * (1 + alpha * alpha),
        },
        "r2": {
            "kappa_c_hat": -M * M,
            "kappa_s_hat": L * N,
            "kappa_int_hat": Fraction(0),
        },
    }


def rolechspec_n3(gradient, hessian=None, carrier=None) -> dict:
    """n=3 RoleChSpec density record with linear recovery of O."""
    g = _vec(gradient)
    if len(g) != 3 or any(x == 0 for x in g):
        raise ValueError("RoleChSpec n=3 requires all three gradient components nonzero")
    if carrier is None:
        if hessian is None:
            raise ValueError("provide either hessian or carrier")
        O = _carrier_o_n3(g, _mat(hessian))
    else:
        O = _vec(carrier)
        if len(O) != 3:
            raise ValueError("n=3 carrier must be [O12,O13,O23]")

    role_names = {0: "D", 1: "S", 2: "P"}
    charts = {role_names[k]: _role_graph_densities(g, O, k) for k in (0, 1, 2)}

    rows = []
    values = []
    for k in (0, 1, 2):
        values.append(charts[role_names[k]]["r1"]["kappa_c_hat"])
        row = []
        for basis in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            row.append(_role_graph_densities(g, tuple(Fraction(x) for x in basis), k)["r1"]["kappa_c_hat"])
        rows.append(tuple(row))
    recovery_det = _det(tuple(rows))
    recovered = _solve_square(tuple(rows), tuple(values))
    return {
        "carrier_O": O,
        "charts": charts,
        "recovery": {
            "source": "three r=1 coupling-density rows",
            "matrix": tuple(rows),
            "rhs": tuple(values),
            "determinant": recovery_det,
            "recovered_O": recovered,
            "matches_input_O": recovered == O,
        },
        "injectivity_certificate": {
            "regularity": "g1*g2*g3 != 0",
            "method": "linear rank-3 r=1 coupling minor; no Groebner basis",
        },
    }


def role_pair_loss_diagnostic(n: int) -> dict:
    """Role-pair carrier dimensions and loss status for S_n."""
    n = int(n)
    if n < 3:
        raise ValueError("role-pair carrier starts at n>=3")
    carrier_dim = comb(n, 2)
    chart_components = n * comb(n - 1, 2)
    shape_dim = n * (n - 3) // 2
    if n == 3:
        status = "absent"
        margin = 0
    elif n == 4:
        status = "quotient_S4_over_V4"
        margin = 0
    else:
        status = "faithful"
        margin = 2 * (n - 3)
    return {
        "n": n,
        "chart_view_components": chart_components,
        "carrier_dim": carrier_dim,
        "realizable_carrier": "M^(n-2,2) = Q[role-pairs] = triv + std + shape",
        "magnitude_summary": "triv + std",
        "magnitude_summary_dim": n,
        "shape_repr": f"S^({n - 2},2)" if n >= 4 else "none",
        "shape_dim": shape_dim,
        "shape_status": status,
        "faithfulness_margin": margin,
        "discarded_by_magnitude_summary": shape_dim,
    }


def shadow_law(n: int, gradient) -> dict:
    """Johnson shadow-law scalar for the coupling quadratic form."""
    n = int(n)
    g = _vec(gradient)
    if len(g) != n:
        raise ValueError("gradient length must equal n")
    if n < 3:
        raise ValueError("shadow law needs n>=3")
    if any(x == 0 for x in g):
        raise ValueError("shadow law requires nonzero gradient entries")
    g2 = tuple(x * x for x in g)
    en = Fraction(1)
    for x in g2:
        en *= x
    weights = {}
    total = Fraction(0)
    for S in combinations(range(n), 3):
        denom = Fraction(1)
        for m in range(n):
            if m not in S:
                denom *= g2[m]
        w = 1 / denom
        weights[_fmt_key(S)] = w
        total += w
    scalar = total / comb(n, 3)
    return {
        "n": n,
        "pair_count": comb(n, 2),
        "triangle_count": comb(n, 3),
        "triangle_weights": weights,
        "scalar_s": scalar,
        "scalar_formula": "e3(g^2)/(C(n,3)*e_n(g^2))",
        "direction_operator": "(n-2)*I - A1 on Johnson J(n,2)",
        "direction_eigenvalues": {
            "triv": -(n - 2),
            "std": 2,
            "shape": n,
        },
    }


def wreath_law(kind: str, m, k=None) -> dict:
    """Closed-form monodromy law for gcd layers and self-glue covers."""
    kind = str(kind)
    m = int(m)
    if m <= 0:
        raise ValueError("m must be positive")
    if kind == "trinomial_layer":
        if k is None:
            raise ValueError("trinomial_layer requires k")
        k = int(k)
        d = gcd(m, k)
        blocks = m // d
        return {
            "kind": kind,
            "m": m,
            "k": k,
            "gcd": d,
            "block_count": blocks,
            "within_block": f"C_{d}",
            "block_group": f"S_{blocks}",
            "group": f"C_{d} wr S_{blocks}",
            "degree": m,
            "order": (d ** blocks) * factorial(blocks),
            "endpoint": "cyclic" if k == 0 else ("symmetric" if d == 1 else "mixed"),
        }
    if kind == "self_glue_product":
        return {
            "kind": kind,
            "m": m,
            "group": f"C_{m} wr C_{m}",
            "degree": m * m,
            "order": m ** (m + 1),
            "reading": "pure-power product layers give cyclic wreaths",
        }
    if kind == "self_glue_directive":
        fm = factorial(m)
        return {
            "kind": kind,
            "m": m,
            "group": f"S_{m} wr S_{m}",
            "degree": m * m,
            "order": (fm ** m) * fm,
            "reading": "coprime directive trinomials give symmetric wreaths",
        }
    raise ValueError("kind must be trinomial_layer, self_glue_product, or self_glue_directive")
