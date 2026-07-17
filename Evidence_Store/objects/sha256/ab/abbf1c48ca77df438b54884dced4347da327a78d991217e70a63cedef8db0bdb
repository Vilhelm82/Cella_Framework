# stageB_k2.py -- Stage B rung k=2 (PREREG v2 pin 96b3e09c, predecl pin 3a675143)
# Arm W: principal-chain shooting witnesses (default). Arm T: symbolic tower ('tower').
import sympy as sp, hashlib, time, sys
import mpmath as mp
T0=time.time(); OUT=[]
MODE=sys.argv[1] if len(sys.argv)>1 else 'witness'
def emit(m): print(m,flush=True); OUT.append(m)
def tick(m): print(f"[{time.time()-T0:7.1f}s] {m}",flush=True)

c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2')
pi1,pi2,h,g=sp.symbols('pi1 pi2 h g')
x1,u,ta,tb,t2=sp.symbols('x1 u ta tb t2')
HV=sp.Rational(1,40)
def build(qa,qb):
    qa=sp.Matrix(qa); qb=sp.Matrix(qb); qm=(qa+qb)/2; v=(qb-qa)/h
    om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
    w1,w2=om(0,qm,v),om(1,qm,v); cd=qm[0]*qm[2]+qm[1]*qm[3]
    return h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cd+g*(2*qm[0]+qm[2]))
Ld=build((c1,s1,c2,s2),(C1,S1,C2,S2))
D1=[sp.diff(Ld,v) for v in (c1,s1,c2,s2)]
D2=[sp.diff(Ld,v) for v in (C1,S1,C2,S2)]
G1=pi1+(D1[0]*(-s1)+D1[1]*c1); G2=pi2+(D1[2]*(-s2)+D1[3]*c2)
P1u=D2[0]*(-S1)+D2[1]*C1; P2u=D2[2]*(-S2)+D2[3]*C2      # explicit momentum updates
NUM={g:10}

if MODE=='witness':
    import multiprocessing as MP
    GU=[sp.Rational(n,4000) for n in range(-24,25)]+[sp.Rational(n,40) for n in list(range(-20,0))+list(range(1,21))]
    GU=sorted(set(GU))
    import os
    if os.environ.get('SMOKE'): GU=[sp.Rational(n,4000) for n in (-8,-2,0,2,8)]+[sp.Rational(1,10)]
    def worker_init():
        global fS,fJ,fP,gS,gJ,gP,mp,math
        import mpmath as mp, math
        mp.mp.dps=60
        Y=(C1,S1,C2,S2)
        SYS=[e.subs(NUM) for e in (G1,G2,C1**2+S1**2-1,C2**2+S2**2-1)]
        Jm=sp.Matrix(SYS).jacobian(Y)
        A=(c1,s1,c2,s2,pi1,pi2,h)+Y
        fS=sp.lambdify(A,SYS,'mpmath',cse=True)
        fJ=sp.lambdify(A,Jm,'mpmath',cse=True)
        fP=sp.lambdify((c1,s1,c2,s2,h)+Y,[e.subs(NUM) for e in (P1u,P2u)],'mpmath',cse=True)
        gS=sp.lambdify(A,SYS,'math',cse=True)
        gJ=sp.lambdify(A,Jm.tolist(),'math',cse=True)
        gP=sp.lambdify((c1,s1,c2,s2,h)+Y,[e.subs(NUM) for e in (P1u,P2u)],'math',cse=True)
    def fsolve4(M,b):
        M=[r[:] for r in M]; b=b[:]
        for i in range(4):
            p=max(range(i,4),key=lambda r:abs(M[r][i]))
            M[i],M[p]=M[p],M[i]; b[i],b[p]=b[p],b[i]
            for r in range(i+1,4):
                f=M[r][i]/M[i][i]; b[r]-=f*b[i]
                for cc in range(i,4): M[r][cc]-=f*M[i][cc]
        x=[0.0]*4
        for i in (3,2,1,0):
            x[i]=(b[i]-sum(M[i][j]*x[j] for j in range(i+1,4)))/M[i][i]
        return x
    def fstep(q0,p0,hh,seed,bmot):
        y=list(seed)
        for it in range(40):
            Fv=gS(*q0,*p0,hh,*y)
            if max(abs(t) for t in Fv)<1e-13: break
            Jv=gJ(*q0,*p0,hh,*y)
            d=fsolve4([list(r) for r in Jv],[-t for t in Fv])
            y=[y[i]+d[i] for i in range(4)]
        mo=max(abs(y[i]-q0[i]) for i in range(4))
        ok=(max(abs(t) for t in gS(*q0,*p0,hh,*y))<1e-11) and (mo<=bmot)
        return ok,y
    def fchainK(th,uu,hh,k):
        q0=(math.cos(th),math.sin(th),(uu*uu-1)/(uu*uu+1),2*uu/(uu*uu+1))
        ok,q1=fstep(q0,(0.0,0.0),hh,list(q0),20/1600)
        if not ok: return None
        if k==1: return q1
        pp=gP(*q0,hh,*q1)
        ok,q2=fstep(tuple(q1),tuple(pp),hh,[2*q1[i]-q0[i] for i in range(4)],60/1600)
        return q2 if ok else None
    def solve_step(q0,p0,hh,seed,bmot,tol,itmax):
        y=list(seed); last=mp.inf
        for it in range(itmax):
            Fv=mp.matrix(fS(*q0,*p0,hh,*y)); Jv=mp.matrix(fJ(*q0,*p0,hh,*y))
            d=mp.lu_solve(Jv,-Fv); y=[y[i]+d[i] for i in range(4)]
            last=max(abs(t) for t in d)
            if last<tol*mp.mpf(10)**-10: break
        r=max(abs(t) for t in mp.matrix(fS(*q0,*p0,hh,*y)))
        mo=max(abs(y[i]-q0[i]) for i in range(4))
        return (r<=tol) and (mo<=bmot) and (last<=mp.mpf(10)**-20), y
    def chainK(th,uu,hh,k,cert):
        tol=mp.mpf(10)**(-45 if cert else -25); itm=90 if cert else 40
        with mp.workdps(60 if cert else 30):
            q0=(mp.cos(th),mp.sin(th),(uu*uu-1)/(uu*uu+1),2*uu/(uu*uu+1))
            ok,q1=solve_step(q0,(mp.mpf(0),mp.mpf(0)),hh,list(q0),mp.mpf(20)/1600,tol,itm)
            if not ok: return None
            if k==1: return q1
            pp=fP(*q0,hh,*q1)
            ok,q2=solve_step(tuple(q1),tuple(pp),hh,[2*q1[i]-q0[i] for i in range(4)],mp.mpf(60)/1600,tol,itm)
            return q2 if ok else None
    def u_witnesses(args):
        uu_r,hs,k=args
        uu=mp.mpf(sp.N(uu_r,60)); hh=mp.mpf(hs)/40
        TH=[-mp.pi+2*mp.pi*(i+mp.mpf(1)/2)/720 for i in range(720)]
        fh=float(hh); fu=float(uu)
        vals=[fchainK(float(th),fu,fh,k) for th in TH]
        roots=[]
        for i in range(720):
            a,b=vals[i],vals[(i+1)%720]
            if a is None or b is None: continue
            if a[3]*b[3]<0 and a[2]<0 and b[2]<0:
                lo=TH[i]; hi=TH[i]+2*mp.pi/720
                f=lambda t:(chainK(t,uu,hh,k,True) or [None]*4)[3]
                try:
                    th=mp.findroot(f,(lo+hi)/2,solver='secant',tol=mp.mpf(10)**-90)
                except Exception:
                    fa=vals[i][3]
                    for _ in range(170):
                        mid=(lo+hi)/2; qm=chainK(mid,uu,hh,k,True)
                        if qm is None: break
                        if fa*qm[3]<0: hi=mid
                        else: lo=mid; fa=qm[3]
                    th=(lo+hi)/2
                q=chainK(th,uu,hh,k,True)
                if q is not None and abs(q[3])<mp.mpf(10)**-40 and q[2]<0:
                    roots.append((mp.nstr(th,50),str(uu_r)))
        return (str(uu_r),roots)
    if __name__=='__main__' or True:
        import mpmath as mp; mp.mp.dps=60
        pool=MP.get_context('fork').Pool(12,initializer=worker_init)
        emit("== ARM W: k=2 principal shooting ==")
        F2=dict(pool.map(u_witnesses,[(uu,1,2) for uu in GU]))
        tot=0;violP=0;unres=0;exb=0;mmin=None;ext2=[];allw=[]
        for uu_r in GU:
            key=str(uu_r); R=F2[key]
            if R: ext2.append(uu_r)
            for ths,_ in R:
                tot+=1; th=mp.mpf(ths); um=mp.mpf(sp.N(uu_r,60))
                m=2*mp.cos(th)+(um*um-1)/(um*um+1)-1
                if abs(m)<mp.mpf(10)**-6:
                    if uu_r==0 and abs(th)<mp.mpf(10)**-40: exb+=1  # PROVEN: inverted-equilibrium fixed point, margin==0 exact, satisfies <=
                    else: unres+=1
                elif m>0: violP+=1
                mmin=m if mmin is None else (m if abs(m)<abs(mmin) else mmin)
                allw.append((key,ths))
        emit(f"[W/k2] principal witnesses={tot} over {len(ext2)} u-values; energy violations={violP} unresolved={unres} exact-boundary(PROVEN lemma)={exb}")
        emit(f"[W/k2] min |margin|={mp.nstr(abs(mmin),4) if mmin is not None else '-'}; extent u=[{min(ext2) if ext2 else '-'},{max(ext2) if ext2 else '-'}]")
        emit("== PB.2 backward ==")
        B2=dict(pool.map(u_witnesses,[(uu,-1,2) for uu in sorted(set(sp.Rational(k_) for k_,_ in [(w[0],0) for w in allw]))]))
        mism=0
        for key,ths in allw:
            th=mp.mpf(ths)
            if not any(abs(mp.mpf(t2s)-th)<mp.mpf(10)**-38 for t2s,_ in B2.get(key,[])): mism+=1
        emit(f"[W/k2] PB.2: {len(allw)} witnesses, backward mismatches={mism}")
        emit("== SP-2(a) k=1 comparator ==")
        F1=dict(pool.map(u_witnesses,[(uu,1,1) for uu in GU]))
        ext1=[uu for uu in GU if F1[str(uu)]]
        emit(f"[W] u-values with witnesses: k=1 {len(ext1)} (ext [{min(ext1) if ext1 else '-'},{max(ext1) if ext1 else '-'}]) | k=2 {len(ext2)}")
        pool.close()
        emit("== VERDICTS (Arm W) ==")
        emit(f"PB.1' (CERTIFIED-numeric, margin ledger): {'PASS' if violP==0 and unres==0 else ('KB.1 FIRED - HALT' if violP>0 else 'UNRESOLVED -> Will')}")
        emit(f"SP-2(a) wider at k=2: {len(ext2)>len(ext1)}")
        emit(f"SP-2(b): {violP==0}")
        emit(f"SP-2(c): {mism==0}")
        blob="\n".join(OUT).encode()
        print("RESULTS-SHA256:",hashlib.sha256(blob).hexdigest())
        tick("done")
else:
    # ARM T: symbolic tower, u-chart, ledger per level
    W =lambda t:((1-t**2)/(1+t**2),2*t/(1+t**2))
    WU=lambda t:((t**2-1)/(1+t**2),2*t/(1+t**2))
    prm={g:10,h:HV,pi1:0,pi2:0}
    wc1,ws1=W(x1); wc2,ws2=WU(u)
    ac1,as1=W(ta); ac2,as2=WU(tb)
    zc1,zs1=W(t2)
    s01={c1:wc1,s1:ws1,c2:wc2,s2:ws2,C1:ac1,S1:as1,C2:ac2,S2:as2}
    s12={c1:ac1,s1:as1,c2:ac2,s2:as2,C1:zc1,S1:zs1,C2:-1,S2:0}
    E1=sp.expand(sp.fraction(sp.together((h*G1).subs(prm).subs(s01)))[0])
    E2=sp.expand(sp.fraction(sp.together((h*G2).subs(prm).subs(s01)))[0])
    PU1=P1u.subs(NUM).subs({h:HV}).subs(s01); PU2=P2u.subs(NUM).subs({h:HV}).subs(s01)
    E3=sp.expand(sp.fraction(sp.together((h*(G1.subs({pi1:PU1}))).subs(prm).subs(s12)))[0])
    E4=sp.expand(sp.fraction(sp.together((h*(G2.subs({pi2:PU2}))).subs(prm).subs(s12)))[0])
    def strip(EE,vars_,tag):
        gg=sp.gcd(sp.Poly(EE[0],*vars_),sp.Poly(EE[1],*vars_)).as_expr()
        if gg!=1:
            for fac,m in sp.factor_list(gg)[1]:
                s_=fac.free_symbols
                ok=(len(s_)==1 and fac==1+list(s_)[0]**2)
                tick(f"{tag} shared ({fac})^{m} {'corner' if ok else 'ANOMALY'}")
                assert ok
            EE=[sp.expand(sp.cancel(e/gg)) for e in EE]
        return EE
    tick(f"E degs t2:{[sp.degree(E3,t2),sp.degree(E4,t2)]} tb:{[sp.degree(e,tb) for e in (E1,E2,E3,E4)]} ta:{[sp.degree(e,ta) for e in (E1,E2,E3,E4)]}")
    E3,E4=strip([E3,E4],(t2,ta,tb,x1,u),'L1')
    tick("L1: res_t2(E3,E4)")
    R34=sp.expand(sp.resultant(sp.Poly(E3,t2),sp.Poly(E4,t2)).as_expr() if isinstance(E3,sp.Expr) else 0)
    tick(f"L1 done: degs ta={sp.degree(R34,ta)} tb={sp.degree(R34,tb)} x1={sp.degree(R34,x1)} u={sp.degree(R34,u)} terms={len(sp.Poly(R34,ta,tb,x1,u).terms())}")
    E1,R34=strip([E1,R34],(ta,tb,x1,u),'L2a'); E2b,R34b=strip([E2,R34],(ta,tb,x1,u),'L2b')
    tick("L2: res_tb(E1,E2), res_tb(E1,R34)")
    A=sp.expand(sp.resultant(sp.Poly(E1,tb),sp.Poly(E2b,tb)).as_expr())
    tick(f"L2 A done: ta={sp.degree(A,ta)} x1={sp.degree(A,x1)} u={sp.degree(A,u)}")
    B=sp.expand(sp.resultant(sp.Poly(E1,tb),sp.Poly(R34b,tb)).as_expr())
    tick(f"L2 B done: ta={sp.degree(B,ta)} x1={sp.degree(B,x1)} u={sp.degree(B,u)}")
    A,B=strip([A,B],(ta,x1,u),'L3')
    tick("L3: res_ta(A,B)")
    R=sp.expand(sp.resultant(sp.Poly(A,ta),sp.Poly(B,ta)).as_expr())
    tick(f"L3 done: x1={sp.degree(R,x1)} u={sp.degree(R,u)}")
    F=sp.factor_list(R)
    tick("factored")
    for fac,m in F[1]:
        print("FACTOR deg(x1,u)=",sp.degree(fac,x1),sp.degree(fac,u),"mult",m)
    tick("tower complete")
