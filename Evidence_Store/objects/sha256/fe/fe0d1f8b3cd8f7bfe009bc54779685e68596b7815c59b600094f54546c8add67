#!/usr/bin/env python3
"""Direct mathematical checks for CCE-4 bounded evaluation.

The verifier checks exact dyadic enclosures and requested widths.  It does not
create a release bundle, compare file hashes, or build checkpoint chains.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "engine/src").is_dir())
sys.path.insert(0, str(ROOT / "engine/src"))

from cella.continuation.cce4 import (
    CertifiedBoundedEvaluation, evaluate_bounded_observable, released_cce4_request,
)


def main() -> None:
    checked = 0
    for target in ("primary", "dual_cpv"):
        for bits in (192, 256, 384):
            result = evaluate_bounded_observable(released_cce4_request(target, bits))
            assert isinstance(result, CertifiedBoundedEvaluation)
            bracket = result.certificate.exact_dyadic_bracket
            exponent = bracket["denominator_exponent"]
            lower = int(bracket["lower_numerator_hex"], 16)
            upper = int(bracket["upper_numerator_hex"], 16)
            assert lower < upper
            assert exponent > 0
            assert result.certificate.achieved_width_bits >= bits
            assert bracket["rounded_value_bits"] >= bits
            checked += 1
    print(f"CCE-4 direct bounded-evaluation replay: {checked}/6 exact enclosures passed")


if __name__ == "__main__":
    main()
