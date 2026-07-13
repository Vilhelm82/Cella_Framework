"""
mutation_check.py -- prove the campaign suite is NON-TAUTOLOGICAL: a lying engine must be
caught.  Each mutation deliberately breaks one engine object and asserts that the relevant
stage flips a verdict to REFUTED/BRANCHED (or raises in the referee cross-check).

If every mutation is caught, the gates have teeth.  Run:
    cd evals/dbp_involution && PYTHONPATH=../../src python3 mutation_check.py
"""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "src"))

import sympy as sp
import rep_utils as RU
import dbp_carrier as E
from harness import Recorder, REFUTED, BRANCHED


def caught(rec):
    return any(r["verdict"] in (REFUTED, BRANCHED) for r in rec.records)


def mutate(name, target_mod, attr, fake, stage_mod, run_kwargs=None):
    orig = getattr(target_mod, attr)
    setattr(target_mod, attr, fake)
    try:
        rec = Recorder("mutant")
        try:
            stage_mod.run(rec, **(run_kwargs or {}))
            hit = caught(rec)
            why = "verdict flipped to REFUTED/BRANCHED"
        except AssertionError as e:
            hit = True
            why = f"referee cross-check raised AssertionError ({str(e)[:50]})"
        except Exception as e:
            hit = True
            why = f"raised {type(e).__name__}"
        print(f"  [{'CAUGHT' if hit else 'MISSED'}] {name}: {why}")
        return hit
    finally:
        setattr(target_mod, attr, orig)


def main():
    import stage0_regression, stageA_sym_wedge_split, stageC_integral_snf
    ok = True

    # Capture originals BEFORE patching so fakes call the genuine engine, not themselves.
    orig_Lflag = E.L_flag
    orig_specht = RU.specht_char
    orig_split = E.sym_wedge_split_matrix

    # 1. Lying carrier: L_flag returns a perturbed matrix (breaks ker=gauge / character).
    def bad_L_flag(n):
        M = orig_Lflag(n).copy()
        M[0, 0] += 1
        return M
    ok &= mutate("Stage0 L_flag perturbed", E, "L_flag", bad_L_flag,
                 stage0_regression, {"n_hi_pair": 4, "n_hi_margin": 4})

    # 2. Lying referee: specht_char off by a constant -> decomposition/orthogonality breaks.
    def bad_specht(lam, mu):
        v = orig_specht(lam, mu)
        return v + (1 if tuple(lam) == (2, 2) else 0)
    ok &= mutate("Stage0 referee specht_char lies", RU, "specht_char", bad_specht,
                 stage0_regression, {"n_hi_pair": 4, "n_lo_margin": 4, "n_hi_margin": 4})

    # 3. Lying involution: tau is replaced by identity -> projector algebra / split breaks.
    def bad_tau(n):
        return sp.eye((n - 1) ** 2)
    ok &= mutate("StageA tau := I", E, "tau_matrix", bad_tau,
                 stageA_sym_wedge_split, {"n_hi": 4})

    # 4. Lying integral split: inject an odd (3) factor -> P-C1 must flag non-2-primary.
    def bad_split(n):
        M, a, b = orig_split(n)
        M = M.copy()
        M[0, 0] = 3
        return M, a, b
    ok &= mutate("StageC split injects odd torsion", E, "sym_wedge_split_matrix", bad_split,
                 stageC_integral_snf, {"n_hi": 4})

    print("\nMUTATION CHECK:", "ALL MUTATIONS CAUGHT (suite has teeth)" if ok
          else "A MUTATION WAS MISSED -- suite is tautological!")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
