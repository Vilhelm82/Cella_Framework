"""Generation of standalone Macaulay2 scripts from a validated ProblemSpec.

Scripts inline the synthesized model (ring, incidence ideal, channels,
divisors) with every polynomial already expanded down to ring variables, so
they are rerunnable by hand with `M2 --script <file>`; the only external
dependency is WreathEngine.m2, loaded by absolute path.

Each mathematical check prints a fenced JSON result block via emitResult;
everything else in stdout is human-readable audit text.
"""

from __future__ import annotations

from pathlib import Path

from . import spec as spec_mod
from .spec import ProblemSpec

M2_DIR = Path(__file__).resolve().parent.parent / "m2"
LIB_PATH = M2_DIR / "WreathEngine.m2"

DEFAULT_ORD_BOUND = 8


def _ring_decl(ps: ProblemSpec, extra_var: str | None = None,
               extra_weight_expr: str | None = None) -> str:
    vars_ = ", ".join(ps.ring.variables)
    weights = ", ".join(str(w) for w in ps.ring.weights)
    if extra_var:
        vars_ += f", {extra_var}"
        weights_expr = f"append({{{weights}}}, {extra_weight_expr})"
    else:
        weights_expr = f"{{{weights}}}"
    return (f"QQ[{vars_}, Degrees => {weights_expr}, "
            f"MonomialOrder => {ps.ring.order}]")


def _header(ps: ProblemSpec, purpose: str) -> str:
    return (
        f"-- wreath-engine generated script: {purpose}\n"
        f"-- spec: {ps.name}   spec-hash: {ps.content_hash()}\n"
        f"-- group claim: {ps.base_cover.group.name} "
        f"(order {ps.base_cover.group.order}), "
        f"claimed by: {ps.base_cover.group.claimed_by}\n"
        f'load "{LIB_PATH}";\n'
    )


def _model_block(ps: ProblemSpec) -> str:
    ix = ", ".join(ps.base_cover.incidence_gens)
    sheets = ", ".join(ps.base_cover.sheet_vars)
    gden = spec_mod.expand_poly(ps, ps.generic_denominator) if ps.generic_denominator else "1"
    return (
        f"S = {_ring_decl(ps)};\n"
        f"IX = ideal({ix});\n"
        f"sheetVars = {{{sheets}}};\n"
        f"dCover = {ps.d};\n"
        f"expectedCodim = {ps.base_cover.expected_codim};\n"
        f"genericDenS = {gden};\n"
    )


def _structural_block(ps: ProblemSpec) -> str:
    lines = [
        "cIX = codim IX;",
        'emitResult {"kind" => "structural", "gate" => "codim_incidence", '
        '"pass" => (cIX == expectedCodim), "value" => cIX};',
        "sheetPositions = apply(sheetVars, v -> index v);",
        "Jrel = submatrix(jacobian IX, sheetPositions, toList(0..(numgens IX - 1)));",
        "ramDet = det Jrel;",
    ]
    if ps.base_cover.ramification_det_identity:
        ident = spec_mod.expand_poly(ps, ps.base_cover.ramification_det_identity)
        lines += [
            f"ramIdent = {ident};",
            "ramOK = ((ramDet - ramIdent) % IX == 0) or ((ramDet + ramIdent) % IX == 0);",
            'emitResult {"kind" => "structural", "gate" => "ramification_det_identity", '
            '"pass" => ramOK};',
        ]
    lines += [
        "IR = IX + ideal(ramDet);",
        "Ising = IX + minors(expectedCodim, jacobian IX);",
        "Q = S/IX;",
        "use S;",
    ]
    return "\n".join(lines) + "\n"


def _charpoly_block(ps: ProblemSpec, index: int, name: str, radicand: str,
                    kind: str = "channel") -> str:
    """Emit computation of the characteristic (minimal) polynomial of one
    radicand over the base, storing eChan{index}, c0Chan{index}, ceChan{index}
    as elements of S. kind == "primitive" adds the cover-degree gates."""
    sheets_t = ", ".join(ps.base_cover.sheet_vars)
    ix = ", ".join(ps.base_cover.incidence_gens)
    suffix = f"Chan{index}" if kind == "channel" else "Prim"
    ring_t = _ring_decl(ps, extra_var="Tnorm", extra_weight_expr=f"max(1, wtR{suffix})")
    lines = [
        f"-- characteristic polynomial of {kind} {name!r} over the base",
        "use S;",
        f"rS{suffix} = {radicand};",
        f"wtR{suffix} = (degree rS{suffix})#0;",
        f"ST{suffix} = {ring_t};",
        f"use ST{suffix};",
        f"IXT = ideal({ix});",
        f"rT = {radicand};",
        f"charIdeal = trim eliminate(IXT + ideal(Tnorm - rT), {{{sheets_t}}});",
        "charOK = (numgens charIdeal == 1);",
        f'emitResult {{"kind" => "charpoly", "name" => "{name}", '
        '"gate" => "charpoly_principal", "pass" => charOK, "value" => numgens charIdeal};',
        "if charOK then (",
        "    chiPoly = charIdeal_0;",
        f"    e{suffix} = degree(Tnorm, chiPoly);",
        f"    c0{suffix} = sub(sub(chiPoly, Tnorm => 0), S);",
        f"    ce{suffix} = sub(((coefficients(chiPoly, Variables => {{Tnorm}}))#1)_(0,0), S);",
        f"    divOK = (e{suffix} > 0 and dCover % e{suffix} == 0);",
        f'    emitResult {{"kind" => "charpoly", "name" => "{name}", '
        f'"gate" => "charpoly_degree_divides", "pass" => divOK, "value" => e{suffix}}};',
    ]
    if kind == "primitive":
        lines += [
            f'    emitResult {{"kind" => "structural", "gate" => "cover_degree", '
            f'"pass" => (e{suffix} == dCover), "value" => e{suffix}}};',
            "    facs = select(toList factor chiPoly, p -> (first degree p#0) > 0);",
            "    irredOK = (#facs == 1 and facs#0#1 == 1);",
            '    emitResult {"kind" => "structural", "gate" => "cover_irreducible", '
            '"pass" => irredOK, "value" => #facs};',
        ]
    lines += [
        "    );",
        "use S;",
    ]
    return "\n".join(lines) + "\n"


def _divisor_block(ps: ProblemSpec, div_index: int) -> str:
    dv = ps.divisors[div_index]
    gens = ", ".join(spec_mod.expand_poly(ps, g) for g in dv.gens)
    odd_channels = [i for i, b in enumerate(dv.claimed_parity_row) if b == 1]
    lines = [
        f"-- ============ divisor {dv.name} ({dv.type}) ============",
        "use S;",
        f"D0 = ideal({gens});",
        "P0 = D0 + IX;",
    ]
    if dv.type == "contact" and ps.generic_denominator:
        lines.append("P0 = saturate(P0, genericDenS);")
    lines += [
        "mps = minimalPrimes P0;",
        f'emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
        '"gate" => "prime_upstairs", "pass" => (#mps == 1), "value" => #mps};',
        "if #mps == 1 then (",
        "    P = mps#0;",
        f'    emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
        '"gate" => "not_in_ramification", "pass" => (not isSubset(IR, P))};',
        f'    emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
        '"gate" => "not_in_singular_locus", "pass" => (not isSubset(Ising, P))};',
    ]
    # base divisor: contact divisors are checked against the expected wall by
    # elimination; private divisors find their base factor among the factors
    # of the constant coefficients of odd-claimed channels.
    if dv.type == "contact":
        expected = spec_mod.expand_poly(ps, dv.expected_base_image) if dv.expected_base_image else None
        lines += [
            "    Ebase = trim eliminate(P, sheetVars);",
            "    basePrincipal = (numgens Ebase == 1);",
            f'    emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
            '"gate" => "base_image_principal", "pass" => basePrincipal, '
            '"value" => numgens Ebase};',
        ]
        if expected:
            lines += [
                f"    expectedWall = {expected};",
                "    wallOK = basePrincipal and (Ebase == trim ideal(expectedWall));",
                f'    emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
                '"gate" => "expected_base_image", "pass" => wallOK, '
                '"value" => toString Ebase};',
            ]
        lines += [
            "    baseFound = basePrincipal;",
            "    if baseFound then fbase = Ebase_0;",
        ]
    else:
        cand_scans = "\n".join(
            f"    if class c0Chan{i} =!= Symbol then "
            f"scan(select(toList factor c0Chan{i}, p -> (first degree p#0) > 0), "
            "p -> (f := p#0; if f % P == 0 then baseCands = append(baseCands, "
            "(1/(leadCoefficient f)) * f)));"
            for i in odd_channels
        )
        lines += [
            "    baseCands = {};",
            cand_scans,
            "    baseCands = unique baseCands;",
            "    baseFound = (#baseCands == 1);",
            f'    emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
            '"gate" => "base_divisor_found", "pass" => baseFound, '
            '"value" => #baseCands};',
            "    if baseFound then fbase = baseCands#0;",
        ]
    # per-channel gates
    lines += ["    Pbar = sub(P, Q);"]
    for i, ch in enumerate(ps.channels):
        claimed = dv.claimed_parity_row[i]
        lines += [
            f"    -- channel {ch.name} (claimed parity {claimed})",
            f"    rbar = sub(rSChan{i}, Q);",
            f'    emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
            f'"channel" => "{ch.name}", "gate" => "radicand_nonzero", '
            '"pass" => (rbar != 0)};',
            f"    mOrd{i} = ordAlongPrime(rbar, Pbar, {DEFAULT_ORD_BOUND});",
            f'    emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
            f'"channel" => "{ch.name}", "gate" => "on_sheet_parity", '
            f'"pass" => (mOrd{i} >= 0 and mOrd{i} % 2 == {claimed}), '
            f'"value" => mOrd{i}, "bound_hit" => (mOrd{i} < 0)}};',
            f"    vNorm{i} = if baseFound and class eChan{i} =!= Symbol then "
            f"(dCover // eChan{i}) * (multiplicityOf(c0Chan{i}, fbase) - "
            f"multiplicityOf(ceChan{i}, fbase)) else -999;",
            f'    emitResult {{"kind" => "gate", "divisor" => "{dv.name}", '
            f'"channel" => "{ch.name}", "gate" => "off_sheet_even", '
            f'"pass" => (vNorm{i} == mOrd{i} and mOrd{i} >= 0), '
            f'"value" => vNorm{i}}};',
        ]
    lines += [
        "    ) else (",
        f'    print "divisor {dv.name}: not prime upstairs; remaining gates skipped";',
        "    );",
    ]
    return "\n".join(lines) + "\n"


def generate_verify(ps: ProblemSpec) -> str:
    """The certified verification script: structural gates, channel norm data,
    and the per-divisor checklist of theorem section 5's geometric route."""
    parts = [
        _header(ps, "verify_valuation_matrix"),
        _model_block(ps),
        _structural_block(ps),
        _charpoly_block(ps, 0, ps.base_cover.sheet_vars[0],
                        ps.base_cover.sheet_vars[0], kind="primitive"),
    ]
    expansions = spec_mod.channel_expansions(ps)
    for i, ch in enumerate(ps.channels):
        parts.append(_charpoly_block(ps, i, ch.name, expansions[ch.name]))
    for i in range(len(ps.divisors)):
        parts.append(_divisor_block(ps, i))
    parts.append('print "wreath-engine verify script complete";\n')
    return "\n".join(parts)


def generate_realize_fast(ps: ProblemSpec) -> str:
    """Fast realization stages: contact walls, incidence table, slices."""
    expansions = spec_mod.channel_expansions(ps)
    parts = [
        _header(ps, "realize_branch_poset (fast stages)"),
        _model_block(ps),
        _structural_block(ps),
    ]
    # channel divisors upstairs
    chan_divs = []
    for i, ch in enumerate(ps.channels):
        parts.append(f"Chan{i} = IX + ideal({expansions[ch.name]});  -- channel {ch.name}\n")
        chan_divs.append((f"Chan{i}", ch.name))
    # contact walls
    for i, dv in enumerate(ps.divisors):
        gens = ", ".join(spec_mod.expand_poly(ps, g) for g in dv.gens)
        parts.append(f"Div{i} = IX + ideal({gens});  -- divisor {dv.name}\n")
        if dv.type == "contact" and dv.expected_base_image:
            expected = spec_mod.expand_poly(ps, dv.expected_base_image)
            parts.append(
                f"wallImage = trim eliminate(Div{i}, sheetVars);\n"
                f"wallOK = (wallImage == trim ideal({expected}));\n"
                f'emitResult {{"kind" => "poset", "stage" => "contact_wall", '
                f'"stratum" => "{dv.name}", "pass" => wallOK}};\n'
            )
    # incidence table
    strata = ['("IR", IR)']
    strata += [f'("{dv.name}", Div{i})' for i, dv in enumerate(ps.divisors)]
    strata += [f'("{name}", {var})' for var, name in chan_divs]
    for i, dv in enumerate(ps.divisors):
        for var, name in chan_divs:
            strata.append(f'("{dv.name}+{name}", Div{i} + {var})')
    for var, name in chan_divs:
        strata.append(f'("IR+{name}", IR + {var})')
    parts.append(
        "tbl = {" + ", ".join(strata) + "};\n"
        "scan(tbl, pr -> (\n"
        "    lbl := pr#0; I := pr#1;\n"
        "    c := codim I;\n"
        "    dg := degree I;\n"
        "    Icl := trim saturate(I, genericDenS);\n"
        '    emitResult {"kind" => "poset", "stage" => "incidence_table", '
        '"stratum" => lbl, "codim" => c, "codim_in_X" => (c - expectedCodim), '
        '"degree" => dg, "empty_generic" => (Icl == ideal(1_S))};\n'
        "    ));\n"
    )
    # slices
    for sl in ps.slices:
        assigns = ", ".join(f"{k}-({v})" for k, v in sl.assignments.items())
        parts.append(f"slice = ideal({assigns});  -- slice {sl.name}\n")
        parts.append(
            "branchSlice = trim eliminate(saturate(IR + slice, genericDenS), sheetVars);\n"
            f'emitResult {{"kind" => "poset", "stage" => "slice_branch_image", '
            f'"slice" => "{sl.name}", "value" => toString branchSlice}};\n'
        )
        for var, name in chan_divs:
            parts.append(
                f"chSlice = trim eliminate(saturate({var} + slice, genericDenS), sheetVars);\n"
                f'emitResult {{"kind" => "poset", "stage" => "slice_channel_image", '
                f'"slice" => "{sl.name}", "stratum" => "{name}", '
                f'"value" => toString chSlice}};\n'
            )
    parts.append('print "wreath-engine realize (fast) complete";\n')
    return "\n".join(parts)


def generate_realize_decomp(ps: ProblemSpec) -> str:
    """Slow realization stage: decomposition of each channel divisor upstairs."""
    expansions = spec_mod.channel_expansions(ps)
    parts = [
        _header(ps, "realize_branch_poset (decompositions; potentially long)"),
        _model_block(ps),
    ]
    for i, ch in enumerate(ps.channels):
        parts.append(
            f"Chan{i} = IX + ideal({expansions[ch.name]});\n"
            f"mp = minimalPrimes Chan{i};\n"
            f'emitResult {{"kind" => "poset", "stage" => "channel_min_primes", '
            f'"stratum" => "{ch.name}", "value" => #mp, '
            f'"degrees" => apply(mp, degree), "codims" => apply(mp, codim), '
            f'"primes" => apply(mp, p -> toString gens p)}};\n'
            f"pd = primaryDecomposition Chan{i};\n"
            f'emitResult {{"kind" => "poset", "stage" => "channel_primary_decomp", '
            f'"stratum" => "{ch.name}", "value" => #pd, '
            f'"is_prime_ideal" => (#pd == 1 and pd#0 == mp#0)}};\n'
        )
    parts.append('print "wreath-engine realize (decomp) complete";\n')
    return "\n".join(parts)


def generate_explore_parity(ps: ProblemSpec, divisor_gens: list[str],
                            saturate_generic: bool = False) -> str:
    """Exploratory (non-certifying) parity probe for a candidate divisor."""
    gens = ", ".join(spec_mod.expand_poly(ps, g) for g in divisor_gens)
    expansions = spec_mod.channel_expansions(ps)
    parts = [
        _header(ps, "suggest_parity_rows (EXPLORATORY - never certifies)"),
        _model_block(ps),
        "Q = S/IX;\nuse S;\n",
        f"P0 = ideal({gens}) + IX;\n",
    ]
    if saturate_generic:
        parts.append("P0 = saturate(P0, genericDenS);\n")
    parts.append(
        "mps = minimalPrimes P0;\n"
        'emitResult {"kind" => "explore", "gate" => "component_count", "value" => #mps};\n'
        "scan(#mps, k -> (\n"
        "    P := mps#k;\n"
        "    Pbar := sub(P, Q);\n"
    )
    ords = []
    for i, ch in enumerate(ps.channels):
        parts.append(
            f"    ord{i} := ordAlongPrime(sub({expansions[ch.name]}, Q), Pbar, "
            f"{DEFAULT_ORD_BOUND});\n"
        )
        ords.append(f"ord{i}")
    parts.append(
        '    emitResult {"kind" => "explore", "component" => k, '
        '"codim" => codim P, "degree" => degree P, '
        f'"orders" => {{{", ".join(ords)}}}, '
        f'"parity_row" => {{{", ".join(f"(if {o} >= 0 then {o} % 2 else -1)" for o in ords)}}}}};\n'
        "    ));\n"
        'print "wreath-engine exploration complete";\n'
    )
    return "".join(parts)
