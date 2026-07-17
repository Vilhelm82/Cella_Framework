"""Campaign D — mutation controls (§6).

Each mutant is deliberately wrong; for each, the correct engine passes a check
and the mutant fails the same check. Proves the suite catches a lying engine.

Run: PYTHONPATH=src pytest -q tests/test_active_role_mutants.py
"""

from fractions import Fraction as Q

import pytest

from lloyd_v4.evals.channel_spectrum_carrier import carrier as CA
from lloyd_v4.evals.channel_spectrum_carrier.actions import gauge_H
from lloyd_v4.evals.active_role_channel_carrier import fixtures as F
from lloyd_v4.evals.active_role_channel_carrier import implicit_graph as IG
from lloyd_v4.evals.active_role_channel_carrier import mutants as M
from lloyd_v4.evals.active_role_channel_carrier import role_spec as RS
from lloyd_v4.evals.active_role_channel_carrier import serialize as S
from lloyd_v4.evals.active_role_channel_carrier.gauge_solver import (
    GAUGE_EQUIVALENT, GAUGE_NOT_EQUIVALENT, gauge_solve,
)

G, H = IG.graph_jet_to_implicit(2, 3, 5, 7, 11)
# CL-D3 truth by output role: k=2 Product, k=0 Directive, k=1 Substrate
TRUTH = {
    2: {"K": Q(3, 98), "kappa_c": Q(-1, 4), "kappa_int": Q(0), "kappa_s": Q(55, 196)},
    0: {"K": Q(3, 98), "kappa_c": Q(-1, 784), "kappa_int": Q(0), "kappa_s": Q(25, 784)},
    1: {"K": Q(3, 98), "kappa_c": Q(-1, 1764), "kappa_int": Q(0), "kappa_s": Q(55, 1764)},
}


def _named(chart):
    g_c, H_c = chart
    q = sum(x * x for x in g_c)
    c2 = CA.channel_vector(g_c, H_c, 2)
    return {"kappa_c": c2[(2, 0)] / q ** 2, "kappa_int": c2[(1, 1)] / q ** 2,
            "kappa_s": c2[(0, 2)] / q ** 2, "K": sum(c2.values()) / q ** 2}


# 1) graph 2nd-derivative missing H_kk term
def test_mutant_missing_Hkk_caught():
    for k in (0, 1, 2):                                            # correct reproduces CL-D3
        assert RS.output_role_carrier(G, H, k)["named"] == TRUTH[k]
    # mutant fails CL-D3 on at least one role (roles where H_kk != 0)
    assert any(_named(M.mutant_rechart_missing_Hkk(G, H, k)) != TRUTH[k] for k in (0, 1, 2))


# 2) graph 1st-derivative wrong sign
def test_mutant_first_derivative_wrong_sign_caught():
    for k in (0, 1, 2):
        assert RS.output_role_carrier(G, H, k)["named"] == TRUTH[k]
    assert any(_named(M.mutant_rechart_wrong_sign(G, H, k)) != TRUTH[k] for k in (0, 1, 2))


# 3) RoleChSpec returns the direct carrier -> not gauge-invariant
def test_mutant_rolechspec_direct_caught():
    a = [Q(1), Q(-2), Q(3)]
    Hg = gauge_H(G, H, a)
    assert RS.rolechspec_fingerprint(G, Hg) == RS.rolechspec_fingerprint(G, H)   # correct invariant
    assert M.mutant_rolechspec_direct(G, Hg) != M.mutant_rolechspec_direct(G, H)  # mutant changes


# 4) gauge solver false negative -> caught by a true gauge pair
def test_mutant_gauge_false_negative_caught():
    p = F.pair_by_id("n3_gauge_pair_keystone")
    assert gauge_solve(p["g"], p["H1"], p["H2"])["status"] == GAUGE_EQUIVALENT     # correct
    assert M.mutant_gauge_false_negative(p["g"], p["H1"], p["H2"])["status"] != GAUGE_EQUIVALENT


# 5) gauge solver false positive -> caught by a non-gauge pair
def test_mutant_gauge_false_positive_caught():
    p = F.pair_by_id("n3_nongauge_pair")
    assert gauge_solve(p["g"], p["H1"], p["H2"])["status"] == GAUGE_NOT_EQUIVALENT  # correct
    assert M.mutant_gauge_false_positive(p["g"], p["H1"], p["H2"])["status"] != GAUGE_NOT_EQUIVALENT


# 6) passive permutation reported as active role orbit
def test_mutant_passive_as_active_caught():
    assert RS.active_role_carrier_size(G, H) == 3                 # correct active size
    assert M.mutant_active_size_via_passive(G, H) == 1            # mutant (passive orbit) trivial
    assert RS.active_role_carrier_size(G, H) != M.mutant_active_size_via_passive(G, H)


# 7) zero role denominator divides -> raw exception
def test_mutant_zero_denominator_divides_caught():
    f = F.by_id("n3_singular_output_role0")
    assert IG.rechart(f["g"], f["H"], 0) == IG.ROLE_CHART_UNAVAILABLE   # correct: typed status
    with pytest.raises(ZeroDivisionError):
        M.mutant_rechart_zero_divide(f["g"], f["H"], 0)                  # mutant: raw crash


# 8) float normalization -> serializer / parity gate
def test_mutant_float_normalization_caught():
    good = S.normalize_coefficient(Q(6), Q(7, 2), 1)
    assert good["rational"] is False and "value" not in good      # correct refuses
    bad = M.mutant_normalize_float(Q(6), Q(7, 2), 1)
    assert isinstance(bad["value"], float)                        # mutant lies
    with pytest.raises(TypeError):
        S.to_canonical(bad["value"])                              # serializer catches


def test_all_eight_mutants_registered():
    for name in M.MUTANT_NAMES:
        assert callable(getattr(M, name))
    assert len(M.MUTANT_NAMES) == 8
