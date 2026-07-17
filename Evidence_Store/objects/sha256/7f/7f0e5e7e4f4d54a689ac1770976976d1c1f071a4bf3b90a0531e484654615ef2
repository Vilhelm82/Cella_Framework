#!/usr/bin/env python3
"""engine_harness.py — L0 certification scaffold (THE ENGINE, Stage A).
Governing predecl: portfolio/campaigns/the_engine/stage_A/STAGE_A_PREDECL.md, pin 44a2c8019b2929b2.
role=probe. The harness never imports a battery as a module; batteries run as subprocesses
(cwd = repo root, per the invocation contract pinned in the predecl). Factored primitives
(pin_gate, clause_gate, records_sha, dual-run certify) are the exports for future batteries.
"""
import sys, os, json, hashlib, subprocess, time, re, argparse, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PREDECL_REL = "portfolio/campaigns/the_engine/stage_A/STAGE_A_PREDECL.md"
PREDECL_PIN16 = "44a2c8019b2929b2"
RECORDS_DIR = os.path.join(HERE, "records")

# ---- Rule 1.8: governing clauses embedded VERBATIM; string-compared against the frozen predecl ----
GRADER_CLAUSES = {
 "PA.1": "PA.1: harness-run portfolio/campaigns/shape_witness/witness_battery.py prints RECORDS_SHA256 39bed5552c805f4d with terminal ALL_PASS and exit 0 on each of two independent runs.",
 "PA.2": "PA.2: harness-run portfolio/campaigns/deficit_engine/wave0_battery.py prints RECORDS_SHA256 74720504dfd88af7 with terminal ALL_PASS and exit 0 on each of two independent runs.",
 "PA.3": "PA.3: harness-run portfolio/campaigns/deficit_engine/rowb_mech_battery.py prints RECORDS_SHA256 cdee40ff26fb262c with terminal ALL_PASS and exit 0 on each of two independent runs.",
 "PA.4": "PA.4: harness-run portfolio/campaigns/deficit_engine/realfiber_probe1.py prints RECORDS_SHA256 7b3b43058ffa0c7c with terminal ALL_PASS and exit 0 on each of two independent runs.",
 "PA.5": "PA.5: harness-run portfolio/campaigns/deficit_engine/realfiber_probe2.py prints RECORDS_SHA256 848b8d8eca916edf with terminal line OUTCOME: INCONCLUSIVE-budget (runs at cap still descending) and exit 0 on each of two independent runs.",
 "PA.6": "PA.6: harness-run portfolio/campaigns/deficit_engine/realfiber_path_cert.py prints RECORDS_SHA256 99fd1859a6e04214 with terminal ALL_PASS and exit 0 on each of two independent runs.",
 "PA.7": "PA.7: harness-run portfolio/campaigns/deficit_engine/realfiber_fullfiber_cert.py prints RECORDS_SHA256 dfde6fbde06ee160 with terminal ALL_PASS and exit 0 on each of two independent runs.",
 "PA.8": "PA.8: control — given expected sha 0000000000000000 for realfiber_path_cert.py, the harness verdict is REFUSE_MISMATCH and never PASS.",
 "PA.9": "PA.9: control — given a predecl copy with any prediction clause byte-altered, the harness refuses with CLAUSE_DRIFT before running any battery.",
}

# ---- Rule 1.9: content pins (sha256[:16] at freeze), gate-enforced before any battery runs ----
CONTENT_PINS = {
 "portfolio/campaigns/shape_witness/witness_battery.py": "abff00bd15d22c84",
 "evals/dbp_involution/rep_utils.py": "0d838e5fd430461b",
 "portfolio/campaigns/deficit_engine/wave0_battery.py": "4b845794e3c5ce0f",
 "portfolio/campaigns/deficit_engine/rowb_mech_battery.py": "de3edfe0b6162b69",
 "portfolio/campaigns/deficit_engine/realfiber_probe1.py": "7296597ea36cbddf",
 "portfolio/campaigns/deficit_engine/realfiber_probe2.py": "5a8540458a7412af",
 "portfolio/campaigns/deficit_engine/realfiber_path_cert.py": "18418b37ee78c949",
 "portfolio/campaigns/deficit_engine/realfiber_fullfiber_cert.py": "36601fb3abe717c2",
 "portfolio/campaigns/shape_witness/WITNESS_PREDECL.md": "967c7909450ef944",
 "portfolio/campaigns/deficit_engine/WAVE0_PREDECL.md": "c6fd7018a4602209",
 "portfolio/campaigns/deficit_engine/ROWB_MECH_PREDECL.md": "0c335fe2fa474d64",
 "portfolio/campaigns/deficit_engine/REALFIBER_PREDECL.md": "9f706c1a74a21317",
 "portfolio/campaigns/shape_witness/STAGEW_report.md": "331b4a34c2714f6f",
 "portfolio/campaigns/deficit_engine/WAVE0_REPORT.md": "768de90c4a73923a",
 "portfolio/campaigns/deficit_engine/ROWB_MECH_REPORT.md": "9a536866ab29a7e6",
 "portfolio/campaigns/deficit_engine/REALFIBER_PROBE1_REPORT.md": "e861efa53efe9f0b",
 "portfolio/campaigns/deficit_engine/REALFIBER_PROBE2_REPORT.md": "397dc9c98b19a3af",
 "portfolio/campaigns/deficit_engine/REALFIBER_THEOREM.md": "9012084fb845fa70",
}

TERMINAL_ALL_PASS = "ALL_PASS"
BATTERIES = {  # id -> (script_rel, expected_sha16, terminal_line)
 "PA.1": ("portfolio/campaigns/shape_witness/witness_battery.py", "39bed5552c805f4d", TERMINAL_ALL_PASS),
 "PA.2": ("portfolio/campaigns/deficit_engine/wave0_battery.py", "74720504dfd88af7", TERMINAL_ALL_PASS),
 "PA.3": ("portfolio/campaigns/deficit_engine/rowb_mech_battery.py", "cdee40ff26fb262c", TERMINAL_ALL_PASS),
 "PA.4": ("portfolio/campaigns/deficit_engine/realfiber_probe1.py", "7b3b43058ffa0c7c", TERMINAL_ALL_PASS),
 "PA.5": ("portfolio/campaigns/deficit_engine/realfiber_probe2.py", "848b8d8eca916edf", "OUTCOME: INCONCLUSIVE-budget (runs at cap still descending)"),
 "PA.6": ("portfolio/campaigns/deficit_engine/realfiber_path_cert.py", "99fd1859a6e04214", TERMINAL_ALL_PASS),
 "PA.7": ("portfolio/campaigns/deficit_engine/realfiber_fullfiber_cert.py", "dfde6fbde06ee160", TERMINAL_ALL_PASS),
}
WALL_CEILING_S = 1200  # 20 min per run, predecl §8

# -------------------- factored primitives (the E6 exports) --------------------
def sha16_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]

def file_pin(rel: str) -> str:
    with open(os.path.join(REPO_ROOT, rel), "rb") as f:
        return sha16_bytes(f.read())

def records_sha(blob: str) -> str:
    """Canonical records hash for batteries: sha256 over the serialized blob, 16 hex."""
    return hashlib.sha256(blob.encode()).hexdigest()[:16]

class HarnessRefusal(SystemExit):
    def __init__(self, token, detail=""):
        self.token = token; self.detail = detail
        super().__init__(f"REFUSE[{token}] {detail}")

def clause_gate(predecl_path: str, clauses: dict, expected_pin16: str | None):
    """Rule 1.8 gate: every embedded clause must appear verbatim in the frozen predecl."""
    with open(predecl_path, "rb") as f:
        raw = f.read()
    if expected_pin16 is not None and sha16_bytes(raw) != expected_pin16:
        raise HarnessRefusal("PREDECL_PIN_MISMATCH", f"{predecl_path} pin != {expected_pin16}")
    text = raw.decode("utf-8")
    for k, cl in clauses.items():
        if cl not in text:
            raise HarnessRefusal("CLAUSE_DRIFT", f"clause {k} not found verbatim in predecl")

def pin_gate(pins: dict):
    """Rule 1.9 gate: recompute every content pin; refuse on any mismatch."""
    for rel, want in pins.items():
        got = file_pin(rel)
        if got != want:
            raise HarnessRefusal("PIN_MISMATCH", f"{rel}: want {want} got {got}")

def env_fingerprint() -> dict:
    fp = {"python": sys.version.split()[0]}
    try:
        import sympy; fp["sympy"] = sympy.__version__
    except Exception: fp["sympy"] = None
    try:
        import numpy; fp["numpy"] = numpy.__version__
    except Exception: fp["numpy"] = None
    return fp

def run_battery(script_rel: str):
    env = dict(os.environ); env["PYTHONHASHSEED"] = "0"
    t0 = time.time()
    p = subprocess.run([sys.executable, os.path.join(REPO_ROOT, script_rel)],
                       cwd=REPO_ROOT, env=env, capture_output=True, timeout=WALL_CEILING_S)
    return p.stdout, p.returncode, round(time.time() - t0, 2), p.stderr

def parse_run(stdout: bytes, terminal: str):
    text = stdout.decode("utf-8", errors="replace")
    shas = re.findall(r"^RECORDS_SHA256 ([0-9a-f]{16})\s*$", text, flags=re.M)
    lines = [ln for ln in text.splitlines() if ln.strip()]
    last = lines[-1] if lines else ""
    return {"records_sha": shas[-1] if shas else None, "terminal_ok": last == terminal, "last_line": last}

def certify(bid: str, script_rel: str, expected: str, terminal: str) -> dict:
    """Dual-run certification: two independent subprocess runs; verdict per predecl §2."""
    os.makedirs(RECORDS_DIR, exist_ok=True)
    runs = []
    for i in (1, 2):
        out, rc, wall, err = run_battery(script_rel)
        with open(os.path.join(RECORDS_DIR, f"{bid}_run{i}.out"), "wb") as f:
            f.write(out)
        pr = parse_run(out, terminal)
        runs.append({"run": i, "rc": rc, "wall_s": wall, "records_sha": pr["records_sha"],
                     "terminal_ok": pr["terminal_ok"], "last_line": pr["last_line"],
                     "stdout_sha16": sha16_bytes(out),
                     "stderr_tail": err.decode("utf-8", "replace")[-300:] if err else ""})
    s1, s2 = runs[0]["records_sha"], runs[1]["records_sha"]
    ok_run = all(r["rc"] == 0 and r["terminal_ok"] and r["records_sha"] for r in runs)
    if s1 != s2:
        verdict = "NONDET"          # K-A2
    elif not ok_run:
        verdict = "FAIL"            # K-A1
    elif s1 == expected:
        verdict = "PASS"
    else:
        verdict = "REFUSE_MISMATCH" # stable but wrong -> never PASS (K-A1 / PA.8 semantics)
    bundle = {"battery": bid, "script": script_rel, "expected_records_sha": expected,
              "terminal_required": terminal, "runs": runs, "byte_stable_x2": s1 == s2,
              "verdict": verdict, "predecl_pin": PREDECL_PIN16, "env": env_fingerprint()}
    with open(os.path.join(RECORDS_DIR, f"{bid}_bundle.json"), "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=1, sort_keys=True)
    return bundle

# -------------------- controls --------------------
def control_pa8() -> dict:
    """PA.8: wrong expected sha must yield REFUSE_MISMATCH, never PASS."""
    b = certify("PA.8", BATTERIES["PA.6"][0], "0" * 16, TERMINAL_ALL_PASS)
    b["control_pass"] = (b["verdict"] == "REFUSE_MISMATCH")
    with open(os.path.join(RECORDS_DIR, "PA.8_bundle.json"), "w", encoding="utf-8") as f:
        json.dump(b, f, indent=1, sort_keys=True)
    return b

def control_pa9() -> dict:
    """PA.9: byte-altered clause in a predecl copy must refuse with CLAUSE_DRIFT pre-battery."""
    src = os.path.join(REPO_ROOT, PREDECL_REL)
    text = open(src, encoding="utf-8").read()
    tampered = text.replace("39bed5552c805f4d", "39bed5552c805f4e", 1)  # one byte in PA.1's clause
    assert tampered != text
    td = tempfile.mkdtemp(); tp = os.path.join(td, "TAMPERED_PREDECL.md")
    open(tp, "w", encoding="utf-8").write(tampered)
    refused, token = False, None
    try:
        clause_gate(tp, GRADER_CLAUSES, expected_pin16=None)
    except HarnessRefusal as r:
        refused, token = True, r.token
    shutil.rmtree(td, ignore_errors=True)
    b = {"battery": "PA.9", "control_pass": refused and token == "CLAUSE_DRIFT",
         "refused": refused, "token": token, "batteries_run": 0,
         "predecl_pin": PREDECL_PIN16, "env": env_fingerprint()}
    os.makedirs(RECORDS_DIR, exist_ok=True)
    with open(os.path.join(RECORDS_DIR, "PA.9_bundle.json"), "w", encoding="utf-8") as f:
        json.dump(b, f, indent=1, sort_keys=True)
    return b

# -------------------- main --------------------
def gates():
    clause_gate(os.path.join(REPO_ROOT, PREDECL_REL), GRADER_CLAUSES, PREDECL_PIN16)
    pin_gate(CONTENT_PINS)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="PA.k ids, or 'controls'")
    a = ap.parse_args()
    gates()  # both gates fire on EVERY invocation, before anything runs
    print("GATES_GREEN predecl_pin", PREDECL_PIN16, "content_pins", len(CONTENT_PINS))
    for t in a.targets:
        if t == "controls":
            r9 = control_pa9(); print("PA.9", "PASS" if r9["control_pass"] else "FAIL", r9["token"])
            r8 = control_pa8(); print("PA.8", "PASS" if r8["control_pass"] else "FAIL",
                                      "verdict=" + r8["verdict"])
        else:
            script, exp, term = BATTERIES[t]
            b = certify(t, script, exp, term)
            print(t, b["verdict"], "sha", b["runs"][0]["records_sha"], b["runs"][1]["records_sha"],
                  "expected", exp, f"wall {b['runs'][0]['wall_s']}s/{b['runs'][1]['wall_s']}s")

if __name__ == "__main__":
    main()
