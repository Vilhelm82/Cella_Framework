#!/usr/bin/env python3
"""Exact finite-jet library for the active output-role cover.

A based jet of the rho-output chart of a regular constraint hypersurface
Sigma = {F(x_0,...,x_n) = 0} is stored as a SymPy polynomial expression

    f_rho  in  QQ[x_j : j != rho],  f_rho(0) = 0,

truncated at total degree r: x_rho = f_rho(x_{j != rho}) solves F = 0 with the
base point translated to the origin.

Active rechart T_(rho,sigma) : J^r_rho -> J^r_sigma is computed by exact formal
inversion (fixed-point iteration in the degree filtration), so every output is
rational in the input jet, localized at the first-order role denominator
a = d f_rho / d x_sigma (0)  — nonzero exactly on the regular role locus.

All arithmetic is exact (sympy Rational / polynomial rings). No floats.
"""
import sympy as sp


def truncate(expr, variables, r):
    """Drop all monomials of total degree > r (and the constant term)."""
    expr = sp.expand(expr)
    out = 0
    for term in sp.Add.make_args(expr):
        poly = term.as_poly(*variables)
        if poly is None:
            continue
        deg = sum(poly.degree_list())
        if 1 <= deg <= r:
            out += term
    return sp.expand(out)


def jet_coeff(jet, variables, exponents):
    """Exact Taylor coefficient of the monomial prod v^e (NOT the derivative)."""
    e = sp.expand(jet)
    for v, k in zip(variables, exponents):
        e = e.diff(v, k)
    e = e.subs({v: 0 for v in variables})
    from math import factorial
    denom = 1
    for k in exponents:
        denom *= factorial(k)
    return sp.together(sp.cancel(e / denom))


def rechart(jet_rho, vars_rho, rho, sigma, r):
    """Active rechart: from the r-jet of the rho-output chart, produce the
    r-jet of the sigma-output chart.

    vars_rho : dict {role_index: symbol} for every role j != rho (the base
               variables of chart rho).  Role rho itself gets a fresh symbol in
               the target chart.
    Returns (jet_sigma, vars_sigma).
    Raises ZeroDivisionError on the singular stratum a = 0 (typed refusal).
    """
    if sigma == rho:
        return sp.expand(jet_rho), dict(vars_rho)
    x_sigma = vars_rho[sigma]
    a = sp.diff(jet_rho, x_sigma).subs({v: 0 for v in vars_rho.values()})
    a = sp.cancel(a)
    if a == 0:
        raise ZeroDivisionError(
            f"singular stratum: role denominator d f_{rho}/d x_{sigma}(0) = 0")
    # target chart variables: x_rho becomes a base variable, x_sigma is output
    x_rho = sp.Symbol(f"x{rho}")
    vars_sigma = {j: v for j, v in vars_rho.items() if j != sigma}
    vars_sigma[rho] = x_rho
    tgt_vars = list(vars_sigma.values())
    # solve  x_rho = jet_rho( ..., u, ... )  for u = x_sigma as a series in
    # tgt_vars by exact fixed-point iteration in the degree filtration.
    others = {j: v for j, v in vars_rho.items() if j != sigma}
    u = truncate((x_rho - jet_rho.subs(x_sigma, 0).subs(
        {v: vars_sigma[j] for j, v in others.items()})) / a, tgt_vars, r)
    # NB the seed above is already the exact solution of the linear part.
    for _ in range(r):
        image = jet_rho.subs(x_sigma, u).subs(
            {v: vars_sigma[j] for j, v in others.items()})
        residual = truncate(sp.expand(image - x_rho), tgt_vars, r)
        if residual == 0:
            break
        u = truncate(sp.expand(u - residual / a), tgt_vars, r)
    # certify: F = x_rho - f_rho vanishes to order r on the solved graph
    image = jet_rho.subs(x_sigma, u).subs(
        {v: vars_sigma[j] for j, v in others.items()})
    residual = truncate(sp.expand(image - x_rho), tgt_vars, r)
    residual = sp.simplify(residual)
    assert residual == 0, f"formal inversion failed: residual {residual}"
    return sp.expand(u), vars_sigma


def generic_jet(n_roles, rho, r, prefix="c"):
    """Fully generic based r-jet of the rho-output chart with symbolic
    coefficients.  Returns (jet, vars_rho, coeffs)."""
    import itertools
    variables = {j: sp.Symbol(f"x{j}") for j in range(n_roles) if j != rho}
    idx = sorted(variables)
    coeffs = {}
    jet = 0
    for deg in range(1, r + 1):
        for combo in itertools.combinations_with_replacement(idx, deg):
            exps = tuple(combo.count(j) for j in idx)
            name = prefix + "_" + "".join(str(j) * combo.count(j) for j in idx
                                          for _ in (0,) if combo.count(j)) \
                   + "_" + "_".join(map(str, exps))
            c = sp.Symbol(f"{prefix}{''.join(map(str, combo))}")
            coeffs[combo] = c
            mono = 1
            for j in idx:
                mono *= variables[j] ** exps[idx.index(j)]
            jet += c * mono
    return sp.expand(jet), variables, coeffs


def random_rational_jet(n_roles, rho, r, rng, den=7):
    """Random exact-QQ based r-jet with all first-order coefficients nonzero."""
    import itertools
    variables = {j: sp.Symbol(f"x{j}") for j in range(n_roles) if j != rho}
    idx = sorted(variables)
    jet = 0
    for deg in range(1, r + 1):
        for combo in itertools.combinations_with_replacement(idx, deg):
            while True:
                num = rng.randint(-9, 9)
                if deg > 1 or num != 0:
                    break
            c = sp.Rational(num, rng.randint(1, den))
            mono = 1
            for j in combo:
                mono *= variables[j]
            jet += c * mono
    return sp.expand(jet), variables


def jets_equal(j1, v1, j2, v2, r):
    """Compare two jets over possibly different symbol objects for the same
    role indices."""
    sub = {v2[k]: v1[k] for k in v2}
    d = sp.expand(j1 - j2.subs(sub, simultaneous=True))
    d = sp.simplify(sp.together(d))
    return sp.expand(sp.cancel(d)) == 0
