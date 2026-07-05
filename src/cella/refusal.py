"""Stratum-typed refusals — degeneracy is a stratum, not a failure.

Admission: A-004 (PROPOSED).

Contract
--------
- A refusal is a first-class result: it flows into Cells and Certificates
  exactly like a value, with the reason where the value would be.
- The vocabulary is CLOSED: tokens are added only by ADMISSIONS record, and
  every token has a plain-language rendering in CERTIFICATE_SCHEMA.md's
  vocabulary map. An unrenderable token is a defect.
- No code path may emit NaN, None-as-value, or an exception in place of a
  refusal.

Founding vocabulary (grows by admission only)
---------------------------------------------
    SINGULAR_GRADIENT   surface has no well-defined direction here
    RANK_DEFICIENT      channels moved in lockstep; no surface can be fitted
    BELOW_DETECTION     any real signal is smaller than what was discarded
    UNRECOVERABLE       true object not reconstructible from this observation
    INDETERMINATE       inputs do not determine the quantity at all
"""

from __future__ import annotations

VOCABULARY = (
    "SINGULAR_GRADIENT",
    "RANK_DEFICIENT",
    "BELOW_DETECTION",
    "UNRECOVERABLE",
    "INDETERMINATE",
)


class Refusal:
    """A typed, stratum-classified non-recovery token. Not yet implemented (G0.4)."""

    def __init__(self, token: str, stratum: str, plain_reason: str):
        raise NotImplementedError("Gate G0.4 open: lands with A-004")
