"""Task 036 source purity and Axiom 11 enforcement (no V3, no forbidden math libs)."""

from __future__ import annotations

import re
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
MODIFIED_FILE = SRC_ROOT / "lloyd_v4" / "observers" / "directional_alpha_probe.py"


def test_no_v3_or_forbidden_imports_in_modified_alpha_probe() -> None:
    text = MODIFIED_FILE.read_text(encoding="utf-8")
    # Axiom 10 + 11
    assert "lloyd_v3" not in text.lower()
    assert "from lloyd_v3" not in text
    forbidden = ["numpy", "scipy", "sympy", "mpmath", "cmath", "import numpy", "import scipy"]
    for pat in forbidden:
        assert pat not in text, f"Forbidden content {pat} found in directional_alpha_probe.py"


def test_companion_import_only_from_sweep_signature_module() -> None:
    text = MODIFIED_FILE.read_text(encoding="utf-8")
    # We import only the sibling sweep module, nothing else new
    assert "sweep_signature_probe" in text
    assert "from lloyd_v4.observers.sweep_signature_probe" in text
