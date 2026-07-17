"""c001 `three_channel_kg` — STAGE D prereg freezer (covenant step 1).

Build tool (NOT the battery). Assembles the FROZEN `prereg.json` for STAGE D
(frame honesty, CL-c7 PARTIAL by design) and writes `prereg_sha256.pin`. Run
ONCE to freeze, BEFORE any battery code exists.

It:
  * embeds the probe source VERBATIM (read byte-for-byte from the stable main
    bench path; its sha256 is re-verified here and pinned in `organ`/`depends_on`);
  * pins the manifest + every bench file executed by the battery (Path A probe,
    Path B referee_total, Path B' referee_channel, Path C oracle, fixtures,
    schema) in `depends_on`, computing each sha256 from the stable main path;
  * pins the frozen authority objects (SCHEMA.md, FIXTURES.md, CLAIM_LEDGER.md,
    freeze_pins_sha256.json) in `frozen_authority_pins`;
  * encodes the STAGE-D `predictions`, `expectations`, `status_move_rules`
    (R2/R3 dispositions; K7 refute; K-soft non-refuting FLAG; CL-c7 -> PARTIAL,
    NOT DEMONSTRATED; CL-c3c-ii OPEN), `referee`, `grader_clauses`, `organ`.

Deterministic: `json.dumps(..., sort_keys=True, indent=2)`; the pin is the
sha256 of the exact bytes written. Exact ℚ only; no tolerance; eval-tier only.
"""

from __future__ import annotations

import hashlib
import json
import os

# Stage dir is THIS file's directory (relocatable); the bench is referenced at
# the STABLE main absolute path (the worktree is bench-less by design — the
# frozen bench is committed on main and imported READ-ONLY by exact path).
STAGE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.dirname(STAGE)
BENCH_DIR = "/home/wlloyd/Lloyd_Engine_V4/src/lloyd_v4/evals/three_channel_kg"
MANIFEST = os.path.join(RESULTS, "manifest_v1.json")


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# --- pins: bench (depends_on) + frozen authority objects --------------------
PROBE_PATH = os.path.join(BENCH_DIR, "probe.py")
PROBE_SRC = read_text(PROBE_PATH)
PROBE_SHA = sha256_file(PROBE_PATH)

DEPENDS_ON = {
    "results/three_channel_kg/manifest_v1.json": sha256_file(MANIFEST),
    "src/lloyd_v4/evals/three_channel_kg/probe.py": sha256_file(PROBE_PATH),
    "src/lloyd_v4/evals/three_channel_kg/referee_total.py":
        sha256_file(os.path.join(BENCH_DIR, "referee_total.py")),
    "src/lloyd_v4/evals/three_channel_kg/referee_channel.py":
        sha256_file(os.path.join(BENCH_DIR, "referee_channel.py")),
    "src/lloyd_v4/evals/three_channel_kg/oracle.py":
        sha256_file(os.path.join(BENCH_DIR, "oracle.py")),
    "src/lloyd_v4/evals/three_channel_kg/fixtures.py":
        sha256_file(os.path.join(BENCH_DIR, "fixtures.py")),
    "src/lloyd_v4/evals/three_channel_kg/schema.py":
        sha256_file(os.path.join(BENCH_DIR, "schema.py")),
}

FROZEN_AUTHORITY_PINS = {
    "results/three_channel_kg/SCHEMA.md":
        sha256_file(os.path.join(RESULTS, "SCHEMA.md")),
    "results/three_channel_kg/FIXTURES.md":
        sha256_file(os.path.join(RESULTS, "FIXTURES.md")),
    "results/three_channel_kg/CLAIM_LEDGER.md":
        sha256_file(os.path.join(RESULTS, "CLAIM_LEDGER.md")),
    "results/three_channel_kg/freeze_pins_sha256.json":
        sha256_file(os.path.join(RESULTS, "freeze_pins_sha256.json")),
}


# --- GRADER_CLAUSES: governing clauses embedded VERBATIM ---------------------
# K7 + K-soft transcribed VERBATIM from results/three_channel_kg/CLAIM_LEDGER.md.
# R2/R3 transcribed VERBATIM from CLAIM_LEDGER.md "Reserved-ruling dispositions".
# Closure / semantics / precondition / type-gate clauses transcribed VERBATIM
# from manifest_v1.json semantics_pinned + SCHEMA.md (the same canonical text
# Stage A pins), restricted to what frame honesty grades against.
GRADER_CLAUSES = {
    # the two armed kills for STAGE D (verbatim, CLAIM_LEDGER.md).
    "K7_frame_undeclared":
        "a legitimate rechart reported as a curvature error, or `σ₂` "
        "not held invariant under F12. *(CL-c7)*",
    "K_soft_completeness":
        "two surfaces, identical `{σ_r}`+orientation, not gauge+permutation "
        "related. *(L1; CL-c3c-ii / CL-c7 completeness)*",
    # the CL-c7 ledger statement (verbatim, CLAIM_LEDGER.md row).
    "CL_c7_statement":
        "frame honesty — sum intrinsic; channels frame-relative, `S₃`+signs "
        "invariants (n=3); completeness OPEN",
    # CL-c3c-ii ledger statement (verbatim) + its OPEN annotation.
    "CL_c3c_ii_statement":
        "no **invariant** scalar (factoring through `Σ`) recovers the channel "
        "representative",
    "CL_c3c_ii_open":
        "NOT_YET_PROBED (OPEN — blocked on `{σ_r}`-completeness / L1)",
    # reserved-ruling dispositions R2 / R3 (verbatim, CLAIM_LEDGER.md).
    "R2_supplied_frame":
        "disposition: the channels are frame-relative in the supplied DBP "
        "frame; only the sum `K_G` is intrinsic",
    "R3_F12_pin":
        "CLOSED. `R∈SO(3)`, rotated jet, and tuples pinned in `FIXTURES.md` "
        "(exact ℚ).",
    # closure / semantics (verbatim from manifest semantics_pinned, the same
    # canonical strings Stage A pins) — the invariance grading rests on these.
    "semantics_K_G": "kappa_c + kappa_s + kappa_int (exact in Q)",
    "semantics_total_referee": "K_G == -det(H_b)/q^2 (Path B, sqrt-q-free)",
    "semantics_channel_referee":
        "channels == split-shape-operator det2 channels (Path B', disjoint source)",
    # preconditions (verbatim, SCHEMA.md / manifest stage0_controls).
    "precondition_P_self_cert":
        "the oracle (Path C) must be external to A/B/B', or the run is void.",
    "precondition_P_frame":
        "every channel fixture must carry its frame annotation, or it is rejected.",
    # type gate (verbatim, SCHEMA.md) — F12 outputs must stay exact Q.
    "type_gate_sqrt_q_leak":
        "a total/channel referee returning a radical/float instead of Fraction "
        "-> hard fail (K8).",
}


# --- expectations: the ground-truth values graded against (exact ℚ) ----------
# Base = keystone F8 in the declared DBP frame. F12a / F12b transcribed VERBATIM
# from FIXTURES.md §F12 (R3 pinned).
EXPECTATIONS = {
    "base_F8_declared_frame": {
        "K_G": "-3/49",
        "channels": ["-1/49", "1/49", "-3/49"],
        "frame": "declared DBP frame",
        "note": "keystone F8 base jet g=(3,1,2), H=[[2,1,0],[1,0,0],[0,0,2]], q=14",
    },
    "F12a_generic_rotation": {
        "rechart": "R=(1/5)[[3,-4,0],[4,3,0],[0,0,5]] in SO(3) (conv. x=Ry; g'=R^T g, H'=R^T H R)",
        "g_prime": ["13/5", "-9/5", "2"],
        "q_prime": "14",
        "K_G": "-3/49",
        "channels": ["-961/30625", "2713/30625", "-3627/30625"],
        "channels_move": True,
        "K_G_invariant": True,
        "frame_required": True,
    },
    "F12b_signed_permutation": {
        "rechart": "signed permutation swap axes 1<->2; P=[[0,1,0],[1,0,0],[0,0,1]]",
        "q_prime": "14",
        "K_G": "-3/49",
        "channels": ["-1/49", "1/49", "-3/49"],
        "channels_fixed": True,
        "K_G_invariant": True,
        "frame_required": True,
    },
    "K7_disposition": {
        "fires_when": "a legitimate rechart reported as a curvature error, OR sigma_2(=K_G) not held invariant under F12",
        "must_not_fire": True,
        "F12a_is_legitimate_rechart": "R^T R == I and det R == +1 (genuine SO(3) frame change)",
        "F12b_is_legitimate_rechart": "P^T P == I (signed permutation, |det P| == 1)",
    },
    "completeness_disposition": {
        "CL_c3c_ii": "OPEN (blocked on {sigma_r}-completeness / L1); NOT closed by Stage D",
        "K_soft": "non-refuting FLAG; no in-scope refuting witness manufactured; does NOT fail a prediction",
        "CL_c7_move": "PARTIAL (provable core graded; completeness left OPEN; NOT DEMONSTRATED)",
    },
}


# --- predictions: falsifiable, units declared --------------------------------
PREDICTIONS = [
    {
        "id": "P1_F12a_channels_move",
        "claims": ["CL-c7"],
        "kills_relevant": ["K7"],
        "statement": (
            "Frame-relativity core (R2): under F12a (generic rotation R in SO(3), "
            "conv. x=Ry), the channel triple MOVES off the declared-frame triple. "
            "Exact Q: (kappa_c,kappa_s,kappa_int)_F12a == (-961/30625, 2713/30625, "
            "-3627/30625) and this != the base triple (-1/49, 1/49, -3/49). The "
            "moved triple agrees across Path A (probe), Path B' (split shape "
            "operator) and Path C (oracle)."),
        "expected": "channels_F12a == (-961/30625,2713/30625,-3627/30625) != base (-1/49,1/49,-3/49) on A/B'/C",
        "units": "exact Q (Fraction) per channel; boolean moved!=base; boolean A==B'==C",
    },
    {
        "id": "P2_F12a_KG_invariant",
        "claims": ["CL-c7"],
        "kills_relevant": ["K7"],
        "statement": (
            "Intrinsic-sum core: under F12a, sigma_2 = K_G is INVARIANT. Exact Q: "
            "K_G_F12a == -3/49 == K_G_base, on Path A total, Path B total "
            "(-det(H_b)/q^2), Path B' sum, and Path C. (K7 fires if sigma_2 is not "
            "held invariant under F12 — here it MUST remain invariant.)"),
        "expected": "K_G_F12a == -3/49 == K_G_base on A/B/B'/C; q'_F12a == 14",
        "units": "exact Q (Fraction); boolean invariance across paths",
    },
    {
        "id": "P3_F12b_channels_fixed",
        "claims": ["CL-c7"],
        "kills_relevant": ["K7"],
        "statement": (
            "S3 x {+/-} invariance core (n=3): under F12b (signed permutation P, "
            "swap axes 1<->2), the channel triple is FIXED at the declared-frame "
            "triple. Exact Q: (kappa_c,kappa_s,kappa_int)_F12b == (-1/49, 1/49, "
            "-3/49) == base, on Path A, Path B' and Path C. The signed permutation "
            "is a symmetry of the monomial channel decomposition (the S3 x {+/-} "
            "stabilizer at n=3), so the channels do not move under it."),
        "expected": "channels_F12b == (-1/49,1/49,-3/49) == base on A/B'/C",
        "units": "exact Q (Fraction) per channel; boolean fixed==base; boolean A==B'==C",
    },
    {
        "id": "P4_F12b_KG_invariant",
        "claims": ["CL-c7"],
        "kills_relevant": ["K7"],
        "statement": (
            "Under F12b, sigma_2 = K_G is INVARIANT. Exact Q: K_G_F12b == -3/49 "
            "== K_G_base, on Path A total, Path B total, Path B' sum, Path C; "
            "q'_F12b == 14. (K7 must NOT fire under the signed permutation.)"),
        "expected": "K_G_F12b == -3/49 == K_G_base on A/B/B'/C; q'_F12b == 14",
        "units": "exact Q (Fraction); boolean invariance across paths",
    },
    {
        "id": "P5_K7_not_fired",
        "claims": ["CL-c7"],
        "kills_relevant": ["K7"],
        "statement": (
            "K7 (frame-undeclared, refute) does NOT fire on either F12 rechart. "
            "Neither trigger is met: (a) the recharts are LEGITIMATE frame changes "
            "— F12a R with R^T R == I and det R == +1 (genuine SO(3)); F12b P a "
            "signed permutation with P^T P == I and |det P| == 1 — and the "
            "curvature K_G is preserved exactly (NOT reported as a curvature "
            "error); AND (b) sigma_2 (= K_G) is held invariant under BOTH F12a and "
            "F12b. So a stage that flagged either legitimate rechart as a curvature "
            "error, or let sigma_2 drift, would fire K7 — and neither happens."),
        "expected": "K7 not fired: recharts legitimate (orthogonal) AND K_G invariant under both F12a,F12b",
        "units": "boolean (rechart orthogonality) AND boolean (K_G invariance) per fixture",
    },
    {
        "id": "P6_frame_relativity_contrast_R2",
        "claims": ["CL-c7"],
        "kills_relevant": ["K7"],
        "statement": (
            "R2 disposition (channels frame-relative, only the sum intrinsic): the "
            "two recharts CONTRAST exactly as R2/CL-c7 predict. Under the generic "
            "rotation F12a the channel representative MOVES "
            "(channels_F12a != channels_base) while the invariant sum is FIXED "
            "(K_G_F12a == K_G_base); under the discrete signed permutation F12b the "
            "channels are FIXED (channels_F12b == channels_base) and the sum is "
            "again FIXED. So: a generic frame change moves the representative but "
            "not the invariant (frame-relativity); the S3 x {+/-} subgroup fixes "
            "the representative (n=3 invariance); the sum K_G is intrinsic under "
            "both. This is the provable PARTIAL core — nothing claims completeness."),
        "expected": "F12a: channels move & K_G fixed; F12b: channels fixed & K_G fixed (R2 contrast holds)",
        "units": "boolean per fixture (channels-move flag, K_G-fixed flag)",
    },
    {
        "id": "P7_completeness_OPEN_Ksoft_flag",
        "claims": ["CL-c7", "CL-c3c-ii"],
        "kills_relevant": ["K-soft"],
        "statement": (
            "PARTIAL-by-design honesty: CL-c3c-ii (no invariant scalar factoring "
            "through Sigma recovers the channel representative) is recorded OPEN — "
            "blocked on {sigma_r}-completeness / L1 — and is NOT closed by Stage D. "
            "K-soft (completeness) is a NON-REFUTING FLAG: no in-scope witness of "
            "two surfaces with identical {sigma_r}+orientation that are not "
            "gauge+permutation related is manufactured (manufacturing one would "
            "reach into closing CL-c3c-ii, which Stage D must not do), so the FLAG "
            "is raised as 'completeness unestablished' and does NOT refute and does "
            "NOT fail this prediction. This prediction PASSES iff the stage records "
            "CL-c3c-ii as OPEN, raises K-soft as a non-refuting flag, and proposes "
            "CL-c7 -> PARTIAL (NOT DEMONSTRATED). The exact-Q near-miss of K-soft "
            "(F12a and F8-base share sigma_2 = -3/49 and orientation but have "
            "different channel triples) is recorded as evidence that identical "
            "sigma_2 + different channels arises precisely under a frame change — "
            "the converse of the open K-soft question, not a closure of it."),
        "expected": "CL-c3c-ii OPEN recorded; K-soft non-refuting flag raised; CL-c7 move == PARTIAL (not DEMONSTRATED)",
        "units": "boolean (OPEN recorded) AND boolean (flag is non-refuting) AND (proposed move == PARTIAL)",
    },
    {
        "id": "P8_F12_preconditions",
        "claims": ["CL-c7"],
        "kills_relevant": [],
        "preconditions": ["P-self-cert", "P-frame"],
        "statement": (
            "Preconditions hold in F12 scope (run not void): P-frame — each F12 "
            "fixture (F12a, F12b) carries a non-empty frame annotation on BOTH the "
            "generated fixture and the Path C oracle (channels are frame-relative, "
            "so the frame is mandatory); P-self-cert — the Path C oracle does NOT "
            "import probe / referee_total / referee_channel / fixtures and they do "
            "not import oracle."),
        "expected": "F12a,F12b carry frame on fixture and oracle; oracle import-disjoint from A/B/B'",
        "units": "boolean (frame-present per F12 fixture) AND boolean (import-graph disjoint)",
    },
    {
        "id": "P9_F12_type_gate_sqrt_q",
        "claims": ["CL-c7"],
        "kills_relevant": ["K8"],
        "statement": (
            "Type gate in F12 scope (sqrt-q-leak): every value emitted for F12a and "
            "F12b on Path A (probe), Path B (total) and Path B' (channels) is an "
            "exact fractions.Fraction (no float, no radical); AND a float operand "
            "offered at the F12 probe door is REFUSED with a TypeError (never "
            "silently coerced). The rotation/permutation arithmetic stays in Q "
            "throughout — q enters only as q^2, never as sqrt(q)."),
        "expected": "all F12 emissions are Fraction on A/B/B'; float operand at door raises TypeError",
        "units": "type predicate (isinstance Fraction); boolean refusal-on-float",
    },
]


# --- status_move_rules: PASS-moves; kill on FAIL; CL-c7 -> PARTIAL ----------
STATUS_MOVE_RULES = {
    "CL-c7": {
        "ledger_statement": (
            "frame honesty — sum intrinsic; channels frame-relative, S3+signs "
            "invariants (n=3); completeness OPEN"),
        "partial_by_design": True,
        "universal_claim": False,
        "R2_disposition": (
            "channels frame-relative in the supplied DBP frame; only the sum K_G "
            "is intrinsic. Graded accordingly: F12a moves the channels (sum fixed); "
            "F12b (signed permutation) fixes the channels (S3 x {+/-} at n=3)."),
        "R3_disposition": (
            "F12 pin CLOSED — R in SO(3), rotated jet, and exact-Q tuples used "
            "verbatim from FIXTURES.md."),
        "on_pass": {
            "condition": (
                "P1 AND P2 AND P3 AND P4 AND P5 AND P6 AND P7 AND P8 AND P9 all "
                "PASS — the provable PARTIAL core: F12a channels MOVE while K_G is "
                "invariant (frame-relativity / R2), F12b channels FIXED and K_G "
                "invariant (S3 x {+/-} at n=3), K7 not fired, and completeness "
                "left OPEN (CL-c3c-ii) with K-soft a non-refuting flag."),
            "move_to": "PARTIAL",
            "explicitly_not": "DEMONSTRATED",
            "warrant_scope": (
                "PARTIAL by design: the intrinsic-sum / frame-relativity / "
                "S3 x {+/-}-invariance core is graded on the frozen F12 pin (R3, "
                "exact Q); completeness (whether {sigma_r}+orientation determines "
                "the gauge+permutation class — CL-c3c-ii / L1) is left OPEN and is "
                "NOT established here. Eval-tier; no substrate promotion; canonical "
                "only on Will's sign-off."),
        },
        "on_fail": {
            "default": "any FAIL -> HALT, preserve chain verbatim, route to Will; no move.",
            "if_K7_trigger": (
                "P2/P4 (sigma_2 not invariant under F12) or P5 (a legitimate "
                "rechart reported as a curvature error) FAIL -> K7 fires (refute) "
                "-> REFUTED candidate; HALT, route to Will."),
            "if_core_fails": (
                "P1/P3/P6 (frame-relativity / S3-invariance core) FAIL -> the "
                "PARTIAL core is broken -> HALT, route to Will; do NOT soften to a "
                "weaker warrant."),
        },
    },
    "CL-c3c-ii": {
        "ledger_statement": (
            "no invariant scalar (factoring through Sigma) recovers the channel "
            "representative"),
        "status": "OPEN",
        "disposition": (
            "OPEN — blocked on {sigma_r}-completeness / L1. Stage D records this "
            "OPEN and does NOT attempt to close it. No status move is proposed."),
        "no_move": True,
    },
    "kills": {
        "K7": {
            "claim": "CL-c7",
            "type": "refute",
            "fires_on": (
                "P5 FAIL (a legitimate rechart reported as a curvature error) OR "
                "P2/P4 FAIL (sigma_2 = K_G not held invariant under F12)."),
            "on_fire": "REFUTED candidate -> HALT, preserve chain, route to Will.",
        },
        "K-soft": {
            "claim": "CL-c3c-ii / CL-c7 completeness",
            "type": "flag (non-refuting)",
            "fires_on": (
                "two surfaces, identical {sigma_r}+orientation, not "
                "gauge+permutation related (L1)."),
            "on_fire": (
                "record as a FLAG only; does NOT refute and does NOT fail a "
                "prediction. In Stage-D scope no such in-scope witness is "
                "manufactured (manufacturing one would reach into closing "
                "CL-c3c-ii); the FLAG is raised as 'completeness unestablished'."),
            "non_refuting": True,
        },
    },
    "preconditions": {
        "P-frame": {"checked_by": "P8", "on_fail": "F12 fixture rejected; run VOID"},
        "P-self-cert": {"checked_by": "P8", "on_fail": "run VOID"},
    },
    "halt_rule": (
        "On ANY prediction FAIL: HALT. Preserve the chain verbatim. Do NOT fix, "
        "redesign, soften, or widen. Write what is held and route to Will. No "
        "status move is proposed for a claim whose gating predictions did not all "
        "PASS. CL-c7's move is PARTIAL (by design) and is NEVER DEMONSTRATED in "
        "this stage. CL-c3c-ii stays OPEN; K-soft is a non-refuting flag."),
    "scope_note": (
        "Stage D grades CL-c7 (frame honesty, PARTIAL by design) and arms K7 "
        "(refute) + K-soft (non-refuting flag) with P-frame/P-self-cert, on the "
        "F12 fixtures (F12a, F12b) under the R3 pin and the R2 disposition. "
        "CL-c3c-ii is recorded OPEN, not closed. No substrate promotion: eval-tier "
        "only; nothing canonical until Will signs off."),
}


# --- organ: the probe + reconstruction law (embedded VERBATIM) --------------
ORGAN = {
    "probe_id": "three_channel_kg_probe_A_v1",
    "role": "probe",
    "path": "A",
    "module": "lloyd_v4.evals.three_channel_kg.probe",
    "sha256": PROBE_SHA,
    "probe_source_verbatim": PROBE_SRC,
    "reconstruction_law": (
        "Bordered Hessian H_b = [[0, g^T],[g, H]] (4x4, H symmetric 3x3, "
        "q = g^T g != 0). det(H_b) is expanded EXACTLY in Q and partitioned into "
        "the exhaustive disjoint monomial classes Delta_c (off-diagonal-H only), "
        "Delta_s (diagonal-H only), Delta_m (one diagonal x one off-diagonal), "
        "with det(H_b) == Delta_c + Delta_s + Delta_m. Then kappa_X = -Delta_X/q^2 "
        "and K_G = kappa_c + kappa_s + kappa_int. FRAME HONESTY (CL-c7): under a "
        "generic rotation R in SO(3) (F12a, conv. x=Ry, g'=R^T g, H'=R^T H R) the "
        "channel triple (kappa_c,kappa_s,kappa_int) MOVES while the sum K_G = "
        "sigma_2 = -det(H_b)/q^2 is INVARIANT (the sum is the intrinsic invariant; "
        "the channels are a frame-relative representative — R2). Under a signed "
        "permutation P (F12b, swap axes 1<->2) the channel triple is FIXED (the "
        "S3 x {+/-} stabilizer of the monomial decomposition at n=3) and K_G is "
        "again invariant. Exact Q only; sqrt-q-free (q enters only as q^2). "
        "Completeness — whether {sigma_r}+orientation determines the "
        "gauge+permutation class (CL-c3c-ii / L1) — is OPEN and NOT established "
        "here (PARTIAL by design)."),
}


# --- referee block ----------------------------------------------------------
REFEREE = {
    "Path_A": "monomial channel read-off (the probe; role=probe).",
    "Path_B": (
        "independent TOTAL referee referee_total.referee_total: "
        "K_G = -det(H_b)/q^2 via fraction-free Bareiss (generic determinant; no "
        "DBP channel formulas; sqrt-q-free); refuses q==0 with RefereeRefusal. "
        "Used to confirm K_G invariance under F12a/F12b on an independent path."),
    "Path_Bprime": (
        "independent CHANNEL referee referee_channel.referee_channel: channels "
        "from the split shape operator P H_X P (P = I - g g^T/q) + trace "
        "identities; disjoint source; refuses q==0. Used to confirm the moved "
        "(F12a) and fixed (F12b) channel triples on an independent path."),
    "Path_C": (
        "frozen external fixture oracle oracle.oracle: exact-Q F12a/F12b "
        "expectations transcribed from FIXTURES.md (R3 pin). P-self-cert: the "
        "oracle does NOT import A/B/B' and they do not import it."),
    "separation_note": (
        "The probe never imports the referee. Path B, Path B', Path C are "
        "code-disjoint sources. All grading is mechanical exact-Q equality (no "
        "tolerance)."),
}


PREREG = {
    "authority": (
        "Frozen objects under results/three_channel_kg/ (manifest_v1.json, "
        "SCHEMA.md, FIXTURES.md, CLAIM_LEDGER.md) verified vs "
        "freeze_pins_sha256.json; built+frozen bench under "
        "src/lloyd_v4/evals/three_channel_kg/ imported READ-ONLY from the stable "
        "main path and pinned in depends_on. Covenant loop; R2/R3 dispositions. "
        "ORCHESTRATOR OVERRIDE: no v4-campaign-discipline skill loaded this "
        "session — frozen objects + embedded covenant are the sole binding "
        "authority."),
    "campaign_id": "three_channel_kg",
    "cycle_id": "c001",
    "stage": "stage_d",
    "stage_title": "frame honesty (CL-c7, PARTIAL by design)",
    "frozen": True,
    "version": "stage_d_prereg_v1",
    "depends_on": DEPENDS_ON,
    "frozen_authority_pins": FROZEN_AUTHORITY_PINS,
    "organ": ORGAN,
    "referee": REFEREE,
    "predictions": PREDICTIONS,
    "expectations": EXPECTATIONS,
    "grader_clauses": GRADER_CLAUSES,
    "status_move_rules": STATUS_MOVE_RULES,
    "scope": {
        "claims": ["CL-c7"],
        "claims_open_recorded": ["CL-c3c-ii"],
        "armed_kills": ["K7", "K-soft"],
        "fixtures": ["F12a", "F12b"],
        "preconditions": ["P-self-cert", "P-frame"],
        "partial_by_design": True,
        "out_of_scope": {
            "note": (
                "CL-c1..c6 and K1..K6/K8..K11 type gates belong to other stages "
                "(Stage A grades CL-c1/CL-c2; B/C/E grade their own). Stage D "
                "touches only the F12 frame-honesty fixtures. CL-c3c-ii is "
                "recorded OPEN, not closed — its closure (L1 / {sigma_r}-"
                "completeness) is out of Stage-D scope."),
        },
    },
    "no_tolerance_note": (
        "Exact Q only; no tolerance band anywhere; a near-miss is a FAIL. No "
        "substrate promotion (eval-tier only). Nothing canonical until Will signs "
        "off."),
    "two_run_byte_stability_note": (
        "The battery is run TWICE; the records jsonl from both runs MUST be "
        "byte-identical (sorted-keys serialisation, exact-Q frac:n/d strings, no "
        "float/time/random)."),
}


def main() -> None:
    body = json.dumps(PREREG, sort_keys=True, indent=2, ensure_ascii=True)
    prereg_path = os.path.join(STAGE, "prereg.json")
    with open(prereg_path, "w", encoding="utf-8") as fh:
        fh.write(body + "\n")
    # the pin is the sha256 of the exact bytes written (including trailing \n).
    with open(prereg_path, "rb") as fh:
        pin = hashlib.sha256(fh.read()).hexdigest()
    with open(os.path.join(STAGE, "prereg_sha256.pin"), "w", encoding="utf-8") as fh:
        fh.write(pin + "\n")
    print(f"wrote {prereg_path}")
    print(f"prereg_sha256.pin = {pin}")
    print(f"probe sha256 (organ/depends_on) = {PROBE_SHA}")


if __name__ == "__main__":
    main()
