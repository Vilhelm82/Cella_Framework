#!/usr/bin/env python3
"""Exact symbolic replay of the four CCE-5 local connection germs."""

import sympy as sp


m = sp.symbols("m")
M = sp.Matrix((
    (-1 / (2*m), -1 / (2*m*(m-1)), 0),
    (-1 / (2*m), 1 / (2*m), 0),
    (1 / (m*(m-1)), (4*m-1)/(2*m*(m-1)**2), -(2*m**2+2*m-1)/(2*m*(m-1)*(2*m-1))),
))

R0 = sp.Matrix(((-sp.Rational(1,2), sp.Rational(1,2), 0), (-sp.Rational(1,2), sp.Rational(1,2), 0), (-1, -sp.Rational(1,2), sp.Rational(1,2))))
Rh = sp.diag(0, 0, sp.Rational(1,2))
Rinf = sp.Matrix(((sp.Rational(1,2), 0, 0), (sp.Rational(1,2), -sp.Rational(1,2), 0), (0, 0, sp.Rational(1,2))))
Nm2 = sp.zeros(3); Nm2[2,1] = sp.Rational(3,2)
Nm1 = sp.Matrix(((0, -sp.Rational(1,2), 0), (0, 0, 0), (1, sp.Rational(1,2), -sp.Rational(3,2))))

passed = 0


def check(label, condition):
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


check("m=0 residue", M.applyfunc(lambda value: sp.limit(m*value, m, 0)) == R0)
check("m=1/2 residue", M.applyfunc(lambda value: sp.limit((m-sp.Rational(1,2))*value, m, sp.Rational(1,2))) == Rh)
check("infinity-chart residue", M.applyfunc(lambda value: -sp.limit(m*value, m, sp.oo)) == Rinf)
check("m=1 double-pole coefficient", M.applyfunc(lambda value: sp.limit((m-1)**2*value, m, 1)) == Nm2)
residue_one = (M - Nm2/(m-1)**2).applyfunc(lambda value: sp.limit((m-1)*value, m, 1))
check("m=1 residual simple-pole coefficient", residue_one == Nm1)
check("m=1 basis is non-logarithmic", Nm2 != sp.zeros(3) and Nm2**2 == sp.zeros(3))

print(f"CCE-5 four-puncture local-germ audit: {passed} assertions passed")
