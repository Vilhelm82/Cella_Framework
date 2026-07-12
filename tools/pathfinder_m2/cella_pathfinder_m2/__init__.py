"""External Macaulay2 adapter for the Cella Pathfinder route core."""

from .capabilities import advertised_capabilities, liftable_route_families
from .model import (
    M2ContactOrbitTask,
    M2ContactProjectionTask,
    M2DifferenceIdealPrimenessTask,
    M2GenericEliminationTask,
)
from .wrapper import (
    LiftedM2Route,
    lower_any_task,
    lower_contact_orbit_task,
    lower_difference_primeness_task,
    lower_generic_elimination_task,
    lower_task,
    plan_and_lift,
)

__all__ = [
    "LiftedM2Route",
    "M2ContactOrbitTask",
    "M2ContactProjectionTask",
    "M2DifferenceIdealPrimenessTask",
    "M2GenericEliminationTask",
    "advertised_capabilities",
    "liftable_route_families",
    "lower_any_task",
    "lower_contact_orbit_task",
    "lower_difference_primeness_task",
    "lower_generic_elimination_task",
    "lower_task",
    "plan_and_lift",
]
