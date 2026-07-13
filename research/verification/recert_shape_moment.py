"""
RC-7 — Shape moment recert (G1.2). FRESH, exact, zero-import.
Retrodiction target (CALC-30, [SR] I.6):  isotypic norms of DeltaA at n=4
    triv 147 / std 153 / (2,2) 24 / (2,1,1) 0 / sgn 0     Parseval Sigma = 324
Two independent routes for the character values (hardcoded table  vs  fresh
Murnaghan-Nakayama on beta-sets). Projectors verified idempotent/orthogonal/complete.
No float on any verdict path (Fraction only).
"""
from fractions import Fraction as F
from itertools import permutations, combinations

# ---------- S_4 ----------
G = list(permutations(range(4)))                      # 24 one-line perms, p[i]=image of i
def compose(p, q): return tuple(p[q[i]] for i in range(4))
def cyc_type(p):
    seen=[False]*4; t=[]
    for i in range(4):
        if not seen[i]:
            L=0; j=i
            while not seen[j]: seen[j]=True; j=p[j]; L+=1
            t.append(L)
    return tuple(sorted(t, reverse=True))
def sign(p):
    s=1; seen=[False]*4
    for i in range(4):
        if not seen[i]:
            L=0; j=i
            while not seen[j]: seen[j]=True; j=p[j]; L+=1
            if L%2==0: s=-s
    return s

CLASSES=[(1,1,1,1),(2,1,1),(2,2),(3,1),(4,)]          # partitions of 4
IRREPS =[(4,),(1,1,1,1),(3,1),(2,1,1),(2,2)]          # triv, sgn, std, std x sgn, (2,2)
NAME={(4,):"triv",(1,1,1,1):"sgn",(3,1):"std",(2,1,1):"(2,1,1)",(2,2):"(2,2)"}

# ---------- route A: textbook S_4 character table ----------
CHAR_TABLE={  # value on class  1^4, 21^2, 2^2, 31, 4
 (4,)      :{(1,1,1,1):1,(2,1,1): 1,(2,2): 1,(3,1): 1,(4,): 1},
 (1,1,1,1) :{(1,1,1,1):1,(2,1,1):-1,(2,2): 1,(3,1): 1,(4,):-1},
 (3,1)     :{(1,1,1,1):3,(2,1,1): 1,(2,2):-1,(3,1): 0,(4,):-1},
 (2,1,1)   :{(1,1,1,1):3,(2,1,1):-1,(2,2):-1,(3,1): 0,(4,): 1},
 (2,2)     :{(1,1,1,1):2,(2,1,1): 0,(2,2): 2,(3,1):-1,(4,): 0},
}
# ---------- route B: FRESH Murnaghan-Nakayama on beta-sets (independent referee) ----------
def beta_set(lam):
    s=len(lam); return frozenset(lam[i]+(s-1-i) for i in range(s))
def mn(beta, mu):
    if not mu: return 1
    k=mu[0]; rest=mu[1:]; tot=0
    for b in beta:
        if b>=k and (b-k) not in beta:
            legs=sum(1 for c in beta if (b-k)<c<b)
            tot+=(-1)**legs * mn(frozenset((beta-{b})|{b-k}), rest)
    return tot
def chi_mn(lam, mu): return mn(beta_set(lam), tuple(sorted(mu, reverse=True)))

# cross-check the two character routes agree
for lam in IRREPS:
    for mu in CLASSES:
        assert CHAR_TABLE[lam][mu]==chi_mn(lam,mu), (lam,mu)
CHI=CHAR_TABLE  # both agree; use it
DIM={lam:CHI[lam][(1,1,1,1)] for lam in IRREPS}
assert DIM=={(4,):1,(1,1,1,1):1,(3,1):3,(2,1,1):3,(2,2):2}

# ---------- the 12 flags (chart k, 2-subset of the other roles) ----------
FLAGS=[]
for k in range(4):
    others=[r for r in range(4) if r!=k]
    for jl in combinations(others,2):
        FLAGS.append((k, frozenset(jl)))
assert len(FLAGS)==12
IDX={f:i for i,f in enumerate(FLAGS)}
def act(p, f):
    k,jl=f; return (p[k], frozenset(p[x] for x in jl))
def rho_perm(p):                                       # 12-permutation as index list
    return [IDX[act(p,FLAGS[i])] for i in range(12)]

# ---------- flag permutation character + multiplicities ----------
def fixed_flags(p): return sum(1 for i in range(12) if rho_perm(p)[i]==i)
chi_flag={mu:0 for mu in CLASSES}
size   ={mu:0 for mu in CLASSES}
for p in G:
    mu=cyc_type(p); chi_flag[mu]+=fixed_flags(p); size[mu]+=1
for mu in CLASSES: chi_flag[mu]=F(chi_flag[mu], size[mu])   # value on the class (avg over class)
mult={}
for lam in IRREPS:
    m=sum(size[mu]*chi_flag[mu]*CHI[lam][mu] for mu in CLASSES)/F(24)
    assert m.denominator==1
    mult[lam]=int(m)

# ---------- isotypic projectors  P_lam = (d/|G|) sum_g chi(g) rho(g) ----------
def zeros(): return [[F(0)]*12 for _ in range(12)]
def proj(lam):
    P=zeros()
    for p in G:
        c=CHI[lam][cyc_type(p)]
        if c==0: continue
        r=rho_perm(p)
        for i in range(12): P[r[i]][i]+=F(c)            # rho(p)[r[i], i] = 1
    d=DIM[lam]
    return [[P[i][j]*F(d,24) for j in range(12)] for i in range(12)]
Pmats={lam:proj(lam) for lam in IRREPS}

def matmul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(12)) for j in range(12)] for i in range(12)]
def matvec(A,v): return [sum(A[i][k]*v[k] for k in range(12)) for i in range(12)]
def dot(a,b): return sum(a[i]*b[i] for i in range(12))

# certificate: idempotent, symmetric, complete
I12=[[F(1 if i==j else 0) for j in range(12)] for i in range(12)]
S=zeros()
for lam in IRREPS:
    P=Pmats[lam]
    assert matmul(P,P)==P, f"{NAME[lam]} not idempotent"
    assert all(P[i][j]==P[j][i] for i in range(12) for j in range(12)), f"{NAME[lam]} not symmetric"
    for i in range(12):
        for j in range(12): S[i][j]+=P[i][j]
assert S==I12, "projectors do not sum to I"

# ---------- the carrier  Lambda_{k,{j,l}} = -(H_jl - H_jk - H_kl + H_kk) ----------
def Hmat(d, o):            # d=(H11,H22,H33), o=(H12,H13,H23); role-0 row/col = 0
    H=[[0]*4 for _ in range(4)]
    H[1][1],H[2][2],H[3][3]=d
    H[1][2]=H[2][1]=o[0]; H[1][3]=H[3][1]=o[1]; H[2][3]=H[3][2]=o[2]
    return H
def carrier(H):
    out=[]
    for k in range(4):
        for (j,l) in combinations([r for r in range(4) if r!=k],2):
            out.append(-(H[j][l]-H[j][k]-H[k][l]+H[k][k]))
    return out
def Cmag(A):               # per-chart squared magnitude (the blind sensor)
    return [A[3*k]**2+A[3*k+1]**2+A[3*k+2]**2 for k in range(4)]

H0=Hmat((2,-1,3),(1,-2,1)); Hx=Hmat((-2,-2,-6),(2,-1,-1))
A0=carrier(H0); Ax=carrier(Hx)
A0_ref=[-1,2,-1,-1,-4,-4,2,2,5,-5,-2,-5]
Ax_ref=[-2,1,1,4,1,4,4,1,4,5,5,2]
assert A0==A0_ref, ("A(H0) mismatch", A0)
assert Ax==Ax_ref, ("A(H)  mismatch", Ax)
dA=[F(Ax[i]-A0[i]) for i in range(12)]

# ---------- ROUTE 1: character-projector isotypic norms ----------
norms={lam: dot(matvec(Pmats[lam],dA), dA) for lam in IRREPS}   # ||P dA||^2 = dA^T P dA
# ---------- ROUTE 2: elementary/independent ----------
total=dot(dA,dA)                                   # Parseval
triv_elem=F(sum(dA))**2/F(12)                      # projection on all-ones (no char theory)
C0,Cx=Cmag(A0),Cmag(Ax)                            # witness property (C)(H0)==(C)(H)

TARGET={"triv":147,"std":153,"(2,2)":24,"(2,1,1)":0,"sgn":0}

print("=== RC-7 shape moment — n=4 isotypic retrodiction ===")
print("carrier A(H0), A(H) reproduced from CALC-14 formula:", A0==A0_ref and Ax==Ax_ref)
print("witness property  (C)(H0)==(C)(H) =", C0, "==", Cx, ":", C0==Cx)
print("flag module M decomposition (multiplicities):",
      {NAME[l]:mult[l] for l in IRREPS}, " dim=",sum(DIM[l]*mult[l] for l in IRREPS))
print("DeltaA =", [int(x) for x in dA])
print()
print(f"{'irrep':8}{'route1 ||P.dA||^2':20}{'target':8}{'ok'}")
ok=True
for lam in IRREPS:
    v=norms[lam]; nm=NAME[lam]; t=TARGET[nm]
    good=(v==t); ok&=good
    print(f"{nm:8}{str(v):20}{t:<8}{good}")
print()
print("ROUTE 2 (independent):")
print(f"  Parseval  sum||.||^2 = {sum(norms.values())}   ||dA||^2 = {total}   agree: {sum(norms.values())==total==324}")
print(f"  triv via all-ones projection = (sum dA)^2/12 = {triv_elem}  (target 147, matches route1: {triv_elem==norms[(4,)]==147})")
print(f"  sgn & (2,1,1) forced 0 (dA in Im(L)=triv+std+(2,2)): {norms[(1,1,1,1)]==0 and norms[(2,1,1)]==0}")
ok &= (sum(norms.values())==324) and (triv_elem==147) and (C0==Cx)

# ---------- n>=5 dimension threshold (CALC-27 re-derivation) ----------
print()
print("=== n>=5 threshold: scalars resolve the shape iff  (n-1) >= dim S^(n-2,2) = n(n-3)/2 ===")
thr_ok=True
for n in range(3,8):
    dim_shape=n*(n-3)//2; nsig=n-1
    resolves = nsig>=dim_shape
    predicted = (n<=4)                              # n^2-5n+2<=0  <=>  n<=4
    thr_ok &= (resolves==predicted)
    print(f"  n={n}: dim_shape={dim_shape:2d}  #sigma_r={nsig}  scalars_resolve={resolves}  (n<=4:{predicted})  kernel>= {max(0,dim_shape-nsig)}")
print("  inequality n(n-3)/2 <= n-1  <=>  n^2-5n+2<=0  <=>  n<=4 :", thr_ok)
ok &= thr_ok

print()
print("RC-7:", "ALL PASS — quintuple retrodicted 147/153/24/0/0, Sigma=324; threshold n<=4" if ok else "FAIL")
import sys; sys.exit(0 if ok else 1)
