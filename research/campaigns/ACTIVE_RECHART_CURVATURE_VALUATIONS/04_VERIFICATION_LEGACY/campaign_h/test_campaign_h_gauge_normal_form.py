"""Campaign H — gauge-normal form (Lemma H1, CL-H1).

H_perp = H - G_g(a) with a_i = H_ii/(2 g_i) has zero diagonal and off-diagonals
exactly the obstruction coordinates. Sym_3(Q)/Im(G_g) ~= Q^3 via H -> O_g(H).

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_gauge_normal_form.py
"""

import sympy as sp

from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import gauge_normal_form as GN
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import symbols as SY


def test_H_perp_zero_diagonal():
    g, H = SY.g_vec(), SY.H_mat()
    Hp = GN.H_perp(g, H)
    for i in range(3):
        assert sp.simplify(Hp[i, i]) == 0


def test_H_perp_offdiag_is_obstruction():
    g, H = SY.g_vec(), SY.H_mat()
    Hp, O = GN.H_perp(g, H), GN.obstruction(g, H)
    assert sp.simplify(Hp[0, 1] - O[0]) == 0
    assert sp.simplify(Hp[0, 2] - O[1]) == 0
    assert sp.simplify(Hp[1, 2] - O[2]) == 0


def test_G_g_symmetric():
    g = SY.g_vec()
    a = list(sp.symbols('a1 a2 a3'))
    M = GN.G_g(g, a)
    for i in range(3):
        for j in range(3):
            assert sp.simplify(M[i, j] - M[j, i]) == 0


def test_gauge_image_rank_is_3():
    assert GN.gauge_image_rank(SY.g_vec()) == 3


def test_obstruction_is_gauge_invariant():
    # O(H + G_g(b)) == O(H): the map descends to the quotient
    g, H = SY.g_vec(), SY.H_mat()
    b = list(sp.symbols('b1 b2 b3'))
    O1 = GN.obstruction(g, H)
    O2 = GN.obstruction(g, sp.expand(H + GN.G_g(g, b)))
    for i in range(3):
        assert sp.simplify(O2[i] - O1[i]) == 0


def test_quotient_iso_Q3():
    # H -> O_g(H) is surjective onto Q^3 (Jacobian rank 3) and Im(G_g) (rank 3)
    # is its kernel -> Sym_3/Im(G_g) ~= Q^3.
    g, H = SY.g_vec(), SY.H_mat()
    O = GN.obstruction(g, H)
    syms = [SY.H11, SY.H22, SY.H33, SY.H12, SY.H13, SY.H23]
    Jac = sp.Matrix([[sp.diff(O[i], v) for v in syms] for i in range(3)])
    assert Jac.rank() == 3
    assert GN.gauge_image_rank(g) == 3
