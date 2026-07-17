import sympy as sp, mpmath as mp, time
c1,s1,c2,s2, C1,S1,C2,S2 = sp.symbols('c1 s1 c2 s2 C1 S1 C2 S2')
pi1,pi2,h,g = sp.symbols('pi1 pi2 h g'); t1,t2=sp.symbols('t1 t2')
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),
     pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,10)}
f1n,f2n = hG1.subs(num), hG2.subs(num)
W={C1:(1-t1**2)/(1+t1**2), S1:2*t1/(1+t1**2), C2:(1-t2**2)/(1+t2**2), S2:2*t2/(1+t2**2)}
P1=sp.expand(sp.fraction(sp.together(f1n.subs(W)))[0]); P2=sp.expand(sp.fraction(sp.together(f2n.subs(W)))[0])
GB=sp.groebner([P1,P2],t1,t2,order='lex')
e1,e2 = GB.polys[0].as_expr(), GB.polys[1].as_expr()
uni = e1 if sp.degree(e1,t1)==0 else e2
other = e2 if uni is e1 else e1
print("shape position: deg_t1(other) =", sp.degree(other,t1), "| eliminant deg_t2 =", sp.degree(uni,t2))
if sp.degree(other,t1)==1:
    # t1 = -b(t2)/a(t2): real t2 root with a(t2)!=0 -> unique real t1 partner
    nreal = len(sp.real_roots(uni,t2))
    a=sp.Poly(other,t1).coeff_monomial(t1)
    common = sp.gcd(sp.Poly(a,t2), sp.Poly(uni,t2))
    print("REAL branch count =", nreal, "(shape lemma; leading-coeff gcd deg:", sp.degree(common.as_expr(),t2),")")
# excluded charts (t=oo <-> C=-1)
for tag,sx,rem in (("C1=-1",{C1:-1,S1:0},(C2,S2)),("C2=-1",{C2:-1,S2:0},(C1,S1))):
    g1x=sp.expand(f1n.subs(sx)); g2x=sp.expand(f2n.subs(sx)); phi=rem[0]**2+rem[1]**2-1
    r1=sp.resultant(g1x,phi,rem[1]); r2=sp.resultant(g2x,phi,rem[1])
    R=sp.gcd(sp.Poly(r1,rem[0]), sp.Poly(r2,rem[0]))
    print(f"excluded chart {tag}: gcd degree {sp.degree(R.as_expr(),rem[0])} (0 => no solutions at infinity chart)")
# numeric sanity: verify 3 roots satisfy the ORIGINAL 4-var system
mp.mp.dps=30
rts=sp.nroots(sp.Poly(uni,t2), n=25)
b=sp.Poly(other,t1)
cnt=0
for r in rts[:6]:
    t1v = sp.nsimplify(0)  # placeholder
    aa = complex(sp.Poly(other,t1).coeff_monomial(t1).subs(t2, r))
    bb = complex((other - sp.Poly(other,t1).coeff_monomial(t1)*t1).subs(t2, r))
    t1v = -bb/aa
    r2c=complex(r)
    Cc1=(1-t1v**2)/(1+t1v**2); Ss1=2*t1v/(1+t1v**2)
    Cc2=(1-r2c**2)/(1+r2c**2); Ss2=2*r2c/(1+r2c**2)
    res=[abs(complex(f.subs({C1:Cc1,S1:Ss1,C2:Cc2,S2:Ss2}))) for f in (f1n,f2n)]
    cnt += (max(res)<1e-15)
print(f"root sanity: {cnt}/6 sampled roots satisfy original system to <1e-15")
