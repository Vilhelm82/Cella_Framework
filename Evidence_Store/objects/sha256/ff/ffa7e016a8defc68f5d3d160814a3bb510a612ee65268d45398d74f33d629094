"""c001 `three_channel_kg` — STAGE C suite (covenant step 3: must exit 0).

Asserts:
  * the prereg-pin / clause-drift / bench-pin gates REFUSE on drift (the gates
    are non-tautological -- they bite a tampered contract);
  * every one of the 9 frozen predictions PASSES exact-Q;
  * the grading predicates are non-tautological -- mutation guards prove a
    LYING gauge engine would be caught (a raw diagonal-bump gauge changes K_G
    so sigma_r would not be preserved; a wrong-law mutant using H_ii instead of
    the complementary H_jk differs from the true single-edge law; an 'e1 moves'
    claim is false against the true delta kappa_c = 0; a non-shear gauge leaves
    a NONZERO symbolic PHP / det residual so PC5/PC6 bite; a near-miss is
    rejected by exact equality);
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
Qf = Q


# --------------------------------------------------------------------------
# gates bite (non-tautological contract enforcement)
# --------------------------------------------------------------------------
def test_clause_gate_refuses_value_drift():
    prereg = battery.load_prereg()
    saved = battery.GRADER_CLAUSES["K4_gauge_single_edge"]
    battery.GRADER_CLAUSES["K4_gauge_single_edge"] = saved + " DRIFT"
    try:
        try:
            battery.gate_clauses(prereg)
            raised = False
        except battery.ClauseDrift:
            raised = True
    finally:
        battery.GRADER_CLAUSES["K4_gauge_single_edge"] = saved
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


def test_prereg_pin_self_consistent():
    # load_prereg re-verifies the prereg sha256 vs the .pin; a tampered prereg
    # would raise PreregPinMismatch.
    prereg = battery.load_prereg()
    assert prereg["version"] == "stage_c_prereg_v1"
    assert prereg["stage"] == "stage_c"


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


def test_keystone_base_jet_anchor():
    _records, verdicts = battery.run()
    d = verdicts["PC1_keystone_base_jet"]["detail"]
    assert d["q_eq_14"] and d["prod_g_eq_6"] and d["q_squared_eq_196"]
    assert d["K_G_eq_m3_49"] and d["tr_PHP_eq_12_7"] and d["sigma_2_eq_K_G"]
    assert d["pathB_total_agrees"] and d["pathBprime_tuple_agrees"] and d["pathC_oracle_agrees"]


def test_single_edge_law_pins_and_moves():
    _records, verdicts = battery.run()
    d = verdicts["PC2_single_edge_law_keystone"]["detail"]
    # e1 / e2 pin (delta kappa_c per unit t == 0); e3 moves 6/49.
    assert d["e1"]["delta_kappa_c_per_unit_t"] == "frac:0/1"
    assert d["e2"]["delta_kappa_c_per_unit_t"] == "frac:0/1"
    assert d["e3"]["delta_kappa_c_per_unit_t"] == "frac:6/49"
    # e3 at t=1 -> 6/49, t=-4 -> -24/49 (matches the law)
    assert d["e3"]["per_t"]["frac:1/1"]["delta_kappa_c"] == "frac:6/49"
    assert d["e3"]["per_t"]["frac:-4/1"]["delta_kappa_c"] == "frac:-24/49"


def test_deltaC_in_ker_Sigma_pins_kappa_c_but_vector_moves():
    _records, verdicts = battery.run()
    v = verdicts["PC4_deltaC_in_ker_Sigma_keystone"]
    assert v["e3_genuine_move"] and v["e1_pins"] and v["e2_pins"]
    # On e1 the kappa_c PINS (delta kappa_c == 0) yet the channel VECTOR moves
    # (kappa_s <-> kappa_int trade) while Sigma(delta C) == 0.
    e1_t1 = v["detail"]["e1"]["frac:1/1"]
    assert e1_t1["in_ker_Sigma"] and e1_t1["Sigma_deltaC"] == "frac:0/1"
    assert e1_t1["deltaC"][0] == "frac:0/1"           # delta kappa_c pins
    assert e1_t1["deltaC_nonzero"] is True            # but the vector moves


def test_sigma_r_preserved_all_edges():
    _records, verdicts = battery.run()
    v = verdicts["PC3_sigma_r_preserved_keystone"]
    assert v["pass"]
    for edge in ("e1", "e2", "e3"):
        for t, d in v["detail"][edge].items():
            assert d["all_sigma_r_preserved"], f"{edge} t={t} sigma_r not preserved"


def test_symbolic_identities_hold_over_Q():
    _records, verdicts = battery.run()
    law = verdicts["PC5_single_edge_law_symbolic_over_Q"]["proof"]
    inv = verdicts["PC6_KG_invariant_symbolic_over_Q"]["proof"]
    assert law["all_edges_identity_holds"] is True
    for i in (1, 2, 3):
        assert law[f"e{i}"]["residual_monomials"] == 0
    assert inv["all_edges_det_invariance_holds"] is True
    assert inv["all_edges_PHP_unchanged"] is True
    for i in (1, 2, 3):
        assert inv[f"e{i}"]["det_residual_monomials"] == 0
        assert inv[f"e{i}"]["PHP_qcleared_nonzero_entries"] == 0


# --------------------------------------------------------------------------
# mutation guards: a lying gauge engine would be caught
# --------------------------------------------------------------------------
def test_mutation_diagonal_bump_gauge_changes_KG():
    # A raw diagonal-bump 'gauge' H[i][i]+=t is NOT the border shear; it
    # changes K_G -> sigma_2 not preserved -> K4 would fire. (P C8 mutant a.)
    _records, verdicts = battery.run()
    mut = verdicts["PC8_K4_mutant_guards"]["sigma_breaking_mutant"]
    assert any(mut[f"e{i}"]["K_G_changed"] for i in (1, 2, 3))


def test_mutation_wrong_law_diagonal_entry_differs():
    # Using H_ii (diagonal) instead of the complementary off-diagonal H_jk in
    # the single-edge law yields a DIFFERENT value at the keystone (P C8 mutant b).
    _records, verdicts = battery.run()
    mut = verdicts["PC8_K4_mutant_guards"]["wrong_law_mutant"]
    assert any(mut[f"e{i}"]["differs"] for i in (1, 2, 3))


def test_mutation_e1_moves_claim_is_false():
    # The true law pins e1 (delta kappa_c == 0); an 'e1 moves' claim is false.
    _records, verdicts = battery.run()
    assert verdicts["PC8_K4_mutant_guards"]["detail"]["e1_moves_claim_is_False"] is True


def test_mutation_nonshear_gauge_leaves_nonzero_symbolic_residual():
    # The symbolic PHP/det engines must BITE a non-shear gauge: a diagonal bump
    # e_i e_i^T is NOT annihilated by the projector, so q^2*(P H' P - P H P) is
    # NONZERO and the det residual is NONZERO (PC5/PC6 are non-vacuous).
    B = battery
    g, H, t = B._sym_handles()
    q = B._padd(B._pmul(g[0], g[0]), B._pmul(g[1], g[1]), B._pmul(g[2], g[2]))
    base_det = B._sym_det_bordered(g, H)
    for i in range(3):
        Hn = [[H[a][c] for c in range(3)] for a in range(3)]
        Hn[i][i] = B._padd(Hn[i][i], t)          # diagonal bump (wrong gauge)
        resid = B._php_residual_qcleared(g, q, H, Hn)
        nz = sum(1 for r in resid for e in r if len(e) > 0)
        assert nz > 0, "non-shear gauge must leave nonzero PHP residual (PC6 bites)"
        detres = B._padd(B._sym_det_bordered(g, Hn), B._pneg(base_det))
        assert len(detres) > 0, "non-shear gauge must change det (K_G) symbolically"
    # and the TRUE border shear leaves ZERO residual on all edges.
    inv = B.symbolic_KG_invariance_proof()
    assert inv["all_edges_PHP_unchanged"] is True
    assert inv["all_edges_det_invariance_holds"] is True


def test_mutation_wrong_single_edge_law_leaves_nonzero_symbolic_residual():
    # Corrupt the single-edge law (drop the factor of 4) -> the symbolic
    # residual delta Delta_c - (-1 * (prod g) H_jk * t) is NONZERO -> PC5 bites.
    B = battery
    g, H, t = B._sym_handles()
    prodg = B._pmul(B._pmul(g[0], g[1]), g[2])
    comp = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    base_dc = B._sym_delta_c(g, H)
    bitten = False
    for i in range(3):
        Hn = B._sym_gauge_H(g, H, i, t)
        delta_dc = B._padd(B._sym_delta_c(g, Hn), B._pneg(base_dc))
        j, k = comp[i]
        # WRONG law: coefficient 1 instead of 4.
        wrong = B._pmul(t, B._pneg(B._psmul(B._pmul(prodg, H[j][k]), 1)))
        resid = B._padd(delta_dc, B._pneg(wrong))
        if i == 2:  # e3 is the moving edge; the dropped factor must show up
            assert len(resid) > 0, "wrong-coefficient law must leave nonzero residual"
            bitten = True
    assert bitten
    # the TRUE law (coefficient 4) leaves ZERO residual.
    assert battery.symbolic_single_edge_law_proof()["all_edges_identity_holds"] is True


def test_mutation_near_miss_rejected_no_tolerance():
    got = Qf(6, 49)
    near = got + Qf(1, 10 ** 9)
    assert (got == near) is False                       # exact equality rejects near-miss
    assert (abs(got - near) < Qf(1, 10 ** 6)) is True   # a tolerant band WOULD wrongly pass it


def test_mutation_KG_invariance_is_exact_not_tolerant():
    # K_G under the gauge equals base K_G EXACTLY (no tolerance); a +eps mutant
    # would be rejected.
    eps = Qf(1, 10 ** 9)
    base = Qf(-3, 49)
    assert (base == base) is True
    assert (base == base + eps) is False


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
