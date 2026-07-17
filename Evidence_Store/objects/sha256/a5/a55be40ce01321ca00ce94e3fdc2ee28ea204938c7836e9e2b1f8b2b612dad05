"""c001 `three_channel_kg` — STAGE C battery (covenant step 2/3/4).

Implements the FROZEN `prereg.json` (pin re-verified at load). It:

  * loads the frozen prereg and re-verifies its sha256 pin;
  * embeds every governing clause VERBATIM in `GRADER_CLAUSES` and string-
    compares each against the frozen prereg's `grader_clauses` at runtime --
    ANY drift -> `ClauseDrift` REFUSAL (Rule 1.8 / covenant step 2);
  * re-verifies the bench module shas against the prereg `depends_on` (Rule
    1.9 content pins) -- ANY mismatch -> `PinDrift` REFUSAL;
  * imports the FROZEN bench READ-ONLY by EXACT FILE PATH from the stable
    `main` checkout (the worktree is bench-less) -- never edits it;
  * builds the SINGLE-EDGE GAUGE (border shear H -> H + t(g e_i^T + e_i g^T),
    g unchanged) on the keystone F8 base jet and runs each of the 9 predictions
    exact-Q (no tolerance), emitting one `three_channel_kg_record_v1` per
    evaluation step and writing a deterministic, sorted-keys, byte-stable
    records jsonl;
  * grades mechanically into prediction verdicts.

Determinism: every value is a `fractions.Fraction` serialised as `frac:n/d`;
records are emitted in a fixed order with `json.dumps(..., sort_keys=True)`; no
float, no time, no randomness. Two runs MUST be byte-identical.

The R2 universal warrant: the single-edge law AND the K_G/sigma_r gauge-
invariance are established by genuine SYMBOLIC polynomial-identity arguments
over Q (indeterminates g1..g3, h11..h33, t) -- NOT by finite-keystone agreement
alone -- using this module's own exact-Q multivariate engine. The bench is
imported read-only; nothing here mutates it.

PATHS are all derived from this file's location (__file__) so the committed
grader re-runs from wherever it lives -- in the originating worktree OR on
`main` after merge. The frozen+committed bench sits at the stable main path
(the worktree is bench-less), loaded READ-ONLY by EXACT FILE PATH (shadow-proof;
the bench modules import only stdlib).
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

STAGE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.dirname(STAGE)
# The frozen+committed bench lives on `main` (the worktree branches from the
# pre-bench base). Load it READ-ONLY by exact file path from the stable main
# checkout. Records content is path-independent, so this leaves the records
# sha256 unchanged regardless of where the grader runs.
MAIN_REPO = "/home/wlloyd/Lloyd_Engine_V4"
BENCH_DIR = os.path.join(MAIN_REPO, "src/lloyd_v4/evals/three_channel_kg")
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
    "CL_c4_ledger":
        "gauge preserves every `σ_r`; `δC∈ker Σ`; single-edge "
        "`δκ_c(t·e_i)=4t·∏g·H_{jk}/q²`",
    "K4_gauge_single_edge":
        "K4 gauge / single-edge (refute) — `σ_r` changes under gauge, "
        "or `δC∉ker Σ`, or single-edge law fails (e₁/e₂ "
        "fail to pin, e₃ fails to move).",
    "R2_supplied_frame":
        "Channels are frame-relative in the supplied DBP frame; only the sum "
        "K_G is intrinsic (merged spec stance; connection-not-metric reading "
        "concurs). CL-c7 graded accordingly.",
    "gauge_definition_single_edge":
        "single-edge gauge: g unchanged; H -> H + t*(g e_i^T + e_i g^T) "
        "(border shear along basis direction e_i, i in {1,2,3}, t in Q).",
    "single_edge_law_symbolic":
        "delta kappa_c(t e_i) = 4 t (prod g) H_jk / q^2 as a symbolic identity "
        "over Q in (t, g, H), {j,k} the index pair complementary to i; "
        "equivalently delta Delta_c(t e_i) = -4 t (prod g) H_jk.",
    "sigma_r_preserved_under_gauge":
        "the gauge fixes the tangent shape operator P H P exactly (P g = 0 => "
        "P(g e_i^T + e_i g^T)P = 0), so every shape invariant sigma_r is "
        "preserved: sigma_2 = det = K_G (in Q) and sigma_1 = tr(PHP)/|g| (in "
        "Q(sqrt q), tracked sqrt-q-free via the rational handle tr(PHP)).",
    "deltaC_in_ker_Sigma":
        "delta C = (delta kappa_c, delta kappa_s, delta kappa_int) in "
        "ker Sigma, Sigma: Q^3 -> Q, Sigma(a,b,c) = a+b+c; i.e. delta K_G = 0 "
        "(the sum is unchanged under the gauge).",
    "keystone_F8_single_edge":
        "keystone F8 (g=(3,1,2), H=[[2,1,0],[1,0,0],[0,0,2]], q=14, prod g=6, "
        "q^2=196): e1 pins (complement {2,3}, H_23=0 => delta kappa_c=0); e2 "
        "pins (complement {1,3}, H_13=0 => delta kappa_c=0); e3 moves "
        "(complement {1,2}, H_12=1 => delta kappa_c = 4*6*1/196 = 6/49 per "
        "unit t).",
    "gauge_KG_invariant_all_paths":
        "K_G under the gauged jet equals the base K_G on Path A, Path B (total "
        "referee), and Path B' (channel referee); exact Q.",
    "two_derivation_under_gauge":
        "Path-A channels == Path-B' channels under the gauged jet (the split "
        "shape-operator agreement persists for the moved channel decomposition).",
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
    "semantics_K_G": "kappa_c + kappa_s + kappa_int (exact in Q)",
    "semantics_kappa_X": (
        "-Delta_X / q^2, with det(H_b) = Delta_c + Delta_s + Delta_m "
        "(off-diagonal -> Delta_c, diagonal -> Delta_s, mixed -> Delta_m)"),
    "semantics_total_referee": "K_G == -det(H_b)/q^2 (Path B, sqrt-q-free)",
    "semantics_channel_referee":
        "channels == split-shape-operator det2 channels (Path B', disjoint source)",
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
        stage="stage_c",
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
# the SINGLE-EDGE GAUGE (numeric, exact Q): g unchanged; H -> H + t(g e_i^T +
# e_i g^T). i is 0-indexed here.
# --------------------------------------------------------------------------
def gauge_jet(g: Tuple[Fraction, ...], H: List[List[Fraction]], i: int,
              t: Fraction) -> Tuple[Tuple[Fraction, ...], List[List[Fraction]]]:
    """Apply the single-edge border shear along e_i (0-indexed). Returns the
    gauged (g, H_gauged) -- g is UNCHANGED."""
    Hn = [[H[a][c] + t * (g[a] * (Q(1) if c == i else Q(0))
                          + (Q(1) if a == i else Q(0)) * g[c])
           for c in range(3)] for a in range(3)]
    return g, Hn


# tangent-plane projector P = I - g g^T / q (exact Q; q != 0). Used ONLY by the
# battery to compute the shape-operator invariants sigma_r (sqrt-q-free
# rational handles). Code-disjoint from the bench (the battery owns it).
def _projector(g, q):
    return [[(Q(1) if i == j else Q(0)) - g[i] * g[j] / q for j in range(3)]
            for i in range(3)]


def _matmul(A, B):
    n = len(A)
    return [[sum((A[i][t] * B[t][j] for t in range(n)), Q(0)) for j in range(n)]
            for i in range(n)]


def _trace(A):
    return sum((A[i][i] for i in range(len(A))), Q(0))


def shape_invariants(g, H):
    """Return (tr_PHP, sigma_2) in exact Q. tr_PHP is the rational handle for
    sigma_1 (= tr_PHP/|g| in Q(sqrt q)); sigma_2 = det = K_G. sqrt-q-free."""
    q = sum((x * x for x in g), Q(0))
    P = _projector(g, q)
    PHP = _matmul(_matmul(P, H), P)
    tr1 = _trace(PHP)
    tr2 = _trace(_matmul(PHP, PHP))
    sigma2 = (tr1 * tr1 - tr2) / 2 / q
    return tr1, sigma2


# --------------------------------------------------------------------------
# the SYMBOLIC engine over Q (multivariate polynomials in g1..g3,h11..h33,t).
# Mirrors Stage A's exact-Q engine. Used to establish the single-edge law and
# K_G/sigma_r gauge-invariance as SYMBOLIC IDENTITIES over Q (R2 warrant), not
# finite-keystone agreement.
# --------------------------------------------------------------------------
# indeterminate order: g1 g2 g3 h11 h12 h13 h22 h23 h33 t  (10 indeterminates)
_VARS = ("g1", "g2", "g3", "h11", "h12", "h13", "h22", "h23", "h33", "t")
_NI = 10
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
    sq = Q(s)
    return {m: c * sq for m, c in p.items() if c * sq != 0}


def _sym_handles():
    """Return the symbolic (g, H, t) plus a symmetric symbolic H matrix."""
    g1, g2, g3 = _pvar(0), _pvar(1), _pvar(2)
    h11, h12, h13 = _pvar(3), _pvar(4), _pvar(5)
    h22, h23, h33 = _pvar(6), _pvar(7), _pvar(8)
    t = _pvar(9)
    g = [g1, g2, g3]
    H = [[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]]
    return g, H, t


def _sym_delta_c(g, H) -> _Poly:
    """The probe's Delta_c formula, transcribed VERBATIM from
    probe.partition, evaluated symbolically on (g, H)."""
    g1, g2, g3 = g
    h12, h13, h23 = H[0][1], H[0][2], H[1][2]
    return _padd(
        _pmul(_pmul(g1, g1), _pmul(h23, h23)),
        _pneg(_psmul(_pmul(_pmul(g1, g2), _pmul(h13, h23)), 2)),
        _pneg(_psmul(_pmul(_pmul(g1, g3), _pmul(h12, h23)), 2)),
        _pmul(_pmul(g2, g2), _pmul(h13, h13)),
        _pneg(_psmul(_pmul(_pmul(g2, g3), _pmul(h12, h13)), 2)),
        _pmul(_pmul(g3, g3), _pmul(h12, h12)))


def _sym_det_bordered(g, H) -> _Poly:
    """Cofactor-expanded det of the bordered Hessian [[0,g^T],[g,H]],
    symbolically over Q[g,H,t]."""
    Z: _Poly = {}
    Hb = [[Z, g[0], g[1], g[2]],
          [g[0], H[0][0], H[0][1], H[0][2]],
          [g[1], H[1][0], H[1][1], H[1][2]],
          [g[2], H[2][0], H[2][1], H[2][2]]]

    def det3(M):
        return _padd(
            _pmul(M[0][0], _padd(_pmul(M[1][1], M[2][2]), _pneg(_pmul(M[1][2], M[2][1])))),
            _pneg(_pmul(M[0][1], _padd(_pmul(M[1][0], M[2][2]), _pneg(_pmul(M[1][2], M[2][0]))))),
            _pmul(M[0][2], _padd(_pmul(M[1][0], M[2][1]), _pneg(_pmul(M[1][1], M[2][0])))))

    acc: _Poly = {}
    sign = 1
    for c in range(4):
        minor = [[Hb[r][cc] for cc in range(4) if cc != c] for r in range(1, 4)]
        term = _pmul(Hb[0][c], det3(minor))
        acc = _padd(acc, term if sign == 1 else _pneg(term))
        sign = -sign
    return acc


def _sym_gauge_H(g, H, i, t):
    """Symbolic gauged H: H -> H + t(g e_i^T + e_i g^T), i 0-indexed."""
    Hn = []
    for a in range(3):
        row = []
        for c in range(3):
            term = H[a][c]
            if c == i:
                term = _padd(term, _pmul(t, g[a]))
            if a == i:
                term = _padd(term, _pmul(t, g[c]))
            row.append(term)
        Hn.append(row)
    return Hn


def symbolic_single_edge_law_proof() -> Dict[str, Any]:
    """Prove, for each edge i in {1,2,3}, that
        delta Delta_c(t e_i) - (-4 t (prod g) H_jk) == 0
    as a polynomial in Q[g,H,t], where Delta_c is the probe's formula, the
    gauge is the border shear, and {j,k} is the complement of i. (With
    kappa_c = -Delta_c/q^2 this is the single-edge law.) Deterministic and
    complete (no sampling)."""
    g, H, t = _sym_handles()
    prodg = _pmul(_pmul(g[0], g[1]), g[2])
    comp = {0: (1, 2), 1: (0, 2), 2: (0, 1)}  # i -> complement (0-indexed)
    base_dc = _sym_delta_c(g, H)
    out: Dict[str, Any] = {}
    all_zero = True
    for i in range(3):
        Hn = _sym_gauge_H(g, H, i, t)
        gauged_dc = _sym_delta_c(g, Hn)
        delta_dc = _padd(gauged_dc, _pneg(base_dc))           # delta Delta_c
        j, k = comp[i]
        Hjk = H[j][k]
        law = _pneg(_psmul(_pmul(prodg, Hjk), 4))             # -4 (prod g) H_jk
        law_t = _pmul(t, law)                                 # times t
        residual = _padd(delta_dc, _pneg(law_t))
        out[f"e{i+1}"] = {
            "complement_pair_1indexed": [j + 1, k + 1],
            "delta_Delta_c_monomials": len(delta_dc),
            "law_monomials": len(law_t),
            "residual_monomials": len(residual),
            "identity_holds": len(residual) == 0,
        }
        all_zero = all_zero and (len(residual) == 0)
    out["all_edges_identity_holds"] = all_zero
    out["indeterminates"] = list(_VARS)
    return out


def symbolic_KG_invariance_proof() -> Dict[str, Any]:
    """Prove, for each edge i, that det(H_b at the gauged jet) - det(H_b at the
    base jet) == 0 as a polynomial in Q[g,H,t] (cofactor-expanded bordered
    determinant). With K_G = -det/q^2 and q unchanged, K_G (=sigma_2) is
    gauge-invariant for EVERY regular jet. ALSO prove the stronger fact that the
    gauge generator is annihilated by the projector: q^2*(P H' P - P H P) is the
    ZERO matrix symbolically (this gives EVERY sigma_r, not only sigma_2)."""
    g, H, t = _sym_handles()
    base_det = _sym_det_bordered(g, H)
    q = _padd(_pmul(g[0], g[0]), _pmul(g[1], g[1]), _pmul(g[2], g[2]))
    q2 = _pmul(q, q)

    out: Dict[str, Any] = {}
    all_det_zero = True
    all_php_zero = True
    for i in range(3):
        Hn = _sym_gauge_H(g, H, i, t)
        gauged_det = _sym_det_bordered(g, Hn)
        det_residual = _padd(gauged_det, _pneg(base_det))

        # q^2-cleared PHP residual: q^2*P M P with P = I - g g^T/q, i.e.
        # (q I - g g^T) M (q I - g g^T) for M in {Hn, H}, then difference.
        # The difference is q^2*(P H' P - P H P); we prove it is the zero matrix.
        php_resid = _php_residual_qcleared(g, q, H, Hn)
        nonzero_entries = sum(1 for r in php_resid for e in r if len(e) > 0)

        out[f"e{i+1}"] = {
            "det_residual_monomials": len(det_residual),
            "det_invariance_holds": len(det_residual) == 0,
            "PHP_qcleared_nonzero_entries": nonzero_entries,
            "PHP_unchanged_symbolically": nonzero_entries == 0,
        }
        all_det_zero = all_det_zero and (len(det_residual) == 0)
        all_php_zero = all_php_zero and (nonzero_entries == 0)
    out["all_edges_det_invariance_holds"] = all_det_zero
    out["all_edges_PHP_unchanged"] = all_php_zero
    out["indeterminates"] = list(_VARS)
    return out


def _php_residual_qcleared(g, q, H, Hn):
    """Return q^2*(P H' P - P H P) as a 3x3 matrix of polynomials, where
    P = I - g g^T/q. We compute (qI - g g^T) M (qI - g g^T) for M = Hn and M = H
    (this is q^2 * P M P, since q*P = qI - g g^T), and difference. Must be the
    zero matrix (the gauge generator g e_i^T + e_i g^T is annihilated by P)."""
    # B = q I - g g^T  (so B = q*P, B M B = q^2 P M P).
    def Bmat():
        return [[_padd(_pmul(q, _pvar_one(a, c)), _pneg(_pmul(g[a], g[c])))
                 for c in range(3)] for a in range(3)]

    B = Bmat()

    def matmul(A, C):
        return [[_padd(*[_pmul(A[a][k], C[k][cc]) for k in range(3)])
                 for cc in range(3)] for a in range(3)]

    BHnB = matmul(matmul(B, Hn), B)
    BHB = matmul(matmul(B, H), B)
    return [[_padd(BHnB[a][c], _pneg(BHB[a][c])) for c in range(3)]
            for a in range(3)]


def _pvar_one(a: int, c: int) -> _Poly:
    """Symbolic identity-matrix entry (a==c -> 1, else 0)."""
    return {tuple([0] * _NI): Q(1)} if a == c else {}


# --------------------------------------------------------------------------
# precondition checks: P-self-cert (import-graph disjointness) + P-frame
# --------------------------------------------------------------------------
def _module_imports_any(mod_path: str, names: Tuple[str, ...]) -> List[str]:
    with open(mod_path, "r", encoding="utf-8") as fh:
        src = fh.read()
    hits = []
    for n in names:
        if (f"import {n}" in src) or (f" {n} import" in src) or (f".{n} import" in src) \
                or (f"import {n}," in src) or (f", {n}" in src and "import" in src):
            hits.append(n)
    return hits


def check_p_self_cert() -> Dict[str, Any]:
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


# --------------------------------------------------------------------------
# the run: produce records + grade predictions
# --------------------------------------------------------------------------
EDGES = (0, 1, 2)                         # 0-indexed e1, e2, e3
COMP = {0: (1, 2), 1: (0, 2), 2: (0, 1)}  # i -> complement pair (0-indexed)
WITNESS_T = (Q(1), Q(2), Q(3), Q(-4), Q(1, 2))
FRAME_BASE = "declared DBP frame"
ACCOUNT = {"ledger": "stage_c", "covenant": "role=probe + account",
           "campaign": "three_channel_kg", "cycle": "c001"}


def run() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    prereg = load_prereg()
    gate_clauses(prereg)
    gate_bench_pins(prereg)

    # Stage-0 control: every frozen fixture reproduces exactly (raises on drift).
    fx = bench_fixtures.generate_and_check()

    records: List[Dict[str, Any]] = []
    verdicts: Dict[str, Any] = {}

    # ---- the keystone F8 base jet (from the frozen fixtures) ----
    f8 = fx["F8"]
    g0 = tuple(f8.g)
    H0 = [list(row) for row in f8.H]
    base = bench_probe.read_off(g0, H0)
    base_bt = bench_reft.referee_total(g0, H0)
    base_bp = bench_refc.referee_channel(g0, H0)
    orc8 = bench_oracle.oracle("F8")
    prodg = g0[0] * g0[1] * g0[2]
    q0 = base["q"]
    q02 = q0 * q0
    base_tr1, base_sigma2 = shape_invariants(g0, H0)
    base_C = (base["kappa_c"], base["kappa_s"], base["kappa_int"])

    # ===== PC1 keystone base jet =====
    pc1 = {
        "q_eq_14": q0 == Q(14),
        "prod_g_eq_6": prodg == Q(6),
        "q_squared_eq_196": q02 == Q(196),
        "K_G_eq_m3_49": base["K_G"] == Q(-3, 49),
        "kappa_c_eq_m1_49": base["kappa_c"] == Q(-1, 49),
        "kappa_s_eq_1_49": base["kappa_s"] == Q(1, 49),
        "kappa_int_eq_m3_49": base["kappa_int"] == Q(-3, 49),
        "pathB_total_agrees": base_bt == Q(-3, 49),
        "pathBprime_tuple_agrees": (base_bp.kappa_c, base_bp.kappa_s,
                                    base_bp.kappa_int, base_bp.K_G)
                                   == (Q(-1, 49), Q(1, 49), Q(-3, 49), Q(-3, 49)),
        "pathC_oracle_agrees": (orc8.K_G, orc8.kappa_c, orc8.kappa_s, orc8.kappa_int)
                               == (Q(-3, 49), Q(-1, 49), Q(1, 49), Q(-3, 49)),
        "tr_PHP_eq_12_7": base_tr1 == Q(12, 7),
        "sigma_2_eq_K_G": base_sigma2 == base["K_G"],
    }
    verdicts["PC1_keystone_base_jet"] = {
        "pass": all(pc1.values()), "detail": pc1,
        "base_tuple": [fr(base["K_G"]), fr(base["kappa_c"]),
                       fr(base["kappa_s"]), fr(base["kappa_int"])],
        "tr_PHP": fr(base_tr1), "prod_g": fr(prodg), "q": fr(q0), "q_squared": fr(q02)}
    # base-jet record (Path A, role=probe + account; closure_ok gated).
    _rec(records, fixture_id="F8", role="probe", path="A",
         point={k: fr(v) for k, v in zip(("x1", "x2", "x3"), g0)} if f8.point else None,
         frame=FRAME_BASE,
         g=tuple(fr(x) for x in g0),
         H=tuple(tuple(fr(x) for x in row) for row in H0),
         q=fr(q0),
         delta_c=fr(base["Delta_c"]), delta_s=fr(base["Delta_s"]),
         delta_m=fr(base["Delta_m"]), det_hb=fr(base["det_hb"]),
         kappa_c=fr(base["kappa_c"]), kappa_s=fr(base["kappa_s"]),
         kappa_int=fr(base["kappa_int"]), K_G=fr(base["K_G"]),
         account=ACCOUNT, closure_ok=all(pc1.values()),
         telemetry={"tr_PHP": fr(base_tr1), "prod_g": fr(prodg), "q_squared": fr(q02)},
         notes="keystone F8 base jet (Stage C anchor)")

    # ===== sweep the gauge: build all gauged read-offs once, reuse downstream ==
    # gauged[(i,t)] = {'A':read_off, 'bt':K_G, 'bp':Channels, 'tr1','sigma2'}
    gauged: Dict[Tuple[int, str], Dict[str, Any]] = {}
    for i in EDGES:
        for t in WITNESS_T:
            g, Hn = gauge_jet(g0, H0, i, t)
            a = bench_probe.read_off(g, Hn)
            bt = bench_reft.referee_total(g, Hn)
            bp = bench_refc.referee_channel(g, Hn)
            tr1, sig2 = shape_invariants(g, Hn)
            gauged[(i, fr(t))] = {"g": g, "H": Hn, "A": a, "bt": bt, "bp": bp,
                                  "tr1": tr1, "sigma2": sig2, "t": t}

    # ===== PC2 single-edge law at the keystone =====
    pc2_detail: Dict[str, Any] = {}
    pc2_ok = True
    for i in EDGES:
        j, k = COMP[i]
        Hjk = H0[j][k]
        per_unit = 4 * Q(1) * prodg * Hjk / q02
        edge_rows = {"complement_pair_1indexed": [j + 1, k + 1],
                     "H_jk": fr(Hjk),
                     "delta_kappa_c_per_unit_t": fr(per_unit),
                     "disposition": "PINS" if Hjk == 0 else "MOVES",
                     "per_t": {}}
        for t in WITNESS_T:
            law = 4 * t * prodg * Hjk / q02
            a = gauged[(i, fr(t))]["A"]
            dkc = a["kappa_c"] - base["kappa_c"]
            match = dkc == law
            edge_rows["per_t"][fr(t)] = {"law": fr(law), "delta_kappa_c": fr(dkc),
                                         "match": match}
            pc2_ok = pc2_ok and match
            # the pin/move disposition must hold per the keystone H_jk
            if Hjk == 0 and dkc != 0:
                pc2_ok = False
        # the per-unit-t pin/move anchor
        if i == 0:  # e1 pins
            pc2_ok = pc2_ok and (per_unit == Q(0))
        if i == 1:  # e2 pins
            pc2_ok = pc2_ok and (per_unit == Q(0))
        if i == 2:  # e3 moves 6/49
            pc2_ok = pc2_ok and (per_unit == Q(6, 49))
        pc2_detail[f"e{i+1}"] = edge_rows
    verdicts["PC2_single_edge_law_keystone"] = {"pass": pc2_ok, "detail": pc2_detail}

    # ===== PC3 every sigma_r preserved under the gauge =====
    pc3_detail: Dict[str, Any] = {}
    pc3_ok = True
    for i in EDGES:
        per_t = {}
        for t in WITNESS_T:
            gg = gauged[(i, fr(t))]
            tr1_inv = gg["tr1"] == base_tr1
            sig2_inv = gg["sigma2"] == base_sigma2
            kg_a_inv = gg["A"]["K_G"] == base["K_G"]
            kg_b_inv = gg["bt"] == base_bt
            kg_bp_inv = gg["bp"].K_G == base_bp.K_G
            q_inv = gg["A"]["q"] == q0
            ok = tr1_inv and sig2_inv and kg_a_inv and kg_b_inv and kg_bp_inv and q_inv
            per_t[fr(t)] = {"tr_PHP_invariant": tr1_inv, "sigma2_invariant": sig2_inv,
                            "K_G_invariant_A": kg_a_inv, "K_G_invariant_B": kg_b_inv,
                            "K_G_invariant_Bprime": kg_bp_inv, "q_invariant": q_inv,
                            "all_sigma_r_preserved": ok}
            pc3_ok = pc3_ok and ok
        pc3_detail[f"e{i+1}"] = per_t
    verdicts["PC3_sigma_r_preserved_keystone"] = {
        "pass": pc3_ok, "base_tr_PHP": fr(base_tr1), "base_sigma2": fr(base_sigma2),
        "detail": pc3_detail}

    # ===== PC4 delta C in ker Sigma =====
    pc4_detail: Dict[str, Any] = {}
    pc4_ok = True
    for i in EDGES:
        per_t = {}
        for t in WITNESS_T:
            gg = gauged[(i, fr(t))]
            a = gg["A"]
            C = (a["kappa_c"], a["kappa_s"], a["kappa_int"])
            dC = (C[0] - base_C[0], C[1] - base_C[1], C[2] - base_C[2])
            sigma_dC = dC[0] + dC[1] + dC[2]
            in_ker = sigma_dC == Q(0)
            # Path-A channels == Path-B' channels under the gauge.
            ab = C == (gg["bp"].kappa_c, gg["bp"].kappa_s, gg["bp"].kappa_int)
            # genuine move on e3 (nonzero dC vector at t!=0); pins on e1/e2.
            moved = any(x != 0 for x in dC)
            per_t[fr(t)] = {"Sigma_deltaC": fr(sigma_dC), "in_ker_Sigma": in_ker,
                            "deltaC": [fr(x) for x in dC], "A_eq_Bprime": ab,
                            "deltaC_nonzero": moved}
            pc4_ok = pc4_ok and in_ker and ab
        pc4_detail[f"e{i+1}"] = per_t
    # "pins"/"moves" are about the single-edge-law channel delta kappa_c (the
    # coupling channel the law delta kappa_c(t e_i) governs), NOT the whole
    # channel vector: on e1/e2 delta kappa_c == 0 (kappa_c pins) while kappa_s
    # and kappa_int individually trade within ker Sigma (Sigma(delta C)=0). The
    # frozen prereg's single_edge_law_per_unit_t pins delta_kappa_c, not C. So
    # e3 MOVES iff delta kappa_c != 0 at some t; e1/e2 PIN iff delta kappa_c == 0
    # at every t.
    e3_moves = any(gauged[(2, fr(t))]["A"]["kappa_c"] != base["kappa_c"] for t in WITNESS_T)
    e1_pins = all(gauged[(0, fr(t))]["A"]["kappa_c"] == base["kappa_c"] for t in WITNESS_T)
    e2_pins = all(gauged[(1, fr(t))]["A"]["kappa_c"] == base["kappa_c"] for t in WITNESS_T)
    verdicts["PC4_deltaC_in_ker_Sigma_keystone"] = {
        "pass": pc4_ok and e3_moves and e1_pins and e2_pins,
        "e3_genuine_move": e3_moves, "e1_pins": e1_pins, "e2_pins": e2_pins,
        "detail": pc4_detail}

    # ===== PC5 single-edge law symbolic over Q =====
    sym_law = symbolic_single_edge_law_proof()
    pc5_pass = (sym_law["all_edges_identity_holds"] is True
                and all(sym_law[f"e{i+1}"]["residual_monomials"] == 0 for i in EDGES))
    verdicts["PC5_single_edge_law_symbolic_over_Q"] = {"pass": pc5_pass, "proof": sym_law}

    # ===== PC6 K_G/sigma_r invariance symbolic over Q =====
    sym_inv = symbolic_KG_invariance_proof()
    pc6_pass = (sym_inv["all_edges_det_invariance_holds"] is True
                and sym_inv["all_edges_PHP_unchanged"] is True
                and all(sym_inv[f"e{i+1}"]["det_residual_monomials"] == 0 for i in EDGES)
                and all(sym_inv[f"e{i+1}"]["PHP_qcleared_nonzero_entries"] == 0 for i in EDGES))
    verdicts["PC6_KG_invariant_symbolic_over_Q"] = {"pass": pc6_pass, "proof": sym_inv}

    # ===== PC7 two-derivation under gauge =====
    pc7_detail: Dict[str, Any] = {}
    pc7_ok = True
    for i in EDGES:
        per_t = {}
        for t in WITNESS_T:
            gg = gauged[(i, fr(t))]
            a = gg["A"]; bp = gg["bp"]
            agree = (a["kappa_c"], a["kappa_s"], a["kappa_int"]) == (bp.kappa_c, bp.kappa_s, bp.kappa_int)
            per_t[fr(t)] = {"A_eq_Bprime": agree}
            pc7_ok = pc7_ok and agree
        pc7_detail[f"e{i+1}"] = per_t
    verdicts["PC7_two_derivation_under_gauge"] = {"pass": pc7_ok, "detail": pc7_detail}

    # ----- emit the gauged-jet records (A/B/Bprime per edge per t) -----
    for i in EDGES:
        for t in WITNESS_T:
            gg = gauged[(i, fr(t))]
            g, Hn, a, bt, bp = gg["g"], gg["H"], gg["A"], gg["bt"], gg["bp"]
            frame = (f"single-edge gauge e{i+1} t={fr(t)} "
                     f"(H -> H + t(g e_{i+1}^T + e_{i+1} g^T)), declared DBP frame")
            _rec(records, fixture_id="F8", role="probe", path="A",
                 frame=frame,
                 g=tuple(fr(x) for x in g),
                 H=tuple(tuple(fr(x) for x in row) for row in Hn),
                 q=fr(a["q"]),
                 delta_c=fr(a["Delta_c"]), delta_s=fr(a["Delta_s"]),
                 delta_m=fr(a["Delta_m"]), det_hb=fr(a["det_hb"]),
                 kappa_c=fr(a["kappa_c"]), kappa_s=fr(a["kappa_s"]),
                 kappa_int=fr(a["kappa_int"]), K_G=fr(a["K_G"]),
                 account=ACCOUNT, closure_ok=(a["K_G"] == base["K_G"]),
                 telemetry={"tr_PHP": fr(gg["tr1"]),
                            "delta_kappa_c": fr(a["kappa_c"] - base["kappa_c"])},
                 notes=f"gauged Path A: edge e{i+1}, t={fr(t)}")
            _rec(records, fixture_id="F8", role="referee_total", path="B",
                 frame=frame, K_G=fr(bt),
                 notes=f"gauged Path B total: edge e{i+1}, t={fr(t)}")
            _rec(records, fixture_id="F8", role="referee_channel", path="Bprime",
                 frame=frame,
                 kappa_c=fr(bp.kappa_c), kappa_s=fr(bp.kappa_s),
                 kappa_int=fr(bp.kappa_int), K_G=fr(bp.K_G),
                 notes=f"gauged Path B' channels: edge e{i+1}, t={fr(t)}")

    # ===== PC8 K4 mutant guards =====
    # (a) sigma-breaking mutant gauge: H -> H + t*(e_i e_i^T) (raw diagonal bump,
    #     NOT the border shear). Must change K_G on the keystone for some edge.
    mut_a_detail = {}
    mut_a_breaks = False
    for i in EDGES:
        Hmut = [list(row) for row in H0]
        Hmut[i][i] += Q(1)  # bump the diagonal entry (t=1)
        kg_mut = bench_probe.read_off(g0, Hmut)["K_G"]
        changed = kg_mut != base["K_G"]
        mut_a_detail[f"e{i+1}"] = {"K_G_mut": fr(kg_mut), "K_G_changed": changed}
        mut_a_breaks = mut_a_breaks or changed
    # (b) wrong-law mutant: use H_ii (diagonal) instead of H_jk (off-diagonal
    #     complement). Must DIFFER from the true single-edge law on the keystone.
    mut_b_detail = {}
    mut_b_differs = False
    for i in EDGES:
        j, k = COMP[i]
        true_law = 4 * Q(1) * prodg * H0[j][k] / q02       # complementary off-diagonal
        wrong_law = 4 * Q(1) * prodg * H0[i][i] / q02       # diagonal entry (wrong)
        diff = true_law != wrong_law
        mut_b_detail[f"e{i+1}"] = {"true_law": fr(true_law), "wrong_law": fr(wrong_law),
                                   "differs": diff}
        mut_b_differs = mut_b_differs or diff
    # (c) e1-moves mutant claim: asserting e1 moves; FALSE against true dkc=0 on e1.
    e1_dkc = gauged[(0, fr(Q(1)))]["A"]["kappa_c"] - base["kappa_c"]
    e1_moves_claim_false = (e1_dkc == Q(0))   # true law: e1 pins, so 'e1 moves' is false
    # true gauge passes: K_G invariant on all edges/t; true law matches; e1/e2 pin.
    true_kg_invariant = all(gauged[(i, fr(t))]["A"]["K_G"] == base["K_G"]
                            for i in EDGES for t in WITNESS_T)
    pc8 = {
        "sigma_breaking_mutant_changes_KG": mut_a_breaks,
        "wrong_law_mutant_differs_from_true": mut_b_differs,
        "e1_moves_claim_is_False": e1_moves_claim_false,
        "true_gauge_KG_invariant": true_kg_invariant,
        "true_gauge_e1_pins": e1_pins, "true_gauge_e2_pins": e2_pins,
        "true_gauge_e3_moves": e3_moves}
    verdicts["PC8_K4_mutant_guards"] = {
        "pass": (mut_a_breaks and mut_b_differs and e1_moves_claim_false
                 and true_kg_invariant and e1_pins and e2_pins and e3_moves),
        "sigma_breaking_mutant": mut_a_detail, "wrong_law_mutant": mut_b_detail,
        "detail": pc8}
    # record the sigma-breaking mutant contrast (role=contrast) on e3.
    Hmut3 = [list(row) for row in H0]
    Hmut3[2][2] += Q(1)
    _rec(records, fixture_id="F8", role="contrast", path="A",
         frame="sigma-breaking MUTANT gauge e3 (H33 += t; NOT the border shear) -- K4 must fire",
         K_G=fr(bench_probe.read_off(g0, Hmut3)["K_G"]),
         notes="K4 mutant: raw diagonal bump changes K_G (sigma_2 not preserved)")

    # ===== PC9 preconditions =====
    psc = check_p_self_cert()
    # P-frame: every channel-bearing record carries a frame (validate already
    # enforces this on construction; re-check here over the emitted set).
    pfr_missing = [r.get("fixture_id") for r in records
                   if any(r.get(n) is not None for n in ("kappa_c", "kappa_s", "kappa_int"))
                   and not r.get("frame")]
    pfr_ok = pfr_missing == []
    verdicts["PC9_preconditions"] = {
        "pass": psc["ok"] and pfr_ok,
        "P_self_cert": psc, "P_frame": {"ok": pfr_ok, "missing_frame": pfr_missing}}

    return records, verdicts


def write_records(records: List[Dict[str, Any]], path: str) -> str:
    """Write records as a deterministic, sorted-keys, byte-stable jsonl;
    return its sha256."""
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
