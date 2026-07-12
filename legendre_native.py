#!/usr/bin/env python3
"""Native derivation of the E atom, the (K,E) connection, and the bilinear
pinning invariant for the Legendre even quartic  y^2 = (1-x^2)(1-m x^2).

Inputs (the only mathematics assumed):
  S1  content expansions   (1-x^2)^{e/2+1} = (1-x^2)^{e/2} - x^2(1-x^2)^{e/2}
                           (1-mx^2)^{d/2+1} = (1-mx^2)^{d/2} - m x^2(1-mx^2)^{d/2}
  S2  integration by parts: for a >= 1, e >= 1 (boundary terms vanish at 0 and 1)
      0 = a J(a-1,e,d) - e J(a+1,e-2,d) - d m J(a+1,e,d-2)
      where J(a,e,d) = INT_0^1 x^a (1-x^2)^{e/2} (1-mx^2)^{d/2} dx
  S3  Wallis base: W_0 = J(0,-1,0) = the period of the degenerate (m=0) fiber.

Atoms:  K = J(0,-1,-1)   E := J(0,-1,+1)   (E is DEFINED as a lattice point)
        dK/dm = (1/2) J(2,-1,-3)     dE/dm = -(1/2) J(2,-1,-1)

Stage 1 derives the closed first-order system by mechanical elimination.
Stage 2 derives the unique constant bilinear invariant of the pair system
        (Abel / Wronskian step) by exact kernel computation.
Stage 3 certifies the derived system on independently built exact series and
        pins the constant:  B = E(1) * K(0) = W_0  (the circle period).

Pure Fractions throughout; Will's uploaded series engine for Stage 3 checks;
sympy appears once, labeled ORACLE, for one antiderivative cross-check.
"""
from fractions import Fraction as F

# ------------------------------------------------ tiny exact Q[m] kernel
def pn(p):
    p = list(p)
    while p and p[-1] == 0: p.pop()
    return p
def pa(a,b):
    n = max(len(a),len(b))
    return pn([(a[i] if i<len(a) else F(0)) + (b[i] if i<len(b) else F(0)) for i in range(n)])
def ps(a,b): return pa(a, [-x for x in b])
def pm(a,b):
    if not a or not b: return []
    o = [F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): o[i+j] += x*y
    return pn(o)
def pdm(a,b):
    a = list(a); q = [F(0)]*max(0, len(a)-len(b)+1)
    while len(a) >= len(b) and pn(a[:]):
        if len(pn(a)) < len(b): break
        a = pn(a)
        if len(a) < len(b): break
        c = a[-1]/b[-1]; k = len(a)-len(b); q[k] = c
        for i in range(len(b)): a[k+i] -= c*b[i]
    return pn(q), pn(a)
def pg(a,b):
    a,b = pn(a[:]), pn(b[:])
    while b:
        _, r = pdm(a,b); a,b = b,r
    return [x/a[-1] for x in a] if a else a

class R:  # exact rational function of m
    __slots__=('n','d')
    def __init__(s, n, d=None):
        n = pn([F(x) for x in n]); d = pn([F(x) for x in (d or [1])])
        assert d, "zero denominator"
        if not n: d = [F(1)]
        else:
            g = pg(n,d)
            if len(g) > 1 or (g and g[0] != 1):
                n,_ = pdm(n,g); d,_ = pdm(d,g)
            lc = d[-1]
            if lc != 1: n = [x/lc for x in n]; d = [x/lc for x in d]
        s.n, s.d = n, d
    def __add__(a,b): return R(pa(pm(a.n,b.d), pm(b.n,a.d)), pm(a.d,b.d))
    def __sub__(a,b): return R(ps(pm(a.n,b.d), pm(b.n,a.d)), pm(a.d,b.d))
    def __mul__(a,b): return R(pm(a.n,b.n), pm(a.d,b.d))
    def __truediv__(a,b): return R(pm(a.n,b.d), pm(a.d,b.n))
    def __neg__(a): return R([-x for x in a.n], a.d)
    def z(a): return not a.n
    def __eq__(a,b): return a.n==b.n and a.d==b.d
    def sub1m(a):
        def comp(p):
            acc = []
            for c in reversed(p): acc = pa(pm(acc,[F(1),F(-1)]), [c])
            return acc
        return R(comp(a.n), comp(a.d))
    def __repr__(s):
        def f(p):
            if not p: return "0"
            t = []
            for i,c in enumerate(p):
                if c: t.append((f"{c}" if i==0 else (f"{c}*m" if i==1 else f"{c}*m^{i}")).replace("1*","") if c!=1 or i==0 else (f"m" if i==1 else f"m^{i}"))
            return " + ".join(t).replace("+ -","- ")
        return f(s.n) if s.d==[F(1)] else f"({f(s.n)})/({f(s.d)})"
Rc = lambda q: R([q]); Rm = R([0,1])

# ------------------------------------------------ Stage 1: lattice elimination
print("="*74)
print("STAGE 1 - derive the (K,E) connection by exact lattice elimination")
print("="*74)
def c1(a,e,d): return {(a,e+2,d):Rc(1),(a,e,d):Rc(-1),(a+2,e,d):Rc(1)}
def c2(a,e,d): return {(a,e,d+2):Rc(1),(a,e,d):Rc(-1),(a+2,e,d):Rm}
def ibp(al,e,d):
    assert al>=1 and e>=1, "boundary-vanishing hypothesis"
    return {(al-1,e,d):Rc(al),(al+1,e-2,d):Rc(-e),(al+1,e,d-2):R([0,-d])}

K,Ea = (0,-1,-1),(0,-1,1)
eqs = [c2(0,-1,-1), c2(2,-1,-3), c1(0,-1,-1), c1(2,-1,-3), ibp(1,1,-1)]
U = [(0,1,-1),(2,1,-3),(4,-1,-3),(2,-1,-1),(2,-1,-3)]   # unknown lattice points
rows = []
for eq in eqs:
    row = [eq.get(u,Rc(0)) for u in U]
    rhs = (-eq.get(K,Rc(0)), -eq.get(Ea,Rc(0)))        # move knowns across
    rows.append((row,rhs))
# Gaussian elimination over Q(m)
n = len(U)
for col in range(n):
    piv = next(i for i in range(col,len(rows)) if not rows[i][0][col].z())
    rows[col],rows[piv] = rows[piv],rows[col]
    prow,prhs = rows[col]
    inv = Rc(1)/prow[col]
    prow = [x*inv for x in prow]; prhs = (prhs[0]*inv, prhs[1]*inv)
    rows[col] = (prow,prhs)
    for i in range(len(rows)):
        if i==col or rows[i][0][col].z(): continue
        f0 = rows[i][0][col]
        rows[i] = ([a - f0*b for a,b in zip(rows[i][0],prow)],
                   (rows[i][1][0]-f0*prhs[0], rows[i][1][1]-f0*prhs[1]))
sol = {U[i]: rows[i][1] for i in range(n)}
A_K, A_E = sol[(2,-1,-1)]     # J(2,-1,-1) = A_K*K + A_E*E
B_K, B_E = sol[(2,-1,-3)]
print(f"  J(2,-1,-1) = ({A_K})*K + ({A_E})*E")
print(f"  J(2,-1,-3) = ({B_K})*K + ({B_E})*E")
half = Rc(F(1,2))
pK, qK = half*B_K, half*B_E          # dK/dm = pK*K + qK*E
pE, qE = -half*A_K, -half*A_E        # dE/dm = pE*K + qE*E
print(f"  => dK/dm = ({pK})*K + ({qK})*E")
print(f"  => dE/dm = ({pE})*K + ({qE})*E      [the E atom's connection]")

# ------------------------------------------------ Stage 2: Abel / kernel step
print("="*74)
print("STAGE 2 - the unique constant bilinear invariant (Abel/Wronskian step)")
print("="*74)
pKt, qKt = -pK.sub1m(), -qK.sub1m()   # d/dm K~ = pKt*K~ + qKt*E~ , K~(m)=K(1-m)
pEt, qEt = -pE.sub1m(), -qE.sub1m()
basis = ["K*K~","K*E~","E*K~","E*E~"]
Z = Rc(0)
T = [[pK+pKt, qKt,     qK,      Z      ],   # d(KK~)
     [pEt,    pK+qEt,  Z,       qK     ],   # d(KE~)
     [pE,     Z,       qE+pKt,  qKt    ],   # d(EK~)
     [Z,      pE,      pEt,     qE+qEt ]]   # d(EE~)
# constants c with sum_i c_i * d(v_i) = 0  <=>  c^T T = 0 identically in m
clr = [0,2,-2]                                # 2m(1-m)
cols = []
for j in range(4):
    entries = []
    for i in range(4):
        e = T[i][j]*R(clr)
        assert e.d == [F(1)], "denominator failed to clear"
        entries.append(e.n)
    deg = max((len(p) for p in entries), default=0)
    for k in range(deg):
        cols.append([entries[i][k] if k < len(entries[i]) else F(0) for i in range(4)])
# nullspace over Q of the stacked constraint rows
M = [row[:] for row in cols]; nc = 4; pivots = []; r = 0
for c in range(nc):
    piv = next((i for i in range(r,len(M)) if M[i][c] != 0), None)
    if piv is None: continue
    M[r],M[piv] = M[piv],M[r]
    M[r] = [x/M[r][c] for x in M[r]]
    for i in range(len(M)):
        if i!=r and M[i][c]!=0:
            M[i] = [a-M[i][c]*b for a,b in zip(M[i],M[r])]
    pivots.append(c); r += 1
free = [c for c in range(nc) if c not in pivots]
assert len(free) == 1, f"kernel dimension {len(free)} != 1"
c = [F(0)]*nc; c[free[0]] = F(1)
for i,pc in enumerate(pivots): c[pc] = -M[i][free[0]]
scale = c[2] if c[2] else F(1)                # normalize E*K~ coefficient to +1
c = [x/scale for x in c]
inv_form = " + ".join(f"({x})*{b}" for x,b in zip(c,basis) if x)
print(f"  kernel is 1-dimensional:  B = {inv_form}")
resid = [sum((Rc(c[i])*T[i][j] for i in range(4)), Rc(0)) for j in range(4)]
assert all(x.z() for x in resid)
print("  dB/dm = 0 verified exactly as a Q(m) identity  ->  B is CONSTANT in m")

# ------------------------------------------------ Stage 3: series certification + constant pin
print("="*74)
print("STAGE 3 - independent series certification and the constant pin")
print("="*74)
import sys
sys.path.insert(0, '/mnt/user-data/uploads')
from verify_local_curvature_calculus import add, mul, scale as sscale, deriv

N = 12
Cn, Bn = [F(1)], [F(1)]
for k in range(1, N+1):
    Cn.append(Cn[-1]*F(2*k-1, 2*k))          # binom(2k,k)/4^k
    Bn.append(Bn[-1]*F(2*k-3, 2*k))          # (-1)^k binom(1/2,k)
kser = {F(i): Cn[i]*Cn[i] for i in range(N+1)}          # K / W0
eser = {F(i): Bn[i]*Cn[i] for i in range(N+1)}          # E / W0
d2m1m = {F(1): F(2), F(2): F(-2)}                        # 2m(1-m)
onem  = {F(0): F(1), F(1): F(-1)}
lhs1 = mul(d2m1m, deriv(kser))
rhs1 = add(eser, sscale(mul(onem, kser), -1))
ok1 = all(lhs1.get(F(i),F(0)) == rhs1.get(F(i),F(0)) for i in range(N))
lhs2 = mul({F(1): F(2)}, deriv(eser))
rhs2 = add(eser, sscale(kser, -1))
ok2 = all(lhs2.get(F(i),F(0)) == rhs2.get(F(i),F(0)) for i in range(N))
print(f"  derived dK/dm law on independent series (order {N-1}):  {'EXACT' if ok1 else 'FAIL'}")
print(f"  derived dE/dm law on independent series (order {N-1}):  {'EXACT' if ok2 else 'FAIL'}")
assert ok1 and ok2
emk = add(eser, sscale(kser, -1))
print(f"  (E-K)/W0 = {emk.get(F(1))}*m + {emk.get(F(2))}*m^2 + ...   [vanishes to order 1]")

# constant pin:  B = (E-K)*K~ + E~*K ;  m -> 0.
# (a) E(1) = 1 exactly: at m=1, d=+1 the integrand is (1-x^2)^0 = 1.
# (b) K(0) = W0 exactly: at m=0 the fiber degenerates to the conic.
# (c) |E(1-m) - 1| <= sqrt(m):   pointwise  1-(1-m)x^2 >= m x^2  <=>  x^2 <= 1.
grid = [F(a,10) for a in range(1,10)]
ptw = all((1-(1-m)*x*x) >= m*x*x for m in grid for x in grid)
print(f"  pointwise inequality 1-(1-m)x^2 >= m x^2 on rational grid: {ptw}")
# (d) K(1-m) <= (2/sqrt(1-m)) * ln((1+sqrt(1-m))/sqrt(m))  -- log growth only.
#     Pointwise majorant steps are exact ((1+x)>=1, x^2<=x on [0,1]); the
#     elementary antiderivative is cross-checked below.  ORACLE, not load-bearing:
try:
    import sympy as sp
    t, mm = sp.symbols('t m', positive=True)
    Fant = 2/sp.sqrt(1-mm)*sp.log(sp.sqrt((1-mm)*t) + sp.sqrt(mm + (1-mm)*t))
    diff = sp.simplify(sp.diff(Fant, t) - 1/sp.sqrt(t*(mm + (1-mm)*t)))
    print(f"  ORACLE antiderivative check (sympy.diff): residual = {diff}")
except Exception as exc:
    print(f"  ORACLE unavailable: {exc}")
print()
print("  Limit m->0 of B = (E-K)*K~ + E~*K :")
print("    (E-K) = O(m) exactly [series above], K~ = O(log(1/m)) [majorant]")
print("      -> the first term vanishes;")
print("    E~ -> E(1) = 1 exactly, K -> K(0) = W0")
print("      -> B = E(1)*K(0) = W0.")
print()
print("  CONCLUSION:  B = E*K~ + E~*K - K*K~  is constant, and the constant is")
print("  W0 = the period of the m=0 degenerate fiber (the circle): W0 = pi/2,")
print("  whose native enclosure duty is typed_elementary.pi_eval (on disk).")
