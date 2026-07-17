import sympy as sp
c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2')
pi1,pi2,h,g=sp.symbols('pi1 pi2 h g'); t1,t2=sp.symbols('t1 t2'); I=sp.I
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,40)}
G1,G2=sp.expand(hG1.subs(num)),sp.expand(hG2.subs(num))
def blockdeg(F,vars2):
    P=sp.Poly(F,*vars2); return max(sum(m[:len(vars2)]) for m in P.monoms())
for nm,F in (("hG1",G1),("hG2",G2)):
    print(nm,"block degrees: circ1 =",blockdeg(F,(C1,S1)),", circ2 =",blockdeg(F,(C2,S2)))
# 0) pullback identity, verified generically
a0,b0,c0=sp.symbols('a0 b0 c0'); t=sp.Symbol('t')
q=a0*C2**2+b0*C2*S2+c0*S2**2
pb=sp.expand((1+t**2)**2*q.subs({C2:(1-t**2)/(1+t**2),S2:2*t/(1+t**2)}))
print("pullback identity ((1+t²)²·q)|_{t=i} == 4·q(1,i):", sp.simplify(pb.subs(t,I)-4*q.subs({C2:1,S2:I}))==0)
# 1) circle-2 leading forms at the isotropic vector
def lead_iso(F, blockvars, iso):
    P=sp.Poly(F,*blockvars); d=max(sum(m[:2]) for m in P.monoms())
    top=sum(cf*sp.prod([blockvars[i]**m[i] for i in range(2)]) for m,cf in zip(P.monoms(),P.coeffs()) if sum(m[:2])==d)
    return d, sp.expand(top.subs({blockvars[0]:iso[0],blockvars[1]:iso[1]}))
d21,L1=lead_iso(G1,(C2,S2),(1,I)); d22,L2=lead_iso(G2,(C2,S2),(1,I))
print("circ2-leading degrees:",d21,d22)
L1r,L1i=sp.re(sp.expand(L1)),sp.im(sp.expand(L1)); L2r,L2i=sp.re(sp.expand(L2)),sp.im(sp.expand(L2))
# ghost system over t2=+i: {L1=0, L2=0, C1²+S1²=1} — complex system; count via resultants over C[.]
R1=sp.resultant(sp.expand(L1),C1**2+S1**2-1,S1); R2=sp.resultant(sp.expand(L2),C1**2+S1**2-1,S1)
Gg=sp.gcd(sp.Poly(R1,C1),sp.Poly(R2,C1))
print("circle-2 ghost count over t2=+i (deg of gcd of C1-resultants):", sp.degree(Gg.as_expr(),C1))
sol=sp.solve([sp.expand(L1),sp.expand(L2),C1**2+S1**2-1],[C1,S1],dict=True)
print("ghost circle-1 point(s):", sol)
if sol:
    C1v,S1v=sol[0][C1],sol[0][S1]
    t1g=sp.simplify(S1v/(1+C1v))
    print("mapped ghost t1 =", sp.nsimplify(t1g), "=", complex(t1g))
# cross-check against shape position: t1 = -b(i)/a(i)
Wt={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
Pa=sp.expand(sp.fraction(sp.together(G1.subs(Wt)))[0]); Pb=sp.expand(sp.fraction(sp.together(G2.subs(Wt)))[0])
GB=sp.groebner([Pa,Pb],t1,t2,order='lex')
oth=[q_.as_expr() for q_ in GB.polys if sp.degree(q_.as_expr(),t1)==1][0]
av=sp.Poly(oth,t1).coeff_monomial(t1); bv=oth-av*t1
t1_shape=sp.simplify((-bv/av).subs(t2,I))
print("shape-position t1 over t2=i:", sp.nsimplify(t1_shape), "| match:", sp.simplify(t1_shape-t1g)==0 if sol else "n/a")
# 2) circle-1 side: leading forms at (C1,S1)=(1,i) -> predicted t1-ghosts
d11,M1=lead_iso(G1,(C1,S1),(1,I)); d12,M2=lead_iso(G2,(C1,S1),(1,I))
print("circ1-leading degrees:",d11,d12)
Rm1=sp.resultant(sp.expand(M1),C2**2+S2**2-1,S2); Rm2=sp.resultant(sp.expand(M2),C2**2+S2**2-1,S2)
Gm=sp.gcd(sp.Poly(Rm1,C2),sp.Poly(Rm2,C2))
print("circle-1 ghost count over t1=+i (gcd degree):", sp.degree(Gm.as_expr(),C2))
# direct check: t1-eliminant factorization
GB2=sp.groebner([Pa,Pb],t2,t1,order='lex')
uni1=[q_.as_expr() for q_ in GB2.polys if q_.free_symbols<={t1}][0]
fl=sp.factor_list(uni1)
print("t1-eliminant factor degrees:", [(sp.degree(f,t1),m) for f,m in fl[1]], "| (t1²+1) divides:", any(sp.expand(f-(t1**2+1))==0 for f,m in fl[1]))
# 3) corner ghosts: bidegree-(2,2) coefficient at both isotropic vectors
P22=sp.Poly(G1,C1,S1,C2,S2)
corner1=sum(cf*sp.prod([sp.Matrix([1,I,1,I])[i]**m[i] for i in range(4)]) for m,cf in zip(P22.monoms(),P22.coeffs()) if sum(m[:2])==d11 and sum(m[2:])==d21)
print("hG1 corner ((1,i),(1,i)) leading value:", sp.simplify(corner1), "(nonzero => no corner ghosts from G1)")
# 4) basepoint B: T²+1 | U_B ?
numB={c1:sp.Rational(-20,29),s1:sp.Rational(21,29),c2:sp.Rational(-9,41),s2:sp.Rational(40,41),pi1:sp.Rational(2,5),pi2:sp.Rational(3,11),g:10,h:sp.Rational(1,40)}
PaB=sp.expand(sp.fraction(sp.together(hG1.subs(numB).subs(Wt)))[0]); PbB=sp.expand(sp.fraction(sp.together(hG2.subs(numB).subs(Wt)))[0])
GBB=sp.groebner([PaB,PbB],t1,t2,order='lex')
uB=[q_.as_expr() for q_ in GBB.polys if q_.free_symbols<={t2}][0]
qq,rr=sp.div(sp.Poly(uB,t2),sp.Poly(t2**2+1,t2))
print("basepoint B: (t2²+1) | U_B :", rr.is_zero)
