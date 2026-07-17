# t4_derive.py -- CAS derivation of the T^4 fold coefficient (T4_PREDECL pin a4e70c97)
import sympy as sp, mpmath as mp, re, hashlib
t1,t2,v1,v2,g=sp.symbols('t1 t2 v1 v2 g',real=True)
a,phi0,T=sp.symbols('a phi0 T',real=True)
# exact EOM: (2-cD^2) t1dd = ... derive from Lagrangian to avoid my hand algebra entirely
th1,th2=sp.Function('th1')(sp.Symbol('t')),sp.Function('th2')(sp.Symbol('t'))
tt=sp.Symbol('t')
L=sp.diff(th1,tt)**2+sp.Rational(1,2)*sp.diff(th2,tt)**2+sp.diff(th1,tt)*sp.diff(th2,tt)*sp.cos(th1-th2)+g*(2*sp.cos(th1)+sp.cos(th2))
E1=sp.diff(sp.diff(L,sp.diff(th1,tt)),tt)-sp.diff(L,th1)
E2=sp.diff(sp.diff(L,sp.diff(th2,tt)),tt)-sp.diff(L,th2)
d1,d2=sp.symbols('d1 d2')  # accelerations
sub={sp.diff(th1,tt,2):d1,sp.diff(th2,tt,2):d2,sp.diff(th1,tt):v1,sp.diff(th2,tt):v2,th1:t1,th2:t2}
S=sp.solve([E1.subs(sub),E2.subs(sub)],[d1,d2],dict=True)[0]
F1=sp.simplify(S[d1]); F2=sp.simplify(S[d2])
# from-rest Taylor: th(t) = th0 + t^2/2 F + t^4/24 (F_th . F + Hess_v F [F,F]) evaluated at (th0, v=0)
X=(t1,t2); V=(v1,v2); F=(F1,F2)
def at0(e): return e.subs({v1:0,v2:0})
F0=[sp.simplify(at0(f)) for f in F]
G4=[]
for f in F:
    term=sum(at0(sp.diff(f,X[j]))*F0[j] for j in range(2))
    term+=sum(at0(sp.diff(f,V[i],V[j]))*F0[i]*F0[j] for i in range(2) for j in range(2))/1  # Hess contraction: d2F/dvidvj Fi Fj
    G4.append(sp.simplify(term))
# careful: d^2/dt^2 F(th(t),v(t)) at rest = F_th.thdd + F_vv[thdd,thdd] ; thdd=F0 ; cross F_thv terms vanish (v=0 slot linear) -- F_thv * (v * thdd) has v=0 factor
# wait: d/dt F = F_th.v + F_v.vd ; d2/dt2 F = F_thth[v,v]+F_th.vd+F_thv[...]v + F_vv[vd,vd]+F_v.vdd + F_vth[v,..] ; at v=0: = F_th.F0 + F_vv[F0,F0] + F_v.vdd ; vdd = d/dt F = 0 at rest? vdd(0)=dF/dt|0 = F_th.v+F_v.vd |0 = F_v.F0 -- NOT zero unless F_v|0=0. F is quadratic in v => F_v|v=0 = 0. OK so F_v.vdd term = 0. Good.
phi=t2-sp.pi
th10,th20=a,sp.pi+phi0
E={t1:th10,t2:th20}
phi_T = phi0 + T**2/2*F0[1].subs(E) + T**4/24*G4[1].subs(E)
# solve phi(T)=0 with phi0 = p2 T^2 + p4 T^4
p2,p4=sp.symbols('p2 p4')
expr=phi_T.subs(phi0,p2*T**2+p4*T**4)
ser=sp.series(expr,T,0,6).removeO()
c2=sp.simplify(ser.coeff(T,2)); c4=sp.simplify(ser.coeff(T,4))
s2=sp.solve(c2,p2)[0]
s4=sp.solve(c4.subs(p2,s2),p4)[0]
u0 = -sp.tan((p2*T**2+p4*T**4)/2)
u_ser=sp.series(u0.subs({p2:s2,p4:sp.simplify(s4)}),T,0,6).removeO()
U2=sp.simplify(u_ser.coeff(T,2)); U4=sp.simplify(u_ser.coeff(T,4))
# extremize over a: a* = a0 + d2 T^2 ; leading condition U2'(a0)=0 ; envelope: u*(T)=U2(a0)T^2+U4(a0)T^4
gval={g:10}
a0=-sp.acos(sp.Rational(1,3))/2
U2n=sp.simplify(U2.subs(gval)); U4n=sp.simplify(U4.subs(gval))
chk=sp.simplify(sp.diff(U2n,a).subs(a,a0))
Gc=sp.nsimplify(U4n.subs(a,a0),rational=False)
Gnum=sp.N(U4n.subs(a,a0),30)
d2s=sp.simplify(-sp.diff(U4n,a)/sp.diff(U2n,a,2))
d2num=sp.N(d2s.subs(a,a0),30)
OUT=[]
def emit(s): print(s,flush=True); OUT.append(s)
emit(f"U2(a) = {sp.simplify(U2)}")
emit(f"U2'(a0) check (must be 0): {chk}")
emit(f"G := U4(a0) = {Gnum}")
emit(f"b_pred = G/640 = {sp.N(Gnum/640,12)}")
emit(f"d2 (angle T^2 drift) = {d2num}")
emit(f"b_theta_pred = d2/1600 = {sp.N(d2num/1600,12)}")
# refit banked theta drift for T2 target
mp.mp.dps=50
Lg=open('runF_a.log').read()
th={}; 
for m in re.finditer(r"k=(\d) th\*=([-\d.]+) u\*=([\d.]+)",Lg): th[int(m.group(1))]=mp.mpf(m.group(2))
ks=[1,2,3,4,5]
A=[[mp.mpf(1),mp.mpf(k)**2,mp.mpf(k)**4] for k in ks]; y=[th[k] for k in ks]
M=[[sum(A[r][i]*A[r][j] for r in range(5)) for j in range(3)] for i in range(3)]
bb=[sum(A[r][i]*y[r] for r in range(5)) for i in range(3)]
for i in range(3):
    p=max(range(i,3),key=lambda r:abs(M[r][i])); M[i],M[p]=M[p],M[i]; bb[i],bb[p]=bb[p],bb[i]
    for r in range(i+1,3):
        f=M[r][i]/M[i][i]; bb[r]-=f*bb[i]
        for c in range(i,3): M[r][c]-=f*M[i][c]
x=[mp.mpf(0)]*3
for i in (2,1,0): x[i]=(bb[i]-sum(M[i][j]*x[j] for j in range(i+1,3)))/M[i][i]
bth=x[1]
emit(f"T2 target b_theta (banked refit) = {mp.nstr(bth,10)}")
bT=mp.mpf('-0.0026780449')
bp=mp.mpf(str(sp.N(Gnum/640,20)))
btp=mp.mpf(str(sp.N(d2num/1600,20)))
emit(f"P-T4a: |{mp.nstr(bp,8)} - {mp.nstr(bT,8)}| = {mp.nstr(abs(bp-bT),4)} band {mp.nstr(mp.mpf('0.15')*abs(bT),4)} -> {'PASS' if abs(bp-bT)<=mp.mpf('0.15')*abs(bT) else 'FAIL'}")
emit(f"P-T4b: |{mp.nstr(btp,8)} - {mp.nstr(bth,8)}| = {mp.nstr(abs(btp-bth),4)} band {mp.nstr(mp.mpf('0.20')*abs(bth),4)} -> {'PASS' if abs(btp-bth)<=mp.mpf('0.20')*abs(bth) else 'FAIL'}")
print("RESULTS-SHA256:",hashlib.sha256("\n".join(OUT).encode()).hexdigest())
