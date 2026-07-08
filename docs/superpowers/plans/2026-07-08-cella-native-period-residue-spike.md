# Cella Native Period Residue Spike Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a first Cella-native certified period/residue kernel spike that reduces elliptic quartic third-kind routes to exact structural normal forms and reports the next gaps explicitly.

**Architecture:** Add a focused `periods.py` module using only Cella-native exact rationals and sparse records, then expose it through MCP proof wrappers. The spike does not numerically evaluate periods; it certifies curve structure, pole residues, branch jumps, exact period-basis linear forms, route equality, and gap records for unimplemented reductions.

**Tech Stack:** Python stdlib `fractions`, existing Cella certificate/MCP serialization, existing sparse exact style from `symbolic.py`.

---

### Task 1: Failing Gate

**Files:**
- Create: `tests/gate_mcp_periods.py`

- [ ] **Step 1: Write the failing test**

Create `tests/gate_mcp_periods.py` with assertions for:
- native quartic record for `y^2=(1-x^2)(1-m*x^2)`;
- exact third-kind pole residue and signed branch jumps from rational `m,n,prefactor`;
- exact CPV normal form `scale*(weight_pi*(K-Pi(q))-weight_k*K)`;
- route comparison by normal-form equality;
- gap report naming missing certified evaluation, general algebraic parser, general differential reduction, and raw surface route.

- [ ] **Step 2: Run test to verify it fails**

Run: `python tests/gate_mcp_periods.py`
Expected: import failure for missing MCP callables.

### Task 2: Native Period Module

**Files:**
- Create: `src/cella/periods.py`

- [ ] **Step 1: Implement exact rational parser**

Accept integers, rational strings, and nested lists where needed. Reject floats.

- [ ] **Step 2: Implement quartic structure**

Return exact Legendre quartic coefficients, branch points as symbolic labels, discriminant factors, and `j=256*(1-m+m^2)^3/(m^2*(1-m)^2)` when `m` is rational.

- [ ] **Step 3: Implement third-kind residue law**

For `omega=prefactor*dx/((1-n*x^2)*y)` on the declared Legendre quartic, compute `x0^2=1/n`, `y0^2=(1-x0^2)*(1-m*x0^2)`, the signed residue-square, and exact branch-jump coefficients without choosing a square root branch unless the weighted residue is declared.

- [ ] **Step 4: Implement period normal form**

Represent linear combinations over basis atoms `K(m)` and `Pi(q;m)` plus residue jumps. Normalize coefficients exactly and compare records structurally.

- [ ] **Step 5: Implement gap report**

Emit a deterministic gap list with status, why it matters, and the next spike target.

### Task 3: MCP Wiring

**Files:**
- Modify: `src/cella/mcp_server.py`
- Modify: `tests/gate_mcp.py`
- Modify: `tests/gate_mcp_profiles.py`

- [ ] **Step 1: Add imports, tool names, and profile entries**

Add period tools to `TOOL_NAMES`, `TOOL_GROUPS["arithmetic"]`, help records, and callable map.

- [ ] **Step 2: Add wrappers**

Add `call_period_quartic`, `call_period_third_kind_residue`, `call_period_normal_form`, `call_period_route_compare`, and `call_period_gap_report`.

- [ ] **Step 3: Update profile gates**

Update expected tool-name and arithmetic-profile sets.

### Task 4: Verification

**Files:**
- Test all touched gates.

- [ ] **Step 1: Run targeted gates**

Run:
- `python tests/gate_mcp_periods.py`
- `python tests/gate_mcp_arithmetic.py`
- `python tests/gate_mcp_profiles.py`
- `python tests/gate_mcp.py`

- [ ] **Step 2: Run compile check**

Run: `python -m compileall src tests`

- [ ] **Step 3: Run profile construction check**

Run: `PYTHONPATH=src python -m cella.mcp_server --list-profiles`

### Self-Review

- Spec coverage: The plan covers native exact period records, residue ledgers, CPV normal forms, route comparison, gap exposure, MCP exposure, and tests.
- Placeholder scan: No task depends on an unnamed future implementation.
- Type consistency: Tool names and module names are fixed in the tasks above.
