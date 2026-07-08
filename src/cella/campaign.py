"""Paper-native R&D campaign tools for Cella.

These helpers package the repeated proof moves from the LEAD7 and PFC papers
into small exact records. They are deliberately formula-level: the point is to
avoid assembling global scalar-curvature monsters when a local germ, support
polytope, or proof-obligation table already carries the campaign decision.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations

from .proofs import shifted_polynomial_certificate, sturm_positive_on_open_ray


def _q(value) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("booleans are not exact rationals")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value.strip())
    raise TypeError(f"expected exact rational string/integer, got {type(value).__name__}")


def _maybe_q(value):
    if isinstance(value, bool):
        raise TypeError("booleans are not valid symbolic scalars")
    if isinstance(value, int) or isinstance(value, Fraction):
        return Fraction(value)
    if isinstance(value, str):
        s = value.strip()
        try:
            return Fraction(s)
        except ValueError:
            return s
    return str(value)


def _fraction_text(value: Fraction) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _scalar_text(value) -> str:
    if isinstance(value, Fraction):
        return _fraction_text(value)
    return str(value)


def _over_text(numerator, denominator) -> str:
    denominator = _scalar_text(denominator)
    numerator = _scalar_text(numerator)
    if denominator == "1":
        return numerator
    return f"{numerator}/({denominator})"


def _sum_terms(terms: list[str]) -> str:
    if not terms:
        return "0"
    return " + ".join(terms)


def diag_germ_classifier(coordinate: str, native: dict, transverse: list[dict]) -> dict:
    """Classify a diagonal local metric germ by PFC/LEAD7 normal forms."""
    if not transverse:
        raise ValueError("at least one transverse channel is required")
    coordinate = str(coordinate)
    native_power = _q(native.get("power"))
    native_leading = _maybe_q(native.get("leading", "B"))
    native_parity = str(native.get("parity", "")).lower()
    powers = [_q(t.get("power", "0")) for t in transverse]
    parities = [str(t.get("parity", native_parity)).lower() for t in transverse]

    if native_power == 2 and all(p == -2 for p in powers) and native_parity == "even" and all(p == "even" for p in parities):
        m = len(transverse)
        coeff_num = Fraction(-m * (m + 5))
        coefficient = coeff_num / native_leading if isinstance(native_leading, Fraction) else None
        return {
            "kind": "parity_fixed",
            "coordinate": coordinate,
            "m": Fraction(m),
            "order": Fraction(4),
            "coefficient": coefficient,
            "coefficient_text": _over_text(coeff_num, native_leading),
            "law": "R = -m(m+5)/B * x^-4 + O(x^-2)",
            "proof_obligations": (
                "native component has even quadratic collapse",
                "all transverse channels have x^-2 leading poles",
                "all components are even in the boundary coordinate",
                "B and transverse leading units are nonzero on the stratum",
            ),
            "sympy_killer": "read coefficient from local germ; do not expand global curvature",
        }

    generic_ready = native_power == 2 and all(p == 0 for p in powers) and all("P0" in t and "P1" in t for t in transverse)
    if generic_ready:
        A = native_leading
        drift_terms = [f"{t['P1']}/{t['P0']}" for t in transverse]
        coefficient_text = f"({_sum_terms(drift_terms)})/({_scalar_text(A)})"
        coefficient = None
        try:
            drift = sum(_q(t["P1"]) / _q(t["P0"]) for t in transverse)
            if isinstance(A, Fraction):
                coefficient = drift / A
                coefficient_text = _fraction_text(coefficient)
        except (TypeError, ValueError, ZeroDivisionError):
            pass
        return {
            "kind": "generic_quadratic",
            "coordinate": coordinate,
            "m": Fraction(len(transverse)),
            "order": Fraction(3),
            "coefficient": coefficient,
            "coefficient_text": coefficient_text,
            "law": "R = (1/A) * sum(P_a1/P_a0) * x^-3 + O(x^-2)",
            "proof_obligations": (
                "native component has quadratic collapse",
                "transverse channels have finite nonzero leading values",
                "at least one transverse first drift is nonzero for exact order 3",
            ),
            "sympy_killer": "read odd pole from transverse first drift",
        }

    if native_power == 2 and all(p == 0 for p in powers):
        return {
            "kind": "flat_collapsing_only",
            "coordinate": coordinate,
            "order": Fraction(0),
            "coefficient": Fraction(0),
            "coefficient_text": "0",
            "law": "Bx^2 dx^2 with finite flat transverse channels is curvature-flat at leading order",
            "proof_obligations": ("transverse channels do not carry x^-2 poles",),
            "sympy_killer": "reject false reflection claims from metric collapse alone",
        }

    return {
        "kind": "unsupported_germ",
        "coordinate": coordinate,
        "order": None,
        "coefficient": None,
        "coefficient_text": None,
        "law": None,
        "native_power": native_power,
        "transverse_powers": tuple(powers),
        "proof_obligations": ("derive a new local normal form or reduce to a supported germ",),
    }


def role_divisor_retrodict(divisors: list[dict], expected_orders: dict | None = None) -> dict:
    """Build a complementarity retrodiction table from classified local germs."""
    table = []
    for item in divisors:
        classifier = dict(item.get("classifier", {}))
        order = item.get("order", classifier.get("order"))
        coefficient = item.get("coefficient", classifier.get("coefficient_text"))
        row = {
            "divisor": str(item["name"]),
            "local_type": classifier.get("kind", item.get("type", "declared")),
            "coordinate": classifier.get("coordinate", item.get("coordinate")),
            "order": order,
            "coefficient": coefficient,
            "law": classifier.get("law", item.get("law")),
            "proof_obligations": classifier.get("proof_obligations", ()),
        }
        table.append(row)
    expected_orders = expected_orders or {}
    comparisons = {}
    for row in table:
        name = row["divisor"]
        if name in expected_orders:
            comparisons[name] = _q(row["order"]) == _q(expected_orders[name])
    return {
        "table": table,
        "order_signature": tuple(row["order"] for row in table),
        "expected_orders": {str(k): _q(v) for k, v in expected_orders.items()},
        "order_checks": comparisons,
        "orders_match_expected": all(comparisons.values()) if comparisons else None,
        "method": "local_germ_retrodiction_table",
    }


def _support_order(vertices: dict, ax: Fraction, ay: Fraction) -> tuple[Fraction, tuple[str, ...], dict]:
    orders = {}
    for name, record in vertices.items():
        if not record.get("active", False):
            continue
        u, v = record["exponent"]
        orders[name] = -(u * ax + v * ay)
    if not orders:
        return Fraction(0), (), {}
    best = max(orders.values())
    active = tuple(name for name, value in orders.items() if value == best)
    return best, active, orders


def _corner_from_face_data(face_data: dict) -> dict:
    p_x = _q(face_data["p_x"])
    p_y = _q(face_data["p_y"])
    r_x = _q(face_data["r_x"])
    r_y = _q(face_data["r_y"])
    vertices = {
        "Vx": {"exponent": (-p_x, r_y), "coefficient": None},
        "Vy": {"exponent": (r_x, -p_y), "coefficient": None},
    }
    for item in vertices.values():
        u, v = item["exponent"]
        item["polar"] = (u < 0 or v < 0)
        item["active"] = item["polar"]
    denom = p_x + r_x
    balanced = (p_y + r_y) / denom if denom else None
    return vertices, {
        "p_x": p_x,
        "p_y": p_y,
        "r_x": r_x,
        "r_y": r_y,
        "balanced_direction": {"ax_over_ay": balanced},
        "cancellation": {},
    }


def _corner_from_weights(weights: dict) -> tuple[dict, dict]:
    p0, q0 = _q(weights["p0"]), _q(weights["q0"])
    p1, q1 = _q(weights["p1"]), _q(weights["q1"])
    p2, q2 = _q(weights["p2"]), _q(weights["q2"])
    A = -p0 * p0 + p0 * p1 - p0 * p2 + 2 * p0 + p1 * p2 - p2 * p2 + 2 * p2
    B = -q0 * q0 - q0 * q1 + q0 * q2 + 2 * q0 - q1 * q1 + q1 * q2 + 2 * q1
    vertices = {
        "V1": {"exponent": (-(p1 + 2), -q1), "coefficient": A},
        "V2": {"exponent": (-p2, -(q2 + 2)), "coefficient": B},
        "V0": {"exponent": (-p0, -q0), "coefficient": None},
    }
    for name, item in vertices.items():
        u, v = item["exponent"]
        item["polar"] = (u < 0 or v < 0)
        if name == "V0":
            item["active"] = item["polar"]
        else:
            item["active"] = item["polar"] and item["coefficient"] != 0
    p_x, p_y = p1 + 2, q2 + 2
    r_x, r_y = -p2, -q1
    denom = p_x + r_x
    balanced = (p_y + r_y) / denom if denom else None
    return vertices, {
        "p_x": p_x,
        "p_y": p_y,
        "r_x": r_x,
        "r_y": r_y,
        "balanced_direction": {"ax_over_ay": balanced},
        "cancellation": {"A": A, "B": B, "V0": "s-jet"},
    }


def corner_frontface(
    face_data: dict | None = None,
    weights: dict | None = None,
    path: dict | None = None,
) -> dict:
    """Codimension-2 corner workbench: support, balanced ray, and cancellation."""
    if (face_data is None) == (weights is None):
        raise ValueError("provide exactly one of face_data or weights")
    if face_data is not None:
        vertices, meta = _corner_from_face_data(face_data)
        input_kind = "face_data"
    else:
        vertices, meta = _corner_from_weights(weights)
        input_kind = "weights"
    path_record = None
    support_order = None
    support_terms = {}
    active_support = ()
    if path is not None:
        ax = _q(path["ax"])
        ay = _q(path["ay"])
        support_order, active_support, support_terms = _support_order(vertices, ax, ay)
        path_record = {"ax": ax, "ay": ay}
    active_vertices = tuple(name for name, item in vertices.items() if item["active"])
    return {
        "input_kind": input_kind,
        "vertices": vertices,
        "active_vertices": active_vertices,
        "face_data": {
            "p_x": meta["p_x"],
            "p_y": meta["p_y"],
            "r_x": meta["r_x"],
            "r_y": meta["r_y"],
        },
        "balanced_direction": meta["balanced_direction"],
        "cancellation": meta["cancellation"],
        "path": path_record,
        "support_terms": support_terms,
        "support_order": support_order,
        "active_frontface": active_support,
        "method": "corner_support_function_frontface_certificate",
    }


def positive_factor_certificate(variables: list, factors: list[dict]) -> dict:
    """Compose coefficient-shift and Sturm positivity certificates."""
    if not factors:
        raise ValueError("at least one factor is required")
    variables = tuple(str(v) for v in variables)
    out = {}
    for factor in factors:
        name = str(factor["name"])
        method = str(factor.get("method", "coefficient_shift"))
        terms = [( _q(coeff), tuple(int(p) for p in powers)) for coeff, powers in factor["terms"]]
        if method == "coefficient_shift":
            cert = shifted_polynomial_certificate(variables, terms, factor.get("shifts"))
        elif method == "sturm_open_ray":
            if len(variables) != 1:
                raise ValueError("sturm_open_ray factors must be univariate")
            cert = sturm_positive_on_open_ray(variables[0], terms, factor["lower"])
            if "sample" in factor:
                sample = _q(factor["sample"])
                # The underlying cert already samples at lower+1; record the
                # campaign-declared sample as a reproducibility hook.
                cert = dict(cert)
                cert["declared_sample"] = sample
        else:
            raise ValueError(f"unknown positivity method {method!r}")
        cert = dict(cert)
        cert["method"] = cert.get("method", method)
        cert["input_method"] = method
        out[name] = cert
    return {
        "variables": variables,
        "factors": out,
        "positive": all(bool(cert.get("positive")) for cert in out.values()),
        "method": "factorwise_positivity_composer",
    }


def metric_candidate_selector(candidates: list[dict]) -> dict:
    """Select DBP metric candidates by campaign canonicity gates."""
    if not candidates:
        raise ValueError("at least one candidate is required")
    results = {}
    selected = []
    for candidate in candidates:
        name = str(candidate["name"])
        reasons = []
        if not candidate.get("n2_reduction", False):
            reasons.append("fails_n2_reduction")
        if not candidate.get("positive_definite", False):
            reasons.append("loses_positive_definiteness")
        if not candidate.get("role_boundary_sensitive", False):
            reasons.append("hides_role_boundary_poles")
        if not candidate.get("interior_pole_free", False):
            reasons.append("interior_channel_isotropy_pole")
        if candidate.get("graph_norm") is False:
            reasons.append("graph_norm_missing")
        decision = "selected" if not reasons else "rejected"
        if decision == "selected":
            selected.append(name)
        results[name] = {
            "decision": decision,
            "reasons": tuple(reasons),
            "gates": {
                "n2_reduction": bool(candidate.get("n2_reduction", False)),
                "positive_definite": bool(candidate.get("positive_definite", False)),
                "role_boundary_sensitive": bool(candidate.get("role_boundary_sensitive", False)),
                "interior_pole_free": bool(candidate.get("interior_pole_free", False)),
                "graph_norm": candidate.get("graph_norm"),
            },
        }
    return {
        "selected": selected[0] if len(selected) == 1 else None,
        "selected_candidates": tuple(selected),
        "candidate_results": results,
        "unique_selection": len(selected) == 1,
        "method": "dbp_metric_candidate_gate_selector",
    }


def kn_metric_builder(
    roles: list[str] | None = None,
    assembly: str = "mass_role_inverse_sum",
    graph_norm: bool = True,
    u="0",
) -> dict:
    """Return the paper-native KN metric construction record."""
    roles = tuple(roles or ("S", "J", "Q"))
    if set(roles) != {"S", "J", "Q"}:
        raise ValueError("the KN builder currently supports roles ['S','J','Q']")
    assembly = str(assembly)
    u_q = _q(u)
    selected = assembly == "mass_role_inverse_sum" and graph_norm and u_q == 0
    warnings = []
    if not graph_norm:
        warnings.append("graph_norm_missing_changes_extremal_coefficient")
    if u_q != 0:
        warnings.append("role_role_weight_creates_or_tests_channel_isotropy_strata")
    if assembly != "mass_role_inverse_sum":
        warnings.append("assembly_is_not_the_selected_LEAD7_metric")
    return {
        "surface": "Kerr-Newman",
        "roles": roles,
        "U": "S/(4*pi) + pi*J^2/S + Q^2/2 + pi*Q^4/(4*S)",
        "selected_metric": "g_F(u=0)" if selected else "candidate_metric",
        "assembly": assembly,
        "graph_norm": bool(graph_norm),
        "u": u_q,
        "role_divisors": {"T": "U_S=0", "Omega": "J=0", "Phi_e": "Q=0"},
        "couplings": {
            "mass_role": "Lambda_{i,{M,a}} = 2M*(U_ii*U_a - U_i*U_ia)/U_i^3",
            "role_role": "Lambda_{i,{a,b}} = -D_{i,{a,b}}/U_i^3",
        },
        "components": {
            "G_i": {
                "formula": "(U_i^2 + 4U + U_a^2 + U_b^2)^2 * U_i^2/(4U) * (1/D_{i,a}^2 + 1/D_{i,b}^2)",
                "normalization": "q_i = (U_i^2 + 4U + U_a^2 + U_b^2)/U_i^2",
            }
        },
        "expected_retrodiction": {
            "T=0": {"local_type": "generic_quadratic", "order": Fraction(3)},
            "Omega=0": {"local_type": "parity_fixed", "order": Fraction(4), "coefficient": "-14/B_J"},
            "Phi_e=0": {"local_type": "parity_fixed", "order": Fraction(4), "coefficient": "-14/B_Q"},
            "Omega=Phi_e=0": {"local_type": "double_corner", "wedge": "max(4a-2,4-2a)", "minimum_order": Fraction(2)},
        },
        "warnings": tuple(warnings),
        "method": "LEAD7_graph_normalized_mass_role_inverse_channel_metric",
    }


def _det(matrix: list[list[Fraction]]) -> Fraction:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("determinant needs a square matrix")
    total = Fraction(0)
    for perm in permutations(range(n)):
        inv = 0
        prod = Fraction(1)
        for i, j in enumerate(perm):
            prod *= matrix[i][j]
            for k in range(i + 1, n):
                if perm[i] > perm[k]:
                    inv += 1
        total += (-prod if inv % 2 else prod)
    return total


def implicit_gaussian_curvature(gradient: list, hessian: list[list]) -> dict:
    """Exact bordered-Hessian Gaussian curvature for an implicit surface in R^3."""
    g = tuple(_q(x) for x in gradient)
    if len(g) != 3:
        raise ValueError("implicit Gaussian curvature referee currently supports R^3")
    H = tuple(tuple(_q(x) for x in row) for row in hessian)
    if len(H) != 3 or any(len(row) != 3 for row in H):
        raise ValueError("hessian must be 3 by 3")
    if any(H[i][j] != H[j][i] for i in range(3) for j in range(3)):
        raise ValueError("hessian must be symmetric")
    q = sum(x * x for x in g)
    if q == 0:
        raise ValueError("gradient is singular")
    bordered = [
        [H[0][0], H[0][1], H[0][2], g[0]],
        [H[1][0], H[1][1], H[1][2], g[1]],
        [H[2][0], H[2][1], H[2][2], g[2]],
        [g[0], g[1], g[2], Fraction(0)],
    ]
    det_bh = _det(bordered)
    return {
        "gradient": g,
        "hessian": H,
        "gradient_norm_squared": q,
        "bordered_hessian_det": det_bh,
        "K_G": -det_bh / (q * q),
        "method": "bordered_hessian_implicit_surface",
        "formula": "K = -det([[H,grad],[grad^T,0]]) / |grad|^4",
    }
