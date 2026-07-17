import sympy as sp, time
c1,s1,c2,s2, C1,S1,C2,S2 = sp.symbols('c1 s1 c2 s2 C1 S1 C2 S2')
pi1,pi2, h,g = sp.symbols('pi1 pi2 h g')
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),
     pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,10)}
f1,f2=sp.expand(hG1.subs(num)),sp.expand(hG2.subs(num))
p1,p2=sp.expand(C1**2+S1**2-1),sp.expand(C2**2+S2**2-1)
t0=time.time()
A=sp.resultant(f1,p2,S2); B=sp.resultant(f2,p2,S2)
Cc=sp.resultant(A,p1,S1); Dd=sp.resultant(B,p1,S1)
E=sp.expand(sp.resultant(Cc,Dd,C2))
t1=time.time()
P=sp.Poly(E,C1); Efac=sp.factor_list(P.as_expr())
print(f"resultant chain: {t1-t0:.1f}s | deg of C1-eliminant = {P.degree()}")
print("factor degrees:", [(sp.Poly(f,C1).degree(),m) for f,m in Efac[1]])
rts=sp.Poly(E,C1).nroots(n=15, maxsteps=200)
real=[r for r in rts if abs(sp.im(r))<1e-9 and -1-1e-9<=sp.re(r)<=1+1e-9]
print(f"roots: {len(rts)} total | real in [-1,1]: {len(real)}")
