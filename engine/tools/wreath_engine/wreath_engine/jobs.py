"""Async job manager for long M2 computations (decompositions, full verifies).

Each job is an independent OS process running `python -m wreath_engine.jobrun`;
the registry lives at <runs_root>/jobs.json. Cancel kills the process group,
which takes the M2 subprocess down with it.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

from . import m2run
from .spec import ProblemSpec

JOB_KINDS = ("verify", "realize", "realize_full", "explore")


def _jobs_dir(root: Path | None = None) -> Path:
    d = m2run.runs_root(str(root) if root else None) / "jobs"
    d.mkdir(exist_ok=True)
    return d


def _registry_path(root: Path | None = None) -> Path:
    return _jobs_dir(root) / "jobs.json"


def _read_registry(root: Path | None = None) -> dict:
    path = _registry_path(root)
    if path.exists():
        return json.loads(path.read_text())
    return {}


def _write_registry(reg: dict, root: Path | None = None) -> None:
    _registry_path(root).write_text(json.dumps(reg, indent=2))


def start_job(ps: ProblemSpec, kind: str, root: Path | None = None,
              timeout: float = m2run.DEFAULT_TIMEOUT,
              extra: dict | None = None) -> dict:
    if kind not in JOB_KINDS:
        return {"status": "error", "error": f"unknown job kind {kind!r}"}
    job_id = f"job_{time.strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:6]}"
    jdir = _jobs_dir(root)
    spec_path = jdir / f"{job_id}.spec.json"
    spec_path.write_text(json.dumps(ps.raw))
    out_path = jdir / f"{job_id}.result.json"
    log_path = jdir / f"{job_id}.log"
    cmd = [sys.executable, "-m", "wreath_engine.jobrun",
           "--spec", str(spec_path), "--kind", kind,
           "--out", str(out_path), "--timeout", str(timeout)]
    if root:
        cmd += ["--root", str(root)]
    if extra:
        cmd += ["--extra", json.dumps(extra)]
    with open(log_path, "w") as log:
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                                start_new_session=True)
    reg = _read_registry(root)
    reg[job_id] = {"pid": proc.pid, "kind": kind, "spec": ps.name,
                   "spec_hash": ps.content_hash(), "state": "running",
                   "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "out": str(out_path), "log": str(log_path)}
    _write_registry(reg, root)
    return {"status": "certified", "job_id": job_id, "pid": proc.pid,
            "kind": kind}


def _pid_running(pid: int) -> bool:
    """True only for a live, non-zombie process. A finished child that has
    not been reaped by its parent is a zombie: os.kill(pid, 0) still succeeds
    on it, so we must read the process state from /proc."""
    try:
        with open(f"/proc/{pid}/stat") as f:
            state = f.read().rsplit(") ", 1)[-1].split()[0]
        return state != "Z"
    except OSError:
        return False


def _refresh(job_id: str, reg: dict, root: Path | None = None) -> dict:
    entry = reg[job_id]
    if entry["state"] == "running":
        try:  # reap if we happen to be the parent; harmless otherwise
            os.waitpid(entry["pid"], os.WNOHANG)
        except (ChildProcessError, OSError):
            pass
        if Path(entry["out"]).exists():
            entry["state"] = "done"
            _write_registry(reg, root)
        elif not _pid_running(entry["pid"]):
            entry["state"] = "failed"
            _write_registry(reg, root)
    return entry


def job_status(job_id: str, root: Path | None = None) -> dict:
    reg = _read_registry(root)
    if job_id not in reg:
        return {"status": "error", "error": f"unknown job {job_id}"}
    entry = _refresh(job_id, reg, root)
    out = {"status": "certified", "job_id": job_id, "state": entry["state"],
           "kind": entry["kind"], "spec": entry["spec"],
           "started": entry["started"]}
    if entry["state"] in ("failed",):
        try:
            out["log_tail"] = "\n".join(
                Path(entry["log"]).read_text().splitlines()[-30:])
        except OSError:
            pass
    return out


def job_result(job_id: str, root: Path | None = None) -> dict:
    reg = _read_registry(root)
    if job_id not in reg:
        return {"status": "error", "error": f"unknown job {job_id}"}
    entry = _refresh(job_id, reg, root)
    if entry["state"] == "running":
        return {"status": "error", "error": "job still running",
                "job_id": job_id, "state": "running"}
    out_path = Path(entry["out"])
    if not out_path.exists():
        tail = ""
        try:
            tail = "\n".join(Path(entry["log"]).read_text().splitlines()[-30:])
        except OSError:
            pass
        return {"status": "error", "error": "job produced no result",
                "job_id": job_id, "state": entry["state"], "log_tail": tail}
    return json.loads(out_path.read_text())


def cancel_job(job_id: str, root: Path | None = None) -> dict:
    reg = _read_registry(root)
    if job_id not in reg:
        return {"status": "error", "error": f"unknown job {job_id}"}
    entry = reg[job_id]
    if entry["state"] != "running":
        return {"status": "certified", "job_id": job_id,
                "state": entry["state"], "note": "job was not running"}
    try:
        pgid = os.getpgid(entry["pid"])
        os.killpg(pgid, signal.SIGTERM)
        time.sleep(1.0)
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    except ProcessLookupError:
        pass
    entry["state"] = "cancelled"
    _write_registry(reg, root)
    return {"status": "certified", "job_id": job_id, "state": "cancelled"}


def list_jobs(root: Path | None = None) -> dict:
    reg = _read_registry(root)
    for job_id in reg:
        _refresh(job_id, reg, root)
    return {"status": "certified",
            "jobs": [{"job_id": k, **{kk: vv for kk, vv in v.items()
                                      if kk in ("kind", "spec", "state", "started")}}
                     for k, v in sorted(reg.items())]}
