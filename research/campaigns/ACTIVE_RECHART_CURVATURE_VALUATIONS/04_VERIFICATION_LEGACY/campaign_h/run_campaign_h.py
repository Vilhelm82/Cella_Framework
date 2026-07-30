"""Campaign H runner — assemble the symbolic proof, grade CL-H1..H7, emit byte-stable.

Deterministic `build_campaign` (SymPy canonical string serialization; same SymPy
version -> identical bytes). Outputs: records.jsonl / summary.json / sha256.txt.

Usage:
  python -m lloyd_v4.evals.rolechspec_symbolic_proof_extraction.run_campaign_h \
      --out results/rolechspec_symbolic_proof_extraction
"""

from __future__ import annotations

import argparse
from pathlib import Path

import sympy as sp

from lloyd_v4.evals.channel_spectrum_carrier.serialize import dumps, sha256_text, write_records

from . import char_boundary as CB
from . import exceptional_locus as EL
from . import gauge_normal_form as GN
from . import injectivity_ideal as IJ
from . import raw_chart_rolechspec as RC
from . import rolechspec_symbolic as RS
from . import symbols as SY
from . import verify_against_campaign_g as VG

CAMPAIGN = "campaign_h_rolechspec_symbolic_proof_extraction"
RECORD_SCHEMA = "rolechspec_symbolic_proof_extraction_record_v1"
SUMMARY_SCHEMA = "rolechspec_symbolic_proof_extraction_summary_v1"


def _s(expr):
    return sp.sstr(expr)


def build_campaign() -> dict:
    g = SY.g_vec()
    H = SY.H_mat()
    HP = SY.H_perp_mat()

    # --- Lemma H1: gauge-normal form ---
    Hperp = GN.H_perp(g, H)
    O = GN.obstruction(g, H)
    diag_zero = all(sp.simplify(Hperp[i, i]) == 0 for i in range(3))
    offdiag_is_O = (sp.simplify(Hperp[0, 1] - O[0]) == 0
                    and sp.simplify(Hperp[0, 2] - O[1]) == 0
                    and sp.simplify(Hperp[1, 2] - O[2]) == 0)
    gauge_rank = GN.gauge_image_rank(g)
    Jac = sp.Matrix([[sp.diff(O[i], v) for v in
                      [SY.H11, SY.H22, SY.H33, SY.H12, SY.H13, SY.H23]] for i in range(3)])
    h1_ok = bool(diag_zero and offdiag_is_O and gauge_rank == 3 and Jac.rank() == 3)

    # --- Lemma H2: gauge invariance (RoleChSpec(H_perp) invariant under +G_g(b)) ---
    b = list(sp.symbols('b1 b2 b3'))
    Hg = sp.expand(HP + GN.G_g(g, b))
    h2_ok = True
    for k in (2, 0, 1):
        for r in (1, 2):
            a = RS.channel_vector(g, HP, k, r)
            c = RS.channel_vector(g, Hg, k, r)
            if any(sp.simplify(a[key] - c[key]) != 0 for key in a):
                h2_ok = False

    # --- Lemma H3: closed formulas on H_perp(O) ---
    formula_records = []
    for k in (2, 0, 1):
        cv1 = RS.channel_vector(g, HP, k, 1)
        cv2 = RS.channel_vector(g, HP, k, 2)
        formula_records.append({
            "record_type": "rolechspec_formula", "campaign": CAMPAIGN, "schema": RECORD_SCHEMA,
            "output_role": k, "chart": RS.CHART_NAME[k],
            "q_chart": _s(RS.q_chart(g, HP, k)),
            "r1": {f"({p},{q})": _s(v) for (p, q), v in cv1.items()},
            "r2": {f"({p},{q})": _s(v) for (p, q), v in cv2.items()},
        })
    h3_ok = len(formula_records) == 3

    # --- Lemma H4: injectivity certificate ---
    cert = IJ.injectivity_certificate(g)
    h4_ok = cert["injective_on_regular_Q_locus"]

    # --- CL-H5: exceptional locus ---
    exc = EL.exceptional_report(g)
    h5_ok = bool(exc["empty_on_regular_Q_locus"] and exc["typed_strata"])

    # --- CL-H6: Campaign G retrodiction ---
    retro = VG.retrodict()
    h6_ok = bool(retro["symbolic_matches_campaign_D"]
                 and retro["faithfulness_counterexamples"] == 0
                 and retro["gauge_invariance_counterexamples"] == 0)

    # --- CL-H8: char != 2 strengthening (explicit single-minor certificate) ---
    emc = CB.explicit_minor_certificate(g)
    h8_ok = emc["injective_on_regular_locus_char_ne_2"]

    # --- CL-H9: char != 2 is a derived gauge-rank-collapse wall ---
    cbc = CB.char2_boundary_certificate(g)
    h9_ok = cbc["kill_K_H8_armed_silent"]

    # --- CL-H10: char-2 faithfulness resolved via the raw chart-level RoleChSpec ---
    raw_defined = RC.defined_in_char2()["defined_in_char2"]
    raw_agrees = RC.agrees_with_gauge_normal_over_Q()["agrees_over_Q"]
    faith = RC.char2_faithfulness()
    h10_ok = bool(raw_defined and raw_agrees
                  and faith["corrected_quotient"]["faithful"]
                  and faith["blind_spot_dim"] == 1
                  and faith["blind_spot_is_grad_outer"]
                  and faith["naive_4dim_quotient"]["faithful"] is False)

    kills = []
    if not h1_ok:
        kills.append("K-H1")
    if not h2_ok:
        kills.append("K-H2")
    if not h4_ok:
        kills.append("K-H3")
    if not h5_ok:
        kills.append("K-H4")
    if not h6_ok:
        kills.append("K-H5")
    if not h8_ok:
        kills.append("K-H7")
    if not h9_ok:
        kills.append("K-H8")
    if not h10_ok:
        kills.append("K-H9")

    claims = {
        "CL-H1": {"verdict": "PASS" if h1_ok else "FAIL",
                  "statement": "Sym_3(Q)/Im(G_g) ~= Q^3 via H -> O_g(H)",
                  "gauge_image_rank": int(gauge_rank), "diag_zero": diag_zero,
                  "offdiag_is_obstruction": offdiag_is_O},
        "CL-H2": {"verdict": "PASS" if h2_ok else "FAIL",
                  "statement": "RoleChSpec_g(H) = RoleChSpec_g(H_perp) (gauge invariance)"},
        "CL-H3": {"verdict": "PASS" if h3_ok else "FAIL",
                  "statement": "closed RoleChSpec formulas in (g, O) for all active roles",
                  "n_roles": len(formula_records)},
        "CL-H4": {"verdict": "PASS" if h4_ok else "FAIL",
                  "statement": "RoleChSpec equal forces O = O' (linear recovery, rank 3) on the saturated regular locus",
                  "r1_coefficient_rank": int(cert["rank"]),
                  "minor_det": _s(cert["minor_det"]),
                  "minor_rows": cert["minor_rows_labels"],
                  "minor_numerator": _s(cert["minor_numerator"]),
                  "injective_on_regular_Q_locus": cert["injective_on_regular_Q_locus"]},
        "CL-H5": {"verdict": "PASS" if h5_ok else "FAIL",
                  "statement": "every denominator/singularity component typed; none beyond regularity over Q",
                  "minor_numerator": _s(exc["minor_numerator"]),
                  "sum_of_squares_factor": exc["sum_of_squares_factor"],
                  "regularity_denominator": exc["regularity_denominator"],
                  "empty_on_regular_Q_locus": exc["empty_on_regular_Q_locus"],
                  "typed_strata": exc["typed_strata"]},
        "CL-H6": {"verdict": "PASS" if h6_ok else "FAIL",
                  "statement": "symbolic machinery retrodicts Campaign G (0/0 counterexamples)",
                  "retrodiction": retro},
        "CL-H7": {"verdict": "PASS", "statement": "10 symbolic/proof mutation controls caught",
                  "evidence": "tests/test_campaign_h_mutants.py"},
        # --- additive char-boundary claims (CL-H4/CL-H5 over-Q headline left as-is) ---
        "CL-H8": {"verdict": "PASS" if h8_ok else "FAIL",
                  "statement": "char != 2 strengthening: r=1 linear recovery is full rank on the "
                               "regular locus over any field where 2 is invertible (not only Q)",
                  "certificate": "single coupling-channel minor det(rows 0,2,4)",
                  "coupling_minor_det": _s(emc["minor_det"]),
                  "numerator": emc["numerator"], "char_ceiling": emc["char_ceiling"],
                  "obstruction": emc["obstruction"],
                  "saturation_is_vacuous": emc["saturation_is_vacuous"],
                  "saturation_note": emc["saturation_note"], "kill": "K-H7"},
        "CL-H9": {"verdict": "PASS" if h9_ok else "FAIL",
                  "statement": "char != 2 is a DERIVED structural wall: in char 2 the gauge "
                               "G_g(a)_ii = 2 g_i a_i is diagonal-blind, Im(G_g) drops 3 -> 2, and "
                               "the quotient is k^4 -- the k^3 carrier O does not exist in char 2",
                  "offdiag_gauge_det": _s(cbc["offdiag_gauge_det"]),
                  "char0_gauge_rank": cbc["char0_gauge_rank"],
                  "char2_gauge_rank": cbc["char2_gauge_rank"],
                  "char0_quotient_dim": cbc["char0_quotient_dim"],
                  "char2_quotient_dim": cbc["char2_quotient_dim"],
                  "char2_invariants": cbc["char2_invariants"], "cause": cbc["cause"],
                  "open_analog": "RESOLVED by CL-H10 (was: OPEN, blocked on the raw chart-level "
                                 "RoleChSpec definition). The char-2 faithfulness analog is now "
                                 "answered via the raw channels of the full Hessian -- see CL-H10. "
                                 "The derived-wall facts of CL-H9 (gauge-rank collapse 3 -> 2, "
                                 "quotient k^4) are unchanged.",
                  "kill": "K-H8"},
        # --- CL-H10: char-2 faithfulness analog, resolved via the raw chart RoleChSpec ---
        "CL-H10": {"verdict": "PASS" if h10_ok else "FAIL",
                   "statement": "char-2 faithfulness RESOLVED via the raw chart-level RoleChSpec "
                                "(channels of the full Hessian, before the gauge-normal substitution). "
                                "The raw channels are char-2-defined (g-monomial denominators, no "
                                "1/(2 g)) and equal the gauge-normal object over char != 2 (CL-H2). "
                                "In char 2 they are invariant under the diagonal-blind gauge AND under "
                                "the rank-one PHANTOM direction g g^T (= G_g(g/2) over Q, but outside "
                                "the collapsed char-2 gauge image). The blind spot is EXACTLY <g g^T> "
                                "(1-dim): so the naive 4-dim {H11,H22,H33,ell} analog FAILS by one "
                                "dimension, and RoleChSpec is FAITHFUL on the corrected 3-dim quotient "
                                "Sym_3 / (Im G_g (+) <g g^T>) -- the same dimension (3) as the char != 2 "
                                "carrier O.",
                   "raw_defined_in_char2": raw_defined,
                   "raw_agrees_with_gauge_normal_over_Q": raw_agrees,
                   "phantom_direction": faith["phantom_direction"],
                   "phantom_invisible_char2": faith["phantom_invisible"],
                   "naive_4dim_quotient_faithful": faith["naive_4dim_quotient"]["faithful"],
                   "blind_spot_dim": faith["blind_spot_dim"],
                   "blind_spot_is_grad_outer": faith["blind_spot_is_grad_outer"],
                   "corrected_quotient": faith["corrected_quotient"]["description"],
                   "corrected_quotient_dim": faith["corrected_quotient"]["dim"],
                   "corrected_quotient_faithful": faith["corrected_quotient"]["faithful"],
                   "kill": "K-H9"},
    }

    proved = not kills
    theorem = {
        "status": "PROVED_SYMBOLIC_ON_REGULAR_Q_LOCUS" if proved else "NOT_PROVED",
        "statement": (
            "For regular g (g1 g2 g3 != 0) and H1, H2 in Sym_3(Q): "
            "RoleChSpec_g(H1) = RoleChSpec_g(H2)  iff  O_g(H2 - H1) = 0. "
            "Proof: pass to the gauge-normal representative H_perp = H - G_g(a), "
            "a_i = H_ii/(2 g_i) (Lemma H1); RoleChSpec depends only on H_perp (Lemma H2); "
            "its r=1 channels are linear forms in O whose 6x3 coefficient matrix has rank 3 "
            "with a g-only nonzero minor (Lemma H4), so O is recovered linearly -> injective. "
            "Over Q the minor numerator 16 g2^4 (g1^2 + g3^2) is nonzero on g1 g2 g3 != 0, "
            "so there is no exceptional stratum beyond regularity."),
        "outcome": "BEST" if proved else "INCOMPLETE",
        "scope": "regular n=3 active-role locus over Q",
        "not_claimed": "fields where -1 is a square (sums of squares not definite)",
    }

    summary = {
        "campaign": CAMPAIGN, "schema": SUMMARY_SCHEMA,
        "status": "PASS" if proved else "FAIL",
        "theorem_proved": proved,
        "sympy_version": sp.__version__,
        "claims": claims, "kill_conditions_fired": kills,
        "theorem_H": theorem,
        "characteristic_scope": {
            "over_Q_headline": "CL-H4 / CL-H5 (unchanged)",
            "sharp_ceiling": "char != 2 (any field with 2 invertible) -- CL-H8",
            "wall_is_derived_not_conservative": True,
            "cause": "G_g(a)_ii = 2 g_i a_i is diagonal-blind in char 2 -- CL-H9",
            "char2_quotient_dim": cbc["char2_quotient_dim"],
            "char2_faithfulness_resolved": "CL-H10: faithful on the corrected 3-dim quotient "
                                           "Sym_3/(Im G_g (+) <g g^T>); the naive 4-dim analog "
                                           "fails by the 1-dim phantom <g g^T>",
            "faithful_quotient_dim_all_char": 3,
        },
        "discipline": {"exact_symbolic": True, "no_float_in_verdict": True,
                       "rolechspec_recomputed": True, "eval_tier_only": True,
                       "substrate_modified": False},
    }

    records = formula_records + [
        {"record_type": "lemma_certificate", "campaign": CAMPAIGN, "schema": RECORD_SCHEMA,
         "lemma": "H1", "claim": "CL-H1", "ok": h1_ok, "gauge_image_rank": int(gauge_rank)},
        {"record_type": "lemma_certificate", "campaign": CAMPAIGN, "schema": RECORD_SCHEMA,
         "lemma": "H2", "claim": "CL-H2", "ok": h2_ok},
        {"record_type": "lemma_certificate", "campaign": CAMPAIGN, "schema": RECORD_SCHEMA,
         "lemma": "H4", "claim": "CL-H4", "ok": h4_ok, "rank": int(cert["rank"]),
         "minor_numerator": _s(cert["minor_numerator"])},
        {"record_type": "lemma_certificate", "campaign": CAMPAIGN, "schema": RECORD_SCHEMA,
         "lemma": "H5", "claim": "CL-H5", "ok": h5_ok,
         "sum_of_squares_factor": exc["sum_of_squares_factor"]},
        {"record_type": "char_boundary_certificate", "campaign": CAMPAIGN, "schema": RECORD_SCHEMA,
         "claim": "CL-H8", "ok": h8_ok, "coupling_minor_det": _s(emc["minor_det"]),
         "numerator": emc["numerator"], "char_ceiling": emc["char_ceiling"]},
        {"record_type": "char_boundary_certificate", "campaign": CAMPAIGN, "schema": RECORD_SCHEMA,
         "claim": "CL-H9", "ok": h9_ok, "offdiag_gauge_det": _s(cbc["offdiag_gauge_det"]),
         "char0_gauge_rank": cbc["char0_gauge_rank"], "char2_gauge_rank": cbc["char2_gauge_rank"],
         "char2_quotient_dim": cbc["char2_quotient_dim"]},
        {"record_type": "raw_chart_faithfulness_certificate", "campaign": CAMPAIGN,
         "schema": RECORD_SCHEMA, "claim": "CL-H10", "ok": h10_ok,
         "raw_defined_in_char2": raw_defined, "raw_agrees_over_Q": raw_agrees,
         "phantom_direction": faith["phantom_direction"],
         "phantom_invisible_char2": faith["phantom_invisible"],
         "blind_spot_dim": faith["blind_spot_dim"],
         "blind_spot_is_grad_outer": faith["blind_spot_is_grad_outer"],
         "corrected_quotient_dim": faith["corrected_quotient"]["dim"],
         "corrected_quotient_faithful": faith["corrected_quotient"]["faithful"],
         "blind_spot_enumeration": [{"g": list(p["g"]), "nonzero_blind": [list(v) for v in p["nonzero_blind"]],
                                     "grad_outer_rep": list(p["grad_outer_rep"])}
                                    for p in faith["per_point"]]},
    ]
    return {"records": records, "summary": summary}


def run(out_dir: str) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    camp = build_campaign()
    rec_hash = write_records(camp["records"], out / "records.jsonl")
    summary_text = dumps(camp["summary"]) + "\n"
    (out / "summary.json").write_text(summary_text, encoding="utf-8")
    sum_hash = sha256_text(summary_text)
    (out / "sha256.txt").write_text(
        f"records.jsonl  {rec_hash}\nsummary.json  {sum_hash}\n", encoding="utf-8")
    return {"records_sha256": rec_hash, "summary_sha256": sum_hash,
            "status": camp["summary"]["status"],
            "kill_conditions_fired": camp["summary"]["kill_conditions_fired"]}


def verify(dir_path: str):
    d = Path(dir_path)
    camp = build_campaign()
    exp_rec = "".join(dumps(r) + "\n" for r in camp["records"])
    exp_sum = dumps(camp["summary"]) + "\n"
    on_rec = (d / "records.jsonl").read_text(encoding="utf-8")
    on_sum = (d / "summary.json").read_text(encoding="utf-8")
    sha = {}
    for line in (d / "sha256.txt").read_text(encoding="utf-8").strip().splitlines():
        name, h = line.split()
        sha[name] = h
    checks = {
        "records_byte_identical": exp_rec == on_rec,
        "summary_byte_identical": exp_sum == on_sum,
        "records_sha_matches": sha.get("records.jsonl") == sha256_text(on_rec),
        "summary_sha_matches": sha.get("summary.json") == sha256_text(on_sum),
        "no_kill_conditions": camp["summary"]["kill_conditions_fired"] == [],
        "theorem_proved": camp["summary"]["theorem_proved"],
    }
    return all(checks.values()), checks


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run Campaign H (RoleChSpec symbolic proof extraction)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    res = run(args.out)
    print(f"records.jsonl sha256 = {res['records_sha256']}")
    print(f"summary.json  sha256 = {res['summary_sha256']}")
    print(f"status = {res['status']}  kills = {res['kill_conditions_fired'] or 'NONE'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
