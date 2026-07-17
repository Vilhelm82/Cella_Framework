"""WARP Stage-A tests — D_static/D_dynamic agree on the factor battery (CL-W1) with
the independent referee matching, the wall split holds (CL-W3), the Rule-1.8 clause
gate refuses drift, the frozen prereg pin is live with the kills wired, and the
committed records are byte-stable. Read-only against committed artifacts (the
battery itself is a script-only act)."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import pytest

from lloyd_v4.evals.the_warp.ddynamic import d_dynamic
from lloyd_v4.evals.the_warp.dstatic import d_static
from lloyd_v4.evals.the_warp.fixtures import fixture_index
from lloyd_v4.evals.the_warp.referee import referee_truth, simplify_to_zero
from lloyd_v4.evals.the_warp.mexpr import parse_mexpr

IDX = fixture_index()
BASE = Path(__file__).resolve().parents[1] / "results" / "the_warp"
RECORDS_SHA = "c540c1e0860406336e0639e015f0cf9cad9be7d1baa2c3da37583b9a28517c82"


def _eq(p):
    return {v: Fraction(float.fromhex(h)) for v, h in p.items()}


def _ef(p):
    return {v: float.fromhex(h) for v, h in p.items()}


def test_factor_battery_static_dynamic_agree_and_referee_matches():
    for fid in ("FXWA1", "FXWA2", "FXWA3", "FXWC1", "FXWC2", "FXWC3"):
        f = IDX[fid]; p = f["points"][0]
        e = parse_mexpr(f["sexpr"])
        s = d_static(e, _eq(p))
        dyn = d_dynamic(e, _eq(p), _ef(p))
        assert s["verdict"] == "factors" == dyn["verdict"]      # CL-W1 biconditional
        assert dyn["true_q"] == referee_truth(e, _eq(p))        # not self-certified
        assert dyn["closes"] and dyn["rho_in_Rexact"]


def test_wall_split_clw3():
    for fid in ("FXWD1", "FXWD2", "FXWD3"):
        f = IDX[fid]
        assert d_static(parse_mexpr(f["sexpr"]))["verdict"] == "does_not_factor"
        dyn = d_dynamic(parse_mexpr(f["sexpr"]), {}, {})
        assert dyn["verdict"] == "does_not_factor"
        assert dyn["refusal"] == "transcendental_uninterpreted"
        assert simplify_to_zero(f["sexpr"]) is True             # oracle recovers


def test_clause_gate_refuses_drift(monkeypatch):
    import lloyd_v4.evals.the_warp.run_stage_a as ra
    assert ra.require_stage_a_prereg()["stage"] == "A"
    monkeypatch.setitem(ra.GRADER_CLAUSES, "PMW.4",
                        ra.GRADER_CLAUSES["PMW.4"] + " (drifted)")
    with pytest.raises(RuntimeError, match="DRIFTED"):
        ra.require_stage_a_prereg()


def test_stage_a_prereg_frozen_pin_live_and_kills_wired():
    prereg = json.loads((BASE / "stage_a" / "prereg.json").read_text())
    assert prereg["frozen"] is True
    pin = (BASE / "stage_a" / "prereg_sha256.pin").read_text().strip()
    assert hashlib.sha256(
        (BASE / "stage_a" / "prereg.json").read_bytes()).hexdigest() == pin
    assert prereg["depends_on"]["manifest_v1_sha256"] == hashlib.sha256(
        (BASE / "manifest_v1.json").read_bytes()).hexdigest()
    assert "K-W1 FIRES" in prereg["status_move_rules"]
    assert "THE CAMPAIGN HALTS" in prereg["status_move_rules"]
    assert "no spine claim" in prereg["spine_fence_ack"].lower()


def test_records_byte_stable_and_verdicts_pass_no_status_move():
    recs = BASE / "stage_a" / "records" / "stage_a_records.jsonl"
    assert hashlib.sha256(recs.read_bytes()).hexdigest() == RECORDS_SHA
    v = json.loads((BASE / "stage_a" / "prediction_verdicts.json").read_text())
    assert v["PMW.1"]["pass"] and v["PMW.2"]["pass"] and v["PMW.3"]["pass"]
    assert v["PMW.1"]["k_w1_fired"] is False and v["PMW.1"]["k_w2_fired"] is False
    assert v["PMW.3"]["k_w4_fired"] is False
    # verdicts are PROPOSED only — no status move applied in-campaign
    assert "NO status move applied" in v["NOTE"]
