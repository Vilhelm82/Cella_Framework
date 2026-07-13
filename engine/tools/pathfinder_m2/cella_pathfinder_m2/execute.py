"""External M2 process execution and exact output parsing."""

from __future__ import annotations

import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class M2Execution:
    wall_ns: int
    peak_rss_kb: int
    stdout: str
    stderr: str
    canonical_generators: tuple[str, ...]
    certificate_status: str | None
    execution_cpu_seconds: float | None
    certificate_cpu_seconds: float | None


class M2ExecutionError(RuntimeError):
    pass


def _marker(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}=(.+)$", text, re.MULTILINE)
    return None if match is None else match.group(1).strip()


def _result_block(text: str, begin: str, end: str) -> str:
    match = re.search(re.escape(begin) + r"\s*(.*?)\s*" + re.escape(end), text, re.DOTALL)
    if match is None:
        raise M2ExecutionError(f"M2 output omitted result block {begin!r}")
    return match.group(1).strip()


def canonicalize_generators(matrix_text: str) -> tuple[str, ...]:
    match = re.search(r"matrix\s*\{\{(.*?)\}\}", matrix_text, re.DOTALL)
    if match is None:
        raise M2ExecutionError(f"unsupported M2 generator presentation: {matrix_text!r}")
    generators = tuple(part.strip().replace(" ", "") for part in match.group(1).split(","))
    if not generators or any(not item for item in generators):
        raise M2ExecutionError("empty generator in M2 presentation")
    return tuple(sorted(generators))


def run_m2_script(
    script: str,
    *,
    script_path: Path,
    result_markers: tuple[str, str],
) -> M2Execution:
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(script)
    command = ["/usr/bin/time", "-f", "PATHFINDER_PEAK_RSS_KB=%M", "M2", "--script", str(script_path)]
    environment = dict(os.environ)
    environment["LC_ALL"] = "C"
    started = time.perf_counter_ns()
    completed = subprocess.run(command, capture_output=True, text=True, env=environment, check=False)
    wall_ns = time.perf_counter_ns() - started
    if completed.returncode != 0:
        raise M2ExecutionError(
            f"M2 exited {completed.returncode} for {script_path}\n{completed.stdout}\n{completed.stderr}"
        )
    rss_text = _marker(completed.stderr, "PATHFINDER_PEAK_RSS_KB")
    if rss_text is None:
        raise M2ExecutionError("/usr/bin/time omitted peak RSS")
    result_text = _result_block(completed.stdout, *result_markers)
    exec_cpu = _marker(completed.stdout, "PATHFINDER_M2_EXEC_CPU_SECONDS")
    cert_cpu = _marker(completed.stdout, "PATHFINDER_M2_CERT_CPU_SECONDS")
    return M2Execution(
        wall_ns=wall_ns,
        peak_rss_kb=int(rss_text),
        stdout=completed.stdout,
        stderr=completed.stderr,
        canonical_generators=canonicalize_generators(result_text),
        certificate_status=_marker(completed.stdout, "PATHFINDER_M2_CERTIFICATE"),
        execution_cpu_seconds=None if exec_cpu is None else float(exec_cpu),
        certificate_cpu_seconds=None if cert_cpu is None else float(cert_cpu),
    )
