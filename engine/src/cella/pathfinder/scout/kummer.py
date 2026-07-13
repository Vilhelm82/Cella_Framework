"""Kummer parity-matrix scout: exact F2 rank evidence (Thm 4.1 mechanism).

Full column rank of a valuation-parity matrix is the route evidence for the
square-class independence and wreath-lift families.  The rank itself never
certifies the mathematical claim; the certificate obligations (regularity,
unramifiedness, odd-valuation preservation) stay external.
"""

from __future__ import annotations

from ..ir.problem import NormalizedProblem
from ..ir.scope import AnalysisBudget
from ..ir.evidence import ScoutEvidence
from .f2 import f2_kernel_basis, f2_rank
from .protocol import scout_evidence


def parity_matrix_scout(
    problem: NormalizedProblem,
    budget: AnalysisBudget,
) -> ScoutEvidence | None:
    cover = problem.cover
    if cover is None or not cover.parity_rows:
        return None
    rows = cover.parity_rows
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        return None
    rank = f2_rank(rows)
    kernel = f2_kernel_basis(rows)
    channels = len(cover.channels)
    degree = cover.degree
    # For the structured B (x) I_d pattern, the sheet-level matrix is s x s.
    kronecker_structured = bool(channels and degree and width == channels * degree)
    return scout_evidence(
        scout_family="kummer_parity_matrix",
        problem=problem,
        fingerprint={
            "row_count": len(rows),
            "column_count": width,
            "f2_rank": rank,
            "full_column_rank": rank == width,
            "kernel_dimension": len(kernel),
            "kernel_basis": kernel,
            "channel_count": channels,
            "cover_degree": degree,
            "kronecker_structured_shape": kronecker_structured,
        },
        trace=(f"F2 rank {rank} of {len(rows)}x{width} parity matrix",),
        stability="exact",
        scout_operations=len(rows) * width,
    )
