"""Cella Framework — Layer 0 harness.

Standalone build. Zero imports from previous work (standing rule 1).
Every artifact here entered via an ADMISSIONS.md record (standing rule 2).

Layer 0 exposes the primitives:
    Cell            — (value, residue): a result that carries its own account
    ObservationMap  — a lossy map with a typed, composable defect
    Residue         — the defect algebra, two species (M: measurement, R: representation)
    Refusal         — stratum-typed non-recovery tokens
    QSqrt           — the exact number tower rung ℚ(√q)
    Certificate     — the two-register result object

Contract: nothing above Layer 0 may construct an uncertified number.
"""

__version__ = "0.0.1"
