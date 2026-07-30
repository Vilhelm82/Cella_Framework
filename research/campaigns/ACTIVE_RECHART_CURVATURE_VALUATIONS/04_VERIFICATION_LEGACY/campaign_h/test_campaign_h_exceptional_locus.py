"""Campaign H — exceptional locus (CL-H5, KC-H4).

The recovery minor's numerator factors into g-only terms; over Q it is nonzero
on the entire regular locus (sums of squares are definite), so there is no
exceptional stratum beyond regularity. Every component is typed.

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_exceptional_locus.py
"""

import sympy as sp

from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import exceptional_locus as EL
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import symbols as SY


def test_minor_numerator_factors_typed():
    rep = EL.exceptional_report(SY.g_vec())
    # the minor numerator is a product of g-only factors (a regularity denominator)
    assert all(o not in rep["minor_numerator_factors_free_symbols"]
               for o in (SY.O12, SY.O13, SY.O23))


def test_no_exceptional_stratum_on_regular_Q_locus():
    rep = EL.exceptional_report(SY.g_vec())
    assert rep["empty_on_regular_Q_locus"] is True
    assert "g1**2 + g3**2" in rep["sum_of_squares_factor"] or \
           "g1^2 + g3^2" in rep["sum_of_squares_factor"]


def test_sum_of_squares_definite_over_Q():
    # g1^2 + g3^2 is positive definite over R >= Q, so its only real (hence
    # rational) zero is g1 = g3 = 0 -- which is non-regular. (sp.solve would go
    # to C and give g1 = +-i g3, irrelevant over Q.)
    form = SY.g1 ** 2 + SY.g3 ** 2
    Hm = sp.hessian(form, [SY.g1, SY.g3]) / 2
    assert Hm.is_positive_definite is True
    assert form.subs({SY.g1: sp.Rational(2), SY.g3: sp.Rational(3)}) > 0
