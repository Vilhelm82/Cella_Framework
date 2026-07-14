"""Canonical, deterministic encoding for continuation evidence."""

from __future__ import annotations

import hashlib
import json
from dataclasses import fields, is_dataclass
from enum import Enum
from fractions import Fraction
from typing import Any


def to_canonical_data(value: object) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: to_canonical_data(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Fraction):
        return {
            "numerator": str(value.numerator),
            "denominator": str(value.denominator),
        }
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise TypeError("canonical continuation mappings require string keys")
        return {
            key: to_canonical_data(value[key])
            for key in sorted(value)
        }
    if isinstance(value, (tuple, list)):
        return [to_canonical_data(item) for item in value]
    if value is None or isinstance(value, (bool, int, str)):
        return value
    raise TypeError(
        f"value is outside canonical continuation serialization: {type(value).__name__}"
    )


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        to_canonical_data(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def canonical_digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()
