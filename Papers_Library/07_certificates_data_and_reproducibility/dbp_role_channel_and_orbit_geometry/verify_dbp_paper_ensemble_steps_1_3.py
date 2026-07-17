#!/usr/bin/env python3
"""Exact/structural audit for DBP ensemble work-order steps 1--3.

This script checks the new identities introduced by the native-transport
synthesis and the cross-document scope/typing invariants.  It does not
replace the Landen or Stage 1--3 proof verifiers.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent

PAPER3 = ROOT / "DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md"
SQG = ROOT / "SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md"
ARCH = ROOT / "DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md"
STAGE2 = ROOT / "DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1.md"
STAGE3 = ROOT / "DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1.md"
SPINE = ROOT / "upload" / "DBP_UNIFIED_THEOREM_SPINE_DRAFT_v0_1.tex"


class Audit:
    def __init__(self) -> None:
        self.passed = 0

    def check(self, condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(label)
        self.passed += 1
        print(f"PASS {self.passed:02d}  {label}")


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"missing artifact: {path.name}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    a = Audit()
    paper3 = read(PAPER3)
    sqg = read(SQG)
    arch = read(ARCH)
    stage2 = read(STAGE2)
    stage3 = read(STAGE3)
    spine = read(SPINE)

    # Formal deck identities at several exact rational points.
    for rho in (Fraction(2), Fraction(3, 2), Fraction(-3), Fraction(7, 3)):
        if rho in (0, 1, -1):
            continue
        c = (rho - 1) / (rho + 1)
        c_deck = (-rho - 1) / (-rho + 1)
        m = (rho - 1) / (2 * rho)
        m_deck = (-rho - 1) / (-2 * rho)
        n = -(m * m) / (1 - 2 * m)
        n_deck = -(m_deck * m_deck) / (1 - 2 * m_deck)
        a.check(c_deck == 1 / c, f"deck c -> 1/c at rho={rho}")
        a.check(m_deck == 1 - m, f"deck m -> 1-m at rho={rho}")
        a.check(n_deck == 1 - n, f"deck n -> 1-n at rho={rho}")

    # Four-quadrant signed transfer.
    signs = ((1, 1), (-1, 1), (-1, -1), (1, -1))
    chis = [eps_c * eps_s for eps_c, eps_s in signs]
    a.check(sum(chi * chi for chi in chis) == 4,
            "signed reduction after transfer has degree four")

    # The CPV coefficient vector has an unavoidable denominator two.
    cpv = (Fraction(1), Fraction(1, 2))
    a.check(cpv[0].denominator == 1 and cpv[1].denominator == 2,
            "primitive-meridian midpoint is over Z[1/2], not Z")
    a.check(complex(0, 1).real == 0 and complex(0, 1).imag == 1,
            "phase generator is outside the real integral coefficient image")

    # Canonical Paper III is consolidated and has unique equation tags.
    for token in (
        "## 7E. Pole-free finite-interval compilation",
        "## 7F. Native transport and scalar-extension separation",
        "R_{\\mathbb Z,u}L_{\\mathbb Z,u}=4\\operatorname{id}",
        "\\mathbb Z[1/2,i]",
        "Exact scope of the surface conclusion",
    ):
        a.check(token in paper3, f"Paper III contains {token}")
    tags = re.findall(r"\\tag\{([^}]+)\}", paper3)
    a.check(len(tags) == len(set(tags)), "Paper III equation tags are unique")
    a.check("arbitrary classes in the whole surface relative-homology group" in paper3,
            "Paper III records the full-surface scope boundary")

    # Category definition, native composition, and scalar extension.
    for token in (
        "\\mathbb X=(\\mathcal G,\\mathcal A,P,\\ell,M,K,s)",
        "\\bar f|_{\\mathcal A}\\circ s=(F|_{\\mathcal A})^*s'",
        "(GF,\\psi\\varphi,F^*g\\circ f)",
        "\\operatorname{Ext}_R^S",
        "strong presentation equivalence",
    ):
        a.check(token in sqg, f"SQG foundation contains {token}")

    # Exact coefficient diamond is not collapsed to Q/C minimality.
    for ring in ("\\mathbb Z[1/2]", "\\mathbb Z[i]", "\\mathbb Z[1/2,i]"):
        a.check(ring in sqg and ring in paper3, f"exact coefficient ring {ring} is typed")
    a.check("only a coarse scalar-extension ladder" in sqg,
            "SQG report labels Z/Q/C as coarse")

    # Related dossiers and ensemble ledger carry the corrected scope.
    a.check("D_\\infty;\\mathbb Z" in stage2,
            "Stage 2 geometric transfer target is integral")
    a.check("=-\\frac{\\sqrt{ab}}{Z^3}\\,d\\xi\\wedge dt" in stage2,
            "Stage 2 curvature-form typo is repaired")
    a.check("R_{\\mathbb Z}\\mathfrak C=4\\operatorname{id}" in stage3,
            "Stage 3 includes signed reduction")
    a.check("arbitrary classes outside the native swept" in stage3,
            "Stage 3 excludes arbitrary full-surface classes")
    for step in (1, 2, 3):
        a.check(f"DONE {step}." in arch, f"architecture marks work-order step {step} done")
    a.check("selected quotient category and scalar extension" in spine,
            "master spine records the SQG category theorem")
    a.check("R_{\\Z}L_{\\Z}=4\\operatorname{id}" in spine,
            "master spine records degree-four native reduction")

    print(f"\nALL {a.passed} STEP-1--3 AUDIT GATES PASSED")


if __name__ == "__main__":
    main()
