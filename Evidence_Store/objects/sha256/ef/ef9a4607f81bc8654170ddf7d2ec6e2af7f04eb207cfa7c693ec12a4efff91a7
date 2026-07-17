"""Campaign A — mutation controls (§10).

Each mutant is a deliberately-wrong variant. For each, we show the CORRECT
engine passes a check and the MUTANT fails the SAME check. This proves the
checks are non-tautological: a lying engine would be caught. The mutants are
the only place a kill condition is allowed to fire.

Run: PYTHONPATH=src pytest -q tests/test_channel_spectrum_carrier_mutants.py
"""

from fractions import Fraction as Q

import pytest

from lloyd_v4.evals.channel_spectrum_carrier import actions as A
from lloyd_v4.evals.channel_spectrum_carrier import carrier as C
from lloyd_v4.evals.channel_spectrum_carrier import mutants as M
from lloyd_v4.evals.channel_spectrum_carrier import serialize as S

KEY_G = [Q(3), Q(1), Q(2)]
KEY_H = [[Q(2), Q(1), Q(0)],
         [Q(1), Q(0), Q(0)],
         [Q(0), Q(0), Q(2)]]


# 1) drop_mixed_terms — breaks the CL-A1 reduction identity
def test_mutant_drop_mixed_terms_caught():
    truth = C.channel_density(KEY_G, KEY_H, 2, Q(1), Q(1))
    assert sum(C.channel_vector(KEY_G, KEY_H, 2).values()) == truth        # correct passes
    bad = M.mutant_channel_vector_drop_mixed(KEY_G, KEY_H, 2)
    assert sum(bad.values()) != truth                                       # mutant fails


# 2) wrong_sign — flips (-1)^{r+1}; breaks pinned keystone density
def test_mutant_wrong_sign_caught():
    assert C.channel_density(KEY_G, KEY_H, 2, Q(1), Q(1)) == Q(-12)         # correct
    assert M.mutant_channel_density_wrong_sign(KEY_G, KEY_H, 2, Q(1), Q(1)) != Q(-12)


# 3) bad_split — leaks the diagonal into H_c; breaks pinned pure-coupling channel
def test_mutant_bad_split_caught():
    assert C.channel_vector(KEY_G, KEY_H, 2)[(2, 0)] == Q(-4)               # correct
    assert M.mutant_channel_vector_bad_split(KEY_G, KEY_H, 2)[(2, 0)] != Q(-4)


# 4) float_normalization — emits a float for odd-order; canonical path must refuse it
def test_mutant_float_normalization_caught():
    good = S.normalize_coefficient(Q(6), Q(14), 1)
    assert good["rational"] is False and "value" not in good               # correct refuses
    bad = M.mutant_normalize_float(Q(6), Q(14), 1)
    assert isinstance(bad["value"], float)                                  # mutant lies
    with pytest.raises(TypeError):
        S.to_canonical(bad["value"])                                        # serializer catches


# 5) no_gauge_shift — pretends gauge does not move channels
def test_mutant_no_gauge_shift_caught():
    a = [Q(1), Q(-2), Q(3)]
    real = A.gauge_H(KEY_G, KEY_H, a)
    moved = any(C.channel_vector(KEY_G, real, r) != C.channel_vector(KEY_G, KEY_H, r)
                for r in (1, 2))
    assert moved is True                                                    # correct: channels move
    fake = M.mutant_gauge_H_no_shift(KEY_G, KEY_H, a)
    fake_moved = any(C.channel_vector(KEY_G, fake, r) != C.channel_vector(KEY_G, KEY_H, r)
                     for r in (1, 2))
    assert fake_moved is False                                              # mutant: no move (caught)


# 6) passive_as_active — conflates a passive relabelling with an active orbit
def test_mutant_passive_as_active_caught():
    perms = [(0, 1, 2), (1, 0, 2), (2, 1, 0), (1, 2, 0), (2, 0, 1), (0, 2, 1)]
    canonical = {C.density_fingerprint(*A.passive_permute(KEY_G, KEY_H, s)) for s in perms}
    assert len(canonical) == 1                                              # passive orbit is trivial
    lying = {M.mutant_label_sensitive_fingerprint(*A.passive_permute(KEY_G, KEY_H, s))
             for s in perms}
    assert len(lying) > 1                                                   # mutant fakes an active orbit


# 7) string_fraction_compare — compares by string form, hiding non-reduced values
def test_mutant_string_fraction_compare_caught():
    # raw, non-reduced engine output vs reduced expected: same rational value
    a_pair, b_pair = (-12, 196), (-3, 49)
    assert (Q(*a_pair) == Q(*b_pair)) is True                              # exact: equal
    assert M.mutant_string_eq(a_pair, b_pair) is False                     # string-compare lies


def test_all_seven_mutants_exposed():
    # registry sanity: every named mutant exists and is callable
    for name in M.MUTANT_NAMES:
        assert callable(getattr(M, name))
    assert len(M.MUTANT_NAMES) == 7
