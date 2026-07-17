"""c001 `three_channel_kg` — STAGE A battery (covenant step 2/3/4).

Implements the FROZEN `prereg.json` (pin `ecced952...`). It:

  * loads the frozen prereg and re-verifies its sha256 pin;
  * embeds every governing clause VERBATIM in `GRADER_CLAUSES` and
    string-compares each against the frozen prereg's `grader_clauses` at
    runtime -- ANY drift -> `ClauseDrift` REFUSAL (Rule 1.8 / covenant step 2);
  * re-verifies the bench module shas against the prereg `depends_on` (Rule
    1.9 content pins) -- ANY mismatch -> `PinDrift` REFUSAL;
  * imports the FROZEN bench READ-ONLY (probe Path A; referee_total Path B;
    referee_channel Path B'; oracle Path C; fixtures; schema) -- never edits it;
  * runs each of the 13 predictions exact-Q (no tolerance), emits one
    `three_channel_kg_record_v1` per evaluation step, and writes a
    deterministic, sorted-keys, byte-stable records jsonl;
  * grades mechanically into prediction verdicts.

Determinism: every value is a `fractions.Fraction` serialised as `frac:n/d`;
records are emitted in a fixed order with `json.dumps(..., sort_keys=True)`; no
float, no time, no randomness. Two runs MUST be byte-identical.

This is the stage-runner's grader. The CL-c1 universal warrant (R1) is
established by a genuine SYMBOLIC polynomial-identity argument over Q[g,H]
(P12) -- NOT by finite-fixture agreement alone -- using this module's own
exact-Q multivariate engine (it re-derives the probe's partition formulas,
transcribed from the frozen probe, and proves they equal the cofactor det).
The bench is imported read-only; nothing here mutates it.
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
# paths: ALL derived from this file's location (__file__) so the committed
# grader re-runs from wherever it lives -- in the originating worktree OR on
# `main` after merge. (Post-gate reproducibility retrofit: no ephemeral
# worktree path is baked in. Records content is path-independent, so this
# retrofit leaves the records sha256 unchanged.) STAGE is this file's
# directory; the repo root is three levels up (stage_a -> three_channel_kg ->
# results -> repo); the frozen bench sits under the repo's src/. The bench is
# loaded READ-ONLY by EXACT FILE PATH (shadow-proof: a src/lloyd_v4 that lacks
# this bench would make package-name resolution ambiguous; loading by the
# resolved file path is unambiguous and binds to exactly the files pinned in
# depends_on). The bench modules import only stdlib -- no inter-module / no
# lloyd_v4 package imports -- so direct file-path loading is sound and
# preserves the code-disjoint referee separation.
# --------------------------------------------------------------------------
STAGE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.dirname(STAGE)
REPO_ROOT = os.path.dirname(os.path.dirname(RESULTS))
BENCH_DIR = os.path.join(REPO_ROOT, "src/lloyd_v4/evals/three_channel_kg")
SRC_DIR = os.path.join(REPO_ROOT, "src")
PREREG_PATH = os.path.join(STAGE, "prereg.json")
PREREG_PIN_PATH = os.path.join(STAGE, "prereg_sha256.pin")


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
    "row_pass": (
        "got.(K_G,kappa_c,kappa_s,kappa_int)==expected "
        "AND got.K_G==sum(channels) "
        "AND got.K_G==PathB_total "
        "AND got.channels==PathBprime_channels "
        "AND det(H_b)==Delta_c+Delta_s+Delta_m"),
    "closure_1_tuple_eq_expected":
        "got.(K_G, kappa_c, kappa_s, kappa_int) == expected",
    "closure_2_K_G_eq_sum_channels":
        "got.K_G == sum(channels)  (kappa_c + kappa_s + kappa_int)",
    "closure_3_K_G_eq_pathB_total":
        "got.K_G == Path-B total  (-det(H_b)/q^2, sqrt-q-free)",
    "closure_4_channels_eq_pathBprime":
        "got.channels == Path-B' channels  (split shape-operator det2, code-disjoint)",
    "closure_5_det_hb_eq_partition_sum":
        "det(H_b) == Delta_c + Delta_s + Delta_m",
    "semantics_K_G": "kappa_c + kappa_s + kappa_int (exact in Q)",
    "semantics_kappa_X": (
        "-Delta_X / q^2, with det(H_b) = Delta_c + Delta_s + Delta_m "
        "(off-diagonal -> Delta_c, diagonal -> Delta_s, mixed -> Delta_m)"),
    "semantics_total_referee": "K_G == -det(H_b)/q^2 (Path B, sqrt-q-free)",
    "semantics_channel_referee":
        "channels == split-shape-operator det2 channels (Path B', disjoint source)",
    "type_gate_sqrt_q_leak":
        "a total/channel referee returning a radical/float instead of Fraction -> hard fail (K8).",
    "type_gate_tolerance_leak":
        "any injected mismatch that passes/warns instead of hard-failing -> fail (K9).",
    "type_gate_singular_lie":
        ("q=0 / cone-apex / g_i=0 returning 0/NaN/placeholder instead of typed "
         "REFUSED -> fail (refuse-not-lie, K11)."),
    "precondition_P_self_cert":
        "the oracle (Path C) must be external to A/B/B', or the run is void.",
    "precondition_P_frame":
        "every channel fixture must carry its frame annotation, or it is rejected.",
    "K2_partition": "det(H_b)-(Delta_c+Delta_s+Delta_m)!=0.",
    "K3_two_derivation":
        "Path-A channels != Path-B' channels (incl. kappa_s-mirror mutant).",
    "K5_wrong_sign":
        "bordered-Hessian sign flip inverts an expected sign (F3/F7/F8).",
    "K6_rank_heuristic": "nonzero on the developable cone F9.",
    "K8_sqrt_q_leak": "radical/float instead of Fraction -> hard fail (K8).",
    "K9_tolerance_leak":
        "any injected mismatch passing/warning instead of hard-fail -> fail (K9).",
    "K11_singular_lie":
        "q=0 / cone-apex / g_i=0 -> typed REFUSED, never 0/NaN/placeholder (K11).",
    "R1_proven_warrant":
        ("logic-forced, not discretionary. A verified finite exact-Q both-sign "
         "witness earns [PROVEN] for an impossibility / existence claim (CL-c3); "
         "universal claims (CL-c1, CL-c3b) require the symbolic identity over "
         "Q[g,H]. The stage prereg encodes this in status_move_rules."),
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


def _rec(stage_runner_records: List[Dict[str, Any]], *,
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
        stage="stage_a",
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
    stage_runner_records.append(json.loads(bench_schema.to_json(rec)))


# --------------------------------------------------------------------------
# the kappa_s-mirror MUTANT (battery-owned; NOT bench code) and a sign-flip
# mutant total. These are contrast paths the battery builds to exercise K3/K5.
# --------------------------------------------------------------------------
def _matmul(A, B):
    n = len(A)
    return [[sum((A[i][t] * B[t][j] for t in range(n)), Q(0)) for j in range(n)]
            for i in range(n)]


def _trace(A):
    return sum((A[i][i] for i in range(len(A))), Q(0))


def _det2_form(M):
    return (_trace(M) * _trace(M) - _trace(_matmul(M, M))) / 2


def mutant_kappa_s_mirror(g, H) -> Fraction:
    """A NAIVE kappa_s-mirror: det2 of the BARE self-part H_s (no tangent
    projector) over q. This mirrors the kappa_c det2 shape onto the raw
    diagonal block WITHOUT the P H_s P construction -- the wrong (mirror) form
    K3 must reject. Differs from the genuine split-shape kappa_s on the trap
    fixtures."""
    gg = [Q(x) for x in g]
    q = sum((x * x for x in gg), Q(0))
    if q == 0:
        raise bench_probe.ThreeChannelRefusal("q_zero")
    Hs = [[(Q(H[i][j]) if i == j else Q(0)) for j in range(3)] for i in range(3)]
    return _det2_form(Hs) / q


def mutant_total_sign_flip(g, H) -> Fraction:
    """Sign-flip mutant of the TOTAL: +det(H_b)/q^2 instead of -det(H_b)/q^2.
    Inverts the sign of K_G; K5 must catch it via an inverted expected sign."""
    return -bench_reft.referee_total(g, H)  # negate the true (correct-sign) total


# --------------------------------------------------------------------------
# the SYMBOLIC identity over Q[g,H] (P12): a genuine multivariate polynomial
# identity proof, NOT finite sampling. 9 indeterminates; exact-Q coefficients.
# This module RE-DERIVES the probe's partition formulas (transcribed from the
# frozen probe) and proves they equal the cofactor-expanded det(H_b).
# --------------------------------------------------------------------------
_VARS = ("g1", "g2", "g3", "h11", "h12", "h13", "h22", "h23", "h33")
_NI = 9
_Mono = Tuple[int, ...]
_Poly = Dict[_Mono, Fraction]


def _pvar(i: int) -> _Poly:
    e = [0] * _NI
    e[i] = 1
    return {tuple(e): Q(1)}


def _padd(*ps: _Poly) -> _Poly:
    out: _Poly = {}
    for p in ps:
        for m, c in p.items():
            out[m] = out.get(m, Q(0)) + c
    return {m: c for m, c in out.items() if c != 0}


def _pneg(p: _Poly) -> _Poly:
    return {m: -c for m, c in p.items()}


def _pmul(a: _Poly, b: _Poly) -> _Poly:
    out: _Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(ma[k] + mb[k] for k in range(_NI))
            out[m] = out.get(m, Q(0)) + ca * cb
    return {m: c for m, c in out.items() if c != 0}


def _psmul(p: _Poly, s: int) -> _Poly:
    s = Q(s)
    return {m: c * s for m, c in p.items() if c * s != 0}


def symbolic_identity_proof() -> Dict[str, Any]:
    """Prove det(H_b) == Delta_c + Delta_s + Delta_m as a polynomial identity
    in Q[g1..g3, h11..h33]. Returns the exact monomial counts, the residual
    polynomial's monomial count (must be 0), and the disjointness/exhaustiveness
    facts. Deterministic and complete (no sampling, no tolerance)."""
    g1, g2, g3 = _pvar(0), _pvar(1), _pvar(2)
    h11, h12, h13 = _pvar(3), _pvar(4), _pvar(5)
    h22, h23, h33 = _pvar(6), _pvar(7), _pvar(8)
    Z: _Poly = {}

    # symbolic bordered Hessian
    Hb = [[Z, g1, g2, g3],
          [g1, h11, h12, h13],
          [g2, h12, h22, h23],
          [g3, h13, h23, h33]]

    def det3(M):
        return _padd(
            _pmul(M[0][0], _padd(_pmul(M[1][1], M[2][2]), _pneg(_pmul(M[1][2], M[2][1])))),
            _pneg(_pmul(M[0][1], _padd(_pmul(M[1][0], M[2][2]), _pneg(_pmul(M[1][2], M[2][0]))))),
            _pmul(M[0][2], _padd(_pmul(M[1][0], M[2][1]), _pneg(_pmul(M[1][1], M[2][0])))))

    def det4(M):
        acc: _Poly = {}
        sign = 1
        for c in range(4):
            minor = [[M[r][cc] for cc in range(4) if cc != c] for r in range(1, 4)]
            term = _pmul(M[0][c], det3(minor))
            acc = _padd(acc, term if sign == 1 else _pneg(term))
            sign = -sign
        return acc

    det_sym = det4(Hb)

    # The probe's partition formulas, transcribed VERBATIM from probe.partition:
    delta_c = _padd(
        _pmul(_pmul(g1, g1), _pmul(h23, h23)),
        _pneg(_psmul(_pmul(_pmul(g1, g2), _pmul(h13, h23)), 2)),
        _pneg(_psmul(_pmul(_pmul(g1, g3), _pmul(h12, h23)), 2)),
        _pmul(_pmul(g2, g2), _pmul(h13, h13)),
        _pneg(_psmul(_pmul(_pmul(g2, g3), _pmul(h12, h13)), 2)),
        _pmul(_pmul(g3, g3), _pmul(h12, h12)))
    delta_s = _padd(
        _pneg(_pmul(_pmul(g1, g1), _pmul(h22, h33))),
        _pneg(_pmul(_pmul(g2, g2), _pmul(h11, h33))),
        _pneg(_pmul(_pmul(g3, g3), _pmul(h11, h22))))
    delta_m = _padd(
        _psmul(_pmul(_pmul(g1, g2), _pmul(h12, h33)), 2),
        _psmul(_pmul(_pmul(g1, g3), _pmul(h13, h22)), 2),
        _psmul(_pmul(_pmul(g2, g3), _pmul(h11, h23)), 2))

    partition = _padd(delta_c, delta_s, delta_m)
    residual = _padd(det_sym, _pneg(partition))

    sc, ss, sm = set(delta_c), set(delta_s), set(delta_m)
    sd = set(det_sym)
    disjoint = (sc & ss == set()) and (sc & sm == set()) and (ss & sm == set())
    union_eq = (sc | ss | sm) == sd

    return {
        "det_monomials": len(det_sym),
        "delta_c_monomials": len(delta_c),
        "delta_s_monomials": len(delta_s),
        "delta_m_monomials": len(delta_m),
        "partition_monomials": len(partition),
        "residual_monomials": len(residual),
        "identity_holds": len(residual) == 0,
        "supports_pairwise_disjoint": disjoint,
        "support_union_eq_det_support": union_eq,
        "indeterminates": list(_VARS),
    }


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
        # match `import ... n` / `from ... n import` token occurrences
        if (f"import {n}" in src) or (f" {n} import" in src) or (f".{n} import" in src) \
                or (f"import {n}," in src) or (f", {n}" in src and "import" in src):
            hits.append(n)
    return hits


def check_p_self_cert() -> Dict[str, Any]:
    """P-self-cert: oracle (Path C) external to A/B/B'. Check the oracle source
    does not import probe/referee_total/referee_channel/fixtures, and that the
    referees + probe do not import oracle."""
    oracle_src = os.path.join(BENCH_DIR, "oracle.py")
    forbidden_in_oracle = ("probe", "referee_total", "referee_channel", "fixtures")
    oracle_hits = _module_imports_any(oracle_src, forbidden_in_oracle)

    reverse = {}
    for m in ("probe", "referee_total", "referee_channel"):
        hits = _module_imports_any(os.path.join(BENCH_DIR, f"{m}.py"), ("oracle",))
        reverse[m] = hits

    ok = (oracle_hits == []) and all(v == [] for v in reverse.values())
    return {
        "ok": ok,
        "oracle_imports_of_ABBprime_fixtures": oracle_hits,
        "ABBprime_imports_of_oracle": reverse,
    }


def check_p_frame(fx: Dict[str, Any]) -> Dict[str, Any]:
    """P-frame: every in-scope channel fixture carries a non-empty frame."""
    missing = []
    for fid in ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11"):
        f = fx[fid]
        if not getattr(f, "frame", None):
            missing.append(fid)
    return {"ok": missing == [], "missing_frame": missing}


# --------------------------------------------------------------------------
# the run: produce records + grade predictions
# --------------------------------------------------------------------------
IN_SCOPE = ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11")
KAPPA_S_TRAP = ("F5", "F6", "F8")
WRONG_SIGN_SET = ("F3", "F7", "F8")
ACCOUNT = {"ledger": "stage_a", "covenant": "role=probe + account",
           "campaign": "three_channel_kg", "cycle": "c001"}


def run() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    prereg = load_prereg()
    gate_clauses(prereg)
    gate_bench_pins(prereg)

    # Stage-0 control: every frozen fixture reproduces exactly (raises on drift).
    fx = bench_fixtures.generate_and_check()

    records: List[Dict[str, Any]] = []
    verdicts: Dict[str, Any] = {}

    # ----- emit one record per fixture per path (A/B/Bprime/C) -----
    # exact-Q channel rows, all five closure identities computed and recorded.
    row_pass_count = 0
    row_pass_detail: Dict[str, Dict[str, bool]] = {}
    for fid in IN_SCOPE:
        f = fx[fid]
        a = bench_probe.read_off(f.g, f.H)
        bt = bench_reft.referee_total(f.g, f.H)
        bp = bench_refc.referee_channel(f.g, f.H)
        orc = bench_oracle.oracle(fid)

        exp = tuple(Q(s) for s in prereg["expectations"]["channel_fixtures"][fid])
        got_tuple = (a["K_G"], a["kappa_c"], a["kappa_s"], a["kappa_int"])
        c1 = got_tuple == exp
        c2 = a["K_G"] == a["kappa_c"] + a["kappa_s"] + a["kappa_int"]
        c3 = a["K_G"] == bt
        c4 = (a["kappa_c"], a["kappa_s"], a["kappa_int"]) == (bp.kappa_c, bp.kappa_s, bp.kappa_int)
        c5 = a["det_hb"] == a["Delta_c"] + a["Delta_s"] + a["Delta_m"]
        # Path C oracle agreement (external; part of c1 since exp==oracle, but
        # record the explicit oracle equality too).
        c_oracle = got_tuple == (orc.K_G, orc.kappa_c, orc.kappa_s, orc.kappa_int)
        row_ok = c1 and c2 and c3 and c4 and c5 and c_oracle
        if row_ok:
            row_pass_count += 1
        row_pass_detail[fid] = {
            "c1_tuple_eq_expected": c1, "c2_KG_eq_sum_channels": c2,
            "c3_KG_eq_pathB_total": c3, "c4_channels_eq_pathBprime": c4,
            "c5_det_eq_partition": c5, "c_oracle_eq": c_oracle, "row_pass": row_ok}

        # Path A probe record (role=probe; closure_ok gated -> carries account).
        _rec(records, fixture_id=fid, role="probe", path="A",
             point=({k: fr(v) for k, v in zip(("x1", "x2", "x3"), f.point)} if f.point else None),
             frame=f.frame,
             g=tuple(fr(x) for x in f.g),
             H=tuple(tuple(fr(x) for x in row) for row in f.H),
             q=fr(a["q"]),
             delta_c=fr(a["Delta_c"]), delta_s=fr(a["Delta_s"]),
             delta_m=fr(a["Delta_m"]), det_hb=fr(a["det_hb"]),
             kappa_c=fr(a["kappa_c"]), kappa_s=fr(a["kappa_s"]),
             kappa_int=fr(a["kappa_int"]), K_G=fr(a["K_G"]),
             account=ACCOUNT, closure_ok=row_ok,
             referee={"P1_row_pass": row_pass_detail[fid]},
             notes="Path A monomial read-off")
        # Path B total referee record.
        _rec(records, fixture_id=fid, role="referee_total", path="B",
             frame=f.frame, K_G=fr(bt),
             notes="Path B total -det(H_b)/q^2 (Bareiss)")
        # Path B' channel referee record.
        _rec(records, fixture_id=fid, role="referee_channel", path="Bprime",
             frame=f.frame,
             kappa_c=fr(bp.kappa_c), kappa_s=fr(bp.kappa_s),
             kappa_int=fr(bp.kappa_int), K_G=fr(bp.K_G),
             notes="Path B' split shape-operator channels")
        # Path C oracle record.
        _rec(records, fixture_id=fid, role="oracle", path="C",
             frame=orc.frame,
             kappa_c=fr(orc.kappa_c), kappa_s=fr(orc.kappa_s),
             kappa_int=fr(orc.kappa_int), K_G=fr(orc.K_G),
             notes="Path C frozen external oracle")

    # ===== P1 =====
    verdicts["P1_row_pass_all"] = {
        "pass": row_pass_count == len(IN_SCOPE),
        "rows_passing": row_pass_count, "rows_total": len(IN_SCOPE),
        "units": "rows passing all five closure identities out of 11",
        "detail": row_pass_detail,
    }

    # ===== P2 keystone F8 =====
    f8 = fx["F8"]
    a8 = bench_probe.read_off(f8.g, f8.H)
    bt8 = bench_reft.referee_total(f8.g, f8.H)
    bp8 = bench_refc.referee_channel(f8.g, f8.H)
    orc8 = bench_oracle.oracle("F8")
    ek = prereg["expectations"]["keystone_F8"]
    p2 = {
        "q_eq_14": a8["q"] == Q(14),
        "det_hb_eq_12": a8["det_hb"] == Q(12),
        "K_G_eq_m3_49": a8["K_G"] == Q(-3, 49),
        "kappa_c_eq_m1_49": a8["kappa_c"] == Q(-1, 49),
        "kappa_s_eq_1_49": a8["kappa_s"] == Q(1, 49),
        "kappa_int_eq_m3_49": a8["kappa_int"] == Q(-3, 49),
        "K_G_negative_signed": a8["K_G"] < 0,
        "K_G_eq_sum_channels": a8["K_G"] == a8["kappa_c"] + a8["kappa_s"] + a8["kappa_int"],
        "pathB_total_agrees": bt8 == Q(-3, 49),
        "pathBprime_tuple_agrees": (bp8.kappa_c, bp8.kappa_s, bp8.kappa_int, bp8.K_G)
                                   == (Q(-1, 49), Q(1, 49), Q(-3, 49), Q(-3, 49)),
        "pathC_oracle_agrees": (orc8.K_G, orc8.kappa_c, orc8.kappa_s, orc8.kappa_int)
                               == (Q(-3, 49), Q(-1, 49), Q(1, 49), Q(-3, 49)),
        "expected_anchor": ek,
    }
    verdicts["P2_keystone_F8"] = {"pass": all(v for k, v in p2.items()
                                              if isinstance(v, bool)),
                                  "detail": p2}

    # ===== P3 partition (K2) =====
    p3_detail = {}
    p3_ok = True
    for fid in IN_SCOPE:
        f = fx[fid]
        a = bench_probe.read_off(f.g, f.H)
        residual = a["det_hb"] - (a["Delta_c"] + a["Delta_s"] + a["Delta_m"])
        bt_det = bench_reft.bordered_det(f.g, f.H)  # Path B generic det
        d = {"residual_zero": residual == Q(0),
             "pathA_det_eq_pathB_det": a["det_hb"] == bt_det,
             "residual": fr(residual)}
        p3_detail[fid] = d
        p3_ok = p3_ok and d["residual_zero"] and d["pathA_det_eq_pathB_det"]
    verdicts["P3_partition_K2"] = {"pass": p3_ok, "K2_fires": not p3_ok,
                                   "detail": p3_detail}

    # ===== P4 two-derivation (K3) + kappa_s-mirror mutant =====
    p4_detail = {}
    p4_ok = True
    for fid in IN_SCOPE:
        f = fx[fid]
        a = bench_probe.read_off(f.g, f.H)
        bp = bench_refc.referee_channel(f.g, f.H)
        a_ch = (a["kappa_c"], a["kappa_s"], a["kappa_int"])
        bp_ch = (bp.kappa_c, bp.kappa_s, bp.kappa_int)
        agree = a_ch == bp_ch
        p4_detail[fid] = {"A_eq_Bprime": agree,
                          "A_channels": [fr(x) for x in a_ch],
                          "Bprime_channels": [fr(x) for x in bp_ch]}
        p4_ok = p4_ok and agree
    # mutant differs from truth on the trap set
    mutant_detail = {}
    mutant_distinguished = True
    for fid in KAPPA_S_TRAP:
        f = fx[fid]
        truth_ks = bench_refc.referee_channel(f.g, f.H).kappa_s
        mut_ks = mutant_kappa_s_mirror(f.g, f.H)
        differs = truth_ks != mut_ks
        mutant_detail[fid] = {"truth_kappa_s": fr(truth_ks),
                              "mirror_mutant_kappa_s": fr(mut_ks),
                              "differs_so_K3_would_fire": differs}
        mutant_distinguished = mutant_distinguished and differs
    verdicts["P4_two_derivation_K3"] = {
        "pass": p4_ok and mutant_distinguished,
        "A_eq_Bprime_all": p4_ok, "mirror_mutant_distinguished_on_trap": mutant_distinguished,
        "K3_fires_on_truth": not p4_ok, "detail": p4_detail, "mutant_detail": mutant_detail}
    # mutant contrast records (role=contrast)
    for fid in KAPPA_S_TRAP:
        f = fx[fid]
        _rec(records, fixture_id=fid, role="contrast", path="Bprime",
             frame=f.frame, kappa_s=fr(mutant_kappa_s_mirror(f.g, f.H)),
             notes="kappa_s-mirror MUTANT (no projector det2 H_s / q) -- K3 must reject")

    # ===== P5 wrong-sign (K5) =====
    p5_detail = {}
    p5_ok = True
    for fid in WRONG_SIGN_SET:
        f = fx[fid]
        orc = bench_oracle.oracle(fid)
        true_kg = bench_reft.referee_total(f.g, f.H)
        flip_kg = mutant_total_sign_flip(f.g, f.H)
        true_sign = (true_kg > 0) - (true_kg < 0)
        flip_sign = (flip_kg > 0) - (flip_kg < 0)
        oracle_sign = (orc.K_G > 0) - (orc.K_G < 0)
        d = {"true_K_G": fr(true_kg), "flip_K_G": fr(flip_kg),
             "true_sign_matches_oracle": true_sign == oracle_sign,
             "flip_inverts_sign": flip_sign == -true_sign and true_sign != 0,
             "oracle_K_G": fr(orc.K_G)}
        p5_detail[fid] = d
        p5_ok = p5_ok and d["true_sign_matches_oracle"] and d["flip_inverts_sign"]
        _rec(records, fixture_id=fid, role="contrast", path="B",
             frame=f.frame, K_G=fr(flip_kg),
             notes="sign-flip MUTANT (+det/q^2) -- K5 must catch inverted sign")
    verdicts["P5_wrong_sign_K5"] = {"pass": p5_ok, "K5_catches_flip": p5_ok,
                                    "detail": p5_detail}

    # ===== P6 rank-heuristic (K6) on F9 =====
    f9 = fx["F9"]
    a9 = bench_probe.read_off(f9.g, f9.H)
    bt9 = bench_reft.referee_total(f9.g, f9.H)
    bp9 = bench_refc.referee_channel(f9.g, f9.H)
    orc9 = bench_oracle.oracle("F9")
    p6 = {"pathA_KG_zero": a9["K_G"] == Q(0), "pathB_KG_zero": bt9 == Q(0),
          "pathBprime_KG_zero": bp9.K_G == Q(0), "pathC_KG_zero": orc9.K_G == Q(0),
          "never_nonzero": a9["K_G"] == Q(0) and bt9 == Q(0) and bp9.K_G == Q(0)}
    verdicts["P6_rank_heuristic_K6"] = {"pass": all(p6.values()),
                                        "K6_fires": not all(p6.values()), "detail": p6}

    # ===== P7 sqrt-q-leak (K8) =====
    all_fraction = True
    type_detail = {}
    for fid in IN_SCOPE:
        f = fx[fid]
        a = bench_probe.read_off(f.g, f.H)
        bt = bench_reft.referee_total(f.g, f.H)
        bp = bench_refc.referee_channel(f.g, f.H)
        vals = ([a["K_G"], a["kappa_c"], a["kappa_s"], a["kappa_int"], a["q"], a["det_hb"]]
                + [bt] + [bp.kappa_c, bp.kappa_s, bp.kappa_int, bp.K_G])
        ok = all(isinstance(v, Fraction) for v in vals)
        type_detail[fid] = ok
        all_fraction = all_fraction and ok
    # float at the door -> TypeError
    float_refused = False
    try:
        bench_probe.read_off((1.0, 1.0, 1.0),
                             ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    except TypeError:
        float_refused = True
    except Exception:
        float_refused = False
    verdicts["P7_sqrt_q_leak_K8"] = {
        "pass": all_fraction and float_refused,
        "all_emitted_are_Fraction": all_fraction,
        "float_operand_raises_TypeError": float_refused,
        "detail": type_detail}

    # ===== P8 tolerance-leak (K9) =====
    # inject +1/10^9 into the F8 expected K_G; the exact-equality row-pass MUST be False.
    eps = Q(1, 10 ** 9)
    f8 = fx["F8"]
    a8 = bench_probe.read_off(f8.g, f8.H)
    perturbed_expected = (a8["K_G"] + eps, a8["kappa_c"], a8["kappa_s"], a8["kappa_int"])
    got = (a8["K_G"], a8["kappa_c"], a8["kappa_s"], a8["kappa_int"])
    near_miss_rowpass = got == perturbed_expected  # must be False
    verdicts["P8_tolerance_leak_K9"] = {
        "pass": near_miss_rowpass is False,
        "injected_eps": fr(eps),
        "near_miss_rowpass_must_be_False": near_miss_rowpass,
        "note": "exact equality rejects a +1e-9 near-miss (no tolerance band)"}

    # ===== P9 singular-lie (K11) =====
    g0 = (Q(0), Q(0), Q(0))
    H0 = ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1)))
    refusals = {}
    # Path A
    try:
        bench_probe.read_off(g0, H0)
        refusals["pathA"] = {"refused": False, "kind": None}
    except bench_probe.ThreeChannelRefusal as e:
        refusals["pathA"] = {"refused": True, "kind": e.kind}
    # Path B
    try:
        bench_reft.referee_total(g0, H0)
        refusals["pathB"] = {"refused": False}
    except bench_reft.RefereeRefusal:
        refusals["pathB"] = {"refused": True}
    # Path B'
    try:
        bench_refc.referee_channel(g0, H0)
        refusals["pathBprime"] = {"refused": False}
    except bench_refc.RefereeRefusal:
        refusals["pathBprime"] = {"refused": True}
    # F6 single g_i=0 regular jet must NOT refuse and == 1
    f6 = fx["F6"]
    f6_refused = False
    f6_kg = None
    try:
        f6_kg = bench_probe.read_off(f6.g, f6.H)["K_G"]
    except bench_probe.ThreeChannelRefusal:
        f6_refused = True
    all_refused = (refusals["pathA"]["refused"] and refusals["pathB"]["refused"]
                   and refusals["pathBprime"]["refused"])
    f6_ok = (not f6_refused) and (f6_kg == Q(1))
    verdicts["P9_singular_lie_K11"] = {
        "pass": all_refused and f6_ok,
        "q0_all_paths_refused": all_refused,
        "q0_refusals": refusals,
        "F6_single_gi0_not_refused_and_KG_1": f6_ok,
        "F6_K_G": fr(f6_kg) if f6_kg is not None else None}
    # record the q=0 refusal (typed; no numeric value, only refusals tag)
    _rec(records, fixture_id="F9", role="contrast", path="A",
         frame="declared DBP frame (singular probe g=(0,0,0))",
         refusals=("singular_refused",),
         notes="K11 genuine q=0 (g=(0,0,0)) -> typed REFUSED on A/B/Bprime (no numeric)")

    # ===== P10 preconditions =====
    psc = check_p_self_cert()
    pfr = check_p_frame(fx)
    verdicts["P10_preconditions"] = {
        "pass": psc["ok"] and pfr["ok"],
        "P_self_cert": psc, "P_frame": pfr}

    # ===== P11 both-sign witnesses (CL-c1 signed) =====
    f6_kg = bench_probe.read_off(fx["F6"].g, fx["F6"].H)["K_G"]
    f8_kg = bench_probe.read_off(fx["F8"].g, fx["F8"].H)["K_G"]
    f10_ki = bench_probe.read_off(fx["F10"].g, fx["F10"].H)["kappa_int"]
    f11_ki = bench_probe.read_off(fx["F11"].g, fx["F11"].H)["kappa_int"]
    p11 = {"F6_KG_positive": f6_kg == Q(1) and f6_kg > 0,
           "F8_KG_negative": f8_kg == Q(-3, 49) and f8_kg < 0,
           "F10_kappa_int_negative": f10_ki == Q(-1, 9) and f10_ki < 0,
           "F11_kappa_int_positive": f11_ki == Q(2, 9) and f11_ki > 0}
    verdicts["P11_both_sign_witnesses_CLc1_signed"] = {
        "pass": all(p11.values()),
        "F6_KG": fr(f6_kg), "F8_KG": fr(f8_kg),
        "F10_kappa_int": fr(f10_ki), "F11_kappa_int": fr(f11_ki),
        "detail": p11}

    # ===== P12 symbolic identity over Q[g,H] (CL-c1 universal warrant, R1) =====
    sym = symbolic_identity_proof()
    p12_pass = (sym["identity_holds"] and sym["residual_monomials"] == 0
                and sym["det_monomials"] == 12 and sym["partition_monomials"] == 12
                and sym["supports_pairwise_disjoint"] is True
                and sym["support_union_eq_det_support"] is True)
    verdicts["P12_symbolic_identity_CLc1_universal"] = {"pass": p12_pass, "proof": sym}
    # record the symbolic-identity outcome (no jet; a meta-record on F8 keystone slot)
    _rec(records, fixture_id="F8", role="contrast", path="A",
         frame="symbolic Q[g,H] (no numeric jet)",
         notes=("P12 symbolic identity over Q[g,H]: det(H_b)-(Delta_c+Delta_s+Delta_m)=0 "
                f"(residual_monomials={sym['residual_monomials']}, det={sym['det_monomials']}, "
                f"partition={sym['partition_monomials']}, disjoint={sym['supports_pairwise_disjoint']})"),
         telemetry={"symbolic_proof": sym})

    # ===== P13 F13 parity contrast =====
    f13 = bench_fixtures.F13_NOTE
    orc_f13 = bench_oracle.F13
    sigma2_eq_f8 = orc_f13.sigma_2 == f8_kg  # == F8 K_G
    p13 = {"sigma_2_eq_m3_49": orc_f13.sigma_2 == Q(-3, 49),
           "sigma_2_eq_F8_KG": sigma2_eq_f8,
           "C1_hat_eq_m24": orc_f13.C1_hat == Q(-24),
           "sigma_1_field_label": f13["sigma_1_field"],
           "sigma_1_not_emitted_numerically": f13["sigma_1_field"] == "Q(sqrt14)"
                                              and not hasattr(orc_f13, "sigma_1")}
    verdicts["P13_F13_parity_contrast"] = {
        "pass": (p13["sigma_2_eq_m3_49"] and p13["sigma_2_eq_F8_KG"]
                 and p13["C1_hat_eq_m24"] and p13["sigma_1_not_emitted_numerically"]),
        "sigma_2": fr(orc_f13.sigma_2), "C1_hat": fr(orc_f13.C1_hat),
        "sigma_1_field": f13["sigma_1_field"], "detail": p13}
    _rec(records, fixture_id="F13", role="oracle", path="C",
         frame="declared DBP frame (keystone, rungs r=1,2)",
         notes=("F13 parity contrast: sigma_2=%s (==F8 K_G), C1_hat=%s, sigma_1 in %s "
                "(NOT emitted numerically)" % (fr(orc_f13.sigma_2), fr(orc_f13.C1_hat),
                                               f13["sigma_1_field"])),
         telemetry={"sigma_2": fr(orc_f13.sigma_2), "C1_hat": fr(orc_f13.C1_hat),
                    "sigma_1_field": f13["sigma_1_field"]})

    return records, verdicts


def write_records(records: List[Dict[str, Any]], path: str) -> str:
    """Write records as a deterministic, sorted-keys, byte-stable jsonl;
    return its sha256. The records list is already in a fixed emission order;
    each line is canonical JSON (sort_keys, no NaN)."""
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
