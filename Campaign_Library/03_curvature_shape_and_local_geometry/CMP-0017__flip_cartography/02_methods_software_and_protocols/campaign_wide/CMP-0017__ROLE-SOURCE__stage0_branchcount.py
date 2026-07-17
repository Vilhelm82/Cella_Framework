import sympy as sp, time
c1,s1,c2,s2, C1,S1,C2,S2 = sp.symbols('c1 s1 c2 s2 C1 S1 C2 S2')
pi1,pi2,h,g = sp.symbols('pi1 pi2 h g')
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),
     pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,10)}
t1,t2=sp.symbols('t1 t2')
W={C1:(1-t1**2)/(1+t1**2), S1:2*t1/(1+t1**2), C2:(1-t2**2)/(1+t2**2), S2:2*t2/(1+t2**2)}
P1=sp.expand(sp.fraction(sp.together(hG1.subs(num).subs(W)))[0])
P2=sp.expand(sp.fraction(sp.together(hG2.subs(num).subs(W)))[0])
print("bivariate degrees: P1", (sp.degree(P1,t1),sp.degree(P1,t2)), " P2", (sp.degree(P2,t1),sp.degree(P2,t2)))
t0=time.time()
GB=sp.groebner([P1,P2],t1,t2,order='lex')
print(f"lex GB (bivariate): {time.time()-t0:.1f}s, basis {len(GB.exprs)}")
# zero-dim check + quotient dimension via staircase
LTs=[sp.LT(p,order='lex') for p in GB.polys]
lt=[(sp.Poly(m,t1,t2).monoms()[0]) for m in LTs]
d1=min(a for a,b in lt if b==0) if any(b==0 for a,b in lt) else None
d2=min(b for a,b in lt if a==0) if any(a==0 for a,b in lt) else None
if d1 is not None and d2 is not None:
    std=[(i,j) for i in range(d1) for j in range(d2) if not any(i>=a and j>=b for a,b in lt)]
    print("zero-dimensional: quotient dim (complex count w/ mult) =", len(std))
uni=[p.as_expr() for p in GB.polys if p.free_symbols<= {t2}]
if uni:
    U=sp.Poly(sp.factor(uni[0]),t2)
    Usf=sp.Poly(sp.prod([f for f,m in sp.factor_list(U.as_expr())[1]]),t2)
    print("univariate eliminant deg:", U.degree(), "| squarefree deg (distinct t2):", Usf.degree())
    rr=sp.real_roots(Usf.as_expr(),t2)
    print("real t2 roots:", len(rr))
    # for each real t2, count real t1 partners via gcd of P1,P2 specialized
    import mpmath as mp
    mp.mp.dps=40
    total=0; sols=[]
    for r in rr:
        rv=sp.nsimplify(r, rational=False)
        p1s=sp.Poly(P1.subs(t2, r), t1); p2s=sp.Poly(P2.subs(t2, r), t1)
        gcd=sp.gcd(p1s,p2s)
        rt1=sp.real_roots(gcd.as_expr(), t1) if gcd.degree()>0 else []
        total+=len(rt1)
        for a in rt1: sols.append((a,r))
    print("REAL branch count (t-chart) =", total)
    # excluded Weierstrass points C_i=-1: check directly on original system
    for tag,subs_x in (("C1=-1",{C1:-1,S1:0}),("C2=-1",{C2:-1,S2:0})):
        f1x=sp.expand(hG1.subs(num).subs(subs_x)); f2x=sp.expand(hG2.subs(num).subs(subs_x))
        rem=[C2,S2] if "C1" in tag else [C1,S1]
        phi=rem[0]**2+rem[1]**2-1
        R=sp.resultant(sp.resultant(f1x,phi,rem[1]), sp.resultant(f2x,phi,rem[1]), rem[0])
        print(f"excluded chart {tag}: consistency resultant zero? {sp.simplify(R)==0}")
