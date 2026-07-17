import sympy as sp, numpy as np, warnings
warnings.filterwarnings("ignore")
c1,s1,c2,s2, C1,S1,C2,S2 = sp.symbols('c1 s1 c2 s2 C1 S1 C2 S2')
pi1,pi2,h,g = sp.symbols('pi1 pi2 h g')
q0=sp.Matrix([c1,s1,c2,s2]); q1=sp.Matrix([C1,S1,C2,S2]); qb=(q0+q1)/2; v=(q1-q0)/h
om=lambda i,q,vv: q[2*i]*vv[2*i+1]-q[2*i+1]*vv[2*i]
w1,w2=om(0,qb,v),om(1,qb,v); cD=qb[0]*qb[2]+qb[1]*qb[3]
Ld=h*(w1**2+sp.Rational(1,2)*w2**2+w1*w2*cD+g*(2*qb[0]+qb[2]))
D1=[sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
D2=[sp.cancel(sp.diff(Ld,x)) for x in (C1,S1,C2,S2)]
hG1=sp.expand(sp.cancel(h*(pi1+(D1[0]*(-s1)+D1[1]*c1))))
hG2=sp.expand(sp.cancel(h*(pi2+(D1[2]*(-s2)+D1[3]*c2))))
P1o,P2o=D2[0]*(-S1)+D2[1]*C1, D2[2]*(-S2)+D2[3]*C2
args=(c1,s1,c2,s2,pi1,pi2,C1,S1,C2,S2,h,g)
F=sp.lambdify(args,[hG1,hG2,C1**2+S1**2-1,C2**2+S2**2-1],'numpy')
J=sp.lambdify(args,[[sp.diff(e,x) for x in (C1,S1,C2,S2)] for e in [hG1,hG2,C1**2+S1**2-1,C2**2+S2**2-1]],'numpy')
Po=sp.lambdify(args,[P1o*h,P2o*h],'numpy'); gv=10.0
class StepFail(Exception): pass
def Minv(cd): d=2-cd*cd; return np.array([[1,-cd],[-cd,2]])/d
def newton(qp, x, hh):
    q,pi=qp[:4],qp[4:]
    for _ in range(40):
        r=np.array(F(*q,*pi,*x,hh,gv),float)
        if not np.all(np.isfinite(r)): return None
        if np.max(np.abs(r))<1e-12:
            pn=np.array(Po(*q,*pi,*x,hh,gv),float)/hh
            return np.concatenate([x,pn])
        try: x=x-np.linalg.solve(np.array(J(*q,*pi,*x,hh,gv),float),r)
        except np.linalg.LinAlgError: return None
    return None
def guess_rot(qp,hh):
    q,pi=qp[:4],qp[4:]; omg=Minv(q[0]*q[2]+q[1]*q[3])@pi; a1,a2=omg*hh
    return np.array([q[0]*np.cos(a1)-q[1]*np.sin(a1), q[1]*np.cos(a1)+q[0]*np.sin(a1),
                     q[2]*np.cos(a2)-q[3]*np.sin(a2), q[3]*np.cos(a2)+q[2]*np.sin(a2)])
def step(qp,hh,depth=0):
    out=newton(qp,guess_rot(qp,hh),hh)
    if out is not None: return out
    if depth>=5: raise StepFail()
    mid=step(qp,hh/2,depth+1); pred=step(mid,hh/2,depth+1)   # predictor only
    out=newton(qp,pred[:4],hh)
    if out is None: raise StepFail()
    return out
def energy(st):
    q,pi=st[:4],st[4:]; return 0.5*pi@(Minv(q[0]*q[2]+q[1]*q[3])@pi)-gv*(2*q[0]+q[2])
th1,th2=2.2,2.9
ic=np.array([np.cos(th1),np.sin(th1),np.cos(th2),np.sin(th2),0,0]); E0=energy(ic)
print(f"IC: theta=({th1},{th2}) rest | 2c1+c2={2*ic[0]+ic[2]:.3f} | E0={E0:.4f}")
print(f"{'h':>8} {'N':>5} {'halt':>6} {'maxRelE':>9} {'endRelE':>9} {'maxPhi':>8} {'revErr':>8} {'flipStep':>8} {'flipT':>7}")
results={}
for hh in [1/10,1/20,1/40,1/80]:
    N=int(round(10/hh)); st=ic.copy(); mx=fe=0; mc=0; flip=None; halt='—'
    prev=st.copy()
    try:
        for k in range(1,N+1):
            st=step(st,hh)
            mc=max(mc,np.max(np.abs(np.array(F(*st[:4]*0+st[:4],*st[4:],*st[:4],hh,gv),float)[2:])))
            e=abs(energy(st)-E0)/abs(E0); mx=max(mx,e)
            if flip is None and prev[3]*st[3]<0 and prev[2]<0 and st[2]<0: flip=k
            prev=st.copy()
        fe=abs(energy(st)-E0)/abs(E0)
        rb=st.copy(); rb[4:]=-rb[4:]
        for k in range(N): rb=step(rb,hh)
        rb[4:]=-rb[4:]; rev=np.max(np.abs(rb-ic))
    except StepFail:
        halt=str(k); rev=float('nan'); fe=float('nan')
    results[hh]=(flip,hh*flip if flip else None, halt)
    print(f"{hh:8.4f} {N:5d} {halt:>6} {mx:9.1e} {fe:9.1e} {mc:8.1e} {rev:8.1e} {str(flip):>8} {('%.3f'%(hh*flip)) if flip else '—':>7}")
# flip-time h-convergence
for pair in [(1/40,1/80),(1/20,1/40)]:
    a,b=pair
    ta,tb=results[a][1],results[b][1]
    if ta and tb: print(f"flip-time agreement h={a:.4f} vs {b:.4f}: {abs(ta-tb)/tb*100:.2f}%")
