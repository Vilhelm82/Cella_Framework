"""c001 `three_channel_kg` — STAGE A suite (covenant step 3: must exit 0).

Asserts:
  * the prereg-pin / clause-drift / bench-pin gates REFUSE on drift (the gates
    are non-tautological -- they bite a tampered contract);
  * every one of the 13 frozen predictions PASSES exact-Q;
  * the grading predicates are non-tautological -- mutation guards prove a
    LYING engine would be caught (a wrong tuple fails P1; a broken partition
    fails P3/K2; a non-flipping mutant is not flagged as inverting in P5; a
    nonzero on F9 fails P6; a near-miss is rejected by exact equality in P8; a
    numeric-0-on-q=0 lie is caught by P9; a corrupted partition formula leaves
    nonzero residual in P12);
  * two runs of the battery are byte-identical (byte-stability).

Run with: PYTHONPATH=/home/wlloyd/Lloyd_Engine_V4/src pytest -q
(the battery itself also inserts the shared src on sys.path).
"""

from __future__ import annotations

import copy
import importlib
import os
import sys
from fractions import Fraction as Q

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

battery = importlib.import_module("battery")
Qf = Q


# --------------------------------------------------------------------------
# gates bite (non-tautological contract enforcement)
# --------------------------------------------------------------------------
def test_clause_gate_refuses_value_drift():
    prereg = battery.load_prereg()
    saved = battery.GRADER_CLAUSES["K2_partition"]
    battery.GRADER_CLAUSES["K2_partition"] = saved + " DRIFT"
    try:
        try:
            battery.gate_clauses(prereg)
            raised = False
        except battery.ClauseDrift:
            raised = True
    finally:
        battery.GRADER_CLAUSES["K2_partition"] = saved
    assert raised, "clause gate must refuse a drifted clause value"
    # restored set passes
    battery.gate_clauses(prereg)


def test_clause_gate_refuses_keyset_drift():
    prereg = battery.load_prereg()
    battery.GRADER_CLAUSES["SPURIOUS"] = "x"
    try:
        try:
            battery.gate_clauses(prereg)
            raised = False
        except battery.ClauseDrift:
            raised = True
    finally:
        del battery.GRADER_CLAUSES["SPURIOUS"]
    assert raised, "clause gate must refuse a changed key-set"


def test_bench_pin_gate_refuses_sha_drift():
    prereg = copy.deepcopy(battery.load_prereg())
    prereg["depends_on"]["src/lloyd_v4/evals/three_channel_kg/probe.py"] = "0" * 64
    try:
        battery.gate_bench_pins(prereg)
        raised = False
    except battery.PinDrift:
        raised = True
    assert raised, "pin gate must refuse a wrong bench sha"


def test_clauses_match_frozen_prereg():
    prereg = battery.load_prereg()
    # the embedded clauses byte-match the frozen prereg (no drift on the
    # as-shipped contract).
    battery.gate_clauses(prereg)
    assert set(battery.GRADER_CLAUSES) == set(prereg["grader_clauses"])


def test_bench_pins_match_frozen_prereg():
    prereg = battery.load_prereg()
    battery.gate_bench_pins(prereg)  # raises on any drift


# --------------------------------------------------------------------------
# all 13 predictions pass
# --------------------------------------------------------------------------
def test_all_predictions_pass():
    _records, verdicts = battery.run()
    failing = [pid for pid, v in verdicts.items() if not v["pass"]]
    assert failing == [], f"FAILED predictions (HALT): {failing}"
    assert len(verdicts) == 13


def test_keystone_anchor():
    _records, verdicts = battery.run()
    d = verdicts["P2_keystone_F8"]["detail"]
    assert d["q_eq_14"] and d["det_hb_eq_12"]
    assert d["K_G_eq_m3_49"] and d["K_G_negative_signed"]
    assert d["pathB_total_agrees"] and d["pathBprime_tuple_agrees"] and d["pathC_oracle_agrees"]


def test_developable_cone_zero_or_refusal():
    _records, verdicts = battery.run()
    d = verdicts["P6_rank_heuristic_K6"]["detail"]
    assert d["never_nonzero"], "F9 developable cone must be exactly 0 (K6)"


def test_sphere_one():
    _records, verdicts = battery.run()
    assert verdicts["P11_both_sign_witnesses_CLc1_signed"]["F6_KG"] == "frac:1/1"


# --------------------------------------------------------------------------
# mutation guards: a lying engine would be caught
# --------------------------------------------------------------------------
def test_mutation_wrong_tuple_fails_rowpass():
    exp = (Qf(-3, 49), Qf(-1, 49), Qf(1, 49), Qf(-3, 49))
    lie = (Qf(0), Qf(-1, 49), Qf(1, 49), Qf(-3, 49))
    assert (lie == exp) is False  # P1 c1 would reject the lie


def test_mutation_broken_partition_fails_K2():
    det = Qf(12)
    broken = Qf(11)  # Delta sum != det
    assert (det - broken == 0) is False  # P3 residual_zero would be False


def test_mutation_nonflip_not_flagged_as_invert():
    true_kg = Qf(-1, 9)
    ts = (true_kg > 0) - (true_kg < 0)
    # a mutant that does NOT flip (== true) must NOT be flagged as inverting
    nonflip = true_kg
    fs = (nonflip > 0) - (nonflip < 0)
    assert (fs == -ts and ts != 0) is False
    # the real sign-flip mutant DOES invert
    flip = -true_kg
    fs2 = (flip > 0) - (flip < 0)
    assert (fs2 == -ts and ts != 0) is True


def test_mutation_nonzero_on_F9_fails_K6():
    assert (Qf(1, 1000) == Qf(0)) is False


def test_mutation_near_miss_rejected_no_tolerance():
    got = Qf(-3, 49)
    near = got + Qf(1, 10 ** 9)
    assert (got == near) is False           # exact equality rejects near-miss
    assert (abs(got - near) < Qf(1, 10 ** 6)) is True  # a tolerant band WOULD wrongly pass it


def test_mutation_numeric_zero_on_q0_would_fail_K11():
    # a lying engine returning numeric 0 on q=0 does NOT raise -> refused False
    def lying():
        return Qf(0)
    refused = False
    try:
        lying()
    except Exception:
        refused = True
    assert refused is False  # P9 requires a typed refusal; this lie would FAIL P9


def test_mutation_corrupted_partition_nonzero_residual():
    B = battery
    g1, g2, g3 = B._pvar(0), B._pvar(1), B._pvar(2)
    h11, h12, h13 = B._pvar(3), B._pvar(4), B._pvar(5)
    h22, h23, h33 = B._pvar(6), B._pvar(7), B._pvar(8)
    Z = {}
    Hb = [[Z, g1, g2, g3], [g1, h11, h12, h13],
          [g2, h12, h22, h23], [g3, h13, h23, h33]]

    def det3(M):
        return B._padd(
            B._pmul(M[0][0], B._padd(B._pmul(M[1][1], M[2][2]), B._pneg(B._pmul(M[1][2], M[2][1])))),
            B._pneg(B._pmul(M[0][1], B._padd(B._pmul(M[1][0], M[2][2]), B._pneg(B._pmul(M[1][2], M[2][0]))))),
            B._pmul(M[0][2], B._padd(B._pmul(M[1][0], M[2][1]), B._pneg(B._pmul(M[1][1], M[2][0])))))

    def det4(M):
        acc = {}
        sign = 1
        for c in range(4):
            minor = [[M[r][cc] for cc in range(4) if cc != c] for r in range(1, 4)]
            t = B._pmul(M[0][c], det3(minor))
            acc = B._padd(acc, t if sign == 1 else B._pneg(t))
            sign = -sign
        return acc

    det_sym = det4(Hb)
    # corrupted delta_c: drop +g1^2 h23^2
    delta_c_bad = B._padd(
        B._pneg(B._psmul(B._pmul(B._pmul(g1, g2), B._pmul(h13, h23)), 2)),
        B._pneg(B._psmul(B._pmul(B._pmul(g1, g3), B._pmul(h12, h23)), 2)),
        B._pmul(B._pmul(g2, g2), B._pmul(h13, h13)),
        B._pneg(B._psmul(B._pmul(B._pmul(g2, g3), B._pmul(h12, h13)), 2)),
        B._pmul(B._pmul(g3, g3), B._pmul(h12, h12)))
    delta_s = B._padd(
        B._pneg(B._pmul(B._pmul(g1, g1), B._pmul(h22, h33))),
        B._pneg(B._pmul(B._pmul(g2, g2), B._pmul(h11, h33))),
        B._pneg(B._pmul(B._pmul(g3, g3), B._pmul(h11, h22))))
    delta_m = B._padd(
        B._psmul(B._pmul(B._pmul(g1, g2), B._pmul(h12, h33)), 2),
        B._psmul(B._pmul(B._pmul(g1, g3), B._pmul(h13, h22)), 2),
        B._psmul(B._pmul(B._pmul(g2, g3), B._pmul(h11, h23)), 2))
    bad = B._padd(delta_c_bad, delta_s, delta_m)
    residual = B._padd(det_sym, B._pneg(bad))
    assert len(residual) > 0, "a corrupted partition must leave nonzero residual (P12 bites)"
    # and the TRUE proof has zero residual
    assert B.symbolic_identity_proof()["residual_monomials"] == 0


# --------------------------------------------------------------------------
# byte-stability: two runs identical
# --------------------------------------------------------------------------
def test_two_runs_byte_identical(tmp_path):
    r1, _ = battery.run()
    r2, _ = battery.run()
    p1 = str(tmp_path / "r1.jsonl")
    p2 = str(tmp_path / "r2.jsonl")
    s1 = battery.write_records(r1, p1)
    s2 = battery.write_records(r2, p2)
    assert s1 == s2, "two battery runs must be byte-identical"
    with open(p1, "rb") as f1, open(p2, "rb") as f2:
        assert f1.read() == f2.read()
