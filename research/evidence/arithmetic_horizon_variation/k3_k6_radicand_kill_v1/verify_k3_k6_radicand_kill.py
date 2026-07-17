#!/usr/bin/env python3
"""Replay-verifier for the k=3/k=6 canonical-radicand kill test."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUILDER_PATH = HERE / "build_k3_k6_radicand_kill.py"
CERTIFICATE_PATH = HERE / "certificates/k3_k6_radicand_kill.json"
REPORT_PATH = HERE / "reports/K3_K6_RADICAND_KILL_TEST_v1.0.md"


def load_builder():
    spec = importlib.util.spec_from_file_location("k3_k6_radicand_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load radicand builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify() -> None:
    builder = load_builder()
    stored = json.loads(CERTIFICATE_PATH.read_text())
    rebuilt = builder.build_certificate()
    assert stored == rebuilt
    assert stored["verdict"] == "SURVIVES_K3_AND_K6"
    assert stored["scope"] == {
        "arbitrary_k_identity_derived": True,
        "arbitrary_k_theorem_claimed": False,
        "k3_generic_closure_claimed": True,
        "k6_generic_closure_claimed": True,
        "reason": "this falsifier run probes k=3 and k=6; promotion of the displayed all-k identity to a corpus theorem is a separate proof-and-audit action",
    }

    expected = {
        "3": {
            "degree": 4,
            "alpha": "e3(w)+u*e1(w)",
            "beta": "e2(w)+u",
            "even_reciprocal": "7/4",
            "even_beta": "14",
            "odd_reciprocal": "-1/4",
            "odd_beta": "2",
            "rank": 8,
            "group_order": "6144",
        },
        "6": {
            "degree": 22,
            "alpha": "e6(w)+u*e4(w)+u^2*e2(w)+u^3",
            "beta": "e5(w)+u*e3(w)+u^2*e1(w)",
            "even_reciprocal": "63/32",
            "even_beta": "64512",
            "odd_reciprocal": "-1/32",
            "odd_beta": "1024",
            "rank": 44,
            "group_order": str(2**44 * __import__("math").factorial(22)),
        },
    }

    for key, wanted in expected.items():
        case = stored["cases"][key]
        assert case["delta_k"] == wanted["degree"]
        assert case["alpha"] == wanted["alpha"]
        assert case["beta"] == wanted["beta"]
        assert all(case["formal_identity_checks"].values())
        assert case["sheet_level_B"] == [[1, 0], [1, 1]]
        assert case["sheet_level_rank_F2"] == 2
        assert case["square_class_rank"] == wanted["rank"]
        assert case["normal_closure_group_order"] == wanted["group_order"]

        even = case["even_contact"]
        odd = case["odd_contact"]
        assert even["reciprocal_sum"] == wanted["even_reciprocal"]
        assert even["beta_contact"] == wanted["even_beta"]
        assert odd["reciprocal_sum"] == wanted["odd_reciprocal"]
        assert odd["beta_contact"] == wanted["odd_beta"]
        assert even["valuation_parity_u_gamma_plus"] == [1, 0]
        assert odd["valuation_parity_u_gamma_plus"] == [1, 1]
        for contact in (even, odd):
            coefficients = [int(value) for value in contact["mass_norm_coefficients_low_first"]]
            assert len(coefficients) - 1 == wanted["degree"]
            assert coefficients[0] == 0
            assert coefficients[1] != 0
            assert contact["mass_norm_derivative_at_zero"] == str(coefficients[1])
            assert contact["u_zero_is_simple"]
            assert contact["signed_wall_is_unique"]
            assert contact["matching_signed_walls"] == [contact["signs"]]

    for source in stored["source_refs"].values():
        path = builder.ROOT / source["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"]

    report = REPORT_PATH.read_text()
    assert "**SURVIVES at both k=3 and k=6**" in report
    assert "gamma_k(gamma_k-4P)=4u beta_k^2" in report
    assert "k=3: rank 8" in report
    assert "k=6: rank 44" in report
    assert "does **not** silently promote two probes into an arbitrary-k theorem" in report
    print("PASS: exact k=3/k=6 canonical-radicand kill test survives with ranks 8 and 44")


if __name__ == "__main__":
    verify()
