"""Campaign E — mutation controls (§12).

Eight deliberately-wrong variants; for each, the correct engine passes a check
and the mutant fails the same check (CL-E6).

Run: PYTHONPATH=src pytest -q tests/test_rolechspec_survival_grammar_mutants.py
"""

from fractions import Fraction as Q

import pytest

from lloyd_v4.evals.rolechspec_survival_grammar import features as F
from lloyd_v4.evals.rolechspec_survival_grammar import labels as L
from lloyd_v4.evals.rolechspec_survival_grammar import mutants as M
from lloyd_v4.evals.rolechspec_survival_grammar import rule_eval as RE
from lloyd_v4.evals.rolechspec_survival_grammar import serialize as S

SMALL = [Q(-1), Q(0), Q(1)]
GS = [[Q(1), Q(1), Q(1)]]
SURV, COLL = L.SURVIVES, L.COLLAPSES

# one surviving + one collapsing class (from Campaign D)
from lloyd_v4.evals.channel_spectrum_carrier.actions import gauge_H  # noqa: E402
SG = [Q(1), Q(1), Q(1)]
SREPS = [[[Q(-2), Q(-2), Q(-2)], [Q(-2), Q(-2), Q(-2)], [Q(-2), Q(-2), Q(-1)]],
         [[Q(-2), Q(-2), Q(-2)], [Q(-2), Q(-1), Q(-1)], [Q(-2), Q(-1), Q(-1)]]]
CG = [Q(3), Q(1), Q(2)]
CH1 = [[Q(2), Q(1), Q(0)], [Q(1), Q(0), Q(0)], [Q(0), Q(0), Q(2)]]
CREPS = [CH1, gauge_H(CG, CH1, [Q(1), Q(-2), Q(3)])]
TRUE_LABELS = [L.survival_label(SG, SREPS), L.survival_label(CG, CREPS)]


# 1) label leakage into the feature table
def test_mutant_label_leakage_caught():
    c = F.enumerate_classes(GS, SMALL)[0]
    F.assert_no_forbidden(F.class_features(c["g"], c["reps"], c["reduced_tower"]))  # correct ok
    leaked = M.mutant_class_features_with_leak(c["g"], c["reps"], c["reduced_tower"])
    with pytest.raises(ValueError):
        F.assert_no_forbidden(leaked)


# 2) all-survive labelling fails to reproduce the split
def test_mutant_all_survive_caught():
    assert set(TRUE_LABELS) == {SURV, COLL}                       # truth is mixed
    bad = M.mutant_all_survive([SG, CG], [SREPS, CREPS])
    assert L.label_counts(bad) != L.label_counts(TRUE_LABELS)


# 3) all-collapse likewise
def test_mutant_all_collapse_caught():
    bad = M.mutant_all_collapse([SG, CG], [SREPS, CREPS])
    assert L.label_counts(bad) != L.label_counts(TRUE_LABELS)


# 4) reporting a mixed predicate as zero-violation
def test_mutant_bad_rule_no_violations_caught():
    recs = [{"a": 1}, {"a": 1}] * 5 + [{"a": 1}, {"a": 1}] * 5
    labels = [SURV] * 10 + [COLL] * 10                            # a==1 is mixed
    assert RE.evaluate_rule([("a", "eq", 1)], recs, labels)["violations"] == 10   # correct
    assert M.mutant_bad_rule_no_violations([("a", "eq", 1)], recs, labels)["violations"] == 0


# 5) skipping classes to improve purity
def test_mutant_skip_classes_caught():
    full = F.enumerate_classes(GS, SMALL)
    skipped = M.mutant_enumerate_skip(GS, SMALL)
    assert len(skipped) < len(full)                              # mutant drops classes
    # the count check (KC-E7) would fire: skipped != full count


# 6) float feature
def test_mutant_float_feature_caught():
    c = F.enumerate_classes(GS, SMALL)[0]
    good = F.class_features(c["g"], c["reps"], c["reduced_tower"])
    S.dumps(good)                                                 # correct serializes
    bad = M.mutant_float_feature(c["g"], c["reps"], c["reduced_tower"])
    with pytest.raises(TypeError):
        S.to_canonical(bad)


# 7) unstable (unsorted set) feature value
def test_mutant_unstable_order_caught():
    c = F.enumerate_classes(GS, SMALL)[0]
    bad = M.mutant_unstable_features(c["g"], c["reps"], c["reduced_tower"])
    with pytest.raises(TypeError):
        S.to_canonical(bad)                                      # a raw set is non-canonical


# 8) held-out marked validated without evaluation
def test_mutant_holdout_not_run_caught():
    # c==1 present only in group 0 -> truly TRAIN_ONLY
    recs = [{"c": 1}, {"c": 1}] * 6 + [{"c": 0}, {"c": 0}] * 6
    labels = [SURV] * 12 + [COLL] * 12
    groups = [0] * 12 + [1] * 6 + [2] * 6
    assert RE.heldout_status([("c", "eq", 1)], SURV, recs, labels, groups) == "RULE_TRAIN_ONLY"
    assert M.mutant_holdout_always_validated([("c", "eq", 1)], SURV, recs, labels, groups) \
        == "RULE_VALIDATED_HELDOUT"


def test_all_eight_mutants_registered():
    for name in M.MUTANT_NAMES:
        assert callable(getattr(M, name))
    assert len(M.MUTANT_NAMES) == 8
