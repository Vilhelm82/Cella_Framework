"""The certificate — two registers, one record.

Schema: CERTIFICATE_SCHEMA.md (fixed at Layer 0; versioned).

Contract
--------
- Every emitted result is a Certificate; there is no bare-value exit from the
  engine.
- ``plain()`` renders the four questions in ordinary language:
      WHAT WAS COMPUTED / WHAT IS EXACT / WHAT WAS REFUSED, AND WHY /
      WHAT WOULD CHANGE THIS RESULT
  using only the vocabulary map — no internal jargon can reach the plain
  register.
- ``machine()`` renders inputs hashes, the two-ledger residue account,
  refusal tokens, number-type tags, and the double-run digest.
- A certificate certifies the computation and its account — NEVER a state of
  the world. Detection statements are a separate object that cites
  certificates and carries its own confidence figures.
- Emission requires double-run bit-identity; a certificate that cannot state
  its rerun digest does not exist.
"""

from __future__ import annotations


class Certificate:
    """Two-register result object. Not yet implemented (Gate G0.4)."""

    def __init__(self, record: dict):
        raise NotImplementedError("Gate G0.4 open")

    def plain(self) -> str:
        """The four questions, ordinary language only."""
        raise NotImplementedError

    def machine(self) -> dict:
        """Everything needed to re-run bit-for-bit."""
        raise NotImplementedError
