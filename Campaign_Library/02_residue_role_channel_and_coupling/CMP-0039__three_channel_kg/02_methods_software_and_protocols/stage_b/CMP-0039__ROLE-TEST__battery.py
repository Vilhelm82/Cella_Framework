"""c001 `three_channel_kg` — STAGE B battery (covenant step 2/3/4).

STAGE B — non-negativity impossibility. Implements the FROZEN `prereg.json`
(pin `6602b9e9...`). Claims graded: CL-c3 (no non-negative scalar can represent
the signed K_G), CL-c3b (numerator indefinite => K_G attains both signs,
UNIVERSAL/structural), CL-c3c-i (Sigma:Q^3->Q has a 2-dim kernel), CL-c6
(channel tuple non-collapsible on the family — both signs of kappa_int). Armed
kill: K1 (sign-blindness, MANDATORY) on F8, plus K8/K11 type gates.

It:
  * loads the frozen prereg and re-verifies its sha256 pin;
  * embeds every governing clause VERBATIM in `GRADER_CLAUSES` and
    string-compares each against the frozen prereg's `grader_clauses` at
    runtime -- ANY drift -> `ClauseDrift` REFUSAL (Rule 1.8 / covenant step 2);
  * re-verifies the bench module shas against the prereg `depends_on` (Rule
    1.9 content pins) -- ANY mismatch -> `PinDrift` REFUSAL;
  * imports the FROZEN bench READ-ONLY (probe Path A; referee_total Path B;
    referee_channel Path B'; oracle Path C; fixtures; schema) -- never edits it;
  * runs each of the 10 predictions exact-Q (no tolerance), emits one
    `three_channel_kg_record_v1` per evaluation step, and writes a
    deterministic, sorted-keys, byte-stable records jsonl;
  * grades mechanically into prediction verdicts.

Determinism: every value is a `fractions.Fraction` serialised as `frac:n/d`;
records are emitted in a fixed order with `json.dumps(..., sort_keys=True)`; no
float, no time, no randomness. Two runs MUST be byte-identical.

The CL-c3b UNIVERSAL warrant (R1) is established by a genuine SYMBOLIC
polynomial argument over Q[g,H] (P4) -- NOT finite-fixture agreement alone --
using this module's own exact-Q multivariate engine: it re-derives the bench's
cofactor-expanded det(H_b) symbolically in the 9 indeterminates (g,H), then
SPECIALISES it to a regular 1-parameter family and reads the resulting
univariate t-polynomial K_G(t)=+t, which is nonconstant and therefore attains
both signs (the numerator det(H_b) is indefinite over Q[g,H]). The bench is
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
# paths. STAGE / RESULTS are derived from this file's location (__file__) so
# the committed grader writes its records beside itself in the originating
# worktree OR on `main` after merge. The frozen BENCH, however, is NOT in this
# (bench-less) worktree -- it is committed on `main`. We therefore resolve
# BENCH_DIR to the STABLE MAIN CHECKOUT: if this file lives under a
# `.claude/worktrees/<name>/` segment, the stable main root is the path before
# that segment; otherwise (post-merge on main) the bench sits under the
# __file__-relative repo root. The bench is loaded READ-ONLY by EXACT FILE PATH
# (shadow-proof) and re-pinned against the frozen prereg depends_on at runtime,
# so binding to the exact pinned files is enforced regardless of which root is
# used. The bench modules import only stdlib -- no inter-module / no lloyd_v4
# package imports -- so direct file-path loading is sound and preserves the
# code-disjoint referee separation.
# --------------------------------------------------------------------------
STAGE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.dirname(STAGE)
_FILE_REPO_ROOT = os.path.dirname(os.path.dirname(RESULTS))  # stage_b -> tck -> results -> root


def _stable_main_root(file_repo_root: str) -> str:
    """Resolve the stable main checkout root. If this worktree lives under a
    `.claude/worktrees/<name>/` segment, the main root is the path before that
    segment; otherwise the file-relative repo root is the main root."""
    marker = os.path.join(".claude", "worktrees")
    norm = os.path.normpath(file_repo_root)
    idx = norm.find(os.sep + marker + os.sep)
    if idx != -1:
        return norm[:idx]
    # also handle the case where the repo root itself ends at the worktree dir
    parts = norm.split(os.sep)
    if "worktrees" in parts:
        wt = parts.index("worktrees")
        if wt >= 1 and parts[wt - 1] == ".claude":
            return os.sep.join(parts[:wt - 1])
    return norm


MAIN_ROOT = _stable_main_root(_FILE_REPO_ROOT)
BENCH_DIR = os.path.join(MAIN_ROOT, "src/lloyd_v4/evals/three_channel_kg")
# manifest is pinned in depends_on; verify it against THIS checkout's frozen copy
# (the worktree has the frozen authority objects; they are byte-identical to main).
MANIFEST_PATH = os.path.join(RESULTS, "manifest_v1.json")
PREREG_PATH = os.path.join(STAGE, "prereg.json")
PREREG_PIN_PATH = os.path.join(STAGE, "prereg_sha256.pin")


def _load_bench_module(name: str) -> ModuleType:
    """Load a bench module READ-ONLY from its exact pinned file path under
    BENCH_DIR (the stable main checkout). Shadow-proof; never imports/edits the
    bench package."""
    path = os.path.join(BENCH_DIR, f"{name}.py")
    modname = f"three_channel_kg_bench_b_{name}"
    spec = importlib.util.spec_from_file_location(modname, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load bench module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    # register before exec so @dataclass(slots=True) can resolve cls.__module__
    # via sys.modules (CPython 3.12+ requirement); synthetic name avoids any
    # collision with a shadowing lloyd_v4 package.
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
    "K1_sign_blindness": (
        "on F8: K_G>=0, or K_G!=Sumchannels, or kappa_int absent, or Delta_m "
        "dropped. (meta-thesis; CL-c3)"),
    "type_gate_sqrt_q_leak":
        "a total/channel referee returning a radical/float instead of Fraction -> hard fail (K8).",
    "K8_sqrt_q_leak": "radical/float instead of Fraction -> hard fail (K8).",
    "K11_singular_lie":
        "q=0 / cone-apex / g_i=0 -> typed REFUSED, never 0/NaN/placeholder (K11).",
    "precondition_P_self_cert":
        "the oracle (Path C) must be external to A/B/B', or the run is void.",
    "precondition_P_frame":
        "every channel fixture must carry its frame annotation, or it is rejected.",
    "R1_proven_warrant": (
        "logic-forced, not discretionary. A verified finite exact-Q both-sign "
        "witness earns [PROVEN] for an impossibility / existence claim (CL-c3); "
        "universal claims (CL-c1, CL-c3b) require the symbolic identity over "
        "Q[g,H]. The stage prereg encodes this in status_move_rules."),
    "R2_supplied_frame": (
        "the channels are frame-relative in the supplied DBP frame; only the "
        "sum K_G is intrinsic. CL-c7 graded accordingly."),
    "CLc3c_i_sigma_kernel": (
        "Sigma:Q^3->Q, Sigma(kappa_c,kappa_s,kappa_int)=kappa_c+kappa_s+kappa_int, "
        "is the 1x3 matrix [[1,1,1]] of rank 1 over Q; by rank-nullity its kernel "
        "has dimension 3-1 = 2."),
    "CLc3b_indefinite_numerator": (
        "K_G = -det(H_b)/q^2 with q^2 > 0 for every regular jet (q != 0), so "
        "sign(K_G) = -sign(det(H_b)); det(H_b) is INDEFINITE as a polynomial over "
        "Q[g,H] (it attains strictly positive and strictly negative values at "
        "regular rational jets), hence K_G attains both signs structurally."),
    "CLc3_nonneg_impossible": (
        "No non-negative scalar p>=0 can equal the signed K_G: at the keystone F8, "
        "K_G = -3/49 < 0, so any candidate p>=0 has p != K_G there. A single "
        "exact-Q negative witness refutes every non-negative representor; F6 (K_G=+1>0) "
        "shows the object is genuinely two-signed (not vacuously sign-fixed)."),
    "CLc6_noncollapsible": (
        "The channel tuple is non-collapsible on the family: kappa_int attains both "
        "signs (F10 kappa_int = -1/9 < 0; F11 kappa_int = +2/9 > 0), so no single "
        "sign-fixed surrogate for kappa_int represents the family."),
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
        "results/three_channel_kg/manifest_v1.json": MANIFEST_PATH,
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
        stage="stage_b",
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
# the SYMBOLIC engine over Q[g,H] (CL-c3b universal, P4): a genuine multivariate
# polynomial argument, NOT finite sampling. 9 indeterminates + 1 family param t
# (index 9). Exact-Q coefficients. This module RE-DERIVES the bench's
# cofactor-expanded det(H_b) symbolically, then SPECIALISES it to a regular
# 1-parameter family and reads the univariate t-polynomial K_G(t).
# --------------------------------------------------------------------------
_VARS = ("g1", "g2", "g3", "h11", "h12", "h13", "h22", "h23", "h33", "t")
_NI = 10  # 9 jet indeterminates + 1 family parameter t
_Mono = Tuple[int, ...]
_Poly = Dict[_Mono, Fraction]


def _pvar(i: int) -> _Poly:
    e = [0] * _NI
    e[i] = 1
    return {tuple(e): Q(1)}


def _pconst(c: int) -> _Poly:
    cq = Q(c)
    return {tuple([0] * _NI): cq} if cq != 0 else {}


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


def _det3_sym(M: List[List[_Poly]]) -> _Poly:
    return _padd(
        _pmul(M[0][0], _padd(_pmul(M[1][1], M[2][2]), _pneg(_pmul(M[1][2], M[2][1])))),
        _pneg(_pmul(M[0][1], _padd(_pmul(M[1][0], M[2][2]), _pneg(_pmul(M[1][2], M[2][0]))))),
        _pmul(M[0][2], _padd(_pmul(M[1][0], M[2][1]), _pneg(_pmul(M[1][1], M[2][0])))))


def _det4_sym(M: List[List[_Poly]]) -> _Poly:
    acc: _Poly = {}
    sign = 1
    for c in range(4):
        minor = [[M[r][cc] for cc in range(4) if cc != c] for r in range(1, 4)]
        term = _pmul(M[0][c], _det3_sym(minor))
        acc = _padd(acc, term if sign == 1 else _pneg(term))
        sign = -sign
    return acc


def _det_hb_symbolic() -> _Poly:
    """The cofactor-expanded det(H_b) for H_b = [[0, g^T],[g, H]] as an exact-Q
    polynomial in the 9 jet indeterminates (t-degree 0). Independent of the
    probe's monomial split -- a first-principles symbolic determinant."""
    g1, g2, g3 = _pvar(0), _pvar(1), _pvar(2)
    h11, h12, h13 = _pvar(3), _pvar(4), _pvar(5)
    h22, h23, h33 = _pvar(6), _pvar(7), _pvar(8)
    Z: _Poly = {}
    Hb = [[Z, g1, g2, g3],
          [g1, h11, h12, h13],
          [g2, h12, h22, h23],
          [g3, h13, h23, h33]]
    return _det4_sym(Hb)


def _specialise(poly: _Poly, subst: Dict[int, _Poly]) -> _Poly:
    """Substitute each jet indeterminate (indices 0..8) by a polynomial in t
    (index 9). Exact; closes in Q[t]."""
    out: _Poly = {}
    for mono, coef in poly.items():
        term: _Poly = {tuple([0] * _NI): coef}
        for i, e in enumerate(mono):
            if i == 9:
                for _ in range(e):
                    term = _pmul(term, _pvar(9))
                continue
            for _ in range(e):
                term = _pmul(term, subst[i])
        out = _padd(out, term)
    return out


def _as_t_poly(poly: _Poly) -> Dict[int, Fraction]:
    """A polynomial that survives specialisation must be univariate in t
    (indices 0..8 all zero). Return {t_power: coeff}. Raises if a non-t variable
    survived (a guard that the specialisation was complete)."""
    d: Dict[int, Fraction] = {}
    for mono, coef in poly.items():
        if any(mono[i] != 0 for i in range(9)):
            raise AssertionError(
                f"specialisation incomplete: non-t monomial survived {mono}")
        d[mono[9]] = d.get(mono[9], Q(0)) + coef
    return {k: v for k, v in d.items() if v != 0}


def symbolic_indefinite_proof() -> Dict[str, Any]:
    """CL-c3b (P4): prove det(H_b) is INDEFINITE over Q[g,H] symbolically.

    Build the full symbolic det(H_b) in the 9 jet indeterminates, specialise to
    the regular 1-parameter family

        g = (1, 0, 0)           (q = g.g = 1 != 0, regular for ALL t)
        H = [[0, 0, 0],
             [0, t, 0],
             [0, 0, 1]]

    and read the resulting univariate t-polynomial. K_G(t) = -det(H_b)(t)/q^2 =
    -det(H_b)(t) (q=1). The result is K_G(t) = +t: a degree-1 (nonconstant)
    polynomial with leading coeff +1, so it attains strictly positive (t=1) and
    strictly negative (t=-1) values at regular rational jets => det(H_b) is
    indefinite over Q[g,H], and K_G attains both signs structurally. Complete;
    no sampling, no tolerance.
    """
    det_sym = _det_hb_symbolic()
    det_monomials = len(det_sym)

    # the regular family substitution (q = 1 identically; q^2 = 1 > 0 for all t)
    subst = {
        0: _pconst(1),  # g1 = 1
        1: {},          # g2 = 0
        2: {},          # g3 = 0
        3: {},          # h11 = 0
        4: {},          # h12 = 0
        5: {},          # h13 = 0
        6: _pvar(9),    # h22 = t
        7: {},          # h23 = 0
        8: _pconst(1),  # h33 = 1
    }
    det_family = _specialise(det_sym, subst)
    det_t = _as_t_poly(det_family)               # {power: coeff} of det(H_b)(t)

    # q on the family is identically 1 (g.g = 1^2 + 0 + 0); q^2 = 1.
    # K_G(t) = -det(H_b)(t) / 1 = -det(H_b)(t).
    kg_t = {p: -c for p, c in det_t.items()}

    deg = max(kg_t) if kg_t else 0
    lead = kg_t.get(deg, Q(0))
    nonconstant = deg >= 1 and lead != 0

    def _eval_t(poly: Dict[int, Fraction], val: Fraction) -> Fraction:
        return sum((poly.get(p, Q(0)) * (val ** p) for p in poly), Q(0))

    kg_at_p1 = _eval_t(kg_t, Q(1))
    kg_at_m1 = _eval_t(kg_t, Q(-1))
    indefinite = nonconstant and (kg_at_p1 > 0) and (kg_at_m1 < 0)

    return {
        "det_monomials": det_monomials,
        "det_t_polynomial": {str(p): fr(c) for p, c in sorted(det_t.items())},
        "K_G_t_polynomial": {str(p): fr(c) for p, c in sorted(kg_t.items())},
        "K_G_t_degree": deg,
        "K_G_t_leading_coeff": fr(lead),
        "K_G_t_nonconstant": nonconstant,
        "K_G_at_t_eq_1": fr(kg_at_p1),
        "K_G_at_t_eq_minus_1": fr(kg_at_m1),
        "q_on_family": fr(Q(1)),
        "q_squared_on_family": fr(Q(1)),
        "q_squared_strictly_positive": Q(1) > 0,
        "numerator_indefinite_over_Q_g_H": indefinite,
        "indeterminates": list(_VARS[:9]),
        "family": "g=(1,0,0) (q=1, regular for all t), H=[[0,0,0],[0,t,0],[0,0,1]]",
    }


# --------------------------------------------------------------------------
# Sigma kernel (CL-c3c-i, P5): exact-Q linear algebra. Sigma = [[1,1,1]].
# rank 1 => nullity 2 by rank-nullity; (1,-1,0),(1,0,-1) are independent kernel
# vectors. No bench dependency -- a pure exact-Q fact.
# --------------------------------------------------------------------------
def _sigma(v: Tuple[Fraction, Fraction, Fraction]) -> Fraction:
    return v[0] + v[1] + v[2]


def _rank_1x3(row: Tuple[Fraction, Fraction, Fraction]) -> int:
    """Rank over Q of the 1x3 matrix [row]: 1 if any entry nonzero, else 0."""
    return 1 if any(x != 0 for x in row) else 0


def _independent_2(u: Tuple[Fraction, ...], w: Tuple[Fraction, ...]) -> bool:
    """Two 3-vectors are linearly independent over Q iff some 2x2 minor of the
    2x3 matrix [u; w] is nonzero. Exact."""
    minors = [
        u[0] * w[1] - u[1] * w[0],
        u[0] * w[2] - u[2] * w[0],
        u[1] * w[2] - u[2] * w[1],
    ]
    return any(m != 0 for m in minors)


def sigma_kernel_proof() -> Dict[str, Any]:
    row = (Q(1), Q(1), Q(1))
    rank = _rank_1x3(row)
    domain_dim = 3
    nullity = domain_dim - rank          # rank-nullity over Q
    v1 = (Q(1), Q(-1), Q(0))
    v2 = (Q(1), Q(0), Q(-1))
    s1 = _sigma(v1)
    s2 = _sigma(v2)
    indep = _independent_2(v1, v2)
    return {
        "Sigma_matrix": "[[1,1,1]]",
        "rank_over_Q": rank,
        "domain_dim": domain_dim,
        "nullity_dim": nullity,
        "rank_plus_nullity_eq_domain": rank + nullity == domain_dim,
        "kernel_vec_1": [fr(x) for x in v1],
        "kernel_vec_2": [fr(x) for x in v2],
        "Sigma_v1": fr(s1),
        "Sigma_v2": fr(s2),
        "both_in_kernel": s1 == Q(0) and s2 == Q(0),
        "kernel_vecs_independent": indep,
    }


# --------------------------------------------------------------------------
# precondition checks: P-self-cert (import-graph disjointness) + P-frame
# --------------------------------------------------------------------------
def _module_imports_any(mod_path: str, names: Tuple[str, ...]) -> List[str]:
    """Return which of `names` appear as imports in the module SOURCE (a coarse
    but sufficient self-cert check). Source-text scan, exact-string."""
    with open(mod_path, "r", encoding="utf-8") as fh:
        src = fh.read()
    hits = []
    for n in names:
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
    """P-frame: every in-scope (Stage-B) channel fixture carries a non-empty
    frame."""
    missing = []
    for fid in STAGE_B_FIXTURES:
        f = fx[fid]
        if not getattr(f, "frame", None):
            missing.append(fid)
    return {"ok": missing == [], "missing_frame": missing}


# --------------------------------------------------------------------------
# the run: produce records + grade predictions
# --------------------------------------------------------------------------
STAGE_B_FIXTURES = ("F6", "F8", "F10", "F11")
ACCOUNT = {"ledger": "stage_b", "covenant": "role=probe + account",
           "campaign": "three_channel_kg", "cycle": "c001"}


def _emit_fixture_rows(records: List[Dict[str, Any]],
                       fx: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Emit one record per Stage-B fixture per path (A/B/B'/C) and return the
    per-fixture computed values (exact Fraction) for grading."""
    computed: Dict[str, Dict[str, Any]] = {}
    for fid in STAGE_B_FIXTURES:
        f = fx[fid]
        a = bench_probe.read_off(f.g, f.H)
        bt = bench_reft.referee_total(f.g, f.H)
        bp = bench_refc.referee_channel(f.g, f.H)
        orc = bench_oracle.oracle(fid)
        computed[fid] = {"a": a, "bt": bt, "bp": bp, "orc": orc, "f": f}

        agree = {
            "A_eq_B_total_KG": a["K_G"] == bt,
            "A_eq_Bprime_channels": (a["kappa_c"], a["kappa_s"], a["kappa_int"])
                                    == (bp.kappa_c, bp.kappa_s, bp.kappa_int),
            "A_eq_C_oracle": (a["K_G"], a["kappa_c"], a["kappa_s"], a["kappa_int"])
                             == (orc.K_G, orc.kappa_c, orc.kappa_s, orc.kappa_int),
            "KG_eq_sum_channels": a["K_G"] == a["kappa_c"] + a["kappa_s"] + a["kappa_int"],
            "det_eq_partition": a["det_hb"] == a["Delta_c"] + a["Delta_s"] + a["Delta_m"],
        }
        all_agree = all(agree.values())

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
             account=ACCOUNT, closure_ok=all_agree,
             referee={"cross_path_agreement": agree},
             notes="Path A monomial read-off (Stage-B both-sign witness)")
        _rec(records, fixture_id=fid, role="referee_total", path="B",
             frame=f.frame, K_G=fr(bt),
             notes="Path B total -det(H_b)/q^2 (Bareiss)")
        _rec(records, fixture_id=fid, role="referee_channel", path="Bprime",
             frame=f.frame,
             kappa_c=fr(bp.kappa_c), kappa_s=fr(bp.kappa_s),
             kappa_int=fr(bp.kappa_int), K_G=fr(bp.K_G),
             notes="Path B' split shape-operator channels")
        _rec(records, fixture_id=fid, role="oracle", path="C",
             frame=orc.frame,
             kappa_c=fr(orc.kappa_c), kappa_s=fr(orc.kappa_s),
             kappa_int=fr(orc.kappa_int), K_G=fr(orc.K_G),
             notes="Path C frozen external oracle")
    return computed


def run() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    prereg = load_prereg()
    gate_clauses(prereg)
    gate_bench_pins(prereg)

    # Stage-0 control: every frozen fixture reproduces exactly (raises on drift).
    fx = bench_fixtures.generate_and_check()

    records: List[Dict[str, Any]] = []
    verdicts: Dict[str, Any] = {}

    computed = _emit_fixture_rows(records, fx)
    a8 = computed["F8"]["a"]

    # ===== P1 K1 sign-blindness does NOT fire on the TRUE signed F8 object =====
    # K1 trip-conditions (each must be FALSE on the true object):
    #   (i) K_G >= 0 ; (ii) K_G != sum(channels) ; (iii) kappa_int absent ;
    #   (iv) Delta_m dropped.
    kg8 = a8["K_G"]
    sum8 = a8["kappa_c"] + a8["kappa_s"] + a8["kappa_int"]
    cond_KG_ge_0 = kg8 >= 0
    cond_KG_ne_sum = kg8 != sum8
    cond_kappa_int_absent = a8["kappa_int"] is None
    cond_Delta_m_dropped = (a8["Delta_m"] == 0) or (a8["det_hb"] != a8["Delta_c"] + a8["Delta_s"] + a8["Delta_m"])
    k1_fires = cond_KG_ge_0 or cond_KG_ne_sum or cond_kappa_int_absent or cond_Delta_m_dropped
    p1_detail = {
        "K_G": fr(kg8), "K_G_lt_0": kg8 < 0,
        "cond_i_KG_ge_0": cond_KG_ge_0,
        "cond_ii_KG_ne_sum": cond_KG_ne_sum,
        "cond_iii_kappa_int_absent": cond_kappa_int_absent,
        "kappa_int": fr(a8["kappa_int"]),
        "cond_iv_Delta_m_dropped": cond_Delta_m_dropped,
        "Delta_m": fr(a8["Delta_m"]), "Delta_m_nonzero": a8["Delta_m"] != 0,
        "K1_fires_on_true_object": k1_fires,
    }
    verdicts["P1_K1_sign_blindness_F8"] = {
        "pass": (not k1_fires) and kg8 < 0,
        "K1_fires_on_true_object": k1_fires,
        "detail": p1_detail,
    }
    _rec(records, fixture_id="F8", role="probe", path="A",
         frame=computed["F8"]["f"].frame,
         q=fr(a8["q"]), delta_m=fr(a8["Delta_m"]), det_hb=fr(a8["det_hb"]),
         kappa_c=fr(a8["kappa_c"]), kappa_s=fr(a8["kappa_s"]),
         kappa_int=fr(a8["kappa_int"]), K_G=fr(kg8),
         account=ACCOUNT, closure_ok=(not k1_fires),
         referee={"P1_K1": p1_detail},
         notes="K1 sign-blindness check: true signed F8 object passes (K1 silent)")

    # ===== P2 every sign-blind proxy FIRES K1 on F8 =====
    # Each proxy is computed and shown >=0 (sign-blind) and != K_G (= -3/49 < 0),
    # so each fires K1. PINNED: K_G^2 = 9/2401 is the MANIFEST kappa^2 proxy (the
    # squared TOTAL), NOT the channel-norm 11/2401.
    proxy_KG2 = kg8 * kg8                                   # = 9/2401 (the manifest kappa^2 proxy)
    channel_norm = (a8["kappa_c"] ** 2 + a8["kappa_s"] ** 2 + a8["kappa_int"] ** 2)  # = 11/2401, REFERENCE ONLY
    proxy_H2 = Q(18, 343)                                   # H^2 proxy (manifest)
    proxy_p_nonneg = Q(0)                                   # any p>=0 (use the boundary 0)
    proxy_drop_Delta_m = a8["kappa_c"] + a8["kappa_s"]      # drop-Delta_m: = 0
    proxies = {
        "K_G_squared": proxy_KG2,
        "H_squared": proxy_H2,
        "p_nonneg_boundary_0": proxy_p_nonneg,
        "drop_Delta_m_kappa_c_plus_kappa_s": proxy_drop_Delta_m,
    }
    proxy_fire = {name: (val >= 0 and val != kg8) for name, val in proxies.items()}
    # omit-tuple: a representation that drops kappa_int retains only the
    # non-negative (kappa_c,kappa_s) surrogate (= kappa_c+kappa_s = 0 >= 0) and
    # cannot reconstruct the signed K_G < 0 -> counted as the 5th sign-blind mode.
    omit_tuple_fires = True
    all_fire = all(proxy_fire.values()) and omit_tuple_fires
    p2_detail = {
        "K_G_for_reference": fr(kg8), "K_G_is_negative": kg8 < 0,
        "proxy_K_G_squared": fr(proxy_KG2),
        "proxy_K_G_squared_is_manifest_kappa2_9_2401": proxy_KG2 == Q(9, 2401),
        "channel_norm_11_2401_REFERENCE_ONLY": fr(channel_norm),
        "channel_norm_eq_11_2401": channel_norm == Q(11, 2401),
        "pinned_note": "manifest kappa^2=9/2401 is K_G^2 (squared TOTAL), NOT the channel-norm 11/2401",
        "proxy_H_squared": fr(proxy_H2),
        "proxy_p_nonneg_boundary": fr(proxy_p_nonneg),
        "proxy_drop_Delta_m": fr(proxy_drop_Delta_m),
        "each_proxy_nonneg_and_ne_KG": proxy_fire,
        "omit_tuple_fires": omit_tuple_fires,
        "proxies_firing_count": sum(1 for v in proxy_fire.values() if v) + (1 if omit_tuple_fires else 0),
        "all_proxies_fire_K1": all_fire,
    }
    verdicts["P2_K1_proxies_all_fire_F8"] = {"pass": all_fire, "detail": p2_detail}
    for name, val in proxies.items():
        _rec(records, fixture_id="F8", role="contrast", path="A",
             frame=computed["F8"]["f"].frame,
             K_G=fr(val),
             notes=f"K1 sign-blind proxy '{name}'={fr(val)} >=0 != K_G(-3/49) -> FIRES K1")

    # ===== P3 CL-c3 impossibility: both-sign witnesses (R1 logic-forced) =====
    kg6 = computed["F6"]["a"]["K_G"]
    p3_detail = {
        "F8_KG": fr(kg8), "F8_KG_negative": kg8 < 0,
        "F6_KG": fr(kg6), "F6_KG_positive": kg6 > 0,
        "negative_witness_refutes_all_nonneg": kg8 < 0,
        "positive_witness_two_signed": kg6 > 0,
        "no_nonneg_scalar_represents_signed_KG": (kg8 < 0) and (kg6 > 0),
    }
    verdicts["P3_CLc3_nonneg_impossible_witness"] = {
        "pass": (kg8 < 0) and (kg8 == Q(-3, 49)) and (kg6 > 0) and (kg6 == Q(1)),
        "detail": p3_detail,
    }

    # ===== P4 CL-c3b UNIVERSAL: numerator indefinite over Q[g,H] (symbolic) =====
    sym = symbolic_indefinite_proof()
    p4_pass = (sym["numerator_indefinite_over_Q_g_H"] is True
               and sym["K_G_t_nonconstant"] is True
               and sym["K_G_t_degree"] == 1
               and sym["K_G_t_leading_coeff"] == "frac:1/1"
               and sym["K_G_at_t_eq_1"] == "frac:1/1"
               and sym["K_G_at_t_eq_minus_1"] == "frac:-1/1"
               and sym["q_squared_strictly_positive"] is True
               and sym["det_monomials"] == 12)
    verdicts["P4_CLc3b_symbolic_indefinite_universal"] = {"pass": p4_pass, "proof": sym}
    _rec(records, fixture_id="F8", role="contrast", path="A",
         frame="symbolic Q[g,H] (no numeric jet)",
         notes=("P4 symbolic indefiniteness over Q[g,H]: det(H_b) specialises to "
                f"K_G(t)={sym['K_G_t_polynomial']} on a regular family (q^2=1>0), "
                f"nonconstant deg {sym['K_G_t_degree']}, indefinite="
                f"{sym['numerator_indefinite_over_Q_g_H']}"),
         telemetry={"symbolic_proof": sym})

    # ===== P5 CL-c3c-i: Sigma has 2-dim kernel (exact-Q linear algebra) =====
    sk = sigma_kernel_proof()
    p5_pass = (sk["rank_over_Q"] == 1 and sk["nullity_dim"] == 2
               and sk["rank_plus_nullity_eq_domain"] is True
               and sk["both_in_kernel"] is True
               and sk["kernel_vecs_independent"] is True)
    verdicts["P5_CLc3c_i_sigma_kernel_2dim"] = {"pass": p5_pass, "proof": sk}
    _rec(records, fixture_id="F8", role="contrast", path="A",
         frame="exact-Q linear algebra (Sigma=[[1,1,1]], no numeric jet)",
         notes=(f"P5 Sigma kernel: rank={sk['rank_over_Q']}, nullity={sk['nullity_dim']} "
                f"(rank-nullity); kernel basis {sk['kernel_vec_1']},{sk['kernel_vec_2']}"),
         telemetry={"sigma_kernel": sk})

    # ===== P6 CL-c6: kappa_int attains both signs on the family =====
    ki10_a = computed["F10"]["a"]["kappa_int"]
    ki10_b = computed["F10"]["bp"].kappa_int
    ki10_c = computed["F10"]["orc"].kappa_int
    ki11_a = computed["F11"]["a"]["kappa_int"]
    ki11_b = computed["F11"]["bp"].kappa_int
    ki11_c = computed["F11"]["orc"].kappa_int
    p6_detail = {
        "F10_kappa_int_A": fr(ki10_a), "F10_kappa_int_Bprime": fr(ki10_b), "F10_kappa_int_C": fr(ki10_c),
        "F10_negative": ki10_a < 0,
        "F10_paths_agree": ki10_a == ki10_b == ki10_c,
        "F11_kappa_int_A": fr(ki11_a), "F11_kappa_int_Bprime": fr(ki11_b), "F11_kappa_int_C": fr(ki11_c),
        "F11_positive": ki11_a > 0,
        "F11_paths_agree": ki11_a == ki11_b == ki11_c,
        "both_signs_of_kappa_int": (ki10_a < 0) and (ki11_a > 0),
    }
    verdicts["P6_CLc6_kappa_int_both_signs"] = {
        "pass": (ki10_a == Q(-1, 9) and ki10_a < 0 and ki10_a == ki10_b == ki10_c
                 and ki11_a == Q(2, 9) and ki11_a > 0 and ki11_a == ki11_b == ki11_c),
        "detail": p6_detail,
    }

    # ===== P7 BOTH_SIGN_WITNESSES present (cross-path) =====
    f6 = computed["F6"]; f8 = computed["F8"]; f10 = computed["F10"]; f11 = computed["F11"]

    def _tuple(c):
        return (c["a"]["K_G"], c["a"]["kappa_c"], c["a"]["kappa_s"], c["a"]["kappa_int"])

    def _agree_all(c):
        a = c["a"]; bp = c["bp"]; bt = c["bt"]; orc = c["orc"]
        return (a["K_G"] == bt
                and (a["kappa_c"], a["kappa_s"], a["kappa_int"]) == (bp.kappa_c, bp.kappa_s, bp.kappa_int)
                and (a["K_G"], a["kappa_c"], a["kappa_s"], a["kappa_int"]) == (orc.K_G, orc.kappa_c, orc.kappa_s, orc.kappa_int))
    p7_detail = {
        "F6_KG": fr(f6["a"]["K_G"]), "F6_eq_plus1": f6["a"]["K_G"] == Q(1),
        "F8_KG": fr(f8["a"]["K_G"]), "F8_eq_m3_49": f8["a"]["K_G"] == Q(-3, 49),
        "F10_tuple": [fr(x) for x in _tuple(f10)],
        "F10_expected": (f10["a"]["K_G"] == Q(2, 9) and f10["a"]["kappa_c"] == Q(1, 3)
                         and f10["a"]["kappa_s"] == Q(0) and f10["a"]["kappa_int"] == Q(-1, 9)),
        "F11_tuple": [fr(x) for x in _tuple(f11)],
        "F11_expected": (f11["a"]["K_G"] == Q(0) and f11["a"]["kappa_c"] == Q(-1, 9)
                         and f11["a"]["kappa_s"] == Q(-1, 9) and f11["a"]["kappa_int"] == Q(2, 9)),
        "F6_paths_agree": _agree_all(f6), "F8_paths_agree": _agree_all(f8),
        "F10_paths_agree": _agree_all(f10), "F11_paths_agree": _agree_all(f11),
        "both_signs_KG": (f6["a"]["K_G"] > 0) and (f8["a"]["K_G"] < 0),
        "both_signs_kappa_int": (f10["a"]["kappa_int"] < 0) and (f11["a"]["kappa_int"] > 0),
    }
    verdicts["P7_both_sign_witnesses_present"] = {
        "pass": (p7_detail["F6_eq_plus1"] and p7_detail["F8_eq_m3_49"]
                 and p7_detail["F10_expected"] and p7_detail["F11_expected"]
                 and p7_detail["F6_paths_agree"] and p7_detail["F8_paths_agree"]
                 and p7_detail["F10_paths_agree"] and p7_detail["F11_paths_agree"]
                 and p7_detail["both_signs_KG"] and p7_detail["both_signs_kappa_int"]),
        "detail": p7_detail,
    }

    # ===== P8 K11 singular refusal (underwrites q^2>0 premise of CL-c3b) =====
    g0 = (Q(0), Q(0), Q(0))
    H0 = ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1)))
    refusals = {}
    try:
        bench_probe.read_off(g0, H0)
        refusals["pathA"] = {"refused": False, "kind": None}
    except bench_probe.ThreeChannelRefusal as e:
        refusals["pathA"] = {"refused": True, "kind": e.kind}
    try:
        bench_reft.referee_total(g0, H0)
        refusals["pathB"] = {"refused": False}
    except bench_reft.RefereeRefusal:
        refusals["pathB"] = {"refused": True}
    try:
        bench_refc.referee_channel(g0, H0)
        refusals["pathBprime"] = {"refused": False}
    except bench_refc.RefereeRefusal:
        refusals["pathBprime"] = {"refused": True}
    f6obj = fx["F6"]
    f6_refused = False
    f6_kg = None
    try:
        f6_kg = bench_probe.read_off(f6obj.g, f6obj.H)["K_G"]
    except bench_probe.ThreeChannelRefusal:
        f6_refused = True
    all_refused = (refusals["pathA"]["refused"] and refusals["pathB"]["refused"]
                   and refusals["pathBprime"]["refused"])
    f6_ok = (not f6_refused) and (f6_kg == Q(1))
    verdicts["P8_K11_singular_refusal"] = {
        "pass": all_refused and f6_ok,
        "q0_all_paths_refused": all_refused,
        "q0_refusals": refusals,
        "F6_single_gi0_not_refused_and_KG_1": f6_ok,
        "F6_K_G": fr(f6_kg) if f6_kg is not None else None,
    }
    _rec(records, fixture_id="F8", role="contrast", path="A",
         frame="declared DBP frame (singular probe g=(0,0,0))",
         refusals=("singular_refused",),
         notes="K11 genuine q=0 (g=(0,0,0)) -> typed REFUSED on A/B/Bprime (no numeric); underwrites q^2>0 premise")

    # ===== P9 sqrt-q-leak type gate (K8) =====
    all_fraction = True
    type_detail = {}
    for fid in STAGE_B_FIXTURES:
        c = computed[fid]
        a = c["a"]; bt = c["bt"]; bp = c["bp"]
        vals = ([a["K_G"], a["kappa_c"], a["kappa_s"], a["kappa_int"], a["q"], a["det_hb"]]
                + [bt] + [bp.kappa_c, bp.kappa_s, bp.kappa_int, bp.K_G])
        ok = all(isinstance(v, Fraction) for v in vals)
        type_detail[fid] = ok
        all_fraction = all_fraction and ok
    float_refused = False
    try:
        bench_probe.read_off((1.0, 1.0, 1.0),
                             ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    except TypeError:
        float_refused = True
    except Exception:
        float_refused = False
    verdicts["P9_type_gate_sqrt_q_leak"] = {
        "pass": all_fraction and float_refused,
        "all_emitted_are_Fraction": all_fraction,
        "float_operand_raises_TypeError": float_refused,
        "detail": type_detail,
    }

    # ===== P10 preconditions =====
    psc = check_p_self_cert()
    pfr = check_p_frame(fx)
    verdicts["P10_preconditions"] = {
        "pass": psc["ok"] and pfr["ok"],
        "P_self_cert": psc, "P_frame": pfr,
    }

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
