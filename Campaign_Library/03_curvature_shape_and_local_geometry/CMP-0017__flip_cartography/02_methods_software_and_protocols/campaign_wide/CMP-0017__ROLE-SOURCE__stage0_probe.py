import sympy as sp, time
c1,s1,c2,s2, C1,S1,C2,S2 = sp.symbols('c1 s1 c2 s2 C1 S1 C2 S2')
pi1,pi2, h,g = sp.symbols('pi1 pi2 h g')
q0 = sp.Matrix([c1,s1,c2,s2]); q1 = sp.Matrix([C1,S1,C2,S2])
qb=(q0+q1)/2; v=(q1-q0)/h
om = lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2 = om(0,qb,v), om(1,qb,v); cD = qb[0]*qb[2]+qb[1]*qb[3]
Ld = h*(w1**2 + sp.Rational(1,2)*w2**2 + w1*w2*cD + g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
G1 = pi1 + (D1[0]*(-s1)+D1[1]*c1); G2 = pi2 + (D1[2]*(-s2)+D1[3]*c2)
hG1,hG2 = sp.expand(sp.cancel(h*G1)), sp.expand(sp.cancel(h*G2))

# second consistency point (different torus point + rates)
D2=[sp.cancel(sp.diff(Ld,x)) for x in (C1,S1,C2,S2)]
P1 = D2[0]*(-S1)+D2[1]*C1; P2 = D2[2]*(-S2)+D2[3]*C2
hP1,hP2 = sp.expand(sp.cancel(h*P1)), sp.expand(sp.cancel(h*P2))
a1,a2 = sp.symbols('a1 a2')
tr = {C1: c1*(1-(h*a1)**2/2)-s1*(h*a1), S1: s1*(1-(h*a1)**2/2)+c1*(h*a1),
      C2: c2*(1-(h*a2)**2/2)-s2*(h*a2), S2: s2*(1-(h*a2)**2/2)+c2*(h*a2)}
pt2 = {c1:sp.Rational(-8,17), s1:sp.Rational(15,17), c2:sp.Rational(-7,25), s2:sp.Rational(24,25), g:10}
cD0=(c1*c2+s1*s2).subs(pt2); picont={pi1:2*a1+a2*cD0, pi2:a2+a1*cD0}
res=[]
for e,tgt in ((hG1,None),(hG2,None),(hP1,picont[pi1]),(hP2,picont[pi2])):
    f=sp.expand(e.subs(tr).subs(pt2).subs(picont))
    if tgt is not None: f=sp.expand(f-h*tgt)
    res.append(sp.simplify(sp.expand(f.coeff(h,1)))==0)
print("CHECK2b consistency at 2nd exact point:", all(res), res)

# per-step algebraic solve at frozen rationals
num = {c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),
       pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,10)}
gens=[sp.expand(hG1.subs(num)), sp.expand(hG2.subs(num)), C1**2+S1**2-1, C2**2+S2**2-1]
t0=time.time(); GB=sp.groebner(gens,C1,S1,C2,S2,order='lex'); t1=time.time()
uni=[p for p in GB.exprs if len(p.free_symbols)==1]
d=[sp.Poly(p,list(p.free_symbols)[0]).degree() for p in uni]
print(f"TOOLING per-step lex GB: {t1-t0:.2f}s | basis {len(GB.exprs)} | univariate elim degrees {d}")
