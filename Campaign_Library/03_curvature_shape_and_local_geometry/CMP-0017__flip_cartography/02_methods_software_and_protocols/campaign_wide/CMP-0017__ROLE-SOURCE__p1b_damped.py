import sympy as sp, time
T0=time.time()
c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2')
pi1,pi2,h,g,gam=sp.symbols('pi1 pi2 h g gamma'); t1,t2=sp.symbols('t1 t2'); I=sp.I
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
D2=[sp.cancel(sp.diff(Ld,x)) for x in (C1,S1,C2,S2)]
W1=c1*S1-s1*C1; W2=c2*S2-s2*C2   # discrete wedge = h*omega_d per circle
# DF-6: Rayleigh equal-joint damping in angle rates, midpoint discrete force, symmetric split
hG1c=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1)))); hG2c=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
hP1c=sp.expand(sp.cancel(h*(D2[0]*(-S1)+D2[1]*C1)));       hP2c=sp.expand(sp.cancel(h*(D2[2]*(-S2)+D2[3]*C2)))
hG1=sp.expand(hG1c-(gam*h/2)*W1); hG2=sp.expand(hG2c-(gam*h/2)*W2)
hP1=sp.expand(hP1c-(gam*h/2)*W1); hP2=sp.expand(hP2c-(gam*h/2)*W2)
# (1) reversal defect: swapped out-eq + in-eq (P1a identity kills the conservative part)
swap={c1:C1,s1:S1,c2:C2,s2:S2,C1:c1,S1:s1,C2:c2,S2:s2}
d1=sp.expand(hP1.subs(swap,simultaneous=True)+ (hG1 - h*pi1))
d2=sp.expand(hP2.subs(swap,simultaneous=True)+ (hG2 - h*pi2))
print("reversal defect (should be exactly the doubled force term):")
print("  delta_1 =", sp.factor(d1)); print("  delta_2 =", sp.factor(d2))
# (2) corner identity persists: (2,2)-parts of damped == conservative
def part22(F):
    P=sp.Poly(F,C1,S1,C2,S2)
    return sp.expand(sum(cf*C1**m[0]*S1**m[1]*C2**m[2]*S2**m[3] for m,cf in zip(P.monoms(),P.coeffs()) if m[0]+m[1]==2 and m[2]+m[3]==2))
print("damping preserves (2,2)-parts:", sp.expand(part22(hG1)-part22(hG1c))==0 and sp.expand(part22(hG2)-part22(hG2c))==0)
# (3) consistency spot-check of the damped assembly (truncated rotations, exact point)
a1,a2=sp.symbols('a1 a2')
tr={C1:c1*(1-(h*a1)**2/2)-s1*(h*a1), S1:s1*(1-(h*a1)**2/2)+c1*(h*a1),
    C2:c2*(1-(h*a2)**2/2)-s2*(h*a2), S2:s2*(1-(h*a2)**2/2)+c2*(h*a2)}
pt={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),g:10,gam:sp.Rational(1,10)}
cD0=(c1*c2+s1*s2).subs(pt); pic={pi1:2*a1+a2*cD0, pi2:a2+a1*cD0}
ok=[]
for e in (hG1,hG2):
    f=sp.expand(e.subs(tr).subs(pt).subs(pic))
    ok.append(sp.simplify(sp.expand(f.coeff(h,1)))==0)
# out-momentum drop should show -gamma*a_i at O(h): (P_out - pi_cont) coeff h^1 == -gamma*a_i * <xi,xi>? check numerically vs expected
outs=[]
for e,pc,aa in ((hP1,pic[pi1],a1),(hP2,pic[pi2],a2)):
    f=sp.expand(e.subs(tr).subs(pt)) - sp.expand(h*pc)
    lead=sp.simplify(sp.expand(f.coeff(h,2)))   # h*(P/h - pi) at O(h) -> coeff of h^2 in h-cleared
    outs.append(sp.factor(lead))
print("damped in-eq consistency at exact point:", all(ok), "| momentum-drop O(h) terms:", outs)
# (4) forward eliminant at gamma=1/10 (basepoint) + ghosts + honest + real
num={**pt, pi1:sp.Rational(1,3), pi2:sp.Rational(-1,7), h:sp.Rational(1,40)}
Wt={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
def eliminant(e1,e2,subsmap,chart,elimfirst,keep):
    Pa=sp.expand(sp.fraction(sp.together(e1.subs(subsmap).subs(chart)))[0])
    Pb=sp.expand(sp.fraction(sp.together(e2.subs(subsmap).subs(chart)))[0])
    GB=sp.groebner([Pa,Pb],elimfirst,keep,order='lex')
    return [q_.as_expr() for q_ in GB.polys if q_.free_symbols<={keep}][0]
Uf=eliminant(hG1,hG2,num,Wt,t1,t2)
q_,r_=sp.div(sp.Poly(Uf,t2),sp.Poly(t2**2+1,t2))
Uf30=q_
print(f"FWD gamma=1/10: deg {sp.degree(Uf,t2)} | T²+1 divides: {r_.is_zero} | honest deg {Uf30.degree()} | real {len(sp.real_roots(Uf30.as_expr(),t2))}")
# (5) backward system: unknown q0 (chart r), data (q1,pi1) — control at gamma=0 vs P1a identity, then gamma=1/10
r1s,r2s=sp.symbols('r1 r2')
Wr={c1:(1-r1s**2)/(1+r1s**2),s1:2*r1s/(1+r1s**2),c2:(1-r2s**2)/(1+r2s**2),s2:2*r2s/(1+r2s**2)}
# backward equations: hP_i(q0,q1) - h*pi1_i = 0 with (q1,pi1)=data
datB={C1:sp.Rational(3,5),S1:sp.Rational(4,5),C2:sp.Rational(5,13),S2:sp.Rational(12,13),g:10,h:sp.Rational(1,40)}
for gv,tag in ((0,"gamma=0 CONTROL"),(sp.Rational(1,10),"gamma=1/10")):
    dat={**datB, gam:gv, pi1:sp.Rational(1,3), pi2:sp.Rational(-1,7)}
    B1=sp.expand(hP1.subs(dat)-sp.Rational(1,40)*sp.Rational(1,3))
    B2=sp.expand(hP2.subs(dat)-sp.Rational(1,40)*sp.Rational(-1,7))
    Ub=eliminant(B1,B2,{},Wr,r1s,r2s)
    qb_,rb_=sp.div(sp.Poly(Ub,r2s),sp.Poly(r2s**2+1,r2s))
    # forward eliminant at the REVERSED point Rx=(q,-pi)
    numR={**datB, gam:gv, c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(-1,3),pi2:sp.Rational(1,7)}
    UfR=eliminant(hG1,hG2,numR,Wt,t1,t2)
    Pb_=sp.Poly(Ub,r2s); Pf_=sp.Poly(UfR.subs(t2,r2s),r2s)
    same=sp.expand(Pb_.as_expr()/Pb_.LC()-Pf_.as_expr()/Pf_.LC())==0
    print(f"BWD {tag}: deg {Pb_.degree()} | T²+1: {rb_.is_zero} | honest {qb_.degree()} | real {len(sp.real_roots(qb_.as_expr(),r2s))} | U^bwd(x) == U^fwd(Rx): {same}")
print(f"[{time.time()-T0:.0f}s]")
