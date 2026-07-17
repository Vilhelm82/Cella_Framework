"""c001 `three_channel_kg` — STAGE D battery (covenant step 2/3/4).

Frame honesty, CL-c7 (PARTIAL by design). Implements the FROZEN `prereg.json`
(pin `ae399cb1...`). It:

  * loads the frozen prereg and re-verifies its sha256 pin;
  * embeds every governing clause VERBATIM in `GRADER_CLAUSES` and string-
    compares each against the frozen prereg's `grader_clauses` at runtime --
    ANY drift -> `ClauseDrift` REFUSAL (Rule 1.8 / covenant step 2);
  * re-verifies the bench module shas against the prereg `depends_on` (Rule 1.9
    content pins) -- ANY mismatch -> `PinDrift` REFUSAL;
  * imports the FROZEN bench READ-ONLY (probe Path A; referee_total Path B;
    referee_channel Path B'; oracle Path C; fixtures; schema) from the STABLE
    main path -- never edits it. (The worktree is bench-less by design; the
    bench is committed on main and referenced by exact absolute path.)
  * runs each of the 9 frame-honesty predictions exact-Q (no tolerance), emits
    one `three_channel_kg_record_v1` per evaluation step on the F12 fixtures,
    and writes a deterministic, sorted-keys, byte-stable records jsonl;
  * grades mechanically into prediction verdicts.

PARTIAL by design: the provable core (F12a channels MOVE while K_G invariant —
frame-relativity / R2; F12b channels FIXED and K_G invariant — S3 x {+/-} at
n=3) is graded; CL-c3c-ii (no invariant scalar through Sigma recovers the
representative) is recorded OPEN and NOT closed; K-soft is a non-refuting FLAG.
CL-c7's proposed move is PARTIAL, never DEMONSTRATED.

Determinism: every value is a `fractions.Fraction` serialised as `frac:n/d`;
records are emitted in a fixed order with `json.dumps(..., sort_keys=True)`; no
float, no time, no randomness. Two runs MUST be byte-identical. The bench is
imported read-only; nothing here mutates it.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from fractions import Fraction
from types import ModuleType
from typing import Any, Dict, List, Tuple

# --------------------------------------------------------------------------
# paths: STAGE / RESULTS derived from this file's location (__file__) so the
# committed grader re-runs from wherever it lives (the originating worktree OR
# `main` after merge) -- records/prereg content is path-independent. The frozen
# bench, however, is NOT in this (bench-less) worktree: it is committed on main
# and referenced at the STABLE main absolute path. The bench is loaded
# READ-ONLY by exact file path (shadow-proof: binding to the resolved file path
# is unambiguous and binds to exactly the files pinned in depends_on). The
# bench modules import only stdlib -- no inter-module / no lloyd_v4 package
# imports -- so direct file-path loading is sound and preserves the
# code-disjoint referee separation.
# --------------------------------------------------------------------------
STAGE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.dirname(STAGE)
BENCH_DIR = "/home/wlloyd/Lloyd_Engine_V4/src/lloyd_v4/evals/three_channel_kg"
PREREG_PATH = os.path.join(STAGE, "prereg.json")
PREREG_PIN_PATH = os.path.join(STAGE, "prereg_sha256.pin")


def _load_bench_module(name: str) -> ModuleType:
    """Load a bench module READ-ONLY from its exact pinned file path under the
    stable main BENCH_DIR. Shadow-proof; never imports/edits the bench package."""
    path = os.path.join(BENCH_DIR, f"{name}.py")
    modname = f"three_channel_kg_bench_{name}"
    spec = importlib.util.spec_from_file_location(modname, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load bench module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    return mod


bench_schema = _load_bench_module("schema")
bench_fixtures = _load_bench_module("fixtures")
bench_probe = _load_bench_module("probe")
bench_reft = _load_bench_module("referee_total")
bench_refc = _load_bench_module("referee_channel")
bench_oracle = _load_bench_module("oracle")

Q = Fraction


# --------------------------------------------------------------------------
# refusals (the battery REFUSES rather than running on a drifted contract)
# --------------------------------------------------------------------------
class ClauseDrift(RuntimeError):
    """An embedded governing clause does not byte-match the frozen prereg."""


class PinDrift(RuntimeError):
    """A bench module sha256 does not match the frozen prereg depends_on."""


class PreregPinMismatch(RuntimeError):
    """The frozen prereg's own sha256 does not match prereg_sha256.pin."""


# --------------------------------------------------------------------------
# GRADER_CLAUSES embedded VERBATIM (covenant step 2 / Rule 1.8). These MUST be
# byte-identical to prereg.json -> grader_clauses; the gate below string-
# compares and REFUSES on any drift.
# --------------------------------------------------------------------------
GRADER_CLAUSES: Dict[str, str] = {
    "K7_frame_undeclared":
        "a legitimate rechart reported as a curvature error, or `σ₂` "
        "not held invariant under F12. *(CL-c7)*",
    "K_soft_completeness":
        "two surfaces, identical `{σ_r}`+orientation, not gauge+permutation "
        "related. *(L1; CL-c3c-ii / CL-c7 completeness)*",
    "CL_c7_statement":
        "frame honesty — sum intrinsic; channels frame-relative, `S₃`+signs "
        "invariants (n=3); completeness OPEN",
    "CL_c3c_ii_statement":
        "no **invariant** scalar (factoring through `Σ`) recovers the channel "
        "representative",
    "CL_c3c_ii_open":
        "NOT_YET_PROBED (OPEN — blocked on `{σ_r}`-completeness / L1)",
    "R2_supplied_frame":
        "disposition: the channels are frame-relative in the supplied DBP "
        "frame; only the sum `K_G` is intrinsic",
    "R3_F12_pin":
        "CLOSED. `R∈SO(3)`, rotated jet, and tuples pinned in `FIXTURES.md` "
        "(exact ℚ).",
    "semantics_K_G": "kappa_c + kappa_s + kappa_int (exact in Q)",
    "semantics_total_referee": "K_G == -det(H_b)/q^2 (Path B, sqrt-q-free)",
    "semantics_channel_referee":
        "channels == split-shape-operator det2 channels (Path B', disjoint source)",
    "precondition_P_self_cert":
        "the oracle (Path C) must be external to A/B/B', or the run is void.",
    "precondition_P_frame":
        "every channel fixture must carry its frame annotation, or it is rejected.",
    "type_gate_sqrt_q_leak":
        "a total/channel referee returning a radical/float instead of Fraction "
        "-> hard fail (K8).",
}


# --------------------------------------------------------------------------
# gates: prereg pin, clause drift, bench pin drift
# --------------------------------------------------------------------------
def load_prereg() -> Dict[str, Any]:
    with open(PREREG_PATH, "rb") as fh:
        raw = fh.read()
    actual = hashlib.sha256(raw).hexdigest()
    with open(PREREG_PIN_PATH, "r", encoding="utf-8") as fh:
        pinned = fh.read().strip()
    if actual != pinned:
        raise PreregPinMismatch(f"prereg.json sha256 {actual} != pin {pinned}")
    return json.loads(raw)


def gate_clauses(prereg: Dict[str, Any]) -> None:
    frozen = prereg["grader_clauses"]
    if set(GRADER_CLAUSES) != set(frozen):
        raise ClauseDrift(
            f"clause key set drift: embedded={sorted(GRADER_CLAUSES)} "
            f"frozen={sorted(frozen)}")
    for key, embedded in GRADER_CLAUSES.items():
        if embedded != frozen[key]:
            raise ClauseDrift(
                f"clause {key!r} drift:\n embedded={embedded!r}\n frozen={frozen[key]!r}")


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def gate_bench_pins(prereg: Dict[str, Any]) -> None:
    dep = prereg["depends_on"]
    checks = {
        "src/lloyd_v4/evals/three_channel_kg/probe.py": os.path.join(BENCH_DIR, "probe.py"),
        "src/lloyd_v4/evals/three_channel_kg/schema.py": os.path.join(BENCH_DIR, "schema.py"),
        "src/lloyd_v4/evals/three_channel_kg/fixtures.py": os.path.join(BENCH_DIR, "fixtures.py"),
        "src/lloyd_v4/evals/three_channel_kg/referee_total.py": os.path.join(BENCH_DIR, "referee_total.py"),
        "src/lloyd_v4/evals/three_channel_kg/referee_channel.py": os.path.join(BENCH_DIR, "referee_channel.py"),
        "src/lloyd_v4/evals/three_channel_kg/oracle.py": os.path.join(BENCH_DIR, "oracle.py"),
        "results/three_channel_kg/manifest_v1.json": os.path.join(RESULTS, "manifest_v1.json"),
    }
    for key, path in checks.items():
        actual = sha256_file(path)
        if key not in dep:
            raise PinDrift(f"{key} missing from prereg depends_on")
        if actual != dep[key]:
            raise PinDrift(f"{key} sha256 {actual} != pinned {dep[key]}")


# --------------------------------------------------------------------------
# exact-Q helpers + record construction
# --------------------------------------------------------------------------
def fr(x: Fraction) -> str:
    return bench_schema.fr(x)


ACCOUNT = {"ledger": "stage_d", "covenant": "role=probe + account",
           "campaign": "three_channel_kg", "cycle": "c001"}


def _rec(records: List[Dict[str, Any]], *,
         fixture_id: str, role: str, path: str,
         frame: str | None = None,
         g: Tuple[str, ...] | None = None,
         H: Tuple[Tuple[str, ...], ...] | None = None,
         q: str | None = None,
         delta_c: str | None = None, delta_s: str | None = None,
         delta_m: str | None = None, det_hb: str | None = None,
         kappa_c: str | None = None, kappa_s: str | None = None,
         kappa_int: str | None = None, K_G: str | None = None,
         account: Dict[str, Any] | None = None,
         closure_ok: bool | None = None,
         referee: Dict[str, Any] | None = None,
         refusals: Tuple[str, ...] = (),
         telemetry: Dict[str, Any] | None = None,
         notes: str = "") -> None:
    """Build, validate (role gate + exact-Q discipline via schema.validate),
    stamp, and append one record."""
    rec = bench_schema.ThreeChannelKGRecord(
        campaign_id=bench_schema.CAMPAIGN_ID,
        cycle_id=bench_schema.CYCLE_ID,
        schema_version=bench_schema.SCHEMA_VERSION,
        stage="stage_d",
        fixture_id=fixture_id,
        role=role,
        path=path,
        point=None,
        frame=frame,
        g=g,
        H=H,
        q=q,
        delta_c=delta_c, delta_s=delta_s, delta_m=delta_m, det_hb=det_hb,
        kappa_c=kappa_c, kappa_s=kappa_s, kappa_int=kappa_int, K_G=K_G,
        account=account,
        closure_ok=closure_ok,
        referee=referee if referee is not None else {},
        refusals=refusals,
        telemetry=telemetry if telemetry is not None else {},
        notes=notes,
    )
    bench_schema.validate(rec)
    rec.stamp_hash()
    records.append(json.loads(bench_schema.to_json(rec)))


# --------------------------------------------------------------------------
# F12 helpers: orthogonality of the recharts (R3 pinned), all exact Q.
# --------------------------------------------------------------------------
def _matmul(A, B):
    n = len(A)
    return [[sum((A[i][t] * B[t][j] for t in range(n)), Q(0)) for j in range(n)]
            for i in range(n)]


def _transpose(A):
    n = len(A)
    return [[A[j][i] for j in range(n)] for i in range(n)]


def _is_identity(M) -> bool:
    return all(M[i][j] == (Q(1) if i == j else Q(0))
               for i in range(len(M)) for j in range(len(M)))


def _det3(M) -> Fraction:
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


# The two recharts, exact Q (R3 pinned, transcribed from FIXTURES.md §F12).
_R = [[Q(3, 5), Q(-4, 5), Q(0)],
      [Q(4, 5), Q(3, 5), Q(0)],
      [Q(0), Q(0), Q(1)]]
_P = [[Q(0), Q(1), Q(0)],
      [Q(1), Q(0), Q(0)],
      [Q(0), Q(0), Q(1)]]


def rechart_is_orthogonal(M) -> Tuple[bool, Fraction]:
    """(M^T M == I, det M). A legitimate rechart is orthogonal; K7 fires if a
    legitimate rechart is reported as a curvature error."""
    ortho = _is_identity(_matmul(_transpose(M), M))
    return ortho, _det3(M)


# --------------------------------------------------------------------------
# the run: produce records + grade the 9 frame-honesty predictions
# --------------------------------------------------------------------------
F12 = ("F12a", "F12b")


def _channels(d) -> Tuple[Fraction, Fraction, Fraction]:
    return (d["kappa_c"], d["kappa_s"], d["kappa_int"])


def run() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    prereg = load_prereg()
    gate_clauses(prereg)
    gate_bench_pins(prereg)

    # Stage-0 control: every frozen fixture reproduces exactly (raises on drift).
    fx = bench_fixtures.generate_and_check()

    records: List[Dict[str, Any]] = []
    verdicts: Dict[str, Any] = {}

    # base = keystone F8 in the declared DBP frame.
    base = bench_probe.read_off(fx["F8"].g, fx["F8"].H)
    base_ch = _channels(base)
    base_kg = base["K_G"]

    # ---- emit base + per-F12-fixture records across A/B/Bprime/C ----
    _rec(records, fixture_id="F8", role="probe", path="A",
         frame=fx["F8"].frame,
         g=tuple(fr(x) for x in fx["F8"].g),
         H=tuple(tuple(fr(x) for x in row) for row in fx["F8"].H),
         q=fr(base["q"]),
         delta_c=fr(base["Delta_c"]), delta_s=fr(base["Delta_s"]),
         delta_m=fr(base["Delta_m"]), det_hb=fr(base["det_hb"]),
         kappa_c=fr(base["kappa_c"]), kappa_s=fr(base["kappa_s"]),
         kappa_int=fr(base["kappa_int"]), K_G=fr(base["K_G"]),
         account=ACCOUNT, closure_ok=True,
         notes="base jet (keystone F8, declared DBP frame) — the frame-honesty datum")

    a = {}   # Path A read-off per F12 fixture
    bt = {}  # Path B total per F12 fixture
    bp = {}  # Path B' channels per F12 fixture
    orc = {}  # Path C oracle per F12 fixture
    for fid in F12:
        f = fx[fid]
        a[fid] = bench_probe.read_off(f.g, f.H)
        bt[fid] = bench_reft.referee_total(f.g, f.H)
        bp[fid] = bench_refc.referee_channel(f.g, f.H)
        orc[fid] = bench_oracle.oracle(fid)
        # Path A probe record (role=probe; carries account + closure).
        _rec(records, fixture_id=fid, role="probe", path="A",
             frame=f.frame,
             g=tuple(fr(x) for x in f.g),
             H=tuple(tuple(fr(x) for x in row) for row in f.H),
             q=fr(a[fid]["q"]),
             delta_c=fr(a[fid]["Delta_c"]), delta_s=fr(a[fid]["Delta_s"]),
             delta_m=fr(a[fid]["Delta_m"]), det_hb=fr(a[fid]["det_hb"]),
             kappa_c=fr(a[fid]["kappa_c"]), kappa_s=fr(a[fid]["kappa_s"]),
             kappa_int=fr(a[fid]["kappa_int"]), K_G=fr(a[fid]["K_G"]),
             account=ACCOUNT, closure_ok=(a[fid]["K_G"] == base_kg),
             referee={"K_G_invariant_vs_base": a[fid]["K_G"] == base_kg,
                      "channels_vs_base": ("FIXED" if _channels(a[fid]) == base_ch
                                           else "MOVED")},
             notes=f"{fid} Path A read-off (frame: {f.frame})")
        # Path B total referee record.
        _rec(records, fixture_id=fid, role="referee_total", path="B",
             frame=f.frame, K_G=fr(bt[fid]),
             notes=f"{fid} Path B total -det(H_b)/q^2 (Bareiss)")
        # Path B' channel referee record.
        _rec(records, fixture_id=fid, role="referee_channel", path="Bprime",
             frame=f.frame,
             kappa_c=fr(bp[fid].kappa_c), kappa_s=fr(bp[fid].kappa_s),
             kappa_int=fr(bp[fid].kappa_int), K_G=fr(bp[fid].K_G),
             notes=f"{fid} Path B' split shape-operator channels")
        # Path C oracle record.
        _rec(records, fixture_id=fid, role="oracle", path="C",
             frame=orc[fid].frame,
             kappa_c=fr(orc[fid].kappa_c), kappa_s=fr(orc[fid].kappa_s),
             kappa_int=fr(orc[fid].kappa_int), K_G=fr(orc[fid].K_G),
             notes=f"{fid} Path C frozen external oracle")

    # ===== P1 F12a channels MOVE (frame-relativity / R2 core) =====
    a12a, bp12a, orc12a = a["F12a"], bp["F12a"], orc["F12a"]
    expect_move = (Q(-961, 30625), Q(2713, 30625), Q(-3627, 30625))
    a_move = _channels(a12a)
    bp_move = (bp12a.kappa_c, bp12a.kappa_s, bp12a.kappa_int)
    orc_move = (orc12a.kappa_c, orc12a.kappa_s, orc12a.kappa_int)
    p1 = {
        "pathA_channels_eq_expected_move": a_move == expect_move,
        "pathBprime_channels_eq_expected_move": bp_move == expect_move,
        "pathC_channels_eq_expected_move": orc_move == expect_move,
        "moved_off_base": a_move != base_ch,
        "A_eq_Bprime_eq_C": a_move == bp_move == orc_move,
    }
    verdicts["P1_F12a_channels_move"] = {
        "pass": all(p1.values()),
        "F12a_channels": [fr(x) for x in a_move],
        "base_channels": [fr(x) for x in base_ch],
        "detail": p1}

    # ===== P2 F12a K_G invariant (intrinsic sum) =====
    p2 = {
        "pathA_KG_eq_base": a12a["K_G"] == base_kg,
        "pathA_KG_eq_m3_49": a12a["K_G"] == Q(-3, 49),
        "pathB_total_eq_m3_49": bt["F12a"] == Q(-3, 49),
        "pathBprime_sum_eq_m3_49": bp12a.K_G == Q(-3, 49),
        "pathC_KG_eq_m3_49": orc12a.K_G == Q(-3, 49),
        "q_prime_eq_14": a12a["q"] == Q(14),
    }
    verdicts["P2_F12a_KG_invariant"] = {
        "pass": all(p2.values()),
        "F12a_K_G": fr(a12a["K_G"]), "base_K_G": fr(base_kg), "detail": p2}

    # ===== P3 F12b channels FIXED (S3 x {+/-} invariance core) =====
    a12b, bp12b, orc12b = a["F12b"], bp["F12b"], orc["F12b"]
    expect_fixed = (Q(-1, 49), Q(1, 49), Q(-3, 49))
    a_fix = _channels(a12b)
    bp_fix = (bp12b.kappa_c, bp12b.kappa_s, bp12b.kappa_int)
    orc_fix = (orc12b.kappa_c, orc12b.kappa_s, orc12b.kappa_int)
    p3 = {
        "pathA_channels_eq_expected_fixed": a_fix == expect_fixed,
        "pathBprime_channels_eq_expected_fixed": bp_fix == expect_fixed,
        "pathC_channels_eq_expected_fixed": orc_fix == expect_fixed,
        "fixed_eq_base": a_fix == base_ch,
        "A_eq_Bprime_eq_C": a_fix == bp_fix == orc_fix,
    }
    verdicts["P3_F12b_channels_fixed"] = {
        "pass": all(p3.values()),
        "F12b_channels": [fr(x) for x in a_fix],
        "base_channels": [fr(x) for x in base_ch],
        "detail": p3}

    # ===== P4 F12b K_G invariant =====
    p4 = {
        "pathA_KG_eq_base": a12b["K_G"] == base_kg,
        "pathA_KG_eq_m3_49": a12b["K_G"] == Q(-3, 49),
        "pathB_total_eq_m3_49": bt["F12b"] == Q(-3, 49),
        "pathBprime_sum_eq_m3_49": bp12b.K_G == Q(-3, 49),
        "pathC_KG_eq_m3_49": orc12b.K_G == Q(-3, 49),
        "q_prime_eq_14": a12b["q"] == Q(14),
    }
    verdicts["P4_F12b_KG_invariant"] = {
        "pass": all(p4.values()),
        "F12b_K_G": fr(a12b["K_G"]), "base_K_G": fr(base_kg), "detail": p4}

    # ===== P5 K7 not fired =====
    # (a) recharts are legitimate (orthogonal) frame changes; (b) K_G invariant
    #     under both. K7 fires iff a legitimate rechart is reported as a
    #     curvature error OR sigma_2 not held invariant under F12.
    R_ortho, R_det = rechart_is_orthogonal(_R)
    P_ortho, P_det = rechart_is_orthogonal(_P)
    f12a_kg_invariant = (a12a["K_G"] == base_kg == bt["F12a"] == bp12a.K_G == orc12a.K_G)
    f12b_kg_invariant = (a12b["K_G"] == base_kg == bt["F12b"] == bp12b.K_G == orc12b.K_G)
    # "reported as a curvature error" would mean K_G drifted from the base value
    # under a legitimate rechart -> that is exactly NOT invariant. So the K7
    # not-fired condition is: recharts orthogonal AND K_G invariant under both.
    f12a_rechart_legit = R_ortho and R_det == Q(1)          # genuine SO(3)
    f12b_rechart_legit = P_ortho and abs(P_det) == Q(1)     # signed permutation
    k7_trigger_a = (f12a_rechart_legit and not f12a_kg_invariant) or \
                   (f12b_rechart_legit and not f12b_kg_invariant)  # legit rechart -> curvature error
    k7_trigger_b = not (f12a_kg_invariant and f12b_kg_invariant)   # sigma_2 not invariant
    k7_fired = bool(k7_trigger_a or k7_trigger_b)
    p5 = {
        "F12a_rechart_orthogonal": R_ortho, "F12a_det_eq_plus1": R_det == Q(1),
        "F12b_rechart_orthogonal": P_ortho, "F12b_absdet_eq_1": abs(P_det) == Q(1),
        "F12a_KG_invariant": f12a_kg_invariant,
        "F12b_KG_invariant": f12b_kg_invariant,
        "K7_trigger_legit_rechart_as_error": k7_trigger_a,
        "K7_trigger_sigma2_not_invariant": k7_trigger_b,
        "K7_fired": k7_fired,
    }
    verdicts["P5_K7_not_fired"] = {"pass": (k7_fired is False),
                                   "K7_fired": k7_fired, "detail": p5}
    # record the rechart-legitimacy verdict (contrast row; no channels).
    _rec(records, fixture_id="F12a", role="contrast", path="A",
         frame="rechart-legitimacy probe (R in SO(3))",
         refusals=(),
         notes=("K7 not-fired: F12a R^T R == I, det R == +1 (legitimate SO(3) "
                "rechart), K_G held invariant -> NOT reported as a curvature error"))
    _rec(records, fixture_id="F12b", role="contrast", path="A",
         frame="rechart-legitimacy probe (signed permutation P)",
         refusals=(),
         notes=("K7 not-fired: F12b P^T P == I, |det P| == 1 (legitimate signed "
                "permutation), K_G held invariant -> NOT reported as a curvature error"))

    # ===== P6 frame-relativity contrast (R2) =====
    p6 = {
        "F12a_channels_move": _channels(a12a) != base_ch,
        "F12a_KG_fixed": a12a["K_G"] == base_kg,
        "F12b_channels_fixed": _channels(a12b) == base_ch,
        "F12b_KG_fixed": a12b["K_G"] == base_kg,
        "sum_intrinsic_both": (a12a["K_G"] == base_kg) and (a12b["K_G"] == base_kg),
    }
    verdicts["P6_frame_relativity_contrast_R2"] = {
        "pass": all(p6.values()),
        "note": ("R2: generic rotation MOVES the channel representative "
                 "(F12a) while the sum is intrinsic; the signed permutation "
                 "FIXES the channels (S3 x {+/-} at n=3); K_G invariant under both"),
        "detail": p6}

    # ===== P7 completeness OPEN + K-soft non-refuting FLAG =====
    # PARTIAL-by-design honesty. CL-c3c-ii recorded OPEN; K-soft a non-refuting
    # FLAG; CL-c7 proposed move == PARTIAL (not DEMONSTRATED). No in-scope
    # refuting witness is manufactured (that would reach into closing CL-c3c-ii).
    smr = prereg["status_move_rules"]
    cl_c3c_ii_open = (smr["CL-c3c-ii"]["status"] == "OPEN"
                      and smr["CL-c3c-ii"].get("no_move") is True)
    ksoft = smr["kills"]["K-soft"]
    ksoft_nonrefuting = (ksoft["non_refuting"] is True
                         and ksoft["type"] == "flag (non-refuting)")
    cl_c7_move = smr["CL-c7"]["on_pass"]["move_to"]
    cl_c7_not_demonstrated = (cl_c7_move == "PARTIAL"
                              and smr["CL-c7"]["on_pass"]["explicitly_not"] == "DEMONSTRATED")
    # the exact-Q near-miss of K-soft (recorded, not closed): F12a and F8-base
    # share sigma_2 (= K_G) and orientation but DIFFER in channels -- and they
    # ARE frame-related (by R in SO(3)). This is the converse of the open
    # K-soft question, NOT a closure of it.
    ksoft_nearmiss = {
        "same_sigma2": a12a["K_G"] == base_kg,
        "different_channels": _channels(a12a) != base_ch,
        "and_they_are_frame_related": True,  # by R in SO(3) (F12a is the rechart)
        "reading": ("identical sigma_2 + different channels arises precisely "
                    "under a frame change; whether a NON-frame-related pair with "
                    "identical {sigma_r}+orientation exists is the OPEN K-soft "
                    "question (CL-c3c-ii / L1) -- NOT decided here"),
    }
    p7 = {
        "CL_c3c_ii_recorded_OPEN": cl_c3c_ii_open,
        "K_soft_non_refuting_flag": ksoft_nonrefuting,
        "CL_c7_move_is_PARTIAL_not_DEMONSTRATED": cl_c7_not_demonstrated,
        "no_in_scope_refuting_witness_manufactured": True,
        "ksoft_nearmiss_recorded": ksoft_nearmiss["same_sigma2"] and ksoft_nearmiss["different_channels"],
    }
    verdicts["P7_completeness_OPEN_Ksoft_flag"] = {
        "pass": all(bool(v) for v in p7.values()),
        "CL_c3c_ii": "OPEN", "K_soft": "non-refuting FLAG (completeness unestablished)",
        "CL_c7_proposed_move": cl_c7_move,
        "ksoft_nearmiss": ksoft_nearmiss,
        "detail": p7}
    # record the K-soft FLAG (contrast row; non-refuting).
    _rec(records, fixture_id="F12a", role="contrast", path="A",
         frame="K-soft completeness FLAG (non-refuting)",
         refusals=(),
         notes=("K-soft (non-refuting FLAG): completeness OPEN (CL-c3c-ii, "
                "blocked on {sigma_r}-completeness / L1). near-miss recorded: "
                "F12a and F8-base share sigma_2=-3/49 + orientation but differ in "
                "channels AND are frame-related (R in SO(3)) -- the converse of "
                "the open K-soft question, not a closure. CL-c7 -> PARTIAL."),
         telemetry={"ksoft_nearmiss": {
             "same_sigma2": ksoft_nearmiss["same_sigma2"],
             "different_channels": ksoft_nearmiss["different_channels"]}})

    # ===== P8 F12 preconditions (P-frame + P-self-cert) =====
    frame_present = {}
    for fid in F12:
        frame_present[fid] = {
            "fixture_frame": bool(getattr(fx[fid], "frame", None)),
            "oracle_frame": bool(getattr(orc[fid], "frame", None)),
        }
    p_frame_ok = all(d["fixture_frame"] and d["oracle_frame"]
                     for d in frame_present.values())
    psc = _check_p_self_cert()
    verdicts["P8_F12_preconditions"] = {
        "pass": p_frame_ok and psc["ok"],
        "P_frame": {"ok": p_frame_ok, "detail": frame_present},
        "P_self_cert": psc}

    # ===== P9 F12 type gate (sqrt-q-leak) =====
    all_fraction = True
    type_detail = {}
    for fid in F12:
        vals = ([a[fid]["K_G"], a[fid]["kappa_c"], a[fid]["kappa_s"],
                 a[fid]["kappa_int"], a[fid]["q"], a[fid]["det_hb"]]
                + [bt[fid]]
                + [bp[fid].kappa_c, bp[fid].kappa_s, bp[fid].kappa_int, bp[fid].K_G])
        ok = all(isinstance(v, Fraction) for v in vals)
        type_detail[fid] = ok
        all_fraction = all_fraction and ok
    # a float operand offered at the F12 probe door -> TypeError
    float_refused = False
    try:
        bench_probe.read_off((13 / 5, -9 / 5, 2.0),
                             ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    except TypeError:
        float_refused = True
    except Exception:
        float_refused = False
    verdicts["P9_F12_type_gate_sqrt_q"] = {
        "pass": all_fraction and float_refused,
        "all_emitted_are_Fraction": all_fraction,
        "float_operand_raises_TypeError": float_refused,
        "detail": type_detail}

    return records, verdicts


def _check_p_self_cert() -> Dict[str, Any]:
    """P-self-cert: oracle (Path C) external to A/B/B'. Source-text scan: the
    oracle must not import probe/referee_total/referee_channel/fixtures, and the
    referees + probe must not import oracle."""
    def imports_any(mod_path: str, names: Tuple[str, ...]) -> List[str]:
        with open(mod_path, "r", encoding="utf-8") as fh:
            src = fh.read()
        hits = []
        for n in names:
            if (f"import {n}" in src) or (f" {n} import" in src) \
                    or (f".{n} import" in src) or (f"import {n}," in src):
                hits.append(n)
        return hits

    oracle_src = os.path.join(BENCH_DIR, "oracle.py")
    oracle_hits = imports_any(oracle_src, ("probe", "referee_total",
                                           "referee_channel", "fixtures"))
    reverse = {}
    for m in ("probe", "referee_total", "referee_channel"):
        reverse[m] = imports_any(os.path.join(BENCH_DIR, f"{m}.py"), ("oracle",))
    ok = (oracle_hits == []) and all(v == [] for v in reverse.values())
    return {"ok": ok, "oracle_imports_of_ABBprime_fixtures": oracle_hits,
            "ABBprime_imports_of_oracle": reverse}


def write_records(records: List[Dict[str, Any]], path: str) -> str:
    """Write records as a deterministic, sorted-keys, byte-stable jsonl; return
    its sha256. The records list is already in a fixed emission order; each line
    is canonical JSON (sort_keys, no NaN)."""
    lines = [json.dumps(r, sort_keys=True, ensure_ascii=True, allow_nan=False)
             for r in records]
    body = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    recs, verds = run()
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(STAGE, "records.jsonl")
    sha = write_records(recs, out)
    n_pass = sum(1 for v in verds.values() if v["pass"])
    print(f"records: {len(recs)} -> {out}")
    print(f"records_sha256: {sha}")
    print(f"predictions PASS: {n_pass}/{len(verds)}")
    for pid, v in verds.items():
        print(f"  {'PASS' if v['pass'] else 'FAIL'}  {pid}")
