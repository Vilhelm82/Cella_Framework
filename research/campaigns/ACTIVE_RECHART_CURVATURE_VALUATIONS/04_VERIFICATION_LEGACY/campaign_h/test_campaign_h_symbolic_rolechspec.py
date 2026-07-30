"""Campaign H — symbolic RoleChSpec on the gauge-normal form (Lemma H2/H3).

Closed rational formulas for the active graph-chart channel vectors in terms of
(g, O); RoleChSpec depends only on the gauge-normal carrier (gauge invariance,
Lemma H2 / CL-H2). The r=2 density channels are quadratic (even) in O with
kappa_int = 0; the r=1 channels are linear (odd).

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_symbolic_rolechspec.py
"""

import sympy as sp

from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import rolechspec_symbolic as RS
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import symbols as SY

G = SY.g_vec()
HP = SY.H_perp_mat()                       # H_perp(O12,O13,O23)
OVARS = [SY.O12, SY.O13, SY.O23]


def test_kappa_int_zero_all_roles():
    for k in (2, 0, 1):
        assert sp.simplify(RS.channel_vector(G, HP, k, 2)[(1, 1)]) == 0


def test_q_chart_depends_only_on_g():
    for k in (2, 0, 1):
        q = RS.q_chart(G, HP, k)
        for o in OVARS:
            assert sp.simplify(sp.diff(q, o)) == 0


def test_r1_channels_linear_in_O():
    for k in (2, 0, 1):
        for comp in RS.channel_vector(G, HP, k, 1).values():
            num = sp.numer(sp.cancel(comp))
            assert sp.Poly(num, *OVARS).total_degree() == 1


def test_r2_channels_quadratic_even_in_O():
    for k in (2, 0, 1):
        for comp in RS.channel_vector(G, HP, k, 2).values():
            num = sp.numer(sp.cancel(comp))
            if num == 0:
                continue
            p = sp.Poly(num, *OVARS)
            assert p.total_degree() == 2
            # even: invariant under O -> -O
            assert sp.simplify(num.subs({o: -o for o in OVARS}) - num) == 0


def test_lemma_H3_product_self_channel_hand_pinned():
    # Product chart (k=2): kappa_hat_(0,2) = 4 g1 g2 O13 O23 / g3^4
    expr = RS.channel_vector(G, HP, 2, 2)[(0, 2)]
    expected = 4 * SY.g1 * SY.g2 * SY.O13 * SY.O23 / SY.g3 ** 4
    assert sp.simplify(expr - expected) == 0


def test_CLH2_gauge_normal_reduction():
    # RoleChSpec(g, H_perp(O)) is invariant under adding a gauge G_g(b)
    from lloyd_v4.evals.rolechspec_symbolic_proof_extraction.gauge_normal_form import G_g
    b = list(sp.symbols('b1 b2 b3'))
    Hg = sp.expand(HP + G_g(G, b))
    for k in (2, 0, 1):
        for r in (1, 2):
            a = RS.channel_vector(G, HP, k, r)
            c = RS.channel_vector(G, Hg, k, r)
            for key in a:
                assert sp.simplify(a[key] - c[key]) == 0
