"""Problem specification: validation of the declarative JSON spec.

A spec describes one application of the wreath-lift theorem: the base cover,
the radical channels, the candidate divisors with claimed parity rows, and
the named slices. Validation is structural and syntactic only — every
mathematical claim in the spec (primality, parities, base images) is checked
later by Macaulay2, never here.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field

IDENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*")
POLY_CHARS_RE = re.compile(r"^[A-Za-z0-9+\-*/^() \t]*$")
ALLOWED_ORDERS = {"GRevLex", "Lex", "GLex"}
DIVISOR_TYPES = {"contact", "private"}


class SpecError(ValueError):
    """Validation failure; message carries a JSON-pointer-style path."""

    def __init__(self, path: str, message: str):
        self.path = path
        super().__init__(f"{path}: {message}")


@dataclass(frozen=True)
class Ring:
    variables: tuple[str, ...]
    weights: tuple[int, ...]
    order: str
    coefficients: str


@dataclass(frozen=True)
class Group:
    name: str
    order: int
    claimed_by: str


@dataclass(frozen=True)
class BaseCover:
    incidence_gens: tuple[str, ...]
    sheet_vars: tuple[str, ...]
    degree: int
    expected_codim: int
    group: Group
    ramification_det_identity: str | None = None


@dataclass(frozen=True)
class Channel:
    name: str
    radicand: str


@dataclass(frozen=True)
class Divisor:
    name: str
    gens: tuple[str, ...]
    claimed_parity_row: tuple[int, ...]
    type: str
    expected_base_image: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class Slice:
    name: str
    assignments: dict[str, int | str]


@dataclass(frozen=True)
class ProblemSpec:
    name: str
    ring: Ring
    base_cover: BaseCover
    channels: tuple[Channel, ...]
    divisors: tuple[Divisor, ...]
    generic_denominator: str | None
    slices: tuple[Slice, ...]
    base_cycle_data: tuple[dict, ...] = field(default_factory=tuple)
    raw: dict = field(default_factory=dict, compare=False, repr=False)

    @property
    def s(self) -> int:
        return len(self.channels)

    @property
    def d(self) -> int:
        return self.base_cover.degree

    def content_hash(self) -> str:
        canonical = json.dumps(self.raw, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()[:12]


def _require(cond: bool, path: str, message: str) -> None:
    if not cond:
        raise SpecError(path, message)


def _check_poly(expr: str, allowed_names: set[str], path: str) -> None:
    _require(isinstance(expr, str) and expr.strip() != "", path, "must be a nonempty string")
    _require(POLY_CHARS_RE.match(expr) is not None, path,
             "contains characters outside the polynomial charset [A-Za-z0-9 +-*/^()]")
    for token in TOKEN_RE.findall(expr):
        _require(token in allowed_names, path,
                 f"unknown identifier {token!r}; not a ring variable or previously defined channel")


def validate(doc: dict) -> ProblemSpec:
    _require(isinstance(doc, dict), "/", "spec must be a JSON object")

    name = doc.get("name")
    _require(isinstance(name, str) and IDENT_RE.match(name.replace("_", "x")) is not None
             and re.match(r"^[A-Za-z][A-Za-z0-9_]*$", name) is not None,
             "/name", "must be an identifier-like string")

    # --- ring ---
    ring_doc = doc.get("ring")
    _require(isinstance(ring_doc, dict), "/ring", "required object")
    variables = ring_doc.get("variables")
    _require(isinstance(variables, list) and variables, "/ring/variables", "nonempty list required")
    for i, v in enumerate(variables):
        _require(isinstance(v, str) and IDENT_RE.match(v) is not None,
                 f"/ring/variables/{i}", f"invalid variable name {v!r}")
    _require(len(set(variables)) == len(variables), "/ring/variables", "duplicate variable names")
    weights = ring_doc.get("weights", [1] * len(variables))
    _require(isinstance(weights, list) and len(weights) == len(variables),
             "/ring/weights", "must match variables in length")
    for i, w in enumerate(weights):
        _require(isinstance(w, int) and w >= 1, f"/ring/weights/{i}", "weights are positive integers")
    order = ring_doc.get("order", "GRevLex")
    _require(order in ALLOWED_ORDERS, "/ring/order", f"must be one of {sorted(ALLOWED_ORDERS)}")
    coefficients = ring_doc.get("coefficients", "QQ")
    _require(coefficients == "QQ", "/ring/coefficients", "only QQ is supported in v1")
    ring = Ring(tuple(variables), tuple(weights), order, coefficients)
    var_set = set(variables)

    # --- base cover ---
    bc = doc.get("base_cover")
    _require(isinstance(bc, dict), "/base_cover", "required object")
    gens = bc.get("incidence_gens")
    _require(isinstance(gens, list) and gens, "/base_cover/incidence_gens", "nonempty list required")
    for i, g in enumerate(gens):
        _check_poly(g, var_set, f"/base_cover/incidence_gens/{i}")
    sheet_vars = bc.get("sheet_vars")
    _require(isinstance(sheet_vars, list) and sheet_vars, "/base_cover/sheet_vars", "nonempty list required")
    for i, v in enumerate(sheet_vars):
        _require(v in var_set, f"/base_cover/sheet_vars/{i}", f"{v!r} is not a ring variable")
    _require(len(gens) == len(sheet_vars), "/base_cover",
             "incidence_gens and sheet_vars must have equal length "
             "(the relative Jacobian must be square for the ramification determinant)")
    degree = bc.get("degree")
    _require(isinstance(degree, int) and degree >= 2, "/base_cover/degree", "integer >= 2 required")
    expected_codim = bc.get("expected_codim", len(gens))
    _require(isinstance(expected_codim, int) and expected_codim >= 1,
             "/base_cover/expected_codim", "positive integer required")
    group_doc = bc.get("group")
    _require(isinstance(group_doc, dict), "/base_cover/group", "required object")
    gname = group_doc.get("name")
    _require(isinstance(gname, str) and gname, "/base_cover/group/name", "required string")
    gorder = group_doc.get("order")
    _require(isinstance(gorder, int) and gorder >= 1, "/base_cover/group/order", "positive integer required")
    _require(math.factorial(degree) % gorder == 0, "/base_cover/group/order",
             f"claimed order {gorder} does not divide {degree}! — inconsistent with a degree-{degree} cover")
    claimed_by = group_doc.get("claimed_by", "unspecified")
    _require(isinstance(claimed_by, str), "/base_cover/group/claimed_by", "must be a string")
    ram_identity = bc.get("ramification_det_identity")
    if ram_identity is not None:
        _check_poly(ram_identity, var_set, "/base_cover/ramification_det_identity")
    base_cover = BaseCover(tuple(gens), tuple(sheet_vars), degree, expected_codim,
                           Group(gname, gorder, claimed_by), ram_identity)

    # --- channels ---
    ch_doc = doc.get("channels")
    _require(isinstance(ch_doc, list) and ch_doc, "/channels", "nonempty list required")
    channels: list[Channel] = []
    known_names = set(var_set)
    for i, ch in enumerate(ch_doc):
        _require(isinstance(ch, dict), f"/channels/{i}", "object required")
        cname = ch.get("name")
        _require(isinstance(cname, str) and IDENT_RE.match(cname) is not None,
                 f"/channels/{i}/name", "identifier required")
        _require(cname not in {c.name for c in channels}, f"/channels/{i}/name", "duplicate channel name")
        radicand = ch.get("radicand")
        _check_poly(radicand, known_names, f"/channels/{i}/radicand")
        if cname in var_set:
            _require(radicand.strip() == cname, f"/channels/{i}/radicand",
                     f"channel named after ring variable {cname!r} must have radicand exactly {cname!r} "
                     "(anything else would shadow the variable in generated M2)")
        channels.append(Channel(cname, radicand))
        known_names.add(cname)

    # --- divisors ---
    div_doc = doc.get("divisors")
    _require(isinstance(div_doc, list) and div_doc, "/divisors", "nonempty list required")
    divisors: list[Divisor] = []
    s = len(channels)
    for i, dv in enumerate(div_doc):
        _require(isinstance(dv, dict), f"/divisors/{i}", "object required")
        dname = dv.get("name")
        _require(isinstance(dname, str) and re.match(r"^[A-Za-z][A-Za-z0-9_]*$", dname) is not None,
                 f"/divisors/{i}/name", "identifier required")
        _require(dname not in {d.name for d in divisors}, f"/divisors/{i}/name", "duplicate divisor name")
        dgens = dv.get("gens")
        _require(isinstance(dgens, list) and dgens, f"/divisors/{i}/gens", "nonempty list required")
        for j, g in enumerate(dgens):
            _check_poly(g, known_names, f"/divisors/{i}/gens/{j}")
        row = dv.get("claimed_parity_row")
        _require(isinstance(row, list) and len(row) == s, f"/divisors/{i}/claimed_parity_row",
                 f"must have length s={s} (one entry per channel)")
        for j, x in enumerate(row):
            _require(x in (0, 1), f"/divisors/{i}/claimed_parity_row/{j}", "entries are 0 or 1")
        dtype = dv.get("type")
        _require(dtype in DIVISOR_TYPES, f"/divisors/{i}/type", f"must be one of {sorted(DIVISOR_TYPES)}")
        ebi = dv.get("expected_base_image")
        if ebi is not None:
            _check_poly(ebi, known_names, f"/divisors/{i}/expected_base_image")
        divisors.append(Divisor(dname, tuple(dgens), tuple(row), dtype, ebi, dv.get("note")))

    # --- generic denominator ---
    gd = doc.get("generic_denominator")
    if gd is not None:
        _check_poly(gd, known_names, "/generic_denominator")

    # --- slices ---
    slices: list[Slice] = []
    for i, sl in enumerate(doc.get("slices", [])):
        _require(isinstance(sl, dict), f"/slices/{i}", "object required")
        sname = sl.get("name")
        _require(isinstance(sname, str) and re.match(r"^[A-Za-z][A-Za-z0-9_]*$", sname) is not None,
                 f"/slices/{i}/name", "identifier required")
        assignments = sl.get("assignments")
        _require(isinstance(assignments, dict) and assignments, f"/slices/{i}/assignments",
                 "nonempty object required")
        for k, v in assignments.items():
            _require(k in var_set, f"/slices/{i}/assignments/{k}", "not a ring variable")
            _require(isinstance(v, int), f"/slices/{i}/assignments/{k}",
                     "slice values are integers (exact rational slices)")
        slices.append(Slice(sname, dict(assignments)))

    base_cycle_data = tuple(doc.get("base_cycle_data", []))

    return ProblemSpec(
        name=name, ring=ring, base_cover=base_cover, channels=tuple(channels),
        divisors=tuple(divisors), generic_denominator=gd, slices=tuple(slices),
        base_cycle_data=base_cycle_data, raw=doc,
    )


def load(path: str) -> ProblemSpec:
    with open(path) as f:
        return validate(json.load(f))


def _expand_tokens(expr: str, bindings: dict[str, str]) -> str:
    """Replace channel-name tokens with their (parenthesized) expansions.

    After expansion every identifier in the string is a ring variable, so the
    generated Macaulay2 never depends on symbol-assignment order.
    """
    def repl(match: re.Match) -> str:
        tok = match.group(0)
        return f"({bindings[tok]})" if tok in bindings else tok

    return TOKEN_RE.sub(repl, expr)


def channel_expansions(ps: ProblemSpec) -> dict[str, str]:
    """Map channel name -> radicand expressed purely in ring variables."""
    bindings: dict[str, str] = {}
    for ch in ps.channels:
        expanded = _expand_tokens(ch.radicand, bindings)
        if ch.name not in ps.ring.variables:
            bindings[ch.name] = expanded
    return {ch.name: _expand_tokens(ch.radicand, bindings) for ch in ps.channels}


def expand_poly(ps: ProblemSpec, expr: str) -> str:
    """Expand any spec polynomial string down to ring variables."""
    bindings = {name: exp for name, exp in channel_expansions(ps).items()
                if name not in ps.ring.variables}
    return _expand_tokens(expr, bindings)
