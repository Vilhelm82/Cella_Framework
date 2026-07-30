"""Campaign H — byte stability (acceptance §13.9).

Two builds are byte-identical (same SymPy version) and the proof status is PASS.

Run: PYTHONPATH=src pytest -q tests/test_campaign_h_byte_stability.py
"""

from lloyd_v4.evals.channel_spectrum_carrier.serialize import dumps
from lloyd_v4.evals.rolechspec_symbolic_proof_extraction import run_campaign_h as RH


def test_two_builds_byte_identical():
    a = RH.build_campaign()
    b = RH.build_campaign()
    assert "".join(dumps(r) + "\n" for r in a["records"]) == \
           "".join(dumps(r) + "\n" for r in b["records"])
    assert dumps(a["summary"]) == dumps(b["summary"])


def test_theorem_proved_no_kills():
    camp = RH.build_campaign()
    assert camp["summary"]["status"] == "PASS"
    assert camp["summary"]["theorem_proved"] is True
    assert camp["summary"]["kill_conditions_fired"] == []
    assert camp["summary"]["theorem_H"]["status"] == "PROVED_SYMBOLIC_ON_REGULAR_Q_LOCUS"
