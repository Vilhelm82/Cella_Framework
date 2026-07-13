"""Job child process: runs one pipeline call and writes the envelope to --out."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import pipeline
from .spec import validate


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--kind", required=True,
                    choices=["verify", "realize", "realize_full", "explore"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=float, default=3600.0)
    ap.add_argument("--root", default=None)
    ap.add_argument("--extra", default=None)
    args = ap.parse_args()

    ps = validate(json.loads(Path(args.spec).read_text()))
    root = Path(args.root) if args.root else None
    extra = json.loads(args.extra) if args.extra else {}

    if args.kind == "verify":
        env = pipeline.verify_valuation_matrix(ps, root, timeout=args.timeout)
    elif args.kind == "realize":
        env = pipeline.realize_branch_poset(ps, root, include_decompositions=False,
                                            timeout=args.timeout)
    elif args.kind == "realize_full":
        env = pipeline.realize_branch_poset(ps, root, include_decompositions=True,
                                            timeout=args.timeout)
    else:
        env = pipeline.suggest_parity_rows(ps, extra.get("divisor_gens", []),
                                           root, timeout=args.timeout)

    Path(args.out).write_text(json.dumps(env, indent=2))
    return 0 if env.get("status") != "error" else 1


if __name__ == "__main__":
    sys.exit(main())
