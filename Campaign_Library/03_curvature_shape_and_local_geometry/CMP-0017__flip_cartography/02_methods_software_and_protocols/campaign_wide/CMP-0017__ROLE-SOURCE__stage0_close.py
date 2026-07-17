import sympy as sp, mpmath as mp, numpy as np, time
c1,s1,c2,s2, C1,S1,C2,S2 = sp.symbols('c1 s1 c2 s2 C1 S1 C2 S2')
pi1,pi2,h,g = sp.symbols('pi1 pi2 h g'); t1,t2=sp.symbols('t1 t2')
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
D2=[sp.cancel(sp.diff(Ld,x)) for x in (C1,S1,C2,S2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
P1o=D2[0]*(-S1)+D2[1]*C1; P2o=D2[2]*(-S2)+D2[3]*C2
gv=10.0
argsF=(c1,s1,c2,s2,pi1,pi2,C1,S1,C2,S2,h,g)
F=sp.lambdify(argsF,[hG1,hG2,C1**2+S1**2-1,C2**2+S2**2-1],'numpy')
J=sp.lambdify(argsF,[[sp.diff(e,x) for x in (C1,S1,C2,S2)] for e in [hG1,hG2,C1**2+S1**2-1,C2**2+S2**2-1]],'numpy')
Pout=sp.lambdify(argsF,[P1o*h,P2o*h],'numpy')  # h-cleared; divide back
def Minv(cd): d=2-cd*cd; return np.array([[1,-cd],[-cd,2]])/d
def step(st,hh):
    q=st[:4]; pi=st[4:]
    cd=q[0]*q[2]+q[1]*q[3]; omg=Minv(cd)@pi
    a1,a2=omg*hh
    guess=np.array([q[0]*np.cos(a1)-q[1]*np.sin(a1), q[1]*np.cos(a1)+q[0]*np.sin(a1),
                    q[2]*np.cos(a2)-q[3]*np.sin(a2), q[3]*np.cos(a2)+q[2]*np.sin(a2)])
    x=guess.copy()
    for _ in range(60):
        r=np.array(F(*q,*pi,*x,hh,gv),float)
        if np.max(np.abs(r))<1e-13: break
        x=x-np.linalg.solve(np.array(J(*q,*pi,*x,hh,gv),float),r)
    pn=np.array(Pout(*q,*pi,*x,hh,gv),float)/hh
    return np.concatenate([x,pn]), np.max(np.abs(np.array(F(*q,*pi,*x,hh,gv),float)))
def energy(st):
    q=st[:4]; pi=st[4:]; cd=q[0]*q[2]+q[1]*q[3]
    return 0.5*pi@ (Minv(cd)@pi) - gv*(2*q[0]+q[2])

# --- membership: physical branch of the census point lies among the 32 ---
cen=np.array([3/5,4/5,5/13,12/13,1/3,-1/7]); hh=0.1
xn,_=step(cen,hh)
tt1=xn[1]/(1+xn[0]); tt2=xn[3]/(1+xn[2])
numQ={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,10)}
W={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
Pa=sp.expand(sp.fraction(sp.together(hG1.subs(numQ).subs(W)))[0]); Pb=sp.expand(sp.fraction(sp.together(hG2.subs(numQ).subs(W)))[0])
GB=sp.groebner([Pa,Pb],t1,t2,order='lex')
uni=[p.as_expr() for p in GB.polys if p.free_symbols<={t2}][0]
fu=sp.lambdify(t2,uni,'mpmath'); mp.mp.dps=40
# refine (t1,t2) to high precision via mpmath newton on the pair
Fmp=sp.lambdify((t1,t2),[Pa,Pb],'mpmath'); Jmp=sp.lambdify((t1,t2),[[sp.diff(Pa,t1),sp.diff(Pa,t2)],[sp.diff(Pb,t1),sp.diff(Pb,t2)]],'mpmath')
x1,x2=mp.mpf(tt1),mp.mpf(tt2)
for _ in range(50):
    r=mp.matrix(Fmp(x1,x2)); Jm=mp.matrix(Jmp(x1,x2))
    d=mp.lu_solve(Jm,r); x1,x2=x1-d[0],x2-d[1]
    if max(abs(r[0]),abs(r[1]))<mp.mpf('1e-60'): break
scale=abs(sp.lambdify(t2,sp.diff(uni,t2),'mpmath')(x2))*abs(x2)+1
print("PHYSICAL-BRANCH MEMBERSHIP: |uni(t2*)| / scale =", mp.nstr(abs(fu(x2))/scale,3), " (tiny => the physical branch is one of the 32)")

# --- high-precision root sanity on 6 roots (fixing yesterday's conditioning trap) ---
rts=mp.polyroots([mp.mpf(str(cf)) for cf in sp.Poly(uni,t2).all_coeffs()],maxsteps=200,extraprec=200)
oth=[p.as_expr() for p in GB.polys if p is not GB.polys[0]] 
other=[p.as_expr() for p in GB.polys if sp.degree(p.as_expr(),t1)==1][0]
acf=sp.lambdify(t2,sp.Poly(other,t1).coeff_monomial(t1),'mpmath'); bcf=sp.lambdify(t2,other-sp.Poly(other,t1).coeff_monomial(t1)*t1,'mpmath')
ok=0
f1mp=sp.lambdify((t1,t2),Pa,'mpmath'); f2mp=sp.lambdify((t1,t2),Pb,'mpmath')
for r in rts[:6]:
    tv1=-bcf(r)/acf(r)
    res=max(abs(f1mp(tv1,r)),abs(f2mp(tv1,r)))
    sc=1+abs(r)**8
    ok+= (res/sc < mp.mpf('1e-25'))
print(f"root sanity (40 dps, relative): {ok}/6 pass")

# --- h-scan / diagnostics ---
th1,th2=2.2,2.9
ic=np.array([np.cos(th1),np.sin(th1),np.cos(th2),np.sin(th2),0,0]); E0=energy(ic)
print(f"IC gate check 2c1+c2 = {2*ic[0]+ic[2]:.3f} (<1 => flip-capable) | E0={E0:.4f}")
print(f"{'h':>7} {'steps':>6} {'maxRelEdrift':>13} {'maxConstr':>10} {'reversErr':>10} {'1stFlipStep':>11} {'1stFlipTime':>11}")
for hh in [1/5,1/10,1/20,1/40]:
    N=int(round(10/hh)); st=ic.copy(); mx=0; mc=0; flip=None
    prev=st.copy()
    for k in range(1,N+1):
        st,cr=step(st,hh); mc=max(mc,cr)
        mx=max(mx,abs(energy(st)-E0)/abs(E0))
        if flip is None and prev[3]*st[3]<0 and prev[2]<0 and st[2]<0: flip=k
        prev=st.copy()
    # reversibility: negate pi, run back N, negate pi, compare
    rb=st.copy(); rb[4:]=-rb[4:]
    for k in range(N): rb,_=step(rb,hh)
    rb[4:]=-rb[4:]
    rev=np.max(np.abs(rb-ic))
    print(f"{hh:7.4f} {N:6d} {mx:13.2e} {mc:10.1e} {rev:10.1e} {str(flip):>11} {('%.3f'%(flip*hh)) if flip else '—':>11}")
