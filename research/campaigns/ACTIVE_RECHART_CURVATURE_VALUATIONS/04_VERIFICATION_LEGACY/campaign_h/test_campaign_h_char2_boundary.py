"""Campaign H — characteristic boundary (CL-H8 char != 2 cert, CL-H9 char-2 wall).

CL-H8: the coupling-channel minor det(rows 0,2,4) of the r=1 coefficient matrix
is 32/(g1 g2 g3); its numerator is the unit 32 = 2^5, so r=1 recovery is full
rank on the regular locus over any field where 2 is invertible (char != 2) --
an explicit single-minor certificate, stronger than the over-Q headline.

CL-H9: char != 2 is a derived structural wall. In char 2 the gauge G_g(a)_ii =
2 g_i a_i is diagonal-blind; the off-diagonal gauge map has det -2 g1 g2 g3 (= 0
in char 2), rank drops 3 -> 2, Im(G_g) drops 3 -> 2, the quotient is k^4 (not the
k^3 carrier O), with new invariants {H11, H22, H33, ell = g3 O12 + g2 O13 + g1 O23}.

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_char2_boundary.py
"""

import sympy as sp

from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import char_boundary as CB
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import symbols as SY

G = SY.g_vec()


# ---- CL-H8: explicit single-minor certificate over char != 2 ----
def test_coupling_minor_is_32_over_g1g2g3():
    minor = CB.coupling_minor(G)
    assert sp.simplify(minor - sp.Integer(32) / (SY.g1 * SY.g2 * SY.g3)) == 0


def test_explicit_minor_certificate():
    cert = CB.explicit_minor_certificate(G)
    assert cert["numerator"] == 32
    assert cert["numerator_is_unit"] is True
    assert sp.simplify(cert["denominator"] - SY.g1 * SY.g2 * SY.g3) == 0
    assert cert["char_ceiling"] == "char != 2"
    assert cert["injective_on_regular_locus_char_ne_2"] is True


# ---- CL-H9: char-2 gauge-rank collapse ----
def test_offdiag_gauge_det_is_minus_2g1g2g3():
    assert sp.simplify(CB.offdiag_gauge_det(G) + 2 * SY.g1 * SY.g2 * SY.g3) == 0


def test_gauge_rank_char0_is_3_char2_is_2():
    assert CB.gauge_rank_char0(G) == 3
    assert CB.gauge_rank_char2(G) == 2


def test_quotient_dim_3_vs_4():
    assert CB.char0_quotient_dim(G) == 3
    assert CB.char2_quotient_dim(G) == 4


def test_cokernel_invariant_ell():
    # ell(G_g(a)) = 2 * (...) -> vanishes on Im(G_g) in char 2; not in char != 2
    ell_on_image = CB.ell_on_gauge_image(G)
    assert sp.simplify(ell_on_image - 2 * (SY.g1 * SY.g2 * sp.Symbol('a3')
                                           + SY.g1 * SY.g3 * sp.Symbol('a2')
                                           + SY.g2 * SY.g3 * sp.Symbol('a1'))) == 0


def test_char2_invariants_named():
    inv = CB.char2_invariants()
    assert inv["diagonal"] == ["H11", "H22", "H33"]
    assert sp.simplify(inv["offdiagonal_ell"]
                       - (SY.g3 * SY.O12 + SY.g2 * SY.O13 + SY.g1 * SY.O23)) == 0


def test_char2_boundary_certificate_KH8():
    cert = CB.char2_boundary_certificate(G)
    assert cert["offdiag_det_equals_minus_2g1g2g3"] is True
    assert cert["char2_surviving_2x2_minor_nonzero"] is True
    assert cert["char2_gauge_rank"] == 2
    assert cert["char2_quotient_dim"] == 4
    assert cert["kill_K_H8_armed_silent"] is True
