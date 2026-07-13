from fractions import Fraction as Q


def kg_three_channel(g, H):
    g1, g2, g3 = g
    H11, H22, H33 = H[0][0], H[1][1], H[2][2]
    H12, H13, H23 = H[0][1], H[0][2], H[1][2]
    den = (g1*g1 + g2*g2 + g3*g3) ** 2
    Dc = (g1*g1*H23*H23 + g2*g2*H13*H13 + g3*g3*H12*H12
          - 2*g1*g2*H13*H23 - 2*g1*g3*H12*H23 - 2*g2*g3*H12*H13)
    Ds = -(g1*g1*H22*H33 + g2*g2*H11*H33 + g3*g3*H11*H22)
    Dm =  2*(g1*g2*H12*H33 + g1*g3*H13*H22 + g2*g3*H11*H23)
    kc, ks, ki = -Dc/den, -Ds/den, -Dm/den
    return kc + ks + ki, kc, ks, ki


def gauge_H(g, H, a):
    return [[H[i][j] + g[i]*a[j] + a[i]*g[j] for j in range(3)] for i in range(3)]


def formula(u, v, w):
    kc = (12*u*v + 6*u*w + 18*v*w + 6*w - 1) / Q(49)
    ks = (12*u*v + 6*u*w + 3*u + 18*v*w + 13*v + 2*w + 1) / Q(49)
    ki = -(24*u*v + 12*u*w + 3*u + 36*v*w + 13*v + 8*w + 3) / Q(49)
    return kc + ks + ki, kc, ks, ki


def delta_kc_formula(u, v, w):
    return 6*(2*u*v + u*w + 3*v*w + w) / Q(49)


def main():
    g = [Q(3), Q(1), Q(2)]
    H = [[Q(2), Q(1), Q(0)],
         [Q(1), Q(0), Q(0)],
         [Q(0), Q(0), Q(2)]]
    base = kg_three_channel(g, H)
    assert base == (Q(-3,49), Q(-1,49), Q(1,49), Q(-3,49))

    gauges = [
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(1), Q(-2), Q(3)),
        (Q(-1,2), Q(5), Q(1)),
    ]
    expected = [
        (Q(-3,49), Q(-1,49), Q(4,49), Q(-6,49)),
        (Q(-3,49), Q(-1,49), Q(2,7), Q(-16,49)),
        (Q(-3,49), Q(-97,49), Q(-130,49), Q(32,7)),
        (Q(-3,49), Q(62,49), Q(247,98), Q(-377,98)),
    ]
    for a, exp in zip(gauges, expected):
        got = kg_three_channel(g, gauge_H(g,H,a))
        assert got == exp, (a, got, exp)
        assert got == formula(*a), (a, got, formula(*a))
        shifts = [got[i] - base[i] for i in range(4)]
        assert shifts[0] == 0
        assert sum(shifts[1:]) == 0

    # e1/e2 axes preserve kappa_c for arbitrary rational scale.
    for t in [Q(-3), Q(-1,2), Q(0), Q(7,5), Q(11)]:
        assert delta_kc_formula(t, Q(0), Q(0)) == 0
        assert delta_kc_formula(Q(0), t, Q(0)) == 0
        assert delta_kc_formula(Q(0), Q(0), t) == 6*t/Q(49)

    # kappa_c-preserving sheet: w = -2uv/(u+3v+1)
    for u, v in [(Q(1), Q(2)), (Q(-3), Q(4)), (Q(5,7), Q(-2,3))]:
        den = u + 3*v + 1
        if den != 0:
            w = -2*u*v/den
            assert delta_kc_formula(u, v, w) == 0

    print('PASS: keystone gauge-channel transport law verified exactly in Q')
    for a in gauges:
        print(a, formula(*a))


if __name__ == '__main__':
    main()
