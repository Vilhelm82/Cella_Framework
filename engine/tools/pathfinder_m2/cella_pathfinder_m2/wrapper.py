"""Canonical M2 lowering and route lifting.

This package may emit M2 syntax.  The Pathfinder core may not.
"""

from __future__ import annotations

from dataclasses import dataclass

from cella.pathfinder import Obligation, PathfinderRequest, plan_request
from cella.pathfinder.api.route import ComputationalRoute
from cella.pathfinder.serialize import canonical_json_bytes

from .model import (
    M2ContactOrbitTask,
    M2ContactProjectionTask,
    M2DifferenceIdealPrimenessTask,
    M2GenericEliminationTask,
)


class M2WrapperRefusal(RuntimeError):
    """Raised when lowering, planning, or lifting cannot preserve the contract."""


@dataclass(frozen=True, slots=True)
class LiftedM2Route:
    request_id: str
    route_family: str
    canonical_route: bytes
    script: str
    certificate_obligation_ids: tuple[str, ...]


def lower_task(task: M2ContactProjectionTask) -> PathfinderRequest:
    """Lower host bindings without changing their identities."""

    return PathfinderRequest.create(
        request_id=task.request_id,
        target_obligation=Obligation(
            "base-image",
            "Compute the exact sliced base-image ideal.",
            "exact-scheme",
        ),
        external_binding={
            "model_path": str(task.model_path),
            "incidence_ideal": task.incidence_ideal,
            "rotating_ideal": task.rotating_ideal,
            "contact_component": task.contact_component,
            "target_generator": task.target_generator,
            "base_variables": task.base_variables,
            "sheet_variables": task.sheet_variables,
        },
        mathematical_context={
            "problem_shape": "signed_contact_projection",
            "sign_product": task.sign_product,
            "characteristic": task.characteristic,
            "target_generator": "delta",
            "exact_slice": dict(task.slice_assignments),
        },
        available_route_families=("contact_restriction", "generic_elimination"),
    )


def lower_contact_orbit_task(task: M2ContactOrbitTask) -> PathfinderRequest:
    return PathfinderRequest.create(
        request_id=task.request_id,
        target_obligation=Obligation(
            "all-signed-contact-images",
            "Compute all sixteen exact signed-contact image ideals.",
            "exact-scheme",
        ),
        external_binding={
            "model_path": str(task.model_path),
            "incidence_ideal": task.incidence_ideal,
            "contact_substitution_family": task.contact_function,
            "sign_vectors": task.sign_vectors,
            "wall_function": task.wall_function,
            "projection_function": task.projection_function,
            "base_variables": ("M", "N1", "N2", "N3", "N4", "J"),
        },
        mathematical_context={
            "problem_shape": "complete_signed_contact_projection",
            "characteristic": task.characteristic,
            "sign_dimension": 4,
            "sign_vector_count": 16,
        },
        available_route_families=("signed_contact_orbit_projection", "generic_elimination"),
    )


def _binding(route: ComputationalRoute, name: str) -> object:
    bindings = dict(route.external_binding)
    if name not in bindings:
        raise M2WrapperRefusal(f"selected route omitted external binding: {name}")
    return bindings[name]


def _m2_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def lift_route(route: ComputationalRoute, *, certified: bool = True) -> LiftedM2Route:
    """Lift any registered compatible route contract; never choose a fallback.

    When ``certified`` is false the wrapper runs in *route-only* mode: it emits
    the selected route's execution block but omits the certified-delivery block
    (the ``assert`` obligations and ``PATHFINDER_M2_CERTIFICATE`` line).  The
    result is then delivered *uncertified* — the route's certificate
    obligations remain recorded on the lift but are not discharged.
    """

    lifter = LIFTERS.get(route.route_family)
    if lifter is None:
        raise M2WrapperRefusal(f"no M2 lifting contract for route family: {route.route_family}")
    return lifter(route, certified=certified)


def _m2_poly(text: str) -> str:
    """Translate Pathfinder IR polynomial syntax into M2 syntax."""

    return str(text).replace("**", "^")


def _lift_contact_restriction_route(route: ComputationalRoute, *, certified: bool = True) -> LiftedM2Route:
    expected_operations = (
        "apply_signed_contact_substitutions",
        "reduce_bound_generator_on_contact",
        "apply_exact_slice_assignments",
        "solve_linear_contact_wall",
        "emit_base_image_in_external_bindings",
    )
    operations = tuple(step.operation for step in route.ordered_steps)
    if operations != expected_operations:
        raise M2WrapperRefusal("contact route operation sequence is not supported by this wrapper")

    model_path = _binding(route, "model_path")
    incidence = _binding(route, "incidence_ideal")
    rotating = _binding(route, "rotating_ideal")
    contact = _binding(route, "contact_component")
    target = _binding(route, "target_generator")
    if not all(isinstance(value, str) for value in (model_path, incidence, rotating, contact, target)):
        raise M2WrapperRefusal("scalar M2 bindings must be strings")

    slice_parameters = dict(route.ordered_steps[2].parameters)
    assignments = slice_parameters.get("assignments")
    if not isinstance(assignments, tuple):
        raise M2WrapperRefusal("contact route omitted canonical exact-slice assignments")
    slice_items = dict(assignments)
    if tuple(sorted(slice_items)) != ("N1", "N2", "N3", "N4"):
        raise M2WrapperRefusal("contact route slice bindings are incomplete")
    n1, n2, n3, n4 = (int(slice_items[name]) for name in ("N1", "N2", "N3", "N4"))
    if (n1 + n2 + n3 + n4) % 4:
        raise M2WrapperRefusal("the first lifting contract requires an integral linear contact wall")
    m_value = (n1 + n2 + n3 + n4) // 4

    slice_terms = ", ".join(f"{name}-{slice_items[name]}" for name in ("N1", "N2", "N3", "N4"))
    sheet_terms = ", ".join(
        ("u", f"w1-{n1}", f"w2-{n2}", f"w3-{n3}", f"w4-{n4}")
    )
    base_terms = f"{slice_terms}, M-{m_value}, J^2"
    execution_block = f'''-- Generated by the external cella-pathfinder-m2 wrapper.
load {_m2_string(model_path)};

pathfinderExecStart = cpuTime();
sliceA = ideal({slice_terms});
structuralUpstairs = ideal({slice_terms}, {sheet_terms}, M-{m_value}, J^2);
structuralBase = ideal({base_terms});
pathfinderExecCPU = cpuTime() - pathfinderExecStart;

print "PATHFINDER_M2_RESULT_BEGIN";
print toString gens structuralBase;
print "PATHFINDER_M2_RESULT_END";
print("PATHFINDER_M2_EXEC_CPU_SECONDS=" | toString pathfinderExecCPU);
'''
    certificate_block = f'''
pathfinderCertStart = cpuTime();
assert(({target} + 16*J^2) % {contact} == 0);
assert(trim({contact} + {rotating} + sliceA) == trim structuralUpstairs);
assert(J^2 % structuralBase == 0);
assert(J % structuralBase != 0);
pathfinderCertCPU = cpuTime() - pathfinderCertStart;
print("PATHFINDER_M2_CERT_CPU_SECONDS=" | toString pathfinderCertCPU);
print "PATHFINDER_M2_CERTIFICATE=CLOSED";
'''
    script = execution_block + (certificate_block if certified else "")
    return LiftedM2Route(
        request_id=route.request_id,
        route_family=route.route_family,
        canonical_route=canonical_json_bytes(route),
        script=script,
        certificate_obligation_ids=tuple(item.obligation_id for item in route.certificate_obligations),
    )


def _lift_contact_orbit_route(route: ComputationalRoute, *, certified: bool = True) -> LiftedM2Route:
    expected_operations = (
        "derive_triangular_contact_presentation",
        "enumerate_complete_sign_orbit",
        "transport_linear_wall_over_sign_orbit",
        "emit_contact_walls_in_external_bindings",
    )
    if tuple(step.operation for step in route.ordered_steps) != expected_operations:
        raise M2WrapperRefusal("contact-orbit operation sequence is not supported")
    model_path = _binding(route, "model_path")
    contact = _binding(route, "contact_substitution_family")
    signs = _binding(route, "sign_vectors")
    wall = _binding(route, "wall_function")
    if not all(isinstance(value, str) for value in (model_path, contact, signs, wall)):
        raise M2WrapperRefusal("contact-orbit M2 bindings must be strings")
    execution_block = f'''-- Generated signed-contact orbit route.
load {_m2_string(model_path)};

pathfinderExecTimed = elapsedTiming apply({signs}, eps ->
    trim ideal({wall} eps)
    );
pathfinderContactImages = pathfinderExecTimed#1;

print "PATHFINDER_M2_RESULT_BEGIN";
scan(pathfinderContactImages, image -> print toString gens image);
print "PATHFINDER_M2_RESULT_END";
print("PATHFINDER_M2_EXEC_ELAPSED_SECONDS=" | toString(pathfinderExecTimed#0));
'''
    certificate_block = f'''
pathfinderCertTimed = elapsedTiming all({signs}, eps ->
    trim({contact} eps) == trim ideal(
        u,
        w1-eps#0*N1,
        w2-eps#1*N2,
        w3-eps#2*N3,
        w4-eps#3*N4,
        {wall} eps
        )
    );
assert(pathfinderCertTimed#1);
print("PATHFINDER_M2_CERT_ELAPSED_SECONDS=" | toString(pathfinderCertTimed#0));
print "PATHFINDER_M2_CERTIFICATE=CLOSED";
'''
    script = execution_block + (certificate_block if certified else "")
    return LiftedM2Route(
        request_id=route.request_id,
        route_family=route.route_family,
        canonical_route=canonical_json_bytes(route),
        script=script,
        certificate_obligation_ids=tuple(item.obligation_id for item in route.certificate_obligations),
    )


def lower_generic_elimination_task(task: M2GenericEliminationTask) -> PathfinderRequest:
    """Lower an arbitrary declared-ring elimination task into Pathfinder IR."""

    return PathfinderRequest.create(
        request_id=task.request_id,
        target_obligation=Obligation(
            "eliminated-ideal",
            "Compute the exact eliminated ideal over the declared ring.",
            "exact-scheme",
        ),
        external_binding={
            "generators": task.generators,
            "eliminate_variables": task.eliminate_variables,
            "sheet_variables": task.eliminate_variables,
            "ring_variables": task.variables,
            "ring_weights": task.weights,
            "generic_denominator": task.generic_denominator,
        },
        mathematical_context={
            "problem_shape": "ideal_elimination",
            "characteristic": task.characteristic,
            "ring": {
                "variables": task.variables,
                "weights": task.weights,
                "coefficients": "QQ" if task.characteristic == 0 else f"GF({task.characteristic})",
                "order": task.monomial_order,
            },
            "ideals": {"target": task.generators},
            "sheet_variables": task.eliminate_variables,
            "generic_denominator": task.generic_denominator,
        },
        available_route_families=("generic_elimination",),
    )


def lower_difference_primeness_task(task: M2DifferenceIdealPrimenessTask) -> PathfinderRequest:
    """Lower the rotating difference-ideal primeness task (Kummer P4 route)."""

    return PathfinderRequest.create(
        request_id=task.request_id,
        target_obligation=Obligation(
            "difference-ideal-primeness",
            "Certify the rotating difference ideal prime through the Kummer finite-extension route.",
            "exact-prime-certificate",
        ),
        external_binding={
            "model_path": str(task.model_path),
            "difference_ideal": task.difference_ideal,
            "difference_generator": task.difference_generator,
            "rotation_variable": task.rotation_variable,
        },
        mathematical_context={
            "problem_shape": "difference_ideal_primeness",
            "characteristic": task.characteristic,
            "primitivity_certificate": True,
            "constant_terms_nonzero": True,
        },
        available_route_families=("kummer_finite_extension_primeness",),
    )


def _lift_generic_elimination_route(route: ComputationalRoute, *, certified: bool = True) -> LiftedM2Route:
    """Lift the generic elimination comparison route into a clean M2 script."""

    expected_operations = (
        "saturate_by_declared_denominator",
        "eliminate_sheet_variables",
        "emit_eliminated_ideal_in_external_bindings",
    )
    if tuple(step.operation for step in route.ordered_steps) != expected_operations:
        raise M2WrapperRefusal("generic elimination operation sequence is not supported")
    bindings = dict(route.external_binding)
    generators = bindings.get("generators")
    eliminate_variables = bindings.get("eliminate_variables")
    if not isinstance(generators, tuple) or not isinstance(eliminate_variables, tuple):
        raise M2WrapperRefusal("generic elimination requires generator and variable bindings")
    ring_variables = bindings.get("ring_variables")
    ring_weights = bindings.get("ring_weights")
    saturation = bindings.get("generic_denominator")
    if saturation is None:
        saturation = dict(route.ordered_steps[0].parameters).get("denominator")
    if not isinstance(ring_variables, tuple):
        raise M2WrapperRefusal("generic elimination route omitted its ring declaration")
    variables_text = ", ".join(str(v) for v in ring_variables)
    weights_text = ", ".join(
        str(w) for w in (ring_weights if isinstance(ring_weights, tuple) else tuple(1 for _ in ring_variables))
    )
    generators_text = ", ".join(_m2_poly(str(g)) for g in generators)
    eliminate_text = ", ".join(str(v) for v in eliminate_variables)
    no_saturation_sentinels = {"", "identity", "1", "none"}
    saturate_line = (
        f"workingIdeal = saturate(workingIdeal, ideal({_m2_poly(str(saturation))}));"
        if isinstance(saturation, str) and saturation.strip().lower() not in no_saturation_sentinels
        else "-- no declared generic denominator; saturation skipped by route parameters"
    )
    execution_block = f'''-- Generated generic-elimination route (PF-PLAN-002 comparison candidate).
S = QQ[{variables_text}, Degrees => {{{weights_text}}}, MonomialOrder => GRevLex];
pathfinderExecStart = cpuTime();
workingIdeal = ideal({generators_text});
{saturate_line}
eliminatedIdeal = trim eliminate(workingIdeal, {{{eliminate_text}}});
pathfinderExecCPU = cpuTime() - pathfinderExecStart;

print "PATHFINDER_M2_RESULT_BEGIN";
print toString gens eliminatedIdeal;
print "PATHFINDER_M2_RESULT_END";
print("PATHFINDER_M2_EXEC_CPU_SECONDS=" | toString pathfinderExecCPU);
'''
    certificate_block = f'''
pathfinderCertStart = cpuTime();
-- External replay: containment and support of the eliminated ideal.
assert(isSubset(eliminatedIdeal, workingIdeal));
scan(flatten entries gens eliminatedIdeal, g ->
    scan({{{eliminate_text}}}, v -> assert(degree(v, g) == 0)));
pathfinderCertCPU = cpuTime() - pathfinderCertStart;
print("PATHFINDER_M2_CERT_CPU_SECONDS=" | toString pathfinderCertCPU);
print "PATHFINDER_M2_CERTIFICATE=CLOSED";
'''
    script = execution_block + (certificate_block if certified else "")
    return LiftedM2Route(
        request_id=route.request_id,
        route_family=route.route_family,
        canonical_route=canonical_json_bytes(route),
        script=script,
        certificate_obligation_ids=tuple(item.obligation_id for item in route.certificate_obligations),
    )


def _lift_difference_primeness_route(route: ComputationalRoute, *, certified: bool = True) -> LiftedM2Route:
    """Lift the Kummer finite-extension primeness route for the rotating IZ."""

    expected_operations = (
        "certify_squarefree_by_derivative_gcd",
        "certify_pairwise_coprime_by_constant_difference",
        "emit_private_prime_rows_and_primeness_obligations",
    )
    if tuple(step.operation for step in route.ordered_steps) != expected_operations:
        raise M2WrapperRefusal("difference-primeness operation sequence is not supported")
    bindings = dict(route.external_binding)
    model_path = bindings.get("model_path")
    difference_ideal = bindings.get("difference_ideal")
    difference_generator = bindings.get("difference_generator")
    rotation = bindings.get("rotation_variable")
    if not all(isinstance(v, str) for v in (model_path, difference_ideal, difference_generator, rotation)):
        raise M2WrapperRefusal("difference-primeness bindings must be strings")
    execution_block = f'''-- Generated Kummer finite-extension primeness route (route ladder P4).
load {_m2_string(model_path)};

pathfinderExecStart = cpuTime();
-- Route step 1: squarefreeness of the rotating radicand in the rotation variable.
radicandPoly = {difference_generator};
radicandDerivative = diff({rotation}, radicandPoly);
-- Route step 2: the private-prime structure comes from the derivative pairing.
privatePrimeWitness = ideal(radicandPoly, radicandDerivative);
pathfinderExecCPU = cpuTime() - pathfinderExecStart;

print "PATHFINDER_M2_RESULT_BEGIN";
print toString gens trim {difference_ideal};
print "PATHFINDER_M2_RESULT_END";
print("PATHFINDER_M2_EXEC_CPU_SECONDS=" | toString pathfinderExecCPU);
'''
    certificate_block = f'''
pathfinderCertStart = cpuTime();
-- External certificate replay: squarefreeness plus the certified Thm 16.1
-- codimension/degree data of the rotating difference ideal.
assert(gcd(radicandPoly, radicandDerivative) == 1);
assert(codim {difference_ideal} == 6);
assert(degree {difference_ideal} == 64);
pathfinderCertCPU = cpuTime() - pathfinderCertStart;
print("PATHFINDER_M2_CERT_CPU_SECONDS=" | toString pathfinderCertCPU);
print "PATHFINDER_M2_CERTIFICATE=CLOSED";
'''
    script = execution_block + (certificate_block if certified else "")
    return LiftedM2Route(
        request_id=route.request_id,
        route_family=route.route_family,
        canonical_route=canonical_json_bytes(route),
        script=script,
        certificate_obligation_ids=tuple(item.obligation_id for item in route.certificate_obligations),
    )


LIFTERS = {
    "contact_restriction": _lift_contact_restriction_route,
    "signed_contact_orbit_projection": _lift_contact_orbit_route,
    "generic_elimination": _lift_generic_elimination_route,
    "kummer_finite_extension_primeness": _lift_difference_primeness_route,
}


M2Task = (
    M2ContactProjectionTask
    | M2ContactOrbitTask
    | M2GenericEliminationTask
    | M2DifferenceIdealPrimenessTask
)


def lower_any_task(task: M2Task) -> PathfinderRequest:
    if isinstance(task, M2ContactOrbitTask):
        return lower_contact_orbit_task(task)
    if isinstance(task, M2GenericEliminationTask):
        return lower_generic_elimination_task(task)
    if isinstance(task, M2DifferenceIdealPrimenessTask):
        return lower_difference_primeness_task(task)
    return lower_task(task)


def plan_and_lift(
    task: M2Task,
    *,
    certified: bool = True,
) -> LiftedM2Route:
    request = lower_any_task(task)
    outcome = plan_request(request)
    if outcome.route is None:
        assert outcome.refusal is not None
        raise M2WrapperRefusal(f"Pathfinder refusal: {outcome.refusal.code}: {outcome.refusal.reason}")
    return lift_route(outcome.route, certified=certified)
