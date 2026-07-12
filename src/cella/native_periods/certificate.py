"""Canonical deterministic evaluator certificate records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from fractions import Fraction


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
