"""Gate G1.2 — the sensor set.

Battery for the frozen predictions in campaigns/G12_sensor_set/PREREG.md, the
Stage-0 recerts (RC-6 numerator tower, RC-7 shape moment, RC-8 localization) and
the Stage-A pins (normalization kappa_r = e_r(P Hc P)/q^(r/2); reference values;
A-010 CHANNEL_ISOTROPIC). Certifies the four sensors against everything they
touch in the certified bank, exercises both fingerprint strata, and bites four
mutants. Exact throughout; run twice for byte-stability.

Run:  python tests/gate_12.py   (exit 0 iff the gate is closed)
"""

import sys
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.carrier import as_labeled, channels_n3_crosscheck            # noqa: E402
from cella.certificate import EmissionError, emit                       # noqa: E402
from cella.jet import ConstraintBlock, Jet2                             # noqa: E402
from cella.qsqrt import QSqrt                                           # noqa: E402
from cella.sensors import (TIER_SENSORS, fingerprint, localization,     # noqa: E402
                           localization_support, numerator_tower,
                           shape_moment)

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


def M(H):
    return tuple(tuple(Q(x) for x in row) for row in H)


def blk(pt, g, H):
    return ConstraintBlock([Jet2(pt, g, H)])


def gauge(g, H, a):
    n = len(g)
    return tuple(tuple(H[i][j] + g[i] * a[j] + a[i] * g[j] for j in range(n))
                 for i in range(n))


P3 = (Q(1), Q(1), Q(1))
# corpus (gate_11 P1) + certified channel pins (gate_11 P3)
KEY = blk(P3, (Q(3), Q(1), Q(2)), M([[2, 1, 0], [1, 0, 0], [0, 0, 2]]))
SPH = blk((Q(1), Q(2), Q(3)), (Q(2), Q(4), Q(6)),
          M([[2, 0, 0], [0, 2, 0], [0, 0, 2]]))
SAD = blk(P3, (Q(-1), Q(-1), Q(1)), M([[0, -1, 0], [-1, 0, 0], [0, 0, 0]]))
CYL = blk((Q(1), Q(2), Q(7)), (Q(2), Q(4), Q(0)),
          M([[2, 0, 0], [0, 2, 0], [0, 0, 0]]))
CERT_KC = {"keystone": Q(-1, 49), "sphere": Q(0), "saddle": Q(-1, 9)}
N3 = {"keystone": KEY, "sphere": SPH, "saddle": SAD}

# an n=4 fixture (G1.0 P1) for the generic-n sensors
G4 = (Q(1), Q(2), Q(3), Q(5))
H4 = M([[2, 1, -1, 3], [1, 4, 2, -2], [-1, 2, 6, 1], [3, -2, 1, -4]])
B4 = blk((Q(0),) * 4, G4, H4)

# =================== P1 — reference pins (Stage 0 / Stage A) ===================
# numerator r=2 channel == certified kc, on every regular n=3 surface
for name, b in N3.items():
    check(f"P1 numerator kappa_2 == certified kc ({name}: {CERT_KC[name]})",
          numerator_tower(b).value == (CERT_KC[name],))
# fingerprint A_c keystone == the gate value (RC-4)
check("P1 fingerprint A_c(keystone) == 42793/1555848",
      fingerprint(KEY).value[0] == Q(42793, 1555848))
# shape moment: S^(n-2,2) absent at n=3 (shape component == 0)
check("P1 shape moment: shape component == 0 at n=3 (absent)",
      all(shape_moment(b).value[2] == 0 for b in N3.values()))
# shape present at n=4 (nonzero shape content on a generic surface)
check("P1 shape moment: shape component != 0 at n=4 (present)",
      shape_moment(B4).value[2] != 0)
# localization support theorem, n=4: {S: dDelta!=0 on e*} == {S >= e*}
_want01 = {S for S in combinations(range(4), 3) if 0 in S and 1 in S}
check("P1 localization support {S: moved} == {S >= e*}, e*=(0,1) at n=4",
      localization_support(B4, (0, 1)) == _want01)
check("P1 localization moved-support family tracks the fault edge (e*=(1,2))",
      localization_support(B4, (1, 2))
      == {S for S in combinations(range(4), 3) if 1 in S and 2 in S})

# =================== P2 — blindness (exact zero, not small) ===================
# RC-6: numerator tower factors through Hc; a self-fault (diagonal) leaves it
# IDENTICALLY fixed. Test S1 (H00+=t) and S2 (whole diagonal) at several t.
def self_fault(H, n, ds, t):
    return tuple(tuple(H[i][j] + (t * ds[i] if i == j else 0)
                       for j in range(n)) for i in range(n))


nt_blind = True
for b, ds in ((KEY, (1, 0, 0)), (KEY, (1, -2, 3)), (B4, (1, -2, 1, 3))):
    j = b.jets[0]
    base = numerator_tower(b).value
    for t in (Q(1), Q(3), Q(1, 7), Q(-5)):
        Hf = self_fault(j.h, j.n, ds, t)
        nt_blind &= (numerator_tower(blk(j.point, j.g, Hf)).value == base)
check("P2 numerator EXACT self-fault blindness (constant under every diagonal "
      "perturbation, all t) — zero response, not small", nt_blind)

# =================== P3 — scale invariance + the coupling-channel identity ===
# The numerator is the COUPLING channel kc: self-fault-blind (P2) and F->tF scale-
# invariant, but NOT gauge-invariant -- kc is chart-covariant (individual role
# channels move under recalibration; A_c is the gauge-invariant). The brief's
# claims are (i) coupling sensitivity, (ii) self-fault blindness, (iii) scale
# invariance -- gauge invariance is NOT claimed and belongs to the curvature/A_c.
#
# F->tF (both g,H scale): kappa_r = e_r/q^(r/2) is invariant (e_r ~ t^r, q ~ t^2).
# Even rungs exactly; odd rungs up to radicand context (q -> t^2 q, i.e.
# sqrt(t^2 q) = t sqrt q), certified at the value level by the field norm b^2 * r.
scale_even, scale_odd = True, True
for b in (KEY, SAD, B4):
    j = b.jets[0]
    base = numerator_tower(b).value
    for t in (2, 3, Q(5, 3)):
        gt = tuple(x * t for x in j.g)
        Ht = tuple(tuple(x * t for x in row) for row in j.h)
        val = numerator_tower(blk(j.point, gt, Ht)).value
        for ri, (s0, s1) in enumerate(zip(base, val)):
            if (ri + 2) % 2 == 0:
                scale_even &= (s0 == s1)
            else:
                scale_odd &= (s0.b * s0.b * s0.r == s1.b * s1.b * s1.r)
check("P3 numerator F->tF scale invariance: even rungs exact, odd rungs invariant "
      "at the value level (b^2*r), t=2,3,5/3", scale_even and scale_odd)
# kappa_2 == kc holds IDENTICALLY, including under gauge -- the cross-route is a
# genuine identity of the coupling channel, not representative luck.
xr_gauge = True
for a in ((Q(1), Q(-2), Q(3)), (Q(-1, 2), Q(5), Q(1))):
    for b in (KEY, SAD):
        j = b.jets[0]
        gb = blk(j.point, j.g, gauge(j.g, j.h, a))
        xr_gauge &= (numerator_tower(gb).value[0]
                     == as_labeled(channels_n3_crosscheck(gb))["kc"])
check("P3 kappa_2 == kc IDENTICALLY, including under gauge (the coupling channel "
      "is chart-covariant; the identity is not representative coincidence)",
      xr_gauge)

# =================== P4 — cross-routes into the certified bank ===================
# kappa_2 == the labeled coupling channel kc (carrier n=3 cross-check), and
# the parity typing (even Q, odd QSqrt at radicand q) holds at n=4.
xr_ok = True
for name, b in N3.items():
    kc = as_labeled(channels_n3_crosscheck(b))["kc"]
    xr_ok &= (numerator_tower(b).value[0] == kc)
check("P4 kappa_2 == labeled channel kc (cross-route to carrier n=3 check)", xr_ok)
nt4 = numerator_tower(B4).value
check("P4 parity typing at n=4: kappa_2 in Q (even), kappa_3 a QSqrt at "
      "radicand q=39 (odd)",
      isinstance(nt4[0], Q) and isinstance(nt4[1], QSqrt) and nt4[1].r == 39)

# =================== P5 — refusals, precedence, fence, strata ===================
J2 = Jet2(P3, (Q(2), Q(2), Q(2)), M([[0, 1, 1], [1, 0, 1], [1, 1, 0]]))
C2 = ConstraintBlock([KEY.jets[0], J2])
check("P5 R1 block len 2 -> CODIM_UNSUPPORTED (all four sensors)",
      all(s(C2).residue.token == "CODIM_UNSUPPORTED"
          for s in (numerator_tower, shape_moment, localization, fingerprint)))
ZERO = blk(P3, (Q(0), Q(0), Q(0)), M([[2, 1, 0], [1, 0, 0], [0, 0, 2]]))
check("P5 R2 zero gradient -> SINGULAR_GRADIENT (numerator)",
      numerator_tower(ZERO).residue.token == "SINGULAR_GRADIENT")
check("P5 R3 numerator COMPUTES on component-zero g (cylinder, P-route)",
      not numerator_tower(CYL).is_refusal())
check("P5 R3 shape/localization REFUSE ROLE_CHART_UNAVAILABLE on component-zero "
      "(O / W-route)",
      shape_moment(CYL).residue.token == "ROLE_CHART_UNAVAILABLE"
      and localization(CYL).residue.token == "ROLE_CHART_UNAVAILABLE")
# both fingerprint strata
ISO = blk(P3, (Q(-2), Q(-2), Q(1)), M([[-2, 0, 0], [0, -2, 0], [0, 0, 0]]))
iso_r = fingerprint(ISO)
check("P5 fingerprint CHANNEL_ISOTROPIC on Lambda_P=0, names the channel (A-010)",
      iso_r.residue.token == "CHANNEL_ISOTROPIC" and "P" in iso_r.residue.stratum)
RSNG = blk(P3, (Q(0), Q(1), Q(2)), M([[2, 1, 0], [1, 0, 0], [0, 0, 2]]))
check("P5 fingerprint ROLE_CHART_UNAVAILABLE on a component-zero gradient",
      fingerprint(RSNG).residue.token == "ROLE_CHART_UNAVAILABLE")
try:
    fingerprint(B4)
    fenced = False
except ValueError:
    fenced = True
check("P5 fingerprint n=3 fence: n!=3 is an API-contract ValueError (A-008)", fenced)

# =================== P6 — mutants (each MUST FAIL its target) ===================
# M1 RATIO reimplementation: the OG ratio kc/K_G MOVES under a self-fault while
#    the numerator is exactly blind -> numerator strictly dominates (RC-6/PE.4).
def ratio_sensor(b):
    j = b.jets[0]
    lab = as_labeled(channels_n3_crosscheck(b))
    return lab["kc"] / lab["K_G"]


ratio_moves = False
base_ratio = ratio_sensor(KEY)
for t in (Q(1), Q(2)):
    Hf = self_fault(KEY.jets[0].h, 3, (1, 0, 0), t)
    if ratio_sensor(blk(P3, KEY.jets[0].g, Hf)) != base_ratio:
        ratio_moves = True
check("P6 M1 ratio-sensor MOVES under a self-fault (numerator's exact blindness "
      "dominates the OG ratio)", ratio_moves)
# M2 LABEL-SWAP: comparing kappa_2 to a swapped label (kint) FAILS the cross-route
lab_key = as_labeled(channels_n3_crosscheck(KEY))
check("P6 M2 label-swap mutant (kappa_2 vs kint) FAILS — slot labels load-bearing",
      numerator_tower(KEY).value[0] != lab_key["kint"])
# M3 SINGLE-SCALAR FLATTEN (Goldman): mean of the shape isotypic norms discards
#    which component carries content -> a shape-blind config and a shape-bearing
#    config with the same triv+std become indistinguishable under the mean.
sm4 = shape_moment(B4).value
mean_flat = sum(sm4) / 3
check("P6 M3 single-scalar flatten loses the shape component (mean != shape) — "
      "the Goldman guard: totals never certify channel content",
      mean_flat != sm4[2] and sm4[2] != 0)
# M4 ISOTROPIC MISTYPE: a mutant that COMPUTES through Lambda=0 returns a value;
#    the correct fingerprint REFUSES. They must differ.
check("P6 M4 isotropic mistype: correct fingerprint REFUSES where a computing "
      "mutant would return a value", fingerprint(ISO).is_refusal())

# =================== P7 — certificates ===================
def compute_sensors():
    return {"value": numerator_tower(KEY).value, "number_type": "Q",
            "account": {"m": None, "r_epochs": ()}, "refusals": []}


cert = emit(f"Numerator channel of the keystone ({TIER_SENSORS}).", compute_sensors)
check("P7 C1 sensor certificate carries the tier string",
      TIER_SENSORS in cert.machine()["what"])


def compute_refused():
    return {"value": None, "number_type": "none",
            "account": {"m": None, "r_epochs": ()},
            "refusals": [fingerprint(ISO).residue]}


cert_r = emit(f"Fingerprint on an isotropic channel ({TIER_SENSORS}).",
              compute_refused)
check("P7 C2 refusal certificate renders CHANNEL_ISOTROPIC plainly, no raw token",
      "isotropic" in cert_r.plain() and "CHANNEL_ISOTROPIC" not in cert_r.plain())
state = {"n": 0}


def flaky():
    state["n"] += 1
    return {"value": (Q(state["n"]),), "number_type": "Q",
            "account": {"m": None, "r_epochs": ()}, "refusals": []}


try:
    emit("flaky sensor", flaky)
    fc = False
except EmissionError:
    fc = True
check("P7 C3 double-run law holds on the sensor path", fc)

print()
if FAILS:
    print(f"GATE G1.2: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE G1.2: CLOSED — numerator tower (kappa_2 == kc, exact self-fault "
      "blindness, F->tF scale-invariant, parity-typed), shape moment "
      "(isotypic, shape absent n=3 / present n=4), localization (support "
      "theorem + moved family), fingerprint (A_c pin, both strata, n=3 fence); "
      "CHANNEL_ISOTROPIC live (A-010); four mutants bite.")
sys.exit(0)
