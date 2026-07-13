"""Gate G0 — fails by design until the first primitive is real.

Criterion: a Cell round-trips on the rational-op class —
value ⊕ residue reconstructs the true object exactly.

Run:  python tests/gate_zero.py
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


def main() -> int:
    try:
        from cella.cell import Cell  # noqa

        # The round-trip that makes the cell real: represent 1/3 coarsely,
        # keep the defect, reconstruct exactly.
        true_object = Fraction(1, 3)
        coarse = Fraction(3333, 10000)
        cell = Cell(value=coarse, residue=true_object - coarse)
        assert cell.reconstruct() == true_object, "reconstruction not exact"
        assert not cell.is_refusal()
        print("GATE 0: PASS — the first primitive is real.")
        return 0
    except NotImplementedError:
        print("GATE 0: OPEN (failing by design) — Cell not yet implemented.")
        return 1
    except AssertionError as e:
        print(f"GATE 0: FAIL — implementation exists but is wrong: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
