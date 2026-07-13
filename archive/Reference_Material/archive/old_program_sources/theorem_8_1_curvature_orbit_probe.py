from fractions import Fraction as Q
from itertools import permutations


def channel_spectrum(g, H):
    g1,g2,g3 = g
    H11,H22,H33 = H[0][0],H[1][1],H[2][2]
    H12,H13,H23 = H[0][1],H[0][2],H[1][2]
    den = (g1*g1+g2*g2+g3*g3)**2
    Dc = (g1*g1*H23*H23 + g2*g2*H13*H13 + g3*g3*H12*H12
          - 2*g1*g2*H13*H23 - 2*g1*g3*H12*H23 - 2*g2*g3*H12*H13)
    Ds = -(g1*g1*H22*H33 + g2*g2*H11*H33 + g3*g3*H11*H22)
    Dm = 2*(g1*g2*H12*H33 + g1*g3*H13*H22 + g2*g3*H23*H11)
    kc,ks,ki = -Dc/den, -Ds/den, -Dm/den
    return (kc+ks+ki,kc,ks,ki)


def permute(g,H,p):
    gp = [g[i] for i in p]
    Hp = [[H[p[i]][p[j]] for j in range(3)] for i in range(3)]
    return gp,Hp


def passive_orbit(g,H):
    return [channel_spectrum(*permute(g,H,p)) for p in permutations(range(3))]


def graph_channels(alpha,beta,L,M,N):
    q = 1 + alpha*alpha + beta*beta
    kc = -M*M/(q*q)
    ks = L*N/(q*q)
    ki = Q(0)
    return (kc+ks+ki,kc,ks,ki)


def active_role_charts(a,b,A,B,C):
    # Returns six ordered role charts: (name, alpha, beta, L, M, N, channel spectrum)
    out = []
    # P | D,S
    out.append(("P|D,S", a,b,A,B,C, graph_channels(a,b,A,B,C)))
    # P | S,D
    out.append(("P|S,D", b,a,C,B,A, graph_channels(b,a,C,B,A)))
    # D | P,S
    alpha,beta = 1/a, -b/a
    L = -A/(a**3)
    M = (A*b-a*B)/(a**3)
    N = (-A*b*b+2*a*b*B-a*a*C)/(a**3)
    out.append(("D|P,S", alpha,beta,L,M,N, graph_channels(alpha,beta,L,M,N)))
    # D | S,P
    out.append(("D|S,P", beta,alpha,N,M,L, graph_channels(beta,alpha,N,M,L)))
    # S | D,P
    alpha,beta = -a/b, 1/b
    L = (-C*a*a+2*a*b*B-b*b*A)/(b**3)
    M = (C*a-b*B)/(b**3)
    N = -C/(b**3)
    out.append(("S|D,P", alpha,beta,L,M,N, graph_channels(alpha,beta,L,M,N)))
    # S | P,D
    out.append(("S|P,D", beta,alpha,N,M,L, graph_channels(beta,alpha,N,M,L)))
    return out


def explicit_output_spectra(a,b,A,B,C):
    q = 1+a*a+b*b
    K = (A*C-B*B)/(q*q)
    CP = (K, -B*B/(q*q), A*C/(q*q), Q(0))
    CD = (K,
          -((A*b-a*B)**2)/(a*a*q*q),
          A*(A*b*b-2*a*b*B+a*a*C)/(a*a*q*q),
          Q(0))
    CS = (K,
          -((C*a-b*B)**2)/(b*b*q*q),
          C*(C*a*a-2*a*b*B+b*b*A)/(b*b*q*q),
          Q(0))
    return CP,CD,CS


def run_checks():
    # Passive orbit is trivial for a generic implicit jet.
    g = [Q(2),Q(-3),Q(5)]
    H = [[Q(7),Q(11),Q(-13)],
         [Q(11),Q(17),Q(19)],
         [Q(-13),Q(19),Q(-23)]]
    po = passive_orbit(g,H)
    assert len(set(po)) == 1, po

    # Active role charts: six ordered charts collapse to three scalar spectra.
    a,b,A,B,C = Q(5),Q(7),Q(2),Q(3),Q(4)
    charts = active_role_charts(a,b,A,B,C)
    spectra = [c[-1] for c in charts]
    assert spectra[0] == spectra[1]
    assert spectra[2] == spectra[3]
    assert spectra[4] == spectra[5]
    assert len(set(spectra)) == 3
    assert (spectra[0],spectra[2],spectra[4]) == explicit_output_spectra(a,b,A,B,C)

    # Total curvature is unchanged across active role charts.
    totals = {s[0] for s in spectra}
    assert totals == {Q(-1,5625)}, totals

    print("PASS: passive curvature orbit is trivial under coordinate permutations")
    print("PASS: active graph-role spectra reduce 6 ordered charts to 3 output-role spectra")
    for name,alpha,beta,L,M,N,spec in charts:
        print(f"{name:6s} slopes=({alpha},{beta}) second=({L},{M},{N}) spectrum={spec}")


if __name__ == "__main__":
    run_checks()
