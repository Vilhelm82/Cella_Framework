#!/usr/bin/env python3
"""REALFIBER full-fiber theorem certificate.
Certifies: (a) discrete move-graph connectivity for m=3,4,5 (the combinatorial core of O5),
(b) the m=2 boundary (fiber = exactly two points), (c) structure-law identities (O1, symbolic).
The continuous glue (O3 convexity, O4 move realization, O6 lift, O7 locking) is proven in prose
in REALFIBER_THEOREM.md; this script certifies every machine-checkable component."""
import json, hashlib
from itertools import combinations, product
import sympy as sp

# ---------- (c) O1 structure-law identities, fully symbolic (any m via m=5 template + general arg) ----------
m5 = 5
u = sp.Matrix(sp.symbols('u0:5', real=True)); v = sp.Matrix(sp.symbols('v0:5', real=True))
a = sp.symbols('a', positive=True)
W = a*(u*u.T - v*v.T)
uu, vv, uv = (u.T*u)[0], (v.T*v)[0], (u.T*v)[0]
O1a = all(sp.simplify(sp.expand((W*u)[i] - a*u[i]) - (a*u[i]*(uu-1) - a*v[i]*uv)) == 0 for i in range(m5))
O1b = all(sp.simplify(sp.expand((W*v)[i] + a*v[i]) - (-a*v[i]*(vv-1) + a*u[i]*uv)) == 0 for i in range(m5))
O1c = all(sp.simplify(W[i, i] - a*(u[i]**2 - v[i]**2)) == 0 for i in range(m5))
# bipartite law: W_ij = a c_i c_j (e_i e_j - d_i d_j) vanishes when s_i s_j = +1  [symbolic on signs]
e0,e1,d0,d1,c0,c1 = sp.symbols('e0 e1 d0 d1 c0 c1', real=True)
O1d = sp.simplify((e0*e1 - d0*d1).subs({d0: e0*1, d1: e1*1})) == 0   # s_i=s_j=+1 -> 0
O1e = sp.simplify((e0*e1 - d0*d1).subs({d0: -e0, d1: -e1})) == 0    # s_i=s_j=-1 -> 0

# ---------- (b) m=2 boundary: fiber is exactly two points ----------
w = sp.symbols('w', real=True)
lam = sp.symbols('lam')
cp2 = sp.Matrix([[0, w], [w, 0]]).charpoly(lam).as_expr()
sols = sp.solve(sp.Eq(cp2, lam**2 - a**2), w)   # charpoly must equal lam^2 - a^2
Bm2 = (set(sols) == {a, -a})                     # exactly two points, +-a; finite => 2 components

# ---------- (a) discrete move-graph connectivity, m = 3, 4, 5 ----------
def move_graph_components(m):
    """Nodes: (frozen active set A as frozenset, class map s on A both classes nonempty, eps on A).
    Edges: PARK i (allowed iff |class(i)| >= 2) <-> REVIVE (reverse; any class, any eps)."""
    nodes = []
    idx = {}
    for k in range(2, m + 1):
        for A in combinations(range(m), k):
            for sbits in product((1, -1), repeat=k):
                if all(b == 1 for b in sbits) or all(b == -1 for b in sbits):
                    continue
                for ebits in product((1, -1), repeat=k):
                    node = (A, sbits, ebits)
                    idx[node] = len(nodes); nodes.append(node)
    # union-find
    parent = list(range(len(nodes)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry: parent[rx] = ry
    for node, ni in idx.items():
        A, sbits, ebits = node
        for pos, i in enumerate(A):
            cls = sbits[pos]
            if sum(1 for b in sbits if b == cls) >= 2:      # PARK i allowed
                A2 = tuple(x for x in A if x != i)
                s2 = tuple(b for p, b in enumerate(sbits) if p != pos)
                e2 = tuple(b for p, b in enumerate(ebits) if p != pos)
                union(ni, idx[(A2, s2, e2)])
    return len({find(i) for i in range(len(nodes))}), len(nodes)

comp3, n3 = move_graph_components(3)
comp4, n4 = move_graph_components(4)
comp5, n5 = move_graph_components(5)

V = {"O1_eigen_u": bool(O1a), "O1_eigen_v": bool(O1b), "O1_diag": bool(O1c),
     "O1_bipartite_same_class_vanishes": bool(O1d and O1e),
     "m2_two_points": bool(Bm2),
     "movegraph_m3_connected": comp3 == 1, "movegraph_m4_connected": comp4 == 1,
     "movegraph_m5_connected": comp5 == 1}
rec = {"verdicts": V,
       "movegraph_sizes": {"m3": n3, "m4": n4, "m5": n5},
       "movegraph_components": {"m3": comp3, "m4": comp4, "m5": comp5},
       "note": "park allowed iff vertex's class retains a member; revive = reverse edge, any class/eps"}
blob = json.dumps(rec, sort_keys=True, indent=1)
print(blob)
print("RECORDS_SHA256", hashlib.sha256(blob.encode()).hexdigest()[:16])
print("ALL_PASS" if all(V.values()) else "FAIL")
