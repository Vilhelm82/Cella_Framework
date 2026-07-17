"""
harness.py -- reusable engine for the Block-Verification Contract v1.

Copy this file next to the paper, then write `<paper>_modules.py` that does:

    from harness import module, figure, Result, run_all

    @module("1.7", "1", "Genus claim", "formula", r"g=1+2^{k-2}(k-3)", deps=["3.2"])
    def m_1_7(ctx, deps):
        g = deps["3.2"].value            # CONSUME the premise's verified value
        ok = g == {3: 1, 4: 5, 5: 17, 6: 49}
        return Result("OK" if ok else "FAIL", g, f"genus from Prop 3.3: {g}")

    if __name__ == "__main__":
        import sys, os
        here = os.path.dirname(os.path.abspath(__file__))
        raise SystemExit(run_all(
            title="Paper Title",
            artifact_path=os.path.join(here, "paper_verification.json"),
            figures_dir=os.path.join(here, "figures"),
            make_figures="--figures" in sys.argv,
        ))

Statuses returned by run(): "OK" | "STRUCTURAL" | "SKIP" | "FAIL".
"BLOCKED" is assigned automatically when a premise did not establish.
"""

from __future__ import annotations

import itertools
import json
import os
from dataclasses import dataclass
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Core types
# ---------------------------------------------------------------------------

@dataclass
class Result:
    status: str                     # OK | STRUCTURAL | SKIP | FAIL | BLOCKED
    value: Any = None               # verified output consumed by downstream modules
    detail: str = ""


@dataclass
class MathModule:
    tag: str
    section: str
    title: str
    kind: str                       # definition|formula|theorem|example|structural
    deps: tuple
    latex: str
    run: Callable[[dict, dict], Result]     # run(ctx, dep_results) -> Result
    order: int


@dataclass
class Figure:
    keystone_tag: str               # module whose `figure` field records the path
    title: str
    source_tags: tuple              # verified modules whose .value drives the plot
    filename: str
    build: Callable[[dict, str], None]      # build(results, out_path) -> None
    order: int


REGISTRY: list[MathModule] = []
FIGURES: list[Figure] = []
_ORDER = itertools.count()
_FORDER = itertools.count()


def module(tag, section, title, kind, latex, deps=()):
    """Register one displayed-math block as a DAG node."""
    def deco(fn):
        REGISTRY.append(
            MathModule(tag, section, title, kind, tuple(deps),
                       latex.strip(), fn, next(_ORDER))
        )
        return fn
    return deco


def figure(keystone_tag, title, source_tags, filename):
    """Register a keystone figure. Its data MUST come from results[tag].value
    for tags in `source_tags` -- never hand-typed. Only registered figures the
    user selected should exist in the transcription."""
    def deco(fn):
        FIGURES.append(
            Figure(keystone_tag, title, tuple(source_tags), filename,
                   fn, next(_FORDER))
        )
        return fn
    return deco


# ---------------------------------------------------------------------------
# Status mappings
# ---------------------------------------------------------------------------

SATISFYING = {"OK", "STRUCTURAL", "SKIP"}    # a premise in one of these does not block

BADGE = {"OK": "PASS", "STRUCTURAL": "STRC", "SKIP": "SKIP",
         "FAIL": "FAIL", "BLOCKED": "BLOK"}

CLAIM_STATUS = {                              # contract DAG mapping
    "OK": "machine-verified",
    "STRUCTURAL": "demonstrated",
    "FAIL": "refuted",
    "BLOCKED": "open",
    "SKIP": "open",
}


# ---------------------------------------------------------------------------
# Dependency-order execution
# ---------------------------------------------------------------------------

def topological_order(mods):
    """Kahn's algorithm; document order breaks ties. Raises on unknown dep/cycle."""
    by_tag = {m.tag: m for m in mods}
    for m in mods:
        for dtag in m.deps:
            if dtag not in by_tag:
                raise ValueError(f"module {m.tag!r} depends on unknown {dtag!r}")
    indeg = {m.tag: len(m.deps) for m in mods}
    children = {m.tag: [] for m in mods}
    for m in mods:
        for dtag in m.deps:
            children[dtag].append(m.tag)
    ready = sorted([t for t, n in indeg.items() if n == 0],
                   key=lambda t: by_tag[t].order)
    out = []
    while ready:
        t = ready.pop(0)
        out.append(by_tag[t])
        for ch in children[t]:
            indeg[ch] -= 1
            if indeg[ch] == 0:
                ready.append(ch)
        ready.sort(key=lambda t: by_tag[t].order)
    if len(out) != len(mods):
        stuck = [t for t, n in indeg.items() if n > 0]
        raise ValueError(f"dependency cycle among: {stuck}")
    return out


def _generate_figures(results, records, figures_dir):
    if not FIGURES:
        return
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # noqa: F401  (available to build fns)
    except Exception as exc:
        print(f"[fig] matplotlib unavailable ({exc!r}); skipping figures")
        return
    os.makedirs(figures_dir, exist_ok=True)
    rec_by_tag = {r["tag"]: r for r in records}
    for fig in sorted(FIGURES, key=lambda f: f.order):
        unverified = [t for t in fig.source_tags
                      if results.get(t) is None
                      or results[t].status not in ("OK", "STRUCTURAL")]
        if unverified:
            print(f"[fig-skip] {fig.filename}: unverified source(s) {unverified}")
            continue
        path = os.path.join(figures_dir, fig.filename)
        fig.build(results, path)
        if fig.keystone_tag in rec_by_tag:
            rec_by_tag[fig.keystone_tag]["figure"] = path
        print(f"[fig] {fig.title} -> {path}")


def run_all(*, title, artifact_path, figures_dir=None, make_figures=False):
    """Execute all registered modules in dependency order, print the report,
    write the JSON artifact, optionally build selected keystone figures.
    Returns a shell exit code (0 = clean, 1 = any FAIL or BLOCKED)."""
    ctx = {}
    order = topological_order(REGISTRY)
    results, records = {}, []
    width = 90

    print("=" * width)
    print(title)
    print("Block-Verification Contract v1 -- proof-DAG (dependency order)".center(width))
    print("=" * width)

    tally = {k: 0 for k in ("OK", "STRUCTURAL", "SKIP", "FAIL", "BLOCKED")}
    failures, blocked = [], []

    for m in order:
        dep_results = {t: results[t] for t in m.deps}
        blockers = [t for t, r in dep_results.items() if r.status not in SATISFYING]
        if blockers:
            res = Result("BLOCKED", None,
                         f"blocked by unproven premise(s): {', '.join(blockers)}")
        else:
            try:
                res = m.run(ctx, dep_results)
            except Exception as exc:
                res = Result("FAIL", None, f"exception: {exc!r}")
        results[m.tag] = res
        tally[res.status] = tally.get(res.status, 0) + 1
        if res.status == "FAIL":
            failures.append(f"({m.tag}) {m.title}: {res.detail}")
        if res.status == "BLOCKED":
            blocked.append(f"({m.tag}) {m.title}: {res.detail}")

        records.append({
            "tag": m.tag,
            "section": m.section,
            "kind": m.kind,
            "latex": m.latex,
            "depends_on": list(m.deps),
            "status": "PASS" if res.status == "OK" else res.status,
            "claim_status": CLAIM_STATUS[res.status],
            "detail": res.detail,
            "figure": None,
        })

        dep_str = (" <= " + ", ".join(m.deps)) if m.deps else " (axiom/base)"
        print(f"[{BADGE[res.status]}] ({m.tag:<7}) {m.title}{dep_str}")
        if res.detail:
            print(f"         {res.detail}")

    if make_figures and figures_dir:
        print("-" * width)
        _generate_figures(results, records, figures_dir)

    print("=" * width)
    print(f"Modules: {len(order)}   PASS={tally['OK']}  STRUCTURAL={tally['STRUCTURAL']}"
          f"  SKIP={tally['SKIP']}  BLOCKED={tally['BLOCKED']}  FAIL={tally['FAIL']}")
    if blocked:
        print("\nBLOCKED (premise not established):")
        for b in blocked:
            print("  -", b)
    if failures:
        print("\nFAILURES (code disagrees with prose -- flag prose stale):")
        for f in failures:
            print("  -", f)

    with open(artifact_path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=2, ensure_ascii=False)
    print(f"\nJSON artifact ({len(records)} module nodes) -> {artifact_path}")
    print("=" * width)
    return 1 if (failures or blocked) else 0
