#!/usr/bin/env python3
"""Exact symbolic-function proof of the two LEAD7 transverse Laurent lemmas."""

import sympy as sp


def scalar_curvature(gdiag, coords):
    n = len(coords)
    g = sp.diag(*gdiag)
    ginv = sp.diag(*[1 / entry for entry in gdiag])
    gamma = [[[sp.Integer(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                gamma[a][b][c] = sp.cancel(sum(
                    ginv[a, d] * (
                        sp.diff(g[d, b], coords[c])
                        + sp.diff(g[d, c], coords[b])
                        - sp.diff(g[b, c], coords[d])
                    )
                    for d in range(n)
                ) / 2)
    ricci = [[sp.Integer(0)] * n for _ in range(n)]
    for b in range(n):
        for d in range(n):
            value = 0
            for a in range(n):
                value += sp.diff(gamma[a][b][d], coords[a]) - sp.diff(gamma[a][b][a], coords[d])
                for e in range(n):
                    value += gamma[a][a][e] * gamma[e][b][d] - gamma[a][d][e] * gamma[e][b][a]
            ricci[b][d] = value
    return sp.cancel(sum(ginv[b, b] * ricci[b][b] for b in range(n)))


passed = 0


def check(label, condition):
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


x, y, z = sp.symbols("x y z", real=True)
A2 = sp.Function("A2")(y, z)
A3 = sp.Function("A3")(y, z)
P0 = sp.Function("P0")(y, z)
P1 = sp.Function("P1")(y, z)
R0 = sp.Function("R0")(y, z)
R1 = sp.Function("R1")(y, z)

generic_metric = (
    A2 * x**2 + A3 * x**3,
    P0 + P1 * x,
    R0 + R1 * x,
)
generic_curvature = scalar_curvature(generic_metric, (x, y, z))
generic_lead = sp.cancel(sp.limit(x**3 * generic_curvature, x, 0))
generic_expected = sp.cancel((P1 / P0 + R1 / R0) / A2)
check("generic variable-transverse coefficient", sp.cancel(generic_lead - generic_expected) == 0)
check("generic y derivatives absent", not generic_lead.has(sp.Derivative))

B = sp.Function("B")(y, z)
B4 = sp.Function("B4")(y, z)
C1 = sp.Function("C1")(y, z)
C2 = sp.Function("C2")(y, z)
C10 = sp.Function("C10")(y, z)
C20 = sp.Function("C20")(y, z)

reflection_metric = (
    B * x**2 + B4 * x**4,
    C1 * x**-2 + C10,
    C2 * x**-2 + C20,
)
reflection_curvature = scalar_curvature(reflection_metric, (x, y, z))
reflection_lead = sp.cancel(sp.limit(x**4 * reflection_curvature, x, 0))
check("reflection variable-transverse coefficient", sp.cancel(reflection_lead + 14 / B) == 0)
check("reflection transverse derivatives absent", not reflection_lead.has(sp.Derivative))

print(f"LEAD7 variable-transverse Laurent audit: {passed} assertions passed")
