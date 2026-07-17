"""c001 `three_channel_kg` — STAGE A mechanical grader (covenant step 4).

Runs the battery once, captures the 13 prediction verdicts, and writes
`prediction_verdicts.json`: each prediction `pass: true|false` with counts/
units, the `prereg_pin`, the `records_sha256`, and `status_moves_proposed`.

The status moves are derived MECHANICALLY from the frozen prereg's
`status_move_rules` against the realized PASS/FAIL set. HALT discipline: if any
prediction FAILs, no status move is proposed for a claim whose gating
predictions did not all PASS, and the HALT reason is recorded.
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

    # units per prediction, transcribed from the frozen prereg predictions list.
    units_by_id = {p["id"]: p["units"] for p in prereg["predictions"]}

    # records sha256 (canonical serialization, same as the run output)
    lines = [json.dumps(r, sort_keys=True, ensure_ascii=True, allow_nan=False)
             for r in records]
    body = "\n".join(lines) + "\n"
    records_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()

    # cross-check against the on-disk records.jsonl (must match run output)
    with open(RECORDS_PATH, "rb") as fh:
        disk_sha = hashlib.sha256(fh.read()).hexdigest()

    with open(battery.PREREG_PIN_PATH, "r", encoding="utf-8") as fh:
        prereg_pin = fh.read().strip()

    n_pass = sum(1 for v in verdicts.values() if v["pass"])
    all_pass = n_pass == len(verdicts)
    failing = [pid for pid, v in verdicts.items() if not v["pass"]]

    smr = prereg["status_move_rules"]

    # mechanical status moves: only propose a move when ALL gating predictions
    # for that claim PASS (HALT discipline otherwise).
    clc1_gates = ["P1_row_pass_all", "P2_keystone_F8", "P3_partition_K2",
                  "P11_both_sign_witnesses_CLc1_signed",
                  "P12_symbolic_identity_CLc1_universal",
                  "P13_F13_parity_contrast"]
    clc2_gates = ["P1_row_pass_all", "P2_keystone_F8", "P4_two_derivation_K3"]

    clc1_ok = all(verdicts[g]["pass"] for g in clc1_gates)
    clc2_ok = all(verdicts[g]["pass"] for g in clc2_gates)

    status_moves = []
    if clc1_ok:
        status_moves.append({
            "claim": "CL-c1",
            "from": "NOT_YET_PROBED",
            "to": smr["CL-c1"]["on_pass"]["move_to"],
            "gating_predictions": clc1_gates,
            "all_gates_pass": True,
            "warrant_scope": smr["CL-c1"]["on_pass"]["warrant_scope"],
            "R1_universal": True,
            "R1_note": ("universal warrant satisfied via the symbolic identity "
                        "over Q[g,H] (P12), NOT finite-fixture agreement alone."),
        })
    else:
        status_moves.append({
            "claim": "CL-c1", "from": "NOT_YET_PROBED", "to": "NO MOVE (HALT)",
            "gating_predictions": clc1_gates, "all_gates_pass": False,
            "halt": "gating predictions did not all pass; route to Will."})

    if clc2_ok:
        status_moves.append({
            "claim": "CL-c2",
            "from": "NOT_YET_PROBED",
            "to": smr["CL-c2"]["on_pass"]["move_to"],
            "gating_predictions": clc2_gates,
            "all_gates_pass": True,
            "warrant_scope": smr["CL-c2"]["on_pass"]["warrant_scope"],
            "R1_universal": False,
            "R1_note": ("CL-c2 not an R1 universal claim; warrant scope is the "
                        "frozen Stage-A family {F1..F11}, the non-mirror kappa_s "
                        "established (mirror mutant rejected by K3)."),
        })
    else:
        status_moves.append({
            "claim": "CL-c2", "from": "NOT_YET_PROBED", "to": "NO MOVE (HALT)",
            "gating_predictions": clc2_gates, "all_gates_pass": False,
            "halt": "gating predictions did not all pass; route to Will."})

    # which kills fired (a kill fires iff its mapped prediction FAILed)
    kills_fired = []
    kill_map = {"K2": "P3_partition_K2", "K3": "P4_two_derivation_K3",
                "K5": "P5_wrong_sign_K5", "K6": "P6_rank_heuristic_K6",
                "K8": "P7_sqrt_q_leak_K8", "K9": "P8_tolerance_leak_K9",
                "K11": "P9_singular_lie_K11"}
    for kill, pid in kill_map.items():
        if not verdicts[pid]["pass"]:
            kills_fired.append({"kill": kill, "via_prediction": pid})

    out = {
        "campaign_id": "three_channel_kg",
        "cycle_id": "c001",
        "stage": "stage_a",
        "version": "stage_a_prediction_verdicts_v1",
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
            "P-self-cert": verdicts["P10_preconditions"]["P_self_cert"]["ok"],
            "P-frame": verdicts["P10_preconditions"]["P_frame"]["ok"],
            "run_void": not (verdicts["P10_preconditions"]["P_self_cert"]["ok"]
                             and verdicts["P10_preconditions"]["P_frame"]["ok"]),
        },
        "scope": {
            "claims": ["CL-c1", "CL-c2"],
            "armed_kills": ["K2", "K3", "K5", "K6", "K8", "K9", "K11"],
            "preconditions": ["P-self-cert", "P-frame"],
            "fixtures": ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
                         "F10", "F11", "F13"],
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
