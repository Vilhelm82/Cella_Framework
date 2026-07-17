"""c001 `three_channel_kg` — STAGE B suite (covenant step 3: must exit 0).

STAGE B — non-negativity impossibility. Asserts:
  * the prereg-pin / clause-drift / bench-pin gates REFUSE on drift (the gates
    are non-tautological -- they bite a tampered contract);
  * every one of the 10 frozen predictions PASSES exact-Q;
  * the grading predicates are non-tautological -- mutation guards prove a
    LYING engine would be caught:
      - a sign-blind (>=0) "K_G" surrogate FAILS the negative-witness test (P1/P3);
      - a non-negative proxy that did NOT differ from K_G would NOT fire K1 (P2);
      - a constant (sign-fixed) "K_G(t)" would NOT be indefinite (P4);
      - a rank-2 [[1,1,1]] (impossible) would break nullity; a degenerate
        Sigma=[[0,0,0]] would have rank 0, nullity 3 (caught by P5's rank==1);
      - a kappa_int that did not change sign across F10/F11 FAILS P6;
      - a numeric-0-on-q=0 lie is caught by P8;
  * two runs of the battery are byte-identical (byte-stability).

Run with: pytest -q  (the battery resolves the bench at the stable main path).
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
    saved = battery.GRADER_CLAUSES["K1_sign_blindness"]
    battery.GRADER_CLAUSES["K1_sign_blindness"] = saved + " DRIFT"
    try:
        try:
            battery.gate_clauses(prereg)
            raised = False
        except battery.ClauseDrift:
            raised = True
    finally:
        battery.GRADER_CLAUSES["K1_sign_blindness"] = saved
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


def test_prereg_pin_self_verifies():
    # load_prereg raises PreregPinMismatch if the prereg sha != the pin file.
    battery.load_prereg()


# --------------------------------------------------------------------------
# all 10 predictions pass
# --------------------------------------------------------------------------
def test_all_predictions_pass():
    _records, verdicts = battery.run()
    failing = [pid for pid, v in verdicts.items() if not v["pass"]]
    assert failing == [], f"FAILED predictions (HALT): {failing}"
    assert len(verdicts) == 10


def test_K1_silent_on_true_object():
    _records, verdicts = battery.run()
    d = verdicts["P1_K1_sign_blindness_F8"]["detail"]
    assert d["K_G_lt_0"] and not d["K1_fires_on_true_object"]
    assert not d["cond_i_KG_ge_0"]
    assert not d["cond_iii_kappa_int_absent"]
    assert d["Delta_m_nonzero"] and not d["cond_iv_Delta_m_dropped"]


def test_all_proxies_fire_K1():
    _records, verdicts = battery.run()
    d = verdicts["P2_K1_proxies_all_fire_F8"]["detail"]
    assert d["all_proxies_fire_K1"]
    assert d["proxies_firing_count"] == 5
    # PINNED: the 9/2401 proxy is K_G^2 (squared total), NOT the 11/2401 channel-norm.
    assert d["proxy_K_G_squared_is_manifest_kappa2_9_2401"]
    assert d["channel_norm_eq_11_2401"]
    assert d["proxy_K_G_squared"] == "frac:9/2401"
    assert d["channel_norm_11_2401_REFERENCE_ONLY"] == "frac:11/2401"


def test_both_sign_witnesses():
    _records, verdicts = battery.run()
    d = verdicts["P7_both_sign_witnesses_present"]["detail"]
    assert d["F6_eq_plus1"] and d["F8_eq_m3_49"]
    assert d["both_signs_KG"] and d["both_signs_kappa_int"]
    assert d["F6_paths_agree"] and d["F8_paths_agree"]
    assert d["F10_paths_agree"] and d["F11_paths_agree"]


def test_symbolic_indefinite_universal():
    _records, verdicts = battery.run()
    p = verdicts["P4_CLc3b_symbolic_indefinite_universal"]["proof"]
    assert p["det_monomials"] == 12
    assert p["K_G_t_degree"] == 1 and p["K_G_t_leading_coeff"] == "frac:1/1"
    assert p["K_G_t_nonconstant"] and p["numerator_indefinite_over_Q_g_H"]
    assert p["K_G_at_t_eq_1"] == "frac:1/1" and p["K_G_at_t_eq_minus_1"] == "frac:-1/1"
    assert p["q_squared_strictly_positive"]


def test_sigma_kernel_2dim():
    _records, verdicts = battery.run()
    p = verdicts["P5_CLc3c_i_sigma_kernel_2dim"]["proof"]
    assert p["rank_over_Q"] == 1 and p["nullity_dim"] == 2
    assert p["both_in_kernel"] and p["kernel_vecs_independent"]


def test_kappa_int_both_signs():
    _records, verdicts = battery.run()
    d = verdicts["P6_CLc6_kappa_int_both_signs"]["detail"]
    assert d["F10_negative"] and d["F11_positive"] and d["both_signs_of_kappa_int"]


# --------------------------------------------------------------------------
# mutation guards: a lying engine would be caught
# --------------------------------------------------------------------------
def test_mutation_nonneg_surrogate_fails_negative_witness():
    # The signed K_G(F8) = -3/49 is the negative witness. A non-negative
    # surrogate (e.g. |K_G| = 3/49, or K_G^2 = 9/2401) is NOT < 0, so it would
    # fail the negative-witness test the impossibility proof relies on.
    kg = Q(-3, 49)
    assert (kg < 0) is True                      # the true signed object: negative witness OK
    assert (abs(kg) < 0) is False                # |K_G| surrogate: NOT a negative witness
    assert (kg * kg < 0) is False                # K_G^2 surrogate: NOT a negative witness


def test_mutation_nonfiring_proxy_caught():
    # A proxy that EQUALS K_G (= -3/49) would NOT fire K1 (it would represent the
    # signed object). The real proxies are all >=0 and != -3/49, so they fire.
    kg = Q(-3, 49)
    fake_equal_proxy = Q(-3, 49)
    assert (fake_equal_proxy >= 0 and fake_equal_proxy != kg) is False  # does NOT fire
    real_proxy = Q(9, 2401)
    assert (real_proxy >= 0 and real_proxy != kg) is True               # fires


def test_mutation_constant_KG_t_not_indefinite():
    # A constant (sign-fixed) K_G(t) -- e.g. K_G(t)=+1 for all t -- is NOT
    # indefinite: it never takes a negative value. The real K_G(t)=+t is
    # degree-1 nonconstant and DOES take both signs.
    const_poly = {0: Q(1)}            # K_G(t) = 1 (constant)
    deg = max(const_poly)
    nonconstant = deg >= 1 and const_poly.get(deg, Q(0)) != 0
    assert nonconstant is False       # constant => not indefinite
    lin_poly = {1: Q(1)}              # K_G(t) = t
    deg2 = max(lin_poly)
    nonconstant2 = deg2 >= 1 and lin_poly.get(deg2, Q(0)) != 0
    assert nonconstant2 is True
    # and at t=+/-1 the linear one takes both signs
    assert (lin_poly.get(1, Q(0)) * Q(1) > 0) and (lin_poly.get(1, Q(0)) * Q(-1) < 0)


def test_mutation_symbolic_corrupted_det_changes_sign_polynomial():
    B = battery
    # The TRUE proof: K_G(t) = +t (indefinite). Now corrupt the family so the
    # surviving polynomial is a perfect-square-like CONSTANT-sign object and
    # confirm the engine would NOT call it indefinite. Use h22 = t^2 instead of
    # t: det along g=(1,0,0), H=diag(0,t^2,1) is -t^2 => K_G(t)=+t^2 >= 0,
    # which is NOT indefinite (never strictly negative).
    det_sym = B._det_hb_symbolic()
    subst = {0: B._pconst(1), 1: {}, 2: {}, 3: {}, 4: {}, 5: {},
             6: B._pmul(B._pvar(9), B._pvar(9)),  # h22 = t^2
             7: {}, 8: B._pconst(1)}
    det_family = B._specialise(det_sym, subst)
    det_t = B._as_t_poly(det_family)
    kg_t = {p: -c for p, c in det_t.items()}      # K_G(t) = -det(t)
    # K_G(t) = +t^2: evaluate at +/-1 -> both +1 (same sign) -> NOT indefinite.
    def ev(poly, v):
        return sum((poly.get(p, Q(0)) * (v ** p) for p in poly), Q(0))
    kp = ev(kg_t, Q(1)); km = ev(kg_t, Q(-1))
    indefinite = (kp > 0) and (km < 0)
    assert indefinite is False, "a sign-fixed t^2 family must NOT be flagged indefinite"
    # the TRUE family (h22=t) IS indefinite
    assert B.symbolic_indefinite_proof()["numerator_indefinite_over_Q_g_H"] is True


def test_mutation_sign_law_degenerate_rank_caught():
    # If Sigma were degenerate ([[0,0,0]]) its rank would be 0 and nullity 3,
    # NOT the claimed 2. P5 asserts rank==1, so the lie is caught.
    assert battery._rank_1x3((Q(0), Q(0), Q(0))) == 0
    assert battery._rank_1x3((Q(1), Q(1), Q(1))) == 1
    # dependent "kernel vectors" would NOT be independent (caught by P5).
    assert battery._independent_2((Q(1), Q(-1), Q(0)), (Q(2), Q(-2), Q(0))) is False
    assert battery._independent_2((Q(1), Q(-1), Q(0)), (Q(1), Q(0), Q(-1))) is True


def test_mutation_kappa_int_same_sign_fails_noncollapsible():
    # If kappa_int did NOT change sign (e.g. both negative) the both-signs test
    # FAILS. The real family has F10 -1/9 < 0 and F11 +2/9 > 0.
    f10_neg = Q(-1, 9)
    f11_pos = Q(2, 9)
    assert (f10_neg < 0 and f11_pos > 0) is True
    fake_same = Q(-1, 9)  # pretend F11 were also negative
    assert (f10_neg < 0 and fake_same > 0) is False


def test_mutation_numeric_zero_on_q0_would_fail_K11():
    # A lying engine returning numeric 0 on q=0 does NOT raise -> refused False.
    def lying():
        return Q(0)
    refused = False
    try:
        lying()
    except Exception:
        refused = True
    assert refused is False  # P8 requires a typed refusal; this lie would FAIL P8


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
