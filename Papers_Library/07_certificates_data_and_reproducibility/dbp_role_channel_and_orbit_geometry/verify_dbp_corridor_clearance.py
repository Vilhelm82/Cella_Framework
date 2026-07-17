#!/usr/bin/env python3
"""Exact base, tube, derived-parameter and pole-clearance verifier."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
import json
from pathlib import Path
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "engine/src").is_dir())
sys.path.insert(0, str(ROOT / "engine/src"))

from cella.continuation.canonical import to_canonical_data  # noqa: E402
from cella.continuation.corridors import (  # noqa: E402
    CORRIDORS, QComplex, ROUTE_BOUNDS, TUBE_BOUNDS, exact_certificate_payload,
    exact_segment_minima, path_maximum_modulus_squared, path_minimum_squared,
    symbolic_identity_checks, verify_manifest, verify_published_bound_arithmetic,
)

passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


stored = json.loads((Path(__file__).parent / "DBP_EXACT_CORRIDOR_CLEARANCE_CERTIFICATES_v1.0.json").read_text())
check("stored certificate replay", stored["certificates"] == {k: to_canonical_data(exact_certificate_payload(v)) for k, v in CORRIDORS.items()})
for name, manifest in CORRIDORS.items():
    minima = exact_segment_minima(manifest)
    check(f"{name} has all 21 exact minima", len(minima) == 21)
    check(f"{name} positive segment clearance", all(item.minimum_squared > 0 for item in minima))
    check(f"{name} sigma bound", path_minimum_squared(manifest, "sigma_zero") >= F(1, 4))
    check(f"{name} maximum modulus", path_maximum_modulus_squared(manifest) <= 4)
    check(f"{name} tube avoids all punctures", min(path_minimum_squared(manifest, p) for p in ("sigma_zero", "plus_i", "minus_i")) > TUBE_BOUNDS["radius"] ** 2)
check("all Q(rho) identities", all(symbolic_identity_checks().values()))
check("all displayed bound arithmetic", all(verify_published_bound_arithmetic().values()))
check("curve factor lower bounds positive", all(value > 0 for key, value in ROUTE_BOUNDS.items() if not key.endswith("upper")))
check("tube factor lower bounds positive", all(value > 0 for key, value in TUBE_BOUNDS.items() if not key.endswith("upper")))

hit = replace(CORRIDORS["upper"], vertices=(QComplex(F(1), F(0)), QComplex(F(0), F(0)), *CORRIDORS["upper"].vertices[2:]))
try:
    verify_manifest(hit)
except ValueError as exc:
    check("tampered divisor crossing rejected", str(exc) in {"route_vertex_not_exact", "path_hits_divisor", "wrong_free_group_word"})
else:
    check("tampered divisor crossing rejected", False)
check("oversized tube rejected by exact margin", F(1, 2) ** 2 >= min(path_minimum_squared(CORRIDORS["upper"], p) for p in ("sigma_zero", "plus_i", "minus_i")))
print(f"DBP exact corridor clearance: {passed} assertions passed")
