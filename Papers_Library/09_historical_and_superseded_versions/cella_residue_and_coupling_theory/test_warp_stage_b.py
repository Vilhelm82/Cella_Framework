"""WARP Stage-B tests — free-module additive reconstruction closes on every FX-W-E
carrier (CL-W4); the ℙ¹ keystone holds (CL-W5: additive residue representative-
dependent while cross-multiply says same point — [ANALYTIC]; Möbius maps equal points
to equal points and moves the point — [MEASURED]); the Rule-1.8 clause gate refuses
drift; the frozen prereg pin is live; records byte-stable. Read-only against committed
artifacts."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import pytest

from lloyd_v4.evals.the_warp.carrier import (
    additive_residue,
    as_repr,
    carrier_sort,
    free_module_reconstruct,
    mobius,
    p1_equal,
)
from lloyd_v4.evals.the_warp.fixtures import fixture_index

IDX = fixture_index()
BASE = Path(__file__).resolve().parents[1] / "results" / "the_warp"
RECORDS_SHA = "71ca79585b7959f5c494f392c3fa0a5bf1baf235510c010da9497402091500d5"


def test_clw4_free_module_additive_closes():
    for fid in ("FXWE1", "FXWE2", "FXWE3"):
        f = IDX[fid]
        assert carrier_sort(f["carrier"]) == "free_module"
        rec = free_module_reconstruct(f["samples"][0]["true"],
                                      f["samples"][0]["float"])
        assert rec["closes"] is True


def test_clw5_keystone_quotient_edge():
    f = IDX["FXWF1"]
    assert carrier_sort(f["carrier"]) == "quotient"
    reps = [as_repr(r) for r in f["representatives"]]
    # all the same projective point by cross-multiply
    assert all(p1_equal(reps[0], r) for r in reps)
    # [ANALYTIC] foregone: additive residue representative-dependent
    assert additive_residue(reps[1], reps[0]) != additive_residue(reps[1], reps[1])
    # [MEASURED]: Möbius maps equal points to equal points, and moves the point
    m = tuple(Fraction(v) for v in f["mobius"])
    imgs = [mobius(m, r) for r in reps]
    assert all(p1_equal(imgs[0], im) for im in imgs)
    assert not p1_equal(imgs[0], reps[0])


def test_clause_gate_refuses_drift(monkeypatch):
    import lloyd_v4.evals.the_warp.run_stage_b as rb
    assert rb.require_stage_b_prereg()["stage"] == "B"
    monkeypatch.setitem(rb.GRADER_CLAUSES, "PMB.3",
                        rb.GRADER_CLAUSES["PMB.3"] + " (drifted)")
    with pytest.raises(RuntimeError, match="DRIFTED"):
        rb.require_stage_b_prereg()


def test_stage_b_prereg_frozen_pin_and_kw3_wired():
    prereg = json.loads((BASE / "stage_b" / "prereg.json").read_text())
    assert prereg["frozen"] is True
    pin = (BASE / "stage_b" / "prereg_sha256.pin").read_text().strip()
    assert hashlib.sha256(
        (BASE / "stage_b" / "prereg.json").read_bytes()).hexdigest() == pin
    assert "K-W3 (refute-row-and-continue)" in prereg["status_move_rules"]
    assert prereg["depends_on"]["manifest_v1_sha256"] == hashlib.sha256(
        (BASE / "manifest_v1.json").read_bytes()).hexdigest()


def test_records_byte_stable_and_verdicts_pass_no_status_move():
    recs = BASE / "stage_b" / "records" / "stage_b_records.jsonl"
    assert hashlib.sha256(recs.read_bytes()).hexdigest() == RECORDS_SHA
    v = json.loads((BASE / "stage_b" / "prediction_verdicts.json").read_text())
    assert v["PMB.1"]["pass"] and v["PMB.2"]["pass"]
    assert v["k_w3_fired"] is False
    assert "NO status move applied" in v["NOTE"]
