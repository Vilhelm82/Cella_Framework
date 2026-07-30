"""Campaign H — injectivity (Lemma H4, CL-H4).

The r=1 channel vectors give 6 linear forms in O with a rank-3 coefficient
matrix; a 3x3 minor is nonzero on the regular locus, so O is recovered as an
explicit linear function of the RoleChSpec components -> RoleChSpec injective.

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_injectivity_checks.py
"""

import sympy as sp

from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import injectivity_ideal as IJ
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import symbols as SY

G = SY.g_vec()
OVARS = [SY.O12, SY.O13, SY.O23]


def test_r1_coefficient_matrix_rank_3():
    assert IJ.injectivity_rank(G) == 3


def test_recovery_minor_nonzero():
    _, det, _ = IJ.recovery_minor(G)
    assert det != 0
    # the minor depends only on g (no O)
    for o in OVARS:
        assert sp.diff(det, o) == 0


def test_r1_forms_are_homogeneous_linear_in_O():
    forms, _ = IJ.r1_forms(G)
    M, _ = IJ.r1_coefficient_matrix(G)
    # form = (coeff row) . O exactly
    for idx, f in enumerate(forms):
        recon = sum(M[idx, c] * OVARS[c] for c in range(3))
        assert sp.simplify(f - recon) == 0


def test_O_recovered_linearly():
    # the recovery operator inverts the chosen minor: sub^{-1} (sub . O) = O
    sub, _, _ = IJ.recovery_minor(G)
    rec = sub.inv()
    Ovec = sp.Matrix(OVARS)
    assert sp.simplify(rec * (sub * Ovec) - Ovec) == sp.zeros(3, 1)


def test_injectivity_forces_O_equal():
    # RoleChSpec equal => the chosen r=1 components equal => O = O' (minor invertible)
    cert = IJ.injectivity_certificate(G)
    assert cert["rank"] == 3
    assert cert["minor_det"] != 0
    assert cert["injective_on_regular_Q_locus"] is True
