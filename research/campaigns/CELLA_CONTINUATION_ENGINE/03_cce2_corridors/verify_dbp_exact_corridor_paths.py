#!/usr/bin/env python3
"""Dependency-free exact verifier for the two locked Q(i) path manifests."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
import json
from pathlib import Path
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "engine/src").is_dir())
sys.path.insert(0, str(ROOT / "engine/src"))

from cella.continuation.canonical import to_canonical_data
from cella.continuation.corridors import (  # noqa: E402
    CORRIDORS, LOWER_VERTICES, PLUS_I, QComplex, UPPER_VERTICES,
    polygon_winding, structural_free_group_word, verify_manifest,
)

passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


artifact = json.loads((Path(__file__).parent / "DBP_EXACT_CORRIDOR_MANIFEST_v1.0.json").read_text())
check("artifact exactly matches production manifest", artifact["routes"] == to_canonical_data(CORRIDORS))
check("upper locked vertices", CORRIDORS["upper"].vertices == UPPER_VERTICES)
check("lower is exact conjugate", LOWER_VERTICES == tuple(QComplex(z.re, -z.im) for z in UPPER_VERTICES))
check("both routes close", all(m.vertices[0] == m.vertices[-1] == QComplex(F(1), F(0)) for m in CORRIDORS.values()))
check("upper structural word", structural_free_group_word(CORRIDORS["upper"]) == "a_+")
check("lower structural word", structural_free_group_word(CORRIDORS["lower"]) == "a_-^(-1)")
check("upper exact winding", polygon_winding(UPPER_VERTICES, PLUS_I) == 1)
check("lower exact winding", polygon_winding(LOWER_VERTICES, QComplex(F(0), F(-1))) == -1)
check("canonical digests differ", CORRIDORS["upper"].digest != CORRIDORS["lower"].digest)
check("production verifier accepts both", all(verify_manifest(m) for m in CORRIDORS.values()))

wrong_orientation = replace(CORRIDORS["lower"], vertices=(LOWER_VERTICES[0], LOWER_VERTICES[1], *reversed(LOWER_VERTICES[2:6]), LOWER_VERTICES[6], LOWER_VERTICES[7]))
try:
    structural_free_group_word(wrong_orientation)
except ValueError:
    check("wrong lower orientation is detected", True)
else:
    check("wrong lower orientation is detected", False)

check("winding alone is not identity evidence", structural_free_group_word(CORRIDORS["upper"]) == "a_+")
print(f"DBP exact corridor paths: {passed} assertions passed")
