# stageB_gens.py — Stage B rung k=1: T_1 on the rest-from-release torus
# Prereg pin c4875c25 (FROZEN). Generators verbatim from stageA_modspec.py build().
import sympy as sp, hashlib, time
T0=time.time()
def tick(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)
c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2')
pi1,pi2,h,g=sp.symbols('pi1 pi2 h g'); x1,x2,t1=sp.symbols('x1 x2 t1')
def build(qa,qb):
    qa=sp.Matrix(qa); qb=sp.Matrix(qb); qm=(qa+qb)/2; v=(qb-qa)/h
    om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
    w1,w2=om(0,qm,v),om(1,qm,v); cd=qm[0]*qm[2]+qm[1]*qm[3]
    return h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cd+g*(2*qm[0]+qm[2]))
def T1_eliminant(hsign):
    Ld=build((c1,s1,c2,s2),(C1,S1,C2,S2))
    D1=[sp.diff(Ld,v) for v in (c1,s1,c2,s2)]
    hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
    hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
    prm={g:10,h:sp.Rational(hsign,40),pi1:0,pi2:0}
    W=lambda t:((1-t**2)/(1+t**2),2*t/(1+t**2))
    wc1,ws1=W(x1); wc2,ws2=W(x2); tc1,ts1=W(t1)
    out={}
    for br,(TC2,TS2) in (('inv',(-1,0)),('bot',(1,0))):
        sub={C1:tc1,S1:ts1,C2:TC2,S2:TS2,c1:wc1,s1:ws1,c2:wc2,s2:ws2}
        E=[sp.fraction(sp.together(G.subs(prm).subs(sub)))[0] for G in (hG1,hG2)]
        E=[sp.expand(e) for e in E]
        tick(f"h={hsign}/40 {br}: t1-degs {[sp.degree(e,t1) for e in E]}")
        R=sp.resultant(sp.Poly(E[0],t1),sp.Poly(E[1],t1))
        R=sp.Poly(sp.expand(R),x1,x2)
        tick(f"  raw resultant deg (x1,x2) = {R.degree(x1)},{R.degree(x2)}")
        F=sp.factor_list(R.as_expr())
        ghosts=[]; honest=[]
        for fac,mult in F[1]:
            if fac in (1+x1**2,1+x2**2) or fac.free_symbols<=set() : ghosts.append((fac,mult))
            else: honest.append((fac,mult))
        Hs=sp.expand(sp.prod([f for f,m in honest]))  # squarefree honest part
        out[br]=dict(raw_deg=(R.degree(x1),R.degree(x2)),ghosts=ghosts,
                     honest_sqfree=Hs,honest_facs=[(sp.degree(f,x1),sp.degree(f,x2),m) for f,m in honest])
    return out
tick("forward run")
FWD=T1_eliminant(+1)
tick("backward run (PB.2)")
BWD=T1_eliminant(-1)
print("="*60)
for br in ('inv','bot'):
    Hf,Hb=FWD[br]['honest_sqfree'],BWD[br]['honest_sqfree']
    same=sp.simplify(Hf*sp.LC(sp.Poly(Hb,x1,x2))-Hb*sp.LC(sp.Poly(Hf,x1,x2)))==0
    print(f"[{br}] raw degs {FWD[br]['raw_deg']}  ghosts {FWD[br]['ghosts']}")
    print(f"[{br}] honest factor shape (dx1,dx2,mult): {FWD[br]['honest_facs']}")
    print(f"[{br}] PB.2 forward==backward (exact, normalized): {same}")
    print(f"[{br}] honest sha16: {hashlib.sha256(sp.srepr(sp.Poly(Hf,x1,x2)).encode()).hexdigest()[:16]}")
print("="*60)
# PB.1 witness scan on the inv branch: real points, exact energy check 2*c1+c2<=1
H=sp.Poly(FWD['inv']['honest_sqfree'],x1)
viol=0; wit=0
for X2 in [sp.Rational(n,7) for n in range(-21,22)]:
    q=sp.Poly([cf.subs(x2,X2) for cf in H.all_coeffs()],x1)
    if q.degree() is None or q.degree()<1: continue
    for r in sp.real_roots(q):
        wit+=1
        cc1=(1-r**2)/(1+r**2); cc2=(1-X2**2)/(1+X2**2)
        if sp.simplify(2*cc1+cc2-1)>0: viol+=1
print(f"PB.1: {wit} real witnesses scanned, energy-gate violations = {viol}")
print("VERDICT PB.1:", "PASS" if viol==0 else "KB.1 FIRED — HALT")
tick("done")
