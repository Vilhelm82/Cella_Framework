#!/usr/bin/env python3
"""hunt_v2_msolve.py — P-F3 hunt, addendum v2 (route b). Pin 70ed8967e1f06b24.
Same eight slice systems as v1 (K=6/D=15 interpolation, self-checked); engine = msolve RUR.
Blob = canonical rational-point sets + verdicts only. role=probe.
"""
import sys, os, json, time, subprocess, ast, hashlib
from fractions import Fraction as Fr
from math import lcm

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "portfolio", "campaigns", "the_engine", "stage_A"))
sys.path.insert(0, os.path.join(REPO, "evals", "dbp_involution"))
import engine_harness as EH
import flagship_stageA_battery as B
import sympy as sp

ADDENDUM = os.path.join(HERE, "HUNT_ADDENDUM_v2_2.md")
PIN = "a9d02dac46fea22e"
ADDENDUM3 = os.path.join(HERE, "HUNT_ADDENDUM_v2_3.md")
PIN3 = "15f4ab251ce34645"
MSOLVE = os.path.expanduser("~/msolve_jll/bin/msolve")
MSOLVE_PIN = "2caed4b3596acb38"
MSOLVE_ENV = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser("~/msolve_jll/lib"))

HB = {
 "HB.1pp": "HB.1'': after the pinned K=6, D=15 interpolation with fresh-point self-check, each tie polynomial is exactly divided by the Cayley denominators D1(t1) and D2(t2,t3) to maximal powers with zero remainder required at every step and the division multiplicities (a1_X, a2_X) recorded; saturation is verified at three fresh rational points by the exact identity P_sat(p) * D1(p)^a1_X * D2(p)^a2_X == P_raw(p); the saturated system is handed to msolve with integer-cleared coefficients; D1 and D2 are bounded below by 1 on the reals, so no rational point is removed.",
 "HB.2": "HB.2: a WITNESS_FOUND is banked only after the unchanged exact certification: all three m2 ties, Ehat ties for r=1..4, O2 != O1, at pairwise-distinct g.",
 "HB.3": "HB.3: an EMPTY_CERTIFIED verdict requires msolve completion with an eliminating polynomial whose nonzero rational roots are exhaustively excluded by exact rational root finding.",
 "HB.4": "HB.4: per-slice cap 600 seconds; caps, timings, and raw solver output live outside the hashed blob; the blob carries only the canonical rational-point sets and verdicts, and is byte-stable across two independent runs.",
 "HB.6": 'HB.6: for any slice whose saturated system is msolve-certified positive-dimensional, the runner intersects it with the pinned blind hyperplane schedule [t3 = 1, t3 = 1/2, t1 + t2 + t3 = 1, t1 - t2 = 1/3] in that order, solves each 0-dimensional result with msolve under the same 600-second cap, extracts rational points exactly per HB.3 semantics, certifies every candidate with the unchanged exact pipeline, and banks per-plane point sets canonically; the schedule was pinned before any curve was examined.',
 "HB.5": "HB.5: outcome routing \u2014 any WITNESS_FOUND routes to Will same breath; eight EMPTY_CERTIFIED verdicts constitute the route-(a) decision evidence and route as such; SOLVER_INCOMPLETE and error data are banked verbatim.",
}
PINS = {
 "portfolio/campaigns/shape_witness/FLAGSHIP_STAGE_A_PREREG.md": "d5e69a10fee4897d",
 "portfolio/campaigns/shape_witness/flagship_stageA_battery.py": "81bc3de5e0a9937b",
 "portfolio/campaigns/the_engine/stage_A/engine_harness.py": "7f0e5e7e4f4d54a6",
 "evals/dbp_involution/rep_utils.py": "0d838e5fd430461b",
}

n, N = 5, 10
PAIRS = B.pairs_of(n); IDX = B.idx_of(PAIRS)
Ps = B.projectors(n, PAIRS, IDX)
g = [Fr(x) for x in (1, 2, 3, 5, 7)]
H = [[Fr(0)]*n for _ in range(n)]
OFFD = [Fr(x) for x in (1, -2, 3, 1, 2, -1, 4, -3, 1, 2)]
for (i, j), v in zip(PAIRS, OFFD): H[i][j] = H[j][i] = v
O1 = B.O_of(H, g, PAIRS); M_T = B.m2s(O1, Ps, N)
E1 = [B.Ehat(H, g, n, r) for r in (1, 2, 3, 4)]
GG = sum(x*x for x in g)

def perp(w):
    wg = sum(Fr(a)*b for a, b in zip(w, g))
    return [Fr(a) - wg*b/GG for a, b in zip(w, g)]

def make_eval(slate):
    u1, v1, u2, v2, e = slate
    pu1, pv1, pu2, pv2, pe = (perp(w) for w in (u1, v1, u2, v2, e))
    def evalpt(a1, a2, a3):
        U1 = [x + a1*y for x, y in zip(pu1, pe)]
        U2 = [x + a2*y + a3*z for x, y, z in zip(pu2, pe, pv1)]
        A = B.matmul(B.cayley(U1, pv1, g, n), B.cayley(U2, pv2, g, n), n)
        H2 = B.matmul(B.matT(A), B.matmul(H, A, n), n)
        return H2, B.m2s(B.O_of(H2, g, PAIRS), Ps, N)
    def D1f(a1):
        U1 = [x + a1*y for x, y in zip(pu1, pe)]
        return 1 + B.dotf(U1, U1)*B.dotf(pv1, pv1) - B.dotf(U1, pv1)**2
    def D2f(a2, a3):
        U2 = [x + a2*y + a3*z for x, y, z in zip(pu2, pe, pv1)]
        return 1 + B.dotf(U2, U2)*B.dotf(pv2, pv2) - B.dotf(U2, pv2)**2
    return evalpt, D1f, D2f

def build_polys(si):
    evalpt, D1f, D2f = make_eval(B.SLATES[si])
    K, D = 6, 15
    xs = [Fr(k) for k in range(-(D//2), D - D//2)]
    grid = {}
    for a1 in xs:
        for a2 in xs:
            for a3 in xs:
                _, mm = evalpt(a1, a2, a3)
                w = D1f(a1)**K * D2f(a2, a3)**K
                grid[(a1, a2, a3)] = [(mm[X]-M_T[X])*w for X in range(3)]
    polys = []
    for X in range(3):
        c3 = {}
        for a1 in xs:
            for a2 in xs:
                co = B.interp_1d(xs, [grid[(a1, a2, a3)][X] for a3 in xs])
                for k3, c in enumerate(co): c3.setdefault(k3, {})[(a1, a2)] = c
        cdict = {}
        for k3, tbl in c3.items():
            c2 = {}
            for a1 in xs:
                co = B.interp_1d(xs, [tbl.get((a1, a2), Fr(0)) for a2 in xs])
                for k2, c in enumerate(co): c2.setdefault(k2, {})[a1] = c
            for k2, tb1 in c2.items():
                co = B.interp_1d(xs, [tb1.get(a1, Fr(0)) for a1 in xs])
                for k1, c in enumerate(co):
                    if c != 0: cdict[(k1, k2, k3)] = c
        import random as _r; rr = _r.Random(2000 + si)
        for _ in range(3):
            p = tuple(Fr(rr.randint(8, 12), rr.choice([1, 3])) for _ in range(3))
            _, mm = evalpt(*p)
            direct = (mm[X]-M_T[X])*D1f(p[0])**K*D2f(p[1], p[2])**K
            val = sum(c*p[0]**i*p[1]**j*p[2]**k for (i, j, k), c in cdict.items())
            if val != direct: raise RuntimeError(f"self-check failed slice {si} X={X}")
        polys.append(cdict)
    return polys, evalpt

def poly_to_ms(cdict):
    L = 1
    for c in cdict.values(): L = lcm(L, c.denominator)
    terms = []
    for (i, j, k), c in sorted(cdict.items()):
        ci = int(c*L)
        if ci == 0: continue
        mono = "*".join(([f"t1^{i}"] if i else []) + ([f"t2^{j}"] if j else []) + ([f"t3^{k}"] if k else [])) or "1"
        terms.append(f"{'+' if ci > 0 and terms else ''}{ci}*{mono}")
    return "".join(terms)

def parse_rur(text):
    s = text.strip().rstrip(":").strip()
    data = ast.literal_eval(s)
    if data == [-1] or data[0] == -1:
        return {"kind": "inconsistent"}
    if data[0] != 0:
        return {"kind": "posdim", "dim": data[0]}
    body = data[1]
    nvars = body[1]; varnames = body[3]; lf = body[4]
    rur = body[5]
    blocks = rur[1]
    wdeg, wco = blocks[0]
    dpair = blocks[1]
    vlist = blocks[2]
    return {"kind": "rur", "nvars": nvars, "vars": varnames, "lf": lf,
            "w": wco, "d": dpair[1],
            "vs": [(v[0][1] if isinstance(v[0], list) and len(v[0]) == 2 and isinstance(v[0][1], list) else v[0]) for v in vlist]}

def rational_points(r):
    t = sp.symbols("t")
    w = sp.Poly(list(reversed(r["w"])), t)
    roots = [q for q in sp.roots(w, filter="Q")]
    pts = []
    d = sp.Poly(list(reversed(r["d"])), t)
    for q in roots:
        dq = d.eval(q)
        if dq == 0: continue
        coords = []
        for vco in r["vs"]:
            v = sp.Poly(list(reversed(vco)), t)
            coords.append(sp.Rational(-v.eval(q), 1)/dq)
        if len(coords) == r["nvars"] - 1:
            # separating variable = the one with lf coefficient 1 (msolve convention: last listed nonzero)
            known = coords
            csum = sum(sp.Rational(c)*x for c, x in zip(r["lf"][:-1], known))
            last = (q - csum)/sp.Rational(r["lf"][-1]) if r["lf"][-1] != 0 else q
            coords = known + [last]
        pts.append(tuple(Fr(int(sp.numer(c)), int(sp.denom(c))) for c in coords))
    return sorted(set(pts))

PARENT = os.path.join(HERE, "HUNT_ADDENDUM_v2.md")
PARENT_PIN = "70ed8967e1f06b24"

def main():
    EH.clause_gate(ADDENDUM, {"HB.1pp": HB["HB.1pp"]}, PIN)
    EH.clause_gate(ADDENDUM3, {"HB.6": HB["HB.6"]}, PIN3)
    EH.clause_gate(PARENT, {k: v for k, v in HB.items() if k not in ("HB.1pp", "HB.6")}, PARENT_PIN)
    EH.pin_gate(PINS)
    got = hashlib.sha256(open(MSOLVE, "rb").read()).hexdigest()[:16]
    if got != MSOLVE_PIN: raise SystemExit(f"REFUSE[ENGINE_PIN] msolve {got} != {MSOLVE_PIN}")
    print("GATES_GREEN addendum_pin", PIN, "engine_pin", MSOLVE_PIN)
    blob, tm = {}, {}
    for si in range(len(B.SLATES)):
        t0 = time.perf_counter()
        polys, evalpt = build_polys(si)
        t1s, t2s, t3s = sp.symbols("t1 t2 t3")
        _, D1f, D2f = make_eval(B.SLATES[si])
        d1co = B.interp_1d([Fr(-1), Fr(0), Fr(1)], [D1f(Fr(-1)), D1f(Fr(0)), D1f(Fr(1))])
        D1p = sp.Poly(sum(sp.Rational(c.numerator, c.denominator)*t1s**k for k, c in enumerate(d1co)), t1s, t2s, t3s)
        pts2 = [(Fr(a), Fr(b)) for a in (-1, 0, 1) for b in (-1, 0, 1)]
        D2expr = sp.Integer(0)
        m2co = {}
        for (i2, j2) in [(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]:
            pass
        # build D2 exactly by symbolic expansion (quadratic, tiny)
        u2p = [sp.Rational(x.numerator, x.denominator) for x in ( [q for q in ()] )] if False else None
        sl = B.SLATES[si]
        pu2 = [sp.Rational(x.numerator, x.denominator) for x in perp(sl[2])]
        pe_ = [sp.Rational(x.numerator, x.denominator) for x in perp(sl[4])]
        pv1_ = [sp.Rational(x.numerator, x.denominator) for x in perp(sl[1])]
        pv2_ = [sp.Rational(x.numerator, x.denominator) for x in perp(sl[3])]
        U2s = [a + t2s*b + t3s*c for a, b, c in zip(pu2, pe_, pv1_)]
        D2p = sp.Poly(sp.expand(1 + sum(x*x for x in U2s)*sum(y*y for y in pv2_) - sum(x*y for x, y in zip(U2s, pv2_))**2), t1s, t2s, t3s)
        sat = []
        mults = []
        for X, cd in enumerate(polys):
            P = sp.Poly(sum(sp.Rational(c.numerator, c.denominator)*t1s**i*t2s**j*t3s**k for (i, j, k), c in cd.items()), t1s, t2s, t3s)
            P_raw = P; mult = {"D1": 0, "D2": 0}
            for Dp, nm in ((D1p, "D1"), (D2p, "D2")):
                while True:
                    q, r = sp.div(P, Dp, domain="QQ")
                    if r == 0 and not q.is_zero: P = sp.Poly(q, t1s, t2s, t3s); mult[nm] += 1
                    else: break
            import random as _r2; rr2 = _r2.Random(3000 + si*10 + X)
            for _ in range(3):
                pt = {t1s: sp.Rational(rr2.randint(13, 17), rr2.choice([1, 2])),
                      t2s: sp.Rational(rr2.randint(13, 17), rr2.choice([1, 2])),
                      t3s: sp.Rational(rr2.randint(13, 17), rr2.choice([1, 2]))}
                lhs = P.as_expr().subs(pt) * D1p.as_expr().subs(pt)**mult["D1"] * D2p.as_expr().subs(pt)**mult["D2"]
                assert sp.simplify(lhs - P_raw.as_expr().subs(pt)) == 0, f"saturation consistency failed X={X}"
            mults.append([mult["D1"], mult["D2"]])
            sat.append({m: Fr(int(sp.numer(c)), int(sp.denom(c))) for m, c in zip(P.monoms(), P.coeffs())})
        print(f"[hb] slice {si}: saturated degs {[max(sum(m) for m in s) if s else 0 for s in sat]}", file=sys.stderr, flush=True)
        polys = sat
        ms = "t1,t2,t3\n0\n" + ",\n".join(poly_to_ms(p) for p in polys) + "\n"
        fin, fout = f"/tmp/hv2_s{si}.ms", f"/tmp/hv2_s{si}.out"
        open(fin, "w").write(ms)
        rec = {"slice": si, "sat_mult": mults}
        try:
            pr = subprocess.run([MSOLVE, "-P", "2", "-f", fin, "-o", fout],
                                env=MSOLVE_ENV, capture_output=True, timeout=600)
            r = parse_rur(open(fout).read())
            if r["kind"] == "inconsistent":
                rec.update(verdict="EMPTY_CERTIFIED", note="inconsistent_over_closure", points=[])
            elif r["kind"] == "posdim":
                rec.update(dim=r["dim"])
                planes = [("t3-1", "1*t3-1"), ("t3-1/2", "2*t3-1"), ("t1+t2+t3-1", "1*t1+1*t2+1*t3-1"), ("t1-t2-1/3", "3*t1-3*t2-1")]
                per_plane, wit = {}, None
                for pname, pexpr in planes:
                    fin2, fout2 = f"/tmp/hv2_s{si}_{pname.replace('/','_').replace('+','p')}.ms", f"/tmp/hv2_s{si}_plane.out"
                    open(fin2, "w").write("t1,t2,t3\n0\n" + ",\n".join(poly_to_ms(p) for p in polys) + ",\n" + pexpr + "\n")
                    try:
                        subprocess.run([MSOLVE, "-P", "2", "-f", fin2, "-o", fout2], env=MSOLVE_ENV, capture_output=True, timeout=600)
                        r2 = parse_rur(open(fout2).read())
                        if r2["kind"] == "rur":
                            pts2 = [p for p in rational_points(r2) if p != (0, 0, 0)]
                            per_plane[pname] = [[B.to_s(x) for x in p] for p in pts2]
                            for p in pts2:
                                H2, mm = evalpt(*p)
                                if mm != M_T: continue
                                O2 = B.O_of(H2, g, PAIRS)
                                E2 = [B.Ehat(H2, g, n, r_) for r_ in (1, 2, 3, 4)]
                                if E2 == E1 and O2 != O1:
                                    wit = {"plane": pname, "t": [B.to_s(x) for x in p], "O2": [B.to_s(x) for x in O2],
                                           "m2_tied": [B.to_s(x) for x in mm], "Ehat_tied": [B.to_s(x) for x in E2]}
                                    break
                        else:
                            per_plane[pname] = {"kind": r2["kind"]}
                    except subprocess.TimeoutExpired:
                        per_plane[pname] = "SOLVER_INCOMPLETE"
                    if wit: break
                rec["plane_points"] = per_plane
                if wit: rec.update(verdict="WITNESS_FOUND", witness=wit)
                else: rec.update(verdict="DIM_POSITIVE_NO_RATIONAL_ON_PLANES", points=[])
            else:
                pts = [p for p in rational_points(r) if p != (0, 0, 0)]
                rec["points"] = [[B.to_s(x) for x in p] for p in pts]
                rec["w_degree"] = len(r["w"]) - 1
                wit = None
                for p in pts:
                    H2, mm = evalpt(*p)
                    if mm != M_T: continue
                    O2 = B.O_of(H2, g, PAIRS)
                    E2 = [B.Ehat(H2, g, n, r_) for r_ in (1, 2, 3, 4)]
                    if E2 == E1 and O2 != O1:
                        wit = {"t": [B.to_s(x) for x in p], "O2": [B.to_s(x) for x in O2],
                               "m2_tied": [B.to_s(x) for x in mm], "Ehat_tied": [B.to_s(x) for x in E2]}
                        break
                if wit: rec.update(verdict="WITNESS_FOUND", witness=wit)
                else: rec.update(verdict="EMPTY_CERTIFIED" if not pts else "POINTS_UNCERTIFIED")
        except subprocess.TimeoutExpired:
            rec.update(verdict="SOLVER_INCOMPLETE", points=[])
        except Exception as ex:
            rec.update(verdict="ERROR", error=str(ex)[:150], points=[])
        tm[f"s{si}"] = round(time.perf_counter()-t0, 2)
        print(f"[hb] slice {si}: {rec['verdict']} {tm[f's{si}']}s", file=sys.stderr, flush=True)
        blob[f"s{si}"] = rec
    verdicts = [blob[f"s{k}"]["verdict"] for k in range(len(B.SLATES))]
    blob["hunt_v2_outcome"] = ("WITNESS_FOUND" if "WITNESS_FOUND" in verdicts
                               else "ALL_EMPTY_CERTIFIED" if all(v == "EMPTY_CERTIFIED" for v in verdicts)
                               else "MIXED")
    out = json.dumps(blob, sort_keys=True, indent=1)
    print(out)
    print("RECORDS_SHA256", EH.records_sha(out))
    print("TIMINGS_JSON", json.dumps(tm, sort_keys=True))
    print("HUNT_V2_COMPLETE")

if __name__ == "__main__":
    main()
