# stageB_k2.py -- Stage B rung k=2 (PREREG v2 pin 96b3e09c, predecl pin 3a675143)
# Arm W: principal-chain shooting witnesses (default). Arm T: symbolic tower ('tower').
import sympy as sp, hashlib, time, sys
import mpmath as mp
T0=time.time(); OUT=[]
K=int(sys.argv[1]) if len(sys.argv)>1 else 3
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


import multiprocessing as MP, os
NF=4*K*K+16
GU=[sp.Rational(n,4000) for n in range(-NF,NF+1)]+[sp.Rational(n,40) for n in list(range(-20,0))+list(range(1,21))]
GU=sorted(set(GU))
if os.environ.get('SMOKE'): GU=[sp.Rational(n,4000) for n in (-4*K*K,-2,0,2,4*K*K)]
def worker_init():
    global fS,fJ,fP,gS,gJ,gP,mp,math
    import mpmath as mp, math
    mp.mp.dps=60
    Y=(C1,S1,C2,S2)
    SYS=[e.subs(NUM) for e in (G1,G2,C1**2+S1**2-1,C2**2+S2**2-1)]
    Jm=sp.Matrix(SYS).jacobian(Y)
    A=(c1,s1,c2,s2,pi1,pi2,h)+Y
    fS=sp.lambdify(A,SYS,'mpmath',cse=True); fJ=sp.lambdify(A,Jm,'mpmath',cse=True)
    fP=sp.lambdify((c1,s1,c2,s2,h)+Y,[e.subs(NUM) for e in (P1u,P2u)],'mpmath',cse=True)
    gS=sp.lambdify(A,SYS,'math',cse=True); gJ=sp.lambdify(A,Jm.tolist(),'math',cse=True)
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
def fchain(th,uu,hh,k):
    import math
    q0=(math.cos(th),math.sin(th),(uu*uu-1)/(uu*uu+1),2*uu/(uu*uu+1))
    qp=None; p=(0.0,0.0); q=q0
    for j in range(1,k+1):
        seed=list(q) if qp is None else [2*q[i]-qp[i] for i in range(4)]
        y=list(seed)
        for it in range(40):
            Fv=gS(*q,*p,hh,*y)
            if max(abs(t) for t in Fv)<1e-13: break
            d=fsolve4([list(r) for r in gJ(*q,*p,hh,*y)],[-t for t in Fv])
            y=[y[i]+d[i] for i in range(4)]
        mo=max(abs(y[i]-q[i]) for i in range(4))
        if not (max(abs(t) for t in gS(*q,*p,hh,*y))<1e-11 and mo<=2*(20*(j-1)+10)/1600): return None
        p=gP(*q,hh,*y); qp=q; q=tuple(y)
    return q
def mchain(th,uu,hh,k):
    with mp.workdps(60):
        q0=(mp.cos(th),mp.sin(th),(uu*uu-1)/(uu*uu+1),2*uu/(uu*uu+1))
        qp=None; p=(mp.mpf(0),mp.mpf(0)); q=q0
        for j in range(1,k+1):
            seed=list(q) if qp is None else [2*q[i]-qp[i] for i in range(4)]
            y=list(seed); last=mp.inf
            for it in range(90):
                Fv=mp.matrix(fS(*q,*p,hh,*y)); Jv=mp.matrix(fJ(*q,*p,hh,*y))
                d=mp.lu_solve(Jv,-Fv); y=[y[i]+d[i] for i in range(4)]
                last=max(abs(t) for t in d)
                if last<mp.mpf(10)**-55: break
            r=max(abs(t) for t in mp.matrix(fS(*q,*p,hh,*y)))
            mo=max(abs(y[i]-q[i]) for i in range(4))
            if not (r<=mp.mpf(10)**-45 and mo<=mp.mpf(2*(20*(j-1)+10))/1600 and last<=mp.mpf(10)**-20): return None
            p=fP(*q,hh,*y); qp=q; q=tuple(y)
        return q
def u_witnesses(args):
    uu_r,hs,k=args
    uu=mp.mpf(sp.N(uu_r,60)); hh=mp.mpf(hs)/40
    fu=float(uu); fh=hs/40.0
    TH=[-mp.pi+2*mp.pi*(i+mp.mpf(1)/2)/720 for i in range(720)]
    vals=[fchain(float(t),fu,fh,k) for t in TH]
    roots=[]
    for i in range(720):
        a,b=vals[i],vals[(i+1)%720]
        if a is None or b is None: continue
        if a[3]*b[3]<0 and a[2]<0 and b[2]<0:
            lo=TH[i]; hi=TH[i]+2*mp.pi/720
            f=lambda t:(mchain(t,uu,hh,k) or [None]*4)[3]
            try: th=mp.findroot(f,(lo+hi)/2,solver='secant',tol=mp.mpf(10)**-90)
            except Exception:
                fa=vals[i][3]
                for _ in range(170):
                    mid=(lo+hi)/2; qm=mchain(mid,uu,hh,k)
                    if qm is None: break
                    if fa*qm[3]<0: hi=mid
                    else: lo=mid; fa=qm[3]
                th=(lo+hi)/2
            q=mchain(th,uu,hh,k)
            if q is not None and abs(q[3])<mp.mpf(10)**-40 and q[2]<0:
                roots.append(mp.nstr(th,50))
    return (str(uu_r),roots)
if True:
    import mpmath as mp; mp.mp.dps=60
    pool=MP.get_context('fork').Pool(12,initializer=worker_init)
    emit(f"== LADDER rung k={K} ==")
    F=dict(pool.map(u_witnesses,[(uu,1,K) for uu in GU]))
    tot=0;violP=0;unres=0;exb=0;mmin=None;ext=[];allw=[]
    for uu_r in GU:
        R=F[str(uu_r)]
        if R: ext.append(uu_r)
        for ths in R:
            tot+=1; th=mp.mpf(ths); um=mp.mpf(sp.N(uu_r,60))
            m=2*mp.cos(th)+(um*um-1)/(um*um+1)-1
            if abs(m)<mp.mpf(10)**-6:
                if uu_r==0 and abs(th)<mp.mpf(10)**-40: exb+=1
                else: unres+=1
            elif m>0: violP+=1
            mmin=m if mmin is None else (m if abs(m)<abs(mmin) else mmin)
            allw.append((str(uu_r),ths))
    w=max(abs(x) for x in ext) if ext else 0
    emit(f"[k={K}] witnesses={tot} u-values={len(ext)} half-width w={w} = {sp.nsimplify(w*4000)}/4000")
    emit(f"[k={K}] violations={violP} unresolved={unres} exact-boundary={exb}")
    B=dict(pool.map(u_witnesses,[(sp.Rational(kk),-1,K) for kk in sorted(set(k0 for k0,_ in allw))]))
    mism=sum(0 if any(abs(mp.mpf(t)-mp.mpf(ths))<mp.mpf(10)**-38 for t in B.get(k0,[])) else 1 for k0,ths in allw)
    emit(f"[k={K}] PB.2 backward mismatches={mism}/{tot}")
    pool.close()
    emit(f"VERDICT PB.1': {'PASS' if violP==0 and unres==0 else ('KB.1 FIRED - HALT' if violP>0 else 'UNRESOLVED -> Will')}")
    emit(f"VERDICT PB.2: {'PASS' if mism==0 else 'KB.2 FIRED - HALT'}")
    blob="\n".join(OUT).encode()
    print("RESULTS-SHA256:",hashlib.sha256(blob).hexdigest())
    tick("done")
