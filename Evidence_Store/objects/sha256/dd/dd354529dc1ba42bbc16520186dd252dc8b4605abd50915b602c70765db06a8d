# stageB_fold.py -- fold-point extraction (FOLD_PREDECL pin cf95a3c9, PREREG v2 96b3e09c)
import sympy as sp, mpmath as mp, hashlib, time
T0=time.time(); OUT=[]
def emit(m): print(m,flush=True); OUT.append(m)
c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2')
pi1,pi2,h,g=sp.symbols('pi1 pi2 h g')
def build(qa,qb):
    qa=sp.Matrix(qa); qb=sp.Matrix(qb); qm=(qa+qb)/2; v=(qb-qa)/h
    om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
    w1,w2=om(0,qm,v),om(1,qm,v); cd=qm[0]*qm[2]+qm[1]*qm[3]
    return h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cd+g*(2*qm[0]+qm[2]))
Ld=build((c1,s1,c2,s2),(C1,S1,C2,S2))
D1=[sp.diff(Ld,v) for v in (c1,s1,c2,s2)]; D2=[sp.diff(Ld,v) for v in (C1,S1,C2,S2)]
G1=pi1+(D1[0]*(-s1)+D1[1]*c1); G2=pi2+(D1[2]*(-s2)+D1[3]*c2)
P1u=D2[0]*(-S1)+D2[1]*C1; P2u=D2[2]*(-S2)+D2[3]*C2
NUM={g:10}; Y=(C1,S1,C2,S2); A=(c1,s1,c2,s2,pi1,pi2,h)+Y
SYS=[e.subs(NUM) for e in (G1,G2,C1**2+S1**2-1,C2**2+S2**2-1)]
fS=sp.lambdify(A,SYS,'mpmath',cse=True)
fJ=sp.lambdify(A,sp.Matrix(SYS).jacobian(Y),'mpmath',cse=True)
fP=sp.lambdify((c1,s1,c2,s2,h)+Y,[e.subs(NUM) for e in (P1u,P2u)],'mpmath',cse=True)
def mchain(th,uu,k):
    hh=mp.mpf(1)/40
    q0=(mp.cos(th),mp.sin(th),(uu*uu-1)/(uu*uu+1),2*uu/(uu*uu+1))
    qp=None; p=(mp.mpf(0),mp.mpf(0)); q=q0
    for j in range(1,k+1):
        seed=list(q) if qp is None else [2*q[i]-qp[i] for i in range(4)]
        y=list(seed); last=mp.inf
        for it in range(120):
            Fv=mp.matrix(fS(*q,*p,hh,*y)); Jv=mp.matrix(fJ(*q,*p,hh,*y))
            d=mp.lu_solve(Jv,-Fv); y=[y[i]+d[i] for i in range(4)]
            last=max(abs(t) for t in d)
            if last<mp.mpf(10)**-70: break
        r=max(abs(t) for t in mp.matrix(fS(*q,*p,hh,*y)))
        mo=max(abs(y[i]-q[i]) for i in range(4))
        assert r<=mp.mpf(10)**-60 and mo<=mp.mpf(2*(20*(j-1)+10))/1600 and last<=mp.mpf(10)**-30, f"gate k={k} j={j}"
        p=fP(*q,hh,*y); qp=q; q=tuple(y)
    return q[3]  # s2 after k steps
def fold(k,th0,u0):
    HD=mp.mpf(10)**-30
    th,uu=mp.mpf(th0),mp.mpf(u0)
    F=lambda t,v:(mchain(t,v,k), (mchain(t+HD,v,k)-mchain(t-HD,v,k))/(2*HD))
    for it in range(60):
        f0,f1=F(th,uu)
        if abs(f0)<mp.mpf(10)**-40 and abs(f1)<mp.mpf(10)**-30: break
        j00=(mchain(th+HD,uu,k)-mchain(th-HD,uu,k))/(2*HD)
        j01=(mchain(th,uu+HD,k)-mchain(th,uu-HD,k))/(2*HD)
        j10=(mchain(th+2*HD,uu,k)-2*mchain(th,uu,k)+mchain(th-2*HD,uu,k))/(4*HD*HD)
        j11=((mchain(th+HD,uu+HD,k)-mchain(th-HD,uu+HD,k))-(mchain(th+HD,uu-HD,k)-mchain(th-HD,uu-HD,k)))/(4*HD*HD)
        det=j00*j11-j01*j10
        dth=(-f0*j11+f1*j01)/det; du=(-j00*f1+j10*f0)/det
        th+=dth; uu+=du
        if max(abs(dth),abs(du))<mp.mpf(10)**-50: break
    f0,f1=F(th,uu)
    return th,uu,abs(f0),abs(f1)
mp.mp.dps=80
seeds={1:(-0.9,0.00115),2:(-0.9,0.0044),3:(-0.9,0.0099),4:(-0.9,0.0177),5:(-0.9,0.0272)}
emit("== FOLD EXTRACTION k=1..7 ==")
banked={1:4,2:17,3:39,4:70,5:108}
us={}
ok_fp1=True; ok_fp2=True
for k in range(1,8):
    if k in seeds: th0,u0=seeds[k]
    else:
        # extrapolate u from fitted r(k) trend
        r5=4.5*25-us[5]*4000; r4=4.5*16-us[4]*4000
        rk=r5+(r5-r4)*(k-5)*1.8
        u0=float((4.5*k*k-rk)/4000); th0=-0.9
    th,uu,e0,e1=fold(k,th0,u0)
    us[k]=uu
    thm,um,e0m,e1m=fold(k,-th0,-u0)
    mir=abs(um+uu)
    fp2=mir<mp.mpf(10)**-35
    ok_fp2 &= fp2
    assert uu>0, f"converged to wrong edge k={k}"
    line=f"k={k} th*={mp.nstr(th,8)} u*={mp.nstr(uu,40)} 4000u*={mp.nstr(4000*uu,12)} |s2|={mp.nstr(e0,3)} |ds2|={mp.nstr(e1,3)} mirror_dev={mp.nstr(mir,3)}"
    if k in banked:
        fp1=(int(mp.floor(4000*uu))==banked[k])
        ok_fp1 &= fp1
        line+=f" floor={int(mp.floor(4000*uu))} banked={banked[k]} FP1={'OK' if fp1 else 'FAIL'}"
    emit(line)
emit("== FP-3: residual r(k)=4.5k^2-4000u* ==")
rs={}
for k in range(1,8):
    rs[k]=mp.mpf(4.5)*k*k-4000*us[k]
    emit(f"k={k} r={mp.nstr(rs[k],20)}")
inc=all(rs[k+1]>rs[k] for k in range(2,7)) and all(rs[k]>0 for k in range(2,8))
emit(f"FP-3 (r>0, increasing k>=2): {inc}")
emit("== FP-4: form identification ==")
for k in range(2,8):
    emit(f"k={k} r/k^3={mp.nstr(rs[k]/k**3,12)} r/k^4={mp.nstr(rs[k]/k**4,12)} (r-r_prev)/k^2={mp.nstr((rs[k]-rs[k-1])/k**2,10) if k>2 else '-'}")
emit(f"VERDICT FP-1: {'PASS' if ok_fp1 else 'FAIL - HALT'}  FP-2: {'PASS' if ok_fp2 else 'FAIL - HALT'}")
blob="\n".join(OUT).encode()
print("RESULTS-SHA256:",hashlib.sha256(blob).hexdigest())
print(f"[{time.time()-T0:.1f}s] done")
