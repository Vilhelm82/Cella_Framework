"""Native structural-algebra scouts over the bounded polynomial shadow."""

from __future__ import annotations

from math import gcd

from ..ir.expression import ExpressionShadowUnavailable
from ..ir.polynomial import PolynomialShadow, shadow_polynomial
from ..ir.problem import NormalizedProblem
from ..ir.scope import AnalysisBudget
from ..ir.evidence import ScoutEvidence
from .protocol import scout_evidence


def _shadow_ideal(
    problem: NormalizedProblem,
    ideal_name: str,
    budget: AnalysisBudget,
) -> tuple[PolynomialShadow, ...] | None:
    if problem.ring is None:
        return None
    ideal = problem.ideal(ideal_name)
    if ideal is None:
        return None
    try:
        return tuple(
            shadow_polynomial(
                generator,
                problem.ring.variables,
                max_nodes=budget.max_expression_nodes,
            )
            for generator in ideal.generators
        )
    except ExpressionShadowUnavailable:
        return None


def fresh_variable_monic_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
    *,
    ideal_name: str = "target",
) -> ScoutEvidence | None:
    """Detect the fresh-variable monic regular-sequence pattern (v1.3 §11.7).

    Order the generators so each is monic in a variable absent from every
    earlier generator.  A monic polynomial in a fresh variable is a
    non-zero-divisor over any coefficient ring, so the sequence is regular
    without a domain assumption; this is checkable syntactically.
    """

    shadows = _shadow_ideal(problem, ideal_name, budget)
    if shadows is None:
        return None
    field_coefficients = problem.ring is not None and problem.ring.coefficient_domain in {
        "QQ",
        "Q",
    } or (problem.ring is not None and problem.ring.coefficient_domain.startswith("GF("))

    remaining = list(range(len(shadows)))
    order: list[int] = []
    fresh_variables: list[str] = []
    ring_safe = True
    seen: set[str] = set()
    operations = 0
    while remaining:
        chosen = None
        for position in remaining:
            shadow = shadows[position]
            for variable in shadow.variables_used():
                operations += 1
                if variable in seen:
                    continue
                others_used = set(seen)
                for other in remaining:
                    if other != position:
                        others_used.update(shadows[other].variables_used())
                if variable in others_used:
                    continue
                if shadow.is_monic_in(variable):
                    chosen = (position, variable, True)
                    break
                if field_coefficients and shadow.has_unit_leading_in(variable):
                    chosen = (position, variable, False)
                    break
            if chosen is not None:
                break
        if chosen is None:
            break
        position, variable, monic = chosen
        ring_safe = ring_safe and monic
        order.append(position)
        fresh_variables.append(variable)
        seen.update(shadows[position].variables_used())
        remaining.remove(position)

    complete = not remaining
    return scout_evidence(
        scout_family="fresh_variable_monic",
        problem=problem,
        fingerprint={
            "ideal": ideal_name,
            "generator_count": len(shadows),
            "regular_sequence_certified": complete,
            "ring_safe_monic": complete and ring_safe,
            "field_unit_leading_only": complete and not ring_safe,
            "certified_prefix_length": len(order),
            "fresh_variables": tuple(fresh_variables),
            "sequence_order": tuple(order),
        },
        trace=(
            f"fresh-variable monic scan over {len(shadows)} generators",
            f"certified prefix length {len(order)}",
        ),
        stability="exact" if complete else "conditional",
        scout_operations=operations,
    )


def triangular_tower_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
    *,
    ideal_name: str = "target",
) -> ScoutEvidence | None:
    """Detect a triangular tower: an order where each generator introduces
    exactly one new variable relative to the earlier ones."""

    shadows = _shadow_ideal(problem, ideal_name, budget)
    if shadows is None:
        return None
    remaining = list(range(len(shadows)))
    introduced: list[tuple[int, str]] = []
    seen: set[str] = set()
    operations = 0
    # Seed with base variables that appear in every generator's coefficients:
    # the tower property is relative to the smallest generator's variables.
    while remaining:
        chosen = None
        for position in remaining:
            operations += 1
            new_variables = [v for v in shadows[position].variables_used() if v not in seen]
            if len(new_variables) == 1:
                chosen = (position, new_variables[0])
                break
            if not new_variables:
                chosen = (position, "")
                break
        if chosen is None:
            # allow the first pick to seed several base variables at once
            if not introduced and remaining:
                position = remaining[0]
                seen.update(shadows[position].variables_used())
                introduced.append((position, ""))
                remaining.remove(position)
                continue
            break
        position, variable = chosen
        if variable:
            seen.add(variable)
        seen.update(shadows[position].variables_used())
        introduced.append((position, variable))
        remaining.remove(position)

    complete = not remaining
    monic_steps = sum(
        1
        for position, variable in introduced
        if variable and shadows[position].is_monic_in(variable)
    )
    return scout_evidence(
        scout_family="triangular_tower",
        problem=problem,
        fingerprint={
            "ideal": ideal_name,
            "triangular": complete,
            "tower_order": tuple(position for position, _ in introduced),
            "introduced_variables": tuple(variable for _, variable in introduced),
            "monic_step_count": monic_steps,
            "generator_count": len(shadows),
        },
        trace=(f"triangular tower scan over {len(shadows)} generators",),
        stability="exact" if complete else "conditional",
        scout_operations=operations,
    )


def degree_balance_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
    *,
    ideal_name: str = "target",
) -> ScoutEvidence | None:
    """Exact weighted-degree bookkeeping for the CI degree route (v1.3 §12.2).

    For a certified regular sequence, the complete-intersection degree is the
    product of the generators' weighted degrees.  The scout computes that
    product exactly; comparing it against candidate components stays external.
    """

    if problem.ring is None:
        return None
    shadows = _shadow_ideal(problem, ideal_name, budget)
    if shadows is None:
        return None
    weights = problem.ring.weight_vector()
    degrees = tuple(shadow.weighted_degree(weights) for shadow in shadows)
    product = 1
    for degree in degrees:
        product *= max(degree, 1)
    return scout_evidence(
        scout_family="degree_balance",
        problem=problem,
        fingerprint={
            "ideal": ideal_name,
            "weighted_degrees": degrees,
            "complete_intersection_degree": product,
            "weights": weights,
        },
        trace=(f"weighted degrees {degrees}; CI product {product}",),
        stability="exact",
        scout_operations=len(shadows),
    )


def sign_orbit_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
) -> ScoutEvidence | None:
    """Verify a declared sign orbit is the complete {+1,-1}^k set."""

    symmetry = problem.symmetry
    if symmetry is None or symmetry.kind != "sign_orbit":
        return None
    detail = dict(symmetry.detail)
    vectors = detail.get("sign_vectors")
    if not isinstance(vectors, tuple):
        return None
    seen: set[tuple[int, ...]] = set()
    dimension: int | None = None
    for vector in vectors:
        if not isinstance(vector, tuple) or not all(isinstance(s, int) and s in (-1, 1) for s in vector):
            return None
        if dimension is None:
            dimension = len(vector)
        if len(vector) != dimension:
            return None
        seen.add(tuple(int(s) for s in vector))
    complete = dimension is not None and len(seen) == 2 ** dimension and len(vectors) == len(seen)
    return scout_evidence(
        scout_family="sign_orbit",
        problem=problem,
        fingerprint={
            "dimension": dimension or 0,
            "declared_count": len(vectors),
            "distinct_count": len(seen),
            "complete_orbit": complete,
        },
        trace=(f"sign orbit: {len(seen)} distinct of expected {2 ** (dimension or 0)}",),
        stability="exact",
        scout_operations=len(vectors) or 1,
    )


def self_glue_trinomial_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
    *,
    ideal_name: str = "target",
) -> ScoutEvidence | None:
    """Recognize the self-glue layer x^m + s*x^k - c and compute d = gcd(m,k).

    The candidate geometric layer structure is C_d wr S_(m/d) subject to the
    separability/coprimality/base-field hypotheses of the selected theorem
    (v1.3 §15.4); the scout records exponent structure only.
    """

    shadows = _shadow_ideal(problem, ideal_name, budget)
    if shadows is None or len(shadows) != 1:
        return None
    shadow = shadows[0]
    used = shadow.variables_used()
    if len(used) != 1:
        return None
    variable = used[0]
    index = shadow.variables.index(variable)
    exponents = sorted({monomial[index] for monomial, _ in shadow.terms}, reverse=True)
    if len(exponents) != 3 or exponents[-1] != 0:
        return None
    m, k = exponents[0], exponents[1]
    d = gcd(m, k)
    return scout_evidence(
        scout_family="self_glue_trinomial",
        problem=problem,
        fingerprint={
            "variable": variable,
            "m": m,
            "k": k,
            "gcd": d,
            "layer_candidate": f"C_{d} wr S_{m // d}",
            "pure_power": k == 0,
            "coprime": d == 1,
        },
        trace=(f"trinomial exponents ({m},{k},0), gcd {d}",),
        stability="exact",
        scout_operations=len(shadow.terms),
    )
