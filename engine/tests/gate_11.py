"""Gate G1.1 — the invariant tower.

Battery for the frozen prereg campaigns/G11_invariant_tower/PREREG.md
(sha b736cfb9d88e6957, frozen before any implementation code existed).
Certifies: the sigma tower against 7 corpus pins (incl. n=4 and square-q
rows); parity typing at the type level; the sigma2/channel cross-route at
n=3; identical gauge invariance; purity wiring; refusals with the
chart/regularity asymmetry pinned; certificates carrying QSqrt; and three
mutants (sign-flip, normalization, radicand-context) that MUST FAIL.

Run:  python tests/gate_11.py   (exit 0 iff the gate is closed)
"""

import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.carrier import as_labeled, carrier, channels_n3_crosscheck  # noqa: E402
from cella.certificate import EmissionError, canon, emit               # noqa: E402
from cella.jet import ConstraintBlock, Jet2                            # noqa: E402
from cella.qsqrt import QSqrt                                          # noqa: E402
from cella.refusal import Refusal                                      # noqa: E402
from cella.residue import SPECIES_R, Account, Residue, madd, msub      # noqa: E402
from cella.tower import TIER_TOWER, sigma_tower                        # noqa: E402

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


def gauge(g, H, a):
    n = len(g)
    return tuple(tuple(H[i][j] + g[i] * a[j] + a[i] * g[j] for j in range(n))
                 for i in range(n))


def blk(point, g, H):
    return ConstraintBlock([Jet2(point, g, H)])


# ---------------- corpus (PREREG P1) ----------------
CORPUS = {
    "keystone": ((Q(1), Q(1), Q(1)), (Q(3), Q(1), Q(2)),
                 ((Q(2), Q(1), Q(0)), (Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(2))),
                 (QSqrt(0, Q(-6, 49), 14), Q(-3, 49))),
    "sphere3": ((Q(1), Q(2), Q(3)), (Q(2), Q(4), Q(6)),
                ((Q(2), Q(0), Q(0)), (Q(0), Q(2), Q(0)), (Q(0), Q(0), Q(2))),
                (QSqrt(0, Q(-1, 14), 56), Q(1, 14))),
    "cylinder": ((Q(1), Q(2), Q(7)), (Q(2), Q(4), Q(0)),
                 ((Q(2), Q(0), Q(0)), (Q(0), Q(2), Q(0)), (Q(0), Q(0), Q(0))),
                 (QSqrt(0, Q(-1, 10), 20), Q(0))),
    "saddle": ((Q(1), Q(1), Q(1)), (Q(-1), Q(-1), Q(1)),
               ((Q(0), Q(-1), Q(0)), (Q(-1), Q(0), Q(0)), (Q(0), Q(0), Q(0))),
               (QSqrt(0, Q(-2, 9), 3), Q(-1, 9))),
    "ellipsoid": ((Q(1), Q(1), Q(1)), (Q(2), Q(4), Q(6)),
                  ((Q(2), Q(0), Q(0)), (Q(0), Q(4), Q(0)), (Q(0), Q(0), Q(6))),
                  (QSqrt(0, Q(-6, 49), 56), Q(9, 49))),
    "monkey": ((Q(0), Q(0), Q(0)), (Q(0), Q(0), Q(1)),
               ((Q(0), Q(0), Q(0)), (Q(0), Q(0), Q(0)), (Q(0), Q(0), Q(0))),
               (Q(0), Q(0))),
    "sphere4": ((Q(1), Q(2), Q(3), Q(4)), (Q(2), Q(4), Q(6), Q(8)),
                ((Q(2), Q(0), Q(0), Q(0)), (Q(0), Q(2), Q(0), Q(0)),
                 (Q(0), Q(0), Q(2), Q(0)), (Q(0), Q(0), Q(0), Q(2))),
                (QSqrt(0, Q(-1, 20), 120), Q(1, 10),
                 QSqrt(0, Q(-1, 1800), 120))),
}

# P1 — corpus pins
for name, (pt, g, H, pin) in CORPUS.items():
    c = sigma_tower(blk(pt, g, H))
    check(f"P1 {name}: sigma tower == pin, exact reconstruction",
          not c.is_refusal() and c.value == pin and c.reconstruct() == pin)

# P2 — parity typing at the type level
parity_ok = True
for name, (pt, g, H, pin) in CORPUS.items():
    val = sigma_tower(blk(pt, g, H)).value
    q = sum(x * x for x in g)
    for r, s in enumerate(val, start=1):
        if r % 2 == 0:
            parity_ok &= isinstance(s, Q)
        else:
            if isinstance(s, QSqrt):
                parity_ok &= (s.r == q and s.a == 0)
            else:
                # rational odd value permitted only by theorem (exact test):
                import math as _m
                sq = Q(q)
                is_square = (_m.isqrt(sq.numerator) ** 2 == sq.numerator and
                             _m.isqrt(sq.denominator) ** 2 == sq.denominator)
                parity_ok &= (s == 0 or is_square)
check("P2 parity typing: even Fraction; odd QSqrt at radicand q, rational "
      "only by square-q/zero theorem", parity_ok)

# P3 — cross-route sigma2 == labeled channel sum (K-1 armed) + labeled triples
TRIPLES = {"keystone": {"kc": Q(-1, 49), "kint": Q(-3, 49), "ks": Q(1, 49)},
           "sphere3": {"kc": Q(0), "kint": Q(0), "ks": Q(1, 14)},
           "saddle": {"kc": Q(-1, 9), "kint": Q(0), "ks": Q(0)},
           "ellipsoid": {"kc": Q(0), "kint": Q(0), "ks": Q(9, 49)}}
for name, want in TRIPLES.items():
    pt, g, H, pin = CORPUS[name]
    lab = as_labeled(channels_n3_crosscheck(blk(pt, g, H)))
    s2 = sigma_tower(blk(pt, g, H)).value[1]
    check(f"P3 {name}: labeled triple pinned and sigma2 == kc+kint+ks",
          {k: lab[k] for k in ("kc", "kint", "ks")} == want
          and lab["K_G"] == s2)
# the chart/regularity ASYMMETRY row
pt, g, H, pin = CORPUS["cylinder"]
tower_ok = sigma_tower(blk(pt, g, H))
carr = carrier(blk(pt, g, H))
check("P3 asymmetry: cylinder tower COMPUTES while carrier refuses "
      "ROLE_CHART_UNAVAILABLE on the same block",
      not tower_ok.is_refusal() and carr.is_refusal()
      and carr.residue.token == "ROLE_CHART_UNAVAILABLE")

# P4 — identical gauge invariance (K-3 armed)
GAUGE_ROWS = {3: ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(1), Q(-2), Q(3)),
                  (Q(-1, 2), Q(5), Q(1))),
              4: ((Q(1), Q(0), Q(0), Q(0)), (Q(1, 3), Q(-2), Q(5), Q(7)))}
for name, (pt, g, H, pin) in CORPUS.items():
    base = sigma_tower(blk(pt, g, H)).value
    ok = all(sigma_tower(blk(pt, g, gauge(g, H, a))).value == base
             for a in GAUGE_ROWS[len(g)])
    check(f"P4 {name}: tower invariant under every gauge row", ok)

# P5 — purity wiring
K_PT, K_G3, K_H3, K_PIN = CORPUS["keystone"]
acct = Account().absorb(Residue(SPECIES_R, (Q(1), Q(-2), Q(3)), base=K_G3))
check("P5 U1 R-epoch through the Account leaves the tower fixed",
      sigma_tower(blk(K_PT, K_G3,
                      gauge(K_G3, K_H3, acct.r_epochs[0][1]))).value == K_PIN)
E = ((Q(0), Q(1), Q(0)), (Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(0)))
H_def = madd(K_H3, E)
check("P5 U2 M-defect moves the tower; pinned witness "
      "(QSqrt(0,-9/98,14), -9/49)",
      sigma_tower(blk(K_PT, K_G3, H_def)).value
      == (QSqrt(0, Q(-9, 98), 14), Q(-9, 49)))
check("P5 U3 M-corrected reconstruction recovers the base tower",
      sigma_tower(blk(K_PT, K_G3, msub(H_def, E))).value == K_PIN)

# P6 — refusal rows
j1 = Jet2(K_PT, K_G3, K_H3)
j2 = Jet2(K_PT, (Q(2), Q(2), Q(2)),
          ((Q(0), Q(1), Q(1)), (Q(1), Q(0), Q(1)), (Q(1), Q(1), Q(0))))
r1 = sigma_tower(ConstraintBlock([j1, j2]))
check("P6 R1 block len 2 -> CODIM_UNSUPPORTED",
      r1.is_refusal() and r1.residue.token == "CODIM_UNSUPPORTED")
r2 = sigma_tower(blk(K_PT, (Q(0), Q(0), Q(0)), K_H3))
check("P6 R2 zero gradient -> SINGULAR_GRADIENT",
      r2.is_refusal() and r2.residue.token == "SINGULAR_GRADIENT")
try:
    Jet2(K_PT, (3.0, 1.0, 2.0), K_H3)
    fb = False
except TypeError:
    fb = True
check("P6 R3 float in a jet is a TypeError", fb)

# P7 — certificates
def compute_tower():
    cell = sigma_tower(blk(K_PT, K_G3, K_H3))
    return {"value": cell.value, "number_type": "Q + Q(sqrt q)",
            "account": {"m": cell.residue, "r_epochs": ()}, "refusals": []}


cert = emit(f"Invariant tower of the keystone block ({TIER_TOWER}).",
            compute_tower)
check("P7 C1 tower certificate: tier stated, QSqrt flows through canon",
      TIER_TOWER in cert.machine()["what"]
      and "sqrt(14/1)" in str(cert.machine()["value"]))


def compute_refused():
    cell = sigma_tower(ConstraintBlock([j1, j2]))
    return {"value": None, "number_type": "none",
            "account": {"m": None, "r_epochs": ()},
            "refusals": [cell.residue]}


cert_r = emit(f"Invariant tower for a two-constraint system ({TIER_TOWER}).",
              compute_refused)
check("P7 C2 refusal certificate renders plainly, no raw token",
      "system of constraints" in cert_r.plain()
      and "CODIM_UNSUPPORTED" not in cert_r.plain())
state = {"n": 0}


def flaky():
    state["n"] += 1
    return {"value": Q(state["n"]), "number_type": "Q",
            "account": {"m": None, "r_epochs": ()}, "refusals": []}


try:
    emit("flaky tower", flaky)
    fc = False
except EmissionError:
    fc = True
check("P7 C3 double-run law holds on the tower path", fc)

# P8 — mutants MUST FAIL
def mutant_signflip(pt, g, H):
    """M1: S = +(1/sqrt q) A — odd sector negated, even unchanged.
    (0-based index i even <=> order r = i+1 odd.)"""
    val = sigma_tower(blk(pt, g, H)).value
    return tuple(-s if i % 2 == 0 else s for i, s in enumerate(val))


m1_odd_bites, m1_even_passes = True, True
for name, (pt, g, H, pin) in CORPUS.items():
    mv = mutant_signflip(pt, g, H)
    for i, (m, p) in enumerate(zip(mv, pin)):
        r = i + 1
        if r % 2 == 1 and p != 0:
            m1_odd_bites &= (m != p)
        if r % 2 == 0:
            m1_even_passes &= (m == p)
check("P8 M1 sign-flip mutant FAILS every nonzero odd pin and is INVISIBLE "
      "to the even sector (the odd tier is the discriminating layer)",
      m1_odd_bites and m1_even_passes)


def mutant_norm(pt, g, H):
    """M2: q^r in place of the q^(r/2) scheme."""
    val = sigma_tower(blk(pt, g, H)).value
    q = Q(sum(x * x for x in g))
    out = []
    for i, s in enumerate(val):
        r = i + 1
        scale = q ** ((r + 1) // 2) / q ** r if r % 2 else q ** (r // 2) / q ** r
        out.append(s * scale if not isinstance(s, QSqrt)
                   else QSqrt(0, s.b * scale, s.r))
    return tuple(out)


m2_bites = any(mutant_norm(pt, g, H) != pin
               for name, (pt, g, H, pin) in CORPUS.items()
               if any(x != 0 for x in pin))
check("P8 M2 normalization mutant FAILS nonzero pins", m2_bites)

m3 = QSqrt(0, Q(-6, 49), 56)   # keystone sigma1 at radicand 4q instead of q
check("P8 M3 radicand-context mutant FAILS the pin (one sqrt per context "
      "is an identity, not formatting)", m3 != K_PIN[0])

print()
if FAILS:
    print(f"GATE G1.1: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE G1.1: CLOSED — sigma tower generic-n and parity-typed against "
      "the corpus, cross-routed to the channel sum at n=3, identically "
      "gauge-invariant, chart/regularity asymmetry pinned, odd sector live "
      "in the engine, mutants bite.")
sys.exit(0)
