"""Bounded, non-verdict-bearing route-discovery scouts.

Every scout returns ScoutEvidence or None (evidence unavailable).  Scouts
never compute the host's deliverable, never cache a final answer, and never
emit a fabricated runtime prediction.
"""

from .protocol import Scout, run_scouts, scout_evidence
from .f2 import f2_kernel_basis, f2_orbit_rank, f2_rank
from .algebra import (
    degree_balance_scout,
    fresh_variable_monic_scout,
    self_glue_trinomial_scout,
    sign_orbit_scout,
    triangular_tower_scout,
)
from .expression import expression_shape_scout
from .inertia import congruence_inertia, exact_inertia_scout
from .kummer import parity_matrix_scout
from .newton import newton_corner_scout, support_function, vertex_coefficient
from .regularity import regularity_scout
from .sturm import sturm_chain, sturm_root_count, sturm_scout

__all__ = [
    "Scout",
    "congruence_inertia",
    "degree_balance_scout",
    "exact_inertia_scout",
    "expression_shape_scout",
    "f2_kernel_basis",
    "f2_orbit_rank",
    "f2_rank",
    "fresh_variable_monic_scout",
    "newton_corner_scout",
    "parity_matrix_scout",
    "regularity_scout",
    "run_scouts",
    "scout_evidence",
    "self_glue_trinomial_scout",
    "sign_orbit_scout",
    "sturm_chain",
    "sturm_root_count",
    "sturm_scout",
    "support_function",
    "triangular_tower_scout",
    "vertex_coefficient",
]
