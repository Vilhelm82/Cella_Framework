"""
Exact-Q probe for Theorem 8.1 role-jet transposition.
Verifies the S3 group laws for first-, second-, and third-order local jets,
and pins the monomial role exponent / degree spectra.
"""
from fractions import Fraction as Q


def s1(j):
    a, b = j
    return (b, a)


def t1(j):
    a, b = j
    return (Q(1) / a, -b / a)


def s2(j):
    a, b, A, B, C = j
    return (b, a, C, B, A)


def t2(j):
    a, b, A, B, C = j
    return (
        Q(1) / a,
        -b / a,
        -A / a**3,
        (A * b - a * B) / a**3,
        (-A * b * b + 2 * a * b * B - a * a * C) / a**3,
    )


def s3(j):
    a, b, A, B, C, E, F, G, H = j
    return (b, a, C, B, A, H, G, F, E)


def t3(j):
    a, b, A, B, C, E, F, G, H = j
    return (
        Q(1) / a,
        -b / a,
        -A / a**3,
        (A * b - a * B) / a**3,
        (-A * b * b + 2 * a * b * B - a * a * C) / a**3,
        (3 * A * A - a * E) / a**5,
        (-3 * A * A * b + 3 * a * A * B + a * b * E - a * a * F) / a**5,
        (
            3 * A * A * b * b
            - 6 * a * A * B * b
            + a * a * A * C
            + 2 * a * a * B * B
            - a * b * b * E
            + 2 * a * a * b * F
            - a**3 * G
        )
        / a**5,
        (
            -3 * A * A * b**3
            + 9 * a * A * B * b * b
            - 3 * a * a * A * C * b
            - 6 * a * a * B * B * b
            + 3 * a**3 * B * C
            + a * b**3 * E
            - 3 * a * a * b * b * F
            + 3 * a**3 * b * G
            - a**4 * H
        )
        / a**5,
    )


def compose(f, g):
    return lambda x: f(g(x))


def assert_s3(j, s, t):
    assert s(s(j)) == j, ("s^2 failed", j, s(s(j)))
    assert t(t(j)) == j, ("t^2 failed", j, t(t(j)))
    st = compose(s, t)
    assert st(st(st(j))) == j, ("(st)^3 failed", j, st(st(st(j))))


def first_projective_invariants(a, b):
    e1 = Q(1) - a - b
    e2 = a * b - a - b
    e3 = a * b
    I1 = e1 * e2 / e3
    I2 = e1**3 / e3
    Delta = (a - b) ** 2 * (a + 1) ** 2 * (b + 1) ** 2
    return I1, I2, Delta


def exponent_orbit(m, n):
    # ordered six-chart multiset; duplicates are meaningful stabilizers
    return [
        (m, n),
        (n, m),
        (Q(1) / m, -n / m),
        (-n / m, Q(1) / m),
        (-m / n, Q(1) / n),
        (Q(1) / n, -m / n),
    ]


def degree_spectrum(m, n):
    return sorted([alpha + beta for alpha, beta in exponent_orbit(m, n)])


def main():
    j1 = (Q(4), Q(3))
    j2 = (Q(4), Q(3), Q(5, 2), Q(-7, 3), Q(11, 5))
    j3 = j2 + (Q(13, 7), Q(-17, 11), Q(19, 13), Q(-23, 17))

    assert_s3(j1, s1, t1)
    assert_s3(j2, s2, t2)
    assert_s3(j3, s3, t3)

    assert first_projective_invariants(Q(4), Q(3)) == (Q(-5, 2), Q(-18), Q(400))

    assert sorted(exponent_orbit(Q(1), Q(1))) == sorted([(Q(1), Q(1)), (Q(1), Q(1)), (Q(1), Q(-1)), (Q(-1), Q(1)), (Q(-1), Q(1)), (Q(1), Q(-1))])
    assert degree_spectrum(Q(1), Q(1)) == [Q(0), Q(0), Q(0), Q(0), Q(2), Q(2)]

    assert degree_spectrum(Q(2), Q(1)) == [Q(-1), Q(-1), Q(0), Q(0), Q(3), Q(3)]

    print("PASS: exact S3 role-jet group laws and power spectra verified")
    print("first_projective_invariants(a=4,b=3) =", first_projective_invariants(Q(4), Q(3)))
    print("exponent_orbit(m=2,n=1) =", exponent_orbit(Q(2), Q(1)))
    print("degree_spectrum(m=2,n=1) =", degree_spectrum(Q(2), Q(1)))


if __name__ == "__main__":
    main()
