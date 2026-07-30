#!/usr/bin/env python3
"""Stage 0 packaging: copy the frozen corpus into the campaign package and
write MANIFEST.csv with sha256 hashes, source paths, roles, dispositions.

Run from the repository root:
    python3 research/campaigns/ACTIVE_RECHART_CURVATURE_VALUATIONS/00_CAMPAIGN/package_corpus.py

Source copies are never edited in place; the package is the working copy.
Missing files are recorded with status=MISSING, never silently dropped.
"""
import csv
import hashlib
import os
import shutil
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
CAMP = os.path.join(REPO, "research", "campaigns", "ACTIVE_RECHART_CURVATURE_VALUATIONS")

# (source_path_rel_repo, dest_dir_rel_camp, role, canonical_status, disposition)
ENTRIES = [
    # ---- 5.1 canonical core -------------------------------------------------
    ("Papers_Library/01_completed_papers/dbp_role_channel_and_orbit_geometry/dbp_orbit_calculus.tex",
     "01_SOURCES_CORE/paper_I_active_rechart", "Paper I: active S3 recharting, orbit theorem, channel reduction", "canonical", "candidate for absorption"),
    ("Papers_Library/01_completed_papers/dbp_role_channel_and_orbit_geometry/dbp_orbit_calculus.pdf",
     "01_SOURCES_CORE/paper_I_active_rechart", "Paper I compiled render", "canonical", "candidate for absorption"),
    ("Papers_Library/02_theorems_and_lemmas/dbp_role_channel_and_orbit_geometry/theorem_8_1.tex",
     "01_SOURCES_CORE/paper_I_active_rechart", "Abstract invariant-preservation theorem, kappa dichotomy", "canonical", "retain as companion unless fully absorbed"),
    ("Papers_Library/02_theorems_and_lemmas/dbp_role_channel_and_orbit_geometry/theorem_8_1.pdf",
     "01_SOURCES_CORE/paper_I_active_rechart", "Theorem 8.1 compiled render", "canonical", "retain as companion"),
    ("Papers_Library/02_theorems_and_lemmas/cella_residue_and_coupling_theory/CCE_8_FINITE_TOWER_NATURALITY_THEOREM_v1.0.md",
     "01_SOURCES_CORE/finite_tower", "Exact naturality through every finite truncation level", "canonical", "foundational strengthening; not infinite convergence"),
    ("Papers_Library/01_completed_papers/local_curvature_and_black_hole_metrics/LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md",
     "01_SOURCES_CORE/paper_II_local_curvature", "Fullest proof spine for diagonal divisor curvature", "canonical", "candidate for absorption"),
    ("Papers_Library/01_completed_papers/local_curvature_and_black_hole_metrics/pfc_normal_forms.tex",
     "01_SOURCES_CORE/paper_II_local_curvature", "Released concise normal-form paper", "canonical", "retain as concise predecessor until theorem mapping"),
    ("Papers_Library/01_completed_papers/local_curvature_and_black_hole_metrics/pfc_normal_forms.pdf",
     "01_SOURCES_CORE/paper_II_local_curvature", "pfc compiled render", "canonical", "retain"),
    ("Papers_Library/02_theorems_and_lemmas/local_curvature_and_black_hole_metrics/LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md",
     "01_SOURCES_CORE/paper_II_local_curvature", "Strongest variable-transverse leading-coefficient theorem", "canonical", "absorb into weighted-jet section"),
    ("Papers_Library/05_expository_companions_and_research_maps/dbp_role_channel_and_orbit_geometry/DBP_Curvature_Role_Reduction.md",
     "01_SOURCES_CORE/paper_I_active_rechart", "Order-2 reduction, continuous gauge orbit, Gauss-Lovelock elevation", "independent companion", "retain until elevation material mapped"),
    ("Papers_Library/05_expository_companions_and_research_maps/dbp_role_channel_and_orbit_geometry/dbp_four_role_calc_log_v8.md",
     "01_SOURCES_CORE/paper_I_active_rechart", "All-n role-pair carrier scaffold (frontier evidence)", "frontier evidence", "not a sole proof source; extract formal lemmas"),
    ("Papers_Library/01_completed_papers/dbp_role_channel_and_orbit_geometry/role_channel_anisotropy.pdf",
     "02_PROOF_SUPPLEMENTS/gauge_reduction", "Higher-order channel targets, anisotropy definitions", "proof supplement", "audit against canonical source"),
    # ---- 5.2 load-bearing proof supplements ---------------------------------
    ("Papers_Library/02_theorems_and_lemmas/dbp_role_channel_and_orbit_geometry/Canonical_Invariant_Reduction_Theorem.md",
     "02_PROOF_SUPPLEMENTS/gauge_reduction", "Lorentzian single-edge corollary; exact reduction workings", "proof supplement", "transfer unique proof"),
    ("Papers_Library/02_theorems_and_lemmas/dbp_role_channel_and_orbit_geometry/Gauge_Channel_Transport_Law.md",
     "02_PROOF_SUPPLEMENTS/gauge_reduction", "Full Lorentzian pinning + gauge-transport derivation", "proof supplement", "transfer unique proof"),
    ("Papers_Library/03_proofs_derivations_and_audits/dbp_role_channel_and_orbit_geometry/GAUGE_NORMAL_FORM_PROOF.md",
     "02_PROOF_SUPPLEMENTS/gauge_reduction", "Unique gauge-normal-form quotient proof Sym3/Im(G_g)~=Q^3", "proof supplement", "transfer unique proof"),
    ("Papers_Library/02_theorems_and_lemmas/dbp_role_channel_and_orbit_geometry/Theorem_8_1_Curvature_Orbit_Correction.md",
     "02_PROOF_SUPPLEMENTS/curvature_orbit_correction", "Worked exact example, self-channel formulas, transverse quadratic", "proof supplement", "transfer unique proof"),
    ("Papers_Library/02_theorems_and_lemmas/local_curvature_and_black_hole_metrics/LEAD7_masscharge_zeros_theorem.md",
     "02_PROOF_SUPPLEMENTS/masscharge_support", "Six-numerator factorization + inner-branch counterexample", "proof supplement", "transfer unique proof"),
    ("Papers_Library/05_expository_companions_and_research_maps/dbp_role_channel_and_orbit_geometry/Three_Channel_KG_New_Math_Extension.md",
     "02_PROOF_SUPPLEMENTS/gauge_reduction", "Legacy gauge and channel formulas (audit target)", "proof supplement", "audit against canonical source"),
    # ---- 5.3 Kerr-Newman application package --------------------------------
    ("Papers_Library/01_completed_papers/local_curvature_and_black_hole_metrics/lead7_kn_n3_dbp_metric.tex",
     "03_APPLICATION_KERR_NEWMAN/paper", "Flagship physical realization", "application", "cite for examples only"),
    ("Papers_Library/01_completed_papers/local_curvature_and_black_hole_metrics/lead7_kn_n3_dbp_metric.pdf",
     "03_APPLICATION_KERR_NEWMAN/paper", "KN paper render", "application", "cite for examples only"),
    ("Papers_Library/01_completed_papers/local_curvature_and_black_hole_metrics/lead7_kn_n3_dbp_metric_v2.pdf",
     "03_APPLICATION_KERR_NEWMAN/paper", "KN paper render v2", "application", "cite for examples only"),
    ("Papers_Library/05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/LEAD7_retrodiction_n3.md",
     "03_APPLICATION_KERR_NEWMAN/reports", "Retrodiction and application dictionary", "application", "cite for examples only"),
    ("Papers_Library/04_drafts_and_incomplete_papers/dbp_role_channel_and_orbit_geometry/LEAD2_Role_Singularity_Valuation_Brief.md",
     "03_APPLICATION_KERR_NEWMAN/reports", "Earlier valuation framing and terminology map", "historical", "terminology map only"),
    ("Papers_Library/01_completed_papers/dbp_role_channel_and_orbit_geometry/gtd_vs_dbp.pdf",
     "03_APPLICATION_KERR_NEWMAN/reports", "Comparison example, external-facing motivation", "reference only", "not a foundational proof source"),
    ("Papers_Library/05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/Lext.txt",
     "03_APPLICATION_KERR_NEWMAN/exact_factor_dumps", "Exact factor dump used by extremal-sign proof", "computational supplement", "retain"),
    ("Papers_Library/05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/num_factor.txt",
     "03_APPLICATION_KERR_NEWMAN/exact_factor_dumps", "Exact numerator factor dump", "computational supplement", "retain"),
    ("Papers_Library/05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/P_coeff_A_q2.txt",
     "03_APPLICATION_KERR_NEWMAN/exact_factor_dumps", "Extremal-gate coefficient dump A(q^2)", "computational supplement", "retain"),
    ("Papers_Library/05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/P_coeff_B_q1.txt",
     "03_APPLICATION_KERR_NEWMAN/exact_factor_dumps", "Extremal-gate coefficient dump B(q)", "computational supplement", "retain"),
    ("Papers_Library/05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/P_coeff_C_q0.txt",
     "03_APPLICATION_KERR_NEWMAN/exact_factor_dumps", "Extremal-gate coefficient dump C(q^0)", "computational supplement", "retain"),
    ("Papers_Library/05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/positive_core_P.txt",
     "03_APPLICATION_KERR_NEWMAN/exact_factor_dumps", "Positivity core dump for extremal gate", "computational supplement", "retain"),
    # ---- 5.4 computational supplements: role/channel ------------------------
    ("research/verification/cv_e1_lame_formula.py",
     "04_VERIFICATION_LEGACY/role_rechart", "Lame formula verifier", "computational supplement", "retain"),
    ("research/verification/cv_e2_canonical_gauge.py",
     "04_VERIFICATION_LEGACY/role_rechart", "Canonical gauge verifier", "computational supplement", "retain"),
    ("research/verification/recert_gtd_dbp_n2.py",
     "04_VERIFICATION_LEGACY/role_rechart", "GTD/DBP n=2 recertification", "computational supplement", "retain"),
    ("research/verification/recert_holonomy.py",
     "04_VERIFICATION_LEGACY/role_rechart", "Holonomy recertification", "computational supplement", "retain"),
    ("research/verification/recert_role_channels.py",
     "04_VERIFICATION_LEGACY/role_rechart", "Role-channel recertification", "computational supplement", "retain"),
    ("Papers_Library/07_certificates_data_and_reproducibility/dbp_role_channel_and_orbit_geometry/theorem_8_1_proof.py",
     "04_VERIFICATION_LEGACY/role_rechart", "Theorem 8.1 proof script", "computational supplement", "retain"),
    ("engine/tests/gate_continuation_cce8.py",
     "04_VERIFICATION_LEGACY/role_rechart", "CCE-8 finite-tower gate verifier (referenced by canonical paper)", "computational supplement", "retain"),
    # ---- 5.4 computational supplements: weighted jet / normal forms ---------
    ("research/campaigns/CELLA_CONTINUATION_ENGINE/10_post8_universalization/verify_lead7_variable_transverse_weighted_jet.py",
     "04_VERIFICATION_LEGACY/weighted_jet", "Weighted-jet verifier", "computational supplement", "retain"),
    ("Papers_Library/07_certificates_data_and_reproducibility/local_curvature_and_black_hole_metrics/lead7_variable_transverse_weighted_jet.py",
     "04_VERIFICATION_LEGACY/weighted_jet", "Weighted-jet driver (audit flags broken shim path; fixed local runner in package)", "computational supplement", "fix package-local run path"),
    ("research/verification/pfc_test1_local_normal_forms.py",
     "04_VERIFICATION_LEGACY/local_curvature", "pfc local normal forms verifier", "computational supplement", "retain"),
    ("research/verification/pfc_test2_corner_valuation.py",
     "04_VERIFICATION_LEGACY/local_curvature", "pfc corner valuation verifier", "computational supplement", "retain"),
    ("research/verification/pfc_test3_vertex_rule.py",
     "04_VERIFICATION_LEGACY/local_curvature", "pfc vertex rule verifier", "computational supplement", "retain"),
    ("research/verification/lead7_test10_reflection_lemma.py",
     "04_VERIFICATION_LEGACY/local_curvature", "Reflection lemma -m(m+5)/B verifier", "computational supplement", "retain"),
    # ---- 5.4 computational supplements: Kerr-Newman --------------------------
    ("research/verification/lead7_test5_pole_orders_n3.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN pole orders", "computational supplement", "retain"),
    ("research/verification/lead7_test6_pole_coeffs_n3.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN pole coefficients", "computational supplement", "retain"),
    ("research/verification/lead7_test7_extremal_coeff_n3.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN extremal coefficient", "computational supplement", "retain"),
    ("research/verification/lead7_test8_extremal_gate.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN extremal gate", "computational supplement", "retain"),
    ("research/verification/lead7_test8_extremal_gate_graphnorm.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN extremal gate (graph norm)", "computational supplement", "retain"),
    ("research/verification/lead7_test8_extremal_gate_replacement.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN extremal gate (replacement)", "computational supplement", "retain"),
    ("research/verification/lead7_test9_corner.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN double-reflection corner", "computational supplement", "retain"),
    ("research/verification/lead7_test4_masscharge_zeros.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN mass-role zeros = role divisors", "computational supplement", "retain"),
    ("research/verification/lead7_test1_candD_n2.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN candidate D n=2", "computational supplement", "retain"),
    ("research/verification/lead7_test2_candD_n3.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN candidate D n=3", "computational supplement", "retain"),
    ("research/verification/lead7_test3_candF_n3.py",
     "04_VERIFICATION_LEGACY/kerr_newman", "KN candidate F n=3 (selection)", "computational supplement", "retain"),
    # ---- 5.4 optional all-n / characteristic scaffold (Campaign H sources) ---
    ("Papers_Library/05_expository_companions_and_research_maps/dbp_role_channel_and_orbit_geometry/CHAR2_BOUNDARY_REPORT.md",
     "09_HISTORICAL_REFERENCE", "Campaign H char-2 boundary report", "frontier evidence", "package only if load-bearing"),
    ("Papers_Library/05_expository_companions_and_research_maps/dbp_role_channel_and_orbit_geometry/RAW_CHART_ROLECHSPEC_REPORT.md",
     "09_HISTORICAL_REFERENCE", "Campaign H raw chart RoleChSpec report", "frontier evidence", "package only if load-bearing"),
    ("Papers_Library/05_expository_companions_and_research_maps/dbp_role_channel_and_orbit_geometry/SYMBOLIC_ROLECHSPEC_FORMULAS.md",
     "09_HISTORICAL_REFERENCE", "Campaign H symbolic RoleChSpec formulas", "frontier evidence", "package only if load-bearing"),
    ("Papers_Library/05_expository_companions_and_research_maps/dbp_role_channel_and_orbit_geometry/INJECTIVITY_IDEAL_REPORT.md",
     "09_HISTORICAL_REFERENCE", "Campaign H injectivity ideal report", "frontier evidence", "package only if load-bearing"),
    ("Papers_Library/05_expository_companions_and_research_maps/dbp_role_channel_and_orbit_geometry/EXCEPTIONAL_LOCUS_REPORT.md",
     "09_HISTORICAL_REFERENCE", "Campaign H exceptional locus report", "frontier evidence", "package only if load-bearing"),
    # ---- 5.5 audit and architecture controls ---------------------------------
    ("research/campaigns/Succession_Map/DBP_PAPER_SUCCESSION_AND_REDUNDANCY_MAP_v1.0.md",
     "00_CAMPAIGN", "Disposition authority", "governance", "authoritative"),
    ("research/paper/Theorems/DBP/DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md",
     "00_CAMPAIGN", "Architecture control (spine must not become cited proof source)", "governance", "authoritative"),
    ("research/campaigns/Succession_Map/CODEX_HANDOFF_DBP_PAPER_SUCCESSION_AND_REDUNDANCY_AUDIT_v1.0.md",
     "00_CAMPAIGN", "Audit handoff", "governance", "authoritative"),
    # ---- 5.6 reference-only / historical --------------------------------------
    ("Papers_Library/05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt",
     "09_HISTORICAL_REFERENCE", "Historical roadmap; no unique mathematics after completed spine", "historical", "provenance only"),
    ("Papers_Library/03_proofs_derivations_and_audits/local_curvature_and_black_hole_metrics/LOCAL_CURVATURE_CALCULUS_COMPANION.md",
     "09_HISTORICAL_REFERENCE", "Companion; only dual-constant block merges elsewhere", "historical", "provenance only"),
    # ---- referenced but ABSENT from the repository (record, do not drop) ------
    ("MISSING:dbp_curvature_reduction_harness.py", "04_VERIFICATION_LEGACY/role_rechart",
     "Named in plan 5.4; not present anywhere in repository", "computational supplement", "MISSING - open obligation"),
    ("MISSING:char2_generalization.py", "04_VERIFICATION_LEGACY/role_rechart",
     "Named in plan 5.4 (all-n scaffold); not present in repository", "computational supplement", "MISSING - open obligation"),
    ("MISSING:verify_campaignH_parity.py", "04_VERIFICATION_LEGACY/role_rechart",
     "Named in plan 5.4 (all-n scaffold); not present in repository", "computational supplement", "MISSING - open obligation"),
    ("MISSING:verify_against_paper.py", "04_VERIFICATION_LEGACY/role_rechart",
     "Named in plan 5.4 (all-n scaffold); not present in repository", "computational supplement", "MISSING - open obligation"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    rows = []
    n_copied = n_missing = 0
    for src_rel, dest_rel, role, status, disposition in ENTRIES:
        if src_rel.startswith("MISSING:"):
            rows.append({"original_path": src_rel[8:], "package_path": "", "sha256": "",
                         "canonical_status": status, "role": role, "disposition": disposition,
                         "present": "MISSING"})
            n_missing += 1
            continue
        src = os.path.join(REPO, src_rel)
        if not os.path.exists(src):
            rows.append({"original_path": src_rel, "package_path": "", "sha256": "",
                         "canonical_status": status, "role": role, "disposition": disposition,
                         "present": "MISSING"})
            n_missing += 1
            continue
        dest_dir = os.path.join(CAMP, dest_rel)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(src))
        shutil.copy2(src, dest)
        rows.append({"original_path": src_rel,
                     "package_path": os.path.relpath(dest, CAMP),
                     "sha256": sha256(src),
                     "canonical_status": status, "role": role, "disposition": disposition,
                     "present": "ok"})
        n_copied += 1
    out = os.path.join(CAMP, "00_CAMPAIGN", "MANIFEST.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["original_path", "package_path", "sha256",
                                           "canonical_status", "role", "disposition", "present"])
        w.writeheader()
        w.writerows(rows)
    print(f"copied={n_copied} missing={n_missing} manifest={out}")
    return 0 if n_missing == 4 else 1  # exactly the four known-absent scripts


if __name__ == "__main__":
    sys.exit(main())
