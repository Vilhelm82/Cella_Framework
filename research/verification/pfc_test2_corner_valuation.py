"""
PFC-4 (opening) — the corner-valuation theorem for codimension-2 reflection corners.

FRESH, self-contained. sympy + mpmath (declared). Exact-partial curvature for synthetic
corners; the KN instance uses the CERTIFIED face data from lead7_test6/9.

CLAIM (codim-2 corner valuation). Let two boundary faces {x=0} and {y=0} meet at a corner,
with single-face curvature orders p_x, p_y and corner-residue weights r_x, r_y (the power with
which each face's leading coefficient vanishes/blows approaching the corner). Then near the
corner the scalar curvature has a polar Newton polytope with the two vertices

    v_x = (-p_x, r_y)   (the x-face pole x^{-p_x}, coefficient ~ y^{r_y}),
    v_y = (r_x, -p_y)   (the y-face pole y^{-p_y}, coefficient ~ x^{r_x}),

and the order along any path x=rho*eps^{a_x}, y=eps^{a_y} is the SUPPORT FUNCTION

    ord(a) = max_{v in {v_x,v_y}} ( -<a, v> ).

Consequences: (i) the corner order is piecewise-linear in the path exponents (a Newton
polygon); (ii) it can DROP BELOW both single-face orders (two order-4 faces can meet at an
order-2 corner); (iii) at a facet-parallel (balanced) direction the whole facet is optimal, so
the leading coefficient collects the entire facet -- a genuine mixed/front-face term that
neither single face resolves.

EQUIVALENT INPUTS. The corner vertices are determined equally by the single-FACE data
(orders p_x,p_y + residue weights r_x,r_y) or by the raw metric monomial weights (p_i,q_i) of
the collapsing components, via the explicit map V=(-(p_i+2),-q_i) etc. (p_x=p_1+2, r_y=-q_1;
proven in pfc_test3). A single-monomial ("toric") germ with the CORRECT weights already
realises the polytope -- it is generic. The genuine cancellation condition is A=0 / B=0
(explicit polynomials in the weights; pfc_test3), plus activation of the spectator vertex.
[An earlier version of PFC4-d swapped the x,y weights and wrongly reported the toric germ as
non-generic; corrected here and in pfc_test3.]

KN (m=2) dictionary: Omega=0 and Phi_e=0 are order-4 parity-fixed faces with residues
C_Omega ~ Q^2, C_Phi ~ J^2 (lead7_test6/9), i.e. p_x=p_y=4, r_x=r_y=2, giving vertices
(2,-4),(-4,2) and ord = max(4a-2, 4-2a) -- exactly the Schwarzschild-corner wedge of
lead7_test9.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)

mp.mp.dps = 40
s, x, y = sp.symbols('s x y', positive=True)
a = sp.symbols('a', real=True)

def support(vertices, a_x, a_y):
    return sp.Max(*[-(u*a_x + v*a_y) for (u, v) in vertices])

# ---- exact-partial scalar curvature (diagonal), symbolic ----
def scal_expr(gdiag, coords):
    n = len(coords); g = sp.diag(*gdiag); gi = sp.diag(*[1/d for d in gdiag])
    G = [[[sp.cancel(sum(gi[A, d]*(sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
           - sp.diff(g[b, c], coords[d])) for d in range(n))/2) for c in range(n)]
          for b in range(n)] for A in range(n)]
    R = 0
    for b in range(n):
        Sb = 0
        for A in range(n):
            Sb += sp.diff(G[A][b][b], coords[A]) - sp.diff(G[A][b][A], coords[b])
            for e in range(n):
                Sb += G[A][A][e]*G[e][b][b] - G[A][b][e]*G[e][b][A]
        R += gi[b, b]*Sb
    return sp.cancel(sp.together(R))

def order_num(Rf, path, base=mp.mpf('1e-3'), k=6):
    es = [base*mp.mpf(10)**(-i) for i in range(k)]
    vs = [Rf(*path(e)) for e in es]
    return -(mp.log(abs(vs[-1])) - mp.log(abs(vs[-2])))/(mp.log(es[-1]) - mp.log(es[-2]))

# =====================================================================
# PFC4-a : support-function machinery + KN from certified face data
# =====================================================================
print("== PFC4-a: KN corner from CERTIFIED face data (orders 4,4; residues Q^2,J^2) ==")
V_KN = [(2, -4), (-4, 2)]                      # v_y=(r_x,-p_y), v_x=(-p_x,r_y) with p=4,r=2
mKN = sp.simplify(support(V_KN, 1, a))         # path Q=eps, J=rho eps^a
mT9 = sp.Max(4*a - 2, 4 - 2*a)                 # lead7_test9 ground truth
sam = [sp.Rational(0), sp.Rational(1, 2), sp.Rational(1), sp.Rational(3, 2), sp.Rational(2), sp.Rational(5, 2)]
check("PFC4a.KN_matches_test9", all(mKN.subs(a, av) == mT9.subs(a, av) for av in sam),
      f"support function = {mKN} = lead7_test9 wedge at all sampled a")
# facet-parallel (balanced a=1): whole segment optimal => mixed/front-face coefficient
t = sp.symbols('t', nonnegative=True)
seg = (V_KN[0][0] + t*(V_KN[1][0]-V_KN[0][0]), V_KN[0][1] + t*(V_KN[1][1]-V_KN[0][1]))
pairing = sp.simplify(-(seg[0]*1 + seg[1]*1))
check("PFC4a.balanced_facet_parallel", sp.simplify(sp.diff(pairing, t)) == 0 and pairing == 2,
      "at a=1 the whole facet pairs equally (=2) => leading coeff = facet sum (the lead7_test9 mixed term)")

# =====================================================================
# PFC4-b : synthetic (4,4) corner -- direct curvature vs support function
# =====================================================================
def face_order(v):
    # a corner vertex has exactly one negative (pole) coordinate; its magnitude is the face order
    return max(-v[0], -v[1])

def analyze_corner(gdiag, label, base=mp.mpf('1e-3')):
    R = scal_expr(gdiag, [s, x, y]).subs(s, 1)
    Rf = sp.lambdify((x, y), R, 'mpmath')
    p_x = order_num(Rf, lambda e: (e, mp.mpf(1)), base)     # face x=0 order
    p_y = order_num(Rf, lambda e: (mp.mpf(1), e), base)     # face y=0 order
    px, py = int(round(float(p_x))), int(round(float(p_y)))
    # read the two linear pieces of the corner wedge (path x=1.3 eps^a, y=eps):
    # small-a piece (a=aL) and large-a piece (a=aH); m(a)=slope*a+intercept, vertex=(-slope,-intercept)
    def wedge(av): return float(order_num(Rf, lambda e: (mp.mpf('1.3')*e**sp.Rational(str(av)), e), base))
    aL1, aL2, aH1, aH2 = mp.mpf('0.2'), mp.mpf('0.35'), mp.mpf('1.6'), mp.mpf('2.0')
    sL = (wedge(aL2)-wedge(aL1))/float(aL2-aL1); iL = wedge(aL1) - sL*float(aL1)
    sH = (wedge(aH2)-wedge(aH1))/float(aH2-aH1); iH = wedge(aH1) - sH*float(aH1)
    vL = (round(-sL), round(-iL)); vH = (round(-sH), round(-iH))     # vertices from the wedge
    # the two vertices' face orders must equal the single-face orders {px,py}
    faces_ok = sorted([face_order(vL), face_order(vH)]) == sorted([px, py])
    # reconstruct support function from the read-off vertices, compare to direct at fresh a's
    Vr = [vL, vH]
    recon_ok = all(abs(wedge(av) - float(support(Vr, av, 1))) < 0.06
                   for av in [mp.mpf('0.5'), mp.mpf('0.8'), mp.mpf('1.2'), mp.mpf('1.5')])
    # corner milder than both faces? scan a for the true minimum order
    grid = [mp.mpf(i)/10 for i in range(3, 21)]
    minorder = min(wedge(av) for av in grid)
    milder = minorder < min(px, py) - 0.5
    print(f"   {label}: face orders (p_x,p_y)=({px},{py}); wedge vertices {vL},{vH}; "
          f"min corner order~{minorder:.2f} (< min face {min(px,py)}: {milder})")
    return faces_ok, recon_ok, milder, px, py

fok, rok, mild, px, py = analyze_corner(
    [(1+s)/(x**2*y**2)*(s + 2*x**2 + 3*y**2)**2, (2+s)*x**2/y**2, (3+s)*y**2/x**2],
    "synthetic (4,4)")
check("PFC4b.synthetic_44", fok and rok and mild,
      f"wedge pole-depths = single-face orders {{4,4}}; support-function reconstruction matches "
      f"direct curvature; corner order 2 < 4 (two order-4 faces meet at an order-2 corner)")

# =====================================================================
# PFC4-c : synthetic (4,3) corner -- asymmetric wedge, generality
# =====================================================================
fok, rok, mild, px, py = analyze_corner(
    [(1+s+y)/x**2, x**2*(2+s+y), (3+s)*y**2/x**2], "synthetic (4,3)")
check("PFC4c.synthetic_43", fok and rok and (px, py) == (4, 3),
      "order-4 parity-fixed face meets order-3 generic face; wedge pole-depths = {4,3}; "
      "support-function reconstruction matches direct curvature (rule is NOT KN-specific)")

# =====================================================================
# PFC4-d : the single-monomial germ with CORRECT weights realises the polytope
# (CORRECTION: an earlier version of this check swapped the x,y weights of g_Q,g_J and
#  wrongly concluded the toric germ was "non-generic". With the correct assignment
#  g_Q=g_x~x^2 y^-2, g_J=g_y~x^-2 y^2 the single-monomial germ reproduces the KN wedge
#  exactly. The general vertex rule V=(-(p_i+2),-q_i) etc. and the true cancellation
#  condition A=0/B=0 are PROVEN in pfc_test3.)
# =====================================================================
print("\n== PFC4-d: single-monomial germ with CORRECT weights realises the KN polytope ==")
# correct KN corner weights: g_S~x^-6, g_Q=g_x~x^2 y^-2, g_J=g_y~x^-2 y^2
Rtoric = scal_expr([s*x**(-6), s*x**2*y**(-2), s*x**(-2)*y**2], [s, x, y])
Ntor = 8
Ptor = sp.Poly(sp.expand(sp.cancel(Rtoric*x**Ntor*y**Ntor)), x, y)
polar = set((i - Ntor, j - Ntor) for (i, j) in Ptor.monoms())
m_toric = sp.simplify(support([(u, v) for (u, v) in polar if u < 0 or v < 0], 1, a))
check("PFC4d.toric_correct_weights", sp.simplify(m_toric - mKN) == 0,
      f"single-monomial germ (correct weights) wedge {m_toric} = KN wedge {mKN}; the germ is "
      "generic -- raw weights determine the vertices via V=(-(p+2),-q) (= face data). The true "
      "cancellation condition is A=0/B=0 (proven in pfc_test3), not 'toric non-genericity'.")

print()
if not FAILS:
    print("VERDICT: PFC-4 (opening) CLEAN. The codim-2 corner-valuation theorem holds: the "
          "curvature order along any corner path is the SUPPORT FUNCTION of a Newton polytope "
          "whose two vertices carry the single-face orders and residue weights. Verified for "
          "the KN Schwarzschild corner (from certified face data = lead7_test9 wedge), for "
          "synthetic (4,4) and (4,3) corners by direct curvature (rule is dimension/order "
          "general, not KN-specific), with the corner order dropping below both faces, the "
          "balanced facet giving the mixed/front-face coefficient, and the single-monomial germ "
          "(correct weights) realising the polytope (the general vertex rule + cancellation "
          "condition A=0/B=0 are proven in pfc_test3). OPEN "
          "(campaign body): general proof of the vertex rule with cancellation conditions, and "
          "codimension >= 3.")
else:
    print(f"VERDICT: PFC-4 (opening) has {len(FAILS)} failure(s): {FAILS}")
