# stageB_v2.py -- Stage B rung k=1 under PREREG v2 (pin 96b3e09c29a9c182)
# D1 fix (lc saturation + fiber check), DF-7 principal classification,
# dual-chart eliminants, PB.1', PB.5 census, SP-1 graded. Deterministic.
import sympy as sp, hashlib, time
import mpmath as mp
T0=time.time(); OUT=[]
def emit(m):
    print(m, flush=True); OUT.append(m)
def tick(m): print(f"[{time.time()-T0:7.1f}s] {m}", flush=True)

c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2')
pi1,pi2,h,g=sp.symbols('pi1 pi2 h g'); x1,x2,t1,u=sp.symbols('x1 x2 t1 u')
GV={g:10}; HV=sp.Rational(1,40)

def build(qa,qb):
    qa=sp.Matrix(qa); qb=sp.Matrix(qb); qm=(qa+qb)/2; v=(qb-qa)/h
    om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
    w1,w2=om(0,qm,v),om(1,qm,v); cd=qm[0]*qm[2]+qm[1]*qm[3]
    return h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cd+g*(2*qm[0]+qm[2]))

Ld=build((c1,s1,c2,s2),(C1,S1,C2,S2))
D1=[sp.diff(Ld,v) for v in (c1,s1,c2,s2)]
G1=pi1+(D1[0]*(-s1)+D1[1]*c1)          # momentum eq, circle 1 (unscaled)
G2=pi2+(D1[2]*(-s2)+D1[3]*c2)          # momentum eq, circle 2
UNP=[G1.subs(GV),G2.subs(GV),C1**2+S1**2-1,C2**2+S2**2-1]  # unpinned system

W =lambda t:((1-t**2)/(1+t**2),2*t/(1+t**2))     # x = tan(theta/2)
WU=lambda t:((t**2-1)/(1+t**2),2*t/(1+t**2))     # u = cot(theta2/2); u=0 <=> theta2=pi

def eliminant(hsign, chart):
    prm={g:10,h:sp.Rational(hsign,40),pi1:0,pi2:0}
    wc1,ws1=W(x1); tc1,ts1=W(t1)
    if chart=='x': wc2,ws2=W(x2);  v2=x2
    else:          wc2,ws2=WU(u);  v2=u
    res={}
    for br,(TC2,TS2) in (('inv',(-1,0)),('bot',(1,0))):
        if chart=='u' and br=='bot': continue
        sub={C1:tc1,S1:ts1,C2:TC2,S2:TS2,c1:wc1,s1:ws1,c2:wc2,s2:ws2}
        E=[sp.expand(sp.fraction(sp.together(Gq.subs(prm).subs(sub)))[0]) for Gq in (h*G1,h*G2)]
        # shared-factor strip (corner-class only; anything else is a HALT anomaly)
        gg=sp.gcd(sp.Poly(E[0],t1,x1,v2),sp.Poly(E[1],t1,x1,v2)).as_expr()
        shared=[]
        if gg!=1:
            for fac,m in sp.factor_list(gg)[1]:
                s_ = fac.free_symbols
                ok = (len(s_)==1 and fac==1+list(s_)[0]**2)
                shared.append((str(fac),m,'corner-class' if ok else 'ANOMALY-HALT'))
                assert ok, f"non-corner shared factor: {fac}"
            E=[sp.expand(sp.cancel(e/gg)) for e in E]
        lcp=sp.expand(sp.LC(sp.Poly(E[0],t1))*sp.LC(sp.Poly(E[1],t1)))
        R=sp.resultant(sp.Poly(E[0],t1),sp.Poly(E[1],t1))
        R=sp.Poly(sp.expand(R),x1,v2)
        F=sp.factor_list(R.as_expr())
        corner=[];lcrem=[];honest=[]
        for fac,mult in F[1]:
            if fac in (1+x1**2,1+v2**2): corner.append((fac,mult)); continue
            q,r=sp.div(sp.Poly(lcp,x1,v2),sp.Poly(fac,x1,v2))
            if r==0: lcrem.append((fac,mult))
            else: honest.append((fac,mult))
        # fiber check per removed lc factor: pin terminal circle-1 at (-1,0)
        led=[]
        for fac,mult in lcrem:
            sub2=dict(sub); sub2[C1],sub2[S1]=-1,0
            Ep=[sp.expand(sp.fraction(sp.together(Gq.subs(prm).subs(sub2)))[0]) for Gq in (h*G1,h*G2)]
            fs=fac.free_symbols
            if fs=={v2} and sp.degree(fac,v2)==1:
                rt=sp.solve(fac,v2)[0]
                q1,q2=[sp.Poly(e.subs(v2,rt),x1) for e in Ep]
                gd=sp.gcd(q1,q2); led.append((str(fac),mult,'gcd_deg=%d'%sp.degree(gd,x1),
                    'ARTIFACT' if sp.degree(gd,x1)<=0 else 'CHART-INF SOLUTIONS'))
            else: led.append((str(fac),mult,'-','UNCHECKED(nonlinear/multivar)'))
        Hs=sp.prod([f for f,m in honest]) if honest else sp.Integer(1)
        res[br]=dict(shared=shared,raw=(R.degree(x1),R.degree(v2)),corner=corner,lcrem=led,
                     honest=sp.expand(Hs),
                     shapes=[(sp.degree(f,x1),sp.degree(f,v2),m) for f,m in honest])
    return res

tick("x-chart forward"); FX=eliminant(+1,'x')
tick("x-chart backward"); BX=eliminant(-1,'x')
tick("u-chart forward"); FU=eliminant(+1,'u')
tick("u-chart backward"); BU=eliminant(-1,'u')

def norm_eq(A,B,v):
    return sp.expand(A*sp.LC(sp.Poly(B,x1,v))-B*sp.LC(sp.Poly(A,x1,v)))==0
emit("== ELIMINANTS ==")
for tag,Fw,Bw,v in (('x/inv',FX['inv'],BX['inv'],x2),('x/bot',FX['bot'],BX['bot'],x2),
                    ('u/inv',FU['inv'],BU['inv'],u)):
    emit(f"[{tag}] shared {Fw['shared']} raw {Fw['raw']} corner {[(str(f),m) for f,m in Fw['corner']]} "
         f"lc-removed {Fw['lcrem']} honest {Fw['shapes']}")
    emit(f"[{tag}] PB.2 fwd==bwd: {norm_eq(Fw['honest'],Bw['honest'],v)}")
    emit(f"[{tag}] honest sha16: {hashlib.sha256(sp.srepr(sp.Poly(Fw['honest'],x1,v)).encode()).hexdigest()[:16]}")

# ---- DF-7 principal solver ------------------------------------------------
mp.mp.dps=60
Y=(C1,S1,C2,S2)
SYS=[e.subs({h:HV,pi1:0,pi2:0}) for e in UNP]
J=sp.Matrix(SYS).jacobian(Y)
fS=sp.lambdify((c1,s1,c2,s2)+Y,SYS,'mpmath')
fJ=sp.lambdify((c1,s1,c2,s2)+Y,J,'mpmath')
BMOT=mp.mpf(1)/80; RES=mp.mpf(10)**-45; CONTR=mp.mpf(10)**-20; GCLASS=mp.mpf(10)**-20
def principal(q0):
    y=[mp.mpf(t) for t in q0]; last=mp.inf
    for it in range(80):
        Fv=mp.matrix(fS(*q0,*y)); Jv=mp.matrix(fJ(*q0,*y))
        d=mp.lu_solve(Jv,-Fv); y=[y[i]+d[i] for i in range(4)]
        last=max(abs(t) for t in d)
        if last<mp.mpf(10)**-55: break
    r=max(abs(t) for t in mp.matrix(fS(*q0,*y)))
    mo=max(abs(y[i]-mp.mpf(q0[i])) for i in range(4))
    ok=(r<=RES) and (mo<=BMOT) and (last<=CONTR)
    mu=max(abs(y[2]+1),abs(y[3]))
    return ok,mu,r,mo

def scan(H,vv,grid,label,energy_exact):
    Hp=sp.Poly(H,x1); rows=[]; muP=[]; muG=[]
    nP=nG=nU=nW=0; violP=violG=0
    for V in grid:
        q=sp.Poly([cf.subs(vv,V) for cf in Hp.all_coeffs()],x1)
        if q.degree() is None or q.degree()<1: continue
        for r in sp.real_roots(q):
            nW+=1
            cc1=sp.Rational(0); X=r
            cc1e=(1-X**2)/(1+X**2); ss1e=2*X/(1+X**2)
            if vv is x2: cc2e=(1-V**2)/(1+V**2); ss2e=2*V/(1+V**2)
            else:        cc2e=(V**2-1)/(1+V**2); ss2e=2*V/(1+V**2)
            q0=tuple(mp.mpf(sp.N(e,60)) for e in (cc1e,ss1e,cc2e,ss2e))
            ok,mu,rr,mo=principal(q0)
            E=sp.simplify(2*cc1e+cc2e-1)
            vio=bool(E>0)
            if not ok: nU+=1; cls='UNRESOLVED'
            elif mu<=GCLASS: nP+=1; muP.append(mu); cls='PRINCIPAL'; violP+=vio
            elif mu>=mp.mpf(10)**-6: nG+=1; muG.append(mu); cls='GHOST'; violG+=vio
            else: nU+=1; cls='UNRESOLVED'
    sep = (min(muG)/max(muP)) if (muP and muG) else mp.inf
    emit(f"[{label}] witnesses={nW} principal={nP} ghost={nG} unresolved={nU} "
         f"| mu_P_max={mp.nstr(max(muP),3) if muP else '-'} mu_G_min={mp.nstr(min(muG),3) if muG else '-'} sep={mp.nstr(sep,3) if muP and muG else 'inf'}")
    emit(f"[{label}] energy violations: principal={violP} ghost={violG}")
    return nW,nP,nG,nU,violP,violG

emit("== DF-7 CLASSIFICATION + PB.1' + PB.5 ==")
gx=[sp.Rational(n,7) for n in range(-21,22)]
gu=[sp.Rational(n,4000) for n in range(-12,13)]+[sp.Rational(n,40) for n in range(-20,21) if n!=0]
gu=sorted(set(gu))
xr=scan(FX['inv']['honest'],x2,gx,'x/inv',True)
ur=scan(FU['inv']['honest'],u,gu,'u/inv',True)

emit("== VERDICTS ==")
pb1p = (xr[4]==0 and ur[4]==0)
emit(f"PB.1' (principal-only energy gate): {'PASS' if pb1p else 'KB.1 FIRED - HALT'}")
sp1a = (xr[1]==0); sp1b = (ur[1]>0); sp1c = pb1p and ur[1]>0
emit(f"SP-1(a) all x-grid witnesses ghost: {sp1a}")
emit(f"SP-1(b) principal T_1 nonempty in u-chart: {sp1b}")
emit(f"SP-1(c) PB.1' passes non-vacuously: {sp1c}")
blob="\n".join(OUT).encode()
print("RESULTS-SHA256:",hashlib.sha256(blob).hexdigest())
tick("done")
