"""WARP (algebra arm) Stage-0 tests — the deciders behave, the token locus refuses,
the UNDERFLOW-WITNESS factors despite float cancellation, the wall is structurally
non-factoring (oracle-recoverable), the CL-W2 AST-seam holds, the ℙ¹ carrier +
Möbius + free-module reconstruction are sound, the schema role-gate holds, the
probe never imports the referee, and the frozen manifest gate passes with a pinned,
byte-stable sha. Exact ℚ; no battery emitted at Stage 0."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from lloyd_v4.evals.the_warp.carrier import (
    additive_residue,
    as_repr,
    free_module_reconstruct,
    mobius,
    p1_equal,
)
from lloyd_v4.evals.the_warp.ddynamic import d_dynamic
from lloyd_v4.evals.the_warp.dstatic import ast_seam_check, d_static
from lloyd_v4.evals.the_warp.fixtures import fixture_index
from lloyd_v4.evals.the_warp.mexpr import parse_mexpr
from lloyd_v4.evals.the_warp.referee import referee_truth, simplify_to_zero

IDX = fixture_index()


def _eq(points):
    return {v: Fraction(float.fromhex(h)) for v, h in points.items()}


def _ef(points):
    return {v: float.fromhex(h) for v, h in points.items()}


def test_static_dynamic_agree_factors_on_rational_core():
    for fid in ("FXWA1", "FXWA2", "FXWA3"):
        f = IDX[fid]; p = f["points"][0]
        e = parse_mexpr(f["sexpr"])
        assert d_static(e, _eq(p))["verdict"] == "factors"
        assert d_dynamic(e, _eq(p), _ef(p))["verdict"] == "factors"


def test_token_locus_refuses_intrinsic_token():
    for fid, kind in (("FXWB1", "pole"), ("FXWB2", "zero_neg_pow")):
        f = IDX[fid]; p = f["points"][0]
        r = d_dynamic(parse_mexpr(f["sexpr"]), _eq(p), _ef(p))
        assert r["verdict"] == "intrinsic_token"
        assert r["token"] == "indeterminate"
        assert r["refusal"] == kind


def test_underflow_witness_factors_despite_float_cancellation():
    f = IDX["FXWC1"]; p = f["points"][0]
    r = d_dynamic(parse_mexpr(f["sexpr"]), _eq(p), _ef(p))
    assert r["float"] == 0.0                 # total float cancellation
    assert r["true_q"] == 1                   # exact ℚ recovers it
    assert r["residue"] == 1                   # ρ ∈ R_exact
    assert r["closes"] is True and r["verdict"] == "factors"  # R_exact-by-composition


def test_wall_does_not_factor_static_and_oracle_recoverable():
    for fid in ("FXWD1", "FXWD2", "FXWD3"):
        f = IDX[fid]
        assert d_static(parse_mexpr(f["sexpr"]))["verdict"] == "does_not_factor"
        assert simplify_to_zero(f["sexpr"]) is True   # the one declared oracle call


def test_ast_seam_clean_clw2():
    seam = ast_seam_check()
    assert seam["reads_forbidden"] is False
    assert seam["forbidden_hits"] == [] and seam["rogue_calls"] == []


def test_independent_referee_matches_not_self_certified():
    for fid in ("FXWA1", "FXWA2", "FXWA3"):
        f = IDX[fid]; p = f["points"][0]
        e = parse_mexpr(f["sexpr"])
        dyn = d_dynamic(e, _eq(p), _ef(p))
        assert dyn["true_q"] == referee_truth(e, _eq(p))


def test_carrier_p1_equality_mobius_and_free_module():
    assert p1_equal(as_repr([1, 2]), as_repr([2, 4])) is True
    assert p1_equal(as_repr([1, 2]), as_repr([1, 3])) is False
    reps = [as_repr(r) for r in IDX["FXWF1"]["representatives"]]
    m = tuple(Fraction(v) for v in IDX["FXWF1"]["mobius"])
    assert p1_equal(mobius(m, reps[0]), mobius(m, reps[1])) is True  # respects quotient
    for fid in ("FXWE1", "FXWE2", "FXWE3"):
        s = IDX[fid]["samples"][0]
        assert free_module_reconstruct(s["true"], s["float"])["closes"] is True


def test_carrier_additive_residue_representative_dependent_clw5():
    # cross-multiply says same point; additive residue between representatives
    # differs -> ⊕_add ill-defined on ℙ¹ (foregone [ANALYTIC] half, §10.5).
    reps = [as_repr(r) for r in IDX["FXWF1"]["representatives"]]
    assert all(p1_equal(reps[0], r) for r in reps)
    assert additive_residue(reps[1], reps[0]) != additive_residue(reps[1], reps[1])


def test_schema_role_gate():
    from lloyd_v4.evals.the_warp.schema import WarpRecord, validate
    base = dict(
        campaign_id="the_warp_algebra_arm", schema_version="warp_record_v1",
        stage="A", fixture_id="FXWA1", fixture_class="FX-W-A",
        route_id="ctl", point={"x": "0x1.8p+0"},
        factorability_verdict="factors", carrier_sort=None,
        ast_seam_outcome={"reads_forbidden": False}, value="2", true_q="2",
        residue="frac:0/1", account={"ledger": []}, exposure=None,
        referee={}, refusals=(), telemetry={})
    # a verdict on a non-probe role is rejected
    with pytest.raises(ValueError):
        validate(WarpRecord(role="contrast", **base))
    # a verdict with no account is rejected
    bad = dict(base); bad["account"] = None
    with pytest.raises(ValueError):
        validate(WarpRecord(role="probe", **bad))
    # a clean probe verdict validates
    assert validate(WarpRecord(role="probe", **base)).role == "probe"


def test_probe_never_imports_referee_covenant7():
    src_dir = Path(__file__).resolve().parents[1] / "src" / "lloyd_v4" / "evals" / "the_warp"
    for probe in ("dstatic.py", "ddynamic.py"):
        text = (src_dir / probe).read_text()
        assert "the_warp.referee" not in text and "import referee" not in text


def test_frozen_gate_passes_and_manifest_is_pinned_byte_stable():
    from lloyd_v4.evals.the_warp.make_manifest import RESULTS_DIR, require_frozen
    m = require_frozen()                       # raises unless frozen + pins match
    assert m["frozen"] is True
    assert set(m["kill_conditions"]) == {"K-W1", "K-W2", "K-W3", "K-W4", "K-W5"}
    assert "SPINE FENCE" in m["spine_fence"]
    assert {f["fixture_id"] for f in m["fixtures"]} >= {
        "FXWA1", "FXWB1", "FXWC1", "FXWD1", "FXWE1", "FXWF1"}
    import hashlib
    pins = json.loads((Path(RESULTS_DIR) / "freeze_pins_sha256.json").read_text())
    actual = hashlib.sha256(
        (Path(RESULTS_DIR) / "manifest_v1.json").read_bytes()).hexdigest()
    assert pins["manifest_v1.json"] == actual   # frozen manifest matches its pin


def test_stage0_controls_are_pure_and_behave():
    from lloyd_v4.evals.the_warp import make_manifest as mm
    c = mm.stage0_controls()                    # pure; raises if any misbehaves
    assert c["dry_runs_refuse_token_locus"]["div0"]["verdict"] == "intrinsic_token"
    assert c["informativeness_control_fails"]["truth"] == "factors"
    assert c["carrier_informativeness_control_fails"]["truth"] == \
        "representative-dependent"
    assert c["K_W2_detects_planted_disagreement"]["dynamic"] == "factors"
    assert c["ast_seam_clean"]["reads_forbidden"] is False
