"""Persistent Macaulay2 session for exploratory tools.

Used only by suggest_parity_rows for responsiveness; nothing that flows into a
certificate ever runs here. If the session wedges it is killed and the caller
falls back to a batch run.
"""

from __future__ import annotations

import subprocess
import threading
import time

from . import m2run

SENTINEL = "<<WREATH-SESSION-DONE>>"


class M2Session:
    def __init__(self):
        self._proc: subprocess.Popen | None = None
        self._lock = threading.Lock()

    def _ensure(self) -> subprocess.Popen:
        if self._proc is None or self._proc.poll() is not None:
            self._proc = subprocess.Popen(
                ["M2", "--no-readline", "-q"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, bufsize=1,
            )
        return self._proc

    def run(self, script_text: str, timeout: float = 600.0) -> list[dict]:
        """Feed a script, read until the sentinel, return parsed result blocks.

        Raises M2Error on timeout or a dead session (after killing it).
        """
        with self._lock:
            proc = self._ensure()
            assert proc.stdin is not None and proc.stdout is not None
            proc.stdin.write(script_text + f'\nprint "{SENTINEL}";\n')
            proc.stdin.flush()
            lines: list[str] = []
            deadline = time.monotonic() + timeout
            result: list[str] = []
            done = threading.Event()

            def reader():
                for line in proc.stdout:  # type: ignore[union-attr]
                    if SENTINEL in line:
                        done.set()
                        return
                    result.append(line)
                done.set()

            t = threading.Thread(target=reader, daemon=True)
            t.start()
            while not done.is_set():
                if time.monotonic() > deadline:
                    self.kill()
                    raise m2run.M2Error(
                        f"exploratory session timed out after {timeout}s; "
                        "session killed", log_tail="".join(result[-30:]))
                time.sleep(0.1)
            if proc.poll() is not None and not result:
                self.kill()
                raise m2run.M2Error("exploratory session died",
                                    log_tail="".join(lines[-30:]))
            return m2run.parse_results("".join(result))

    def kill(self) -> None:
        if self._proc is not None:
            try:
                self._proc.kill()
            except OSError:
                pass
            self._proc = None


_session: M2Session | None = None


def shared_session() -> M2Session:
    global _session
    if _session is None:
        _session = M2Session()
    return _session
