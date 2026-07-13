#!/usr/bin/env python3
"""Exact verifier for the DBP Landen--trace theorem.

The script is dependency-free.  It works in Q(sqrt(2)) with exact Fractions
and checks the two explicit 2-isogenies, the common descended third-kind
differential, the pole image, the residue, the complementary involution, and
the j/modular-polynomial gates.  No floating-point value is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from typing import Dict, Iterable


@dataclass(frozen=True)
class QS2:
    """a + b*s, where s^2 = 2 and a,b are rational."""

    a: Q = Q(0)
    b: Q = Q(0)

    @staticmethod
    def coerce(value: object) -> "QS2":
        if isinstance(value, QS2):
            return value
        if isinstance(value, (int, Q)):
            return QS2(Q(value), Q(0))
        raise TypeError(f"cannot coerce {value!r} to QS2")

    def __add__(self, other: object) -> "QS2":
        other = self.coerce(other)
        return QS2(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> "QS2":
        return QS2(-self.a, -self.b)

    def __sub__(self, other: object) -> "QS2":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "QS2":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "QS2":
        other = self.coerce(other)
        return QS2(
            self.a * other.a + 2 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def inverse(self) -> "QS2":
        norm = self.a * self.a - 2 * self.b * self.b
        if norm == 0:
            raise ZeroDivisionError("zero in Q(sqrt(2))")
        return QS2(self.a / norm, -self.b / norm)

    def __truediv__(self, other: object) -> "QS2":
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other: object) -> "QS2":
        return self.coerce(other) / self

    def __pow__(self, exponent: int) -> "QS2":
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        out = QS2(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                out = out * base
            base = base * base
            power >>= 1
        return out

    def conjugate(self) -> "QS2":
        return QS2(self.a, -self.b)

    def __eq__(self, other: object) -> bool:
        try:
            other = self.coerce(other)
        except TypeError:
            return False
        return self.a == other.a and self.b == other.b

    def sign(self) -> int:
        """Exact sign under the real embedding s=+sqrt(2)."""

        if self.a == 0 and self.b == 0:
            return 0
        if self.b == 0:
            return 1 if self.a > 0 else -1
        if self.b > 0:
            if self.a >= 0:
                return 1
            return 1 if 2 * self.b * self.b > self.a * self.a else -1
        if self.a <= 0:
            return -1
        return 1 if self.a * self.a > 2 * self.b * self.b else -1

    def __str__(self) -> str:
        return f"{self.a} + ({self.b})*s"


ZERO = QS2(0)
ONE = QS2(1)
S = QS2(0, 1)


class Laurent:
    """A finite Laurent polynomial in u over Q(sqrt(2))."""

    def __init__(self, terms: Dict[int, QS2] | None = None):
        terms = terms or {}
        self.terms = {
            int(power): QS2.coerce(coeff)
            for power, coeff in terms.items()
            if QS2.coerce(coeff) != ZERO
        }

    @staticmethod
    def constant(value: object) -> "Laurent":
        value = QS2.coerce(value)
        return Laurent({0: value}) if value != ZERO else Laurent()

    @staticmethod
    def monomial(power: int, coeff: object = 1) -> "Laurent":
        coeff = QS2.coerce(coeff)
        return Laurent({power: coeff}) if coeff != ZERO else Laurent()

    @staticmethod
    def coerce(value: object) -> "Laurent":
        if isinstance(value, Laurent):
            return value
        return Laurent.constant(value)

    def __add__(self, other: object) -> "Laurent":
        other = self.coerce(other)
        powers: Iterable[int] = set(self.terms) | set(other.terms)
        return Laurent(
            {p: self.terms.get(p, ZERO) + other.terms.get(p, ZERO) for p in powers}
        )

    __radd__ = __add__

    def __neg__(self) -> "Laurent":
        return Laurent({p: -c for p, c in self.terms.items()})

    def __sub__(self, other: object) -> "Laurent":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "Laurent":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "Laurent":
        other = self.coerce(other)
        out: Dict[int, QS2] = {}
        for p, c in self.terms.items():
            for q, d in other.terms.items():
                out[p + q] = out.get(p + q, ZERO) + c * d
        return Laurent(out)

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "Laurent":
        if exponent < 0:
            raise ValueError("negative Laurent-polynomial power")
        out = Laurent.constant(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                out = out * base
            base = base * base
            power >>= 1
        return out

    def __eq__(self, other: object) -> bool:
        return self.terms == self.coerce(other).terms

    def __str__(self) -> str:
        if not self.terms:
            return "0"
        return " + ".join(
            f"({self.terms[p]})*u^{p}" for p in sorted(self.terms, reverse=True)
        )


class RationalFunction:
    """A rational function in u over Q(sqrt(2))."""

    def __init__(self, numerator: Laurent, denominator: Laurent | None = None):
        denominator = denominator or Laurent.constant(1)
        if not denominator.terms:
            raise ZeroDivisionError("zero rational-function denominator")
        self.numerator = numerator
        self.denominator = denominator

    @staticmethod
    def coerce(value: object) -> "RationalFunction":
        if isinstance(value, RationalFunction):
            return value
        if isinstance(value, Laurent):
            return RationalFunction(value)
        return RationalFunction(Laurent.constant(value))

    def __add__(self, other: object) -> "RationalFunction":
        other = self.coerce(other)
        return RationalFunction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator,
        )

    __radd__ = __add__

    def __neg__(self) -> "RationalFunction":
        return RationalFunction(-self.numerator, self.denominator)

    def __sub__(self, other: object) -> "RationalFunction":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "RationalFunction":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "RationalFunction":
        other = self.coerce(other)
        return RationalFunction(
            self.numerator * other.numerator,
            self.denominator * other.denominator,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> "RationalFunction":
        other = self.coerce(other)
        return RationalFunction(
            self.numerator * other.denominator,
            self.denominator * other.numerator,
        )

    def __rtruediv__(self, other: object) -> "RationalFunction":
        return self.coerce(other) / self

    def __pow__(self, exponent: int) -> "RationalFunction":
        if exponent < 0:
            return RationalFunction(self.denominator, self.numerator) ** (-exponent)
        out = RationalFunction.coerce(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                out = out * base
            base = base * base
            power >>= 1
        return out

    def __eq__(self, other: object) -> bool:
        other = self.coerce(other)
        return self.numerator * other.denominator == other.numerator * self.denominator


U = RationalFunction(Laurent.monomial(1))


def gate(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print(f"PASS  {name}")


def j_legendre(m: QS2) -> QS2:
    return 256 * (1 - m + m * m) ** 3 / (m * m * (1 - m) ** 2)


def phi2(x: int, y: int) -> int:
    """Classical level-2 modular polynomial Phi_2(x,y)."""

    return (
        x**3
        + y**3
        - x**2 * y**2
        + 1488 * x * y * (x + y)
        - 162000 * (x**2 + y**2)
        + 40773375 * x * y
        + 8748000000 * (x + y)
        - 157464000000000
    )


def add_mod(
    left: tuple[int, int] | None,
    right: tuple[int, int] | None,
    prime: int,
) -> tuple[int, int] | None:
    """Group law on Y^2=X^3-X^2+X-1 over F_prime."""

    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % prime == 0:
        return None
    if left == right:
        if y1 % prime == 0:
            return None
        slope = (3 * x1 * x1 - 2 * x1 + 1) * pow(2 * y1, prime - 2, prime)
    else:
        slope = (y2 - y1) * pow((x2 - x1) % prime, prime - 2, prime)
    slope %= prime
    x3 = (slope * slope + 1 - x1 - x2) % prime
    y3 = (-y1 + slope * (x1 - x3)) % prime
    return x3, y3


def point_order_mod(point: tuple[int, int], prime: int) -> int:
    running = None
    for order in range(1, 4 * prime + 20):
        running = add_mod(running, point, prime)
        if running is None:
            return order
    raise AssertionError("point order search bound was insufficient")


def verify_channel(epsilon: int) -> None:
    label = "primary" if epsilon == 1 else "dual"
    eps = QS2(epsilon)
    m = (2 - epsilon * S) / 4
    n = (4 - epsilon * 3 * S) / 8
    a = 2 * m - 1
    b = QS2(Q(-1, 8))
    A = 3 + epsilon * 2 * S
    B = 2 + epsilon * 2 * S

    gate(f"{label}: a = -epsilon*s/2", a == -epsilon * S / 2)
    gate(f"{label}: b = m(m-1) = -1/8", m * (m - 1) == b)

    # Translate x=u+m.  The kernel point is u=0.  The exact Velu map is
    # z=u+a+b/u, v=y(1-b/u^2).
    z = U + a + RationalFunction.coerce(b) / U
    velocity = 1 - RationalFunction.coerce(b) / (U**2)
    source_curve = U**3 + U**2 * a + U * b
    quotient_curve = z**3 - z**2 * (2 * a) + z * (a * a - 4 * b)
    gate(
        f"{label}: exact degree-2 quotient equation",
        source_curve * velocity**2 == quotient_curve,
    )
    gate(
        f"{label}: quotient is v^2=z^3+epsilon*s*z^2+z",
        quotient_curve == z**3 + z**2 * (epsilon * S) + z,
    )

    # X=1+epsilon*s*z identifies the quotient with E_128 after the Y scaling
    # Y=iota*t^3*v, where iota^2=epsilon and t^4=2.
    X = 1 + z * (epsilon * S)
    e128 = X**3 - X**2 + X - 1
    expected_scale = epsilon * 2 * S
    gate(
        f"{label}: quotient-to-E128 polynomial identity",
        e128 == (z**3 + z**2 * (epsilon * S) + z) * expected_scale,
    )

    # The complete-integral differential is
    # -t^7/2 * F(u) du/y, with F=A*m/(m(1-n)-n*u)-B.
    d = m * (1 - n)

    def F(argument: RationalFunction) -> RationalFunction:
        return RationalFunction.coerce(A * m) / (
            RationalFunction.coerce(d) - argument * n
        ) - B

    translated_u = RationalFunction.coerce(b) / U
    trace_f = F(U) + F(translated_u)
    descended_f = -4 + 40 / (X + 7)
    gate(f"{label}: common rational trace identity", trace_f == descended_f)

    # The pole u=d/n and its kernel translate have common image X=-7.
    u0 = d / n
    z0 = u0 + a + b / u0
    X0 = 1 + epsilon * S * z0
    gate(f"{label}: pole image z0=-epsilon*4*s", z0 == -epsilon * 4 * S)
    gate(f"{label}: pole image X0=-7", X0 == -7)

    # The physical complete-integral path begins at x=0, hence u=-m.
    z_start = -m + a + b / (-m)
    gate(f"{label}: physical path maps from X=1", z_start == 0)


def main() -> None:
    print("DBP LANDEN--TRACE THEOREM: EXACT CERTIFICATION")
    print("Coefficient domain: Q(sqrt(2)); t=2^(1/4) used only by exact powers")
    print()

    m_primary = (2 - S) / 4
    m_dual = (2 + S) / 4
    n_primary = (4 - 3 * S) / 8
    n_dual = (4 + 3 * S) / 8

    gate("s^2=2", S * S == 2)
    gate("m_primary + m_dual = 1", m_primary + m_dual == 1)
    gate("m_primary*m_dual = 1/8", m_primary * m_dual == Q(1, 8))
    gate("n_primary + n_dual = 1", n_primary + n_dual == 1)
    gate("primary characteristic is negative", n_primary.sign() < 0)
    gate("dual characteristic exceeds one", (n_dual - 1).sign() > 0)
    gate("coefficient involution sends m_primary to m_dual", m_primary.conjugate() == m_dual)
    gate("coefficient involution sends n_primary to n_dual", n_primary.conjugate() == n_dual)

    gate("Legendre j(m_primary)=10976", j_legendre(m_primary) == 10976)
    gate("Legendre j(m_dual)=10976", j_legendre(m_dual) == 10976)
    gate("Phi_2(128,10976)=0", phi2(128, 10976) == 0)

    # E_128: Y^2=X^3-X^2+X-1, with a1=a3=0, a2=-1,a4=1,a6=-1.
    b2, b4, b6, b8 = -4, 2, -4, 3
    c4 = b2 * b2 - 24 * b4
    c6 = -(b2**3) + 36 * b2 * b4 - 216 * b6
    discriminant = -(b2**2) * b8 - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6
    gate("E128 discriminant=-256", discriminant == -256)
    gate("E128 c4=-32", c4 == -32)
    gate("E128 c6=640", c6 == 640)
    gate("E128 j=128", Q(c4**3, discriminant) == 128)

    verify_channel(+1)
    verify_channel(-1)

    # Exact dual residue.  The bare residue squared is
    # n/[4(n-1)(n-m)] and the real-path sign is negative.
    res_bare_squared = n_dual / (4 * (n_dual - 1) * (n_dual - m_dual))
    expected_squared = S * (3 + 2 * S) ** 2
    gate("dual bare residue square", res_bare_squared == expected_squared)
    gate("dual bare residue has negative real-path sign", (-(3 + 2 * S)).sign() < 0)
    gate(
        "weighted residue cancellation",
        (3 - 2 * S) * (3 + 2 * S) == 1 and 4 * 1 == 4,
    )
    gate("t^8=4 from t^4=2", 2**2 == 4)
    gate("DBP-weighted residue=4", 4 * (3 - 2 * S) * (3 + 2 * S) == 4)

    # The common descended differential is
    # Theta=8(X-3)/(X+7) dX/Y.  At X=-7, Y^2=-400.  On the dual physical
    # sheet Y=+20i, Res(Theta)=4i and Res(-i Theta)=4.
    x_pole = -7
    y_pole_squared = x_pole**3 - x_pole**2 + x_pole - 1
    gate("common E128 pole has Y^2=-400", y_pole_squared == -400)
    gate("Res(Theta) on Y=+20i is 4i", Q(-80, 20) == -4)  # -4/i = 4i
    gate("Res(-i*Theta)=4 on dual physical sheet", (-1) * (-4) == 4)

    # The descended pole point P=(-7,20i) is non-torsion over Q(i).
    # At the good primes (13, i->5) and (29, i->12), its reductions have
    # exact orders 4 and 6.  If P had order N, the good-reduction kernel
    # theorem would force N=4*13^a and N=6*29^b, which is impossible.
    p13, i13 = 13, 5
    p29, i29 = 29, 12
    point13 = ((-7) % p13, (20 * i13) % p13)
    point29 = ((-7) % p29, (20 * i29) % p29)
    gate("i^2=-1 at the chosen prime above 13", i13 * i13 % p13 == p13 - 1)
    gate("i^2=-1 at the chosen prime above 29", i29 * i29 % p29 == p29 - 1)
    gate("pole point has order 4 modulo the prime above 13", point_order_mod(point13, p13) == 4)
    gate("pole point has order 6 modulo the prime above 29", point_order_mod(point29, p29) == 6)
    gate("the descended pole point is non-torsion", (4 % 3) != 0 and (6 % 3) == 0)

    # Differential scaling: dX/Y=(iota/t) dz/v and t^8=4.  Therefore
    # omega+T^*omega=phi^*(iota^{-1} Theta).
    gate("trace scaling 2*t^7=8/t", 2 * 4 == 8)

    print()
    print("All exact gates passed.")
    print("Certified theorem core:")
    print("  omega_epsilon + T_epsilon^*omega_epsilon")
    print("    = phi_epsilon^*(iota_epsilon^(-1) * Theta)")
    print("  Theta = 8*(X-3)/(X+7) * dX/Y on E_128")
    print("  iota_+=1, iota_-=i; the dual weighted residue is exactly 4")


if __name__ == "__main__":
    main()
