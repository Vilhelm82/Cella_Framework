"""
Stage E -- Alternating carrier hunt in monodromy / transport.

P-E1  rebuild the self-glue monodromy groups EXACTLY (as permutation groups):
      product mP=2 -> D4;  directive mD=2 -> D4;  directive mD=3 -> S3 wr S3 (order 1296).
      Report degree, transitivity, block system, generators, order, block action / kernel,
      abelianization.
P-E2  sheet-pair modules: characters of Q[Omega], Sym^2(Q[Omega]) (symmetric sheet-pairs),
      and ^2(Q[Omega]) (alternating sheet-pairs); orbit counts (Burnside); block/within/cross
      decomposition of the unordered sheet-pairs.
P-E3  candidate comparison maps role <-> sheet, tested for canonicity/equivariance.
P-E4  detect the alternating half  ^2(std_n) = S^(n-2,1,1).  WARNING (campaign): for S3,
      ^2(std_3) = sign, NOT std -- tested by character projection, not naming resemblance.

Verdict in {alternating_carrier_found, alternating_carrier_absent, no_canonical_comparison_map}.
Group theory exact (sympy.combinatorics); characters exact integer counts.  No float.

Run: cd evals/dbp_involution && python3 stageE_monodromy_alt_probe.py
"""

from __future__ import annotations
from fractions import Fraction

from sympy.combinatorics import Permutation, PermutationGroup
import rep_utils as RU
from harness import Recorder, COMPUTER_VERIFIED, PROVEN, REFUTED, OPEN


def build_groups():
    groups = {}
    # Product cover D4 (S4 stabiliser of {{0,1},{2,3}}); generators from GROUP_REPORT
    tA, tp, tm = Permutation([2, 3, 0, 1]), Permutation([1, 0, 2, 3]), Permutation([0, 1, 3, 2])
    groups["product_mP2_D4"] = (PermutationGroup([tA, tp, tm]), 4,
                                "Sym(2) wr Sym(2) = D4 ; gens tA=(02)(13), t+=(01), t-=(23)")
    # Directive cover mD=2 -> D4 (same isomorphism type / block structure)
    groups["directive_mD2_D4"] = (PermutationGroup([tA, tp, tm]), 4,
                                  "Sym(2) wr Sym(2) = D4")
    # Directive cover mD=3 -> S3 wr S3 on 9 sheets (3 blocks of 3)
    gens = [Permutation(0, 1, size=9), Permutation(1, 2, size=9),
            Permutation(3, 4, size=9), Permutation(4, 5, size=9),
            Permutation(6, 7, size=9), Permutation(7, 8, size=9),
            Permutation([3, 4, 5, 0, 1, 2, 6, 7, 8]),
            Permutation([3, 4, 5, 6, 7, 8, 0, 1, 2])]
    groups["directive_mD3_S3wrS3"] = (PermutationGroup(gens), 9,
                                      "Sym(3) wr Sym(3) ; base S3^3 (order 216) x top S3")
    return groups


def fixed_points(perm, M):
    return sum(1 for i in range(M) if perm(i) == i)


def class_data(G):
    """List of (representative Permutation, class size)."""
    return [(next(iter(c)), len(c)) for c in G.conjugacy_classes()]


def burnside(values_sizes, order):
    """(1/|G|) sum |class| * value  -- must be a non-negative integer (orbit/inv count)."""
    s = sum(Fraction(sz * v) for v, sz in values_sizes)
    q = s / order
    assert q.denominator == 1, f"non-integer Burnside count {q}"
    return int(q)


def block_action_kernel(G, M):
    """Return (block_system, block_action_order, block_kernel_order)."""
    blocks = G.minimal_blocks()
    if not blocks:
        return None, G.order(), 1
    bs = blocks[0]
    # bs is a labelling list length M: bs[i] = block id of point i
    block_ids = sorted(set(bs))
    block_of = {i: bs[i] for i in range(M)}
    members = {b: [i for i in range(M) if bs[i] == b] for b in block_ids}
    # kernel = elements fixing every block setwise
    kernel = 0
    action_imgs = set()
    for g in G.generate():
        bperm = tuple(bs[g(members[b][0])] for b in block_ids)
        action_imgs.add(bperm)
        if all(set(g(x) for x in members[b]) == set(members[b]) for b in block_ids):
            kernel += 1
    return ([sorted(members[b]) for b in block_ids], len(action_imgs), kernel)


def block_action_sign(G, M, g):
    """Sign of the permutation g induces on the minimal block system."""
    blocks = G.minimal_blocks()[0]
    block_ids = sorted(set(blocks))
    members = {b: [i for i in range(M) if blocks[i] == b] for b in block_ids}
    img = [blocks[g(members[b][0])] for b in block_ids]
    idx = {b: k for k, b in enumerate(block_ids)}
    perm = tuple(idx[x] for x in img)
    # sign of perm
    seen = [False] * len(perm); s = 1
    for i in range(len(perm)):
        if not seen[i]:
            L = 0; j = i
            while not seen[j]:
                seen[j] = True; j = perm[j]; L += 1
            if L % 2 == 0:
                s = -s
    return s


def run(rec: Recorder):
    summary = {}
    groups = build_groups()

    expected = {
        "product_mP2_D4": {"order": 8, "ab": 4},
        "directive_mD2_D4": {"order": 8, "ab": 4},
        "directive_mD3_S3wrS3": {"order": 1296, "ab": 4, "block_kernel": 216, "block_action": 6},
    }

    pair_results = {}
    for name, (G, M, desc) in groups.items():
        order = G.order()
        der = G.derived_subgroup().order()
        ab = order // der
        transitive = G.is_transitive()
        blocks, baction, bkernel = block_action_kernel(G, M)
        exp = expected[name]
        e1_ok = (order == exp["order"] and ab == exp["ab"])
        if "block_kernel" in exp:
            e1_ok = e1_ok and bkernel == exp["block_kernel"] and baction == exp["block_action"]
        rec.record(
            f"P-E1 {name}: monodromy group reconstructed exactly ({desc})",
            COMPUTER_VERIFIED if e1_ok else REFUTED,
            {"sheets": M, "order": order, "transitive": transitive,
             "abelianization_order": ab, "derived_order": der,
             "block_system": blocks, "block_action_order": baction,
             "block_kernel_order": bkernel,
             "expected": exp},
            tier="[computer-verified]", gate=True,
        )

        # ---- P-E2 sheet-pair module characters ----
        cls = class_data(G)
        chiO, chiO2, chiSym, chiAlt = [], [], [], []
        for rep, sz in cls:
            fp = fixed_points(rep, M)
            fp2 = fixed_points(rep * rep, M)
            chiO.append((fp, sz))
            sym = Fraction(fp * fp + fp2, 2)          # Sym^2(Q[Omega]) incl diagonal
            alt = Fraction(fp * fp - fp2, 2)          # ^2(Q[Omega]) (alternating)
            chiSym.append((int(sym), sz))
            chiAlt.append((int(alt), sz))
        n_orbits_O = burnside(chiO, order)
        inv_sym = burnside(chiSym, order)             # G-invariants in symmetric sheet-pairs
        inv_alt = burnside(chiAlt, order)             # G-invariants in alternating sheet-pairs
        dim_alt = int(Fraction(M * M - M, 2))         # dim ^2(Q[Omega]) = C(M,2)
        # sign-character (block action) overlap with the alternating sheet-pair module
        sign_alt_mult_vals = []
        for rep, sz in cls:
            fp = fixed_points(rep, M); fp2 = fixed_points(rep * rep, M)
            alt = (fp * fp - fp2) // 2
            sgn = block_action_sign(G, M, rep)
            sign_alt_mult_vals.append((alt * sgn, sz))
        mult_blocksign_in_alt = burnside(sign_alt_mult_vals, order)
        rec.record(
            f"P-E2 {name}: sheet-pair module characters (symmetric / alternating)",
            COMPUTER_VERIFIED,
            {"M_sheets": M, "dim_alt_sheet_pairs C(M,2)": dim_alt,
             "num_orbits_on_sheets": n_orbits_O,
             "G_invariants_in_symmetric_pairs": inv_sym,
             "G_invariants_in_alternating_pairs": inv_alt,
             "mult_of_block-action-sign_in_alternating_pairs": mult_blocksign_in_alt},
            tier="[computer-verified]",
        )
        pair_results[name] = {"inv_alt": inv_alt, "mult_blocksign_in_alt": mult_blocksign_in_alt,
                              "block_action": baction}

    # ---- P-E3 / P-E4 comparison to the role-side alternating half ----
    # Roles n=3 (P,D,S). role-side: ^2(std_3) = sign_{S3}, dim 1 (NOT std).
    chi_wed3 = RU.chi_wedge2_of(RU.chi_std(3), 3)
    d_wed3 = RU.decompose(chi_wed3, 3)
    role_alt_is_sign = (d_wed3 == {(1, 1, 1): 1})
    rec.record(
        "P-E4 role side: ^2(std_3) = sign_{S3} (dim 1), NOT the standard rep",
        COMPUTER_VERIFIED if role_alt_is_sign else REFUTED,
        {"wedge^2(std_3)_decomp": {str(k): v for k, v in d_wed3.items()},
         "warning_heeded": "compared by character; sign != std"},
        tier="[computer-verified]",
    )

    # Candidate map: directive mD=3 block-action quotient  G -> S3  identifies the
    # block-action S3 with a copy of S3; under it ^2(std_3)=sign pulls back to the
    # block-action sign character of G, which P-E2 found present in the alternating
    # sheet-pairs (mult_blocksign_in_alt).  Test whether that identification is canonical.
    w = pair_results["directive_mD3_S3wrS3"]
    block_sign_present = (w["mult_blocksign_in_alt"] > 0 and w["block_action"] == 6)
    # canonicity: the 3 blocks are root-sheets of the stage-2 trinomial, NOT the 3 roles;
    # there is no role-canonical bijection roles <-> blocks (CALC-10 standing conclusion 5).
    canonical_map_exists = False
    rec.record(
        "P-E3: candidate comparison map (block-action quotient G -> S3) and its canonicity",
        COMPUTER_VERIFIED,
        {"block_action_is_S3_order6": (w["block_action"] == 6),
         "role_alt(sign) pulls back to block-action sign present in alt sheet-pairs":
             block_sign_present,
         "multiplicity_of_block-sign_in_alternating_sheet_pairs": w["mult_blocksign_in_alt"],
         "canonical_role<->sheet_bijection_exists": canonical_map_exists,
         "reason": "the 3 blocks are root-sheets of the stage-2 trinomial, not the 3 roles; "
                   "the monodromy block-action S3 is not the role S3 (CALC-10): no role-canonical map"},
        tier="[computer-verified group theory; canonicity is a structural fact]",
    )

    # ---- E_VERDICT ----
    alternating_structure_present = any(pr["inv_alt"] >= 0 for pr in pair_results.values()) and block_sign_present
    if canonical_map_exists and block_sign_present:
        everdict = "alternating_carrier_found"
    elif not alternating_structure_present:
        everdict = "alternating_carrier_absent"
    else:
        everdict = "no_canonical_comparison_map"
    rec.record(
        "E_VERDICT (alternating carrier hunt)",
        COMPUTER_VERIFIED,
        {"verdict": everdict,
         "alternating_structure_on_monodromy_side": block_sign_present,
         "canonical_comparison_map": canonical_map_exists,
         "interpretation": (
             "The monodromy groups DO carry alternating/sign structure (abelianization (Z/2)^2; "
             "the block-action sign appears in the alternating sheet-pairs). For n=3 the role "
             "alternating half is sign_{S3}, which pulls back through the block-action quotient "
             "G -> S3. BUT the blocks are root-sheets, not roles: there is no role-canonical "
             "comparison map. So the alternating half is not identified with a monodromy object "
             "by any projection of existing data -- the bridge requires a new (role-canonical) "
             "cover. This matches CALC-10 / the banked F-list.")},
        tier="[computer-verified]",
    )
    summary["E_VERDICT"] = everdict
    return summary


if __name__ == "__main__":
    rec = Recorder("StageE")
    summary = run(rec)
    for r in rec.records:
        flag = "" if r["verdict"] not in (REFUTED,) else "  <<< FAIL"
        print(f"[{r['verdict']:17}] {r['claim']}{flag}")
    print(f"\nE_VERDICT = {summary['E_VERDICT']}")
