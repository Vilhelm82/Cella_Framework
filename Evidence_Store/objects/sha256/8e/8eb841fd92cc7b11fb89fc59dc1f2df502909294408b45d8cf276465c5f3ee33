"""c001 `three_channel_kg` — STAGE A prereg builder (covenant step 1).

Writes the FROZEN `prereg.json` BEFORE any battery code exists, then computes
`prereg_sha256.pin`. The prereg embeds (a) the probe + its reconstruction law
VERBATIM as the `organ`, (b) every governing clause VERBATIM (the battery
string-compares these at runtime and REFUSES on drift), (c) the falsifiable
predictions with units, (d) the expectations graded against, (e) the
status_move_rules encoding R1 (CL-c1 universal -> symbolic identity over Q[g,H]
required), (f) depends_on = sha256 of the manifest + every bench module the
battery executes, (g) the referee description, frozen:true, version.

This builder is run ONCE to freeze the prereg. It does not grade and is not the
battery; it only assembles the frozen object deterministically (sorted keys).

Bench: imported read-only from the committed+frozen shared checkout
(BENCH below). Its module shas match the known-good instrument shas and are
pinned in depends_on. The frozen authority objects (manifest/SCHEMA/FIXTURES/
ledger) are read from the worktree copy (identical shas to the shared checkout).
"""

from __future__ import annotations

import hashlib
import json
import os

WORKTREE = "/home/wlloyd/Lloyd_Engine_V4/.claude/worktrees/agent-a327d51553a3e8a26"
SHARED = "/home/wlloyd/Lloyd_Engine_V4"
BENCH = os.path.join(SHARED, "src/lloyd_v4/evals/three_channel_kg")  # committed+frozen bench
RESULTS = os.path.join(WORKTREE, "results/three_channel_kg")
STAGE = os.path.join(RESULTS, "stage_a")


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------
# depends_on: manifest + EVERY bench module the Stage-A battery executes.
# (probe = Path A organ; referee_total = Path B; referee_channel = Path B';
#  oracle = Path C; fixtures = operand generator/Stage-0 control; schema =
#  record type + role gate + the verbatim closure identities/type gates.)
# --------------------------------------------------------------------------
DEPENDS_ON = {
    "results/three_channel_kg/manifest_v1.json":
        sha256_file(os.path.join(RESULTS, "manifest_v1.json")),
    "src/lloyd_v4/evals/three_channel_kg/probe.py":
        sha256_file(os.path.join(BENCH, "probe.py")),
    "src/lloyd_v4/evals/three_channel_kg/schema.py":
        sha256_file(os.path.join(BENCH, "schema.py")),
    "src/lloyd_v4/evals/three_channel_kg/fixtures.py":
        sha256_file(os.path.join(BENCH, "fixtures.py")),
    "src/lloyd_v4/evals/three_channel_kg/referee_total.py":
        sha256_file(os.path.join(BENCH, "referee_total.py")),
    "src/lloyd_v4/evals/three_channel_kg/referee_channel.py":
        sha256_file(os.path.join(BENCH, "referee_channel.py")),
    "src/lloyd_v4/evals/three_channel_kg/oracle.py":
        sha256_file(os.path.join(BENCH, "oracle.py")),
}

# Also pin the other frozen objects (read as authority, not executed as code).
FROZEN_AUTHORITY = {
    "results/three_channel_kg/SCHEMA.md":
        sha256_file(os.path.join(RESULTS, "SCHEMA.md")),
    "results/three_channel_kg/FIXTURES.md":
        sha256_file(os.path.join(RESULTS, "FIXTURES.md")),
    "results/three_channel_kg/CLAIM_LEDGER.md":
        sha256_file(os.path.join(RESULTS, "CLAIM_LEDGER.md")),
    "results/three_channel_kg/freeze_pins_sha256.json":
        sha256_file(os.path.join(RESULTS, "freeze_pins_sha256.json")),
}

# --------------------------------------------------------------------------
# organ: the probe + its reconstruction law, embedded VERBATIM.
# --------------------------------------------------------------------------
PROBE_SRC = read_text(os.path.join(BENCH, "probe.py"))

ORGAN = {
    "probe_id": "three_channel_kg_probe_A_v1",
    "role": "probe",
    "path": "A",
    "module": "lloyd_v4.evals.three_channel_kg.probe",
    "sha256": DEPENDS_ON["src/lloyd_v4/evals/three_channel_kg/probe.py"],
    "reconstruction_law": (
        "Bordered Hessian H_b = [[0, g^T],[g, H]] (4x4, H symmetric 3x3, "
        "q = g^T g != 0). det(H_b) is expanded EXACTLY in Q and partitioned "
        "into the exhaustive disjoint monomial classes Delta_c (off-diagonal-H "
        "only), Delta_s (diagonal-H only), Delta_m (one diagonal x one "
        "off-diagonal), with det(H_b) == Delta_c + Delta_s + Delta_m. Then "
        "kappa_X = -Delta_X / q^2 and K_G = kappa_c + kappa_s + kappa_int "
        "(kappa_int read off Delta_m). Exact Q only; sqrt-q-free (q enters only "
        "as q^2). The singular stratum q = g^T g = 0 (vanishing gradient / "
        "cone apex; over R equivalently every g_i = 0) is a TYPED refusal, "
        "never 0/NaN/placeholder. A regular jet with a single zero gradient "
        "component (some g_i = 0 with q != 0) is NOT singular and computes "
        "normally (frozen fixture F6)."),
    "probe_source_verbatim": PROBE_SRC,
}

# --------------------------------------------------------------------------
# referee: the four separated truth paths (no check certifies itself).
# --------------------------------------------------------------------------
REFEREE = {
    "Path_A": "monomial channel read-off (the probe; role=probe).",
    "Path_B": ("independent TOTAL referee referee_total.referee_total: "
               "K_G = -det(H_b)/q^2 via fraction-free Bareiss (generic "
               "determinant; no DBP channel formulas; sqrt-q-free); refuses "
               "q==0 with RefereeRefusal."),
    "Path_Bprime": ("independent CHANNEL referee referee_channel."
                    "referee_channel: channels from the split shape operator "
                    "P H_X P (P = I - g g^T/q) + trace identities (genuine "
                    "non-mirror kappa_s); disjoint source; refuses q==0 with "
                    "RefereeRefusal."),
    "Path_C": ("frozen external fixture oracle oracle.oracle: exact-Q "
               "expectations transcribed from FIXTURES.md. P-self-cert: the "
               "oracle does NOT import A/B/B' and they do not import it."),
    "separation_note": ("The probe never imports the referee. Path B, Path B', "
                        "Path C are code-disjoint sources. All grading is "
                        "mechanical exact-Q equality (no tolerance)."),
}

# --------------------------------------------------------------------------
# GRADER_CLAUSES: governing clauses embedded VERBATIM. The battery embeds the
# SAME dict and string-compares each clause against THIS frozen prereg at
# runtime; any drift -> REFUSE. (Covenant step 2 / Rule 1.8 clause embedding.)
# --------------------------------------------------------------------------
GRADER_CLAUSES = {
    # The five per-row closure identities, transcribed VERBATIM from the frozen
    # SCHEMA.md "Per-row closure identities" / manifest semantics_pinned.row_pass.
    "row_pass": (
        "got.(K_G,kappa_c,kappa_s,kappa_int)==expected "
        "AND got.K_G==sum(channels) "
        "AND got.K_G==PathB_total "
        "AND got.channels==PathBprime_channels "
        "AND det(H_b)==Delta_c+Delta_s+Delta_m"),
    "closure_1_tuple_eq_expected":
        "got.(K_G, kappa_c, kappa_s, kappa_int) == expected",
    "closure_2_K_G_eq_sum_channels":
        "got.K_G == sum(channels)  (kappa_c + kappa_s + kappa_int)",
    "closure_3_K_G_eq_pathB_total":
        "got.K_G == Path-B total  (-det(H_b)/q^2, sqrt-q-free)",
    "closure_4_channels_eq_pathBprime":
        "got.channels == Path-B' channels  (split shape-operator det2, code-disjoint)",
    "closure_5_det_hb_eq_partition_sum":
        "det(H_b) == Delta_c + Delta_s + Delta_m",
    # Semantics pinned (manifest semantics_pinned), VERBATIM.
    "semantics_K_G": "kappa_c + kappa_s + kappa_int (exact in Q)",
    "semantics_kappa_X": (
        "-Delta_X / q^2, with det(H_b) = Delta_c + Delta_s + Delta_m "
        "(off-diagonal -> Delta_c, diagonal -> Delta_s, mixed -> Delta_m)"),
    "semantics_total_referee": "K_G == -det(H_b)/q^2 (Path B, sqrt-q-free)",
    "semantics_channel_referee":
        "channels == split-shape-operator det2 channels (Path B', disjoint source)",
    # Type gates (frozen SCHEMA.md "Type gates"), VERBATIM.
    "type_gate_sqrt_q_leak":
        "a total/channel referee returning a radical/float instead of Fraction -> hard fail (K8).",
    "type_gate_tolerance_leak":
        "any injected mismatch that passes/warns instead of hard-failing -> fail (K9).",
    "type_gate_singular_lie":
        ("q=0 / cone-apex / g_i=0 returning 0/NaN/placeholder instead of typed "
         "REFUSED -> fail (refuse-not-lie, K11)."),
    # Preconditions (frozen SCHEMA.md "Preconditions"), VERBATIM.
    "precondition_P_self_cert":
        "the oracle (Path C) must be external to A/B/B', or the run is void.",
    "precondition_P_frame":
        "every channel fixture must carry its frame annotation, or it is rejected.",
    # Armed kill conditions for THIS stage (CLAIM_LEDGER.md), VERBATIM.
    "K2_partition": "det(H_b)-(Delta_c+Delta_s+Delta_m)!=0.",
    "K3_two_derivation":
        "Path-A channels != Path-B' channels (incl. kappa_s-mirror mutant).",
    "K5_wrong_sign":
        "bordered-Hessian sign flip inverts an expected sign (F3/F7/F8).",
    "K6_rank_heuristic": "nonzero on the developable cone F9.",
    "K8_sqrt_q_leak": "radical/float instead of Fraction -> hard fail (K8).",
    "K9_tolerance_leak":
        "any injected mismatch passing/warning instead of hard-fail -> fail (K9).",
    "K11_singular_lie":
        "q=0 / cone-apex / g_i=0 -> typed REFUSED, never 0/NaN/placeholder (K11).",
    # R1 disposition (CLAIM_LEDGER.md reserved dispositions), VERBATIM.
    "R1_proven_warrant":
        ("logic-forced, not discretionary. A verified finite exact-Q both-sign "
         "witness earns [PROVEN] for an impossibility / existence claim (CL-c3); "
         "universal claims (CL-c1, CL-c3b) require the symbolic identity over "
         "Q[g,H]. The stage prereg encodes this in status_move_rules."),
}

# --------------------------------------------------------------------------
# expectations: the ground-truth values graded against, exact Q (string n/d).
# These are the FROZEN targets (FIXTURES.md / oracle), transcribed.
# --------------------------------------------------------------------------
EXPECTATIONS = {
    "channel_fixtures": {
        # fixture_id -> (K_G, kappa_c, kappa_s, kappa_int) as n/d strings
        "F1":  ["0/1", "0/1", "0/1", "0/1"],
        "F2":  ["0/1", "0/1", "0/1", "0/1"],
        "F3":  ["1/12", "1/12", "0/1", "0/1"],
        "F4":  ["1/3", "1/3", "0/1", "0/1"],
        "F5":  ["4/81", "0/1", "4/81", "0/1"],
        "F6":  ["1/1", "0/1", "1/1", "0/1"],
        "F7":  ["-1/9", "-1/9", "0/1", "0/1"],
        "F8":  ["-3/49", "-1/49", "1/49", "-3/49"],
        "F9":  ["0/1", "0/1", "0/1", "0/1"],
        "F10": ["2/9", "1/3", "0/1", "-1/9"],
        "F11": ["0/1", "-1/9", "-1/9", "2/9"],
    },
    "keystone_F8": {
        "q": "14/1", "det_hb": "12/1",
        "K_G": "-3/49", "kappa_c": "-1/49", "kappa_s": "1/49", "kappa_int": "-3/49",
    },
    "sphere_F6_KG": "1/1",
    "developable_cone_F9_KG": "0/1",
    "both_sign_witnesses": {
        "sphere_F6_KG": "1/1", "keystone_F8_KG": "-3/49",
        "F10_kappa_int": "-1/9", "F11_kappa_int": "2/9",
    },
    "F13_parity_contrast": {
        "sigma_2": "-3/49",  # in Q, equals F8 K_G
        "C1_hat": "-24/1",   # in Q
        "sigma_1_field": "Q(sqrt14)",  # NOT exact-Q; deliberately not emitted as a numeric value
    },
    "singular_stratum_q0": {
        "jet": "g=(0,0,0)",
        "expected": "typed REFUSED on all of Path A / Path B / Path B' (never 0/NaN/placeholder)",
    },
    "symbolic_identity_over_Q_g_H": {
        "indeterminates": ["g1", "g2", "g3", "h11", "h12", "h13", "h22", "h23", "h33"],
        "claim": "det(H_b) - (Delta_c + Delta_s + Delta_m) == 0 as a polynomial in Q[g,H]",
        "expected_residual_monomials": 0,
        "expected_det_monomials": 12,
        "expected_partition_monomials": 12,
        "disjoint_supports": True,
        "support_union_eq_det_support": True,
    },
}

# --------------------------------------------------------------------------
# predictions: falsifiable, units declared. Each maps to a claim / kill /
# precondition in this stage's scope. "units: exact Q (Fraction)" unless noted.
# --------------------------------------------------------------------------
PREDICTIONS = [
    {
        "id": "P1_row_pass_all",
        "statement": ("For every channel fixture in {F1..F11}, all five frozen "
                      "per-row closure identities hold exact-Q (no tolerance): "
                      "tuple==expected; K_G==sum(channels); K_G==Path-B total; "
                      "channels==Path-B' channels; det(H_b)==Delta_c+Delta_s+"
                      "Delta_m."),
        "units": "boolean per row (exact-Q equality); count of passing rows out of 11",
        "expected": "11 of 11 rows pass all five identities",
        "claims": ["CL-c1", "CL-c2"],
        "kills_relevant": ["K2", "K3", "K5"],
    },
    {
        "id": "P2_keystone_F8",
        "statement": ("Keystone F8 (jet g=(3,1,2), q=14): det(H_b)==12 and "
                      "(K_G,kappa_c,kappa_s,kappa_int)==(-3/49,-1/49,1/49,-3/49) "
                      "on all of Path A, Path B (K_G), Path B' (tuple), Path C "
                      "(tuple) -- exact Q. K_G < 0 (signed) and K_G==sum(channels)."),
        "units": "exact Q (Fraction) per component",
        "expected": ("q=14; det_hb=12; K_G=-3/49; kappa_c=-1/49; kappa_s=1/49; "
                     "kappa_int=-3/49; agreement across A/B/B'/C"),
        "claims": ["CL-c1", "CL-c2"],
        "kills_relevant": ["K2", "K3", "K5"],
    },
    {
        "id": "P3_partition_K2",
        "statement": ("K2 (partition) does NOT fire on any in-scope fixture: "
                      "det(H_b)-(Delta_c+Delta_s+Delta_m)==0 exact-Q on Path A "
                      "for every {F1..F11}, AND Path-B generic det(H_b) equals "
                      "the Path-A det(H_b) for every fixture."),
        "units": "exact Q (Fraction); residual must be exactly 0/1",
        "expected": ("residual == 0 on all 11 fixtures (Path A); Path-A det_hb "
                     "== Path-B det_hb on all 11 fixtures"),
        "claims": ["CL-c1"],
        "kills_relevant": ["K2"],
    },
    {
        "id": "P4_two_derivation_K3",
        "statement": ("K3 (two-derivation) silent on truth, armed on mutant: "
                      "Path-A channels == Path-B' channels for every {F1..F11} "
                      "(exact Q), AND a kappa_s-mirror MUTANT (det2 of the bare "
                      "self-part H_s without the tangent projector, over q) "
                      "DIFFERS from the truth kappa_s on the kappa_s-trap "
                      "fixtures F5/F6/F8 (so K3 would fire on the mutant)."),
        "units": ("exact Q (Fraction); per-fixture boolean A==B' and "
                  "mutant!=truth on the trap set"),
        "expected": ("A channels == B' channels on all 11 fixtures; "
                     "mirror-mutant kappa_s != truth kappa_s on F5, F6, F8"),
        "claims": ["CL-c2"],
        "kills_relevant": ["K3"],
    },
    {
        "id": "P5_wrong_sign_K5",
        "statement": ("K5 (wrong-sign) catches a bordered-Hessian sign flip on "
                      "F3/F7/F8: the sign-flipped total (+det(H_b)/q^2 instead "
                      "of -det(H_b)/q^2) inverts the expected sign of K_G on "
                      "each of F3 (+1/12), F7 (-1/9), F8 (-3/49), so a flip "
                      "would change the graded sign; the true (unflipped) sign "
                      "matches the oracle on all three."),
        "units": "exact Q (Fraction); sign comparison",
        "expected": ("true K_G sign matches oracle on F3/F7/F8; sign-flip "
                     "mutant inverts (changes) the sign on all three"),
        "claims": ["CL-c1", "CL-c2"],
        "kills_relevant": ["K5"],
    },
    {
        "id": "P6_rank_heuristic_K6",
        "statement": ("K6 (rank-heuristic) does NOT fire on the developable "
                      "cone F9 (x1^2+x2^2-x3^2 at (3,4,5); indefinite Hessian): "
                      "K_G==0 exactly on Path A, Path B, Path B', Path C -- a "
                      "rank/positivity heuristic that returned nonzero here "
                      "would fire K6, but the object returns exactly 0."),
        "units": "exact Q (Fraction); must be exactly 0/1",
        "expected": "K_G == 0 on F9 across A/B/B'/C (never nonzero)",
        "claims": ["CL-c1", "CL-c2"],
        "kills_relevant": ["K6"],
    },
    {
        "id": "P7_sqrt_q_leak_K8",
        "statement": ("K8 (sqrt-q-leak type gate): every value emitted by Path "
                      "A / Path B / Path B' on every {F1..F11} is an exact "
                      "fractions.Fraction (no float, no radical); AND a float "
                      "operand offered at the probe door is REFUSED with a "
                      "TypeError (never silently coerced)."),
        "units": "type predicate (isinstance Fraction); boolean refusal-on-float",
        "expected": ("all emitted K_G/channels/det_hb/q are Fraction on all 11 "
                     "fixtures; a float operand raises TypeError at the door"),
        "claims": ["CL-c1", "CL-c2"],
        "kills_relevant": ["K8"],
    },
    {
        "id": "P8_tolerance_leak_K9",
        "statement": ("K9 (tolerance-leak type gate): an injected exact-Q "
                      "mismatch is HARD-failed, never passed/warned. Concretely, "
                      "perturbing the keystone F8 expected tuple by +1/10^9 in "
                      "one component makes the row-pass predicate evaluate FALSE "
                      "(strict exact equality; no tolerance band admits the "
                      "near-miss)."),
        "units": "boolean (row-pass under injected near-miss must be FALSE)",
        "expected": ("injected +1/10^9 mismatch on F8 -> row-pass == FALSE "
                     "(hard fail, not a tolerated near-miss)"),
        "claims": ["CL-c1", "CL-c2"],
        "kills_relevant": ["K9"],
    },
    {
        "id": "P9_singular_lie_K11",
        "statement": ("K11 (singular-lie / refuse-not-lie): a GENUINE singular "
                      "jet q=g^T g=0 (g=(0,0,0), cone apex) is a TYPED refusal "
                      "on all of Path A (ThreeChannelRefusal), Path B "
                      "(RefereeRefusal), Path B' (RefereeRefusal) -- never "
                      "0/NaN/placeholder. Separately, a single zero gradient "
                      "component at a regular point (F6: g=(6/5,8/5,0), q=4!=0) "
                      "is NOT refused and evaluates to K_G=1."),
        "units": "typed-exception predicate; boolean (no numeric value on q=0)",
        "expected": ("Path A/B/B' all raise typed refusals on g=(0,0,0); F6 "
                     "(single g_i=0, q=4) returns K_G=1 with no refusal"),
        "claims": ["CL-c1", "CL-c2"],
        "kills_relevant": ["K11"],
    },
    {
        "id": "P10_preconditions",
        "statement": ("Preconditions hold (run not void): P-self-cert -- the "
                      "Path C oracle module does NOT import probe / "
                      "referee_total / referee_channel / fixtures, and they do "
                      "not import oracle; P-frame -- every channel fixture "
                      "carries a non-empty frame annotation."),
        "units": "boolean (import-graph disjointness; frame-present on every channel fixture)",
        "expected": ("oracle imports none of A/B/B'/fixtures and vice-versa; "
                     "all 11 channel fixtures carry a frame string"),
        "claims": ["CL-c1", "CL-c2"],
        "kills_relevant": [],
        "preconditions": ["P-self-cert", "P-frame"],
    },
    {
        "id": "P11_both_sign_witnesses_CLc1_signed",
        "statement": ("Both-sign witnesses present (CL-c1 object integrity / "
                      "the signed three-channel thesis): a verified exact-Q "
                      "positive witness (sphere F6, K_G=+1) and negative "
                      "witness (keystone F8, K_G=-3/49) coexist, and kappa_int "
                      "attains both signs (F10 kappa_int=-1/9 < 0; F11 "
                      "kappa_int=+2/9 > 0) -- exact Q."),
        "units": "exact Q (Fraction); sign of each witness",
        "expected": ("F6 K_G=+1>0; F8 K_G=-3/49<0; F10 kappa_int=-1/9<0; "
                     "F11 kappa_int=+2/9>0"),
        "claims": ["CL-c1"],
        "kills_relevant": [],
    },
    {
        "id": "P12_symbolic_identity_CLc1_universal",
        "statement": ("CL-c1 UNIVERSAL warrant (R1): the partition identity is "
                      "a SYMBOLIC identity over Q[g,H], not finite-fixture "
                      "agreement. In the polynomial ring Q[g1,g2,g3,h11,h12,"
                      "h13,h22,h23,h33], the cofactor-expanded det(H_b) minus "
                      "(Delta_c+Delta_s+Delta_m) is the ZERO polynomial (0 "
                      "residual monomials); det(H_b) and the partition each "
                      "have 12 monomials; the three pieces have pairwise "
                      "DISJOINT monomial supports whose union equals the det "
                      "support (exhaustive & disjoint). This, with K_G=-det/q^2 "
                      "and kappa_X=-Delta_X/q^2, yields K_G=kappa_c+kappa_s+"
                      "kappa_int for EVERY regular jet (q!=0)."),
        "units": ("count of residual monomials (must be 0); count of det / "
                  "partition monomials (12 each); boolean disjoint-supports; "
                  "boolean support-union==det-support"),
        "expected": ("residual == 0 monomials; det monomials == 12; partition "
                     "monomials == 12; supports pairwise disjoint == True; "
                     "support union == det support == True"),
        "claims": ["CL-c1"],
        "kills_relevant": [],
    },
    {
        "id": "P13_F13_parity_contrast",
        "statement": ("F13 parity-contrast (in fixture scope; no channel "
                      "triple): the even-order invariant sigma_2 = -3/49 is "
                      "exact-Q and EQUALS the keystone F8 K_G; C1_hat = -24 is "
                      "exact-Q; the odd-order sigma_1 lies in Q(sqrt14) and is "
                      "therefore NOT emitted as a numeric oracle value "
                      "(emitting a radical would be a sqrt-q leak). The oracle "
                      "exposes sigma_2 and C1_hat and withholds sigma_1."),
        "units": "exact Q (Fraction) for sigma_2/C1_hat; field-label for sigma_1",
        "expected": ("sigma_2 == -3/49 == F8 K_G; C1_hat == -24; sigma_1 field "
                     "label == Q(sqrt14) and no numeric sigma_1 emitted"),
        "claims": ["CL-c1"],
        "kills_relevant": [],
    },
]

# --------------------------------------------------------------------------
# status_move_rules: which PASS moves which claim to which status (encoding
# R1); which kill fires on which FAIL. Vocabulary: NOT_YET_PROBED ->
# DEMONSTRATED | REFUTED | PARTIAL.
# --------------------------------------------------------------------------
STATUS_MOVE_RULES = {
    "CL-c1": {
        "ledger_statement": ("det(H_b)=Delta_c+Delta_s+Delta_m => K_G=kappa_c+"
                             "kappa_s+kappa_int, exhaustive & disjoint"),
        "universal_claim": True,
        "R1_disposition": ("CL-c1 is a UNIVERSAL claim. [PROVEN]/DEMONSTRATED "
                           "REQUIRES the symbolic identity over Q[g,H]; finite-"
                           "fixture agreement alone is necessary but NOT "
                           "sufficient."),
        "on_pass": {
            "condition": ("P1 AND P2 AND P3 AND P11 AND P12 AND P13 all PASS "
                          "-- crucially P12 (the symbolic identity over Q[g,H]) "
                          "AND P3 (K2 partition silent finite) AND P11 (both-"
                          "sign witnesses) -- with P1/P2/P13 the finite "
                          "corroboration."),
            "move_to": "DEMONSTRATED",
            "warrant_scope": ("universal warrant: symbolic identity over "
                              "Q[g,H] established (P12), exhaustive & disjoint "
                              "partition proven, corroborated finitely "
                              "(P1/P2/P3/P11/P13). Eval-tier; no substrate "
                              "promotion; canonical only on Will's sign-off."),
        },
        "on_fail": {
            "if_P12_fails": ("symbolic identity over Q[g,H] NOT established -> "
                             "HALT (do NOT downgrade to a finite-only warrant); "
                             "route to Will."),
            "if_P3_fails": "K2 fires (partition broken) -> REFUTED candidate; HALT, route to Will.",
            "if_P1_or_P2_fails": ("finite corroboration broken -> K2/K3/K5 as "
                                  "applicable; HALT, route to Will."),
            "default": "any FAIL -> HALT, preserve chain, route to Will; no move.",
        },
    },
    "CL-c2": {
        "ledger_statement": ("bordered-determinant channels == split-shape-"
                             "operator channels (kappa_s non-mirror)"),
        "universal_claim": False,
        "R1_disposition": ("CL-c2 is NOT named in R1. Graded per its ledger "
                           "statement: the two channel derivations (Path A "
                           "monomial vs Path B' split-shape-operator) "
                           "identically agree across the family, K3 silent "
                           "(incl. the kappa_s-mirror mutant being rejected)."),
        "on_pass": {
            "condition": ("P4 PASS (Path-A channels == Path-B' channels on all "
                          "{F1..F11}, AND the kappa_s-mirror mutant differs from "
                          "truth on the kappa_s-trap fixtures so K3 would fire "
                          "on it) -- with P1/P2 the per-row corroboration."),
            "move_to": "DEMONSTRATED",
            "warrant_scope": ("the two disjoint channel derivations agree "
                              "channel-for-channel across the frozen Stage-A "
                              "family {F1..F11} (finite family, exact Q); the "
                              "non-mirror kappa_s is established as the correct "
                              "split-shape form (the mirror mutant is rejected "
                              "by K3 on the trap set). Warrant scope: the "
                              "frozen family, NOT a symbolic-over-Q[g,H] "
                              "universal (CL-c2 is not an R1 universal claim). "
                              "Eval-tier; canonical only on Will's sign-off."),
        },
        "on_fail": {
            "if_P4_A_ne_Bprime": "K3 fires (two derivations disagree) -> REFUTED candidate; HALT, route to Will.",
            "if_P4_mutant_eq_truth": ("the kappa_s-mirror mutant FAILS to "
                                      "differ from truth on the trap set -> the "
                                      "non-mirror distinction is not witnessed "
                                      "-> HALT, route to Will."),
            "default": "any FAIL -> HALT, preserve chain, route to Will; no move.",
        },
    },
    "kills": {
        "K2": {"fires_on": "P3 FAIL (det(H_b)-(Delta_c+Delta_s+Delta_m)!=0)", "claim": "CL-c1"},
        "K3": {"fires_on": "P4 FAIL (Path-A channels != Path-B' channels, incl. kappa_s-mirror mutant)", "claim": "CL-c2"},
        "K5": {"fires_on": "P5 FAIL (bordered-Hessian sign flip inverts an expected sign on F3/F7/F8)", "claim": "object integrity"},
        "K6": {"fires_on": "P6 FAIL (nonzero on the developable cone F9)", "claim": "CL-c6 (object integrity here)"},
        "K8": {"fires_on": "P7 FAIL (radical/float instead of Fraction)", "claim": "type gate"},
        "K9": {"fires_on": "P8 FAIL (an injected mismatch passing/warning instead of hard-fail)", "claim": "type gate"},
        "K11": {"fires_on": "P9 FAIL (q=0/cone-apex/g_i=0 returning 0/NaN/placeholder instead of typed REFUSED)", "claim": "refuse-not-lie"},
    },
    "preconditions": {
        "P-self-cert": {"checked_by": "P10", "on_fail": "run VOID"},
        "P-frame": {"checked_by": "P10", "on_fail": "channel fixture rejected; run VOID"},
    },
    "halt_rule": ("On ANY prediction FAIL: HALT. Preserve the chain verbatim. "
                  "Do NOT fix, redesign, soften, or widen. Write what is held "
                  "and route to Will. No status move is proposed for a claim "
                  "whose gating predictions did not all PASS."),
    "scope_note": ("Stage A grades CL-c1, CL-c2 only and arms K2/K3/K5/K6/K8/"
                   "K9/K11 with P-self-cert/P-frame. K1/K4/K7/K10 and "
                   "F12/F12a/F12b are OUT of Stage-A scope (other stages). No "
                   "substrate promotion: eval-tier only; nothing canonical "
                   "until Will signs off."),
}

# --------------------------------------------------------------------------
# assemble + freeze
# --------------------------------------------------------------------------
PREREG = {
    "campaign_id": "three_channel_kg",
    "cycle_id": "c001",
    "stage": "stage_a",
    "stage_title": "retrodiction spine + Stage-0 controls (gating stage)",
    "version": "stage_a_prereg_v1",
    "frozen": True,
    "authority": ("Frozen objects under results/three_channel_kg/ (manifest_v1.json, "
                  "SCHEMA.md, FIXTURES.md, CLAIM_LEDGER.md) verified vs "
                  "freeze_pins_sha256.json; built+frozen bench under "
                  "src/lloyd_v4/evals/three_channel_kg/ imported read-only and "
                  "pinned in depends_on. Covenant loop; R1/R2/R3 dispositions."),
    "scope": {
        "claims": ["CL-c1", "CL-c2"],
        "armed_kills": ["K2", "K3", "K5", "K6", "K8", "K9", "K11"],
        "preconditions": ["P-self-cert", "P-frame"],
        "fixtures": ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F13"],
        "out_of_scope": {
            "kills": ["K1", "K4", "K7", "K10"],
            "fixtures": ["F12", "F12a", "F12b"],
            "note": "K1/K4/K7/K10 and F12 family belong to other stages.",
        },
    },
    "semantics_pinned_anchor": {
        "K_G": "K_G = -det(H_b)/q^2",
        "kappa_X": "kappa_X = -Delta_X/q^2",
        "det_Hb": "det(H_b) = Delta_c + Delta_s + Delta_m",
        "keystone_F8": "q=14, det(H_b)=12, (K_G,kappa_c,kappa_s,kappa_int)=(-3/49,-1/49,1/49,-3/49)",
        "sphere_F6": "K_G=1",
        "developable_cone_F9": "K_G=0 (0-or-refusal, never nonzero -> K6)",
    },
    "organ": ORGAN,
    "referee": REFEREE,
    "grader_clauses": GRADER_CLAUSES,
    "predictions": PREDICTIONS,
    "expectations": EXPECTATIONS,
    "status_move_rules": STATUS_MOVE_RULES,
    "depends_on": DEPENDS_ON,
    "frozen_authority_pins": FROZEN_AUTHORITY,
    "k11_frozen_spec_disposition": (
        "Manifest stage0_controls.singular_refusal lists 'g_i=0' among singular "
        "strata, but frozen fixture F6 (sphere at (3/5,4/5,0), g=(6/5,8/5,0), "
        "g3=0, q=4!=0) is a + sign witness that MUST evaluate to K_G=1. Forced "
        "reading (the probe implements exactly this; FIXTURES.md scope cap "
        "concurs): the genuine singular stratum is q=g^T g=0 (vanishing "
        "gradient / cone apex; over R equivalently every g_i=0). A single zero "
        "gradient component at a regular point (q!=0) evaluates normally. So "
        "K11 is exercised with a genuine q=0 jet (g=(0,0,0)) and F6 itself must "
        "evaluate to K_G=1. This is the Phase-1 tension acted upon, NOT a "
        "spurious FAIL."),
    "no_tolerance_note": ("Exact Q only; no tolerance band anywhere; a near-miss "
                          "is a FAIL. No substrate promotion (eval-tier only). "
                          "Nothing canonical until Will signs off."),
    "two_run_byte_stability_note": ("The battery is run TWICE; the records jsonl "
                                    "from both runs MUST be byte-identical "
                                    "(sorted-keys serialisation, exact-Q frac:n/d "
                                    "strings, no float/time/random)."),
}


def main() -> None:
    body = json.dumps(PREREG, sort_keys=True, indent=2, ensure_ascii=True)
    prereg_path = os.path.join(STAGE, "prereg.json")
    with open(prereg_path, "w", encoding="utf-8") as fh:
        fh.write(body + "\n")
    # pin = sha256 of the EXACT bytes written.
    with open(prereg_path, "rb") as fh:
        pin = hashlib.sha256(fh.read()).hexdigest()
    with open(os.path.join(STAGE, "prereg_sha256.pin"), "w", encoding="utf-8") as fh:
        fh.write(pin + "\n")
    print("prereg.json written:", prereg_path)
    print("prereg_sha256.pin  :", pin)
    print("predictions        :", len(PREDICTIONS))


if __name__ == "__main__":
    main()
