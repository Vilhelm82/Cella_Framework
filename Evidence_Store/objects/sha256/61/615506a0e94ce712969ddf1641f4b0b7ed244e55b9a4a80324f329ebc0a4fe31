import sympy as sp
c1,s1,c2,s2, C1,S1,C2,S2 = sp.symbols('c1 s1 c2 s2 C1 S1 C2 S2')
pi1,pi2,h,g = sp.symbols('pi1 pi2 h g'); t1,t2 = sp.symbols('t1 t2')
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
N=sp.expand(sp.cancel(h*Ld))

# P1a mechanism, part 1: PLAIN EXCHANGE symmetry at fixed h (stronger than adjointness)
swap2={c1:C1,s1:S1,c2:C2,s2:S2,C1:c1,S1:s1,C2:c2,S2:s2}   # h FIXED
print("EXCHANGE  L_d(q1,q0,h) == L_d(q0,q1,h) :", sp.expand(N.subs(swap2,simultaneous=True)-N)==0)

# part 2: the reversed-step identities  <D1Ld(q1,q0),xi(q1)> == <D2Ld(q0,q1),xi(q1)>  (both i)
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
D2=[sp.cancel(sp.diff(Ld,x)) for x in (C1,S1,C2,S2)]
ok=[]
for j in range(4):
    lhs = D1[j].subs(swap2, simultaneous=True)   # D1 L_d evaluated at (q1,q0)
    ok.append(sp.expand(sp.cancel(h*(lhs - D2[j])))==0)
print("REVERSAL  D1Ld(q1,q0) == D2Ld(q0,q1) componentwise :", all(ok), ok)

# ---- genericity: 1-step census at FROZEN h=1/40, two independent basepoints ----
W={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
def census(pt):
    Pa=sp.expand(sp.fraction(sp.together(hG1.subs(pt).subs(W)))[0])
    Pb=sp.expand(sp.fraction(sp.together(hG2.subs(pt).subs(W)))[0])
    GB=sp.groebner([Pa,Pb],t1,t2,order='lex')
    uni=[p.as_expr() for p in GB.polys if p.free_symbols<={t2}][0]
    oth=[p.as_expr() for p in GB.polys if sp.degree(p.as_expr(),t1)==1]
    shape=len(oth)==1
    d=sp.degree(uni,t2); sf=sp.Poly(sp.prod([f for f,m in sp.factor_list(uni)[1]]),t2).degree()
    nr=len(sp.real_roots(uni,t2)) if shape else None
    return d,sf,nr,shape
base={g:10, h:sp.Rational(1,40)}
pA={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),**base}
pB={c1:sp.Rational(-20,29),s1:sp.Rational(21,29),c2:sp.Rational(-9,41),s2:sp.Rational(40,41),pi1:sp.Rational(2,5),pi2:sp.Rational(3,11),**base}
for nm,pt in (("basepoint A (Stage-0 pt, h=1/40)",pA),("basepoint B (fresh, h=1/40)",pB)):
    d,sf,nr,shape=census(pt)
    print(f"CENSUS {nm}: eliminant deg {d} | squarefree {sf} | real {nr} | shape {shape}")
