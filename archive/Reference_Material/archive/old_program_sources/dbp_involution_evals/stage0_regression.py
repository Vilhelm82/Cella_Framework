"""
Stage 0 -- Regression gates.  Reproduce the banked facts before testing the thesis.

P0.1  all-n role-pair theorem:  rank L = C(n,2),  chi_Im(L) = role-pair character.
P0.2  loss law:  Im(L) = triv + std + S^(n-2,2),  dim loss = n(n-3)/2.
P0.3  faithfulness margin:  n=4 kernel V4 margin 0;  n>=5 kernel trivial margin 2(n-3).

Engine (dbp_carrier) characters are traces of explicit matrices; the referee
(rep_utils) computes the same via Murnaghan-Nakayama.  A claim PASSES only when the
two independent routes agree AND the elementary combinatorial formula agrees.

P0.1 / P0.3 are STOP gates: a genuine FAIL halts the whole campaign.

Run: cd evals/dbp_involution && python3 stage0_regression.py
"""

from __future__ import annotations
from math import comb

import rep_utils as RU
import dbp_carrier as E
from harness import Recorder, COMPUTER_VERIFIED, PROVEN, REFUTED


def n2cycles(mu):
    """number of 2-cycles in a cycle type."""
    return sum(1 for k in mu if k == 2)


def chi_pair_elementary(n):
    """Role-pair character by the ELEMENTARY count: C(fix,2) + #2cycles, from a
    class representative.  (Independent of any Sym^2 formula.)"""
    out = {}
    for mu, _ in RU.conjugacy_classes(n):
        g = RU.class_rep(mu, n)
        f = RU.fix(g)
        out[mu] = comb(f, 2) + n2cycles(mu)
    return out


def engine_chi_imL(n, Lmat):
    """Character of Im(L) computed by the ENGINE: chi_conj(Sym^2) - chi_ker, with
    ker = nullspace(L) and the conjugation action restricted to it."""
    ker_basis = Lmat.nullspace()              # exact rational basis of ker L
    from sympy import Matrix
    B = Matrix.hstack(*ker_basis) if ker_basis else None
    chi = {}
    for mu, _ in RU.conjugacy_classes(n):
        g = RU.class_rep(mu, n)
        A = E.conj_sym2(g, n)
        chi_dom = A.trace()
        chi_ker = E.trace_on_subspace(A, B) if B is not None else 0
        chi[mu] = int(chi_dom - chi_ker)
    return chi, (B.cols if B is not None else 0)


def run(rec: Recorder, n_lo_pair=3, n_hi_pair=8, n_lo_margin=4, n_hi_margin=12):
    summary = {"P0.1": [], "P0.2": [], "P0.3": []}

    # ---------------- P0.1  all-n role-pair theorem ----------------
    for n in range(n_lo_pair, n_hi_pair + 1):
        Lf = E.L_flag(n)
        Li = E.L_int(n)
        rank_f, rank_i = Lf.rank(), Li.rank()
        Cn2 = comb(n, 2)

        chi_eng, ker_dim = engine_chi_imL(n, Lf)            # engine route (flag L)
        chi_elem = chi_pair_elementary(n)                    # elementary route
        chi_ref = RU.chi_sym2_of(RU.chi_std(n), n)           # referee route (MN-backed)

        agree_elem = all(chi_eng[mu] == chi_elem[mu] for mu, _ in RU.conjugacy_classes(n))
        agree_ref = all(chi_eng[mu] == chi_ref[mu] for mu, _ in RU.conjugacy_classes(n))
        decomp = RU.decompose(chi_eng, n)                    # referee decomposition
        exp = {(n,): 1, (n - 1, 1): 1}
        if n >= 4:
            exp[(n - 2, 2)] = 1
        decomp_ok = (decomp == exp)

        ok = (rank_f == Cn2 and rank_i == Cn2 and agree_elem and agree_ref
              and decomp_ok and ker_dim == n)
        rec.record(
            f"P0.1 n={n}: rank L = C(n,2) and chi_Im(L) = role-pair character",
            COMPUTER_VERIFIED if ok else REFUTED,
            {
                "n": n, "rank_L_flag": int(rank_f), "rank_L_int": int(rank_i),
                "C(n,2)": Cn2, "ker_dim": int(ker_dim),
                "engine==elementary_chi_pair": agree_elem,
                "engine==referee_Sym2(std)_chi": agree_ref,
                "Im(L)_decomposition": {str(k): v for k, v in decomp.items()},
            },
            tier="[proven for all n; verified n=%d]" % n,
            gate=True,
        )
        summary["P0.1"].append({"n": n, "rank": int(rank_f), "C(n,2)": Cn2, "ok": ok,
                                 "decomp": {str(k): v for k, v in decomp.items()}})

    # ---------------- P0.2  loss law ----------------
    for n in range(n_lo_pair, n_hi_pair + 1):
        chi_eng, _ = engine_chi_imL(n, E.L_flag(n))
        decomp = RU.decompose(chi_eng, n)
        loss_present = (n >= 4)
        loss_dim = RU.specht_dim((n - 2, 2)) if n >= 4 else 0
        formula_dim = n * (n - 3) // 2
        has_loss = ((n - 2, 2) in decomp) if n >= 4 else ((n - 2, 2) not in decomp or True)
        # n=3: (1,2) is not a valid partition -> loss absent
        absent_at_3 = (n != 3) or all(p != (n - 2, 2) for p in decomp)
        dim_ok = (loss_dim == formula_dim)
        ok = dim_ok and (has_loss if n >= 4 else absent_at_3)
        rec.record(
            f"P0.2 n={n}: loss = S^(n-2,2), dim loss = n(n-3)/2 = {formula_dim}",
            COMPUTER_VERIFIED if ok else REFUTED,
            {"n": n, "loss_partition": None if n == 3 else list((n - 2, 2)),
             "loss_dim": loss_dim, "n(n-3)/2": formula_dim,
             "present_in_Im(L)": (n >= 4 and (n - 2, 2) in decomp),
             "absent_at_n3": (n == 3)},
        )
        summary["P0.2"].append({"n": n, "loss_dim": loss_dim, "n(n-3)/2": formula_dim, "ok": ok})

    # n=4 V4 corroboration: perm rep on the three {2+2} partitions = triv (+) S^(2,2)
    parts_2p2 = [frozenset([frozenset(a), frozenset(b)]) for (a, b) in
                 [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]]
    chi_2p2 = {}
    for mu, _ in RU.conjugacy_classes(4):
        g = RU.class_rep(mu, 4)
        def act(part):
            return frozenset(frozenset(g[x] for x in blk) for blk in part)
        chi_2p2[mu] = sum(1 for P in parts_2p2 if act(P) == P)
    decomp_2p2 = RU.decompose(chi_2p2, 4)
    v4_ok = (decomp_2p2 == {(4,): 1, (2, 2): 1})
    rec.record(
        "P0.2 n=4 V4 corroboration: perm rep on three 2+2 partitions = triv (+) S^(2,2)",
        COMPUTER_VERIFIED if v4_ok else REFUTED,
        {"character_on_classes": {str(k): chi_2p2[k] for k, _ in RU.conjugacy_classes(4)},
         "decomposition": {str(k): v for k, v in decomp_2p2.items()},
         "interpretation": "S^(2,2) is the standard rep of S4/V4 on the 3 partitions"},
    )

    # ---------------- P0.3  faithfulness margin ----------------
    for n in range(n_lo_margin, n_hi_margin + 1):
        # chi_shape = character of S^(n-2,2) via Murnaghan-Nakayama (referee)
        chi_shape = {mu: RU.specht_char((n - 2, 2), mu) for mu, _ in RU.conjugacy_classes(n)}
        dim = chi_shape[tuple([1] * n)]
        # kernel = classes acting as identity (chi == dim); margin via next-highest
        kernel_classes = [mu for mu, _ in RU.conjugacy_classes(n)
                          if mu != tuple([1] * n) and chi_shape[mu] == dim]
        kernel_order = 1 + sum(RU.class_size(mu, n) for mu in kernel_classes)
        nonident_max = max(chi_shape[mu] for mu, _ in RU.conjugacy_classes(n)
                           if mu != tuple([1] * n))
        margin = dim - nonident_max
        # least-faithful element a transposition for n>=7: chi_shape = (n-3)(n-4)/2
        transp = tuple([2] + [1] * (n - 2))
        chi_transp = chi_shape[transp]
        if n == 4:
            ok = (margin == 0 and kernel_order == 4 and set(kernel_classes) == {(2, 2)})
            expect = "kernel V4 (order 4), margin 0"
        else:
            ok = (margin == 2 * (n - 3) and kernel_order == 1)
            expect = f"kernel trivial, margin 2(n-3) = {2*(n-3)}"
        rec.record(
            f"P0.3 n={n}: faithfulness margin ({expect})",
            COMPUTER_VERIFIED if ok else REFUTED,
            {"n": n, "dim_S(n-2,2)": dim, "kernel_order": kernel_order,
             "kernel_classes": [list(k) for k in kernel_classes],
             "margin": margin, "2(n-3)": 2 * (n - 3),
             "chi_shape(transposition)": chi_transp, "(n-3)(n-4)/2": (n - 3) * (n - 4) // 2},
            tier="[proven rep-theory fact about S^(n-2,2)]",
            gate=True,
        )
        summary["P0.3"].append({"n": n, "margin": margin, "kernel_order": kernel_order, "ok": ok})

    return summary


if __name__ == "__main__":
    rec = Recorder("Stage0")
    summary = run(rec)
    for r in rec.records:
        flag = "" if r["verdict"] != REFUTED else "  <<< FAIL"
        print(f"[{r['verdict']:17}] {r['claim']}{flag}")
    print("\nGATE FAILED" if rec.failed_gate else "\nSTAGE 0: ALL GATES PASS")
    import json
    print(json.dumps(summary, indent=1))
