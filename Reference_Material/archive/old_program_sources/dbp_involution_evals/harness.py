"""
harness.py -- shared verdict / records plumbing for the DBP involution campaign.

Verdict vocabulary (campaign rule): PROVEN, COMPUTER_VERIFIED, REFUTED, BRANCHED, OPEN.
Certainty tiers (auxiliary): [proven], [computer-verified], [conjecture], [observation].

All records are exact (ints / strings).  No float ever reaches a graded verdict.
"""

from __future__ import annotations
import json
import os

PROVEN = "PROVEN"
COMPUTER_VERIFIED = "COMPUTER_VERIFIED"
REFUTED = "REFUTED"
BRANCHED = "BRANCHED"
OPEN = "OPEN"

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "results", "dbp_involution",
)


class Recorder:
    """Collects records and PASS/FAIL gate state for a stage."""

    def __init__(self, stage):
        self.stage = stage
        self.records = []
        self.failed_gate = False

    def record(self, claim, verdict, evidence, tier="[computer-verified]", gate=False):
        rec = {
            "stage": self.stage,
            "claim": claim,
            "verdict": verdict,
            "tier": tier,
            "evidence": evidence,
        }
        self.records.append(rec)
        if gate and verdict in (REFUTED,):
            self.failed_gate = True
        return rec

    def to_jsonl(self):
        return "\n".join(json.dumps(r, sort_keys=True) for r in self.records)


def append_records(records, path=None):
    """Append a list of record dicts to results/dbp_involution/records.jsonl."""
    if path is None:
        path = os.path.join(RESULTS_DIR, "records.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        for r in records:
            f.write(json.dumps(r, sort_keys=True) + "\n")


def reset_records(path=None):
    if path is None:
        path = os.path.join(RESULTS_DIR, "records.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").close()


def dump_json(obj, name):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
    return path
