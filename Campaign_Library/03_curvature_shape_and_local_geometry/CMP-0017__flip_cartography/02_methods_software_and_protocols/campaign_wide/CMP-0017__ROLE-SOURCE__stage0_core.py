import sympy as sp
c1,s1,c2,s2, C1,S1,C2,S2 = sp.symbols('c1 s1 c2 s2 C1 S1 C2 S2')
pi1,pi2, h,g = sp.symbols('pi1 pi2 h g')
q0 = sp.Matrix([c1,s1,c2,s2]); q1 = sp.Matrix([C1,S1,C2,S2])
qb = (q0+q1)/2; v = (q1-q0)/h
om = lambda i,q,vv: q[2*i]*vv[2*i+1] - q[2*i+1]*vv[2*i]
w1, w2 = om(0,qb,v), om(1,qb,v)
cD = qb[0]*qb[2] + qb[1]*qb[3]
T = w1**2 + sp.Rational(1,2)*w2**2 + w1*w2*cD
V = -g*(2*qb[0] + qb[2])
Ld = h*(T - V)

# CHECK 1: adjoint identity via polynomial N = h*Ld
N = sp.expand(sp.cancel(h*Ld))
swap = {c1:C1,s1:S1,c2:C2,s2:S2, C1:c1,S1:s1,C2:c2,S2:s2, h:-h}
M = sp.expand(N.subs(swap, simultaneous=True))
print("CHECK1 adjoint identity (M==N):", sp.expand(M-N)==0)

# step generators, h-cleared
D1 = [sp.cancel(sp.diff(Ld,x)) for x in (c1,s1,c2,s2)]
D2 = [sp.cancel(sp.diff(Ld,x)) for x in (C1,S1,C2,S2)]
G1 = pi1 + (D1[0]*(-s1) + D1[1]*c1)
G2 = pi2 + (D1[2]*(-s2) + D1[3]*c2)
P1 = D2[0]*(-S1) + D2[1]*C1
P2 = D2[2]*(-S2) + D2[3]*C2
hG1,hG2,hP1,hP2 = [sp.expand(sp.cancel(h*e)) for e in (G1,G2,P1,P2)]

# CHECK 2: h->0 consistency, truncated rotation polys (exact coefficient extraction)
a1,a2 = sp.symbols('a1 a2')
tr = {C1: c1*(1-(h*a1)**2/2) - s1*(h*a1), S1: s1*(1-(h*a1)**2/2) + c1*(h*a1),
      C2: c2*(1-(h*a2)**2/2) - s2*(h*a2), S2: s2*(1-(h*a2)**2/2) + c2*(h*a2)}
pt = {c1:sp.Rational(3,5), s1:sp.Rational(4,5), c2:sp.Rational(5,13), s2:sp.Rational(12,13), g:10}
cD0 = (c1*c2+s1*s2).subs(pt)
picont = {pi1: 2*a1 + a2*cD0, pi2: a2 + a1*cD0}
res = []
for e, tgt in ((hG1,None),(hG2,None),(hP1,picont[pi1]),(hP2,picont[pi2])):
    f = sp.expand(e.subs(tr).subs(pt).subs(picont))
    # h*G ~ h*(G0 + O(h)); consistency <=> coefficient of h^1 is G0 = 0 (in-eqs) or = pi_cont (out-momenta, already subtracted)
    if tgt is not None: f = sp.expand(f - h*tgt)
    c_h1 = sp.expand(f.coeff(h,1))
    res.append(sp.simplify(c_h1)==0)
print("CHECK2 h->0 consistency at exact rational point:", all(res), res)

# CHECK 4: mass matrix
cd = sp.Symbol('cd'); print("CHECK4 det M = 2 - cd^2  (>=1 on |cd|<=1):", sp.det(sp.Matrix([[2,cd],[cd,1]]))==2-cd**2)

# degrees
def degs(e):
    P = sp.Poly(e, c1,s1,c2,s2,C1,S1,C2,S2,pi1,pi2,h,g); d=P.degree_list()
    return dict(q0=max(d[0:4]), q1=max(d[4:8]), pi=max(d[8:10]), h=d[10], g=d[11], tot=P.total_degree())
for nm,e in (("hG1",hG1),("hG2",hG2),("hP1",hP1),("hP2",hP2)): print("DEG",nm,degs(e))
sp.pickle = None
import pickle
pickle.dump({'gens':[sp.srepr(x) for x in (hG1,hG2)],}, open('/tmp/stage0.pkl','wb'))
print("core done")
