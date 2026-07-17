"""Campaign G — mutation controls (§10, M1..M10).

Run: PYTHONPATH=src pytest -q tests/test_campaign_g_mutants.py
"""

from fractions import Fraction as Q

from lloyd_v4.evals.rolechspec_gauge_obstruction_faithfulness import gauge_map as GM
from lloyd_v4.evals.rolechspec_gauge_obstruction_faithfulness import mutants as M
from lloyd_v4.evals.rolechspec_gauge_obstruction_faithfulness import obstruction as OB
from lloyd_v4.evals.rolechspec_gauge_obstruction_faithfulness import rolechspec_local as RL
from lloyd_v4.evals.rolechspec_gauge_obstruction_faithfulness.exact_linear import rank_q

ZERO3 = [[Q(0)] * 3 for _ in range(3)]
G = [Q(2), Q(3), Q(5)]
A = [Q(1), Q(-2), Q(4)]
DH = GM.G_g(G, A)                      # a true gauge difference (O = 0)


def test_M1_factor2_caught():
    assert OB.obstruction(G, DH) == [Q(0)] * 3
    assert M.mutant_obstruction_no_factor2(G, DH) != [Q(0)] * 3


def test_M2_sign_caught():
    assert M.mutant_obstruction_sign(G, DH) != [Q(0)] * 3


def test_M3_float_rank_caught():
    vecs = [[Q(1, 10), Q(2, 10), Q(3, 10)], [Q(7, 10), Q(14, 10), Q(21, 10)]]
    assert rank_q(vecs) == 1
    assert M.mutant_float_rank(vecs) != 1


def test_M4_cached_rolechspec_caught():
    # two genuinely different regular jets -> correct distinguishes, cache equates
    g = [Q(1), Q(1), Q(1)]
    H1 = [[Q(1), Q(0), Q(0)], [Q(0), Q(0), Q(0)], [Q(0), Q(0), Q(0)]]
    H2 = [[Q(0), Q(1), Q(0)], [Q(1), Q(0), Q(0)], [Q(0), Q(0), Q(0)]]
    assert RL.rolechspec_equal(g, H1, H2) is False
    assert M.mutant_cached_equal(g, H1, H2) is True


def test_M5_accept_singular_caught():
    g = [Q(0), Q(1), Q(1)]
    assert RL.regularity(g, ZERO3) == RL.ROLE_CHART_UNAVAILABLE
    assert M.mutant_accept_singular(g, ZERO3) == RL.REGULAR


def test_M6_shuffle_rolechspec_caught():
    # gauge pair: correct RoleChSpec equal, mutant (raw entries) differs
    g = [Q(3), Q(1), Q(2)]
    H1 = [[Q(2), Q(1), Q(0)], [Q(1), Q(0), Q(0)], [Q(0), Q(0), Q(2)]]
    H2 = [[H1[i][j] + GM.G_g(g, [Q(1), Q(-2), Q(3)])[i][j] for j in range(3)] for i in range(3)]
    assert RL.rolechspec_equal(g, H1, H2) is True
    assert M.mutant_shuffle_equal(g, H1, H2) is False


def test_M7_skip_self_glue_caught():
    res = M.mutant_skip_self_glue()
    # claims PASS but ran nothing -> completeness check (PASS requires samples)
    assert res["status"] == "PASS" and res["n_samples"] == 0


def test_M8_suppress_counterexamples_caught():
    real = {"faithfulness_counterexamples": [{"type": "faithfulness_failure"}]}
    assert len(real["faithfulness_counterexamples"]) == 1
    assert M.mutant_suppress_counterexamples(real)["faithfulness_counterexamples"] == []


def test_M9_weak_equal_caught():
    fp1 = ("a" * 30,)
    fp2 = ("a" * 30 + "X",)
    assert (fp1 == fp2) is False
    assert M.mutant_weak_equal(fp1, fp2) is True


def test_M10_forbidden_import_caught():
    src = M.mutant_forbidden_import_source()
    assert "labels import" in src and "SURVIVES" in src     # a source scan flags it


def test_all_ten_mutants_registered():
    for name in M.MUTANT_NAMES:
        assert callable(getattr(M, name))
    assert len(M.MUTANT_NAMES) == 10
