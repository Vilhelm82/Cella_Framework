#!/usr/bin/env python3
"""Exact scalar-curvature library for divisor-germ metrics.

All computations are exact (rational functions / symbolic).  No floats.
Metrics are sympy Matrices whose entries are expressions in the coordinates;
the divisor is {z = 0} with z the first coordinate unless stated otherwise.
"""
import sympy as sp


def scalar_curvature(g, coords):
    """Exact scalar curvature of metric g in coordinates coords.

    Sign convention: round unit two-sphere has R = +2 — matches
    LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0 (frozen ledger 1).
    """
    n = len(coords)
    ginv = g.inv()
    Gam = [[[None] * n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for i in range(n):
            for j in range(i, n):
                expr = 0
                for m in range(n):
                    expr += ginv[l, m] * (sp.diff(g[m, i], coords[j])
                                          + sp.diff(g[m, j], coords[i])
                                          - sp.diff(g[i, j], coords[m]))
                expr = sp.cancel(expr / 2)
                Gam[l][i][j] = Gam[l][j][i] = expr
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(i, n):
            expr = 0
            for l in range(n):
                expr += sp.diff(Gam[l][i][j], coords[l]) - sp.diff(Gam[l][i][l], coords[j])
                for m in range(n):
                    expr += Gam[l][l][m] * Gam[m][i][j] - Gam[l][j][m] * Gam[m][i][l]
            Ric[i, j] = Ric[j, i] = sp.cancel(expr)
    R = 0
    for i in range(n):
        for j in range(n):
            R += ginv[i, j] * Ric[i, j]
    return sp.cancel(sp.together(R))


def diagonal_scalar_curvature(entries, coords):
    """Exact scalar curvature of a DIAGONAL metric via the directional-channel
    formula (LOCAL_CURVATURE_CALCULUS_COMPLETE eq. 2.2-2.3):

        u_i = (1/2) log g_i,
        Q_j(u) = sum_{i != j} [d_j^2 u_i + (d_j u_i)^2 - (d_j u_j)(d_j u_i)]
                 + sum_{r<s, r,s != j} (d_j u_r)(d_j u_s),
        R = -2 sum_j Q_j / g_j.

    Far cheaper than the full tensor route for symbolic function coefficients.
    Cross-validated against scalar_curvature() (see Stage 6 gate C, check J0).
    """
    n = len(coords)
    du = [[sp.cancel(sp.diff(entries[i], coords[j]) / (2 * entries[i]))
           for j in range(n)] for i in range(n)]
    R = 0
    for j in range(n):
        Qj = 0
        for i in range(n):
            if i == j:
                continue
            Qj += sp.diff(du[i][j], coords[j]) + du[i][j]**2 - du[j][j] * du[i][j]
        for r in range(n):
            for s in range(r + 1, n):
                if r == j or s == j:
                    continue
                Qj += du[r][j] * du[s][j]
        R += Qj / entries[j]
    return sp.together(-2 * R)


def leading_laurent(expr, z, max_pole=12, max_van=12):
    """Exact leading Laurent term of expr at z=0: returns (order, coefficient)
    with expr = coeff * z^order * (1 + O(z)).  Works on rational expressions.
    Returns (None, 0) for identically zero."""
    e = sp.cancel(sp.together(expr))
    if e == 0:
        return None, sp.Integer(0)
    num, den = sp.fraction(e)
    num = sp.expand(num)
    den = sp.expand(den)
    onum = _poly_order(num, z)
    oden = _poly_order(den, z)
    order = onum - oden
    cnum = _poly_coeff(num, z, onum)
    cden = _poly_coeff(den, z, oden)
    return order, sp.cancel(cnum / cden)


def _poly_order(p, z):
    p = sp.expand(p)
    for k in range(0, 64):
        c = p.coeff(z, k)
        if sp.simplify(c) != 0:
            return k
    raise ValueError("no nonzero coefficient found through z^63")


def _poly_coeff(p, z, k):
    return sp.expand(p).coeff(z, k)
