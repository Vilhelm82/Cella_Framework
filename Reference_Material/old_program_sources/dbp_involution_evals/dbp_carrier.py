"""
dbp_carrier.py -- The DBP coupling-carrier 'engine' for the involution campaign.

These are the objects UNDER TEST.  They are built here from the gauge structure of
CALC-14 (ker L = the defining-function gauge {v(x)g + g(x)v}), derived independently;
no values, conventions, or results are lifted from the parallel
`dbp_prime2_structure` campaign.  Characters are computed here as TRACES OF EXPLICIT
MATRICES (the engine's own route); the independent `rep_utils` referee computes the
same characters via Murnaghan-Nakayama, and the stage scripts compare the two.

Exact arithmetic only: sympy Integer / Rational / Matrix, and explicit mod-p
integer linear algebra.  No float anywhere.

Carrier realizations (all have Im ~= Sym^2(std), ker = gauge, rank = C(n,2)):
  * L_int  : H |-> ( 2 H_ij - H_ii - H_jj )_{i<j}      -- integral, pair-indexed (mine)
  * L_flag : H |-> ( -(H_jl - H_jk - H_kl + H_kk) )      -- the coupling-numerator
             over flags (k,{j,l}), k not in {j,l}        -- the standard DBP object
"""

from __future__ import annotations

from itertools import combinations
import sympy as sp
from sympy import Matrix, Rational, Integer, zeros

# Neutral (non-referee) helpers: permutations & the integral std rep.
from rep_utils import (
    class_rep, conjugacy_classes, partitions, compose, std_matrix, fix,
)


# --------------------------------------------------------------------------- #
#  Bases / index maps                                                         #
# --------------------------------------------------------------------------- #

def sym2_basis(n):
    """Basis of Sym^2(Z^n) as ordered (i,j), i<=j  (E_ij = e_i e_j^T + e_j e_i^T,
    E_ii = e_i e_i^T)."""
    return [(i, j) for i in range(n) for j in range(i, n)]


def pair_basis(n):
    """Unordered pairs i<j  (the C(n,2) role-pairs)."""
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def flag_basis(n):
    """Flags (k,(j,l)) with j<l and k not in {j,l}."""
    return [(k, (j, l)) for j in range(n) for l in range(j + 1, n)
            for k in range(n) if k != j and k != l]


def _sym_idx(n):
    return {p: i for i, p in enumerate(sym2_basis(n))}


def _pair_idx(n):
    return {p: i for i, p in enumerate(pair_basis(n))}


def _key(i, j):
    return (i, j) if i <= j else (j, i)


# --------------------------------------------------------------------------- #
#  S_n action on Sym^2(Z^n) by conjugation  H |-> P H P^T                      #
# --------------------------------------------------------------------------- #

def conj_sym2(p, n):
    """Permutation matrix of sigma acting on the sym2 basis: E_ij -> E_{p(i)p(j)}."""
    basis = sym2_basis(n)
    idx = _sym_idx(n)
    m = len(basis)
    M = zeros(m, m)
    for c, (i, j) in enumerate(basis):
        img = _key(p[i], p[j])
        M[idx[img], c] = 1
    return M


def trace_on_subspace(A, B):
    """Trace of linear map A (square, exact) restricted to the A-invariant subspace
    spanned by the columns of B.  Solves A*B = B*C exactly and returns tr(C)."""
    # C = B^+ A B  via exact least-squares solve of B*C = A*B
    AB = A * B
    C = B.solve(AB)  # B may be non-square; sympy solves the consistent system
    return C.trace()


# --------------------------------------------------------------------------- #
#  Gauge   G_g(a) = a g^T + g a^T  at  g = (1,...,1)                           #
# --------------------------------------------------------------------------- #

def gauge_matrix(n):
    """M_G : Z^n -> Sym^2(Z^n), columns G_1(e_a).  G_1(e_a)_{kl} = [k=a]+[l=a].
    So column a has a 2 on diagonal E_aa and a 1 on each off-diagonal E_{a,l}."""
    basis = sym2_basis(n)
    idx = _sym_idx(n)
    M = zeros(len(basis), n)
    for a in range(n):
        for (i, j), r in idx.items():
            M[r, a] = ( (1 if i == a else 0) + (1 if j == a else 0) )
    return M


def ggT_vector(n):
    """g g^T at g=(1,...,1) as a Sym^2 coordinate vector: all-ones matrix.
    Diagonal entries 1, off-diagonal entries 1."""
    basis = sym2_basis(n)
    return Matrix(len(basis), 1, [1 for _ in basis])


# --------------------------------------------------------------------------- #
#  Carrier maps L : Sym^2(Z^n) -> coupling numerators                         #
# --------------------------------------------------------------------------- #

def L_int(n):
    """Integral pair-indexed carrier:  L(H)_{ij} = 2 H_ij - H_ii - H_jj  (i<j).
    Rows = pairs (C(n,2)); cols = sym2 basis (n(n+1)/2).  Integer matrix."""
    basis = sym2_basis(n)
    sidx = _sym_idx(n)
    pairs = pair_basis(n)
    M = zeros(len(pairs), len(basis))
    for r, (i, j) in enumerate(pairs):
        M[r, sidx[_key(i, j)]] += 2
        M[r, sidx[_key(i, i)]] += -1
        M[r, sidx[_key(j, j)]] += -1
    return M


def L_flag(n):
    """Coupling-numerator carrier over flags:
        Lambda_{k,{j,l}} = -(H_jl - H_jk - H_kl + H_kk)
                         = -H_jl + H_jk + H_kl - H_kk .
    Rows = flags (n*C(n-1,2)); cols = sym2 basis.  Integer matrix."""
    basis = sym2_basis(n)
    sidx = _sym_idx(n)
    flags = flag_basis(n)
    M = zeros(len(flags), len(basis))
    for r, (k, (j, l)) in enumerate(flags):
        M[r, sidx[_key(j, l)]] += -1
        M[r, sidx[_key(j, k)]] += 1
        M[r, sidx[_key(k, l)]] += 1
        M[r, sidx[_key(k, k)]] += -1
    return M


# --------------------------------------------------------------------------- #
#  std (x) std, swap involution tau, integral Sym/wedge split                 #
# --------------------------------------------------------------------------- #

def tensor_basis(n):
    """Basis of std (x) std as ordered (a,b), a,b in 0..n-2."""
    d = n - 1
    return [(a, b) for a in range(d) for b in range(d)]


def tensor_std_matrix(p, n):
    """Kronecker action of sigma on std (x) std (integer matrix), in tensor_basis."""
    S = std_matrix(p, n)  # (n-1)x(n-1) integer
    return sp.kronecker_product(S, S)


def tau_matrix(n):
    """Swap tau(f_a (x) f_b) = f_b (x) f_a on std (x) std (a permutation matrix)."""
    d = n - 1
    basis = tensor_basis(n)
    idx = {p: i for i, p in enumerate(basis)}
    M = zeros(d * d, d * d)
    for c, (a, b) in enumerate(basis):
        M[idx[(b, a)], c] = 1
    return M


def proj_to_std(n):
    """Integer (n-1) x n matrix q of the equivariant quotient R^n -> R^n/<1> ~= std,
    in the f-basis:  q(e_i) = f_i (i<n-1),  q(e_{n-1}) = -(f_0+...+f_{n-2})."""
    M = zeros(n - 1, n)
    for i in range(n - 1):
        M[i, i] = 1
        M[i, n - 1] = -1
    return M


def sym2_embed_tensor(n):
    """Embed Sym^2(R^n) into R^n (x) R^n (ordered, index i*n+j):
        E_ij (i<j) -> e_i(x)e_j + e_j(x)e_i ,   E_ii -> e_i(x)e_i ."""
    basis = sym2_basis(n)
    M = zeros(n * n, len(basis))
    for c, (i, j) in enumerate(basis):
        M[i * n + j, c] += 1
        if i != j:
            M[j * n + i, c] += 1
    return M


def carrier_into_tensor(n):
    """Explicit equivariant map  Sym^2(R^n) -> std (x) std  via (q (x) q) o embed.
    The Hessian is symmetric, so the image is tau-invariant (lands in Sym^2(std));
    the gauge {v(x)1 + 1(x)v} maps to 0 because q(1)=0, so this descends to an
    isomorphism  carrier = Sym^2(R^n)/gauge  ->  Sym^2(std)."""
    q = proj_to_std(n)
    qq = sp.kronecker_product(q, q)        # (n-1)^2 x n^2
    return qq * sym2_embed_tensor(n)       # (n-1)^2 x n(n+1)/2


def projectors(n):
    """Rational projectors P_+ = (I+tau)/2, P_- = (I-tau)/2 on std (x) std."""
    d = n - 1
    I = sp.eye(d * d)
    T = tau_matrix(n)
    return (I + T) / 2, (I - T) / 2


def sym_wedge_split_matrix(n):
    """Integral map Phi : std(x)std -> Sym^2(std) (+) wedge^2(std),
        f_a (x) f_b  |->  ( f_a (.) f_b ,  f_a (^) f_b )
    with  (.) = symmetric lattice gens {s_ab = e_a e_b + e_b e_a (a<b), s_aa = e_a e_a}
    and   (^) = alternating gens {w_ab = e_a e_b - e_b e_a (a<b)}.
    Returns (Phi, sym_dim, wedge_dim).  Integer matrix; SNF gives 2-primary torsion."""
    d = n - 1
    tb = tensor_basis(n)
    sym_gens = [(a, b) for a in range(d) for b in range(a, d)]   # a<=b
    wed_gens = [(a, b) for a in range(d) for b in range(a + 1, d)]  # a<b
    s_idx = {g: i for i, g in enumerate(sym_gens)}
    w_idx = {g: i for i, g in enumerate(wed_gens)}
    nsym, nwed = len(sym_gens), len(wed_gens)
    M = zeros(nsym + nwed, d * d)
    for c, (a, b) in enumerate(tb):
        if a == b:
            # f_a (.) f_a = 2 e_a e_a = 2 s_aa ;  f_a (^) f_a = 0
            M[s_idx[(a, a)], c] += 2
        else:
            lo, hi = (a, b) if a < b else (b, a)
            M[s_idx[(lo, hi)], c] += 1            # symmetric part: +s_{lo,hi}
            M[nsym + w_idx[(lo, hi)], c] += (1 if a < b else -1)  # +-w_{lo,hi}
    return M, nsym, nwed


# --------------------------------------------------------------------------- #
#  Explicit mod-p linear algebra  (finite fields, no float)                   #
# --------------------------------------------------------------------------- #

def mat_mod(M, p):
    """sympy Matrix -> list-of-lists of ints reduced mod p."""
    return [[int(M[r, c]) % p for c in range(M.cols)] for r in range(M.rows)]


def gf_rank(rows, p):
    """Rank over GF(p) by explicit Gaussian elimination on a copy of `rows`."""
    A = [row[:] for row in rows]
    if not A:
        return 0
    R, C = len(A), len(A[0])
    rank = 0
    col = 0
    for col in range(C):
        piv = None
        for r in range(rank, R):
            if A[r][col] % p != 0:
                piv = r
                break
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        inv = pow(A[rank][col], p - 2, p)
        A[rank] = [(x * inv) % p for x in A[rank]]
        for r in range(R):
            if r != rank and A[r][col] % p != 0:
                f = A[r][col]
                A[r] = [(A[r][c] - f * A[rank][c]) % p for c in range(C)]
        rank += 1
        if rank == R:
            break
    return rank


def gf_nullspace(rows, p):
    """Basis of the right null space {x : A x = 0 mod p} as list of int vectors."""
    A = [row[:] for row in rows]
    if not A:
        return []
    R, C = len(A), len(A[0])
    # RREF
    pivots = []
    r = 0
    for col in range(C):
        piv = None
        for rr in range(r, R):
            if A[rr][col] % p != 0:
                piv = rr
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][col], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for rr in range(R):
            if rr != r and A[rr][col] % p != 0:
                f = A[rr][col]
                A[rr] = [(A[rr][c] - f * A[r][c]) % p for c in range(C)]
        pivots.append(col)
        r += 1
        if r == R:
            break
    pivot_set = set(pivots)
    free = [c for c in range(C) if c not in pivot_set]
    basis = []
    for fcol in free:
        vec = [0] * C
        vec[fcol] = 1
        for ri, pcol in enumerate(pivots):
            vec[pcol] = (-A[ri][fcol]) % p
        basis.append(vec)
    return basis


def in_span_mod(vectors, target, p):
    """Is `target` in the GF(p)-span of `vectors`?  (rank test)."""
    base_rank = gf_rank(vectors, p)
    aug_rank = gf_rank(vectors + [target], p)
    return base_rank == aug_rank


# --------------------------------------------------------------------------- #
#  Smith normal form helpers (exact, over ZZ)                                 #
# --------------------------------------------------------------------------- #

def invariant_factors(M):
    """Invariant factors of an integer matrix via sympy's exact SNF."""
    from sympy.matrices.normalforms import invariant_factors as _inv
    return list(_inv(sp.Matrix(M), domain=sp.ZZ))


def torsion_from_invariant_factors(facs):
    """Given invariant factors of a map A: Z^m -> Z^k, the torsion of coker is the
    multiset of factors > 1.  (Free rank handled separately by the caller.)"""
    return [int(f) for f in facs if int(f) not in (0, 1)]
