"""Host-side task description; these identities are owned by the M2 wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class M2ContactProjectionTask:
    request_id: str
    model_path: Path
    slice_assignments: tuple[tuple[str, int], ...]
    sign_product: int = 1
    characteristic: int = 0
    incidence_ideal: str = "IX"
    rotating_ideal: str = "IZ"
    contact_component: str = "Ceven"
    target_generator: str = "delta"
    base_variables: tuple[str, ...] = ("M", "N1", "N2", "N3", "N4", "J")
    sheet_variables: tuple[str, ...] = ("u", "w1", "w2", "w3", "w4")

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request id must be non-empty")
        if not self.model_path.is_file():
            raise ValueError(f"M2 model does not exist: {self.model_path}")
        keys = tuple(key for key, _ in self.slice_assignments)
        if keys != ("N1", "N2", "N3", "N4"):
            raise ValueError("the first wrapper fixture requires ordered N1..N4 assignments")
        identifiers = (
            self.incidence_ideal,
            self.rotating_ideal,
            self.contact_component,
            self.target_generator,
            *self.base_variables,
            *self.sheet_variables,
        )
        if any(not identifier.replace("_", "").isalnum() for identifier in identifiers):
            raise ValueError("M2 bindings must be simple identifiers")


@dataclass(frozen=True, slots=True)
class M2GenericEliminationTask:
    """Arbitrary declared-ring elimination task lowered to Pathfinder IR.

    Generators are written in Pathfinder IR syntax (Python ``**`` powers);
    the wrapper owns the translation to M2 syntax at lifting time.
    """

    request_id: str
    variables: tuple[str, ...]
    weights: tuple[int, ...]
    generators: tuple[str, ...]
    eliminate_variables: tuple[str, ...]
    generic_denominator: str | None = None
    characteristic: int = 0
    monomial_order: str = "GRevLex"

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request id must be non-empty")
        if not self.variables or not self.generators or not self.eliminate_variables:
            raise ValueError("elimination task requires variables, generators, and targets")
        if len(self.weights) != len(self.variables):
            raise ValueError("weight vector must match the variable list")
        unknown = [v for v in self.eliminate_variables if v not in self.variables]
        if unknown:
            raise ValueError(f"eliminate variables outside the ring: {unknown}")


@dataclass(frozen=True, slots=True)
class M2DifferenceIdealPrimenessTask:
    """Rotating difference-ideal primeness through the Kummer route (P4)."""

    request_id: str
    model_path: Path
    difference_ideal: str = "IZ"
    difference_generator: str = "delta"
    rotation_variable: str = "J"
    characteristic: int = 0

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.model_path.is_file():
            raise ValueError("primeness task requires an id and existing M2 model")
        identifiers = (self.difference_ideal, self.difference_generator, self.rotation_variable)
        if any(not identifier.replace("_", "").isalnum() for identifier in identifiers):
            raise ValueError("M2 bindings must be simple identifiers")


@dataclass(frozen=True, slots=True)
class M2ContactOrbitTask:
    request_id: str
    model_path: Path
    characteristic: int = 0
    incidence_ideal: str = "IX"
    contact_function: str = "contactIdeal"
    sign_vectors: str = "epsilons"
    wall_function: str = "wallPolynomial"
    projection_function: str = "projectToBase"

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.model_path.is_file():
            raise ValueError("contact-orbit task requires an id and existing M2 model")
        identifiers = (
            self.incidence_ideal,
            self.contact_function,
            self.sign_vectors,
            self.wall_function,
            self.projection_function,
        )
        if any(not identifier.replace("_", "").isalnum() for identifier in identifiers):
            raise ValueError("M2 bindings must be simple identifiers")
