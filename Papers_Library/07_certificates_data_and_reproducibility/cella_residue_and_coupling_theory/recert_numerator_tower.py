"""
RC-6 -- Numerator tower recert (G1.2). FRESH, exact, zero-import.
Sensors:  kc_r = e_r(P Hc P)  (numerator tower, Hc = offdiag(H) only),
          Kh   = e_{n-1}(P H P)  (full-Hessian denominator of the OG ratio),
          Dc   = -q * e_2(P Hc P)  (coupling form).
Dominance vs the OG ratio kc/Kh, proven three ways:
  (i)   coupling sensitivity : F1/F2 move kc (same as the ratio).
  (ii)  EXACT self-fault blindness : kc,Dc factor through Hc; S1/S2 hit only the
        diagonal -> offdiag(H+D)=offdiag(H) -> tower identically constant. The
        ratio FAILS (Kh reads the diagonal).  [PE.1 vs PE.4]
  (iii) scale invariance WITHOUT the quotient : P(tg)=P(g) exactly -> kc invariant.
Retrodiction anchor: PREREG_ENG2 PE.0 keystone kc=-2/7, Kh=-6/7, ratio=1/3, Dc=4.
No float on any verdict path (Fraction only).
"""
from fractions import Fraction as F
from itertools import combinations
import random

# ---------- exact linear algebra ----------
def matmul(A,B):
    n,m,p=len(A),len(B),len(B[0])
    return [[sum(A[i][k]*B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]
def det(A):
    M=[r[:] for r in A]; n=len(M); s=F(1)
    for c in range(n):
        piv=next((i for i in range(c,n) if M[i][c]!=0),None)
        if piv is None: return F(0)
        if piv!=c: M[c],M[piv]=M[piv],M[c]; s=-s
        for i in range(c+1,n):
            if M[i][c]!=0:
                f=M[i][c]/M[c][c]; M[i]=[a-f*b for a,b in zip(M[i],M[c])]
    for c in range(n): s*=M[c][c]
    return s
def e_r(A,r):                     # r-th elementary symmetric of eigenvalues = sum of principal r-minors
    n=len(A); tot=F(0)
    for S in combinations(range(n),r):
        sub=[[A[i][j] for j in S] for i in S]
        tot+=det(sub)
    return tot
def e_top(A): return e_r(A,len(A)-1)

def pairs(n): return [(i,j) for i in range(n) for j in range(i+1,n)]
def buildH(n,offd,diag):
    M=[[F(0)]*n for _ in range(n)]
    for idx,(i,j) in enumerate(pairs(n)): M[i][j]=M[j][i]=F(offd[idx])
    for i in range(n): M[i][i]=F(diag[i])
    return M
def offdiag(M):
    n=len(M); return [[M[i][j] if i!=j else F(0) for j in range(n)] for i in range(n)]
def Pmat(g):
    n=len(g); q=sum(F(x)*x for x in g)
    return [[(F(1) if i==j else F(0))-F(g[i])*g[j]/q for j in range(n)] for i in range(n)], q

def kc_tower(g,M):                # numerator tower e_r(P Hc P), r=2..n-1
    P,q=Pmat(g); A=matmul(matmul(P,offdiag(M)),P); n=len(M)
    return {r:e_r(A,r) for r in range(2,n)}, A, q
def Dc(g,M):
    P,q=Pmat(g); A=matmul(matmul(P,offdiag(M)),P)
    trA=sum(A[i][i] for i in range(len(A))); trA2=sum(A[i][j]*A[j][i] for i in range(len(A)) for j in range(len(A)))
    return -q*((trA*trA-trA2)/2)
def kc(g,M): P,q=Pmat(g); return e_top(matmul(matmul(P,offdiag(M)),P))
def Kh(g,M): P,q=Pmat(g); return e_top(matmul(matmul(P,M),P))

# ---------- fixtures (fixtures_eng2.json) ----------
FIX=[
 {"id":"e3key","n":3,"g":[3,1,2],"offd":[1,0,0],"diag":[2,0,2]},
 {"id":"e4a","n":4,"g":[3,1,2,5],"offd":[1,2,-1,3,1,-2],"diag":[2,-1,3,1]},
 {"id":"e4b","n":4,"g":[2,7,1,4],"offd":[5,-3,2,1,-1,4],"diag":[1,2,-2,3]},
 {"id":"e5a","n":5,"g":[3,1,2,5,7],"offd":[1,2,-1,3,1,-2,4,0,2,-3],"diag":[2,-1,3,1,-2]},
]
DC_F2=[1,-1,2,1,-2,1,3,-1,1,2]
DS_S2=[1,-2,1,3,-1]
def fault(n,offd,diag,fam,t):
    o=[F(x) for x in offd]; d=[F(x) for x in diag]; N=len(o)
    if fam=='F1': o[0]+=t
    elif fam=='F2': o=[a+t*b for a,b in zip(o,DC_F2[:N])]
    elif fam=='S1': d[0]+=t
    elif fam=='S2': d=[a+t*b for a,b in zip(d,DS_S2[:n])]
    return buildH(n,o,d)
def interp(pts):
    m=len(pts); co=[F(0)]*m
    for i,(xi,yi) in enumerate(pts):
        basis=[F(1)]; den=F(1)
        for j,(xj,_) in enumerate(pts):
            if j==i: continue
            den*=(xi-xj); nb=[F(0)]*(len(basis)+1)
            for k,c in enumerate(basis): nb[k]+=c*(-xj); nb[k+1]+=c
            basis=nb
        for k,c in enumerate(basis): co[k]+=yi*c/den
    while len(co)>1 and co[-1]==0: co.pop()
    return co

random.seed(7); ok=True
print("=== RC-6 numerator tower -- fault semantics ===\n")

# (0) PE.0 keystone retrodiction
f0=FIX[0]; M0=buildH(3,f0["offd"],f0["diag"])
a_kc,a_Kh,a_dc=kc(f0["g"],M0),Kh(f0["g"],M0),Dc(f0["g"],M0)
pe0=(a_kc==F(-2,7) and a_Kh==F(-6,7) and a_kc/a_Kh==F(1,3) and a_dc==4); ok&=pe0
print(f"PE.0 keystone: kc={a_kc} Kh={a_Kh} ratio={a_kc/a_Kh} Dc={a_dc}  target (-2/7,-6/7,1/3,4): {pe0}")
print(f"  [note] fixture 'anchors' kappa_c=-1/49 is the nu/W-prod channel (RC-4), a DIFFERENT")
print(f"         normalization from raw e_top(P Hc P)=-2/7 -- keystone label collision, not conflated.\n")

# (ii) EXACT self-fault blindness -- the identity + the fixture demonstration
print("(ii) EXACT self-fault blindness (identity: tower factors through offdiag(H)):")
ident_ok=True; const_ok=True; ratio_moves=False
for f in FIX:
    n,g=f["n"],f["g"]; H=buildH(n,f["offd"],f["diag"])
    base_tow,_,_=kc_tower(g,H); base_dc=Dc(g,H)
    # identity: ANY diagonal perturbation leaves offdiag, hence the whole tower, fixed
    for _ in range(3):
        D=[F(random.randint(-9,9)) for _ in range(n)]
        Hd=[[H[i][j]+(D[i] if i==j else 0) for j in range(n)] for i in range(n)]
        assert offdiag(Hd)==offdiag(H)
        tw,_,_=kc_tower(g,Hd)
        if tw!=base_tow or Dc(g,Hd)!=base_dc: ident_ok=False
    # fixture demonstration: S1,S2 -> tower constant polynomials; ratio derivative nonzero
    for fam in ('S1','S2'):
        pts_kc=[]; pts_Kh=[]; pts_dc=[]
        for tv in range(n+2):
            t=F(tv); M=fault(n,f["offd"],f["diag"],fam,t)
            pts_kc.append((t,kc(g,M))); pts_Kh.append((t,Kh(g,M))); pts_dc.append((t,Dc(g,M)))
        ckc,cKh,cdc=interp(pts_kc),interp(pts_Kh),interp(pts_dc)
        if len(ckc)!=1 or len(cdc)!=1: const_ok=False          # numerator EXACT-constant
        kc0,Kh0=ckc[0],cKh[0]; dkc=ckc[1] if len(ckc)>1 else F(0); dKh=cKh[1] if len(cKh)>1 else F(0)
        dratio=(dkc*Kh0-kc0*dKh)/(Kh0*Kh0)
        if dratio!=0: ratio_moves=True                          # OG literal clause FAILS
print(f"  identity  kc,Dc invariant under every diagonal perturbation: {ident_ok}")
print(f"  fixtures  kc(t),Dc(t) CONSTANT under S1,S2 (exact zero response): {const_ok}")
print(f"  ratio kc/Kh MOVES under self-faults (OG literal clause fails, PE.4): {ratio_moves}")
ok&= ident_ok and const_ok and ratio_moves

# (iii) scale invariance WITHOUT the quotient
print("\n(iii) scale invariance without the quotient  P(tg)=P(g):")
scale_ok=True
for f in FIX:
    n,g=f["n"],f["g"]; H=buildH(n,f["offd"],f["diag"]); base=kc(g,H)
    for t in (2,3,F(5,3)):
        g2=[F(x)*t for x in g]
        P2,_=Pmat(g2); P1,_=Pmat(g)
        if P2!=P1: scale_ok=False
        if kc(g2,H)!=base: scale_ok=False                       # numerator alone invariant, no denominator
print(f"  P(tg)==P(g) and kc(tg,H)==kc(g,H) exactly at t=2,3,5/3, every fixture: {scale_ok}")
ok&=scale_ok

# (i) coupling sensitivity -- F1,F2 move the numerator (same as the ratio)
print("\n(i) coupling sensitivity  F1,F2 move kc (and the ratio):")
coup_ok=True
for f in FIX:
    n,g=f["n"],f["g"]
    for fam in ('F1','F2'):
        pts_kc=[]; pts_Kh=[]
        for tv in range(n+2):
            t=F(tv); M=fault(n,f["offd"],f["diag"],fam,t)
            pts_kc.append((t,kc(g,M))); pts_Kh.append((t,Kh(g,M)))
        ckc,cKh=interp(pts_kc),interp(pts_Kh)
        kc0,Kh0=ckc[0],cKh[0]; dkc=ckc[1] if len(ckc)>1 else F(0); dKh=cKh[1] if len(cKh)>1 else F(0)
        dratio=(dkc*Kh0-kc0*dKh)/(Kh0*Kh0)
        moves=(len(ckc)>1) and (dratio!=0)
        if not moves: coup_ok=False
print(f"  kc non-constant and d/dt(kc/Kh)!=0 under F1,F2, every fixture: {coup_ok}")
ok&=coup_ok

print("\n=== DOMINANCE (numerator tower vs OG ratio) ===")
print("  self-fault:  numerator EXACT 0   |  ratio nonzero   -> numerator strictly dominates")
print("  coupling  :  numerator moves     |  ratio moves     -> same sensitivity")
print("  scaling   :  numerator invariant |  needs quotient  -> numerator needs no denominator")
print("\nRC-6:", "ALL PASS -- PE.0 retrodicted; blindness exact (identity+fixtures); scaling+sensitivity proven" if ok else "FAIL")
import sys; sys.exit(0 if ok else 1)
