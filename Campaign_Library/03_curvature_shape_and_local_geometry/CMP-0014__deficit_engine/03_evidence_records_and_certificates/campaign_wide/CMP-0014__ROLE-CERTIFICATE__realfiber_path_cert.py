#!/usr/bin/env python3
"""REALFIBER path certificate — mechanism extraction from Probe-2 stall geometry.
Lemma-1: W = 2uu^T - 2vv^T with u,v orthonormal has spectrum {2,-2,0,0,0}; diag(W)=0 iff u_i^2=v_i^2.
Path: explicit 3-stage continuous path star -> cycle inside the real fiber. Exact/symbolic throughout."""
import json, hashlib
import sympy as sp

R = sp.Rational
t = sp.symbols('t', nonnegative=True)
m = 5

# ---------- Lemma-1 (symbolic, fully general u,v) ----------
u = sp.Matrix(sp.symbols('u0:5', real=True))
v = sp.Matrix(sp.symbols('v0:5', real=True))
W = 2*u*u.T - 2*v*v.T
Cons = [sp.Eq((u.T*u)[0], 1), sp.Eq((v.T*v)[0], 1), sp.Eq((u.T*v)[0], 0)]
subs_rules = {}
# verify eigen-identities modulo the constraint ideal by direct expansion:
Wu = sp.expand(W*u - 2*u)   # = 2u(u.u) - 2v(v.u) - 2u -> 2u((u.u)-1) - 2v(v.u)
Wv = sp.expand(W*v + 2*v)
uu, vv, uv = (u.T*u)[0], (v.T*v)[0], (u.T*v)[0]
lem1a = all(sp.simplify(Wu[i] - (2*u[i]*(uu-1) - 2*v[i]*uv)) == 0 for i in range(m))
lem1b = all(sp.simplify(Wv[i] - (-2*v[i]*(vv-1) + 2*u[i]*uv)) == 0 for i in range(m))
# => on the constraint locus Wu=2u, Wv=-2v; rank(W)<=2 by construction; spectrum {2,-2,0^3}. [PROVEN]
# diag identity:
lem1c = all(sp.simplify(W[i, i] - 2*(u[i]**2 - v[i]**2)) == 0 for i in range(m))

# ---------- Explicit path (3 stages) ----------
# vertex sign data per stage: u_i = eps_i c_i, v_i = del_i c_i
def stage_check(c2list, eps, dl, name):
    """c2list: c_i(t)^2 as rational functions; verify sum=1, u.v=0, c_i^2>=0 on [0,1]."""
    s_sum = sp.simplify(sum(c2list) - 1)
    uv_sum = sp.simplify(sum(e*d*c2 for e, d, c2 in zip(eps, dl, c2list)))
    ok_sum = (s_sum == 0)
    ok_uv = (uv_sum == 0)
    ok_pos = all(sp.simplify(c2.subs(t, 0)) >= 0 and sp.simplify(c2.subs(t, 1)) >= 0
                 and sp.degree(sp.Poly(c2, t)) <= 1 for c2 in c2list)  # linear in t: endpoint check suffices
    return ok_sum and ok_uv and ok_pos, {"sum": str(s_sum), "uv": str(uv_sum)}

# Stage 1: star config, kill c4.  L={0}, R={1,2,3,4}; eps=(+,+,+,+,+), del=(+,-,-,-,-)
eps1 = [1, 1, 1, 1, 1]; dl1 = [1, -1, -1, -1, -1]
c2_s1 = [R(1,2), (3+t)/24, (3+t)/24, (3+t)/24, (1-t)/8]
ok1, d1 = stage_check(c2_s1, eps1, dl1, "S1")
# Stage 2: kill c2 (vertex 2), vertex 4 stays 0.
eps2 = [1, 1, 1, 1, 1]; dl2 = [1, -1, -1, -1, -1]
c2_s2 = [R(1,2), (2+t)/12, (1-t)/6, (2+t)/12, sp.Integer(0)]
ok2, d2 = stage_check(c2_s2, eps2, dl2, "S2")
# Stage 3: revive vertex 2 in class L (del2 flips to +), shrink c0.
eps3 = [1, 1, 1, 1, 1]; dl3 = [1, -1, 1, -1, -1]
c2_s3 = [R(1,2) - t/4, R(1,4), t/4, R(1,4), sp.Integer(0)]
ok3, d3 = stage_check(c2_s3, eps3, dl3, "S3")
# continuity at stage boundaries (c^2 vectors match; vertex-2 sign flip occurs AT c2=0 -> W continuous)
b12 = all(sp.simplify(a.subs(t,1) - b.subs(t,0)) == 0 for a, b in zip(c2_s1, c2_s2))
b23 = all(sp.simplify(a.subs(t,1) - b.subs(t,0)) == 0 for a, b in zip(c2_s2, c2_s3))

# ---------- Exact endpoints ----------
def W_of(c2list, eps, dl, tval):
    cs = [sp.sqrt(sp.nsimplify(c2.subs(t, tval))) for c2 in c2list]
    uu_ = sp.Matrix([e*c for e, c in zip(eps, cs)])
    vv_ = sp.Matrix([d*c for d, c in zip(dl, cs)])
    return sp.expand(2*uu_*uu_.T - 2*vv_*vv_.T)
W_start = W_of(c2_s1, eps1, dl1, 0)
W_end   = W_of(c2_s3, eps3, dl3, 1)
def adjm(edges):
    A = sp.zeros(m)
    for i, j in edges: A[i, j] = A[j, i] = 1
    return A
is_star  = sp.simplify(W_start - adjm([(0,1),(0,2),(0,3),(0,4)])) == sp.zeros(m)
is_cycle = sp.simplify(W_end   - adjm([(0,1),(1,2),(2,3),(3,0)])) == sp.zeros(m)
# spot exact charpoly checks at endpoints + one interior point per stage (belt and braces)
lam = sp.symbols('lam')
def cp_ok(Wm): return sp.expand(Wm.charpoly(lam).as_expr() - (lam**5 - 4*lam**3)) == 0
interior_ok = all(cp_ok(W_of(c2, e, d, R(1,3))) and
                  all(sp.simplify(W_of(c2, e, d, R(1,3))[i, i]) == 0 for i in range(m))
                  for c2, e, d in [(c2_s1, eps1, dl1), (c2_s2, eps2, dl2), (c2_s3, eps3, dl3)])

V = {"Lemma1_eigen_u": bool(lem1a), "Lemma1_eigen_v": bool(lem1b), "Lemma1_diag": bool(lem1c),
     "Stage1": bool(ok1), "Stage2": bool(ok2), "Stage3": bool(ok3),
     "boundary_12": bool(b12), "boundary_23": bool(b23),
     "endpoint_star_exact": bool(is_star), "endpoint_cycle_exact": bool(is_cycle),
     "interior_membership_exact": bool(interior_ok)}
rec = {"verdicts": V, "note": "path = 3 stages, each linear-in-t in c^2 coordinates; sign flip of vertex 2 occurs at c2=0 (W continuous); every path point in the fiber by Lemma-1 + stage constraints"}
blob = json.dumps(rec, sort_keys=True, indent=1)
print(blob)
print("RECORDS_SHA256", hashlib.sha256(blob.encode()).hexdigest()[:16])
print("ALL_PASS" if all(V.values()) else "FAIL")
