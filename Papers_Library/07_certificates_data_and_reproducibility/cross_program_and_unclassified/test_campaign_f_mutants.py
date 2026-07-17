"""Campaign F — mutation controls (§9, M1..M9).

Each mutant is deliberately wrong; the correct engine passes a check and the
mutant fails the same check (CL-F8).

Run: PYTHONPATH=src pytest -q tests/test_campaign_f_mutants.py
"""

from fractions import Fraction as Q

import pytest

from lloyd_v4.evals.channel_spectrum_carrier.actions import gauge_H
from lloyd_v4.evals.rolechspec_diversity_mechanism import features_structural as FS
from lloyd_v4.evals.rolechspec_diversity_mechanism import gauge_obstruction as GO
from lloyd_v4.evals.rolechspec_diversity_mechanism import mutants as M
from lloyd_v4.evals.rolechspec_diversity_mechanism import theorem_candidates as TC
from lloyd_v4.evals.rolechspec_diversity_mechanism.exact_linear import rank_Q

SURV, COLL = "SURVIVES_ROLECHSPEC", "COLLAPSES_GAUGE_RESIDUAL"
ZERO3 = [[Q(0)] * 3 for _ in range(3)]


# M1 / M2 / M3 / M9 — forbidden feature keys caught by the runtime gate
def test_M1_label_leak_caught():
    with pytest.raises(ValueError):
        FS.assert_no_forbidden(M.mutant_features_label_leak({"diag_support_set_size": 3}))


def test_M2_rolechspec_import_caught():
    with pytest.raises(ValueError):
        FS.assert_no_forbidden(M.mutant_features_rolechspec({"diag_support_set_size": 3}))


def test_M3_gauge_verdict_caught():
    with pytest.raises(ValueError):
        FS.assert_no_forbidden(M.mutant_features_gauge_verdict({"diag_support_set_size": 3}))


def test_M9_n_direct_carriers_caught():
    with pytest.raises(ValueError):
        FS.assert_no_forbidden(M.mutant_features_n_direct({"diag_support_set_size": 3}))


# M4 / M5 — obstruction formula corruption caught by gauge construction
def test_M4_factor2_caught():
    g, a = [Q(2), Q(3), Q(5)], [Q(1), Q(-2), Q(4)]
    dH = gauge_H(g, ZERO3, a)
    assert GO.obstruction(dH, g) == [Q(0)] * 3                 # correct: zero
    assert M.mutant_obstruction_no_factor2(dH, g) != [Q(0)] * 3  # mutant: nonzero


def test_M5_sign_flip_caught():
    g, a = [Q(2), Q(3), Q(5)], [Q(1), Q(-2), Q(4)]
    dH = gauge_H(g, ZERO3, a)
    assert M.mutant_obstruction_sign_flip(dH, g) != [Q(0)] * 3


# M6 — float rank gives a wrong answer on an exact near-singular case
def test_M6_float_rank_caught():
    # second row = 7x first, exactly rank 1; float elimination leaves a residual
    vecs = [[Q(1, 10), Q(2, 10), Q(3, 10)], [Q(7, 10), Q(14, 10), Q(21, 10)]]
    assert rank_Q(vecs) == 1
    assert M.mutant_rank_float(vecs) != 1        # float elimination miscounts as 2


# M7 — shuffled labels break the mechanism alignment
def test_M7_shuffle_labels_caught():
    arecs = [{"class_id": "a", "label": SURV, "obstruction_rank": 1, "diag_support_set_size": 4},
             {"class_id": "b", "label": SURV, "obstruction_rank": 2, "diag_support_set_size": 5},
             {"class_id": "c", "label": COLL, "obstruction_rank": 0, "diag_support_set_size": 1},
             {"class_id": "d", "label": COLL, "obstruction_rank": 0, "diag_support_set_size": 2}]
    assert TC.obstruction_mechanism_verdict(arecs)["verdict"] == "PASS_STRONG"
    shuffled = M.mutant_shuffle_labels(arecs)
    assert TC.obstruction_mechanism_verdict(shuffled)["verdict"] != "PASS_STRONG"


# M8 — dropping reported exceptions caught by completeness
def test_M8_drop_exceptions_caught():
    # synthetic arecs with a planted ge5 counterexample (size 5, obstruction 0)
    arecs = [{"class_id": "x", "label": COLL, "obstruction_rank": 0, "diag_support_set_size": 5},
             {"class_id": "y", "label": SURV, "obstruction_rank": 1, "diag_support_set_size": 5}]
    v = TC.pure_survivor_threshold_verdict(arecs)
    assert v["n_ge5_counterexamples"] == 1                     # correct reports it
    assert M.mutant_drop_exceptions(v)["n_ge5_counterexamples"] == 0  # mutant hides it


def test_all_nine_mutants_registered():
    for name in M.MUTANT_NAMES:
        assert callable(getattr(M, name))
    assert len(M.MUTANT_NAMES) == 9
