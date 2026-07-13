"""Small canonical value domain for wrapper-neutral route records."""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, TypeAlias

FrozenScalar: TypeAlias = None | bool | int | str | Fraction
FrozenValue: TypeAlias = FrozenScalar | tuple["FrozenValue", ...] | tuple[tuple[str, "FrozenValue"], ...]


def freeze_value(value: object) -> FrozenValue:
    if value is None or isinstance(value, (bool, int, str, Fraction)):
        return value
    if isinstance(value, float):
        raise TypeError("binary floats are not canonical Pathfinder IR values")
    if isinstance(value, Mapping):
        return freeze_mapping(value)
    if isinstance(value, (tuple, list)):
        return tuple(freeze_value(item) for item in value)
    raise TypeError(f"unsupported Pathfinder IR value: {type(value).__name__}")


def freeze_mapping(mapping: Mapping[str, object]) -> tuple[tuple[str, FrozenValue], ...]:
    if any(not isinstance(key, str) for key in mapping):
        raise TypeError("Pathfinder IR mapping keys must be strings")
    return tuple((key, freeze_value(mapping[key])) for key in sorted(mapping))
