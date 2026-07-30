"""Campaign H — raw chart-level RoleChSpec (channels of the full Hessian) and the
characteristic-2 faithfulness resolution (unblocks the CL-H9 open analog).

Truths here are hand-pinned independently of the channel engine:

* the raw channels are DEFINED in char 2 (g-monomial denominators, no 1/(2 g)),
  while the obstruction map O_ij carries a 1/(2 g) (factor-2 denominator);
* over char!=2 the raw object equals the gauge-normal object (CL-H2);
* the explicit char-2 atlas: r1(1,0)=0, r1(0,1)=g_k^2 * S, r2(1,1)=0, and
  r2(2,0)=(g_i g_j)^2 H_kk^2 + g_k^2 ell^2;
* the rank-one phantom g g^T is invisible in char 2 (= G_g(g/2) over Q, but not
  in the diagonal-blind char-2 gauge image);
* the blind spot is exactly <g g^T> (1-dim) -> the naive 4-dim {H11,H22,H33,ell}
  analog fails by one dimension; RoleChSpec is faithful on the 3-dim quotient.

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_raw_chart_rolechspec.py
"""

import sympy as sp

from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import raw_chart_rolechspec as RC
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import symbols as SY

G = SY.g_vec()
H = SY.H_mat()
g1, g2, g3 = SY.g1, SY.g2, SY.g3
H11, H22, H33 = SY.H11, SY.H22, SY.H33
H12, H13, H23 = SY.H12, SY.H13, SY.H23


def eq2(a, b):
    """Equal mod 2 (a, b polynomials/channels): reduce the difference over GF(2)."""
    return RC.char2_numerator(a - b) == 0


# ---- ell and its char-2 cokernel property ------------------------------------
def test_ell_definition():
    assert sp.expand(RC.ell(G, H) - (g3 * H12 + g2 * H13 + g1 * H23)) == 0


def test_ell_annihilates_offdiag_gauge_in_char2():
    # off-diagonal gauge shift b: ell changes by 2*(...) = 0 in char 2
    b1, b2, b3 = sp.symbols("b1 b2 b3")
    o12, o13, o23 = g1 * b2 + b1 * g2, g1 * b3 + b1 * g3, g2 * b3 + b2 * g3
    Hg = sp.Matrix([[H11, H12 + o12, H13 + o13],
                    [H12 + o12, H22, H23 + o23],
                    [H13 + o13, H23, H33]])
    delta = sp.expand(RC.ell(G, Hg) - RC.ell(G, H))
    assert delta == 2 * (g1 * g3 * b2 + g2 * g3 * b1 + g1 * g2 * b3)  # = 0 in char 2
    assert RC.char2_numerator(delta) == 0


# ---- defined in char 2 (the obstruction map is not) --------------------------
def test_raw_channels_defined_in_char2():
    res = RC.defined_in_char2()
    assert res["defined_in_char2"] is True, res["violations"]


def test_obstruction_map_carries_factor_two():
    # contrast: O_ij = H_ij - g_i H_jj/(2 g_j) - g_j H_ii/(2 g_i) has a 1/(2 g)
    O12 = H12 - g1 * H22 / (2 * g2) - g2 * H11 / (2 * g1)
    den = sp.together(O12).as_numer_denom()[1]
    assert int(den.subs({g1: 1, g2: 1, g3: 1})) % 2 == 0  # even -> undefined in char 2


# ---- char!=2 agreement with the gauge-normal object (CL-H2) ------------------
def test_agrees_with_gauge_normal_over_Q():
    res = RC.agrees_with_gauge_normal_over_Q()
    assert res["agrees_over_Q"] is True, res["mismatches"]


# ---- explicit char-2 atlas ---------------------------------------------------
def test_atlas_r1_offdiag_and_r2_mixed_vanish():
    atlas = RC.char2_atlas()
    for k in (0, 1, 2):
        assert atlas[(k, 1, (1, 0))] == 0
        assert atlas[(k, 2, (1, 1))] == 0


def test_atlas_r1_diagonal_channel():
    S = H11 * (g2**2 + g3**2) + H22 * (g1**2 + g3**2) + H33 * (g1**2 + g2**2)
    atlas = RC.char2_atlas()
    for k, gk in ((0, g1), (1, g2), (2, g3)):
        assert eq2(atlas[(k, 1, (0, 1))], gk**2 * S)


def test_atlas_r2_diagonal_channel_role2_handpinned():
    # role-2 (2,0) numerator, written out by hand (no module helper):
    expected = H12**2 * g3**4 + H13**2 * g2**2 * g3**2 + H23**2 * g1**2 * g3**2 \
        + H33**2 * g1**2 * g2**2
    atlas = RC.char2_atlas()
    assert eq2(atlas[(2, 2, (2, 0))], expected)
    # and it equals the closed form (g1 g2)^2 H33^2 + g3^2 ell^2
    assert eq2(expected, (g1 * g2)**2 * H33**2 + g3**2 * RC.ell(G, H)**2)


def test_r2_diag_form_all_roles():
    forms = RC.char2_r2_diag_form()
    atlas = RC.char2_atlas()
    for k in (0, 1, 2):
        assert eq2(atlas[(k, 2, (2, 0))], forms[k])


# ---- the raw RoleChSpec is char-2 gauge invariant ----------------------------
def test_char2_gauge_invariant():
    assert RC.char2_gauge_invariant()["char2_gauge_invariant"] is True


# ---- phantom direction g g^T -------------------------------------------------
def test_grad_outer_is_g_gT():
    M = RC.grad_outer(G)
    assert sp.expand(M[0, 0] - g1**2) == 0 and sp.expand(M[1, 2] - g2 * g3) == 0


def test_grad_outer_invisible_in_char2():
    assert RC.grad_outer_invisible_char2()["invisible"] is True


def test_grad_outer_not_in_char2_gauge_image():
    # the char-2 gauge is diagonal-blind; g g^T has nonzero diagonal g_i^2
    M = RC.grad_outer(G)
    assert [M[i, i] for i in range(3)] == [g1**2, g2**2, g3**2]


# ---- blind spot is exactly 1-dimensional = <g g^T> ---------------------------
def test_blind_spot_is_exactly_grad_outer():
    for gp in ((1, 3, 5), (3, 5, 7), (9, 1, 11)):
        res = RC.char2_blind_spot(gp)
        assert res["nonzero_blind"] == [res["grad_outer_rep"]]


def test_blind_spot_excludes_nonphantom_directions():
    # CONTROL against a degenerate (all-zero) engine: a pure diagonal E11 bump and
    # the ell-carrier E12 must be VISIBLE (not blind), else "invisible" is vacuous.
    res = RC.char2_blind_spot((1, 3, 5))
    assert (1, 0, 0, 0) not in res["nonzero_blind"]   # E11 visible
    assert (0, 0, 0, 1) not in res["nonzero_blind"]   # E12 (ell) visible
    # and the channels are not identically zero mod 2
    atlas = RC.char2_atlas()
    assert atlas[(2, 2, (2, 0))] != 0


# ---- assembled verdict -------------------------------------------------------
def test_char2_faithfulness_verdict():
    v = RC.char2_faithfulness()
    assert v["naive_4dim_quotient"]["faithful"] is False
    assert v["phantom_invisible"] is True
    assert v["blind_spot_dim"] == 1
    assert v["blind_spot_is_grad_outer"] is True
    assert v["corrected_quotient"]["dim"] == 3
    assert v["corrected_quotient"]["faithful"] is True
