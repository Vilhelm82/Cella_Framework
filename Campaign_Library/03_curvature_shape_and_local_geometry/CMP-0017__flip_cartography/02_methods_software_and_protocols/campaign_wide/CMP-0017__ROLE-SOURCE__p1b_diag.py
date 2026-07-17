import sympy as sp, mpmath as mp, numpy as np
mp.mp.dps=30
c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2')
pi1,pi2,h,g,gam=sp.symbols('pi1 pi2 h g gamma'); t1,t2,r1s,r2s=sp.symbols('t1 t2 r1 r2')
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
D2=[sp.cancel(sp.diff(Ld,x)) for x in (C1,S1,C2,S2)]
W1=c1*S1-s1*C1; W2=c2*S2-s2*C2
hG1c=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1)))); hG2c=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
hP1c=sp.expand(sp.cancel(h*(D2[0]*(-S1)+D2[1]*C1)));       hP2c=sp.expand(sp.cancel(h*(D2[2]*(-S2)+D2[3]*C2)))
hG1=sp.expand(hG1c-(gam*h/2)*W1); hG2=sp.expand(hG2c-(gam*h/2)*W2)
hP1=sp.expand(hP1c-(gam*h/2)*W1); hP2=sp.expand(hP2c-(gam*h/2)*W2)
swap={c1:C1,s1:S1,c2:C2,s2:S2,C1:c1,S1:s1,C2:c2,S2:s2}
# corrected defect: hP(swap) - (hG - h*pi)
for i,(hp,hg,pv,Wv) in enumerate(((hP1,hG1,pi1,W1),(hP2,hG2,pi2,W2)),1):
    d=sp.expand(hp.subs(swap,simultaneous=True)-(hg-h*pv))
    print(f"defect_{i} == gamma*h*W{i}:", sp.expand(d-gam*h*Wv)==0)
# residual test: does the TRUE conservative chain satisfy my backward equations?
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,40),gam:0}
F=[sp.lambdify((C1,S1,C2,S2),e.subs(num),'mpmath') for e in (hG1,hG2)]
Pouts=[sp.lambdify((C1,S1,C2,S2),e.subs(num),'mpmath') for e in (hP1,hP2)]
# physical forward chain via mp Newton (guess=small rotation)
Jl=[[sp.lambdify((C1,S1,C2,S2),sp.diff(e.subs(num),x),'mpmath') for x in (C1,S1,C2,S2)] for e in (hG1,hG2,C1**2+S1**2-1,C2**2+S2**2-1)]
Fl=F+[sp.lambdify((C1,S1,C2,S2),C1**2+S1**2-1,'mpmath'),sp.lambdify((C1,S1,C2,S2),C2**2+S2**2-1,'mpmath')]
X=mp.matrix([mp.mpf('0.6'),mp.mpf('0.8'),mp.mpf(5)/13,mp.mpf(12)/13])
for _ in range(60):
    r=mp.matrix([f(*X) for f in Fl]); J=mp.matrix(4,4)
    for a in range(4):
        for b in range(4): J[a,b]=Jl[a][b](*X)
    d=mp.lu_solve(J,r); X=X-d
    if mp.norm(r)<mp.mpf('1e-40'): break
p1v=Pouts[0](*X)/mp.mpf(1)*40; p2v=Pouts[1](*X)*40
print("forward chain found, |res|:", mp.nstr(mp.norm(mp.matrix([f(*X) for f in Fl])),3), "| pi1',pi2' =", mp.nstr(p1v,8), mp.nstr(p2v,8))
# BACKWARD eqs at data (q1=X, pi'=(p1v,p2v)) must be satisfied by q0=basepoint:
datB={C1:X[0],C2:X[2],S1:X[1],S2:X[3]}
B1=hP1.subs(num).subs({C1:sp.Float(str(X[0]),30),S1:sp.Float(str(X[1]),30),C2:sp.Float(str(X[2]),30),S2:sp.Float(str(X[3]),30)})-sp.Rational(1,40)*sp.Float(str(p1v),30)
B2=hP2.subs(num).subs({C1:sp.Float(str(X[0]),30),S1:sp.Float(str(X[1]),30),C2:sp.Float(str(X[2]),30),S2:sp.Float(str(X[3]),30)})-sp.Rational(1,40)*sp.Float(str(p2v),30)
r1v=float(B1.subs({c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13)}))
r2v=float(B2.subs({c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13)}))
print("backward-eq residuals at the true q0:", r1v, r2v, " (tiny => backward formulation correct)")
# root-set comparison of the two deg-30 polys from the failed control
Wt={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
Wr={c1:(1-r1s**2)/(1+r1s**2),s1:2*r1s/(1+r1s**2),c2:(1-r2s**2)/(1+r2s**2),s2:2*r2s/(1+r2s**2)}
def elim(e1,e2,chart,ef,kp):
    Pa=sp.expand(sp.fraction(sp.together(e1.subs(chart)))[0]); Pb=sp.expand(sp.fraction(sp.together(e2.subs(chart)))[0])
    GB=sp.groebner([Pa,Pb],ef,kp,order='lex')
    return [q_.as_expr() for q_ in GB.polys if q_.free_symbols<={kp}][0]
dat0={**{k:v for k,v in num.items()}, }
B1s=sp.expand(hP1.subs(num)); B2s=sp.expand(hP2.subs(num))  # WRONG data slot? -> rebuild properly:
datq1={C1:sp.Rational(3,5),S1:sp.Rational(4,5),C2:sp.Rational(5,13),S2:sp.Rational(12,13),g:10,h:sp.Rational(1,40),gam:0}
Bb1=sp.expand(hP1.subs(datq1)-sp.Rational(1,40)*sp.Rational(1,3))
Bb2=sp.expand(hP2.subs(datq1)-sp.Rational(1,40)*sp.Rational(-1,7))
Ub=elim(Bb1,Bb2,Wr,r1s,r2s)
numR={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(-1,3),pi2:sp.Rational(1,7),g:10,h:sp.Rational(1,40),gam:0}
UfR=elim(hG1.subs(numR),hG2.subs(numR),Wt,t1,t2)
u30b=sp.div(sp.Poly(Ub,r2s),sp.Poly(r2s**2+1,r2s))[0]
u30f=sp.div(sp.Poly(UfR,t2),sp.Poly(t2**2+1,t2))[0]
rb=sorted([complex(z) for z in mp.polyroots([mp.mpf(str(c)) for c in u30b.all_coeffs()],maxsteps=200,extraprec=120)],key=lambda z:(z.real,z.imag))
rf=sorted([complex(z) for z in mp.polyroots([mp.mpf(str(c)) for c in u30f.all_coeffs()],maxsteps=200,extraprec=120)],key=lambda z:(z.real,z.imag))
md=max(abs(a-b) for a,b in zip(rb,rf))
print(f"gamma=0 root-set comparison (bwd vs fwd@Rx): max matched distance = {md:.2e}")
