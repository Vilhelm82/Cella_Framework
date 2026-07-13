"""The certificate — two registers, one record.

Schema: CERTIFICATE_SCHEMA.md, version cert-v1. Gate G0.4 certifies this.

Contract
--------
- Every emitted result is a Certificate; there is no bare-value exit.
- ``emit()`` runs the computation TWICE and refuses to construct the
  certificate unless the canonical serializations agree bit-for-bit —
  a certificate that cannot state its rerun digest does not exist
  (EmissionError).
- ``plain()`` renders the four questions in ordinary language using only
  the refusal vocabulary's plain renderings — no raw token, no jargon.
- ``machine()`` returns the full canonical record.
- A certificate certifies the computation and its account — NEVER a state
  of the world. Detection statements are a different object.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction

from .qsqrt import QSqrt
from .refusal import Refusal
from .residue import is_zero

SCHEMA = "cert-v1"

_REQUIRED = ("schema", "what", "value", "number_type", "account",
             "refusals", "depends", "rerun_digest")


class EmissionError(RuntimeError):
    """Double-run mismatch: the certificate cannot exist."""


def canon(obj):
    """Canonical JSON-able form; exact types become unambiguous strings."""
    if obj is None or isinstance(obj, (bool, int, str)):
        return obj
    if isinstance(obj, float):
        raise TypeError("float reached a certificate record: forbidden")
    if isinstance(obj, Fraction):
        return f"{obj.numerator}/{obj.denominator}"
    if isinstance(obj, QSqrt):
        return f"({canon(obj.a)})+({canon(obj.b)})*sqrt({canon(obj.r)})"
    if isinstance(obj, Refusal):
        return {"token": obj.token, "stratum": obj.stratum,
                "plain": obj.plain()}
    if isinstance(obj, (tuple, list)):
        return [canon(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): canon(v) for k, v in obj.items()}
    raise TypeError(f"cannot canonicalize {type(obj).__name__}")


def digest(obj) -> str:
    blob = json.dumps(canon(obj), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


class Certificate:
    """Two-register result object. Construct via emit()."""

    __slots__ = ("_record",)

    def __init__(self, record: dict):
        for k in _REQUIRED:
            if k not in record:
                raise ValueError(f"certificate record missing field {k!r}")
        if record["schema"] != SCHEMA:
            raise ValueError(f"schema mismatch: {record['schema']!r}")
        object.__setattr__(self, "_record", dict(record))

    def __setattr__(self, *_):
        raise AttributeError("Certificate is immutable")

    def machine(self) -> dict:
        """Everything needed to re-run bit-for-bit."""
        return canon(self._record)

    def plain(self) -> str:
        """The four questions, ordinary language only."""
        r = self._record
        lines = ["WHAT WAS COMPUTED", f"  {r['what']}", ""]
        lines.append("WHAT IS EXACT")
        if r["refusals"]:
            lines.append("  Nothing here is a numeric value — see the refusal "
                         "below.")
        elif r["account"].get("m") is None or is_zero(r["account"]["m"]):
            lines.append("  The value is exact — no rounding anywhere in this "
                         "number.")
        else:
            lines.append("  The value is representable; the leftover from "
                         "measurement/rounding is recorded exactly and "
                         "reconstructs the true value.")
        lines.append("")
        lines.append("WHAT WAS REFUSED, AND WHY")
        if r["refusals"]:
            for ref in r["refusals"]:
                lines.append(f"  {ref.plain()}")
        else:
            lines.append("  Nothing was refused.")
        lines.append("")
        lines.append("WHAT WOULD CHANGE THIS RESULT")
        for d in r["depends"]:
            lines.append(f"  - {d}")
        if r["account"].get("r_epochs"):
            lines.append("  - A pure recalibration (representation change) "
                         "cannot alter any certified invariant; its parameters "
                         "are recorded separately in the account.")
        if not r["depends"] and not r["account"].get("r_epochs"):
            lines.append("  - Nothing recorded beyond the inputs themselves.")
        return "\n".join(lines)


def emit(what: str, compute, depends=()) -> Certificate:
    """Run twice; construct only on bit-identical accounts (rerun law).

    ``compute()`` must return a dict with keys: value, number_type,
    account ({"m": ..., "r_epochs": ...}), refusals (list of Refusal).
    """
    r1, r2 = compute(), compute()
    d1, d2 = digest(r1), digest(r2)
    if d1 != d2:
        raise EmissionError("double-run mismatch: the certificate cannot exist")
    record = {"schema": SCHEMA, "what": what, "depends": list(depends),
              "rerun_digest": d1, **r1}
    return Certificate(record)
