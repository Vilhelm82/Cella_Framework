"""Deterministic JSON serialization for typed route-analysis records."""

from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from fractions import Fraction
from typing import Any


def to_canonical_data(value: object) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: to_canonical_data(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Fraction):
        return {"numerator": str(value.numerator), "denominator": str(value.denominator)}
    if isinstance(value, tuple):
        return [to_canonical_data(item) for item in value]
    if value is None or isinstance(value, (bool, int, str)):
        return value
    raise TypeError(f"value is outside canonical Pathfinder serialization: {type(value).__name__}")


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        to_canonical_data(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
