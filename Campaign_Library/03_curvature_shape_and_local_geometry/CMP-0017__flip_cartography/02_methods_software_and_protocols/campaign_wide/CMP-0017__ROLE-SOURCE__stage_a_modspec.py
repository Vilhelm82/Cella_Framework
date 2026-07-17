import sympy as sp, numpy as np, flint, time, pickle
T0=time.time()
def tick(msg): print(f"[{time.time()-T0:6.1f}s] {msg}", flush=True)
import sympy as _s
p=int(_s.prevprime(520000000))
print('prime:',p)
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
uni=[q.as_expr() for q in GB.polys if q.free_symbols<={t2}][0]
oth=[q.as_expr() for q in GB.polys if sp.degree(q.as_expr(),t1)==1][0]
def intpoly(e,var):
    P=sp.Poly(sp.together(e),var); den=sp.lcm([sp.fraction(cf)[1] for cf in P.all_coeffs()])
    return [int(x) for x in sp.Poly(sp.expand(e*den),var).all_coeffs()]
U=intpoly(uni,t2); a_=intpoly(sp.Poly(oth,t1).coeff_monomial(t1),t2); b_=intpoly(oth-sp.Poly(oth,t1).coeff_monomial(t1)*t1,t2)
assert len(U)-1==32 and len(a_)-1<=31 and len(b_)-1<=31
F1=sp.expand(sp.fraction(sp.together(E5_1.subs(num).subs(Wt).subs(Wu)))[0])
F2=sp.expand(sp.fraction(sp.together(E5_2.subs(num).subs(Wt).subs(Wu)))[0])
den=sp.lcm([sp.fraction(cf)[1] for cf in sp.Poly(F1,t1,t2,u1,u2).coeffs()]+[sp.fraction(cf)[1] for cf in sp.Poly(F2,t1,t2,u1,u2).coeffs()])
F1i=sp.Poly(sp.expand(F1*den),u1,u2,t1,t2); F2i=sp.Poly(sp.expand(F2*den),u1,u2,t1,t2)
assert max(sp.degree(F1,v) for v in (t1,t2,u1,u2))<=4
# coefficient tables: CM[i][j] = list of (coef,e1,e2) for t1^e1 t2^e2, i=u1-deg,j=u2-deg
def coeftab(Fi):
    tab=[[[] for _ in range(5)] for _ in range(5)]
    for mono,cf in Fi.terms():
        i,j,e1,e2=mono; tab[i][j].append((int(cf)%p,e1,e2))
    return tab
T1,T2c=coeftab(F1i),coeftab(F2i)
tick("exact data prepared")
def hornermod(cs,x):
    r=0
    for cc in cs: r=(r*x+cc)%p
    return r
Uf=flint.nmod_poly(U[::-1],p)
Upr=Uf.derivative()
assert Uf.gcd(Upr).degree()==0, "U not squarefree mod p"
af=flint.nmod_poly(a_[::-1],p)
assert Uf.gcd(af).degree()==0, "gcd(a,U)!=1 mod p"
N=2058; HOLD=9
nodes=[]; k=1
while len(nodes)<N:
    if hornermod(a_,k)!=0: nodes.append(k)
    k+=1
nodes=np.array(nodes,dtype=np.int64)
t1s=np.array([(-hornermod(b_,int(x))*pow(hornermod(a_,int(x)),p-2,p))%p for x in nodes],dtype=np.int64)
a4=np.array([pow(hornermod(a_,int(x)),4,p) for x in nodes],dtype=np.int64)
tick(f"nodes ready ({N})")
# per node: cleared 5x5 coefficient matrices
def matgrid(tab):
    M=np.zeros((N,5,5),dtype=np.int64)
    for i in range(5):
        for j in range(5):
            if not tab[i][j]: continue
            acc=np.zeros(N,dtype=np.int64)
            for (cf,e1,e2) in tab[i][j]:
                term=((cf*pow_arr(t1s,e1))%p*pow_arr(nodes%p,e2))%p
                acc=(acc+term)%p
            M[:,i,j]=(acc*a4)%p
    return M
def pow_arr(v,e):
    r=np.ones_like(v)
    for _ in range(e): r=(r*v)%p
    return r
M1g,M2g=matgrid(T1),matgrid(T2c)
tick("coefficient grids ready")
u2samp=np.arange(1,34,dtype=np.int64)
pw=np.ones((5,33),dtype=np.int64)
for i in range(1,5): pw[i]=(pw[i-1]*u2samp)%p
def batched_det(mats):
    A=mats.copy(); B=A.shape[0]; det=np.ones(B,dtype=np.int64)
    for k in range(8):
        piv=A[:,k,k].copy()
        bad=np.where(piv==0)[0]
        for ib in bad:
            for r in range(k+1,8):
                if A[ib,r,k]!=0:
                    A[ib,[k,r]]=A[ib,[r,k]]; det[ib]=(p-det[ib])%p; break
        piv=A[:,k,k]
        det=(det*piv)%p
        inv=np.array([pow(int(x),p-2,p) if x else 0 for x in piv],dtype=np.int64)
        for r in range(k+1,8):
            f=(A[:,r,k]*inv)%p
            A[:,r,k:]=(A[:,r,k:]-f[:,None]*A[:,k,k:])%p
    return det%p
Vals=np.zeros((N,33),dtype=np.int64)
for jj in range(33):
    cu1_1=(M1g@pw[:,jj])%p  # (N,5) u1-coeffs ascending? M[:,i,j]: i=u1 deg
    cu1_2=(M2g@pw[:,jj])%p
    if np.any(cu1_1[:,4]==0) or np.any(cu1_2[:,4]==0):
        raise RuntimeError(f"leading u1-coeff vanished at u2-sample {jj}")
    S=np.zeros((N,8,8),dtype=np.int64)
    for r in range(4): S[:,r,r:r+5]=cu1_1[:,::-1]
    for r in range(4): S[:,4+r,r:r+5]=cu1_2[:,::-1]
    Vals[:,jj]=batched_det(S)
tick("34k sylvester dets done")
# u2-interp per node: 33x33 inverse Vandermonde once
V=np.zeros((33,33),dtype=np.int64)
for i in range(33):
    for j in range(33): V[i,j]=pow(int(u2samp[i]),j,p)
Vl=[[int(x) for x in row] for row in V]
# invert mod p (gaussian, python)
nI=33; Aug=[row[:]+[1 if i==j else 0 for j in range(nI)] for i,row in enumerate(Vl)]
for k in range(nI):
    pv=Aug[k][k]; iv=pow(pv,p-2,p)
    Aug[k]=[(x*iv)%p for x in Aug[k]]
    for r in range(nI):
        if r!=k and Aug[r][k]:
            f=Aug[r][k]; Aug[r]=[(x-f*y)%p for x,y in zip(Aug[r],Aug[k])]
Vinv=np.array([[Aug[i][nI+j] for j in range(nI)] for i in range(nI)],dtype=np.int64)
Rcoef=(Vals@Vinv.T)%p   # (N,33): R-coeffs in u2, ascending, per node
np.save('/home/claude/Rcoef.npy',Rcoef); np.save('/home/claude/nodes.npy',nodes)
pickle.dump(dict(U=U,a=a_,b=b_,p=p,N=N,HOLD=HOLD),open('/home/claude/modspec_state.pkl','wb'))
tick("R(u2) coefficients per node saved")
# ---------- target u2: E(z)=Res_t2(R(.,z),U) at 1040 z-samples ----------
NZ=1040; zs=np.arange(1,NZ+1,dtype=np.int64)
zpow=np.ones((33,NZ),dtype=np.int64)
for i in range(1,33): zpow[i]=(zpow[i-1]*zs)%p
Rgrid=(Rcoef@zpow)%p   # (N,NZ) values R(node,z)
def newton_interp_batch(xs, Ygrid, deg):
    # xs: nodes (len M>=deg+1, equally... arbitrary); returns monomial coeffs (deg+1, B)
    M=deg+1; x=xs[:M].astype(np.int64); Y=Ygrid[:M].copy()
    invd={}
    c=Y.copy()
    for k in range(1,M):
        diff=(x[k:]-x[:M-k])%p
        inv=np.array([pow(int(d),p-2,p) for d in diff],dtype=np.int64)
        c[k:]=((c[k:]-c[k-1:M-1])*inv[:,None])%p
    # newton -> monomial
    B=Ygrid.shape[1]
    co=np.zeros((M,B),dtype=np.int64); co[0]=c[M-1]
    degc=0
    for k in range(M-2,-1,-1):
        co[1:degc+2]=co[0:degc+1]
        co[0]=0
        co[:degc+2]=(co[:degc+2]-0)%p
        co[:degc+1+1]=co[:degc+2]
        co[0:degc+2]=(co[0:degc+2]- (x[k]*np.vstack([co[1:degc+2],np.zeros((1,B),dtype=np.int64)]) if False else 0))%p
        # simpler: co = co*(t - x_k) + c_k  implemented explicitly:
        pass
    return None
# (vectorized horner-build implemented explicitly below instead)
def newton_to_monomial(xs, Y, deg):
    M=deg+1; x=xs[:M]; c=Y[:M].copy()
    for k in range(1,M):
        diff=(x[k:]-x[:M-k])%p
        inv=np.array([pow(int(d),p-2,p) for d in diff],dtype=np.int64)
        c[k:]=((c[k:]-c[k-1:M-1])*inv[:,None])%p
    B=Y.shape[1]
    co=np.zeros((M,B),dtype=np.int64)
    co[0]=c[M-1]%p; cur=0
    for k in range(M-2,-1,-1):
        # co <- co*(t-x_k)+c[k]:  shift up, subtract x_k*old, add c_k to constant
        co[1:cur+2]=(co[1:cur+2]+co[0:cur+1])%p if False else co[1:cur+2]
        old=co[:cur+1].copy()
        co[1:cur+2]=old
        co[0]=0
        co[:cur+1]=(co[:cur+1]-x[k]*old)%p
        co[0]=(co[0]+c[k])%p
        cur+=1
    return co%p
rng=np.random.default_rng(3)
_tc=rng.integers(0,p,size=(1025,2),dtype=np.int64)
_x=nodes%p
_Y=np.zeros((len(_x),2),dtype=np.int64)
_xp=np.ones((len(_x),2),dtype=np.int64)
for _d in range(1025):
    _Y=(_Y+_tc[_d]*_xp)%p; _xp=(_xp*_x[:,None])%p
_co=newton_to_monomial(_x,_Y,1024)
assert np.all(_co==_tc), "SELF-TEST FAIL: interpolator broken"
print("interpolator self-test: PASS (deg-1024 synthetic recovered exactly)")
tick("interpolating R over t2 (deg<=1024) for u2-target...")
CO=newton_to_monomial(nodes%p, Rgrid, 1024)   # (1025, NZ)
# holdout gate
hold=nodes[1025:1025+HOLD]%p
ok=0
for hi,xh in enumerate(hold):
    xp=np.ones(NZ,dtype=np.int64); val=np.zeros(NZ,dtype=np.int64)
    for d in range(1025):
        val=(val+CO[d]*xp)%p; xp=(xp*xh)%p
    ok+=int(np.all(val==Rgrid[1025+hi]))
print(f"holdout interpolation gate: {ok}/{HOLD} nodes exact")
tick("computing 1040 resultants with U...")
Evals=np.zeros(NZ,dtype=np.int64)
for j in range(NZ):
    Rp=flint.nmod_poly([int(x) for x in CO[:,j]],p)
    Evals[j]=int(Uf.resultant(Rp))
E=newton_to_monomial(zs%p, Evals[:,None].astype(np.int64), 1024)[:,0]
# gate on extra z-samples
xg=0
for j in range(1025,NZ):
    v=0; xp=1
    for d in range(1025):
        v=(v+int(E[d])*xp)%p; xp=(xp*int(zs[j]))%p
    xg+=int(v==int(Evals[j]))
deg=1024
while deg>0 and E[deg]==0: deg-=1
Ef=flint.nmod_poly([int(x) for x in E[:deg+1]],p)
sq=Ef.gcd(Ef.derivative())
print(f"E_u2: deg={deg} | sqfree deg={deg-sq.degree()} | z-holdout gate {xg}/{NZ-1025}")
tick("u2 done")
