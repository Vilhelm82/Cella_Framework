"""
LEAD-7 TEST 8 — extremal gate, GRAPH-NORMALIZED (canonical) metric

Purpose
-------
Close the final extremal gate for the LEAD-7 Kerr-Newman DBP metric by proving

    L_ext := d_S log(G_JJ * G_QQ)|_{T=0} < 0

on the whole open extremal edge

    Q > 0,    S = pi*Q^2*t,    t > 1,
    J^2 = Q^4*(t^2 - 1)/4.

METRIC (canonical DBP graph normalization; supersedes
lead7_test8_extremal_gate_replacement.py). The chart norm is q_i = 1+|grad f_i|^2
= 1 + (4U + U_a^2 + U_b^2)/U_i^2 (the n=2 DBP norm, recert_gtd_dbp_n2.py line 24:
q0 = 1 + a^2 + b^2), so

    G_i = q_i^2 * U_i^6/(4U) * sum(1/D_{i,a}^2)
        = (U_i^2 + 4U + U_a^2 + U_b^2)^2 * U_i^2/(4U) * sum(1/D_{i,a}^2).

The "+U_i^2" (i.e. the "1+" in q_i) is the graph/ambient normalization, NOT an
accidental factor: the graph-norm metric reproduces the banked direct-curvature
coefficients EXACTLY (C_ext(20,1) = -0.0660176096 to 10 digits; Tests 6,7),
whereas the no-"1+" form gives -0.0656... The earlier _replacement.py certified
the no-"1+" metric and is therefore refuted as the LEAD-7 metric; this file is the
certificate for the correct one.

Edge samples are parameterised by S = pi*Q^2*t, t>1 (no off-edge negative-J^2
points), and the symbolic proof is done on the full dimensionless edge with
q=Q^2>0, S=p*q*t, J^2=q^2*(t^2-1)/4 (p represents pi). No Q=1 homogeneity
reduction is assumed.

The exact edge expression reduces to

    L_ext = - P(p,q,t) / D(p,q,t),

where D>0 on p=pi, q>0, t>1 and P is quadratic in q:

    P = A(p,t) q^2 + B(p,t) q + C(p,t).

The script proves:
  - D>0 by explicit factor certificates (nine coefficient-positive factors);
  - B>0 and C>0 by coefficient positivity after p^2=9+b and t=1+r;
  - A>0 via A = C0*p^a*t^b*(p^2 F(t)+G(t)) with F=(t-1)*t^3*(t+3)^3*Htilde(t),
    Htilde degree 5 > 0 on [1,oo) (Sturm), and 9F+G > 0 on [1,oo) (Sturm), so
    for pi^2>9:  p^2 F+G = (p^2-9)F + (9F+G) > 0.

Exit codes
----------
0  gate closed, or --numeric-only passed
1  numeric smoke/positivity failure
2  symbolic gate built but not certified
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import mpmath as mp
import sympy as sp


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

T0 = time.perf_counter()
FAILS: list[str] = []
WARNS: list[str] = []


def stamp() -> str:
    return f"{time.perf_counter() - T0:8.2f}s"


def say(msg: str) -> None:
    print(f"[{stamp()}] {msg}", flush=True)


def check(name: str, ok: bool, detail: str = "", fatal: bool = True) -> bool:
    head = "PASS" if ok else ("FAIL" if fatal else "WARN")
    print(f"{head}  {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not ok:
        (FAILS if fatal else WARNS).append(name)
    return ok


def tc(expr: sp.Expr) -> sp.Expr:
    return sp.cancel(sp.together(expr))


def safe_N(expr: sp.Expr, digits: int = 50) -> sp.Expr:
    return sp.N(expr, digits)


def factor_degrees(expr: sp.Expr) -> str:
    pieces = []
    for var, label in [(p, "p"), (q, "q"), (t, "t")]:
        try:
            deg = sp.Poly(expr, var).degree() if expr.has(var) else 0
        except Exception:
            deg = "?"
        pieces.append(f"deg_{label}={deg}")
    return ", ".join(pieces)


def eval_at_sample(expr: sp.Expr) -> sp.Expr:
    """Evaluate at the interior edge sample p=pi, q=1, t=2."""
    return safe_N(expr.subs({p: sp.pi, q: sp.Integer(1), t: sp.Integer(2)}), 80)


def strip_common_monomial(expr: sp.Expr, vars_: list[sp.Symbol]) -> tuple[sp.Expr, dict[sp.Symbol, int]]:
    """Strip common positive monomial powers. This preserves sign on the open domain."""
    expr = sp.expand(expr)
    try:
        P = sp.Poly(expr, *vars_)
    except sp.PolynomialError:
        return expr, {}
    monoms = P.monoms()
    if not monoms:
        return expr, {}
    mins = [min(m[i] for m in monoms) for i in range(len(vars_))]
    mon = sp.Integer(1)
    powers: dict[sp.Symbol, int] = {}
    for v, m in zip(vars_, mins):
        if m:
            mon *= v**m
            powers[v] = m
    if mon == 1:
        return expr, {}
    return sp.cancel(expr / mon), powers


def poly_coeffs_nonnegative(expr: sp.Expr, vars_: list[sp.Symbol]) -> tuple[bool, int, int, list[sp.Expr]]:
    expr = sp.expand(expr)
    try:
        P = sp.Poly(expr, *vars_)
    except sp.PolynomialError:
        return False, 0, -1, []
    coeffs = P.coeffs()
    bad = []
    for c in coeffs:
        c = sp.factor(c)
        if c.is_number:
            if c < 0:
                bad.append(c)
        else:
            if c.is_nonnegative is not True:
                bad.append(c)
    return len(bad) == 0 and len(coeffs) > 0, len(coeffs), len(bad), bad[:8]


def convert_even_powers_to_a(expr: sp.Expr) -> sp.Expr | None:
    """Convert polynomial in p with even p-powers to a polynomial in a=p^2."""
    expr = sp.expand(expr)
    try:
        Pp = sp.Poly(expr, p)
    except sp.PolynomialError:
        return None
    out = sp.Integer(0)
    for (pow_p,), coeff in Pp.terms():
        if pow_p % 2:
            return None
        out += coeff * a ** (pow_p // 2)
    return sp.expand(out)


def cert_positive_by_coeff_shift(expr: sp.Expr, name: str, *, dump_dir: Path | None = None) -> bool:
    """
    Prove expr>0 on p=pi, q>0, t>1 by coefficient positivity after
    p^2=9+b and t=1+r. This uses pi^2>9.
    """
    expr0 = sp.factor(expr)
    sample = eval_at_sample(expr0)
    if sample <= 0:
        check(name, False, f"sample nonpositive: {sample}", fatal=False)
        return False

    stripped, powers = strip_common_monomial(expr0, [p, q, t])
    if powers:
        say(f"{name}: stripped common positive monomial {powers}")

    # If an odd common p power remains, strip it; p>0 preserves sign.
    stripped, p_powers = strip_common_monomial(stripped, [p])
    if p_powers:
        say(f"{name}: stripped common positive p-power {p_powers}")

    even = convert_even_powers_to_a(stripped)
    if even is None:
        # Fallback: sometimes direct p,r,q coefficient positivity is enough.
        direct = sp.expand(stripped.subs(t, 1 + r))
        ok, n, nb, bad = poly_coeffs_nonnegative(direct, [p, q, r])
        if ok:
            check(name, True, f"coefficient-positive after t=1+r ({n} terms)")
            return True
        detail = f"odd p powers and direct shift failed: {nb} bad among {n}; first={bad}"
        if dump_dir:
            dump_dir.mkdir(parents=True, exist_ok=True)
            path = dump_dir / f"{name}.txt"
            path.write_text(str(sp.factor(stripped)), encoding="utf-8")
            detail += f"; dumped {path}"
        check(name, False, detail, fatal=False)
        return False

    shifted = sp.expand(even.subs({a: 9 + b, t: 1 + r}))
    ok, n, nb, bad = poly_coeffs_nonnegative(shifted, [q, r, b])
    if ok:
        check(name, True, f"coefficient-positive after p^2=9+b, t=1+r ({n} terms)")
        return True

    detail = f"p^2-shift has {nb} bad/unknown coeffs among {n}; first={bad}"
    if dump_dir:
        dump_dir.mkdir(parents=True, exist_ok=True)
        path = dump_dir / f"{name}.txt"
        path.write_text(str(sp.factor(stripped)), encoding="utf-8")
        detail += f"; dumped {path}"
    check(name, False, detail, fatal=False)
    return False


def sturm_positive_on_1_inf(poly: sp.Expr, name: str) -> bool:
    P = sp.Poly(sp.expand(poly), t)
    roots = sp.polys.polytools.count_roots(P, 1, sp.oo)
    value_at_1 = P.eval(1)
    value_at_2 = P.eval(2)
    ok = (roots == 0) and (value_at_1 > 0) and (value_at_2 > 0)
    return check(name, ok, f"deg={P.degree()}, roots(1,oo)={roots}, f(1)={value_at_1}, f(2)={value_at_2}")


# ---------------------------------------------------------------------------
# Symbols and exact even-in-J, even-in-Q construction
# ---------------------------------------------------------------------------

# S is entropy, K=J^2, q=Q^2, p represents pi.
S, K, q, p, t = sp.symbols("S K q p t", positive=True)
r, b, a = sp.symbols("r b a", positive=True)

say("Building exact even-in-J metric components in variables S, K=J^2, q=Q^2, p...")

U = S / (4 * p) + p * K / S + q / 2 + p * q**2 / (4 * S)
US = sp.diff(U, S)

# Squared first derivatives / chart objects. No sqrt(K), sqrt(q) needed.
UJ2 = 4 * p**2 * K / S**2
UQ2 = q * (S + p * q) ** 2 / S**2
UJJ = 2 * p / S
UQQ = (S + 3 * p * q) / S

# Mass-role coupling numerators D_{i,a}=U_ii U_a - U_i U_ia. Where the raw D has
# sqrt(K) or sqrt(q), use its square directly.
N_JS = tc(UJJ * US + 4 * p**2 * K / S**3)                       # UJJ*US - UJ*USJ
N_JQ2 = tc(4 * p**2 * UQ2 / S**2)                               # (UJJ*UQ)^2
N_QS = tc(UQQ * US + p * q**2 * (S + p * q) / S**3)              # UQQ*US - UQ*USQ
N_QJ2 = tc(UQQ**2 * UJ2)                                        # (UQQ*UJ)^2

qnum_J = tc(4 * U + US**2 + UQ2)
qnum_Q = tc(4 * U + US**2 + UJ2)

sumJ = tc(1 / N_JS**2 + 1 / N_JQ2)
sumQ = tc(1 / N_QS**2 + 1 / N_QJ2)

# Correct LEAD-7 components:
# G_i = (4U + U_a^2 + U_b^2)^2 * U_i^2/(4U) * sum(1/D^2)
GJ = tc((UJ2 + qnum_J)**2 * UJ2 / (4 * U) * sumJ)
GQ = tc((UQ2 + qnum_Q)**2 * UQ2 / (4 * U) * sumQ)
A2 = tc((4 * U + UJ2 + UQ2) ** 2 / (4 * U) * (1 / UJ2 + 1 / UQ2))

# Full open extremal edge substitution.
EDGE = {S: p * q * t, K: q**2 * (t**2 - 1) / 4}


def edge_dlog(expr: sp.Expr, label: str) -> sp.Expr:
    """Compute (d_S expr / expr)|edge, differentiating at fixed K,q before substitution."""
    say(f"Edge log-derivative for {label}...")
    out = tc(sp.diff(expr, S).subs(EDGE) / expr.subs(EDGE))
    say(f"  {label}: ops={sp.count_ops(out)}")
    return out


say("Building L_ext directly on the edge...")
L_terms = [
    2 * edge_dlog(UJ2 + qnum_J, "qnum_J(graph)"),
    edge_dlog(UJ2, "UJ2"),
    -edge_dlog(U, "U[J-part]"),
    edge_dlog(sumJ, "sumJ"),
    2 * edge_dlog(UQ2 + qnum_Q, "qnum_Q(graph)"),
    edge_dlog(UQ2, "UQ2"),
    -edge_dlog(U, "U[Q-part]"),
    edge_dlog(sumQ, "sumQ"),
]
Lext = tc(sum(L_terms))
say(f"Built L_ext. ops={sp.count_ops(Lext)}; {factor_degrees(sp.fraction(Lext)[0])}")

GJ_ext = tc(GJ.subs(EDGE))
GQ_ext = tc(GQ.subs(EDGE))
A2_ext = tc(A2.subs(EDGE))


# ---------------------------------------------------------------------------
# Numeric diagnostics
# ---------------------------------------------------------------------------

def build_numeric_functions():
    say("Lambdifying edge numeric functions...")
    Ln = sp.lambdify((p, q, t), Lext, "mpmath")
    A2n = sp.lambdify((p, q, t), A2_ext, "mpmath")
    GJn = sp.lambdify((p, q, t), GJ_ext, "mpmath")
    GQn = sp.lambdify((p, q, t), GQ_ext, "mpmath")
    return Ln, A2n, GJn, GQn


def run_G0_G1_G2(args: argparse.Namespace) -> None:
    Ln, A2n, GJn, GQn = build_numeric_functions()
    mp.mp.dps = args.dps

    print("[G0] numeric smoke test: sign of L_ext=d_S log(G_JJ G_QQ)|ext ...", flush=True)
    signs: set[int] = set()
    min_v = mp.inf
    max_v = -mp.inf

    q_count = 48 if args.dense else 28
    t_count = 72 if args.dense else 40

    # Work directly in q=Q^2 and t. Q in [0.05,6] means q in [0.0025,36].
    for qi in range(1, q_count + 1):
        Qv = mp.mpf("0.05") + (mp.mpf("6.0") - mp.mpf("0.05")) * qi / q_count
        qv = Qv**2
        for ti in range(1, t_count + 1):
            tv = mp.mpf("1.01") + (mp.mpf("11.0") - mp.mpf("1.01")) * ti / t_count
            vr = mp.re(Ln(mp.pi, qv, tv))
            signs.add(1 if vr > 0 else (-1 if vr < 0 else 0))
            min_v = min(min_v, vr)
            max_v = max(max_v, vr)

    # Near-corner and large-t probes.
    for Qv in [mp.mpf("0.05"), mp.mpf("0.5"), mp.mpf(1), mp.mpf(3), mp.mpf(6)]:
        qv = Qv**2
        for eps in ["1e-3", "1e-6", "1e-9"]:
            vr = mp.re(Ln(mp.pi, qv, 1 + mp.mpf(eps)))
            signs.add(1 if vr > 0 else (-1 if vr < 0 else 0))
            min_v = min(min_v, vr)
            max_v = max(max_v, vr)
        for tv in [mp.mpf(50), mp.mpf(5000)]:
            vr = mp.re(Ln(mp.pi, qv, tv))
            signs.add(1 if vr > 0 else (-1 if vr < 0 else 0))
            min_v = min(min_v, vr)
            max_v = max(max_v, vr)

    check(
        "G0.smoke_sign_fixed",
        signs == {-1},
        f"signs={signs}; min={mp.nstr(min_v, 8)}, max={mp.nstr(max_v, 8)}",
    )

    print("[G1] sampled positivity for sign identity ...", flush=True)
    posok = True
    pos_details = []
    for tv, Qv in [
        (mp.mpf("1.0001"), mp.mpf("0.05")),
        (mp.mpf("1.05"), mp.mpf("0.5")),
        (mp.mpf("1.5"), mp.mpf("1.0")),
        (mp.mpf("3.0"), mp.mpf("2.0")),
        (mp.mpf("20.0"), mp.mpf("0.25")),
        (mp.mpf("1000.0"), mp.mpf("6.0")),
    ]:
        qv = Qv**2
        vals = [
            ("A2", mp.re(A2n(mp.pi, qv, tv))),
            ("GJ", mp.re(GJn(mp.pi, qv, tv))),
            ("GQ", mp.re(GQn(mp.pi, qv, tv))),
        ]
        for label, val in vals:
            if not (val > 0):
                posok = False
                pos_details.append((label, Qv, tv, val))
    check(
        "G1.sampled_sign_identity_factors",
        posok,
        "A2, G_JJ, G_QQ positive at sampled open-edge points"
        if posok else f"bad={pos_details[:4]}",
    )

    print("[G2] scaling diagnostic only: no gate decision ...", flush=True)
    # The old script incorrectly treated this as a hard gate. We only report it.
    base_q = mp.mpf(1)
    base_t = mp.mpf(2)
    v0 = Ln(mp.pi, base_q, base_t)
    for ell in [mp.mpf(2), mp.mpf(3), mp.mpf(5)]:
        # Scaling Q -> ell Q means q -> ell^2 q at fixed t.
        ratio = Ln(mp.pi, ell**2 * base_q, base_t) / v0
        exponent = mp.log(abs(ratio)) / mp.log(ell)
        print(f"DIAG  G2.scale ell={ell}: ratio={mp.nstr(ratio, 12)}, effective exponent={mp.nstr(exponent, 12)}")


# ---------------------------------------------------------------------------
# Symbolic proof
# ---------------------------------------------------------------------------

def denominator_certificate(den: sp.Expr, dump_dir: Path) -> bool:
    print("[G3a] denominator positivity ...", flush=True)
    try:
        coeff, factors = sp.factor_list(den)
    except Exception as e:
        check("G3a.factor_denominator", False, f"{type(e).__name__}: {e}", fatal=False)
        return False

    print(f"      global coeff: {coeff}")
    ok = True
    if safe_N(coeff.subs({p: sp.pi}) if hasattr(coeff, "subs") else coeff) <= 0:
        ok = False
        check("G3a.global_coeff_positive", False, f"coeff={coeff}", fatal=False)

    for i, (fac, exp) in enumerate(factors, 1):
        fac = sp.factor(fac)
        sample = eval_at_sample(fac)
        fac_pos = fac if sample > 0 else -fac
        print(f"      factor {i}: exp={exp}, sample_sign={sp.sign(sample)}, {factor_degrees(fac_pos)}, ops={sp.count_ops(fac_pos)}")
        fi_ok = cert_positive_by_coeff_shift(fac_pos, f"G3a.den_factor_{i}", dump_dir=dump_dir)
        ok = ok and fi_ok
    return ok


def numerator_certificate(Ppos: sp.Expr, dump_dir: Path) -> bool:
    print("[G3b] numerator positivity: prove P=-num(L_ext)>0 ...", flush=True)

    Ppos, powers = strip_common_monomial(Ppos, [p, q, t])
    if powers:
        say(f"G3b stripped common positive monomial from P: {powers}")
    Ppos = sp.factor(Ppos)
    (dump_dir / "positive_core_P.txt").write_text(str(Ppos), encoding="utf-8")

    try:
        Pq = sp.Poly(sp.expand(Ppos), q)
    except Exception as e:
        check("G3b.collect_q", False, f"{type(e).__name__}: {e}", fatal=False)
        return False

    deg = Pq.degree()
    check("G3b.P_quadratic_in_q", deg == 2, f"degree in q = {deg}")
    if deg != 2:
        return False

    Acoef = sp.factor(Pq.coeff_monomial(q**2))
    Bcoef = sp.factor(Pq.coeff_monomial(q))
    Ccoef = sp.factor(Pq.coeff_monomial(1))

    (dump_dir / "P_coeff_A_q2.txt").write_text(str(Acoef), encoding="utf-8")
    (dump_dir / "P_coeff_B_q1.txt").write_text(str(Bcoef), encoding="utf-8")
    (dump_dir / "P_coeff_C_q0.txt").write_text(str(Ccoef), encoding="utf-8")

    # B and C are easy after p^2=9+b, t=1+r.
    okB = cert_positive_by_coeff_shift(Bcoef, "G3b.Bcoef_positive", dump_dir=dump_dir)
    okC = cert_positive_by_coeff_shift(Ccoef, "G3b.Ccoef_positive", dump_dir=dump_dir)

    # A needs the Sturm sub-proof from the hand analysis. GENERIC handling (no metric-
    # specific hardcoded factorisation): after stripping positive monomials in (p,t), the
    # core is even in p with p-powers {0,2}, i.e. Acore = C0*(p^2 F(t) + G(t)) with C0>0.
    # Positivity route: prove F>0 and 9F+G>0 on t>1, then for pi^2>9
    #   p^2 F + G = (p^2-9) F + (9F+G) > 0.
    print("[G3c] A coefficient Sturm certificate ...", flush=True)
    Acore, Amon = strip_common_monomial(sp.factor(Acoef), [p, t])
    if Amon:
        say(f"G3c stripped positive monomial {Amon} from A")
    Acore = sp.expand(Acore)
    Ap_poly = sp.Poly(Acore, p)
    ppows = sorted({m[0] for m in Ap_poly.monoms()})
    ok_even = check("G3c.A_even_p2", ppows == [0, 2] or ppows == [2] or ppows == [0],
                    f"A core p-powers = {ppows} (expect subset of {{0,2}})")
    if not ok_even:
        okA = False
    else:
        F = sp.expand(Ap_poly.coeff_monomial(p**2))     # coeff of p^2 (carries C0>0)
        G = sp.expand(Ap_poly.coeff_monomial(1))         # coeff of p^0
        # F>0 on (1,oo): factor out (t-1)^m; cofactor Fc>0 on [1,oo) => F>0 on (1,oo).
        m = 0
        Fc = sp.Poly(F, t)
        while Fc.degree() > 0 and sp.rem(Fc.as_expr(), t - 1, t) == 0:
            Fc = sp.Poly(sp.quo(Fc.as_expr(), t - 1, t), t)
            m += 1
        Fc = Fc.as_expr()
        say(f"G3c: (t-1) multiplicity in F = {m}; F = (t-1)^{m} * Fc, "
            f"Fc factored = {sp.factor(Fc)}")
        okFc = sturm_positive_on_1_inf(Fc, "G3c.Fcofactor_positive_1_inf")
        okF = check("G3c.F_positive_1_inf", okFc and (m % 2 == 1 or m == 0),
                    f"F=(t-1)^{m}*Fc>0 on (1,oo) since Fc>0 and (t-1)^{m}>0 for t>1")
        Llower = sp.expand(9 * F + G)
        okL = sturm_positive_on_1_inf(Llower, "G3c.Llower_9F_plus_G_positive")
        okA = ok_even and okF and okL
        check(
            "G3c.Acoef_positive",
            okA,
            "A = C0*p^a*t^b*(p^2 F+G); F>0, 9F+G>0 on t>1, pi^2>9 "
            "=> p^2 F+G=(p^2-9)F+(9F+G)>0",
        )

    # Since q>0, P=A q^2+B q+C > 0 if all three coefficients are positive.
    ok = okA and okB and okC
    check(
        "G3b.P_positive_on_edge",
        ok,
        "A,B,C positive and q>0" if ok else "some coefficient certificate failed",
        fatal=False,
    )
    return ok


def run_symbolic_gate(args: argparse.Namespace) -> bool:
    dump_dir = Path(args.dump_dir)
    dump_dir.mkdir(parents=True, exist_ok=True)

    print("[G3] factoring full-edge rational expression ...", flush=True)
    num, den = sp.fraction(Lext)
    num = sp.factor(num)
    den = sp.factor(den)

    # Normalize denominator positive at the sample.
    den_sample = eval_at_sample(den)
    if den_sample == 0:
        check("G3.den_sample_nonzero", False, "denominator vanishes at sample")
        return False
    if den_sample < 0:
        num = -num
        den = -den
        say("G3 normalized global sign so denominator sample is positive")

    num_sample = eval_at_sample(num)
    den_sample = eval_at_sample(den)
    L_sample = num_sample / den_sample
    say(f"G3 sample: sign(num)={sp.sign(num_sample)}, sign(den)={sp.sign(den_sample)}, L={safe_N(L_sample, 30)}")

    (dump_dir / "Lext.txt").write_text(str(Lext), encoding="utf-8")
    (dump_dir / "num_factor.txt").write_text(str(num), encoding="utf-8")
    (dump_dir / "den_factor.txt").write_text(str(den), encoding="utf-8")

    den_ok = denominator_certificate(den, dump_dir)

    if num_sample < 0:
        Ppos = sp.factor(-num)
    else:
        # This would contradict G0/sample expectation.
        check("G3.expected_negative_numerator", False, "num sample is not negative", fatal=False)
        Ppos = sp.factor(num)

    num_ok = numerator_certificate(Ppos, dump_dir)

    gate_ok = den_ok and num_ok and (num_sample < 0)
    check(
        "G3.symbolic_gate_closed",
        gate_ok,
        "L_ext=-P/D<0 on p=pi,q>0,t>1" if gate_ok else f"dumps in {dump_dir}",
        fatal=False,
    )
    return gate_ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="LEAD-7 Test 8 replacement extremal gate harness")
    ap.add_argument("--numeric-only", action="store_true", help="run G0/G1/G2 diagnostics only")
    ap.add_argument("--skip-numeric", action="store_true", help="skip numeric smoke tests and go straight to symbolic proof")
    ap.add_argument("--dense", action="store_true", help="use a denser numeric smoke grid")
    ap.add_argument("--dps", type=int, default=50, help="mpmath decimal precision for numeric tests")
    ap.add_argument("--dump-dir", default="lead7_test8_gate_dump", help="directory for symbolic dumps")
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    if not args.skip_numeric:
        run_G0_G1_G2(args)
        if FAILS:
            print(f"\nVERDICT: numeric stage failed ({', '.join(FAILS)}). Fix before symbolic proof.")
            return 1

    if args.numeric_only:
        print("\nVERDICT: numeric-only run passed. Symbolic proof not attempted.")
        return 0

    symbolic_ok = run_symbolic_gate(args)

    if symbolic_ok and not FAILS:
        print(
            "\nVERDICT: LEAD-7 TEST 8 CLEAN. "
            "The full-edge symbolic certificate proves "
            "L_ext=d_S log(G_JJ G_QQ)|ext < 0 for q=Q^2>0 and t=S/(pi Q^2)>1. "
            "Therefore C_ext<0 and the extremal pole is order 3 at every open point of T=0."
        )
        return 0

    print(
        "\nVERDICT: gate not fully closed by this harness. "
        f"Failures={FAILS}; warnings={WARNS}. "
        "If G0 passed, inspect the dumped numerator/denominator files for follow-up."
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
