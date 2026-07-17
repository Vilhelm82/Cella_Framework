"""c001 `three_channel_kg` — STAGE C mechanical grader (covenant step 4).

Runs the battery once, captures the 9 prediction verdicts, and writes
`prediction_verdicts.json`: each prediction `pass: true|false` with units, the
`prereg_pin`, the `records_sha256`, and `status_moves_proposed`.

The status move (CL-c4) is derived MECHANICALLY from the frozen prereg's
`status_move_rules` against the realized PASS/FAIL set. HALT discipline: if any
prediction FAILs, no status move is proposed (route to Will), and the HALT
reason + the fired kill (K4) are recorded.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import battery  # noqa: E402

STAGE = battery.STAGE
RECORDS_PATH = os.path.join(STAGE, "records.jsonl")


def main() -> None:
    prereg = battery.load_prereg()
    battery.gate_clauses(prereg)
    battery.gate_bench_pins(prereg)

    records, verdicts = battery.run()

    units_by_id = {p["id"]: p["units"] for p in prereg["predictions"]}

    lines = [json.dumps(r, sort_keys=True, ensure_ascii=True, allow_nan=False)
             for r in records]
    body = "\n".join(lines) + "\n"
    records_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()

    with open(RECORDS_PATH, "rb") as fh:
        disk_sha = hashlib.sha256(fh.read()).hexdigest()

    with open(battery.PREREG_PIN_PATH, "r", encoding="utf-8") as fh:
        prereg_pin = fh.read().strip()

    n_pass = sum(1 for v in verdicts.values() if v["pass"])
    all_pass = n_pass == len(verdicts)
    failing = [pid for pid, v in verdicts.items() if not v["pass"]]

    smr = prereg["status_move_rules"]

    # CL-c4 gating predictions: ALL nine (PC1..PC9) must pass for DEMONSTRATED.
    clc4_gates = ["PC1_keystone_base_jet", "PC2_single_edge_law_keystone",
                  "PC3_sigma_r_preserved_keystone",
                  "PC4_deltaC_in_ker_Sigma_keystone",
                  "PC5_single_edge_law_symbolic_over_Q",
                  "PC6_KG_invariant_symbolic_over_Q",
                  "PC7_two_derivation_under_gauge",
                  "PC8_K4_mutant_guards", "PC9_preconditions"]
    clc4_ok = all(verdicts[g]["pass"] for g in clc4_gates)

    status_moves = []
    if clc4_ok:
        status_moves.append({
            "claim": "CL-c4",
            "from": "NOT_YET_PROBED",
            "to": smr["CL-c4"]["on_pass"]["move_to"],
            "gating_predictions": clc4_gates,
            "all_gates_pass": True,
            "warrant_scope": smr["CL-c4"]["on_pass"]["warrant_scope"],
            "R2_disposition": smr["CL-c4"]["R2_disposition"],
            "R2_universal_symbolic": True,
            "R2_note": ("R2: channels frame-relative in the supplied DBP frame; "
                        "only the sum K_G = sigma_2 is intrinsic. The single-"
                        "edge law AND K_G/sigma_r invariance are established as "
                        "SYMBOLIC IDENTITIES over Q (PC5/PC6), NOT finite-"
                        "keystone agreement alone; witnessed exactly at the "
                        "keystone (PC1/PC2: e1/e2 pin delta kappa_c, e3 moves "
                        "6/49)."),
        })
    else:
        status_moves.append({
            "claim": "CL-c4", "from": "NOT_YET_PROBED", "to": "NO MOVE (HALT)",
            "gating_predictions": clc4_gates, "all_gates_pass": False,
            "halt": "gating predictions did not all pass; route to Will."})

    # K4 fires iff any of its mapped predictions FAILed.
    k4_pred_map = ["PC1_keystone_base_jet", "PC2_single_edge_law_keystone",
                   "PC3_sigma_r_preserved_keystone",
                   "PC4_deltaC_in_ker_Sigma_keystone",
                   "PC5_single_edge_law_symbolic_over_Q",
                   "PC6_KG_invariant_symbolic_over_Q"]
    k4_fires = any(not verdicts[p]["pass"] for p in k4_pred_map)
    kills_fired = []
    if k4_fires:
        kills_fired.append({
            "kill": "K4",
            "via_predictions": [p for p in k4_pred_map if not verdicts[p]["pass"]],
            "condition_verbatim": smr["kills"]["K4"]["condition_verbatim"]})

    out = {
        "campaign_id": "three_channel_kg",
        "cycle_id": "c001",
        "stage": "stage_c",
        "version": "stage_c_prediction_verdicts_v1",
        "prereg_pin": prereg_pin,
        "records_sha256": records_sha,
        "records_sha256_on_disk": disk_sha,
        "records_byte_stable": records_sha == disk_sha,
        "n_predictions": len(verdicts),
        "n_pass": n_pass,
        "all_pass": all_pass,
        "failing_predictions": failing,
        "halt": (not all_pass),
        "halt_reason": (None if all_pass else
                        f"prediction FAIL(s): {failing} -- HALT, route to Will, chain preserved"),
        "defect_chain_count": (0 if all_pass else len(failing)),
        "predictions": {
            pid: {
                "pass": v["pass"],
                "units": units_by_id.get(pid),
                "detail": v,
            } for pid, v in verdicts.items()
        },
        "status_moves_proposed": status_moves,
        "kills_fired": kills_fired,
        "preconditions": {
            "P-self-cert": verdicts["PC9_preconditions"]["P_self_cert"]["ok"],
            "P-frame": verdicts["PC9_preconditions"]["P_frame"]["ok"],
            "run_void": not (verdicts["PC9_preconditions"]["P_self_cert"]["ok"]
                             and verdicts["PC9_preconditions"]["P_frame"]["ok"]),
        },
        "scope": {
            "claims": ["CL-c4"],
            "armed_kills": ["K4"],
            "preconditions": ["P-self-cert", "P-frame"],
            "fixture_set": "GAUGE_SINGLE_EDGE",
            "fixtures": ["F8"],
        },
        "no_tolerance": True,
        "substrate_promotion": False,
        "eval_tier_only": True,
    }

    path = os.path.join(STAGE, "prediction_verdicts.json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(out, sort_keys=True, indent=2, ensure_ascii=True) + "\n")
    print("prediction_verdicts.json ->", path)
    print("prereg_pin     :", prereg_pin)
    print("records_sha256 :", records_sha, "(byte-stable vs disk:", records_sha == disk_sha, ")")
    print("predictions    :", n_pass, "/", len(verdicts), "PASS")
    print("halt           :", out["halt"], "  defect_chain_count:", out["defect_chain_count"])
    print("status_moves   :", [(m["claim"], m["to"]) for m in status_moves])
    print("kills_fired    :", kills_fired)


if __name__ == "__main__":
    main()
