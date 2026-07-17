"""Campaign H — mutation controls (§10, M1..M10).

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_mutants.py
"""

import sympy as sp

from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import exceptional_locus as EL
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import gauge_normal_form as GN
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import injectivity_ideal as IJ
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import mutants as M
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import rolechspec_symbolic as RS
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import symbols as SY

G, H = SY.g_vec(), SY.H_mat()
HP = SY.H_perp_mat()


def test_M1_wrong_gauge_factor_caught():
    assert all(sp.simplify(GN.H_perp(G, H)[i, i]) == 0 for i in range(3))   # correct
    bad = M.mutant_gauge_coeffs_no2(G, H)
    assert any(sp.simplify(bad[i, i]) != 0 for i in range(3))               # mutant diag nonzero


def test_M2_wrong_obstruction_sign_caught():
    O_good = GN.obstruction(G, H)
    O_bad = M.mutant_obstruction_sign(G, H)
    assert sp.simplify(O_good[0] - O_bad[0]) != 0


def test_M3_keep_diagonal_caught():
    assert all(sp.simplify(GN.H_perp(G, H)[i, i]) == 0 for i in range(3))
    bad = M.mutant_keep_diagonal(G, H)
    assert any(sp.simplify(bad[i, i]) != 0 for i in range(3))


def test_M4_unsaturated_injectivity_caught():
    # a factor with a regular rational zero (g1=g2) must be rejected by saturation
    assert IJ.nonzero_on_regular_Q(SY.g1 - SY.g2, [SY.g1, SY.g2, SY.g3]) is False
    assert M.mutant_unsaturated_nonzero(SY.g1 - SY.g2, [SY.g1, SY.g2, SY.g3]) is True


def test_M5_drop_role_caught():
    comps = RS.rolechspec_components(G, HP)
    assert set(comps) == {0, 1, 2}                          # full RoleChSpec: 3 roles
    assert set(M.mutant_drop_role(comps)) != {0, 1, 2}      # mutant drops one


def test_M6_hash_equality_caught():
    e1 = (SY.O12 + SY.O13) ** 2
    e2 = SY.O12 ** 2 + 2 * SY.O12 * SY.O13 + SY.O13 ** 2
    assert sp.simplify(e1 - e2) == 0                        # symbolically equal
    assert M.mutant_hash_equal(e1, e2) is False             # hash says unequal


def test_M7_float_substitution_caught():
    expr = sp.Rational(1, 10 ** 12)                         # exactly nonzero
    assert (expr == 0) is False                             # exact
    assert M.mutant_is_zero_float(expr, {}) is True         # float tolerance lies


def test_M8_ignore_exceptional_component_caught():
    rep = EL.exceptional_report(G)
    assert rep["typed_strata"] and rep["sum_of_squares_factor"]
    assert not M.mutant_drop_exceptional(rep)["typed_strata"]


def test_M9_cached_rolechspec_caught():
    # two different gauge-normal jets -> recomputation distinguishes, cache equates
    from lloyd_v4.evals.active_role_channel_carrier.role_spec import rolechspec_fingerprint
    from fractions import Fraction as Q
    g = [Q(1), Q(1), Q(1)]
    H1 = [[Q(0), Q(1), Q(0)], [Q(1), Q(0), Q(0)], [Q(0), Q(0), Q(0)]]
    H2 = [[Q(0), Q(0), Q(1)], [Q(0), Q(0), Q(0)], [Q(1), Q(0), Q(0)]]
    assert (rolechspec_fingerprint(g, H1) == rolechspec_fingerprint(g, H2)) is False
    assert M.mutant_cached_equal(g, H1, H2) is True


def test_M10_trivial_identity_caught():
    res = M.mutant_trivial_identity()
    assert res["theorem_proved"] is True and res["injectivity_checked"] is False  # incomplete


def test_all_ten_mutants_registered():
    for name in M.MUTANT_NAMES:
        assert callable(getattr(M, name))
    assert len(M.MUTANT_NAMES) == 10
