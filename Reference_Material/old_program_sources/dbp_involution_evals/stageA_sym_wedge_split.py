"""
Stage A -- Symmetric / alternating split, and the local carrier in the symmetric half.

P-A1  construct std_n: dim n-1, chi_std(sigma) = fix-1  (n=3..8).
P-A2  T_n = std (x) std, swap tau, projectors P_+=(1+tau)/2, P_-=(1-tau)/2;
      dims and characters of Sym^2 / wedge^2; decompositions
      Sym^2(std)=triv+std+S^(n-2,2), wedge^2(std)=S^(n-2,1,1);
      n=4: wedge^2(std_4) = S^(2,1,1) = std (x) sign.
P-A3  the local carrier lands in the symmetric half:  P_-(Im L) = 0, P_+(Im L) = Im L,
      proven two ways -- (i) character orthogonality <chi_Im(L), chi_wedge^2> = 0
      (assumption-free, Schur), and (ii) the explicit q(x)q embedding annihilated by P_-.

Run: cd evals/dbp_involution && python3 stageA_sym_wedge_split.py
"""

from __future__ import annotations
from math import comb
import sympy as sp

import rep_utils as RU
import dbp_carrier as E
from harness import Recorder, COMPUTER_VERIFIED, PROVEN, REFUTED, BRANCHED


def trace_proj_char(P, n):
    """Character g -> trace(P * rho(g)) on std (x) std, where rho = Kronecker std."""
    out = {}
    for mu, _ in RU.conjugacy_classes(n):
        g = RU.class_rep(mu, n)
        R = E.tensor_std_matrix(g, n)
        out[mu] = int((P * R).trace())
    return out


def run(rec: Recorder, n_lo=3, n_hi=8):
    summary = {"P-A1": [], "P-A2": [], "P-A3": []}

    # ---------------- P-A1  std_n ----------------
    for n in range(n_lo, n_hi + 1):
        ok_dim = (E.tensor_std_matrix(RU.class_rep((1,) * n, n), n).shape == ((n - 1) ** 2, (n - 1) ** 2))
        std_dim = RU.std_matrix(RU.class_rep((1,) * n, n), n).shape[0]
        char_ok = all(RU.std_matrix(RU.class_rep(mu, n), n).trace() == RU.fix(RU.class_rep(mu, n)) - 1
                      for mu, _ in RU.conjugacy_classes(n))
        integer_ok = all(x.is_integer for mu, _ in RU.conjugacy_classes(n)
                         for x in RU.std_matrix(RU.class_rep(mu, n), n))
        ok = (std_dim == n - 1 and char_ok and integer_ok)
        rec.record(
            f"P-A1 n={n}: std_n has dim n-1 and chi_std(sigma)=fix-1 (integer matrices)",
            COMPUTER_VERIFIED if ok else REFUTED,
            {"n": n, "dim_std": std_dim, "expected": n - 1,
             "chi_std==fix-1": char_ok, "integral": integer_ok},
        )
        summary["P-A1"].append({"n": n, "dim": std_dim, "ok": ok})

    # ---------------- P-A2  Sym^2 / wedge^2 split ----------------
    for n in range(n_lo, n_hi + 1):
        Pp, Pm = E.projectors(n)
        T = E.tau_matrix(n)
        I = sp.eye((n - 1) ** 2)
        # projector algebra (projector evidence)
        proj_ok = (Pp * Pp == Pp and Pm * Pm == Pm and Pp + Pm == I
                   and Pp * Pm == sp.zeros((n - 1) ** 2) and T * T == I)
        rkp, rkm = Pp.rank(), Pm.rank()
        dim_sym, dim_wed = n * (n - 1) // 2, (n - 1) * (n - 2) // 2
        rank_ok = (rkp == dim_sym and rkm == dim_wed)
        # characters via projector traces (engine)  vs  referee formulas
        chi_sym_eng = trace_proj_char(Pp, n)
        chi_wed_eng = trace_proj_char(Pm, n)
        chi_sym_ref = RU.chi_sym2_of(RU.chi_std(n), n)
        chi_wed_ref = RU.chi_wedge2_of(RU.chi_std(n), n)
        char_ok = (all(chi_sym_eng[k] == chi_sym_ref[k] for k, _ in RU.conjugacy_classes(n))
                   and all(chi_wed_eng[k] == chi_wed_ref[k] for k, _ in RU.conjugacy_classes(n)))
        d_sym = RU.decompose(chi_sym_eng, n)
        d_wed = RU.decompose(chi_wed_eng, n)
        exp_sym = {(n,): 1, (n - 1, 1): 1}
        if n >= 4:
            exp_sym[(n - 2, 2)] = 1
        exp_wed = {(n - 2, 1, 1): 1}
        decomp_ok = (d_sym == exp_sym and d_wed == exp_wed)
        ok = proj_ok and rank_ok and char_ok and decomp_ok
        rec.record(
            f"P-A2 n={n}: std(x)std = Sym^2 (+) wedge^2; "
            f"Sym^2=triv+std+S^(n-2,2), wedge^2=S^(n-2,1,1)",
            COMPUTER_VERIFIED if ok else REFUTED,
            {"n": n, "projector_algebra_ok": proj_ok,
             "rank_P+": int(rkp), "dim_Sym^2": dim_sym,
             "rank_P-": int(rkm), "dim_wedge^2": dim_wed,
             "engine_char==referee_char": char_ok,
             "Sym^2_decomp": {str(k): v for k, v in d_sym.items()},
             "wedge^2_decomp": {str(k): v for k, v in d_wed.items()}},
        )
        summary["P-A2"].append({"n": n, "Sym2": {str(k): v for k, v in d_sym.items()},
                                 "Wedge2": {str(k): v for k, v in d_wed.items()}, "ok": ok})

    # n=4 special: wedge^2(std_4) = S^(2,1,1) = std (x) sign
    std4, sgn4 = RU.chi_std(4), RU.chi_sign(4)
    sxs = {mu: std4[mu] * sgn4[mu] for mu, _ in RU.conjugacy_classes(4)}
    chi_wed4 = RU.chi_wedge2_of(std4, 4)
    n4_ok = (RU.decompose(sxs, 4) == {(2, 1, 1): 1}
             and all(chi_wed4[k] == sxs[k] for k, _ in RU.conjugacy_classes(4)))
    rec.record(
        "P-A2 n=4: wedge^2(std_4) = S^(2,1,1) = std (x) sign",
        COMPUTER_VERIFIED if n4_ok else REFUTED,
        {"wedge^2(std_4)_decomp": {str(k): v for k, v in RU.decompose(chi_wed4, 4).items()},
         "std(x)sign_decomp": {str(k): v for k, v in RU.decompose(sxs, 4).items()},
         "characters_equal": all(chi_wed4[k] == sxs[k] for k, _ in RU.conjugacy_classes(4))},
        tier="[proven]",
    )

    # ---------------- P-A3  local carrier in the symmetric half ----------------
    for n in range(n_lo, n_hi + 1):
        Lf = E.L_flag(n)
        # (i) assumption-free Schur/character test on the ABSTRACT module Im(L)
        ker = Lf.nullspace()
        from sympy import Matrix
        B = Matrix.hstack(*ker) if ker else None
        chi_imL = {}
        for mu, _ in RU.conjugacy_classes(n):
            g = RU.class_rep(mu, n)
            A = E.conj_sym2(g, n)
            chi_imL[mu] = int(A.trace() - (E.trace_on_subspace(A, B) if B is not None else 0))
        chi_wed = RU.chi_wedge2_of(RU.chi_std(n), n)
        chi_sym = RU.chi_sym2_of(RU.chi_std(n), n)
        ip_wed = RU.inner_product(chi_imL, chi_wed, n)            # multiplicity of wedge^2 in Im(L)
        ip_sym = RU.inner_product(chi_imL, chi_sym, n)
        norm_imL = RU.inner_product(chi_imL, chi_imL, n)
        schur_ok = (ip_wed == 0 and ip_sym == norm_imL)          # zero alternating content

        # (ii) explicit q(x)q embedding annihilated by P_-
        Phi = E.carrier_into_tensor(n)                            # Sym^2(R^n) -> std(x)std
        Pp, Pm = E.projectors(n)
        gaugeM = E.gauge_matrix(n)
        gauge_to_zero = (Phi * gaugeM == sp.zeros((n - 1) ** 2, n))   # gauge -> 0
        rank_phi = Phi.rank()
        Pm_kills = (Pm * Phi == sp.zeros((n - 1) ** 2, n * (n + 1) // 2))
        Pp_fixes = (Pp * Phi == Phi)
        explicit_ok = (gauge_to_zero and rank_phi == comb(n, 2) and Pm_kills and Pp_fixes)

        ok = schur_ok and explicit_ok
        verdict = COMPUTER_VERIFIED if ok else BRANCHED
        rec.record(
            f"P-A3 n={n}: P_-(Im L)=0 and P_+(Im L)=Im L (carrier is the symmetric half)",
            verdict,
            {"n": n,
             "mult_wedge^2_in_Im(L)": int(ip_wed),
             "mult_Sym^2_in_Im(L)==norm": (ip_sym == norm_imL),
             "Im(L)_norm(#constituents)": int(norm_imL),
             "explicit_qq_gauge->0": gauge_to_zero,
             "explicit_rank==C(n,2)": (rank_phi == comb(n, 2)),
             "P_-_kills_carrier": Pm_kills, "P_+_fixes_carrier": Pp_fixes},
            tier="[proven via Schur + explicit projector]",
        )
        summary["P-A3"].append({"n": n, "mult_wedge2": int(ip_wed), "ok": ok})

    return summary


if __name__ == "__main__":
    rec = Recorder("StageA")
    summary = run(rec)
    for r in rec.records:
        flag = "" if r["verdict"] not in (REFUTED, BRANCHED) else f"  <<< {r['verdict']}"
        print(f"[{r['verdict']:17}] {r['claim']}{flag}")
    branched = any(r["verdict"] in (REFUTED, BRANCHED) for r in rec.records)
    print("\nSTAGE A: BRANCH/FAIL PRESENT" if branched else "\nSTAGE A: ALL PASS (carrier = symmetric half)")
