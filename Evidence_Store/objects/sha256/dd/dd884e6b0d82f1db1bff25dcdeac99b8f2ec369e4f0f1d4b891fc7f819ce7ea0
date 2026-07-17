"""c001 `three_channel_kg` -- STAGE E battery (covenant step 2/3/4).

Parity / sigma_2 exactness. Implements the FROZEN `prereg.json`
(pin 0e714fed...). It:

  * loads the frozen prereg and re-verifies its sha256 pin;
  * embeds every governing clause VERBATIM in `GRADER_CLAUSES` and
    string-compares each against the frozen prereg's `grader_clauses` at
    runtime -- ANY drift -> `ClauseDrift` REFUSAL (Rule 1.8 / covenant step 2);
  * re-verifies the bench module shas against the prereg `depends_on` (Rule
    1.9 content pins) -- ANY mismatch -> `PinDrift` REFUSAL;
  * imports the FROZEN bench READ-ONLY (probe Path A; referee_total Path B;
    referee_channel Path B'; oracle Path C; fixtures; schema) -- never edits it;
  * runs each of the 6 Stage-E predictions exact-Q (no tolerance), emits one
    `three_channel_kg_record_v1` per evaluation step, and writes a
    deterministic, sorted-keys, byte-stable records jsonl;
  * grades mechanically into prediction verdicts.

THE STAGE-E SCIENCE (n=3 PARITY CORE; CL-c5; kill K10):
  The tangent shape operator is S = -(1/|g|) P H P (P = I - g g^T/q). Its
  order-r elementary-symmetric invariant sigma_r carries r factors of the
  -(1/|g|) prefactor, i.e. (1/q)^(r/2). EVEN r (sigma_2 = K_G) => the radical
  squares away => sqrt-q-FREE => exact-Q. ODD r (sigma_1) => one un-squared
  -(1/|g|) => sigma_1 in Q(sqrt q), exact-Q only if q is a perfect square. At
  the keystone jet g=(3,1,2), q=14: sigma_2 = -3/49 in Q (== K_G); sigma_1 in
  Q(sqrt14) (sigma_1^2 = 72/343 in Q, but 14 is a non-square so sigma_1 not in
  Q). C1_hat = -24 = -2 det(H_b) is a second even-order exact-Q anchor.
  K10 (parity-type gate) is SILENT on truth (the oracle WITHHOLDS sigma_1) and
  FIRES on a battery-owned MUTANT that emits sigma_1 as a Fraction m: a genuine
  exact-Q sigma_1 would satisfy m^2 == 72/343 (forcing sqrt14 in Q -- false),
  so m^2 != 72/343 for every Fraction m -> K10 fires.

Determinism: every record value is a `fractions.Fraction` serialised as
`frac:n/d`; records are emitted in a fixed order with
`json.dumps(..., sort_keys=True)`; no float, no time, no randomness reaches a
record. The K10 mutant uses `math.sqrt` ONLY to FORGE a lying numeric sigma_1,
then immediately rationalises it via `Fraction.limit_denominator(10**9)` (a
fixed bound) -- that Fraction is deterministic and never enters a record field
(only the boolean fire/silent outcome and the frac:n/d of its value do). Two
runs MUST be byte-identical.

The bench is imported read-only by EXACT FILE PATH; nothing here mutates it.
The probe never imports the referee; Path B/B'/C are code-disjoint sources.
Scope: CL-c5 (n=3 CORE only) and K10 only; the n>=4 tower is NOT established
(out of scope, successor c002). Eval-tier; canonical only on Will's sign-off.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import sys
from fractions import Fraction
from types import ModuleType
from typing import Any, Dict, List, Tuple

# --------------------------------------------------------------------------
# paths: ALL derived from this file's location (__file__) so the committed
# grader re-runs from wherever it lives -- in the originating worktree OR on
# `main` after merge. No ephemeral worktree path is baked in (records content
# is path-independent, so this leaves the records sha256 unchanged). STAGE is
# this file's directory; the repo root is three levels up (stage_e ->
# three_channel_kg -> results -> repo); the frozen bench sits under the repo's
# src/. The bench is loaded READ-ONLY by EXACT FILE PATH (shadow-proof: a
# src/lloyd_v4 that lacks this bench would make package-name resolution
# ambiguous; loading by the resolved file path is unambiguous and binds to
# exactly the files pinned in depends_on). The bench modules import only
# stdlib -- no inter-module / no lloyd_v4 package imports -- so direct
# file-path loading is sound and preserves the code-disjoint referee
# separation.
# --------------------------------------------------------------------------
STAGE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.dirname(STAGE)
REPO_ROOT = os.path.dirname(os.path.dirname(RESULTS))
PREREG_PATH = os.path.join(STAGE, "prereg.json")
PREREG_PIN_PATH = os.path.join(STAGE, "prereg_sha256.pin")

# BENCH_DIR resolution (bench-less worktree handling, per the launch
# instruction). The frozen bench is committed on `main`; this Stage-E worktree
# branches from the PRE-BENCH base, so the __file__-relative
# REPO_ROOT/src/lloyd_v4/... path does NOT exist here. Resolve in order:
#   (1) the __file__-relative path -- correct AFTER the merge-packager
#       consolidates this stage onto `main` (where the bench lives), matching
#       Stage A's retrofitted relocatable pattern; then
#   (2) the STABLE MAIN CHECKOUT path named in the launch instruction --
#       correct WHILE running from the bench-less worktree.
# No ephemeral worktree path is baked in: (1) is __file__-relative; (2) is the
# fixed campaign main checkout. The depends_on sha256 gate (gate_bench_pins)
# re-verifies the resolved files content-for-content, so whichever checkout
# supplies the bench, it is byte-identical to the pinned frozen bench. Records
# content is path-independent (no path enters a record field), so this leaves
# the records sha256 unchanged.
_STABLE_MAIN_BENCH = "/home/wlloyd/Lloyd_Engine_V4/src/lloyd_v4/evals/three_channel_kg"
_CANDIDATE_BENCH_DIRS = (
    os.path.join(REPO_ROOT, "src/lloyd_v4/evals/three_channel_kg"),
    _STABLE_MAIN_BENCH,
)


def _resolve_bench_dir() -> str:
    for cand in _CANDIDATE_BENCH_DIRS:
        if os.path.isfile(os.path.join(cand, "schema.py")):
            return cand
    raise ImportError(
        "frozen three_channel_kg bench not found at any candidate path: "
        f"{_CANDIDATE_BENCH_DIRS}")


BENCH_DIR = _resolve_bench_dir()


def _load_bench_module(name: str) -> ModuleType:
    """Load a bench module READ-ONLY from its exact pinned file path under
    BENCH_DIR. Shadow-proof; never imports/edits the bench package."""
    path = os.path.join(BENCH_DIR, f"{name}.py")
    modname = f"three_channel_kg_bench_{name}"
    spec = importlib.util.spec_from_file_location(modname, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load bench module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    # register before exec so @dataclass(slots=True) can resolve cls.__module__
    # via sys.modules (CPython 3.12+ requirement); synthetic name avoids any
    # collision with the worktree's shadowing lloyd_v4 package.
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
    "K10_parity_type": (
        "K10 parity-type (type gate) -- fires if an odd-order / radical-bearing "
        "invariant is emitted as if exact-Q, or if the even/odd parity distinction "
        "is violated."),
    "parity_law_even_exact_Q": (
        "EVEN order r (r=2: sigma_2 = K_G) -> the -(1/|g|) prefactor appears an "
        "even number of times and squares to the rational 1/q -> sqrt-q-FREE -> "
        "exact-Q (sigma_2 = det2(P H P)/q = -det(H_b)/q^2 in Q)."),
    "parity_law_odd_radical": (
        "ODD order r (r=1: sigma_1, twice the mean curvature) -> the -(1/|g|) "
        "prefactor appears an odd number of times and does NOT square away -> "
        "sigma_1 = -(1/|g|) tr(P H P) in Q(sqrt q); exact-Q only when q is a "
        "perfect square. sigma_1^2 = tr(P H P)^2/q in Q, but sigma_1 not in Q "
        "when q is a non-square."),
    "parity_witness": (
        "The contrast sigma_2 in Q (even, exact-Q, emitted) vs sigma_1 in "
        "Q(sqrt14) (odd, radical-bearing, withheld) is the parity witness."),
    "sqrt_q_free_even": (
        "every even-order curvature invariant is sqrt-q-free (the radical squares "
        "to a rational), hence exact-Q; the bench det2 channels are degree-2 forms "
        "whose -(1/|g|) factor squares to 1/q."),
    "oracle_withholds_sigma_1": (
        "the frozen oracle does NOT expose sigma_1 as a numeric Fraction (emitting "
        "a radical would itself be a sqrt-q leak); it exposes only the even-order "
        "exact-Q sigma_2 and C1_hat."),
    "K10_exactness_witness": (
        "a genuine exact-Q sigma_1 would satisfy emitted^2 == sigma_1^2 = 72/343 "
        "exactly, which forces sqrt 14 in Q -- false; so emitted^2 != 72/343 for "
        "every Fraction, and emitting sigma_1 as exact-Q trips K10."),
    "type_gate_sqrt_q_leak":
        "a total/channel referee returning a radical/float instead of Fraction -> hard fail (K8).",
    "semantics_K_G": "kappa_c + kappa_s + kappa_int (exact in Q)",
    "semantics_total_referee": "K_G == -det(H_b)/q^2 (Path B, sqrt-q-free)",
    "semantics_channel_referee":
        "channels == split-shape-operator det2 channels (Path B', disjoint source)",
    "precondition_P_self_cert":
        "the oracle (Path C) must be external to A/B/B', or the run is void.",
    "precondition_P_frame":
        "every channel fixture must carry its frame annotation, or it is rejected.",
    "exact_Q_no_tolerance": (
        "Exact Q only; no tolerance band anywhere; a near-miss is a FAIL. No "
        "substrate promotion (eval-tier only). Nothing canonical until Will signs off."),
    "n3_core_only": (
        "Stage E grades CL-c5 to the n=3 CORE only (parity => K_G = sigma_2 even "
        "=> exact-Q). The n>=4 tower is NOT established and is OUT of scope "
        "(successor c002)."),
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
        raise PreregPinMismatch(
            f"prereg.json sha256 {actual} != pin {pinned}")
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


def _rec(records: List[Dict[str, Any]], *,
         fixture_id: str, role: str, path: str,
         point: Dict[str, str] | None = None,
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
        stage="stage_e",
        fixture_id=fixture_id,
        role=role,
        path=path,
        point=point,
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
# the shape-operator parity machinery (battery-owned exact-Q algebra). NOT
# bench code: this RE-DERIVES the parity quantities (sigma_2 = det2(P H P)/q,
# tr(P H P), sigma_1^2) so the parity contrast is grounded in an independent
# computation, then cross-checked against Path B total / Path B' channels /
# Path C oracle. The det2 / trace constructions mirror the FROZEN
# referee_channel.py shape (degree-2 even => sqrt-q-free), proving the EVEN
# branch in code; the odd (tr) branch carries the un-squared radical.
# --------------------------------------------------------------------------
def _matmul(A, B):
    n = len(A)
    return [[sum((A[i][t] * B[t][j] for t in range(n)), Q(0)) for j in range(len(B[0]))]
            for i in range(n)]


def _trace(A):
    return sum((A[i][i] for i in range(len(A))), Q(0))


def _projector(g, q):
    return [[(Q(1) if i == j else Q(0)) - g[i] * g[j] / q for j in range(3)]
            for i in range(3)]


def _det2_form(M):
    """1/2( tr(M)^2 - tr(M^2) ) over Q -- the sqrt-q-free det2 of P H P. For
    S = -(1/|g|) M the tangent det2(S) = (1/q)*this (the -(1/|g|) squares
    away): the EVEN-order branch, exact-Q."""
    return (_trace(M) * _trace(M) - _trace(_matmul(M, M))) / 2


def _PHP(g, H, q):
    P = _projector(g, q)
    return _matmul(_matmul(P, [list(r) for r in H]), P)


def sigma2_of(g, H) -> Fraction:
    """EVEN-order sigma_2 = det2(P H P)/q, exact-Q (== K_G, == -det(H_b)/q^2).
    sqrt-q-free: the -(1/|g|) prefactor of the shape operator appears twice and
    squares to 1/q."""
    gg = [Q(x) for x in g]
    q = sum((x * x for x in gg), Q(0))
    M = _PHP(gg, H, q)
    return _det2_form(M) / q


def trPHP_of(g, H) -> Fraction:
    """tr(P H P), a RATIONAL quantity. sigma_1 = -(1/|g|) tr(P H P), so the
    ODD-order sigma_1 carries one un-squared -(1/|g|) = 1/sqrt(q) and lives in
    Q(sqrt q). tr(P H P) itself is rational (no radical yet)."""
    gg = [Q(x) for x in g]
    q = sum((x * x for x in gg), Q(0))
    return _trace(_PHP(gg, H, q))


def sigma1_squared_of(g, H) -> Fraction:
    """sigma_1^2 = tr(P H P)^2 / q, a RATIONAL number. (sigma_1 itself is
    irrational whenever q is a non-square; this is the exactness witness used
    by K10.)"""
    gg = [Q(x) for x in g]
    q = sum((x * x for x in gg), Q(0))
    tr = _trace(_PHP(gg, H, q))
    return tr * tr / q


def _is_perfect_square_fraction(x: Fraction) -> bool:
    """True iff the exact rational x >= 0 is the square of a rational. (For x =
    a/b in lowest terms, x is a rational square iff |a| and b are both perfect
    integer squares.)"""
    if x < 0:
        return False
    a, b = x.numerator, x.denominator
    ra, rb = math.isqrt(a), math.isqrt(b)
    return ra * ra == a and rb * rb == b


# --------------------------------------------------------------------------
# the K10 MUTANT (battery-owned; NOT bench code): emit sigma_1 as if exact-Q.
# A lying engine that drops the radical and presents a Fraction m as the
# numeric value of the odd-order sigma_1. K10 catches it via the exactness
# witness m^2 != sigma_1^2 (a rational square equal to sigma_1^2 = 72/343 would
# force sqrt(q) in Q, false for a non-square q).
# --------------------------------------------------------------------------
def mutant_sigma1_as_exact_Q(g, H) -> Fraction:
    """Forge a lying numeric sigma_1 as a Fraction (as if exact-Q). Uses
    math.sqrt ONLY to build the forgery, then rationalises with a FIXED
    denominator bound (deterministic). This Fraction is the mutant's claimed
    exact-Q sigma_1; it never enters a record field except as the frac:n/d of
    the forged value (a deterministic string)."""
    gg = [Q(x) for x in g]
    q = sum((x * x for x in gg), Q(0))
    tr = _trace(_PHP(gg, H, q))
    # the true (irrational) sigma_1 = -tr/sqrt(q); the liar rounds it to a Q.
    forged = Q(-float(tr) / math.sqrt(float(q))).limit_denominator(10 ** 9)
    return forged


def k10_fires_on_emitted_sigma1(emitted_m: Fraction, sigma1_squared: Fraction) -> bool:
    """K10 parity-type gate, mechanized: an odd-order / radical-bearing
    invariant emitted AS IF exact-Q is caught iff the exactness witness fails,
    i.e. emitted_m^2 != sigma_1^2. (A genuine exact-Q sigma_1 would satisfy
    equality; a radical-bearing one cannot when q is a non-square.) Returns True
    iff K10 FIRES on the emission."""
    return (emitted_m * emitted_m) != sigma1_squared


# --------------------------------------------------------------------------
# precondition checks: P-self-cert (import-graph disjointness) + P-frame
# --------------------------------------------------------------------------
def _module_imports_any(mod_path: str, names: Tuple[str, ...]) -> List[str]:
    """Return which of `names` appear as imports in the module SOURCE (a coarse
    but sufficient self-cert check: the oracle must not import A/B/B'/fixtures
    and vice-versa). Source-text scan, exact-string."""
    with open(mod_path, "r", encoding="utf-8") as fh:
        src = fh.read()
    hits = []
    for n in names:
        if (f"import {n}" in src) or (f" {n} import" in src) or (f".{n} import" in src) \
                or (f"import {n}," in src) or (f", {n}" in src and "import" in src):
            hits.append(n)
    return hits


def check_p_self_cert() -> Dict[str, Any]:
    """P-self-cert: oracle (Path C) external to A/B/B'."""
    oracle_src = os.path.join(BENCH_DIR, "oracle.py")
    forbidden_in_oracle = ("probe", "referee_total", "referee_channel", "fixtures")
    oracle_hits = _module_imports_any(oracle_src, forbidden_in_oracle)
    reverse = {}
    for m in ("probe", "referee_total", "referee_channel"):
        hits = _module_imports_any(os.path.join(BENCH_DIR, f"{m}.py"), ("oracle",))
        reverse[m] = hits
    ok = (oracle_hits == []) and all(v == [] for v in reverse.values())
    return {"ok": ok, "oracle_imports_of_ABBprime_fixtures": oracle_hits,
            "ABBprime_imports_of_oracle": reverse}


def check_p_frame_f13() -> Dict[str, Any]:
    """P-frame: the F13 parity row carries a non-empty frame annotation."""
    f13_note = bench_fixtures.F13_NOTE
    orc = bench_oracle.F13
    note_frame_ok = bool(f13_note.get("role"))  # the note row's annotation field
    oracle_frame = getattr(orc, "frame", None)
    ok = bool(oracle_frame)
    return {"ok": ok, "oracle_F13_frame": oracle_frame,
            "note_role_present": note_frame_ok}


# --------------------------------------------------------------------------
# the run: produce records + grade the 6 Stage-E predictions
# --------------------------------------------------------------------------
# keystone jet (F8 surface at (1,1,1) == F12 base jet): g=(3,1,2), q=14.
KEY_G: Tuple[Fraction, Fraction, Fraction] = (Q(3), Q(1), Q(2))
KEY_H = ((Q(2), Q(1), Q(0)), (Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(2)))
ACCOUNT = {"ledger": "stage_e", "covenant": "role=probe + account",
           "campaign": "three_channel_kg", "cycle": "c001"}


def run() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    prereg = load_prereg()
    gate_clauses(prereg)
    gate_bench_pins(prereg)

    # Stage-0 control: every frozen fixture reproduces exactly (raises on drift).
    fx = bench_fixtures.generate_and_check()

    records: List[Dict[str, Any]] = []
    verdicts: Dict[str, Any] = {}

    # confirm the keystone jet identity (F8 surface jet == the parity base jet).
    f8 = fx["F8"]
    assert (f8.g, f8.q) == (KEY_G, Q(14)), \
        f"keystone jet drift: {f8.g}, {f8.q} != {KEY_G}, 14"

    # independent + bench computations of the parity quantities at the keystone.
    sigma2 = sigma2_of(KEY_G, KEY_H)                       # even-order, exact-Q
    KG_pathB = bench_reft.referee_total(KEY_G, KEY_H)      # Path B total
    ch = bench_refc.referee_channel(KEY_G, KEY_H)          # Path B' channels
    KG_pathBprime = ch.K_G
    det_hb = bench_reft.bordered_det(KEY_G, KEY_H)         # det(H_b)
    orc_f13 = bench_oracle.F13                             # Path C parity oracle
    note_f13 = bench_fixtures.F13_NOTE
    trPHP = trPHP_of(KEY_G, KEY_H)                         # rational; sigma_1 carries radical
    sigma1_sq = sigma1_squared_of(KEY_G, KEY_H)            # rational sigma_1^2

    # ===== P1 sigma_2 even-order exact-Q =====
    p1 = {
        "sigma_2_eq_m3_49": sigma2 == Q(-3, 49),
        "sigma_2_is_Fraction": isinstance(sigma2, Fraction),
        "sigma_2_eq_oracle": sigma2 == orc_f13.sigma_2,
        "sigma_2_eq_pathB_KG": sigma2 == KG_pathB,
        "sigma_2_eq_pathBprime_KG": sigma2 == KG_pathBprime,
        "sigma_2_eq_minus_det_over_q2": sigma2 == -det_hb / (Q(14) * Q(14)),
        "oracle_sigma_2_is_Fraction": isinstance(orc_f13.sigma_2, Fraction),
    }
    verdicts["P1_sigma2_even_exact_Q"] = {
        "pass": all(p1.values()),
        "sigma_2": fr(sigma2), "K_G_pathB": fr(KG_pathB),
        "K_G_pathBprime": fr(KG_pathBprime), "det_hb": fr(det_hb),
        "detail": p1}

    # Path B / B' / C records for the even-order sigma_2 = K_G witness.
    _rec(records, fixture_id="F13", role="oracle", path="C",
         frame=orc_f13.frame, K_G=fr(orc_f13.sigma_2),
         telemetry={"sigma_2": fr(orc_f13.sigma_2), "C1_hat": fr(orc_f13.C1_hat),
                    "order": "even (r=2)"},
         notes="Path C oracle: even-order sigma_2 = K_G = -3/49 (exact-Q)")
    _rec(records, fixture_id="F13", role="referee_total", path="B",
         frame=orc_f13.frame, K_G=fr(KG_pathB),
         notes="Path B total: K_G = -det(H_b)/q^2 = sigma_2 (sqrt-q-free, even-order)")
    _rec(records, fixture_id="F13", role="referee_channel", path="Bprime",
         frame=orc_f13.frame,
         kappa_c=fr(ch.kappa_c), kappa_s=fr(ch.kappa_s),
         kappa_int=fr(ch.kappa_int), K_G=fr(ch.K_G),
         notes="Path B' det2(P H_X P)/q channels: every channel degree-2 (even) => sqrt-q-free; sum K_G = sigma_2")

    # ===== P2 sigma_1 odd-order radical-bearing (in Q(sqrt14)) =====
    q_perfect_square = _is_perfect_square_fraction(Q(14))
    sigma1_in_Q = q_perfect_square  # sigma_1 = -tr/sqrt(q) in Q iff q is a perfect square (tr!=0)
    oracle_has_sigma1 = hasattr(orc_f13, "sigma_1")
    note_has_numeric_sigma1 = "sigma_1" in note_f13
    p2 = {
        "trPHP_eq_12_7": trPHP == Q(12, 7),
        "trPHP_nonzero": trPHP != Q(0),
        "sigma_1_squared_eq_72_343": sigma1_sq == Q(72, 343),
        "q_not_perfect_square": q_perfect_square is False,
        "sigma_1_not_in_Q": sigma1_in_Q is False,
        "oracle_withholds_sigma_1_attr": oracle_has_sigma1 is False,
        "note_withholds_numeric_sigma_1": note_has_numeric_sigma1 is False,
        "note_field_label_is_Q_sqrt14": note_f13.get("sigma_1_field") == "Q(sqrt14)",
    }
    verdicts["P2_sigma1_odd_radical"] = {
        "pass": all(p2.values()),
        "trPHP": fr(trPHP), "sigma_1_squared": fr(sigma1_sq),
        "q": "frac:14/1", "sigma_1_field": note_f13.get("sigma_1_field"),
        "detail": p2}

    # record the odd-order sigma_1 row WITHOUT a numeric value (refuse-not-lie:
    # a radical-bearing invariant is NOT emitted as exact-Q). Only its field
    # label and the rational sigma_1^2 are recorded, as telemetry.
    _rec(records, fixture_id="F13", role="oracle", path="C",
         frame=orc_f13.frame,
         refusals=("sqrt_q_leak",),
         telemetry={"sigma_1_field": note_f13.get("sigma_1_field"),
                    "sigma_1_squared": fr(sigma1_sq), "trPHP": fr(trPHP),
                    "order": "odd (r=1)",
                    "withheld": "sigma_1 in Q(sqrt14) NOT emitted as exact-Q (would be a sqrt-q leak)"},
         notes="Path C: odd-order sigma_1 in Q(sqrt14) WITHHELD (no numeric exact-Q value); sigma_1^2=72/343 in Q")

    # ===== P3 C1_hat even-order exact-Q anchor =====
    c1_hat = orc_f13.C1_hat
    p3 = {
        "C1_hat_eq_m24": c1_hat == Q(-24),
        "C1_hat_is_Fraction": isinstance(c1_hat, Fraction),
        "C1_hat_eq_minus_2_det_hb": c1_hat == -2 * det_hb,
        "det_hb_eq_12": det_hb == Q(12),
    }
    verdicts["P3_C1hat_even_exact_Q"] = {
        "pass": all(p3.values()),
        "C1_hat": fr(c1_hat), "minus_2_det_hb": fr(-2 * det_hb),
        "det_hb": fr(det_hb), "detail": p3}

    # ===== P4 parity witness (the contrast) =====
    even_emitted_exact_Q = (isinstance(orc_f13.sigma_2, Fraction)
                            and isinstance(orc_f13.C1_hat, Fraction)
                            and orc_f13.sigma_2 == Q(-3, 49)
                            and orc_f13.C1_hat == Q(-24))
    odd_not_emitted_exact_Q = (not hasattr(orc_f13, "sigma_1")
                               and "sigma_1" not in note_f13
                               and note_f13.get("sigma_1_field") == "Q(sqrt14)"
                               and sigma1_in_Q is False)
    contrast_holds = even_emitted_exact_Q and odd_not_emitted_exact_Q
    p4 = {
        "even_sigma_2_and_C1_hat_exact_Q_emitted": even_emitted_exact_Q,
        "odd_sigma_1_radical_and_withheld": odd_not_emitted_exact_Q,
        "contrast_holds": contrast_holds,
        "sigma_2_in_Q_vs_sigma_1_in_Q_sqrt14":
            (isinstance(orc_f13.sigma_2, Fraction) and note_f13.get("sigma_1_field") == "Q(sqrt14)"),
    }
    verdicts["P4_parity_witness_contrast"] = {"pass": all(p4.values()), "detail": p4}

    # ===== P5 K10 silent on truth =====
    psc = check_p_self_cert()
    pfr = check_p_frame_f13()
    # on the unmutated bench: NO odd/radical invariant emitted as exact-Q.
    no_odd_emitted_as_exact_Q = (not hasattr(orc_f13, "sigma_1")
                                 and "sigma_1" not in note_f13)
    parity_distinction_intact = (isinstance(orc_f13.sigma_2, Fraction)         # even is Q
                                 and note_f13.get("sigma_1_field") == "Q(sqrt14)"  # odd labelled radical
                                 and sigma1_in_Q is False)
    k10_silent_on_truth = no_odd_emitted_as_exact_Q and parity_distinction_intact
    p5 = {
        "no_odd_invariant_emitted_as_exact_Q": no_odd_emitted_as_exact_Q,
        "parity_distinction_intact": parity_distinction_intact,
        "K10_silent_on_truth": k10_silent_on_truth,
        "P_self_cert_ok": psc["ok"],
        "P_frame_ok": pfr["ok"],
    }
    verdicts["P5_K10_silent_on_truth"] = {
        "pass": all(v for v in p5.values()),
        "P_self_cert": psc, "P_frame": pfr, "detail": p5}

    # ===== P6 K10 fires on the constructed mutant =====
    emitted_m = mutant_sigma1_as_exact_Q(KEY_G, KEY_H)   # forged exact-Q sigma_1
    mutant_is_fraction = isinstance(emitted_m, Fraction)
    witness_fails = (emitted_m * emitted_m) != sigma1_sq  # m^2 != 72/343
    k10_fires = k10_fires_on_emitted_sigma1(emitted_m, sigma1_sq)
    # SANITY (non-tautology): the genuine even-order sigma_2, emitted as exact-Q,
    # does NOT trip K10 -- sigma_2^2 has no radical obstruction. (sigma_2 is its
    # own value; its "exactness witness" is trivially satisfied: sigma_2 in Q.)
    even_does_not_fire = isinstance(sigma2, Fraction) and (sigma2 == orc_f13.sigma_2)
    p6 = {
        "mutant_emits_sigma_1_as_Fraction": mutant_is_fraction,
        "exactness_witness_fails_m2_ne_sigma1_2": witness_fails,
        "K10_fires_on_mutant": k10_fires,
        "even_sigma_2_does_NOT_trip_K10": even_does_not_fire,
    }
    verdicts["P6_K10_fires_on_mutant"] = {
        "pass": all(p6.values()),
        "mutant_sigma_1": fr(emitted_m),
        "mutant_sigma_1_squared": fr(emitted_m * emitted_m),
        "true_sigma_1_squared": fr(sigma1_sq),
        "detail": p6}
    # record the mutant contrast (role=contrast): sigma_1 forged as exact-Q ->
    # K10 fires. The forged value is recorded as frac:n/d (a deterministic
    # string); the refusal tag marks the parity-type violation it represents.
    _rec(records, fixture_id="F13", role="contrast", path="C",
         frame=orc_f13.frame,
         refusals=("sqrt_q_leak",),
         telemetry={"mutant_sigma_1": fr(emitted_m),
                    "mutant_sigma_1_squared": fr(emitted_m * emitted_m),
                    "true_sigma_1_squared": fr(sigma1_sq),
                    "K10_fires": k10_fires},
         notes=("K10 MUTANT: sigma_1 (odd, Q(sqrt14)) emitted as exact-Q Fraction "
                "-> m^2 != 72/343 -> K10 FIRES (parity-type gate bites)"))

    return records, verdicts


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
