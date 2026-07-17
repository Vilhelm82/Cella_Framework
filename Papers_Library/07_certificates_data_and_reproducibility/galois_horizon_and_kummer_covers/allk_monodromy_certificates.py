#!/usr/bin/env python3
# All-k monodromy certificates: k=3 and k=6 axial norms. Exact, stdlib only.
# k=3: 4M=32,  N=(4,8,16)            degree 4  target S_4
# k=6: 4M=256, N=(4,8,16,32,64,128)  degree 22 target S_22
# Anchor: rebuilds banked k=4 Point-B quintic before anything else.
import math, itertools, hashlib, sys

def trim(a):
    while a and a[-1] == 0: a.pop()
    return a

def padd(a, b):
    r = [0] * max(len(a), len(b))
    for i, c in enumerate(a): r[i] += c
    for i, c in enumerate(b): r[i] += c
    return trim(r)

def psub(a, b):
    r = [0] * max(len(a), len(b))
    for i, c in enumerate(a): r[i] += c
    for i, c in enumerate(b): r[i] -= c
    return trim(r)

def pmul(a, b):
    if not a or not b: return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    return trim(r)

def pscale(a, c):
    return [] if c == 0 else [c * x for x in a]

def btrim(P):
    while P and not P[-1]: P.pop()
    return P

def bmul(P, Q):
    if not P or not Q: return []
    R = [[] for _ in range(len(P) + len(Q) - 1)]
    for i, a in enumerate(P):
        if a:
            for j, b in enumerate(Q):
                if b: R[i + j] = padd(R[i + j], pmul(a, b))
    return btrim(R)

def bsub(P, Q):
    n = max(len(P), len(Q)); R = []
    for i in range(n):
        a = P[i] if i < len(P) else []
        b = Q[i] if i < len(Q) else []
        R.append(psub(a, b))
    return btrim(R)

def bmul_upoly(P, g):
    return btrim([pmul(c, g) if c else [] for c in P])

def norm_step(P, Nsq):
    wsq = [Nsq, 1]
    degx = len(P) - 1
    wp = [[1]]
    for _ in range(degx // 2 + 1): wp.append(pmul(wp[-1], wsq))
    A = [[] for _ in range(degx + 1)]
    B = [[] for _ in range(degx + 1)]
    for j, cj in enumerate(P):
        if not cj: continue
        for t in range(j + 1):
            term = pscale(cj, math.comb(j, t))
            s, par = divmod(t, 2)
            if s: term = pmul(term, wp[s])
            k = j - t
            if par == 0: A[k] = padd(A[k], term)
            else:        B[k] = padd(B[k], term)
    A = btrim(A); B = btrim(B)
    return bsub(bmul(A, A), bmul_upoly(bmul(B, B), wsq))

def build_norm(M4, Ns):
    P = [[], [1]]
    for N in Ns:
        P = norm_step(P, N * N)
    f_raw = []
    xp = 1
    for c in P:
        if c: f_raw = padd(f_raw, pscale(c, xp))
        xp *= M4
    g = 0
    for c in f_raw: g = math.gcd(g, c)
    f = [c // g for c in f_raw]
    if f[-1] < 0: f = [-c for c in f]
    return f, f_raw

def delta(k):
    return 2 ** (k - 1) if k % 2 else 2 ** (k - 1) - math.comb(k, k // 2) // 2

# ---------- mod-p machinery ----------
def make_monic(a, p):
    inv = pow(a[-1] % p, p - 2, p)
    return [(c * inv) % p for c in a]

def rem_mod(a, fm, p):
    a = [c % p for c in a]
    df = len(fm) - 1
    for i in range(len(a) - 1, df - 1, -1):
        c = a[i]
        if c:
            for j in range(df + 1):
                a[i - df + j] = (a[i - df + j] - c * fm[j]) % p
    return trim(a[:df])

def mulmod(a, b, fm, p):
    return rem_mod(pmul(a, b), fm, p)

def powmod(a, e, fm, p):
    r = [1]; b = a[:]
    while e:
        if e & 1: r = mulmod(r, b, fm, p)
        b = mulmod(b, b, fm, p); e >>= 1
    return r

def gcdp(a, b, p):
    a = trim([c % p for c in a]); b = trim([c % p for c in b])
    while b:
        bm = make_monic(b, p)
        r = rem_mod(a, bm, p)
        a, b = b, r
    return make_monic(a, p) if a else []

def pdiv(a, g, p):
    a = [c % p for c in a]; dg = len(g) - 1
    q = [0] * (len(a) - dg)
    for i in range(len(a) - 1, dg - 1, -1):
        c = a[i] % p
        if c:
            q[i - dg] = c
            for j in range(dg + 1):
                a[i - dg + j] = (a[i - dg + j] - c * g[j]) % p
    return trim(q)

def cycle_type(f, p):
    if f[-1] % p == 0: return None
    fm = make_monic([c % p for c in f], p)
    dfm = trim([(i * c) % p for i, c in enumerate(fm)][1:])
    if len(gcdp(fm, dfm, p)) - 1 > 0: return None
    typ = []; rem = fm[:]; h = [0, 1]; d = 0
    while len(rem) - 1 > 0:
        d += 1
        if 2 * d > len(rem) - 1:
            typ.append(len(rem) - 1); break
        h = powmod(h, p, fm, p)
        g = gcdp(psub(h, [0, 1]), rem, p)
        dg = len(g) - 1
        if dg > 0:
            typ += [d] * (dg // d)
            rem = pdiv(rem, g, p)
    typ.sort()
    return typ

def sieve(nmax):
    s = [True] * (nmax + 1); s[0] = s[1] = False
    for i in range(2, int(nmax ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, nmax + 1, i): s[j] = False
    return [i for i, b in enumerate(s) if b]

PRIMES = sieve(1500)

def analyze(k, M4, Ns):
    n_target = delta(k)
    assert M4 > sum(Ns), "not in strict chamber"
    f, f_raw = build_norm(M4, Ns)
    n = len(f) - 1
    print(f"--- k={k}: 4M={M4}, N={tuple(Ns)} ---")
    print(f"degree: {n} (law predicts {n_target})")
    assert n == n_target
    print("lc (primitive):", f[-1])
    # constant-term cross-check against the direct wall product
    prod = 1
    for eps in itertools.product([1, -1], repeat=k):
        prod *= M4 - sum(e * N for e, N in zip(eps, Ns))
    print("f_raw(0) == wall product over 2^k sign vectors:", f_raw[0] == prod)
    assert f[0] != 0

    jprimes = [p for p in PRIMES if 2 * p > n and p <= n - 3]
    irr_p = jordan_p = odd_p = three_p = None
    table = []
    for p in PRIMES:
        if p < 3: continue
        t = cycle_type(f, p)
        if t is None: continue
        assert sum(t) == n
        table.append((p, t))
        if t == [n] and irr_p is None: irr_p = p
        if jordan_p is None and any(q in t for q in jprimes): jordan_p = p
        if odd_p is None and (n - len(t)) % 2 == 1: odd_p = p
        if n == 4 and three_p is None and t == [1, 3]: three_p = p
        settled = irr_p and odd_p and (jordan_p or (n == 4 and three_p))
        if settled and len(table) >= 20: break

    print("first cycle types:")
    for p, t in table[:14]:
        print(f"  {p:5d} : {t}")
    print("witnesses: irreducible:", irr_p,
          "| jordan(p in", jprimes, "):", jordan_p,
          "| odd:", odd_p, ("| 3-cycle: " + str(three_p)) if n == 4 else "")
    if n == 4:
        ok = irr_p and three_p and odd_p
        why = ("transitive (irred) + 3-cycle excludes D4,C4,V4 => A4 or S4; "
               "odd element => S4")
    else:
        ok = irr_p and jordan_p and odd_p
        why = (f"transitive (irred) + p-cycle p>{n//2} kills all block systems "
               f"=> primitive; Jordan (p<=n-3) => contains A{n}; odd => S{n}")
    verdict = f"S{n}" if ok else "INCONCLUSIVE AT THIS POINT"
    print("VERDICT:", verdict, "--", why if ok else "")
    print()
    return f, table, (irr_p, jordan_p, odd_p, three_p), verdict

# ---------- anchor ----------
NB = [-292521804394659840000, 4906654632404582400, -21548253194223616,
      40515442790400, -34962080625, 11390625]
f4, _ = build_norm(60, [4, 8, 12, 20])
print("k=4 Point-B anchor:", "MATCH" if f4 == NB else "FAIL")
assert f4 == NB
print()

res3 = analyze(3, 32, [4, 8, 16])
res6 = analyze(6, 256, [4, 8, 16, 32, 64, 128])

with open("/home/claude/allk_results.txt", "w") as out:
    for k, (f, table, wit, verdict) in [(3, res3), (6, res6)]:
        out.write(f"# k={k} verdict {verdict}\n")
        out.write("coefficients (low first):\n")
        for i, c in enumerate(f): out.write(f"u^{i}: {c}\n")
        out.write("cycle types:\n")
        for p, t in table: out.write(f"{p}: {t}\n")
        out.write(f"witnesses: {wit}\n\n")

src = open(__file__, "rb").read()
print("script sha256:", hashlib.sha256(src).hexdigest())
