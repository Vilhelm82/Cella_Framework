import sympy as sp, mpmath as mp
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
hG=[sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1)))-(gam*h/2)*W1),
    sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2)))-(gam*h/2)*W2)]
hP=[sp.expand(sp.cancel(h*(D2[0]*(-S1)+D2[1]*C1))-(gam*h/2)*W1),
    sp.expand(sp.cancel(h*(D2[2]*(-S2)+D2[3]*C2))-(gam*h/2)*W2)]
Wt={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
Wr={c1:(1-r1s**2)/(1+r1s**2),s1:2*r1s/(1+r1s**2),c2:(1-r2s**2)/(1+r2s**2),s2:2*r2s/(1+r2s**2)}
def elim(e1,e2,chart,ef,kp):
    Pa=sp.expand(sp.fraction(sp.together(e1.subs(chart)))[0]); Pb=sp.expand(sp.fraction(sp.together(e2.subs(chart)))[0])
    GB=sp.groebner([Pa,Pb],ef,kp,order='lex')
    return [q_.as_expr() for q_ in GB.polys if q_.free_symbols<={kp}][0]
base=dict(g=10); Q={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13)}
QU={C1:sp.Rational(3,5),S1:sp.Rational(4,5),C2:sp.Rational(5,13),S2:sp.Rational(12,13)}
for gv,tag in ((0,"CONTROL gamma=0"),(sp.Rational(1,10),"gamma=1/10")):
    com={g:10,h:sp.Rational(1,40),gam:gv}
    Bb=[sp.expand(hP[0].subs(com).subs(QU)-sp.Rational(1,40)*sp.Rational(1,3)),
        sp.expand(hP[1].subs(com).subs(QU)-sp.Rational(1,40)*sp.Rational(-1,7))]
    Ub=elim(Bb[0],Bb[1],Wr,r1s,r2s)
    fR=[e.subs(com).subs(Q).subs({pi1:sp.Rational(-1,3),pi2:sp.Rational(1,7)}) for e in hG]
    Uf=elim(fR[0],fR[1],Wt,t1,t2).subs(t2,r2s)
    mb=sp.Poly(Ub,r2s); mf=sp.Poly(Uf,r2s)
    mb=sp.Poly(mb/mb.LC(),r2s); mf=sp.Poly(mf/mf.LC(),r2s)
    eq=(mb-mf).is_zero
    hb=sp.div(mb,sp.Poly(r2s**2+1,r2s))[0]; hf=sp.div(mf,sp.Poly(r2s**2+1,r2s))[0]
    rb=mp.polyroots([mp.mpf(str(x)) for x in hb.all_coeffs()],maxsteps=200,extraprec=120)
    rf=mp.polyroots([mp.mpf(str(x)) for x in hf.all_coeffs()],maxsteps=200,extraprec=120)
    # greedy matched displacement
    rf2=list(rf); disp=[]
    for z in rb:
        j=min(range(len(rf2)),key=lambda k:abs(z-rf2[k])); disp.append(abs(z-rf2[j])); rf2.pop(j)
    disp=sorted([float(x) for x in disp])
    realb=len(sp.real_roots(hb.as_expr(),r2s)); realf=len(sp.real_roots(hf.as_expr(),r2s))
    print(f"{tag}: U^bwd(x) == U^fwd(Rx) exactly: {eq} | real bwd/fwd(R): {realb}/{realf} | root displacement min {disp[0]:.2e} median {disp[15]:.2e} max {disp[-1]:.2e}")
