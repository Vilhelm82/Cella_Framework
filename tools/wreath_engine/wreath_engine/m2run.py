"""Batch execution of generated Macaulay2 scripts and result-block parsing."""

from __future__ import annotations

import json
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

from .spec import ProblemSpec

FENCE_BEGIN = "-----BEGIN WREATH RESULT-----"
FENCE_END = "-----END WREATH RESULT-----"

DEFAULT_TIMEOUT = 3600.0


class M2Error(RuntimeError):
    def __init__(self, message: str, log_tail: str = "", script: str = ""):
        super().__init__(message)
        self.log_tail = log_tail
        self.script = script


@dataclass
class M2Result:
    returncode: int
    script_path: Path
    output_path: Path
    results: list[dict] = field(default_factory=list)
    elapsed: float = 0.0

    @property
    def log_tail(self) -> str:
        try:
            text = self.output_path.read_text()
        except OSError:
            return ""
        return "\n".join(text.splitlines()[-50:])


def parse_results(text: str) -> list[dict]:
    out = []
    for block in re.findall(
        re.escape(FENCE_BEGIN) + r"\n(.*?)\n" + re.escape(FENCE_END), text, re.S
    ):
        out.append(json.loads(block))
    return out


def runs_root(explicit: str | None = None) -> Path:
    root = Path(explicit) if explicit else Path(__file__).resolve().parent.parent / "runs"
    root.mkdir(parents=True, exist_ok=True)
    return root


def new_run_dir(ps: ProblemSpec, purpose: str, root: Path | None = None) -> Path:
    root = root if root is not None else runs_root()
    stamp = time.strftime("%Y%m%dT%H%M%S")
    run_dir = root / f"{stamp}_{ps.name}_{purpose}_{ps.content_hash()}"
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "spec.json").write_text(json.dumps(ps.raw, indent=2))
    return run_dir


def run_script(script_text: str, run_dir: Path, name: str,
               timeout: float = DEFAULT_TIMEOUT) -> M2Result:
    """Write the script under run_dir, execute M2 --script, parse fences.

    Scripts must be real files: M2 --script cannot read process-substitution
    paths. Stdout and stderr are merged and saved verbatim as the audit log.
    """
    script_path = run_dir / f"{name}.m2"
    output_path = run_dir / f"{name}.out.txt"
    script_path.write_text(script_text)
    start = time.monotonic()
    try:
        proc = subprocess.run(
            ["M2", "--script", str(script_path)],
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        partial = (exc.stdout or "") + (exc.stderr or "")
        output_path.write_text(partial + f"\n[wreath-engine] TIMEOUT after {timeout}s\n")
        raise M2Error(f"M2 timed out after {timeout}s", log_tail=partial[-2000:],
                      script=str(script_path)) from exc
    except FileNotFoundError as exc:
        raise M2Error("M2 executable not found on PATH") from exc
    elapsed = time.monotonic() - start
    output_path.write_text(proc.stdout + (("\n--- stderr ---\n" + proc.stderr) if proc.stderr else ""))
    result = M2Result(proc.returncode, script_path, output_path,
                      parse_results(proc.stdout), elapsed)
    if proc.returncode != 0:
        raise M2Error(
            f"M2 exited with code {proc.returncode} (script kept at {script_path})",
            log_tail=result.log_tail, script=str(script_path),
        )
    return result
