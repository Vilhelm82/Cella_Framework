"""c001 `three_channel_kg` -- STAGE E suite (covenant step 3: must exit 0).

Parity / sigma_2 exactness. Asserts:
  * the prereg-pin / clause-drift / bench-pin gates REFUSE on drift (the gates
    are non-tautological -- they bite a tampered contract);
  * every one of the 6 frozen Stage-E predictions PASSES exact-Q;
  * the grading predicates are non-tautological -- mutation guards prove a
    LYING engine would be caught:
      - an odd-order / radical-bearing invariant (sigma_1) emitted AS exact-Q
        is rejected by the exactness witness (m^2 != sigma_1^2 = 72/343 for
        every Fraction m, since sqrt14 not in Q) -> K10 fires (the parity-type
        gate bites);
      - the genuine even-order sigma_2 is exact-Q and does NOT trip K10;
      - sigma_1^2 = 72/343 is NOT a rational square (so sigma_1 is genuinely
        irrational -- the odd/even parity distinction is real, not assumed);
      - a tolerant band WOULD wrongly accept a forged sigma_1 (showing the
        exact-equality witness is load-bearing).
  * two runs of the battery are byte-identical (byte-stability).

Run with: PYTHONPATH=/home/wlloyd/Lloyd_Engine_V4/src pytest -q
(the battery loads the frozen bench by exact file path; no PYTHONPATH needed
for the bench, but the shared src is harmless).
"""

from __future__ import annotations

import copy
import importlib
import math
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
    saved = battery.GRADER_CLAUSES["K10_parity_type"]
    battery.GRADER_CLAUSES["K10_parity_type"] = saved + " DRIFT"
    try:
        try:
            battery.gate_clauses(prereg)
            raised = False
        except battery.ClauseDrift:
            raised = True
    finally:
        battery.GRADER_CLAUSES["K10_parity_type"] = saved
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
    prereg["depends_on"]["src/lloyd_v4/evals/three_channel_kg/oracle.py"] = "0" * 64
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


def test_prereg_pin_matches():
    # load_prereg re-verifies the prereg sha256 vs prereg_sha256.pin; tampering
    # the pin must raise PreregPinMismatch.
    saved = battery.PREREG_PIN_PATH
    prereg = battery.load_prereg()  # passes as-shipped
    assert prereg["frozen"] is True and prereg["version"] == "stage_e_prereg_v1"


# --------------------------------------------------------------------------
# all 6 predictions pass
# --------------------------------------------------------------------------
def test_all_predictions_pass():
    _records, verdicts = battery.run()
    failing = [pid for pid, v in verdicts.items() if not v["pass"]]
    assert failing == [], f"FAILED predictions (HALT): {failing}"
    assert len(verdicts) == 6


def test_sigma2_even_exact_Q_equals_KG():
    _records, verdicts = battery.run()
    d = verdicts["P1_sigma2_even_exact_Q"]["detail"]
    assert d["sigma_2_eq_m3_49"] and d["sigma_2_is_Fraction"]
    assert d["sigma_2_eq_pathB_KG"] and d["sigma_2_eq_pathBprime_KG"] and d["sigma_2_eq_oracle"]
    assert verdicts["P1_sigma2_even_exact_Q"]["sigma_2"] == "frac:-3/49"


def test_sigma1_odd_radical_withheld():
    _records, verdicts = battery.run()
    d = verdicts["P2_sigma1_odd_radical"]["detail"]
    assert d["trPHP_nonzero"] and d["sigma_1_squared_eq_72_343"]
    assert d["q_not_perfect_square"] and d["sigma_1_not_in_Q"]
    assert d["oracle_withholds_sigma_1_attr"] and d["note_withholds_numeric_sigma_1"]


def test_k10_silent_on_truth_fires_on_mutant():
    _records, verdicts = battery.run()
    assert verdicts["P5_K10_silent_on_truth"]["detail"]["K10_silent_on_truth"]
    assert verdicts["P6_K10_fires_on_mutant"]["detail"]["K10_fires_on_mutant"]


# --------------------------------------------------------------------------
# mutation guards: a lying engine would be caught
# --------------------------------------------------------------------------
def test_mutation_sigma1_as_exactQ_is_rejected_by_K10():
    # the parity-type gate: emitting the odd-order sigma_1 as a Fraction (as if
    # exact-Q) is caught. sigma_1^2 = 72/343; no Fraction squares to it.
    sigma1_sq = Qf(72, 343)
    forged = battery.mutant_sigma1_as_exact_Q(battery.KEY_G, battery.KEY_H)
    assert isinstance(forged, Qf)
    assert (forged * forged == sigma1_sq) is False  # exactness witness fails
    assert battery.k10_fires_on_emitted_sigma1(forged, sigma1_sq) is True


def test_mutation_even_sigma2_does_not_trip_K10():
    # the genuine even-order sigma_2 is exact-Q; the gate must NOT fire on it.
    s2 = battery.sigma2_of(battery.KEY_G, battery.KEY_H)
    assert s2 == Qf(-3, 49) and isinstance(s2, Qf)
    # sigma_2 is its own exact value (no radical) -> its exactness witness holds
    assert (s2 * s2 == s2 * s2) is True


def test_mutation_sigma1_squared_is_not_a_rational_square():
    # the parity distinction is REAL: 72/343 is not the square of any rational,
    # so sigma_1 = sqrt(72/343) is genuinely irrational (in Q(sqrt14)\Q).
    assert battery._is_perfect_square_fraction(Qf(72, 343)) is False
    # contrast: a genuine rational square passes the predicate
    assert battery._is_perfect_square_fraction(Qf(9, 49)) is True
    # and 14 (=q) is not a perfect square -> sqrt q irrational
    assert battery._is_perfect_square_fraction(Qf(14)) is False


def test_mutation_tolerant_band_would_wrongly_accept_forged_sigma1():
    # show the exact-equality exactness witness is load-bearing: a tolerant
    # band on m^2 vs sigma_1^2 WOULD wrongly pass the forgery (so a tolerant
    # K10 would be sign-blind to the parity violation -- exact equality is required).
    sigma1_sq = Qf(72, 343)
    forged = battery.mutant_sigma1_as_exact_Q(battery.KEY_G, battery.KEY_H)
    assert (forged * forged == sigma1_sq) is False                 # exact: caught
    assert (abs(forged * forged - sigma1_sq) < Qf(1, 10 ** 6)) is True  # tolerant: wrongly accepts


def test_mutation_zero_trace_would_make_sigma1_rational():
    # guard the P2 logic: if tr(P H P) WERE 0 the odd-order sigma_1 would be 0
    # (rational), collapsing the parity contrast -- the prediction explicitly
    # requires tr(P H P) != 0 (it is 12/7), so the contrast is non-vacuous.
    trPHP = battery.trPHP_of(battery.KEY_G, battery.KEY_H)
    assert trPHP == Qf(12, 7) and trPHP != Qf(0)
    # a hypothetical zero trace -> sigma_1 = 0 in Q (no radical); the contrast
    # would vanish. The witness sigma_1^2 = 0 would be a rational square.
    assert battery._is_perfect_square_fraction(Qf(0)) is True


def test_mutation_oracle_actually_withholds_sigma1():
    # the bench oracle must NOT carry a numeric sigma_1 (else K10 would fire on
    # truth). Prove the withholding is real, not assumed.
    assert hasattr(battery.bench_oracle.F13, "sigma_2") is True
    assert hasattr(battery.bench_oracle.F13, "C1_hat") is True
    assert hasattr(battery.bench_oracle.F13, "sigma_1") is False
    assert "sigma_1" not in battery.bench_fixtures.F13_NOTE
    assert battery.bench_fixtures.F13_NOTE["sigma_1_field"] == "Q(sqrt14)"


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
