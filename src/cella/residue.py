"""The residue algebra — two species, one account.

Admissions: A-001 (species M), A-002 (species R; PROPOSED — the composition of
the two species under one account is a DESIGN CONJECTURE that Gate G0.2 exists
to certify or refute).

Species
-------
M (measurement defect)
    The exact leftover of a lossy measurement-like map: rounding, fitting,
    sampling. Lives in the exact carrier; composes so that a chain of maps has
    a derivable total defect (Gate G0.1).

R (representation defect)
    The motion induced by a change of representation only — gauge, chart,
    calibration. It has a declared INVISIBLE SUBSPACE: the directions along
    which the represented quantity provably does not change (zero-sum against
    an invariant total). Type-level guarantee: an R-residue never alters any
    invariant (Gate G0.2).

Account discipline
------------------
- Composition never mixes species: an account is a pair of ledgers (M, R).
- Dropping a residue is impossible by construction; the only exit is into a
  Certificate, which records both ledgers.
- If G0.2 refutes single-account composition, this module splits and the
  ADMISSIONS record is updated — visibly, not silently.
"""

from __future__ import annotations

SPECIES_M = "M"  # measurement defect: exact leftover, reconstructive
SPECIES_R = "R"  # representation defect: zero-sum motion, invariant-preserving


class Residue:
    """A typed defect. Not yet implemented (Gates G0.1 / G0.2)."""

    def __init__(self, species: str, payload):
        raise NotImplementedError("Gate G0.1/G0.2 open: lands with A-001/A-002")

    def compose(self, other: "Residue") -> "Residue":
        """Same-species composition. Cross-species composition is an account
        operation, not a residue operation — see module contract."""
        raise NotImplementedError
