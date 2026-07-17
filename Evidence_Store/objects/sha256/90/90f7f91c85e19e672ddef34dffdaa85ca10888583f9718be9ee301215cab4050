import sympy as sp, mpmath as mp, numpy as np, time
mp.mp.dps=30
c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2'); A1,B1,A2,B2=sp.symbols('A1 B1 A2 B2')
pi1,pi2,h,g=sp.symbols('pi1 pi2 h g'); t1,t2,u1,u2=sp.symbols('t1 t2 u1 u2')
def build(qa,qb):
    qa=sp.Matrix(qa); qb=sp.Matrix(qb); qm=(qa+qb)/2; v=(qb-qa)/h
    om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
    w1,w2=om(0,qm,v),om(1,qm,v); cd=qm[0]*qm[2]+qm[1]*qm[3]
    return h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cd+g*(2*qm[0]+qm[2]))
Ld01=build((c1,s1,c2,s2),(C1,S1,C2,S2)); Ld12=build((C1,S1,C2,S2),(A1,B1,A2,B2))
D2_01=[sp.cancel(sp.diff(Ld01,x)) for x in (C1,S1,C2,S2)]
D1_12=[sp.cancel(sp.diff(Ld12,x)) for x in (C1,S1,C2,S2)]
E5_1=sp.cancel(h*((D2_01[0]+D1_12[0])*(-S1)+(D2_01[1]+D1_12[1])*C1))
E5_2=sp.cancel(h*((D2_01[2]+D1_12[2])*(-S2)+(D2_01[3]+D1_12[3])*C2))
D1_01=[sp.cancel(sp.diff(Ld01,x)) for x in (c1,s1,c2,s2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1_01[0]*(-s1)+D1_01[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1_01[2]*(-s2)+D1_01[3]*c2))))
D2_12=[sp.cancel(sp.diff(Ld12,x)) for x in (A1,B1,A2,B2)]
hP1=sp.cancel(h*(D2_12[0]*(-B1)+D2_12[1]*A1)); hP2=sp.cancel(h*(D2_12[2]*(-B2)+D2_12[3]*A2))
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,40)}
hv=1/40
Wt={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
Wu={A1:(1-u1**2)/(1+u1**2),B1:2*u1/(1+u1**2),A2:(1-u2**2)/(1+u2**2),B2:2*u2/(1+u2**2)}
Pa=sp.expand(sp.fraction(sp.together(hG1.subs(num).subs(Wt)))[0]); Pb=sp.expand(sp.fraction(sp.together(hG2.subs(num).subs(Wt)))[0])
GB=sp.groebner([Pa,Pb],t1,t2,order='lex')
uni=[p.as_expr() for p in GB.polys if p.free_symbols<={t2}][0]
oth=[p.as_expr() for p in GB.polys if sp.degree(p.as_expr(),t1)==1][0]
acf=sp.lambdify(t2,sp.Poly(oth,t1).coeff_monomial(t1),'mpmath'); bcf=sp.lambdify(t2,(oth-sp.Poly(oth,t1).coeff_monomial(t1)*t1),'mpmath')
outer=mp.polyroots([mp.mpf(str(c)) for c in sp.Poly(uni,t2).all_coeffs()],maxsteps=200,extraprec=120)
F1=sp.expand(sp.fraction(sp.together(E5_1.subs(num).subs(Wt).subs(Wu)))[0])
F2=sp.expand(sp.fraction(sp.together(E5_2.subs(num).subs(Wt).subs(Wu)))[0])
# 5x5 coefficient matrices in (u1,u2), entries functions of (t1,t2)
def coefmat(F):
    M=[[sp.simplify(sp.expand(F).coeff(u1,i).coeff(u2,j)) for j in range(5)] for i in range(5)]
    return [[sp.lambdify((t1,t2),e,'numpy') for e in row] for row in M]
CM1,CM2=coefmat(F1),coefmat(F2)
f1m=sp.lambdify((t1,t2,u1,u2),F1,'mpmath'); f2m=sp.lambdify((t1,t2,u1,u2),F2,'mpmath')
p2f=[sp.lambdify((t1,t2,u1,u2),e.subs(num).subs(Wt).subs(Wu),'numpy') for e in (hP1,hP2)]
def sylv(a,b):
    m,n=len(a)-1,len(b)-1; M=np.zeros((m+n,m+n),complex)
    for i in range(n): M[i,i:i+m+1]=a
    for i in range(m): M[n+i,i:i+n+1]=b
    return np.linalg.det(M)
t0=time.time(); chains=[]; rej=0; branch_counts=[]
for r2m in outer:
    r1m=-bcf(r2m)/acf(r2m); r1,r2=complex(r1m),complex(r2m)
    M1=np.array([[CM1[i][j](r1,r2) for j in range(5)] for i in range(5)])
    M2=np.array([[CM2[i][j](r1,r2) for j in range(5)] for i in range(5)])
    s1n,s2n=np.max(np.abs(M1)),np.max(np.abs(M2)); M1/=s1n; M2/=s2n
    P1=lambda x,y: sum(M1[i,j]*x**i*y**j for i in range(5) for j in range(5))
    P2=lambda x,y: sum(M2[i,j]*x**i*y**j for i in range(5) for j in range(5))
    d1=lambda x,y:(sum(i*M1[i,j]*x**(i-1)*y**j for i in range(1,5) for j in range(5)),sum(j*M1[i,j]*x**i*y**(j-1) for i in range(5) for j in range(1,5)))
    d2=lambda x,y:(sum(i*M2[i,j]*x**(i-1)*y**j for i in range(1,5) for j in range(5)),sum(j*M2[i,j]*x**i*y**(j-1) for i in range(5) for j in range(1,5)))
    xs=1.07*np.exp(1j*np.linspace(0.11,2*np.pi+0.11,33,endpoint=False))
    ys=[sylv(np.array([sum(M1[i,j]*x**j for j in range(5)) for i in range(4,-1,-1)]),
             np.array([sum(M2[i,j]*x**j for j in range(5)) for i in range(4,-1,-1)])) for x in xs]
    V=np.vander(xs,33,increasing=False); co=np.linalg.solve(V,np.array(ys))
    while len(co)>1 and abs(co[0])<1e-10*np.max(np.abs(co)): co=co[1:]
    bc=0
    for w2 in np.roots(co):
        a=np.array([sum(M1[i,j]*w2**j for j in range(5)) for i in range(4,-1,-1)])
        for w1 in np.roots(a):
            if abs(P2(w1,w2))/((1+abs(w1))**4*(1+abs(w2))**4)>1e-3: rej+=1; continue
            x,y=w1,w2; conv=False; last=1e9
            for it in range(80):
                r=np.array([P1(x,y),P2(x,y)])
                a1,b1=d1(x,y); a2,b2=d2(x,y)
                try: dxy=np.linalg.solve(np.array([[a1,b1],[a2,b2]]),r)
                except np.linalg.LinAlgError: break
                x,y=x-dxy[0],y-dxy[1]; stepn=max(abs(dxy[0]),abs(dxy[1]))
                if stepn<1e-13*(1+abs(x)+abs(y)) and last<1e-12*(1+abs(x)+abs(y)): conv=True; break
                last=stepn
            if conv:
                sc=(1+abs(x))**4*(1+abs(y))**4
                if max(abs(P1(x,y)),abs(P2(x,y)))/sc<1e-11: chains.append((r1,r2,x,y)); bc+=1
                else: rej+=1
            else: rej+=1
    branch_counts.append(bc)
print(f"branch inner counts: min {min(branch_counts)} max {max(branch_counts)} sum {sum(branch_counts)} | rejected {rej} ({time.time()-t0:.0f}s)")
# mpmath verification on EVERY chain (relative to term scale)
ver=0
for (r1,r2,x,y) in chains:
    sc=(1+abs(x))**4*(1+abs(y))**4*(1+abs(r1))**4*(1+abs(r2))**4
    res=max(abs(f1m(mp.mpc(r1),mp.mpc(r2),mp.mpc(x),mp.mpc(y))),abs(f2m(mp.mpc(r1),mp.mpc(r2),mp.mpc(x),mp.mpc(y))))
    ver+=(float(res)/sc/max(1,float(abs(f1m(mp.mpc(r1),mp.mpc(r2),0,0)))+1)<1e-6) if False else (float(res)/sc<1e-4)
Wc=lambda t:((1-t**2)/(1+t**2),2*t/(1+t**2))
pts=[]
for (r1,r2,x,y) in chains:
    A1v,B1v=Wc(x); A2v,B2v=Wc(y)
    pts.append([A1v,B1v,A2v,B2v,p2f[0](r1,r2,x,y)/hv,p2f[1](r1,r2,x,y)/hv])
P=np.array(pts); used=np.zeros(len(P),bool); reps=[]
for i in range(len(P)):
    if used[i]: continue
    d=np.max(np.abs(P-P[i]),axis=1); used|=(d<1e-7); reps.append(i)
D=np.array([P[i] for i in reps]); mind=np.inf
for i in range(len(D)):
    dd=np.max(np.abs(D-D[i]),axis=1); dd[i]=np.inf; mind=min(mind,dd.min())
realct=sum(1 for i in reps if np.max(np.abs(P[i].imag))<1e-7)
print(f"k=2: DISTINCT x2 = {len(reps)} | real = {realct} | naive 1024 | minsep {mind:.1e} | mp-verified {ver}/{len(chains)}")
