"""Gate G0.4 — refusals, the two-register certificate, observation wiring.

Certifies: every vocabulary token renders in plain language; value and
refusal paths both produce schema-conformant certificates (never exceptions,
never NaN); composition short-circuits refusals; emission requires
double-run bit-identity; the QSqrt rung flows through cells and records.

Run:  python tests/gate_04.py   (exit 0 iff the gate is closed)
"""

import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.cell import Cell                                   # noqa: E402
from cella.certificate import EmissionError, canon, emit      # noqa: E402
from cella.observation import ObservationMap                  # noqa: E402
from cella.qsqrt import QSqrt                                 # noqa: E402
from cella.refusal import PLAIN, VOCABULARY, Refusal          # noqa: E402

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


# 1 — the closed vocabulary renders plainly, and only admitted tokens exist
renders = [Refusal(t, "test stratum").plain() for t in VOCABULARY]
# Vocabulary count: 5 at G0.4 close; 7 since A-009 (G1.0 — CODIM_UNSUPPORTED,
# ROLE_CHART_UNAVAILABLE); 8 since A-010 (G1.2 — CHANNEL_ISOTROPIC). Updates
# declared in advance: G1.0 PREREG P9, G1.2 PREREG Stage-A declaration.
check("G0.4 every token renders plain language (no raw token, no underscores)",
      all(t not in txt and "_" not in txt for t, txt in zip(VOCABULARY, renders))
      and len(renders) == len(PLAIN) == 8)
try:
    Refusal("MADE_UP_TOKEN", "x")
    closed = False
except ValueError:
    closed = True
check("G0.4 vocabulary is closed: unknown token rejected", closed)

# 2 — value path through an observation map
def round3(T):
    v = Q(round(T * 1000), 1000)
    return ("ok", v, T - v)


def round1(T):
    v = Q(round(T * 10), 10)
    return ("ok", v, T - v)


m3, m1 = ObservationMap("round3", round3), ObservationMap("round1", round1)
c = m3.apply(Q(1, 3))
check("G0.4 value path: cell reconstructs exactly", c.reconstruct() == Q(1, 3)
      and not c.is_refusal())

# 3 — composition: residues add; reconstruction survives the chain
cc = m3.then(m1).apply(Q(1, 3))
check("G0.4 chained maps: composed residue reconstructs",
      cc.reconstruct() == Q(1, 3) and cc.value == Q(3, 10))

# 4 — refusal path: never an exception, never NaN
def lockstep_guard(T):
    cols = T
    if all(x == cols[0] for x in cols):
        return Refusal("RANK_DEFICIENT", "lockstep channels",
                       "All channels carried the same values in this window.")
    return ("ok", cols, tuple(Q(0) for _ in cols))


mg = ObservationMap("fit", lockstep_guard)
rc = mg.apply((Q(1), Q(1), Q(1)))
check("G0.4 refusal path: refusal cell, value None, reconstruct = the Refusal",
      rc.is_refusal() and rc.value is None
      and isinstance(rc.reconstruct(), Refusal))
rc2 = m3.then(ObservationMap("always-refuse",
                             lambda T: Refusal("BELOW_DETECTION", "tiny signal"))
              ).apply(Q(1, 3))
check("G0.4 refusal short-circuits through composition", rc2.is_refusal())

# 5 — certificate, value path
def compute_value():
    cell = m3.apply(Q(1, 3))
    return {"value": cell.value, "number_type": "Q",
            "account": {"m": cell.residue, "r_epochs": ()}, "refusals": []}


cert = emit("Rounded reading of channel x over window W.", compute_value,
            depends=("A different window length could change this value.",))
mach = cert.machine()
check("G0.4 machine register complete with 16-hex rerun digest",
      all(k in mach for k in ("schema", "what", "value", "number_type",
                              "account", "refusals", "depends", "rerun_digest"))
      and len(mach["rerun_digest"]) == 16)
p = cert.plain()
check("G0.4 plain register: four headings, no raw tokens, honest exactness line",
      all(h in p for h in ("WHAT WAS COMPUTED", "WHAT IS EXACT",
                           "WHAT WAS REFUSED, AND WHY",
                           "WHAT WOULD CHANGE THIS RESULT"))
      and not any(t in p for t in VOCABULARY)
      and "leftover from measurement" in p)

# 6 — certificate, refusal path
def compute_refused():
    cell = mg.apply((Q(2), Q(2), Q(2)))
    return {"value": None, "number_type": "none",
            "account": {"m": None, "r_epochs": ()},
            "refusals": [cell.residue]}


cert_r = emit("Surface fit for channels (a, b, c), window W.", compute_refused)
check("G0.4 refusal certificate renders the plain reason, no exception",
      "lockstep" in cert_r.plain() and "Nothing here is a numeric value"
      in cert_r.plain())

# 7 — emission law: nondeterminism cannot certify
state = {"n": 0}


def flaky():
    state["n"] += 1
    return {"value": Q(state["n"]), "number_type": "Q",
            "account": {"m": None, "r_epochs": ()}, "refusals": []}


try:
    emit("flaky", flaky)
    flaky_caught = False
except EmissionError:
    flaky_caught = True
check("G0.4 double-run law: nondeterministic compute cannot emit", flaky_caught)

# 8 — the tower flows through cells and records
s1 = QSqrt(0, Q(6, 49), 14)
cq = Cell(s1, Q(0))
check("G0.4 QSqrt cell reconstructs; canon is deterministic",
      cq.reconstruct() == s1
      and canon(s1) == "(0/1)+(6/49)*sqrt(14/1)")

# 9 — no NaN can enter anywhere
try:
    Cell(float("nan"), Q(0))
    nan_blocked = False
except TypeError:
    nan_blocked = True
check("G0.4 NaN/float blocked at the cell boundary", nan_blocked)

print()
if FAILS:
    print(f"GATE G0.4: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE G0.4: CLOSED — refusals first-class, certificates two-register "
      "and double-run gated, observation wiring refuse-not-lie.")
sys.exit(0)
