import sympy as sp, mpmath as mp, numpy as np, time
mp.mp.dps=30
exec(open('stageA_k2c.py').read().split("num={")[0])  # rebuild symbols + E5/F machinery up to num
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,40)}
hv=1/40
Wt={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
Wu={A1:(1-u1**2)/(1+u1**2),B1:2*u1/(1+u1**2),A2:(1-u2**2)/(1+u2**2),B2:2*u2/(1+u2**2)}
Pa=sp.expand(sp.fraction(sp.together(hG1.subs(num).subs(Wt)))[0]); Pb=sp.expand(sp.fraction(sp.together(hG2.subs(num).subs(Wt)))[0])
GB=sp.groebner([Pa,Pb],t1,t2,order='lex')
uniq=[q.as_expr() for q in GB.polys if q.free_symbols<={t2}][0]
oth=[q.as_expr() for q in GB.polys if sp.degree(q.as_expr(),t1)==1][0]
T=t2
U30q=sp.simplify(sp.cancel(uniq/(t2**2+1)))
assert sp.degree(U30q,t2)==30 and sp.simplify(sp.expand(U30q*(t2**2+1)-uniq))==0
acf=sp.lambdify(t2,sp.Poly(oth,t1).coeff_monomial(t1),'mpmath'); bcf=sp.lambdify(t2,(oth-sp.Poly(oth,t1).coeff_monomial(t1)*t1),'mpmath')
outer=mp.polyroots([mp.mpf(str(c)) for c in sp.Poly(U30q,t2).all_coeffs()],maxsteps=200,extraprec=120)
print("honest outer roots:", len(outer))
F1=sp.expand(sp.fraction(sp.together(E5_1.subs(num).subs(Wt).subs(Wu)))[0])
F2=sp.expand(sp.fraction(sp.together(E5_2.subs(num).subs(Wt).subs(Wu)))[0])
f1n=sp.lambdify((t1,t2,u1,u2),F1,'numpy'); f2n=sp.lambdify((t1,t2,u1,u2),F2,'numpy')
g1u=sp.lambdify((t1,t2,u1,u2),sp.diff(F1,u1),'numpy'); g1v=sp.lambdify((t1,t2,u1,u2),sp.diff(F1,u2),'numpy')
g2u=sp.lambdify((t1,t2,u1,u2),sp.diff(F2,u1),'numpy'); g2v=sp.lambdify((t1,t2,u1,u2),sp.diff(F2,u2),'numpy')
c1s=[sp.lambdify((t1,t2,u2),e,'numpy') for e in sp.Poly(F1,u1).all_coeffs()]
c2s=[sp.lambdify((t1,t2,u2),e,'numpy') for e in sp.Poly(F2,u1).all_coeffs()]
D2_12=[sp.cancel(sp.diff(Ld12,x)) for x in (A1,B1,A2,B2)]
hP1=sp.cancel(h*(D2_12[0]*(-B1)+D2_12[1]*A1)); hP2=sp.cancel(h*(D2_12[2]*(-B2)+D2_12[3]*A2))
p2f=[sp.lambdify((t1,t2,u1,u2),e.subs(num).subs(Wt).subs(Wu),'numpy') for e in (hP1,hP2)]
def sylv(a,b):
    m,n=len(a)-1,len(b)-1; M=np.zeros((m+n,m+n),complex)
    for i in range(n): M[i,i:i+m+1]=a
    for i in range(m): M[n+i,i:i+n+1]=b
    return np.linalg.det(M)
t0=time.time(); chains=[]; ghost_per_branch=[]
for r2m in outer:
    r1m=-bcf(r2m)/acf(r2m); r1,r2=complex(r1m),complex(r2m)
    M1=np.array([[c(r1,r2,0) for c in []]]) if False else None
    xs=1.07*np.exp(1j*np.linspace(0.11,2*np.pi+0.11,33,endpoint=False))
    ys=[sylv(np.array([cf(r1,r2,x) for cf in c1s]),np.array([cf(r1,r2,x) for cf in c2s])) for x in xs]
    co=np.polyfit(xs,ys,32)
    while len(co)>1 and abs(co[0])<1e-10*np.max(np.abs(co)): co=co[1:]
    roots=np.roots(co)
    gh=[w for w in roots if min(abs(w-1j),abs(w+1j))<1e-6]
    ghost_per_branch.append(len(gh))
    for w2 in roots:
        if min(abs(w2-1j),abs(w2+1j))<1e-6: continue
        a=np.array([cf(r1,r2,w2) for cf in c1s])
        for w1 in np.roots(a):
            x,y=w1,w2; conv=False; 
            for it in range(80):
                r=np.array([f1n(r1,r2,x,y),f2n(r1,r2,x,y)])
                Jm=np.array([[g1u(r1,r2,x,y),g1v(r1,r2,x,y)],[g2u(r1,r2,x,y),g2v(r1,r2,x,y)]])
                try: d=np.linalg.solve(Jm,r)
                except np.linalg.LinAlgError: break
                x,y=x-d[0],y-d[1]
                if max(abs(d[0]),abs(d[1]))<1e-13*(1+abs(x)+abs(y)): conv=True; break
            if conv and min(abs(y-1j),abs(y+1j))>1e-6 and min(abs(x-1j),abs(x+1j))>1e-6:
                sc=(1+abs(x))**4*(1+abs(y))**4
                if max(abs(f1n(r1,r2,x,y)),abs(f2n(r1,r2,x,y)))/sc<1e-10: chains.append((r1,r2,x,y))
print(f"ghost inner roots per branch: min {min(ghost_per_branch)} max {max(ghost_per_branch)} (predict 2/2)")
Wc=lambda t:((1-t**2)/(1+t**2),2*t/(1+t**2))
pts=[]
for (r1,r2,x,y) in chains:
    A1v,B1v=Wc(x); A2v,B2v=Wc(y)
    pts.append([A1v,B1v,A2v,B2v,p2f[0](r1,r2,x,y)/hv,p2f[1](r1,r2,x,y)/hv])
P=np.array(pts); used=np.zeros(len(P),bool); reps=[]
for i in range(len(P)):
    if used[i]: continue
    d=np.max(np.abs(P-P[i]),axis=1); used|=(d<1e-8); reps.append(i)
D=np.array([P[i] for i in reps])
realct=sum(1 for i in reps if np.max(np.abs(P[i].imag))<1e-8)
mind=np.inf
for i in range(len(D)):
    dd=np.max(np.abs(D-D[i]),axis=1); dd[i]=np.inf; mind=min(mind,dd.min())
print(f"HONEST k=2: raw {len(chains)} | DISTINCT {len(reps)} (predict 900) | real {realct} | minsep {mind:.1e}")
names=['A1','B1','A2','B2','pi2_1','pi2_2']
for tol in (1e-6,1e-10):
    cnt=[]
    for cc in range(6):
        v=np.sort_complex(D[:,cc]); dist=1
        for i in range(1,len(v)):
            if abs(v[i]-v[i-1])>tol: dist+=1
        cnt.append(dist)
    print(f"per-coordinate distinct (tol {tol:.0e}):", dict(zip(names,cnt)))
np.save('/home/claude/k2_honest_reps.npy',D)
print(f"({time.time()-t0:.0f}s)")
