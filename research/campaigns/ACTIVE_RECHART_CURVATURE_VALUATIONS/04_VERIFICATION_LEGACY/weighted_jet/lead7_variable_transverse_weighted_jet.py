#!/usr/bin/env python3
"""Canonical replay for the LEAD-7 variable-transverse weighted-jet proof.

PACKAGE-LOCAL PATH FIX (Stage 0 audit flag, discharged at Stage 6): the
original shim resolved the verifier through a nonexistent parent-tree
location (../campaigns/CELLA_CONTINUATION_ENGINE/...). This packaged copy
runs the verifier that sits BESIDE it, as the campaign plan (5.4) requires.
"""

from __future__ import annotations

import runpy
from pathlib import Path


VERIFIER = Path(__file__).resolve().parent / "verify_lead7_variable_transverse_weighted_jet.py"


if __name__ == "__main__":
    runpy.run_path(str(VERIFIER), run_name="__main__")
