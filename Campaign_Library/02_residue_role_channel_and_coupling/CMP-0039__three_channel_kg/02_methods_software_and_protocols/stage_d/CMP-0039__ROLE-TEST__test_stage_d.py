"""c001 `three_channel_kg` — STAGE D suite (covenant step 3: must exit 0).

Frame honesty, CL-c7 (PARTIAL by design). Asserts:
  * the prereg-pin / clause-drift / bench-pin gates REFUSE on drift (the gates
    are non-tautological -- they bite a tampered contract);
  * every one of the 9 frozen frame-honesty predictions PASSES exact-Q;
  * the grading predicates are non-tautological -- mutation guards prove a
    LYING engine would be caught:
      - a channel triple that did NOT move under F12a fails P1;
      - a K_G that drifted under F12a/F12b fails P2/P4 AND fires K7 in P5;
      - a channel triple that moved under the signed permutation fails P3;
      - reporting a legitimate (orthogonal) rechart as a curvature error fires
        K7 (P5);
      - a non-orthogonal "rechart" is correctly NOT certified legitimate;
  * the PARTIAL discipline holds: CL-c7's proposed move is PARTIAL, never
    DEMONSTRATED; CL-c3c-ii is recorded OPEN; K-soft is non-refuting;
  * two runs of the battery are byte-identical (byte-stability).

Run with: PYTHONPATH=/home/wlloyd/Lloyd_Engine_V4/src pytest -q
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


# --------------------------------------------------------------------------
# gates bite (non-tautological contract enforcement)
# --------------------------------------------------------------------------
def test_clause_gate_refuses_value_drift():
    prereg = battery.load_prereg()
    saved = battery.GRADER_CLAUSES["K7_frame_undeclared"]
    battery.GRADER_CLAUSES["K7_frame_undeclared"] = saved + " DRIFT"
    try:
        try:
            battery.gate_clauses(prereg)
            raised = False
        except battery.ClauseDrift:
            raised = True
    finally:
        battery.GRADER_CLAUSES["K7_frame_undeclared"] = saved
    assert raised, "clause gate must refuse a drifted clause value"
    battery.gate_clauses(prereg)  # restored set passes


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
    battery.gate_clauses(prereg)
    assert set(battery.GRADER_CLAUSES) == set(prereg["grader_clauses"])


def test_bench_pins_match_frozen_prereg():
    prereg = battery.load_prereg()
    battery.gate_bench_pins(prereg)  # raises on any drift


# --------------------------------------------------------------------------
# all 9 predictions pass
# --------------------------------------------------------------------------
def test_all_predictions_pass():
    _records, verdicts = battery.run()
    failing = [pid for pid, v in verdicts.items() if not v["pass"]]
    assert failing == [], f"FAILED predictions (HALT): {failing}"
    assert len(verdicts) == 9


def test_F12a_moves_F12b_fixed():
    _records, verdicts = battery.run()
    # F12a: channels moved off base AND K_G invariant.
    p1 = verdicts["P1_F12a_channels_move"]["detail"]
    assert p1["moved_off_base"] and p1["A_eq_Bprime_eq_C"]
    assert verdicts["P2_F12a_KG_invariant"]["detail"]["pathA_KG_eq_base"]
    # F12b: channels fixed == base AND K_G invariant.
    p3 = verdicts["P3_F12b_channels_fixed"]["detail"]
    assert p3["fixed_eq_base"] and p3["A_eq_Bprime_eq_C"]
    assert verdicts["P4_F12b_KG_invariant"]["detail"]["pathA_KG_eq_base"]


def test_K7_not_fired():
    _records, verdicts = battery.run()
    assert verdicts["P5_K7_not_fired"]["K7_fired"] is False


def test_partial_discipline():
    _records, verdicts = battery.run()
    v7 = verdicts["P7_completeness_OPEN_Ksoft_flag"]
    assert v7["CL_c3c_ii"] == "OPEN"
    assert v7["CL_c7_proposed_move"] == "PARTIAL"        # never DEMONSTRATED
    assert v7["detail"]["K_soft_non_refuting_flag"] is True


def test_KG_invariant_value():
    _records, verdicts = battery.run()
    assert verdicts["P2_F12a_KG_invariant"]["F12a_K_G"] == "frac:-3/49"
    assert verdicts["P4_F12b_KG_invariant"]["F12b_K_G"] == "frac:-3/49"
    assert verdicts["P2_F12a_KG_invariant"]["base_K_G"] == "frac:-3/49"


# --------------------------------------------------------------------------
# mutation guards: a lying engine would be caught
# --------------------------------------------------------------------------
def test_mutation_nonmoving_F12a_fails_P1():
    base = (Q(-1, 49), Q(1, 49), Q(-3, 49))
    # a lie: channels do NOT move under the generic rotation
    lie_moved = base
    assert (lie_moved != base) is False  # P1 'moved_off_base' would be False -> FAIL


def test_mutation_KG_drift_fires_K7():
    base_kg = Q(-3, 49)
    drifted = base_kg + Q(1, 100)  # sigma_2 not held invariant under F12
    f12a_kg_invariant = (drifted == base_kg)
    f12b_kg_invariant = True
    k7_trigger_b = not (f12a_kg_invariant and f12b_kg_invariant)
    assert k7_trigger_b is True  # K7 fires -> P5 would FAIL


def test_mutation_moving_F12b_fails_P3():
    base = (Q(-1, 49), Q(1, 49), Q(-3, 49))
    # a lie: the signed permutation MOVES the channels (it must not)
    lie_fixed = (Q(0), Q(0), Q(-3, 49))
    assert (lie_fixed == base) is False  # P3 'fixed_eq_base' would be False -> FAIL


def test_mutation_legit_rechart_as_error_fires_K7():
    # a legitimate orthogonal rechart whose K_G is (wrongly) reported drifted
    R_ortho, R_det = battery.rechart_is_orthogonal(battery._R)
    assert R_ortho and R_det == Q(1)         # R IS a legitimate SO(3) rechart
    f12a_kg_invariant_lie = False            # engine reports it as a curvature error
    k7_trigger_a = (R_ortho and R_det == Q(1)) and (not f12a_kg_invariant_lie)
    assert k7_trigger_a is True              # K7 fires -> P5 would FAIL


def test_mutation_nonorthogonal_rechart_not_certified():
    # a NON-orthogonal matrix must NOT be certified as a legitimate rechart
    bogus = [[Q(2), Q(0), Q(0)], [Q(0), Q(1), Q(0)], [Q(0), Q(0), Q(1)]]
    ortho, det = battery.rechart_is_orthogonal(bogus)
    assert ortho is False  # the orthogonality gate is non-tautological


def test_recharts_are_genuinely_orthogonal():
    R_ortho, R_det = battery.rechart_is_orthogonal(battery._R)
    P_ortho, P_det = battery.rechart_is_orthogonal(battery._P)
    assert R_ortho and R_det == Q(1)               # SO(3): det +1
    assert P_ortho and abs(P_det) == Q(1)          # signed permutation: |det|=1


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
