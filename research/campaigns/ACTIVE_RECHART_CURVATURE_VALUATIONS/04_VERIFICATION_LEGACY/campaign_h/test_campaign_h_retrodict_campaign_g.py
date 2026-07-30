"""Campaign H — Campaign G retrodiction (CL-H6).

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_retrodict_campaign_g.py
"""

from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import verify_against_campaign_g as VG


def test_symbolic_formulas_match_campaign_D():
    assert VG.symbolic_matches_campaign_D((1, 2, 3), (1, -1, 2)) is True
    assert VG.symbolic_matches_campaign_D((2, 3, 5), (2, 3, -1)) is True


def test_iff_holds_on_samples():
    assert VG.iff_holds((1, 1, 1), (1, 0, 0), (0, 1, 0)) is True
    assert VG.iff_holds((1, 2, 3), (1, -1, 2), (1, -1, 2)) is True   # equal -> O=0


def test_retrodiction_zero_counterexamples():
    res = VG.retrodict()
    assert res["symbolic_matches_campaign_D"] is True
    assert res["faithfulness_counterexamples"] == 0
    assert res["gauge_invariance_counterexamples"] == 0
    assert res["pairs_tested"] > 0
