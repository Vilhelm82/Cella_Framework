"""
Stage A -- per-sensor reference values on {keystone, sphere3, saddle, cylinder}, gated.
Numerator channel  kappa_2 = e_2(P Hc P)/q   (Hc = offdiag H)  -> must equal certified kc
Curvature          sigma_2 = e_2(P H  P)/q                      -> must equal certified K_G
Cross-route        kc+kint+ks == sigma_2 (gate_11 P3)
Cylinder           P-route computes (q!=0); O/fingerprint route refuses (g has a 0 comp)
All exact Fraction. Gates fire if the existing math is wrong.
"""
from fractions import Fraction as F
from itertools import combinations
def det(A):
    M=[r[:] for r in A]; n=len(M); s=F(1)
    for c in range(n):
        pv=next((i for i in range(c,n) if M[i][c]!=0),None)
        if pv is None: return F(0)
        if pv!=c: M[c],M[pv]=M[pv],M[c]; s=-s
        for i in range(c+1,n):
            if M[i][c]!=0:
                f=M[i][c]/M[c][c]; M[i]=[a-f*b for a,b in zip(M[i],M[c])]
    for c in range(n): s*=M[c][c]
    return s
def mm(A,B):
    n,m,p=len(A),len(B),len(B[0]); return [[sum(A[i][k]*B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]
def e2(A): return sum(det([[A[i][j] for j in S] for i in S]) for S in combinations(range(len(A)),2))
def offd(M):
    n=len(M); return [[M[i][j] if i!=j else F(0) for j in range(n)] for i in range(n)]
def Pq(g):
    n=len(g); q=sum(F(x)*x for x in g); return [[(F(1) if i==j else F(0))-F(g[i])*F(g[j])/q for j in range(n)] for i in range(n)],q
def kappa2(g,H):
    P,q=Pq(g); return e2(mm(mm(P,offd(H)),P))/q
def sigma2(g,H):
    P,q=Pq(g); return e2(mm(mm(P,H),P))/q

Fr=lambda a,b: F(a,b)
# corpus (gate_11 P1) + certified pins (gate_11 P3 TRIPLES)
S={
 "keystone":{"g":[3,1,2],"H":[[2,1,0],[1,0,0],[0,0,2]],"kc":F(-1,49),"K_G":F(-3,49),"kint":F(-3,49),"ks":F(1,49)},
 "sphere3":{"g":[2,4,6],"H":[[2,0,0],[0,2,0],[0,0,2]],"kc":F(0),"K_G":F(1,14),"kint":F(0),"ks":F(1,14)},
 "saddle":{"g":[-1,-1,1],"H":[[0,-1,0],[-1,0,0],[0,0,0]],"kc":F(-1,9),"K_G":F(-1,9),"kint":F(0),"ks":F(0)},
 "cylinder":{"g":[2,4,0],"H":[[2,0,0],[0,2,0],[0,0,0]],"kc":None,"K_G":F(0),"kint":None,"ks":None},  # g2=0 -> O refuses
}
def toF(H): return [[F(x) for x in row] for row in H]

print("=== Stage A reference values (n=3 corpus), gated ===\n")
ok=True
print(f"{'surface':10}{'kappa_2=e2(PHcP)/q':22}{'cert kc':10}{'sigma_2':10}{'cert K_G':10}{'kc+kint+ks':12}gate")
for name,d in S.items():
    g=d["g"]; H=toF(d["H"]); k2=kappa2(g,H); s2=sigma2(g,H)
    if name=="cylinder":
        # asymmetry: P-route computes; O/fingerprint refuses (g has a zero component)
        g2=(s2==d["K_G"] and k2==F(0))
        print(f"{name:10}{str(k2):22}{'(refuse)':10}{str(s2):10}{str(d['K_G']):10}{'(refuse)':12}{g2}  [P-route computes; O refuses ROLE_CHART_UNAVAILABLE]")
        ok&=g2
    else:
        gk=(k2==d["kc"]); gs=(s2==d["K_G"]); gx=(d["kc"]+d["kint"]+d["ks"]==s2)
        allg=gk and gs and gx; ok&=allg
        print(f"{name:10}{str(k2):22}{str(d['kc']):10}{str(s2):10}{str(d['K_G']):10}{str(d['kc']+d['kint']+d['ks']):12}{allg}")

print("\nGATE A  kappa_2 == certified kc  (numerator channel = coupling channel):",
      all(kappa2(S[n]['g'],toF(S[n]['H']))==S[n]['kc'] for n in ('keystone','sphere3','saddle')))
print("GATE B  sigma_2 == certified K_G  (curvature = full-Hessian channel):",
      all(sigma2(S[n]['g'],toF(S[n]['H']))==S[n]['K_G'] for n in S))
print("GATE C  cross-route kc+kint+ks == sigma_2:",
      all(S[n]['kc']+S[n]['kint']+S[n]['ks']==sigma2(S[n]['g'],toF(S[n]['H'])) for n in ('keystone','sphere3','saddle')))

# GATE D -- falsification control: using FULL H for the numerator gives sigma_2 (=K_G), NOT kc.
#   at keystone that is -3/49 != -1/49, so mistaking Hc for H is caught.
ctrl=sigma2(S['keystone']['g'],toF(S['keystone']['H']))  # = e2(PHP)/q = -3/49
gD=(ctrl==F(-3,49) and ctrl!=S['keystone']['kc'])
print(f"GATE D  control: full-H numerator = {ctrl} (=K_G) != kc={S['keystone']['kc']} -> Hc restriction is load-bearing:", gD)
ok&=gD

# n>=4 sensors are absent/trivial at n=3 (stated, not computed away):
print("\nshape moment: S^(n-2,2) ABSENT at n=3 (dim 0) -> no shape row here; anchor = RC-7 n=4 quintuple 147/153/24/0")
print("localization: single triangle at n=3 -> support theorem trivial; anchor = RC-8 n>=4")
print("fingerprint A_c (keystone): 42793/1555848 [certified RC-4] -- cited, not re-derived")

print("\nStage-A reference values:", "ALL GATES PASS" if ok else "GATE FIRED")
import sys; sys.exit(0 if ok else 1)
