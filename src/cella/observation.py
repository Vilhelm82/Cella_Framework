"""Observation maps — where every residue is born.

Admission: A-001 (PROPOSED).

Contract
--------
An ObservationMap Φ takes a finer object to a coarser representable one. Its
lossiness is constitutive; applying one ALWAYS yields a Cell:

    apply(T) -> Cell(Φ(T), defect_of_Φ_at_T)

- The defect is species M (measurement) or species R (representation) or a
  Refusal token; the map declares its species at construction.
- Maps compose; the defect of a composition is derivable from the parts
  (Gates G0.1 / G0.2). A map that cannot state its defect type does not get
  constructed.
- Examples that will live here later: exact rational ops (defect zero),
  float ingestion (M), windowed surface fit (M or refusal), gauge/chart
  change (R), unit recalibration (R).
"""

from __future__ import annotations


class ObservationMap:
    """A declared-defect map producing Cells. Not yet implemented (Gate G0)."""

    def __init__(self, name: str, species: str):
        raise NotImplementedError("Gate G0 open: lands with A-001")

    def apply(self, true_object):
        raise NotImplementedError

    def then(self, other: "ObservationMap") -> "ObservationMap":
        """Composition with derivable defect — the load-bearing primitive."""
        raise NotImplementedError
