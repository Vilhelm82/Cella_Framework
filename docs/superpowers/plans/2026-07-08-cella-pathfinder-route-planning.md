# Cella Pathfinder Route Planning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Cella pathfinder layer that turns one expression into a route decision, generates conservative rewrite candidates, and ranks declared forms by exact-account/BACL burden.

**Architecture:** Add a focused `src/cella/pathfinder.py` module that consumes `residual_profile` and `cleanliness_rank`. Keep `mcp_server.py` as thin wiring. Add one gate file for route planning, rewrite generation, ranking, and router exposure.

**Tech Stack:** Python stdlib `ast`, `fractions`, existing Cella telemetry wrapper, existing `residual_profile.py`, existing BACL/refinery tools in `cleanliness.py`, MCP surface in `mcp_server.py`.

---

## File Structure

- Create `src/cella/pathfinder.py`
  - Owns route decisions, conservative rewrite generation, and pathfinder comparison.
  - Depends on `residual_profile.residual_profile` and `cleanliness.cleanliness_rank`.
  - Does not own MCP serialization.
- Modify `src/cella/mcp_server.py`
  - Imports pathfinder functions.
  - Adds wrappers: `call_route_plan`, `call_rewrite_candidates`, `call_pathfinder_compare`.
  - Adds help records and pathfinder profile entries.
- Create `tests/gate_mcp_pathfinder.py`
  - Pins route decisions, candidate output, comparison ranking, and router dispatch.
- Modify `tests/gate_mcp.py`
  - Adds new tool names to the exact MCP surface check.
- Modify `tests/gate_mcp_profiles.py`
  - Adds new tools to `TOOL_GROUPS["pathfinder"]` expectation.

Use precise `git add` commands for commits. The repository may contain existing untracked files from earlier Cella work; do not sweep unrelated files into commits.

---

### Task 1: Route Planner Failing Gate

**Files:**
- Create: `tests/gate_mcp_pathfinder.py`

- [ ] **Step 1: Write the failing test**

Create `tests/gate_mcp_pathfinder.py`:

```python
"""Gate MCP pathfinder route planning.

Run:  python tests/gate_mcp_pathfinder.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


try:
    from cella.mcp_server import (
        TOOL_GROUPS,
        TOOL_NAMES,
        call_route_plan,
    )
except Exception as exc:
    print(f"GATE MCP PATHFINDER: OPEN - import failed: {exc}")
    sys.exit(1)


def route(expression, constants=None):
    return call_route_plan(
        expression=expression,
        sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
        constants=constants,
    )


linear = route("(1 + eps) - 1")
check("PTH1 catastrophic same-leading-constant expression requests rewrite candidates",
      linear["ok"]
      and linear["value"]["decision"] == "rewrite_candidate_needed"
      and linear["value"]["operation_shape"] == "catastrophic_cancellation"
      and linear["value"]["exact_account_available"] is True
      and "cella_rewrite_candidates" in linear["value"]["next_tools"])

self_cancel = route("eps - eps")
check("PTH2 structural self-cancellation routes to symbolic collapse",
      self_cancel["ok"]
      and self_cancel["value"]["decision"] == "collapse_symbolically"
      and self_cancel["value"]["route_confidence"] == "high"
      and "cella_symbolic_rational" in self_cancel["value"]["next_tools"])

unknown = route("(A + eps) - A")
check("PTH3 missing constants are surfaced as blocking inputs",
      unknown["ok"]
      and unknown["value"]["decision"] == "needs_declared_constants"
      and "A" in unknown["value"]["blocking_inputs"]["missing_constants"])

benign = route("(1 + sqrt(eps)) - 1")
check("PTH4 benign cancellation remains direct but asks for BACL monitoring",
      benign["ok"]
      and benign["value"]["decision"] == "direct_ok"
      and benign["value"]["dominant_pattern"] == "sterbenz_safe_benign"
      and "cella_bacl_pair" in benign["value"]["next_tools"])

print()
if FAILS:
    print(f"GATE MCP PATHFINDER: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP PATHFINDER: CLOSED - route planner, candidates, and comparison are MCP-callable.")
sys.exit(0)
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
```

Expected: import failure for missing `call_route_plan`.

### Task 2: Implement Route Planner Core

**Files:**
- Create: `src/cella/pathfinder.py`
- Test: `tests/gate_mcp_pathfinder.py`

- [ ] **Step 1: Add the pathfinder module with route planning**

Create `src/cella/pathfinder.py`:

```python
"""Cella pathfinder route planning and conservative rewrite support."""

from __future__ import annotations

import ast
from fractions import Fraction

from .cleanliness import cleanliness_rank
from .residual_profile import residual_profile


def route_plan(
    expression: str,
    sweep: dict,
    constants: dict | None = None,
    include_profile: bool = False,
    include_samples: bool = False,
) -> dict:
    try:
        profile = residual_profile(
            str(expression),
            sweep,
            constants=constants or {},
            include_samples=include_samples,
        )
    except Exception as exc:
        return {
            "expression": str(expression),
            "decision": "unsupported_shape",
            "why": f"Residual profile could not parse or probe the expression: {exc}",
            "operation_shape": None,
            "dominant_pattern": None,
            "exact_account_available": False,
            "blocking_inputs": {"unsupported": str(exc), "missing_constants": []},
            "next_tools": ["cella_help"],
            "route_confidence": "low",
            "profile_summary": {},
        }

    sites = list(profile.get("danger_sites", []))
    burden = dict(profile.get("predicted_burden_vector", {}))
    operation_shape = str(profile.get("operation_shape"))
    dominant = burden.get("dominant_pattern")
    missing = _missing_constants(sites)
    exact_account = _has_exact_account(sites)
    known_rewrite = _has_known_rewrite(str(expression), operation_shape)

    if missing:
        decision = "needs_declared_constants"
        why = "At least one subtraction site contains an unknown symbolic parameter."
        next_tools = ["cella_route_plan"]
        confidence = "high"
    elif operation_shape == "no_subtraction":
        decision = "direct_ok"
        why = "No subtraction site was detected."
        next_tools = ["cella_symbolic_rational", "cella_arith_precision_budget"]
        confidence = "high"
    elif operation_shape == "self_cancellation":
        decision = "collapse_symbolically"
        why = "A structural x-x site can be collapsed before arithmetic."
        next_tools = ["cella_symbolic_rational", "cella_symbolic_equal"]
        confidence = "high"
    elif operation_shape == "catastrophic_cancellation" and known_rewrite:
        decision = "rewrite_candidate_needed"
        why = "Catastrophic same-leading-constant cancellation has at least one conservative rewrite family."
        next_tools = ["cella_rewrite_candidates", "cella_pathfinder_compare"]
        confidence = "high" if exact_account else "medium"
    elif operation_shape == "catastrophic_cancellation":
        decision = "precision_budget_needed"
        why = "Catastrophic cancellation was detected but no conservative rewrite family was found."
        next_tools = ["cella_arith_precision_budget", "cella_operand_residue_trace"]
        confidence = "medium"
    elif operation_shape == "benign_cancellation":
        decision = "direct_ok"
        why = "Cancellation opens with a benign fractional signal; monitor BACL/account burden."
        next_tools = ["cella_bacl_pair", "cella_operand_residue_trace"]
        confidence = "medium"
    elif operation_shape == "partly_unrecognised":
        decision = "unsupported_shape"
        why = "At least one subtraction site could not be classified."
        next_tools = ["cella_operand_residue_trace", "cella_help"]
        confidence = "low"
    else:
        decision = "direct_ok"
        why = "No high-risk cancellation route was detected."
        next_tools = ["cella_arith_precision_budget"]
        confidence = "medium"

    out = {
        "expression": str(expression),
        "decision": decision,
        "why": why,
        "operation_shape": operation_shape,
        "dominant_pattern": dominant,
        "exact_account_available": exact_account,
        "blocking_inputs": {"missing_constants": missing},
        "next_tools": next_tools,
        "route_confidence": confidence,
        "profile_summary": {
            "site_count": len(sites),
            "danger_sites": [
                {
                    "path": site.get("path"),
                    "pattern": site.get("pattern"),
                    "severity": site.get("severity"),
                    "signal_exponent": site.get("signal_exponent"),
                    "account_probe_status": site.get("account_probe_status"),
                }
                for site in sites
            ],
            "predicted_burden_vector": burden,
        },
    }
    if include_profile:
        out["profile"] = profile
    return out


def _has_exact_account(sites: list[dict]) -> bool:
    for site in sites:
        if site.get("account_probe_status") == "exact_q_account":
            return True
        for sample in site.get("probe_samples", []):
            if sample.get("exact_account", {}).get("status") == "exact_q_account":
                return True
    return False


def _missing_constants(sites: list[dict]) -> list[str]:
    missing = set()
    marker = "unknown parameter "
    for site in sites:
        text = str(site.get("probe_error", ""))
        if marker in text:
            name = text.split(marker, 1)[1].split(";", 1)[0].strip().strip("'\"")
            if name:
                missing.add(name)
    return sorted(missing)


def _has_known_rewrite(expression: str, operation_shape: str) -> bool:
    if operation_shape == "self_cancellation":
        return True
    if operation_shape != "catastrophic_cancellation":
        return False
    return bool(rewrite_candidates(expression).get("candidates"))
```

- [ ] **Step 2: Run test to verify it still fails on MCP wiring**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
```

Expected: import failure still exists because MCP call wrappers are not wired yet.

### Task 3: Wire `cella_route_plan` into MCP

**Files:**
- Modify: `src/cella/mcp_server.py`
- Modify: `tests/gate_mcp.py`
- Modify: `tests/gate_mcp_profiles.py`
- Test: `tests/gate_mcp_pathfinder.py`

- [ ] **Step 1: Add imports and wrapper**

In `src/cella/mcp_server.py`, add:

```python
from .pathfinder import (
    pathfinder_compare,
    rewrite_candidates,
    route_plan,
)
```

Add wrapper:

```python
def call_route_plan(
    expression: str,
    sweep: dict,
    constants: dict | None = None,
    include_profile: bool = False,
    include_samples: bool = False,
) -> dict:
    """Plan the next Cella route for one expression."""
    return _wrap_telemetry(
        "cella_route_plan",
        "Cella pathfinder route plan for one expression.",
        lambda: route_plan(
            str(expression),
            sweep,
            constants=constants or {},
            include_profile=bool(include_profile),
            include_samples=bool(include_samples),
        ),
        depends=(
            "Route planning consumes residual-profile telemetry and exact-account probes when available.",
            "The decision names the next process; it is not a global symbolic equivalence proof.",
        ),
    )
```

- [ ] **Step 2: Add tool name and callable map**

Add `"cella_route_plan"` to `TOOL_NAMES` near `cella_residual_profile`.

Add `"cella_route_plan"` to `TOOL_GROUPS["pathfinder"]` immediately after `"cella_residual_profile"`.

Add to `tool_callable_map()`:

```python
"cella_route_plan": call_route_plan,
```

- [ ] **Step 3: Add help text**

Add `_HELP_TOOLS["cella_route_plan"]`:

```python
"cella_route_plan": {
    "purpose": "Choose the next Cella process for one expression before expensive symbolic or numeric work.",
    "inputs": "expression, sweep, optional constants, include_profile, include_samples.",
    "proper_use": "Call first in the pathfinder workflow after drafting an expression.",
    "read_result": "decision is the action label; next_tools is the ordered follow-up; profile_summary explains the cancellation/account evidence.",
    "pitfalls": "This chooses a route. It does not prove global algebraic equivalence.",
},
```

- [ ] **Step 4: Update profile and tool-name tests**

In `tests/gate_mcp.py`, add `"cella_route_plan"` to the expected `TOOL_NAMES` set.

In `tests/gate_mcp_profiles.py`, add `"cella_route_plan"` to the expected `TOOL_GROUPS["pathfinder"]` set.

- [ ] **Step 5: Run the route planner gate**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
```

Expected: `PTH1` through `PTH4` pass.

- [ ] **Step 6: Commit route planning**

Run:

```bash
git add src/cella/pathfinder.py src/cella/mcp_server.py tests/gate_mcp.py tests/gate_mcp_profiles.py tests/gate_mcp_pathfinder.py
git commit -m "Add Cella route planner"
```

Expected: commit contains only the route planner module, MCP route-plan wiring, and pathfinder gate changes.

### Task 4: Rewrite Candidate Failing Gate

**Files:**
- Modify: `tests/gate_mcp_pathfinder.py`

- [ ] **Step 1: Extend the failing test**

Add `call_rewrite_candidates` to the import block:

```python
from cella.mcp_server import (
    TOOL_GROUPS,
    TOOL_NAMES,
    call_route_plan,
    call_rewrite_candidates,
)
```

Add these checks before the final print block:

```python
conjugate = call_rewrite_candidates(
    expression="sqrt(1 + eps) - 1",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH5 conjugate template is generated for sqrt(1+eps)-1",
      conjugate["ok"]
      and any(c["family"] == "sqrt_conjugate" for c in conjugate["value"]["candidates"])
      and any("sqrt" in c["expression"] and "/" in c["expression"] for c in conjugate["value"]["candidates"]))

square = call_rewrite_candidates(
    expression="((12 + eps) * (12 + eps)) - 144",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH6 square-minus-constant emits a difference-of-squares candidate",
      square["ok"]
      and any(c["family"] == "difference_of_squares" for c in square["value"]["candidates"])
      and square["value"]["requires_ranking"] is True)

self_candidates = call_rewrite_candidates(
    expression="eps - eps",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
)
check("PTH7 self-cancellation emits zero candidate",
      self_candidates["ok"]
      and self_candidates["value"]["candidates"][0]["expression"] == "0"
      and self_candidates["value"]["candidates"][0]["family"] == "self_collapse")
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
```

Expected: failure because `call_rewrite_candidates` is not implemented or emits no candidates.

### Task 5: Implement Rewrite Candidate Generation

**Files:**
- Modify: `src/cella/pathfinder.py`
- Modify: `src/cella/mcp_server.py`
- Modify: `tests/gate_mcp.py`
- Modify: `tests/gate_mcp_profiles.py`
- Test: `tests/gate_mcp_pathfinder.py`

- [ ] **Step 1: Add candidate helpers to `src/cella/pathfinder.py`**

Add below the route-plan helpers:

```python
def rewrite_candidates(
    expression: str,
    route_plan_record: dict | None = None,
    sweep: dict | None = None,
    constants: dict | None = None,
) -> dict:
    original = str(expression)
    candidates = []
    not_generated = []
    try:
        tree = ast.parse(original, mode="eval").body
    except SyntaxError as exc:
        return {
            "original": original,
            "candidates": [],
            "requires_ranking": False,
            "not_generated": [{"family": "parse", "reason": str(exc)}],
        }

    _add_unique(candidates, _self_collapse_candidate(tree))
    _add_unique(candidates, _difference_of_squares_candidate(tree))
    _add_unique(candidates, _sqrt_conjugate_candidate(tree))
    for candidate in _three_term_regroup_candidates(tree):
        _add_unique(candidates, candidate)

    for family in ("self_collapse", "difference_of_squares", "sqrt_conjugate", "three_term_regroup"):
        if not any(c["family"] == family for c in candidates):
            not_generated.append({"family": family, "reason": "pattern_not_visible"})

    return {
        "original": original,
        "route_decision": None if route_plan_record is None else route_plan_record.get("decision"),
        "candidates": candidates,
        "requires_ranking": len(candidates) > 1,
        "not_generated": not_generated,
    }
```

Add these helpers:

```python
def _add_unique(candidates: list[dict], candidate: dict | None) -> None:
    if candidate is None:
        return
    if any(c["expression"] == candidate["expression"] for c in candidates):
        return
    candidates.append(candidate)


def _source(node: ast.AST) -> str:
    return ast.unparse(node)


def _same_ast(a: ast.AST, b: ast.AST) -> bool:
    return ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False)


def _self_collapse_candidate(node: ast.AST) -> dict | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub) and _same_ast(node.left, node.right):
        return {
            "name": "self_collapse_zero",
            "expression": "0",
            "family": "self_collapse",
            "reason": "The subtraction operands are structurally identical.",
            "risk": "low",
        }
    return None
```

Add `difference_of_squares`, `sqrt_conjugate`, and three-term helpers:

```python
def _is_square_product(node: ast.AST) -> ast.AST | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) and _same_ast(node.left, node.right):
        return node.left
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
        if isinstance(node.right, ast.Constant) and node.right.value == 2:
            return node.left
    return None


def _sqrt_int_constant(node: ast.AST) -> int | None:
    if not isinstance(node, ast.Constant) or not isinstance(node.value, (int, float)):
        return None
    value = float(node.value)
    root = int(round(value ** 0.5))
    if root * root == value:
        return root
    return None


def _difference_of_squares_candidate(node: ast.AST) -> dict | None:
    if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub)):
        return None
    left_base = _is_square_product(node.left)
    right_root = _sqrt_int_constant(node.right)
    if left_base is None or right_root is None:
        return None
    base = _source(left_base)
    expr = f"(({base}) - {right_root}) * (({base}) + {right_root})"
    return {
        "name": "difference_of_squares",
        "expression": expr,
        "family": "difference_of_squares",
        "reason": "The expression has visible a^2-b^2 structure.",
        "risk": "medium",
    }


def _sqrt_call_arg(node: ast.AST) -> ast.AST | None:
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "sqrt" and len(node.args) == 1:
        return node.args[0]
    return None


def _split_one_plus_x(node: ast.AST) -> ast.AST | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        if isinstance(node.left, ast.Constant) and node.left.value == 1:
            return node.right
        if isinstance(node.right, ast.Constant) and node.right.value == 1:
            return node.left
    return None


def _sqrt_conjugate_candidate(node: ast.AST) -> dict | None:
    if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub)):
        return None
    left_arg = _sqrt_call_arg(node.left)
    if left_arg is not None and isinstance(node.right, ast.Constant) and node.right.value == 1:
        x_node = _split_one_plus_x(left_arg)
        if x_node is not None:
            x = _source(x_node)
            inner = _source(left_arg)
            return {
                "name": "sqrt_conjugate",
                "expression": f"({x}) / (sqrt({inner}) + 1)",
                "family": "sqrt_conjugate",
                "reason": "Conjugate removes same-leading-constant subtraction.",
                "risk": "medium",
            }
    return None


def _flatten_add(node: ast.AST) -> list[ast.AST]:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _flatten_add(node.left) + _flatten_add(node.right)
    return [node]


def _three_term_regroup_candidates(node: ast.AST) -> list[dict]:
    terms = _flatten_add(node)
    if len(terms) != 3:
        return []
    a, b, c = [_source(t) for t in terms]
    return [
        {
            "name": "pair_0_1_then_2",
            "expression": f"(({a}) + ({b})) + ({c})",
            "family": "three_term_regroup",
            "reason": "Pair-first additive regrouping for BACL ranking.",
            "risk": "low",
        },
        {
            "name": "pair_0_2_then_1",
            "expression": f"(({a}) + ({c})) + ({b})",
            "family": "three_term_regroup",
            "reason": "Pair-first additive regrouping for BACL ranking.",
            "risk": "low",
        },
        {
            "name": "pair_1_2_then_0",
            "expression": f"(({b}) + ({c})) + ({a})",
            "family": "three_term_regroup",
            "reason": "Pair-first additive regrouping for BACL ranking.",
            "risk": "low",
        },
    ]
```

- [ ] **Step 2: Add MCP wrapper**

In `src/cella/mcp_server.py`, add:

```python
def call_rewrite_candidates(
    expression: str,
    route_plan: dict | None = None,
    sweep: dict | None = None,
    constants: dict | None = None,
) -> dict:
    """Generate conservative rewrite candidates for one expression."""
    return _wrap_telemetry(
        "cella_rewrite_candidates",
        "Conservative pathfinder rewrite candidates for one expression.",
        lambda: rewrite_candidates(
            str(expression),
            route_plan_record=route_plan,
            sweep=sweep,
            constants=constants or {},
        ),
        depends=(
            "Candidates are small syntactic rewrites, not a full CAS simplification.",
            "Use cella_pathfinder_compare before trusting a candidate operationally.",
        ),
    )
```

Add `"cella_rewrite_candidates"` to `TOOL_NAMES`, `TOOL_GROUPS["pathfinder"]`, help text, and `tool_callable_map()`.

- [ ] **Step 3: Update expected tool sets**

Add `"cella_rewrite_candidates"` to:

- `tests/gate_mcp.py`
- `tests/gate_mcp_profiles.py`

- [ ] **Step 4: Run pathfinder gate**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
```

Expected: route and candidate checks pass. Compare checks are not present yet.

- [ ] **Step 5: Commit candidate generation**

Run:

```bash
git add src/cella/pathfinder.py src/cella/mcp_server.py tests/gate_mcp.py tests/gate_mcp_profiles.py tests/gate_mcp_pathfinder.py
git commit -m "Add Cella rewrite candidates"
```

Expected: commit contains candidate generation and MCP exposure.

### Task 6: Pathfinder Compare Failing Gate

**Files:**
- Modify: `tests/gate_mcp_pathfinder.py`

- [ ] **Step 1: Extend the failing test**

Add `CellaRouter` and `call_pathfinder_compare` to the import block:

```python
from cella.mcp_server import (
    CellaRouter,
    TOOL_GROUPS,
    TOOL_NAMES,
    call_route_plan,
    call_rewrite_candidates,
    call_pathfinder_compare,
)
```

Add before the final print block:

```python
comparison = call_pathfinder_compare(
    variables=["small", "big", "neg_big"],
    forms=[
        {"name": "dirty_left_first", "expression": "(small + big) + neg_big"},
        {"name": "clean_absorb_first", "expression": "small + (big + neg_big)"},
        {"name": "clean_absorb_commuted", "expression": "(big + neg_big) + small"},
    ],
    grid={
        "small": ["0x1.0000000000001p+0"],
        "big": ["0x1p+1"],
        "neg_big": ["-0x1p+1"],
    },
)
check("PTH8 pathfinder compare ranks declared equivalent forms by BACL/refinery burden",
      comparison["ok"]
      and comparison["value"]["winner"] in ["clean_absorb_first", "clean_absorb_commuted"]
      and comparison["value"]["equivalence_status"] == "verified_exact_real_equivalence_on_declared_grid"
      and comparison["value"]["burden_vectors"]["dirty_left_first"]["max_integer_residual"] == "1/2")

router = CellaRouter(default_profile="pathfinder")
router_route = router.call(
    "route_plan",
    {"expression": "(1 + eps) - 1", "sweep": {"variable": "eps", "low": "1e-12", "high": "1e-4"}},
)
check("PTH9 router dispatches route planning from the pathfinder profile",
      router_route["ok"]
      and router_route["tool"] == "cella_route_plan"
      and router_route["result"]["value"]["decision"] == "rewrite_candidate_needed")
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
```

Expected: failure because `call_pathfinder_compare` is not implemented.

### Task 7: Implement Pathfinder Compare and MCP Wiring

**Files:**
- Modify: `src/cella/pathfinder.py`
- Modify: `src/cella/mcp_server.py`
- Modify: `tests/gate_mcp.py`
- Modify: `tests/gate_mcp_profiles.py`
- Test: `tests/gate_mcp_pathfinder.py`

- [ ] **Step 1: Add `pathfinder_compare` to `src/cella/pathfinder.py`**

Add:

```python
def pathfinder_compare(
    variables: list,
    forms: list[dict],
    grid: dict,
    dimensions: list[str] | None = None,
) -> dict:
    ranking = cleanliness_rank(
        [str(v) for v in variables],
        forms,
        grid,
        dimensions=None if dimensions is None else [str(d) for d in dimensions],
    )
    winner = ranking["dial_origin"]
    burden = ranking["burden_vectors"][winner]
    return {
        "winner": winner,
        "ranking": {
            "pareto_frontier": ranking["pareto_frontier"],
            "dominated": ranking["dominated"],
            "dominated_by": ranking["dominated_by"],
            "pairwise_comparisons": ranking["pairwise_comparisons"],
        },
        "burden_vectors": ranking["burden_vectors"],
        "equivalence_status": ranking["sample_equivalence"],
        "trace_examples": ranking["trace_examples"],
        "decision_reason": (
            "winner selected by exact declared-grid equivalence, BACL lattice burden, "
            "rounding residual ulps, final residual ulps, operation depth, and stable tie-break"
        ),
        "winner_burden": burden,
        "next_tools": ["cella_operand_residue_trace", "cella_refinery_compare"],
        "scope": "declared_grid_only",
    }
```

- [ ] **Step 2: Add MCP wrapper**

In `src/cella/mcp_server.py`, add:

```python
def call_pathfinder_compare(
    variables: list,
    forms: list,
    grid: dict,
    dimensions: list | None = None,
) -> dict:
    """Rank declared forms by exact-account/BACL pathfinder burden."""
    return _wrap_proof(
        "cella_pathfinder_compare",
        "Pathfinder ranking for declared algebraic forms over a binary64 grid.",
        lambda: pathfinder_compare(
            [str(v) for v in variables],
            forms,
            grid,
            dimensions=None if dimensions is None else [str(d) for d in dimensions],
        ),
        depends=("The comparison scope is the declared grid; it is not a global identity proof.",),
    )
```

Add `"cella_pathfinder_compare"` to `TOOL_NAMES`, `TOOL_GROUPS["pathfinder"]`, help text, and `tool_callable_map()`.

- [ ] **Step 3: Update expected tool sets**

Add `"cella_pathfinder_compare"` to:

- `tests/gate_mcp.py`
- `tests/gate_mcp_profiles.py`

- [ ] **Step 4: Run pathfinder gate**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
```

Expected: all `PTH` checks pass.

- [ ] **Step 5: Commit comparison**

Run:

```bash
git add src/cella/pathfinder.py src/cella/mcp_server.py tests/gate_mcp.py tests/gate_mcp_profiles.py tests/gate_mcp_pathfinder.py
git commit -m "Add Cella pathfinder comparison"
```

Expected: commit contains compare logic and MCP exposure.

### Task 8: Help, Profile List, and Workflow Polish

**Files:**
- Modify: `src/cella/mcp_server.py`
- Modify: `tests/gate_mcp_pathfinder.py`

- [ ] **Step 1: Extend pathfinder help expectations**

Add to `tests/gate_mcp_pathfinder.py`:

```python
from cella.mcp_server import call_cella_help

help_record = call_cella_help("cella_route_plan")
check("PTH10 help documents route-plan result reading",
      help_record["ok"]
      and "decision" in help_record["value"]["tool"]["read_result"]
      and "next_tools" in help_record["value"]["tool"]["read_result"])
```

- [ ] **Step 2: Update recommended workflows**

In `call_cella_help`, update `pathfinder_preflight` to this order:

```python
"pathfinder_preflight": [
    "cella_route_plan for the initial direct/rewrite/collapse/constants decision",
    "cella_residual_profile when the route needs full residual/account telemetry",
    "cella_rewrite_candidates when rewrite_candidate_needed is returned",
    "cella_pathfinder_compare to rank original and candidates over a declared grid",
    "cella_arith_precision_budget when no cleaner rewrite is available",
],
```

- [ ] **Step 3: Run help/profile checks**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
PYTHONPATH=src python tests/gate_mcp_profiles.py
PYTHONPATH=src python -m cella.mcp_server --list-profiles
```

Expected: pathfinder profile lists `cella_route_plan`, `cella_residual_profile`, `cella_rewrite_candidates`, and `cella_pathfinder_compare`.

- [ ] **Step 4: Commit help polish**

Run:

```bash
git add src/cella/mcp_server.py tests/gate_mcp_pathfinder.py
git commit -m "Document Cella pathfinder workflow"
```

Expected: commit contains only help/workflow test polish.

### Task 9: Full Verification

**Files:**
- Verify all touched gates.

- [ ] **Step 1: Run targeted pathfinder gate**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_pathfinder.py
```

Expected: all checks pass and script exits 0.

- [ ] **Step 2: Run MCP/profile/router gates**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp.py
PYTHONPATH=src python tests/gate_mcp_profiles.py
PYTHONPATH=src python tests/gate_mcp_router.py
```

Expected: all scripts exit 0.

- [ ] **Step 3: Run adjacent functional gates**

Run:

```bash
PYTHONPATH=src python tests/gate_mcp_residual_profile.py
PYTHONPATH=src python tests/gate_mcp_cleanliness.py
PYTHONPATH=src python tests/gate_mcp_symbolic.py
PYTHONPATH=src python tests/gate_mcp_arithmetic.py
```

Expected: all scripts exit 0.

- [ ] **Step 4: Run compile check**

Run:

```bash
PYTHONPATH=src python -m compileall src tests
```

Expected: command exits 0.

- [ ] **Step 5: Run profile list check**

Run:

```bash
PYTHONPATH=src python -m cella.mcp_server --list-profiles
```

Expected: `pathfinder` profile includes the route planner, residual profiler, rewrite candidates, pathfinder compare, symbolic helpers, cleanliness helpers, and arithmetic budget helper.

### Self-Review

- Spec coverage: Tasks cover `cella_route_plan`, `cella_rewrite_candidates`, `cella_pathfinder_compare`, MCP integration, help, profile wiring, route errors, candidate conservatism, ranking by existing BACL/refinery burden, and router dispatch.
- Plan scan: No task uses unresolved-marker or fill-in language. Code snippets define the expected function names, input names, output keys, and tool names.
- Type consistency: Tool names are fixed as `cella_route_plan`, `cella_rewrite_candidates`, and `cella_pathfinder_compare`; module functions are `route_plan`, `rewrite_candidates`, and `pathfinder_compare`.
