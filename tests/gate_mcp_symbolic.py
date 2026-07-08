"""Gate MCP symbolic arm — exact rational-function Cella tools.

This gate pins the daily-driver symbolic surface:

- symbolic pole-law coefficients such as -14/B without coefficient swell;
- rational-function equality by exact cross-multiplication;
- gauge-normal carriers over Q(symbols);
- n=3 channel transport identities as rational-function certificates;
- refusal of decimal literals before a CAS can silently rationalize them.

Run:  python tests/gate_mcp_symbolic.py
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
        call_cella_help,
        call_symbolic_channel_sum,
        call_symbolic_equal,
        call_symbolic_gauge_carrier,
        call_symbolic_pole_law,
        call_symbolic_rational,
        call_symbolic_valuation,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP SYMBOLIC: OPEN — import failed: {exc}")
    sys.exit(1)


rat = call_symbolic_rational(
    expression="(-14)/(S*(16*pi*S + 1)**2)",
    variables=["S", "Q", "pi"],
)
eq = call_symbolic_equal(
    left="(-14)/(S*(16*pi*S + 1)**2)",
    right="(-14)/(S*(1 + 16*pi*S)**2)",
    variables=["S", "Q", "pi"],
)
neq = call_symbolic_equal(
    left="(-14)/(S*(16*pi*S + 1)**2)",
    right="(-14)/(S*(16*pi*S + 1))",
    variables=["S", "Q", "pi"],
)
check("S1 rational arm records exact numerator/denominator support and equality witnesses",
      rat["ok"]
      and rat["value"]["expression"]["denominator_terms"] == "3"
      and eq["ok"] and eq["value"]["equal"] is True
      and eq["value"]["cross_difference"]["is_zero"] is True
      and neq["ok"] and neq["value"]["equal"] is False)

pole = call_symbolic_pole_law(
    kind="master_quadric",
    exponents=["2", "-2", "-2"],
    variables=["B"],
    B="B",
)
check("S2 master quadric symbolic pole law preserves -14/B as a rational function",
      pole["ok"]
      and pole["value"]["C_p"] == "-14"
      and pole["value"]["coefficient"]["numerator"] == [["-14", ["0"]]]
      and pole["value"]["coefficient"]["denominator"] == [["1", ["1"]]]
      and pole["value"]["coefficient_text"] == "-14/(B)")

pole_rf = call_symbolic_pole_law(
    kind="parity_fixed",
    m=2,
    variables=["S", "Q", "pi"],
    B="S*(16*pi*S + 1)**2",
)
pole_rf_eq = call_symbolic_equal(
    left=pole_rf["value"]["coefficient_text"],
    right="(-14)/(S*(1 + 16*pi*S)**2)",
    variables=["S", "Q", "pi"],
)
check("S3 parity-fixed law keeps the denominator as a symbolic rational function of S,Q,pi",
      pole_rf["ok"]
      and pole_rf["value"]["coefficient"]["denominator_terms"] == "3"
      and pole_rf_eq["ok"] and pole_rf_eq["value"]["equal"] is True)

carrier = call_symbolic_gauge_carrier(
    variables=["g1", "g2", "g3", "h11", "h22", "h33", "h12", "h13", "h23"],
    g=["g1", "g2", "g3"],
    H=[
        ["h11", "h12", "h13"],
        ["h12", "h22", "h23"],
        ["h13", "h23", "h33"],
    ],
)
o12_eq = call_symbolic_equal(
    left=carrier["value"]["O"]["O12"]["text"],
    right="h12 - g1*h22/(2*g2) - g2*h11/(2*g1)",
    variables=["g1", "g2", "g3", "h11", "h22", "h33", "h12", "h13", "h23"],
)
check("S4 symbolic gauge carrier computes O_ij in exact Q(symbols) normal form",
      carrier["ok"]
      and carrier["value"]["pairs"] == ["O12", "O13", "O23"]
      and carrier["value"]["normal_form"][0][0]["is_zero"] is True
      and o12_eq["ok"] and o12_eq["value"]["equal"] is True)

channels = call_symbolic_channel_sum(
    variables=["u", "v", "w"],
    channels={
        "kc": "(12*u*v + 6*u*w + 18*v*w + 6*w - 1)/49",
        "ks": "(12*u*v + 6*u*w + 3*u + 18*v*w + 13*v + 2*w + 1)/49",
        "kint": "-(24*u*v + 12*u*w + 3*u + 36*v*w + 13*v + 8*w + 3)/49",
    },
    expected_total="-3/49",
)
check("S5 symbolic channel sum certifies the keystone affine transport plane",
      channels["ok"]
      and channels["value"]["sum_equals_expected"] is True
      and channels["value"]["sum"]["text"] == "-3/49")

try:
    call_symbolic_rational("B + 0.1", ["B"])
    decimal_rejected = False
except ValueError:
    decimal_rejected = True
check("S6 symbolic rational arm rejects decimal literals before parsing", decimal_rejected)

valuation = call_symbolic_valuation(
    coordinates=["x", "y"],
    parameters=["S"],
    terms=[
        {"label": "V1", "coefficient": "S - 1", "powers": ["-4", "2"]},
        {"label": "V2", "coefficient": "3", "powers": ["2", "-4"]},
        {"label": "V0", "coefficient": "0", "powers": ["-2", "-2"]},
    ],
    path={"x": "1", "y": "1"},
)
check("S7 symbolic valuation records active support and deletion walls without expanding curvature",
      valuation["ok"]
      and valuation["value"]["active_terms"] == ["V1", "V2"]
      and valuation["value"]["support_order"] == "2"
      and valuation["value"]["leading_terms"] == ["V1", "V2"]
      and valuation["value"]["deletion_walls"][0]["wall"] == "-1 + S = 0")

help_all = call_cella_help()
help_eq = call_cella_help("cella_symbolic_equal")
check("S8 Cella Help explains tools, inputs, and result fields",
      help_all["ok"]
      and "cella_symbolic_pole_law" in help_all["value"]["tools"]
      and "result_contract" in help_all["value"]
      and help_eq["ok"]
      and help_eq["value"]["topic"] == "cella_symbolic_equal"
      and "cross_difference" in help_eq["value"]["tool"]["read_result"])

check("S9 MCP tool names include symbolic-arm and help tools",
      {
          "cella_help",
          "cella_symbolic_channel_sum",
          "cella_symbolic_equal",
          "cella_symbolic_gauge_carrier",
          "cella_symbolic_pole_law",
          "cella_symbolic_rational",
          "cella_symbolic_valuation",
      } <= set(TOOL_NAMES))

print()
if FAILS:
    print(f"GATE MCP SYMBOLIC: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP SYMBOLIC: CLOSED — exact symbolic arm is MCP-callable.")
sys.exit(0)
