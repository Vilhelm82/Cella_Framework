"""
RC-8 -- Localization support theorem recert (G1.2). FRESH, exact, zero-import.
Triangle channels (SHADOW_LAW Lemma 3):  Delta_S = T_S * nu^T (2I-J)_S nu,
  nu_e = W_e * h_e,  W_e = prod_{k not in e} g_k,  T_S = 1/prod_{m not in S} g_m^2.
Support theorem (PE.5):  a coupling fault on edge e* moves only nu_{e*}, so
  {S : d/dt Delta_S != 0 at t=0}  ==  {S : e* subset S}   exactly.
  (subset) direction is STRUCTURAL (Delta_S is free of nu_{e*} when e* not in S);
  (superset) direction is checked nonzero at the pinned n>=4 fixtures.
Two routes per triangle: 3-point exact interpolation vs closed-form derivative.
No float on any verdict path (Fraction only).
"""
from fractions import Fraction as F
from itertools import combinations

def pairs(n): return [(i,j) for i in range(n) for j in range(i+1,n)]
def Wvec(n,g):
    out=[]
    for (i,j) in pairs(n):
        w=F(1)
        for k in range(n):
            if k not in (i,j): w*=F(g[k])
        out.append(w)
    return out
def Tsub(n,g,S):
    d=F(1)
    for m in range(n):
        if m not in S: d*=F(g[m])*F(g[m])
    return F(1)/d
def delta_S(n,g,offd,S):                       # T_S * nu^T (2I-J)_S nu
    prs=pairs(n); idx={p:k for k,p in enumerate(prs)}; W=Wvec(n,g)
    nu=[F(offd[e])*W[e] for e in range(len(prs))]
    es=[idx[p] for p in combinations(S,2)]
    loc=sum(nu[a]*nu[a] for a in es)-sum(nu[a]*nu[b] for a in es for b in es if a!=b)
    return Tsub(n,g,S)*loc
def interp_lin(pts):                           # linear coeff of exact interpolant
    m=len(pts); co=[F(0)]*m
    for i,(xi,yi) in enumerate(pts):
        basis=[F(1)]; den=F(1)
        for j,(xj,_) in enumerate(pts):
            if j==i: continue
            den*=(xi-xj); nb=[F(0)]*(len(basis)+1)
            for k,c in enumerate(basis): nb[k]+=c*(-xj); nb[k+1]+=c
            basis=nb
        for k,c in enumerate(basis): co[k]+=yi*c/den
    return co[1] if len(co)>1 else F(0)

def dDeltaS_interp(n,g,offd,S,estar):          # route 1: interpolate Delta_S(t)
    e0=pairs(n).index(estar)
    pts=[]
    for tv in (F(0),F(1),F(2)):
        o=[F(x) for x in offd]; o[e0]+=tv
        pts.append((tv, delta_S(n,g,o,S)))
    return interp_lin(pts)
def dDeltaS_closed(n,g,offd,S,estar):          # route 2: closed form
    prs=pairs(n); idx={p:k for k,p in enumerate(prs)}; W=Wvec(n,g)
    e0=idx[estar]; es=[idx[p] for p in combinations(S,2)]
    if e0 not in es: return F(0)                # STRUCTURAL: Delta_S free of nu_{e*}
    nu=[F(offd[e])*W[e] for e in range(len(prs))]
    return 2*Tsub(n,g,S)*W[e0]*(nu[e0]-sum(nu[a] for a in es if a!=e0))

FIX=[
 {"id":"e4a","n":4,"g":[3,1,2,5],"offd":[1,2,-1,3,1,-2]},
 {"id":"e4b","n":4,"g":[2,7,1,4],"offd":[5,-3,2,1,-1,4]},
 {"id":"e5a","n":5,"g":[3,1,2,5,7],"offd":[1,2,-1,3,1,-2,4,0,2,-3]},
]

print("=== RC-8 localization support theorem: {S: dDelta_S/dt != 0} == {S: e* subset S} ===\n")
ok=True; routes_agree=True
for estar in [(0,1),(1,2),(0,2)]:              # PE.5 edge + moved-support family
    print(f"-- fault edge e* = {estar} --")
    for f in FIX:
        n,g,offd=f["n"],f["g"],f["offd"]
        moved=set(); want=set()
        for S in combinations(range(n),3):
            d1=dDeltaS_interp(n,g,offd,S,estar); d2=dDeltaS_closed(n,g,offd,S,estar)
            if d1!=d2: routes_agree=False
            if d1!=0: moved.add(S)
            if set(estar)<=set(S): want.add(S)
        law=(moved==want)
        # superset direction: EVERY S >= e* actually nonzero (no accidental vanishing = no K-4)
        superset_nonzero=all(dDeltaS_closed(n,g,offd,S,estar)!=0 for S in combinations(range(n),3) if set(estar)<=set(S))
        ok&= law and superset_nonzero
        print(f"  {f['id']} n={n}: moved={sorted(moved)}  == {{S>=e*}}: {law}  superset all nonzero: {superset_nonzero}")
    print()
print("routes agree (interp == closed form) everywhere:", routes_agree); ok&=routes_agree

# subset direction is structural, state it as an identity check:
struct=all(dDeltaS_closed(f["n"],f["g"],f["offd"],S,(0,1))==0
           for f in FIX for S in combinations(range(f["n"]),3) if not {0,1}<=set(S))
print("subset direction structural (dDelta_S=0 whenever e* not subset S):", struct); ok&=struct

print("\nRC-8:", "ALL PASS -- support theorem holds on the covered class; moved-support family confirmed; K-4 silent" if ok else "FAIL")
import sys; sys.exit(0 if ok else 1)
