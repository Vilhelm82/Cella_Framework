#!/usr/bin/env python3
"""
validate_agent_artifact.py — evidence gate for V4 agent-produced results.

Enforces the Acceptance Criteria of TASK_TEMPLATE_hardened.md against a
result.json emitted by a CLI agent (Grok, Codex, Claude Code). It trusts
nothing the agent asserts: it checks the schema, confirms scope compliance and
the retrodiction gate, then independently RE-RUNS each generating script and
diffs its raw output byte-for-byte. A confabulated value will not reproduce.

Stdlib only. Exit code 0 = all gates pass (artifact admissible); 1 = at least
one gate failed (artifact bounced — nothing enters the record).

Usage:
    python validate_agent_artifact.py scratch/<slug>/result.json
    python validate_agent_artifact.py scratch/<slug>/result.json --skip-rerun
    python validate_agent_artifact.py scratch/<slug>/result.json --python python3
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REQUIRED_TOP = ["task_id", "campaign", "producer", "retrodiction_gate",
                "claims", "scope_compliance", "not_established"]
REQUIRED_CLAIM = ["claim_id", "statement", "kind", "status", "confidence",
                  "value", "generating_script", "raw_output", "byte_stable",
                  "derivation", "falsifier", "axiom_smuggling_check"]
VALID_KIND = {"measured", "inferred"}
VALID_STATUS = {"PROVEN", "PARTIAL", "OPEN", "REFUTED"}
SCOPE_FLAGS = ["touched_substrate", "touched_normative_docs", "wrote_canonical_record"]


class Report:
    def __init__(self):
        self.checks = []  # list of (ok, label, detail)

    def add(self, ok, label, detail=""):
        self.checks.append((bool(ok), label, detail))

    @property
    def passed(self):
        return all(ok for ok, _, _ in self.checks)

    def render(self):
        out = []
        for ok, label, detail in self.checks:
            line = f"[{'PASS' if ok else 'FAIL'}] {label}"
            if detail:
                line += f"  -- {detail}"
            out.append(line)
        out.append("")
        out.append("RESULT: " + ("PASS -- artifact admissible"
                                 if self.passed
                                 else "FAIL -- artifact bounced; nothing enters the record"))
        return "\n".join(out)


def is_blank(v):
    return v is None or (isinstance(v, str) and v.strip() == "")


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(base: Path, rel: str) -> Path:
    p = Path(rel)
    return p if p.is_absolute() else (base / p)


def validate(result_path: Path, do_rerun: bool, python: str) -> Report:
    r = Report()
    try:
        data = json.loads(result_path.read_text())
    except Exception as e:
        r.add(False, "result.json parses as JSON", str(e))
        return r
    r.add(True, "result.json parses as JSON")
    base = result_path.parent

    # Top-level schema
    for k in REQUIRED_TOP:
        r.add(k in data, f"top-level key present: {k}")

    ne = data.get("not_established")
    r.add(isinstance(ne, list) and len(ne) > 0,
          "not_established is a non-empty list",
          "honesty gate: every run must state what it did NOT settle")

    # Scope compliance -- all must be explicitly false
    sc = data.get("scope_compliance", {})
    for k in SCOPE_FLAGS:
        r.add(sc.get(k) is False, f"scope_compliance.{k} is false",
              "agent stays in scratch/worktree; record writes are reviewer-only")

    # Retrodiction gate
    rg = data.get("retrodiction_gate", {})
    r.add(rg.get("passed") is True, "retrodiction_gate.passed is true")
    ev = rg.get("evidence_path")
    if is_blank(ev):
        r.add(False, "retrodiction_gate.evidence_path present")
    else:
        r.add(resolve(base, ev).exists(), "retrodiction evidence file exists", str(ev))

    # Claims
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        r.add(False, "claims is a non-empty list")
        return r
    r.add(True, "claims is a non-empty list", f"{len(claims)} claim(s)")

    for i, c in enumerate(claims):
        cid = c.get("claim_id", f"#{i}")

        # Required fields present and non-blank (an honest 'UNKNOWN' is allowed;
        # an empty/missing field is not).
        for f in REQUIRED_CLAIM:
            r.add(f in c and not is_blank(c.get(f)),
                  f"[{cid}] field present & non-blank: {f}")

        r.add(c.get("kind") in VALID_KIND,
              f"[{cid}] kind valid", str(c.get("kind")))
        r.add(c.get("status") in VALID_STATUS,
              f"[{cid}] status valid", str(c.get("status")))

        d = c.get("derivation")
        if not is_blank(d) and str(d).endswith(".md"):
            r.add(resolve(base, d).exists(), f"[{cid}] derivation file exists", str(d))

        asc = str(c.get("axiom_smuggling_check", ""))
        r.add("derived from spec+axioms only" in asc or asc.lower().startswith("flagged"),
              f"[{cid}] axiom_smuggling_check clean or explicitly flagged", asc)

        # Byte-stable re-run -- the load-bearing gate. measured claims only.
        if c.get("kind") == "measured":
            script, rawout = c.get("generating_script"), c.get("raw_output")
            if is_blank(script) or is_blank(rawout):
                r.add(False, f"[{cid}] has generating_script + raw_output")
                continue
            spath, rpath = resolve(base, script), resolve(base, rawout)
            if not spath.exists():
                r.add(False, f"[{cid}] generating_script exists", str(script))
                continue
            if not rpath.exists():
                r.add(False, f"[{cid}] raw_output exists before re-run", str(rawout))
                continue
            if not do_rerun:
                r.add(c.get("byte_stable") is True,
                      f"[{cid}] byte_stable flag set (re-run skipped)",
                      "TRUST NOT VERIFIED -- drop --skip-rerun to enforce")
                continue
            h0 = sha256(rpath)
            try:
                proc = subprocess.run([python, str(spath)], cwd=str(spath.parent),
                                      capture_output=True, timeout=600)
            except Exception as e:
                r.add(False, f"[{cid}] generating_script re-ran without error", str(e))
                continue
            if proc.returncode != 0:
                tail = proc.stderr.decode("utf-8", "replace")[-300:]
                r.add(False, f"[{cid}] generating_script exits 0", tail)
                continue
            h1 = sha256(rpath)
            r.add(h0 == h1,
                  f"[{cid}] raw_output reproduces byte-for-byte on re-run",
                  "" if h0 == h1 else f"hash {h0[:12]} -> {h1[:12]}")
    return r


def main():
    ap = argparse.ArgumentParser(
        description="Evidence gate for V4 agent result.json artifacts.")
    ap.add_argument("result", type=Path, help="path to result.json")
    ap.add_argument("--skip-rerun", action="store_true",
                    help="schema-only; do NOT re-run scripts (faster, weaker)")
    ap.add_argument("--python", default=(sys.executable or "python3"),
                    help="interpreter used to re-run generating scripts")
    args = ap.parse_args()

    if not args.result.exists():
        print(f"[FAIL] result file not found: {args.result}")
        sys.exit(1)

    report = validate(args.result, do_rerun=not args.skip_rerun, python=args.python)
    print(report.render())
    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
