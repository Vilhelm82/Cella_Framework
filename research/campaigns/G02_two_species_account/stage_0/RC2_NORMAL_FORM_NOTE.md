# RC-2 — the gauge-normal form, re-proven (symbolic tier)

**Certificate:** `verification/recert_normal_form.py` — 27/27 identities, byte-stable
×2, stdout sha16 `b21992f35a46f850`. Symbolic over `Q(g)[H, b, c]` at n = 3, 4, 5.
Fresh derivation; no origin code or values used.

## Statements re-proven (per n ∈ {3,4,5}, as rational-function identities)

```
Regular locus: all g_i != 0.   G_g(a) = g a^T + a g^T.
a*(H)_i = H_ii/(2 g_i),  H_perp = H - G_g(a*),  O_ij = H_ij - g_i H_jj/(2g_j) - g_j H_ii/(2g_i)

NF1/NF2  H_perp is zero-diagonal with off-diagonals exactly O        (normal form)
NF3      a* is the unique diagonal-killing gauge (det = 2^n prod g_i)
NF4      O(H + G_g(b)) = O(H)                                        (gauge invariance)
NF5      O is linear in H
NF6      rank Im(G_g) = n  (diagonal-row minor = 2^n prod g_i)
NF7      dO/dH on off-diagonal slots = identity  =>  rank O = n(n-1)/2
NF8      Im(G_g) ∩ ZeroDiag = 0
```

**Consequences (the Stage-A substrate):**

```
ker O = Im(G_g)                        [NF4 gives ⊇; NF7 + dim count gives equality:
                                        dim Sym_n − n(n−1)/2 = n = dim Im(G_g)]
Sym_n = Im(G_g) ⊕ ZeroDiag             [NF1–NF3 construct; NF8 makes it direct]
Sym_n / Im(G_g) ≅ Q^{n(n-1)/2} via O   [complete same-g invariant at order 2]
```

## The general-n argument (why 3,4,5 is not a coincidence)

Each identity is degree-uniform in n and proven by the same three facts, valid for
every n: `diag(G_g(a))_i = 2 g_i a_i` (so the diagonal system is diag(2g_i), invertible
iff regular — NF1/NF3/NF6/NF8); `offdiag(G_g(a))_ij = g_i a_j + a_i g_j`, which the O
formula subtracts exactly (NF2/NF4 — the cancellation `g_i b_j + b_i g_j − g_i b_j −
g_j b_i = 0` is index-local, touching only positions i, j); and O's dependence on
off-diagonal entries is the identity map slot-by-slot (NF5/NF7). No step consults n
beyond indexing. The n = 3,4,5 certificates are instances of an argument with no
n-dependent case; the derivation-note proof is general-n, the machine certificates pin
it at three sizes.

## Scope, stated exactly

Regular locus only (`∏ g_i ≠ 0` — off it, typed refusal territory). Characteristic 0
(the construction divides by `2 g_i`; the char-2 boundary is real and out of scope
here). Order 2 (Hessian slot) with g exact — the defective-g case is precisely Stage B,
not covered by this certificate.

## What this unblocks

Stage A's direct-sum theorem now stands on in-repo certificates alone: RC-1 (transport,
fixtures + group-element witness) and RC-2 (splitting, symbolic). Remaining Stage 0
item: RC-3 (holonomy instance) — owed before clause (iii) of the conjecture cites it.
