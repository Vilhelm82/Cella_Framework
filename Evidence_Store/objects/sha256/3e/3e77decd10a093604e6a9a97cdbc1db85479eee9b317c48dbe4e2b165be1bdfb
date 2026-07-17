import sympy as sp, mpmath as mp, numpy as np
mp.mp.dps=25
exec(open('stageA_k2c.py').read().split("num={")[0])
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,40)}
Wt={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
Wu={A1:(1-u1**2)/(1+u1**2),B1:2*u1/(1+u1**2),A2:(1-u2**2)/(1+u2**2),B2:2*u2/(1+u2**2)}
Pa=sp.expand(sp.fraction(sp.together(hG1.subs(num).subs(Wt)))[0]); Pb=sp.expand(sp.fraction(sp.together(hG2.subs(num).subs(Wt)))[0])
GB=sp.groebner([Pa,Pb],t1,t2,order='lex')
uniq=[q.as_expr() for q in GB.polys if q.free_symbols<={t2}][0]
oth=[q.as_expr() for q in GB.polys if sp.degree(q.as_expr(),t1)==1][0]
U30q=sp.cancel(uniq/(t2**2+1))
acf=sp.lambdify(t2,sp.Poly(oth,t1).coeff_monomial(t1),'mpmath'); bcf=sp.lambdify(t2,(oth-sp.Poly(oth,t1).coeff_monomial(t1)*t1),'mpmath')
outer=mp.polyroots([mp.mpf(str(c)) for c in sp.Poly(U30q,t2).all_coeffs()],maxsteps=300,extraprec=160)
F1=sp.expand(sp.fraction(sp.together(E5_1.subs(num).subs(Wt).subs(Wu)))[0])
F2=sp.expand(sp.fraction(sp.together(E5_2.subs(num).subs(Wt).subs(Wu)))[0])
f1n=sp.lambdify((t1,t2,u1,u2),F1,'numpy'); f2n=sp.lambdify((t1,t2,u1,u2),F2,'numpy')
g1u=sp.lambdify((t1,t2,u1,u2),sp.diff(F1,u1),'numpy'); g1v=sp.lambdify((t1,t2,u1,u2),sp.diff(F1,u2),'numpy')
g2u=sp.lambdify((t1,t2,u1,u2),sp.diff(F2,u1),'numpy'); g2v=sp.lambdify((t1,t2,u1,u2),sp.diff(F2,u2),'numpy')
CM1=[[sp.lambdify((t1,t2),sp.expand(F1).coeff(u1,i).coeff(u2,j),'numpy') for j in range(5)] for i in range(5)]
CM2=[[sp.lambdify((t1,t2),sp.expand(F2).coeff(u1,i).coeff(u2,j),'numpy') for j in range(5)] for i in range(5)]
def sylv(a,b):
    M=np.zeros((8,8),complex)
    for i in range(4): M[i,i:i+5]=a
    for i in range(4): M[4+i,i:i+5]=b
    return np.linalg.det(M)
print(f"{'br':>3} {'real':>5} {'|t2|':>8} {'ghosts':>6} {'honest':>6}")
tot=0; realtot=0; deficits=[]
for bi,r2m in enumerate(outer):
    r1m=-bcf(r2m)/acf(r2m); r1,r2=complex(r1m),complex(r2m)
    isreal=abs(r2.imag)<1e-20
    M1=np.array([[CM1[i][j](r1,r2) for j in range(5)] for i in range(5)]); M1/=np.max(np.abs(M1))
    M2=np.array([[CM2[i][j](r1,r2) for j in range(5)] for i in range(5)]); M2/=np.max(np.abs(M2))
    P2s=lambda x,y: sum(M2[i,j]*x**i*y**j for i in range(5) for j in range(5))
    xs=1.07*np.exp(1j*np.linspace(0.11,2*np.pi+0.11,33,endpoint=False))
    ys=[sylv(np.array([sum(M1[i,j]*x**j for j in range(5)) for i in range(4,-1,-1)]),
             np.array([sum(M2[i,j]*x**j for j in range(5)) for i in range(4,-1,-1)])) for x in xs]
    co=np.linalg.solve(np.vander(xs,33,increasing=False),np.array(ys))
    while len(co)>1 and abs(co[0])<1e-10*np.max(np.abs(co)): co=co[1:]
    roots=np.roots(co)
    gh=sum(1 for w in roots if min(abs(w-1j),abs(w+1j))<1e-5)
    found=[]
    for w2 in roots:
        if min(abs(w2-1j),abs(w2+1j))<1e-5: continue
        aco=np.array([sum(M1[i,j]*w2**j for j in range(5)) for i in range(4,-1,-1)])
        for w1 in np.roots(aco):
            if abs(P2s(w1,w2))/((1+abs(w1))**4*(1+abs(w2))**4)>1e-3: continue
            x,y=w1,w2; conv=False
            for it in range(80):
                r=np.array([f1n(r1,r2,x,y),f2n(r1,r2,x,y)])
                J=np.array([[g1u(r1,r2,x,y),g1v(r1,r2,x,y)],[g2u(r1,r2,x,y),g2v(r1,r2,x,y)]])
                try: dd=np.linalg.solve(J,r)
                except np.linalg.LinAlgError: break
                x,y=x-dd[0],y-dd[1]
                if max(abs(dd[0]),abs(dd[1]))<1e-13*(1+abs(x)+abs(y)): conv=True; break
            if not conv: continue
            if min(abs(y-1j),abs(y+1j))<1e-5 or min(abs(x-1j),abs(x+1j))<1e-5: continue
            if any(abs(x-fx)<1e-9 and abs(y-fy)<1e-9 for fx,fy in found): continue
            found.append((x,y))
    nreal=sum(1 for (x,y) in found if abs(x.imag)<1e-9 and abs(y.imag)<1e-9) if isreal else 0
    tot+=len(found); realtot+=nreal
    if len(found)<30: deficits.append((bi,isreal,len(found)))
    print(f"{bi:>3} {str(isreal):>5} {abs(r2):8.2f} {gh:>6} {len(found):>6}" + (f"  real-chains {nreal}" if isreal else ""))
print(f"TOTAL found {tot}/900 | real chains {realtot} | deficient branches: {deficits}")
