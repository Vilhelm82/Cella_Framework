"""Canonical deterministic evaluator certificate records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from fractions import Fraction


class HexIntError(ValueError):
    """A hexadecimal integer field was absent, mistyped, or non-canonically spelled."""


_HEX_DIGITS = frozenset("0123456789abcdef")


def encode_hex_int(value: int) -> str:
    """Canonical sign-magnitude lowercase hex: no 0x prefix, no leading zeros, no '-0'.

    JSON has no bignum type and RFC 8259 permits conforming parsers to lose
    precision beyond 2**53, so unbounded certificate integers are carried as
    strings and never as bare JSON numbers.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise HexIntError("hex integer encoding requires a non-boolean int")
    return ("-" if value < 0 else "") + format(abs(value), "x")


def decode_hex_int(text: str) -> int:
    """Strict inverse of encode_hex_int; every non-canonical spelling is refused.

    Canonicity is enforced by re-encoding: each value has exactly one admissible
    spelling, so byte-stable digests survive any conforming JSON round trip.
    """
    if not isinstance(text, str):
        raise HexIntError("hex integer must be a string")
    negative = text.startswith("-")
    body = text[1:] if negative else text
    if not body or not _HEX_DIGITS.issuperset(body):
        raise HexIntError(f"non-canonical hex integer {text!r}")
    value = -int(body, 16) if negative else int(body, 16)
    if encode_hex_int(value) != text:
        raise HexIntError(f"non-canonical hex integer {text!r}")
    return value


def canon(value):
    if is_dataclass(value): value = asdict(value)
    if isinstance(value, Fraction): return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict): return {str(k): canon(v) for k, v in sorted(value.items())}
    if isinstance(value, (tuple, list)): return [canon(v) for v in value]
    if value is None or isinstance(value, (str, int, bool)): return value
    raise TypeError(f"non-canonical certificate value {type(value).__name__}")


def canonical_bytes(record) -> bytes:
    return json.dumps(canon(record), sort_keys=True, separators=(",", ":")).encode()


def digest(record) -> str:
    return hashlib.sha256(canonical_bytes(record)).hexdigest()
