"""Stratum-typed refusals — degeneracy is a stratum, not a failure.

Admission A-004 (ESTABLISHED). Gate G0.4 certifies this implementation.

Contract
--------
- A refusal is a first-class result: it flows into Cells and Certificates
  exactly like a value, with the reason where the value would be.
- The vocabulary is CLOSED: tokens are added only by ADMISSIONS record, and
  every token renders in plain language (the certificate's plain register
  never shows a raw token).
- No code path may emit NaN, None-as-value, or an exception in place of a
  refusal.
"""

from __future__ import annotations

VOCABULARY = (
    "SINGULAR_GRADIENT",
    "RANK_DEFICIENT",
    "BELOW_DETECTION",
    "UNRECOVERABLE",
    "INDETERMINATE",
)

PLAIN = {
    "SINGULAR_GRADIENT": "the surface has no well-defined direction here",
    "RANK_DEFICIENT": "the channels moved in lockstep; no surface can be fitted",
    "BELOW_DETECTION": "any real signal here is smaller than what was discarded",
    "UNRECOVERABLE": "the true object is not reconstructible from this observation",
    "INDETERMINATE": "the inputs do not determine this quantity at all",
}


class Refusal:
    """A typed, stratum-classified non-recovery token."""

    __slots__ = ("_token", "_stratum", "_detail")

    def __init__(self, token: str, stratum: str, detail: str = ""):
        if token not in VOCABULARY:
            raise ValueError(f"unknown refusal token {token!r} — the vocabulary "
                             "is closed; new tokens enter by ADMISSIONS record")
        if not isinstance(stratum, str) or not stratum:
            raise ValueError("a refusal must name its stratum")
        object.__setattr__(self, "_token", token)
        object.__setattr__(self, "_stratum", stratum)
        object.__setattr__(self, "_detail", detail)

    def __setattr__(self, *_):
        raise AttributeError("Refusal is immutable")

    @property
    def token(self) -> str:
        return self._token

    @property
    def stratum(self) -> str:
        return self._stratum

    def plain(self) -> str:
        """Ordinary-language rendering — what the certificate shows."""
        base = f"Refused: {PLAIN[self._token]} (stratum: {self._stratum})."
        return base + (f" {self._detail}" if self._detail else "")

    def __eq__(self, other):
        if not isinstance(other, Refusal):
            return NotImplemented
        return (self._token, self._stratum, self._detail) == \
               (other._token, other._stratum, other._detail)

    def __repr__(self):
        return f"Refusal({self._token}, stratum={self._stratum!r})"
