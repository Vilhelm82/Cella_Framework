"""Gate MCP cleanliness arm — BACL, operand residue, and refinery ranking.

This gate pins the synthesis of the older V4 BACL/refinery/upsilon work into
daily-driver Cella MCP tools:

- exact binary64 BACL pair diagnostics;
- exact rational residue tracing over a float operand chain;
- componentwise refinery comparison of burden vectors;
- cleanliness ranking of algebraically equivalent forms;
- emergent three-term BACL dial generation.

Run:  python tests/gate_mcp_cleanliness.py
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
        TOOL_NAMES,
        call_bacl_dial,
        call_bacl_pair,
        call_cella_help,
        call_cleanliness_rank,
        call_operand_residue_trace,
        call_refinery_compare,
    )
    from cella.slope_flow import compare_slope_flow_to_models, default_slope_models
    from cella.typed_log_log_slope import fit_power_law_signed
    from cella.typed_ulp import ulp_fraction, ulp_record
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP CLEANLINESS: OPEN — import failed: {exc}")
    sys.exit(1)


zero_ulp = ulp_record(0.0)
subnormal_ulp = ulp_record(float.fromhex("0x0.0000000000001p-1022"))
check("C0 Cella-native copied V4 IEEE ULP primitive handles zero/subnormal exactly",
      zero_ulp["status"] == "ULP_ZERO"
      and zero_ulp["format"] == "float64"
      and ulp_fraction(0.0) == ulp_fraction(float.fromhex("0x0.0000000000001p-1022"))
      and subnormal_ulp["status"] == "ULP_SUBNORMAL"
      and subnormal_ulp["ulp"] == zero_ulp["ulp"])

slope_fit = fit_power_law_signed([(1.0e-6, -2.0e-12), (1.0e-5, -2.0e-10), (1.0e-4, -2.0e-8)])
check("C0b Cella-native copied V4 log-log slope primitive preserves fit diagnostics",
      slope_fit["signal_exponent"] == "2"
      and abs(slope_fit["signed_coefficient"] + 2.0) < 1.0e-8
      and slope_fit["fit_quality"]["n_used"] == 3
      and slope_fit["fit_quality"]["standard_error"] is not None
      and slope_fit["fit_quality"]["expression_path"] == "cella_signed_power_law_fit")

slope_flow = compare_slope_flow_to_models(
    [(1.0e-6, 3.0e-12), (1.0e-5, 3.0e-10), (1.0e-4, 3.0e-8)],
    default_slope_models(),
    declared_model_band=1.0e-8,
    comparison_kind="residual_order",
)
check("C0c Cella-native copied V4 slope-flow primitive performs segment model matching",
      slope_flow["status"] == "SLOPE_MODEL_UNIQUE_MATCH"
      and slope_flow["selected_model_name"] == "order_2"
      and len(slope_flow["segment_evidence"]) == 2
      and slope_flow["model_residuals_by_name"]["order_2"]["within_declared_band"] is True
      and slope_flow["comparison_kind"] == "residual_order")


protected = call_bacl_pair("0x1p+1", "0x1p+0")
off = call_bacl_pair("0x1.0000000000001p+0", "0x1p+1")
check("C1 BACL pair proves protected integer lattice and exposes half-cell failures",
      protected["ok"]
      and protected["value"]["theorem_protected"] is True
      and protected["value"]["lattice_class"] == "integer_lattice"
      and off["ok"]
      and off["value"]["theorem_hypothesis"] is False
      and off["value"]["lattice_class"] == "off_integer_lattice"
      and off["value"]["integer_residual"] == "1/2")

trace = call_operand_residue_trace(
    expression="(small + big) + neg_big",
    variables=["small", "big", "neg_big"],
    values={
        "small": "0x1.0000000000001p+0",
        "big": "0x1p+1",
        "neg_big": "-0x1p+1",
    },
)
check("C2 operand residue trace records exact chain residue and additive BACL burden",
      trace["ok"]
      and trace["value"]["operation_chain_depth"] == "2"
      and [entry["op"] for entry in trace["value"]["entries"]] == ["add", "add"]
      and trace["value"]["diagnostics"]["off_lattice_additive_ops"] == "1"
      and trace["value"]["diagnostics"]["max_bacl_integer_residual"] == "1/2")

decision = call_refinery_compare(
    reference={
        "name": "dirty_reference",
        "geometry": {"fixture": "half_cell", "identity": "small+big+neg_big"},
        "burden": {
            "lattice_class": "off_integer_lattice",
            "max_integer_residual": "1/2",
            "operation_chain_depth": "2",
        },
    },
    candidate={
        "name": "clean_candidate",
        "geometry": {"fixture": "half_cell", "identity": "small+big+neg_big"},
        "burden": {
            "lattice_class": "integer_lattice",
            "max_integer_residual": "0",
            "operation_chain_depth": "2",
        },
    },
)
check("C3 refinery compare accepts same-geometry lower-burden rewrite",
      decision["ok"]
      and decision["value"]["admissible"] is True
      and decision["value"]["decision"] == "accepted"
      and decision["value"]["dimension_results"]["lattice_class"] == "candidate_better"
      and decision["value"]["dimension_results"]["max_integer_residual"] == "candidate_better")

ranked = call_cleanliness_rank(
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
check("C4 cleanliness rank selects the BACL-clean form over the locally tempting half-cell form",
      ranked["ok"]
      and ranked["value"]["dial_origin"] in ["clean_absorb_first", "clean_absorb_commuted"]
      and "dirty_left_first" in ranked["value"]["dominated"]["clean_absorb_first"]
      and ranked["value"]["burden_vectors"]["dirty_left_first"]["max_integer_residual"] == "1/2"
      and ranked["value"]["burden_vectors"]["clean_absorb_first"]["max_integer_residual"] == "0")

dial = call_bacl_dial(
    variables=["small", "big", "neg_big"],
    terms=[
        {"label": "small", "expression": "small"},
        {"label": "big", "expression": "big"},
        {"label": "neg_big", "expression": "neg_big"},
    ],
    grid={
        "small": ["0x1.0000000000001p+0"],
        "big": ["0x1p+1"],
        "neg_big": ["-0x1p+1"],
    },
)
check("C5 BACL dial generates pair-first algebraic configurations and finds the clean origin",
      dial["ok"]
      and len(dial["value"]["generated_forms"]) == 3
      and dial["value"]["dial_origin_pair"] == ["big", "neg_big"]
      and dial["value"]["ranking"]["burden_vectors"][dial["value"]["dial_origin"]]["max_integer_residual"] == "0")

help_all = call_cella_help()
help_rank = call_cella_help("cella_cleanliness_rank")
check("C6 help covers the mature cleanliness/refinery tool layer",
      help_all["ok"]
      and "cella_bacl_pair" in help_all["value"]["tools"]
      and "cleanliness_refinery" in help_all["value"]["recommended_workflows"]
      and help_rank["ok"]
      and "Pareto" in help_rank["value"]["tool"]["read_result"])

check("C7 MCP tool names include the cleanliness arm",
      {
          "cella_bacl_dial",
          "cella_bacl_pair",
          "cella_cleanliness_rank",
          "cella_operand_residue_trace",
          "cella_refinery_compare",
      } <= set(TOOL_NAMES))

print()
if FAILS:
    print(f"GATE MCP CLEANLINESS: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP CLEANLINESS: CLOSED — BACL/refinery cleanliness arm is MCP-callable.")
sys.exit(0)
