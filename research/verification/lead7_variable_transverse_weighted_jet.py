#!/usr/bin/env python3
"""Canonical replay for the LEAD-7 variable-transverse weighted-jet proof."""

from __future__ import annotations

import runpy
from pathlib import Path


VERIFIER = (
    Path(__file__).resolve().parents[1]
    / "campaigns"
    / "CELLA_CONTINUATION_ENGINE"
    / "10_post8_universalization"
    / "verify_lead7_variable_transverse_weighted_jet.py"
)


if __name__ == "__main__":
    runpy.run_path(str(VERIFIER), run_name="__main__")
