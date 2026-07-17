import sympy as sp
c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2')
pi1,pi2,h,g=sp.symbols('pi1 pi2 h g'); t=sp.Symbol('t'); I=sp.I
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
# fixed pullback lemma check (cancel BEFORE substituting)
a0,b0,c0=sp.symbols('a0 b0 c0')
q=a0*C2**2+b0*C2*S2+c0*S2**2
pb=sp.cancel((1+t**2)**2*q.subs({C2:(1-t**2)/(1+t**2),S2:2*t/(1+t**2)}))
print("pullback lemma ((1+t²)²·q)|_{t=i} = 4·q(1,i):", sp.simplify(pb.subs(t,I)-4*q.subs({C2:1,S2:I}))==0)
# bidegree-(2,2) parts, FULLY SYMBOLIC data, evaluated at the four isotropic corners
def corner(F, e1, e2):
    P=sp.Poly(F,C1,S1,C2,S2); tot=0
    for m,cf in zip(P.monoms(),P.coeffs()):
        if m[0]+m[1]==2 and m[2]+m[3]==2:
            tot+=cf*(1)**m[0]*(e1*I)**m[1]*(1)**m[2]*(e2*I)**m[3]
    return sp.simplify(sp.expand(tot))
for nm,F in (("hG1",hG1),("hG2",hG2)):
    for e1,e2 in ((1,1),(-1,-1),(1,-1),(-1,1)):
        val=corner(F,e1,e2)
        tag="ZERO" if val==0 else "nonzero"
        print(f"{nm} corner ((1,{e1}i),(1,{e2}i)): {tag}" + (f" = {sp.factor(val)}" if val!=0 else ""))
# the structural factor: show the (2,2)-part carries (C1C2+S1S2)
for nm,F in (("hG1",hG1),("hG2",hG2)):
    P=sp.Poly(F,C1,S1,C2,S2)
    part=sum(cf*C1**m[0]*S1**m[1]*C2**m[2]*S2**m[3] for m,cf in zip(P.monoms(),P.coeffs()) if m[0]+m[1]==2 and m[2]+m[3]==2)
    quo,rem=sp.div(sp.Poly(part,C1,S1,C2,S2), sp.Poly(C1*C2+S1*S2,C1,S1,C2,S2))
    print(f"{nm}: (C1C2+S1S2) divides its (2,2)-part:", rem.is_zero, "| quotient:", sp.factor(quo.as_expr()) if rem.is_zero else "—")
