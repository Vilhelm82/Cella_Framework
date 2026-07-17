import sympy as sp, numpy as np, flint, time
T0=time.time()
def tick(m): print(f"[{time.time()-T0:6.1f}s] {m}", flush=True)
# ---- exact prep (prime-independent) ----
c1,s1,c2,s2=sp.symbols('c1 s1 c2 s2'); C1,S1,C2,S2=sp.symbols('C1 S1 C2 S2'); A1,B1,A2,B2=sp.symbols('A1 B1 A2 B2')
pi1,pi2,h,g=sp.symbols('pi1 pi2 h g'); t1,t2,u1,u2=sp.symbols('t1 t2 u1 u2')
def build(qa,qb):
    qa=sp.Matrix(qa); qb=sp.Matrix(qb); qm=(qa+qb)/2; v=(qb-qa)/h
    om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
    w1,w2=om(0,qm,v),om(1,qm,v); cd=qm[0]*qm[2]+qm[1]*qm[3]
    return h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cd+g*(2*qm[0]+qm[2]))
Ld01=build((c1,s1,c2,s2),(C1,S1,C2,S2)); Ld12=build((C1,S1,C2,S2),(A1,B1,A2,B2))
D2_01=[sp.cancel(sp.diff(Ld01,x)) for x in (C1,S1,C2,S2)]
D1_12=[sp.cancel(sp.diff(Ld12,x)) for x in (C1,S1,C2,S2)]
E5_1=sp.cancel(h*((D2_01[0]+D1_12[0])*(-S1)+(D2_01[1]+D1_12[1])*C1))
E5_2=sp.cancel(h*((D2_01[2]+D1_12[2])*(-S2)+(D2_01[3]+D1_12[3])*C2))
D1_01=[sp.cancel(sp.diff(Ld01,x)) for x in (c1,s1,c2,s2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1_01[0]*(-s1)+D1_01[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1_01[2]*(-s2)+D1_01[3]*c2))))
num={c1:sp.Rational(3,5),s1:sp.Rational(4,5),c2:sp.Rational(5,13),s2:sp.Rational(12,13),pi1:sp.Rational(1,3),pi2:sp.Rational(-1,7),g:10,h:sp.Rational(1,40)}
Wt={C1:(1-t1**2)/(1+t1**2),S1:2*t1/(1+t1**2),C2:(1-t2**2)/(1+t2**2),S2:2*t2/(1+t2**2)}
Wu={A1:(1-u1**2)/(1+u1**2),B1:2*u1/(1+u1**2),A2:(1-u2**2)/(1+u2**2),B2:2*u2/(1+u2**2)}
Pa=sp.expand(sp.fraction(sp.together(hG1.subs(num).subs(Wt)))[0]); Pb=sp.expand(sp.fraction(sp.together(hG2.subs(num).subs(Wt)))[0])
GB=sp.groebner([Pa,Pb],t1,t2,order='lex')
uniq=[q.as_expr() for q in GB.polys if q.free_symbols<={t2}][0]
oth=[q.as_expr() for q in GB.polys if sp.degree(q.as_expr(),t1)==1][0]
def intpoly(e,var):
    P=sp.Poly(sp.together(e),var); den=sp.lcm([sp.fraction(cf)[1] for cf in P.all_coeffs()])
    return [int(x) for x in sp.Poly(sp.expand(e*den),var).all_coeffs()]
U=intpoly(uniq,t2); a_=intpoly(sp.Poly(oth,t1).coeff_monomial(t1),t2); b_=intpoly(oth-sp.Poly(oth,t1).coeff_monomial(t1)*t1,t2)
F1=sp.expand(sp.fraction(sp.together(E5_1.subs(num).subs(Wt).subs(Wu)))[0])
F2=sp.expand(sp.fraction(sp.together(E5_2.subs(num).subs(Wt).subs(Wu)))[0])
def coeftab(F):
    Fi=sp.Poly(F,u1,u2,t1,t2)
    den=sp.lcm([sp.fraction(cf)[1] for cf in Fi.coeffs()])
    Fi=sp.Poly(sp.expand(F*den),u1,u2,t1,t2)
    tab=[[[] for _ in range(5)] for _ in range(5)]
    for mono,cf in Fi.terms():
        i,j,e1,e2=mono; tab[i][j].append((int(cf),e1,e2))
    return tab
T1,T2c=coeftab(F1),coeftab(F2)
tick("exact prep done")
def run_prime(p):
    def horner(cs,x):
        r=0
        for cc in cs: r=(r*(x%p)+cc)%p
        return r
    Uf=flint.nmod_poly(U[::-1],p)
    if Uf.gcd(Uf.derivative()).degree()!=0: return f"p={p}: U not squarefree — skip"
    af=flint.nmod_poly(a_[::-1],p)
    if Uf.gcd(af).degree()!=0: return f"p={p}: gcd(a,U)!=1 — skip"
    quad=flint.nmod_poly([1,0,1],p); U30,rem=divmod(Uf,quad)
    remok=(rem.degree()<0) or all(int(rem[i])==0 for i in range(rem.degree()+1))
    N=2058
    nodes=[]; k=1
    while len(nodes)<N:
        if horner(a_,k)!=0: nodes.append(k)
        k+=1
    nodes=np.array(nodes,dtype=np.int64)
    t1s=np.array([(-horner(b_,int(x))*pow(horner(a_,int(x)),p-2,p))%p for x in nodes],dtype=np.int64)
    a4=np.array([pow(horner(a_,int(x)),4,p) for x in nodes],dtype=np.int64)
    def pow_arr(v,e):
        r=np.ones_like(v)
        for _ in range(e): r=(r*v)%p
        return r
    def matgrid(tab):
        M=np.zeros((N,5,5),dtype=np.int64)
        for i in range(5):
            for j in range(5):
                if not tab[i][j]: continue
                acc=np.zeros(N,dtype=np.int64)
                for (cf,e1,e2) in tab[i][j]:
                    term=(((cf%p)*pow_arr(t1s,e1))%p*pow_arr(nodes%p,e2))%p
                    acc=(acc+term)%p
                M[:,i,j]=(acc*a4)%p
        return M
    M1g,M2g=matgrid(T1),matgrid(T2c)
    u2samp=np.arange(1,34,dtype=np.int64)
    pw=np.ones((5,33),dtype=np.int64)
    for i in range(1,5): pw[i]=(pw[i-1]*u2samp)%p
    def bdet(mats):
        A=mats.copy(); B=A.shape[0]; det=np.ones(B,dtype=np.int64)
        for kk in range(8):
            piv=A[:,kk,kk].copy()
            bad=np.where(piv==0)[0]
            for ib in bad:
                for r in range(kk+1,8):
                    if A[ib,r,kk]!=0:
                        A[ib,[kk,r]]=A[ib,[r,kk]]; det[ib]=(p-det[ib])%p; break
            piv=A[:,kk,kk]; det=(det*piv)%p
            inv=np.array([pow(int(x),p-2,p) if x else 0 for x in piv],dtype=np.int64)
            for r in range(kk+1,8):
                f=(A[:,r,kk]*inv)%p
                A[:,r,kk:]=(A[:,r,kk:]-f[:,None]*A[:,kk,kk:])%p
        return det%p
    Vals=np.zeros((N,33),dtype=np.int64)
    for jj in range(33):
        cA=(M1g@pw[:,jj])%p; cB=(M2g@pw[:,jj])%p
        if np.any(cA[:,4]==0) or np.any(cB[:,4]==0): return f"p={p}: lc vanish — skip"
        S=np.zeros((N,8,8),dtype=np.int64)
        for r in range(4): S[:,r,r:r+5]=cA[:,::-1]
        for r in range(4): S[:,4+r,r:r+5]=cB[:,::-1]
        Vals[:,jj]=bdet(S)
    V=np.array([[pow(int(u2samp[i]),j,p) for j in range(33)] for i in range(33)],dtype=object)
    Aug=[[int(V[i][j]) for j in range(33)]+[1 if i==j else 0 for j in range(33)] for i in range(33)]
    for kk in range(33):
        iv=pow(Aug[kk][kk],p-2,p); Aug[kk]=[(x*iv)%p for x in Aug[kk]]
        for r in range(33):
            if r!=kk and Aug[r][kk]:
                f=Aug[r][kk]; Aug[r]=[(x-f*y)%p for x,y in zip(Aug[r],Aug[kk])]
    Vinv=np.array([[Aug[i][33+j] for j in range(33)] for i in range(33)],dtype=np.int64)
    Rcoef=(Vals@Vinv.T)%p
    # TEST B at this prime
    Ev=np.zeros(N,dtype=np.int64); Od=np.zeros(N,dtype=np.int64)
    for j in range(33):
        s=1 if (j//2)%2==0 else p-1
        if j%2==0: Ev=(Ev+s*Rcoef[:,j])%p
        else: Od=(Od+s*Rcoef[:,j])%p
    x=nodes%p
    def interp1(vals,M):
        c=vals[:M].copy().astype(np.int64)
        for kk in range(1,M):
            diff=(x[kk:M]-x[:M-kk])%p
            inv=np.array([pow(int(d),p-2,p) for d in diff],dtype=np.int64)
            c[kk:M]=((c[kk:M]-c[kk-1:M-1])*inv)%p
        co=np.zeros(M,dtype=np.int64); co[0]=c[M-1]%p; cur=0
        for kk in range(M-2,-1,-1):
            old=co[:cur+1].copy(); co[1:cur+2]=old; co[0]=0
            co[:cur+1]=(co[:cur+1]-x[kk]*old)%p; co[0]=(co[0]+c[kk])%p; cur+=1
        return co
    Epo=flint.nmod_poly([int(v) for v in interp1(Ev,1025)],p)%U30
    Opo=flint.nmod_poly([int(v) for v in interp1(Od,1025)],p)%U30
    tb=(Epo.degree()<0 or all(int(Epo[i])==0 for i in range(Epo.degree()+1))) and (Opo.degree()<0 or all(int(Opo[i])==0 for i in range(Opo.degree()+1)))
    # E30
    NZ=1000; zs=np.arange(1,NZ+1,dtype=np.int64)
    zpow=np.ones((33,NZ),dtype=np.int64)
    for i in range(1,33): zpow[i]=(zpow[i-1]*zs)%p
    Rgrid=(Rcoef@zpow)%p
    M=1025; c=Rgrid[:M].copy().astype(np.int64)
    for kk in range(1,M):
        diff=(x[kk:M]-x[:M-kk])%p
        inv=np.array([pow(int(d),p-2,p) for d in diff],dtype=np.int64)
        c[kk:M]=((c[kk:M]-c[kk-1:M-1])*inv[:,None])%p
    CO=np.zeros((M,NZ),dtype=np.int64); CO[0]=c[M-1]%p; cur=0
    for kk in range(M-2,-1,-1):
        old=CO[:cur+1].copy(); CO[1:cur+2]=old; CO[0]=0
        CO[:cur+1]=(CO[:cur+1]-x[kk]*old)%p; CO[0]=(CO[0]+c[kk])%p; cur+=1
    Evals=np.zeros(NZ,dtype=np.int64)
    for j in range(NZ):
        Evals[j]=int(U30.resultant(flint.nmod_poly([int(v) for v in CO[:,j]],p)))
    M2=961; xs=zs[:M2]; c2=Evals[:M2].copy().astype(np.int64)
    for kk in range(1,M2):
        diff=(xs[kk:M2]-xs[:M2-kk])%p
        inv=np.array([pow(int(d),p-2,p) for d in diff],dtype=np.int64)
        c2[kk:M2]=((c2[kk:M2]-c2[kk-1:M2-1])*inv)%p
    E=np.zeros(M2,dtype=np.int64); E[0]=c2[M2-1]%p; cur=0
    for kk in range(M2-2,-1,-1):
        old=E[:cur+1].copy(); E[1:cur+2]=old; E[0]=0
        E[:cur+1]=(E[:cur+1]-xs[kk]*old)%p; E[0]=(E[0]+c2[kk])%p; cur+=1
    ok=0
    for j in range(M2,NZ):
        v=0; xp=1
        for d in range(M2): v=(v+int(E[d])*xp)%p; xp=(xp*int(zs[j]))%p
        ok+=int(v==int(Evals[j]))
    deg=M2-1
    while deg>0 and E[deg]==0: deg-=1
    Ef=flint.nmod_poly([int(v) for v in E[:deg+1]],p)
    sq=Ef.gcd(Ef.derivative()); gq=Ef.gcd(flint.nmod_poly([1,0,1],p))
    return f"p={p}: T²+1|U {remok} | R(±i)≡0 mod U30: {tb} | E30 deg={deg} sqfree={deg-sq.degree()} gcd(z²+1)={gq.degree()} | holdout {ok}/{NZ-M2}"
for p in [int(sp.prevprime(519999979)), int(sp.prevprime(519999978-10**6))]:
    print(run_prime(p)); tick("prime done")
