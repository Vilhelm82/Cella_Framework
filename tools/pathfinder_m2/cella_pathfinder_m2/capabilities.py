"""Advertised M2 host capabilities.

The wrapper declares which primitives the M2 host exposes and which
Pathfinder route contracts it can lift.  Pathfinder core never imports this;
the wrapper supplies capability names through the request context when a
route family requires them.
"""

from __future__ import annotations

SUPPORTED_M2_PRIMITIVES: tuple[str, ...] = (
    "polynomial_ring_declaration",
    "ideal_construction",
    "ideal_sum",
    "trim",
    "eliminate",
    "saturate",
    "gcd_univariate",
    "polynomial_remainder",
    "minimal_primes",
    "primary_decomposition",
    "is_prime",
    "codim_degree",
    "signed_contact_substitution",
    "linear_wall_solve",
    "sign_orbit_enumeration",
)


def advertised_capabilities() -> tuple[str, ...]:
    return SUPPORTED_M2_PRIMITIVES


def liftable_route_families() -> tuple[str, ...]:
    from .wrapper import LIFTERS

    return tuple(sorted(LIFTERS))
