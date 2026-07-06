"""Gate G1.0 — jets and the carrier (Layer 1 opens).

Battery for the frozen prereg campaigns/G10_jets_carrier/PREREG.md
(sha 45947aa47e22f736, frozen before any implementation code existed).
Certifies: block typing + refusal precedence (A-009 tokens through cells and
certificates); the general-n carrier against 19 hand-pinned references at
n = 3, 4, 5; gauge invariance through the API; normal-form canonicality with
the Im(G_g) decomposition witness; purity wiring against the two-species
account; the labeled n=3 channel cross-check (label-convention case law);
and three mutants that MUST FAIL.

Run:  python tests/gate_10.py   (exit 0 iff the gate is closed)
"""

import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.carrier import (CHANNEL_SLOTS, TIER, as_labeled, carrier,   # noqa: E402
                           channels_n3_crosscheck, normal_form)
from cella.cell import Cell                                            # noqa: E402
from cella.certificate import EmissionError, emit                      # noqa: E402
from cella.jet import ConstraintBlock, Jet2                            # noqa: E402
from cella.refusal import PLAIN, VOCABULARY, Refusal                   # noqa: E402
from cella.residue import SPECIES_R, Account, Residue, madd, msub      # noqa: E402

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


def gauge(g, H, a):
    """Fresh gauge action for the sweep: H -> H + g a^T + a g^T."""
    n = len(g)
    return tuple(tuple(H[i][j] + g[i] * a[j] + a[i] * g[j] for j in range(n))
                 for i in range(n))


def blk(point, g, H):
    return ConstraintBlock([Jet2(point, g, H)])


# ---------------- fixtures and pins (PREREG P1) ----------------
K_PT, K_G3 = (Q(1), Q(1), Q(1)), (Q(3), Q(1), Q(2))
K_H3 = ((Q(2), Q(1), Q(0)), (Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(2)))
PIN3 = (Q(2, 3), Q(-13, 6), Q(-1, 2))

P4, G4 = (Q(0),) * 4, (Q(1), Q(2), Q(3), Q(5))
H4 = ((Q(2), Q(1), Q(-1), Q(3)), (Q(1), Q(4), Q(2), Q(-2)),
      (Q(-1), Q(2), Q(6), Q(1)), (Q(3), Q(-2), Q(1), Q(-4)))
PIN4 = (Q(-2), Q(-5), Q(-8, 5), Q(-3), Q(-31, 5), Q(-14, 5))

P5, G5 = (Q(0),) * 5, (Q(2), Q(1), Q(3), Q(7), Q(5))
H5 = ((Q(4), Q(1), Q(-2), Q(3), Q(-1)), (Q(1), Q(2), Q(5), Q(-3), Q(2)),
      (Q(-2), Q(5), Q(-6), Q(1), Q(-4)), (Q(3), Q(-3), Q(1), Q(10), Q(6)),
      (Q(-1), Q(2), Q(-4), Q(6), Q(8)))
PIN5 = (Q(-2), Q(-3), Q(-38, 7), Q(-38, 5), Q(3), Q(-75, 7), Q(-19, 5),
        Q(41, 7), Q(-7, 5), Q(-111, 35))

FIXTURES = (("n3 keystone", K_PT, K_G3, K_H3, PIN3),
            ("n4 fixture", P4, G4, H4, PIN4),
            ("n5 fixture", P5, G5, H5, PIN5))

GAUGE_ROWS = {
    3: ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(1), Q(-2), Q(3)),
        (Q(-1, 2), Q(5), Q(1)), (Q(2), Q(3), Q(-1))),
    4: ((Q(1), Q(0), Q(0), Q(0)), (Q(0), Q(-1), Q(2), Q(0)),
        (Q(1, 3), Q(-2), Q(5), Q(7)), (Q(2), Q(2), Q(-3), Q(-1, 2))),
    5: ((Q(1), Q(0), Q(0), Q(0), Q(0)), (Q(0), Q(2), Q(-1), Q(3), Q(0)),
        (Q(-1, 2), Q(1), Q(7), Q(-2), Q(1, 3))),
}

# P1 — carrier pins through the API
for name, pt, g, H, pin in FIXTURES:
    c = carrier(blk(pt, g, H))
    check(f"P1 {name}: O == hand pin, exact reconstruction",
          not c.is_refusal() and c.value == pin and c.reconstruct() == pin)

# P2 — gauge-invariance sweep through the API (K-1 armed at n=4,5)
for name, pt, g, H, pin in FIXTURES:
    for a in GAUGE_ROWS[len(g)]:
        moved = carrier(blk(pt, g, gauge(g, H, a)))
        check(f"P2 {name}: O gauge-invariant a={tuple(map(str, a))}",
              moved.value == pin)

# P3 — normal-form canonicality (K-3 armed)
for name, pt, g, H, pin in FIXTURES:
    n = len(g)
    base_nf = normal_form(blk(pt, g, H))
    ok_shape = (all(base_nf.value[i][i] == 0 for i in range(n))
                and tuple(base_nf.value[i][j] for i in range(n)
                          for j in range(i + 1, n)) == pin
                and all(base_nf.value[i][j] == base_nf.value[j][i]
                        for i in range(n) for j in range(n)))
    check(f"P3 {name}: H_perp zero-diagonal, off-diagonal == O, symmetric",
          ok_shape)
    canonical = all(normal_form(blk(pt, g, gauge(g, H, a))).value
                    == base_nf.value for a in GAUGE_ROWS[n])
    check(f"P3 {name}: H_perp canonical under every gauge row", canonical)
    witness_ok = True
    for a in GAUGE_ROWS[n]:
        Hg = gauge(g, H, a)
        D = tuple(tuple(Hg[i][j] - base_nf.value[i][j] for j in range(n))
                  for i in range(n))
        arec = tuple(D[i][i] / (2 * g[i]) for i in range(n))
        witness_ok &= all(D[i][j] == g[i] * arec[j] + arec[i] * g[j]
                          for i in range(n) for j in range(n))
    check(f"P3 {name}: H - H_perp has an exact gauge preimage (Im(G_g))",
          witness_ok)

# P4 — the labeled n=3 cross-check (K-2 armed; label case law)
cc = channels_n3_crosscheck(blk(K_PT, K_G3, K_H3))
lab = as_labeled(cc)
check("P4 keystone labeled channels kc=-1/49 kint=-3/49 ks=1/49 K_G=-3/49",
      lab == {"kc": Q(-1, 49), "kint": Q(-3, 49), "ks": Q(1, 49),
              "K_G": Q(-3, 49)})
check("P4 slot constant pins the order (kc, kint, ks) — interaction MIDDLE",
      CHANNEL_SLOTS == ("kc", "kint", "ks"))
try:
    channels_n3_crosscheck(blk(P4, G4, H4))
    n3_only = False
except ValueError:
    n3_only = True
check("P4 cross-check refuses the pathway role: n=4 call is a contract error",
      n3_only)

# P5 — refusal rows and precedence
j1 = Jet2(K_PT, K_G3, K_H3)
j2 = Jet2(K_PT, (Q(2), Q(2), Q(2)),
          ((Q(0), Q(1), Q(1)), (Q(1), Q(0), Q(1)), (Q(1), Q(1), Q(0))))
r1 = carrier(ConstraintBlock([j1, j2]))
check("P5 R1 block len 2 -> CODIM_UNSUPPORTED refusal cell",
      r1.is_refusal() and r1.residue.token == "CODIM_UNSUPPORTED"
      and r1.value is None)
r2 = carrier(blk(K_PT, (Q(0), Q(0), Q(0)), K_H3))
check("P5 R2 zero gradient -> SINGULAR_GRADIENT",
      r2.is_refusal() and r2.residue.token == "SINGULAR_GRADIENT")
r3 = carrier(blk(K_PT, (Q(3), Q(1), Q(0)), K_H3))
check("P5 R3 component zero -> ROLE_CHART_UNAVAILABLE naming {2}",
      r3.is_refusal() and r3.residue.token == "ROLE_CHART_UNAVAILABLE"
      and "{2}" in r3.residue.stratum)
r4 = carrier(blk(P4, (Q(0), Q(2), Q(0), Q(1)), H4))
check("P5 R4 two components zero -> ROLE_CHART_UNAVAILABLE naming {0, 2}",
      r4.is_refusal() and r4.residue.token == "ROLE_CHART_UNAVAILABLE"
      and "{0, 2}" in r4.residue.stratum)
check("P5 vocabulary grew to 7 and both new tokens render plainly (A-009)",
      len(VOCABULARY) == len(PLAIN) == 7
      and all(t not in Refusal(t, "s").plain()
              and "_" not in Refusal(t, "s").plain().replace("(stratum: s).", "")
              for t in ("CODIM_UNSUPPORTED", "ROLE_CHART_UNAVAILABLE")))
try:
    Jet2(K_PT, (3.0, 1.0, 2.0), K_H3)
    float_blocked = False
except TypeError:
    float_blocked = True
check("P5 R6 float in a jet is a TypeError, not a refusal", float_blocked)

# P6 — purity wiring: the carrier meets the two-species account
a_r = (Q(1), Q(-2), Q(3))
acct = Account().absorb(Residue(SPECIES_R, a_r, base=K_G3))
gauged_H = gauge(K_G3, K_H3, acct.r_epochs[0][1])
check("P6 U1 R-epoch through the Account leaves O fixed (purity)",
      carrier(blk(K_PT, K_G3, gauged_H)).value == PIN3
      and acct.m_total is None)
E = ((Q(0), Q(1), Q(0)), (Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(0)))
H_defect = madd(K_H3, E)
moved = carrier(blk(K_PT, K_G3, H_defect))
check("P6 U2 M-defect moves O; pinned witness (5/3, -13/6, -1/2)",
      moved.value == (Q(5, 3), Q(-13, 6), Q(-1, 2)))
H_corrected = msub(H_defect, E)
check("P6 U3 M-corrected reconstruction recovers truth's O exactly",
      carrier(blk(K_PT, K_G3, H_corrected)).value == PIN3)

# P7 — certificates with tier language
def compute_carrier():
    cell = carrier(blk(K_PT, K_G3, K_H3))
    return {"value": cell.value, "number_type": "Q",
            "account": {"m": cell.residue, "r_epochs": ()}, "refusals": []}


cert = emit(f"Gauge-normal carrier O of the keystone block ({TIER}).",
            compute_carrier,
            depends=("Valid for this constraint block at this base point.",))
check("P7 C1 value certificate: tier stated, 16-hex rerun digest",
      TIER in cert.machine()["what"]
      and len(cert.machine()["rerun_digest"]) == 16)


def compute_refused():
    cell = carrier(ConstraintBlock([j1, j2]))
    return {"value": None, "number_type": "none",
            "account": {"m": None, "r_epochs": ()},
            "refusals": [cell.residue]}


cert_r = emit(f"Carrier for a two-constraint system ({TIER}).", compute_refused)
check("P7 C2 refusal certificate renders the reason, no raw token",
      "system of constraints" in cert_r.plain()
      and "CODIM_UNSUPPORTED" not in cert_r.plain())
state = {"n": 0}


def flaky():
    state["n"] += 1
    return {"value": Q(state["n"]), "number_type": "Q",
            "account": {"m": None, "r_epochs": ()}, "refusals": []}


try:
    emit("flaky carrier", flaky)
    flaky_caught = False
except EmissionError:
    flaky_caught = True
check("P7 C3 double-run law holds on the carrier path", flaky_caught)

# P8 — mutants MUST FAIL their target rows
def mutant_flatten(block):
    """M1 GOLDMAN-FLATTEN: mean over components — total preserved, content
    destroyed."""
    c = carrier(block)
    mean = sum(c.value) / len(c.value)
    return tuple(mean for _ in c.value)


m1_bites = all(mutant_flatten(blk(pt, g, H)) != pin
               for _, pt, g, H, pin in FIXTURES)
m1_total_preserved = (sum(mutant_flatten(blk(K_PT, K_G3, K_H3)))
                      == sum(PIN3))
check("P8 M1 Goldman-flatten preserves the total yet FAILS every O pin "
      "(totals never certify alone)", m1_bites and m1_total_preserved)


def mutant_dropped(g, H):
    """M2 DROPPED-TERM: third term omitted — the gauge-killing term."""
    n = len(g)
    return tuple(H[i][j] - g[i] * H[j][j] / (2 * g[j])
                 for i in range(n) for j in range(i + 1, n))


m2_bites = any(mutant_dropped(K_G3, gauge(K_G3, K_H3, a))
               != mutant_dropped(K_G3, K_H3) for a in GAUGE_ROWS[3])
check("P8 M2 dropped-term mutant FAILS the gauge sweep", m2_bites)

swapped = {"kc": lab["kc"], "kint": lab["ks"], "ks": lab["kint"],
           "K_G": lab["K_G"]}
check("P8 M3 label-swap mutant FAILS the labeled pin (case law armed)",
      swapped != lab and swapped["kint"] != lab["kint"])

print()
if FAILS:
    print(f"GATE G1.0: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE G1.0: CLOSED — jets block-typed, carrier general-n and "
      "gauge-invariant against hand pins, normal form canonical with gauge "
      "preimage witness, refusals typed through certificates, channel "
      "cross-check labeled and n=3-fenced, mutants bite.")
sys.exit(0)
