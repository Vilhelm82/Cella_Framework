"""
DBP Curvature Role Reduction — reference implementation + retrodiction gate + stress-test skeleton.
Exact-Q (fractions only), stdlib only. Substrate for CC to stress-test and vary exhaustively.
"""
import sys, io, json, datetime, random
from fractions import Fraction as Q
from itertools import combinations, permutations

# ===================== exact linear algebra =====================
def det(M):
    n=len(M)
    if n==0: return Q(1)
    if n==1: return M[0][0]
    if n==2: return M[0][0]*M[1][1]-M[0][1]*M[1][0]
    s=Q(0)
    for j in range(n):
        s+=((-1)**j)*M[0][j]*det([row[:j]+row[j+1:] for row in M[1:]])
    return s
def matmul(A,B):
    n=len(A); kk=len(B); m=len(B[0])
    return [[sum(A[i][t]*B[t][j] for t in range(kk)) for j in range(m)] for i in range(n)]
def trace(M): return sum(M[i][i] for i in range(len(M)))
def solve(A,b):
    n=len(A); M=[row[:]+[b[i]] for i,row in enumerate(A)]
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0)
        M[c],M[p]=M[p],M[c]
        piv=M[c][c]; M[c]=[x/piv for x in M[c]]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[M[r][k]-f*M[c][k] for k in range(n+1)]
    return [M[r][n] for r in range(n)]

# ===================== canonical channel-density tower =====================
def q_of(g): return sum(x*x for x in g)

def channel_density(g,H,r,t,u):
    """C_hat_r(t,u) = (-1)^{r+1} * sum_{|I|=r+1} det[[0, gI^T],[gI, (t Hc + u Hs)_I]]."""
    n=len(g)
    M=[[(t*H[i][j] if i!=j else u*H[i][j]) for j in range(n)] for i in range(n)]
    tot=Q(0)
    for I in combinations(range(n), r+1):
        gI=[g[i] for i in I]; MI=[[M[i][j] for j in I] for i in I]; k=len(I)
        B=[[Q(0)]+gI]+[[gI[a]]+MI[a] for a in range(k)]
        tot+=det(B)
    return ((-1)**(r+1))*tot

def sigma_numerator(g,H,r):
    """E_r := C_hat_r(1,1) (rational). sigma_r = E_r / q^((r+2)/2)."""
    return channel_density(g,H,r,Q(1),Q(1))

def channel_vector(g,H,r):
    """coeffs kappa_hat_{r;p,q} of t^p u^{r-p} in C_hat_r (homogeneous degree r)."""
    nodes=list(range(r+1))
    V=[[Q(s)**p for p in range(r+1)] for s in nodes]
    y=[channel_density(g,H,r,Q(s),Q(1)) for s in nodes]
    a=solve(V,y)
    return {(p,r-p):a[p] for p in range(r+1)}

# ===================== gauge action & shape operator =====================
def gauge_H(g,H,a):
    n=len(g); return [[H[i][j]+g[i]*a[j]+a[i]*g[j] for j in range(n)] for i in range(n)]

def PHP(g,H):
    """Rational carrier of the shape operator S = -PHP/sqrt(q). Returns (PHP, q)."""
    n=len(g); qq=q_of(g)
    P=[[(Q(1) if i==j else Q(0))-Q(g[i]*g[j])/qq for j in range(n)] for i in range(n)]
    return matmul(matmul(P,H),P), qq
def e2(M): return (trace(M)**2-trace(matmul(M,M)))/2

# ===================== n=3 single-edge corollary =====================
def kc_n3(g,H):
    return channel_vector(g,H,2)[(2,0)]/q_of(g)**2   # pure-coupling channel kappa_c

# ===================== RETRODICTION GATE (established baseline) =====================
def retrodiction_gate(log):
    P=lambda *a: log(" ".join(str(x) for x in a))
    fails=[]
    def expect(name,got,want):
        ok=(got==want); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {got}" + ("" if ok else f"  (want {want})"))
        if not ok: fails.append(name)

    P("== n=3 keystone  F=x1^2+x1x2+x3^2-3 @(1,1,1) ==")
    g=[Q(3),Q(1),Q(2)]; H=[[Q(2),Q(1),Q(0)],[Q(1),Q(0),Q(0)],[Q(0),Q(0),Q(2)]]
    cv=channel_vector(g,H,2); qq=q_of(g)
    kc,kint,ks=cv[(2,0)]/qq**2, cv[(1,1)]/qq**2, cv[(0,2)]/qq**2
    expect("channels (kc,kint,ks)",(kc,kint,ks),(Q(-1,49),Q(-3,49),Q(1,49)))
    expect("sigma_2 == channel sum == K_G", sigma_numerator(g,H,2)/qq**2, Q(-3,49))
    expect("sigma_1 numerator (=tr S * sqrt q numer)", sigma_numerator(g,H,1), Q(-24))
    php,_=PHP(g,H)
    expect("sigma_2 * q == e2(PHP)", (sigma_numerator(g,H,2)/qq**2)*qq, e2(php))
    expect("sigma_1 numerator / q == -tr(PHP)", Q(sigma_numerator(g,H,1),qq), -trace(php))

    P("== sigma_2 retrodiction anchors (K_G) ==")
    anchors={
        "sphere x2+y2+z2-1 @(3/5,4/5,0)": ([Q(6,5),Q(8,5),Q(0)], [[Q(2),Q(0),Q(0)],[Q(0),Q(2),Q(0)],[Q(0),Q(0),Q(2)]], Q(1)),
        "cone x2+y2-z2 @(3,4,5)":         ([Q(6),Q(8),Q(-10)], [[Q(2),Q(0),Q(0)],[Q(0),Q(2),Q(0)],[Q(0),Q(0),Q(-2)]], Q(0)),
    }
    for name,(gg,HH,want) in anchors.items():
        expect(f"K_G {name}", sigma_numerator(gg,HH,2)/q_of(gg)**2, want)

    P("== gauge transport: every sigma_r numerator invariant; channels move (n=3) ==")
    inv_ok=True; moved=set()
    for a in [[Q(1),Q(0),Q(0)],[Q(0),Q(1),Q(0)],[Q(1),Q(-2),Q(3)],[Q(-1,2),Q(5),Q(1)]]:
        Hg=gauge_H(g,H,a)
        for r in (1,2):
            if sigma_numerator(g,Hg,r)!=sigma_numerator(g,H,r): inv_ok=False
        cvg=channel_vector(g,Hg,2); moved.add((cvg[(2,0)],cvg[(0,2)]))
    expect("all sigma_r numerators gauge-invariant", inv_ok, True)
    expect("channels move under gauge (>1 distinct)", len(moved)>1, True)

    P("== single-edge corollary (n=3): d kappa_c(t e_k) = 4 t (prod g) m_k / q^2 ==")
    rng=random.Random(1); se_ok=True
    for _ in range(200):
        gg=[Q(rng.randint(-6,6),rng.randint(1,5)) for _ in range(3)]
        if 0 in gg: continue
        HH=[[Q(0)]*3 for _ in range(3)]
        for i in range(3): HH[i][i]=Q(rng.randint(-4,4),rng.randint(1,3))
        e=[Q(rng.randint(-5,5),rng.randint(1,4)) for _ in range(3)]
        HH[0][1]=HH[1][0]=e[0]; HH[0][2]=HH[2][0]=e[1]; HH[1][2]=HH[2][1]=e[2]
        for k in range(3):
            t=Q(rng.randint(-3,3),rng.randint(1,2))
            a=[Q(0),Q(0),Q(0)]; a[k]=t
            mk=HH[[1,0,0][k] if False else ([j for j in range(3) if j!=k][0])][[j for j in range(3) if j!=k][1]]
            opp=HH[[j for j in range(3) if j!=k][0]][[j for j in range(3) if j!=k][1]]
            dk=kc_n3(gg,gauge_H(gg,HH,a))-kc_n3(gg,HH)
            pred=4*t*gg[0]*gg[1]*gg[2]*opp/q_of(gg)**2
            if dk!=pred: se_ok=False
    expect("single-edge dkappa_c formula (200 surfaces x 3 axes)", se_ok, True)

    P("== n=4 parity: even r rational, odd r carries sqrt(q); numerators gauge-invariant ==")
    g4=[Q(1),Q(2),Q(1),Q(3)]
    H4=[[Q(2),Q(1),Q(0),Q(1)],[Q(1),Q(3),Q(2),Q(0)],[Q(0),Q(2),Q(1),Q(1)],[Q(1),Q(0),Q(1),Q(4)]]
    for r in (1,2,3):
        even=((r+2)%2==0)
        gi=set(sigma_numerator(g4,gauge_H(g4,H4,a),r)
               for a in [[Q(1),Q(0),Q(0),Q(0)],[Q(1),Q(-1),Q(2),Q(1)],[Q(0),Q(3),Q(-1,2),Q(1)]])
        P(f"  r={r}: parity={'EVEN(rational)' if even else 'ODD(sqrt q)'}  numerator gauge-invariant: {len(gi)==1}")
        if len(gi)!=1: fails.append(f"n4 sigma_{r} gauge")
    return fails

# ===================== STRESS-TEST: random-surface invariant checker =====================
def check_surface(g,H,seed=0,n_gauge=6,perm_cap=8):
    n=len(g); notes=[]; ok=True; rng=random.Random(seed)
    base=[sigma_numerator(g,H,r) for r in range(1,n)]
    # (1) gauge invariance of all sigma_r numerators + channel shift trace-zero
    for _ in range(n_gauge):
        a=[Q(rng.randint(-6,6),rng.randint(1,5)) for _ in range(n)]
        Hg=gauge_H(g,H,a)
        for idx,r in enumerate(range(1,n)):
            if sigma_numerator(g,Hg,r)!=base[idx]:
                ok=False; notes.append(f"GAUGE σ_{r} moved (a={a})")
            cv0=channel_vector(g,H,r); cvg=channel_vector(g,Hg,r)
            shift=sum(cvg[k]-cv0[k] for k in cv0)
            if shift!=0:
                ok=False; notes.append(f"GAUGE channel shift not zero-sum at r={r}")
    # (2) passive permutation invariance of channel vector (sample if n large)
    perms=list(permutations(range(n)))
    if len(perms)>perm_cap: perms=rng.sample(perms,perm_cap)
    for p in perms:
        gp=[g[i] for i in p]; Hp=[[H[p[i]][p[j]] for j in range(n)] for i in range(n)]
        for r in range(1,n):
            if channel_vector(gp,Hp,r)!=channel_vector(g,H,r):
                ok=False; notes.append(f"PASSIVE perm {p} moved channels r={r}")
    return ok, notes

def explore(n, trials, seed, log):
    rng=random.Random(seed); bad=0
    for t in range(trials):
        g=[Q(rng.randint(-6,6),rng.randint(1,5)) for _ in range(n)]
        if 0 in g:  # keep regular locus for now (CC: vary this to probe singular strata)
            g=[x if x!=0 else Q(1) for x in g]
        H=[[Q(0)]*n for _ in range(n)]
        for i in range(n):
            for j in range(i,n):
                v=Q(rng.randint(-5,5),rng.randint(1,4)); H[i][j]=H[j][i]=v
        ok,notes=check_surface(g,H,seed=rng.randint(0,10**6))
        if not ok:
            bad+=1; log(f"  ANOMALY n={n} trial={t}: {notes[:3]}")
    log(f"  n={n}: {trials-bad}/{trials} surfaces upheld all invariants" + ("" if bad==0 else f"  ({bad} ANOMALIES)"))
    return bad

def main():
    out=io.StringIO()
    def log(s): print(s); out.write(s+"\n")
    log("="*92); log("DBP CURVATURE ROLE REDUCTION — RETRODICTION GATE + STRESS SKELETON"); log("="*92)
    log("\n--- RETRODICTION GATE (must be clean before exploring) ---")
    fails=retrodiction_gate(log)
    log(f"\nRETRODICTION GATE: {'CLEAN' if not fails else 'FAILURES: '+str(fails)}")
    log("\n--- EXHAUSTIVE-VARIATION SWEEP (regular locus; CC: extend) ---")
    tot=0
    for n in (3,4,5):
        tot+=explore(n, 25, seed=100+n, log=log)
    log(f"\nSWEEP: {'ALL INVARIANTS UPHELD' if tot==0 else str(tot)+' ANOMALIES — investigate'}")
    rep={"test":"dbp_curvature_reduction_harness","ts":datetime.datetime.now().isoformat(),
         "retrodiction_fails":fails,"sweep_anomalies":tot,"console_log":out.getvalue()}
    try:
        import os
        d="/run/media/wlloyd/Games 2/Lloyd_Workbench/engine/Raw console output"; os.makedirs(d,exist_ok=True)
        fn=os.path.join(d,f"dbp_curvature_reduction_harness_{datetime.datetime.now():%Y%m%d_%H%M%S}.json")
        json.dump(rep,open(fn,"w"),indent=2); print(f"[report: {fn}]")
    except Exception as ex: print(f"[report failed: {ex}]")

if __name__=="__main__":
    main()
