"""Precision Flow — referee-class instruments + Stage-A grading.

REFEREE-CLASS per the brief's fence 4 (precedent: the Quiet's mpmath
arbiter): exact-Q reference rounder (RNE to q bits at x's own binade,
unbounded exponent), the Refinement-Law stepper, and the orbit extractor.
Pure stdlib `fractions` + `math.isqrt`; deterministic; byte-stable; emits
flow RECORDS, not TypedResults — no Amendment-1 membrane, no eval-registry
entry. No floating point participates in any decision.

Grading formulas are derived-and-cited in the frozen Stage-A manifest
(authority: covariance_derivation_2026_06_10.md section 1):
  - the Law is graded in the s-form  s_{q+1} == s_q + (u_q/2)*D  (equivalent
    to the e-form since x is fixed; exact in Q for ALL classes incl. sqrt);
  - D = RNE(2t) by exact comparison: 0 iff |e| <= u/4 (tie -> even), else
    sign(e);
  - the rounder computes s_{q+1} INDEPENDENTLY; the Law must predict it.
Failure behavior: recorded refusal rows, never a wrong zero.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
STAGE_A_DIR = REPO_ROOT / "results" / "precision_flow" / "stage_a"
Q_LO, Q_HI = 53, 80  # inclusive sweep (manifest)


class ManifestGateRefused(RuntimeError):
    pass


def require_stage_a() -> Dict[str, Any]:
    manifest = json.loads((STAGE_A_DIR / "manifest.json").read_text())
    pin = (STAGE_A_DIR / "manifest_sha256.pin").read_text().strip()
    actual = hashlib.sha256((STAGE_A_DIR / "manifest.json").read_bytes()).hexdigest()
    if not manifest.get("frozen") or actual != pin:
        raise ManifestGateRefused("stage-A manifest gate refused")
    for name, prefix in manifest["battery_pins_sha256_prefix16"].items():
        path = STAGE_A_DIR / "battery" / name
        if hashlib.sha256(path.read_bytes()).hexdigest()[:16] != prefix:
            raise ManifestGateRefused(f"battery {name} drifted from pin")
    return manifest


def _frac(s: str) -> Fraction:
    num, den = s.split("/")
    return Fraction(int(num), int(den))


# --- phenomena: exact reals ('rat', Fraction) or ('sqrt', radicand) ---------

class Phen:
    """Exact real: rational value, or sqrt of a positive non-square rational.
    All comparisons exact (sqrt via squaring against positive rationals)."""

    __slots__ = ("kind", "val")

    def __init__(self, kind: str, val: Fraction) -> None:
        self.kind = kind  # 'rat' | 'sqrt'
        self.val = val    # the value itself, or the radicand

    def cmp(self, c: Fraction) -> int:
        """sign(x - c), exact."""
        if self.kind == "rat":
            d = self.val - c
            return (d > 0) - (d < 0)
        if c <= 0:
            return 1  # sqrt phenomena are positive
        d = self.val - c * c
        return (d > 0) - (d < 0)

    def binade(self) -> int:
        """floor(log2 |x|), exact."""
        if self.kind == "rat":
            a = abs(self.val)
        else:
            a = None
        if self.kind == "rat":
            p, r = a.numerator, a.denominator
            b = p.bit_length() - r.bit_length()
            # adjust: want 2^b <= a < 2^(b+1)
            while not (a >= Fraction(2) ** b):
                b -= 1
            while a >= Fraction(2) ** (b + 1):
                b += 1
            return b
        # sqrt: start from radicand binade // 2, adjust exactly
        rb = Phen("rat", self.val).binade()
        b = rb // 2
        while self.cmp(Fraction(2) ** b) < 0:
            b -= 1
        while self.cmp(Fraction(2) ** (b + 1)) >= 0:
            b += 1
        return b

    def floor_div(self, u: Fraction) -> int:
        """floor(x / u), exact (u > 0)."""
        if self.kind == "rat":
            n = self.val / u
            return n.numerator // n.denominator
        ratio2 = self.val / (u * u)  # (x/u)^2, rational
        p, q = ratio2.numerator, ratio2.denominator
        return math.isqrt(p * q) // q

    def equals_frac(self, c: Fraction) -> bool:
        return self.cmp(c) == 0


def rn(phen: Phen, q: int, binade: int) -> Fraction:
    """RNE to q bits at the given binade, unbounded exponent. Independent
    of the Law — this is the referee."""
    u = Fraction(2) ** (binade - q + 1)
    m = phen.floor_div(u)
    mid = Fraction(2 * m + 1, 2) * u
    c = phen.cmp(mid)
    if c > 0:
        n = m + 1
    elif c < 0:
        n = m
    else:  # exact tie: ties-to-even on the integer significand n
        n = m if m % 2 == 0 else m + 1
    return n * u


def law_d(phen: Phen, s_q: Fraction, u_q: Fraction) -> int:
    """D = RNE(2 t_q) by exact comparison (manifest D_from_RNE):
    0 iff |e| < u/4 or |e| == u/4 (tie -> even = ancestor); else sign(e)."""
    quarter = u_q / 4
    if phen.cmp(s_q + quarter) > 0:
        return 1
    if phen.cmp(s_q - quarter) < 0:
        return -1
    return 0


def sweep_case(phen: Phen) -> Dict[str, Any]:
    """Run the full q-sweep; grade the Law in the s-form at every step."""
    b = phen.binade()
    violations: List[Dict[str, Any]] = []
    s = rn(phen, Q_LO, b)
    for q in range(Q_LO, Q_HI):
        u = Fraction(2) ** (b - q + 1)
        d = law_d(phen, s, u)
        s_pred = s + (u / 2) * d
        s_next = rn(phen, q + 1, b)  # independent referee
        if s_next != s_pred:
            violations.append({"q": q, "D": d,
                               "s_pred": str(s_pred), "s_next": str(s_next)})
        s = s_next
    return {"binade": b, "n_steps": Q_HI - Q_LO, "violations": violations}


def t_orbit(phen: Phen, q_lo: int = Q_LO, q_hi: int = Q_HI) -> List[Fraction]:
    """Orbit extractor (rational phenomena): t_q = e_q / u_q exactly."""
    if phen.kind != "rat":
        raise ManifestGateRefused("t_orbit in Q requires a rational phenomenon")
    b = phen.binade()
    orbit = []
    for q in range(q_lo, q_hi + 1):
        u = Fraction(2) ** (b - q + 1)
        orbit.append((phen.val - rn(phen, q, b)) / u)
    return orbit


# --- Stage-A grading ---------------------------------------------------------

def _load(name: str) -> Any:
    return json.loads((STAGE_A_DIR / "battery" / f"{name}.json").read_text())


def grade_a_p1() -> Dict[str, Any]:
    per_class: Dict[str, Dict[str, int]] = {}
    bad: List[Dict[str, Any]] = []
    for name in ("sums", "products", "quotients", "straddle", "ties", "dyadic"):
        steps = viol = 0
        for case in _load(name):
            rec = sweep_case(Phen("rat", _frac(case["x"])))
            steps += rec["n_steps"]
            viol += len(rec["violations"])
            if rec["violations"]:
                bad.append({"class": name, "x": case["x"],
                            "violations": rec["violations"][:3]})
        per_class[name] = {"steps": steps, "violations": viol}
    steps = viol = 0
    for case in _load("sqrts"):
        rec = sweep_case(Phen("sqrt", _frac(case["radicand"])))
        steps += rec["n_steps"]
        viol += len(rec["violations"])
        if rec["violations"]:
            bad.append({"class": "sqrts", "radicand": case["radicand"],
                        "violations": rec["violations"][:3]})
    per_class["sqrts"] = {"steps": steps, "violations": viol}
    total_steps = sum(c["steps"] for c in per_class.values())
    total_viol = sum(c["violations"] for c in per_class.values())
    return {"pass": total_viol == 0, "total_steps": total_steps,
            "total_violations": total_viol, "per_class": per_class,
            "violating_cases": bad}


def grade_a_p2() -> Dict[str, Any]:
    rows = []
    for case in _load("ties"):
        x = _frac(case["x"])
        phen = Phen("rat", x)
        b = phen.binade()
        u53 = Fraction(2) ** (b - 53 + 1)
        s53 = rn(phen, 53, b)
        s54 = rn(phen, 54, b)
        e53, e54 = x - s53, x - s54
        if case["kind"] == "quarter":
            ok = (s54 == s53) and (e54 == e53)  # resolves to the ancestor
        else:  # half
            ok = (e54 == 0)                      # annihilates
        rows.append({"kind": case["kind"], "ok": ok,
                     "t53": str(e53 / u53)})
    n_ok = sum(r["ok"] for r in rows)
    return {"pass": n_ok == len(rows), "n_cases": len(rows), "n_ok": n_ok,
            "failures": [r for r in rows if not r["ok"]]}


def grade_a_p3() -> Dict[str, Any]:
    rows = []
    for case in _load("dyadic"):
        x = _frac(case["x"])
        L = case["L"]
        phen = Phen("rat", x)
        b = phen.binade()
        ok = True
        for q in range(Q_LO, Q_HI + 1):
            dead = rn(phen, q, b) == x  # e_q == 0
            if dead != (q >= L):        # the biconditional, both directions
                ok = False
                break
        rows.append({"x": case["x"], "L": L, "ok": ok})
    n_ok = sum(r["ok"] for r in rows)
    return {"pass": n_ok == len(rows), "n_cases": len(rows), "n_ok": n_ok,
            "failures": [r for r in rows if not r["ok"]]}


def main() -> None:
    require_stage_a()
    verdicts = {"A-P1": grade_a_p1(), "A-P2": grade_a_p2(), "A-P3": grade_a_p3()}
    rec_dir = STAGE_A_DIR / "records"
    rec_dir.mkdir(exist_ok=True)
    (rec_dir / "stage_a_summary.json").write_text(
        json.dumps(verdicts, sort_keys=True, indent=1) + "\n")
    slim = {k: {kk: vv for kk, vv in v.items()
                if kk not in ("violating_cases", "failures")} | {
                "n_failures": len(v.get("violating_cases", v.get("failures", [])))}
            for k, v in verdicts.items()}
    (STAGE_A_DIR / "prediction_verdicts.json").write_text(
        json.dumps(slim, sort_keys=True, indent=1) + "\n")
    for p in ("A-P1", "A-P2", "A-P3"):
        print(f"{p}: {'PASS' if verdicts[p]['pass'] else 'FAIL'}")
    print("total law steps:", verdicts["A-P1"]["total_steps"])


if __name__ == "__main__":
    main()
