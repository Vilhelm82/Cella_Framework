"""G0--G8 gate for the bounded DBP native relative-period evaluator."""

from __future__ import annotations

import inspect
import json
import math
import random
import struct
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

from cella.native_periods import (CertifiedPeriodResult, PeriodRefusal,
    evaluate_dbp_relative_period, verify_dbp_certificate)
from cella.native_periods.account import evaluate_fixed_dag_binary64
from cella.native_periods.dbp_theta_route import (MINUS_EXPRESSION, PLUS_EXPRESSION,
    canonical_source, compile_dbp_theta)
from cella.native_periods.eft import (division_defect, float_fraction, normalize_expansion,
    sqrt_defect, two_prod, two_sum)
from cella.native_periods.records import (CurveRecord, DifferentialRecord, DUAL_PATH,
    PRIMARY_PATH, RelativePathRecord, SourceRecord)
from cella.native_periods.schedule import admitted_m1_schedule


passed = 0
def check(label, condition):
    global passed
    if not condition: raise AssertionError(label)
    passed += 1


root = Path(__file__).resolve().parents[1]
contracts = json.loads((root/"campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_CONTRACTS_v1.0.json").read_text())
plus = compile_dbp_theta(canonical_source(PRIMARY_PATH))
minus = compile_dbp_theta(canonical_source(DUAL_PATH))
check("G1 primary expression exact", plus.expression == contracts["routes"]["dbp_theta_primary_v1"]["compiled_kernel"]["expression"] == PLUS_EXPRESSION)
check("G1 dual expression exact", minus.expression == contracts["routes"]["dbp_theta_dual_cpv_v1"]["compiled_kernel"]["expression"] == MINUS_EXPRESSION)
check("G1 source versions attached", plus.theorem_version.endswith("v1.1") and plus.route_version.endswith("v1.0"))
check("G5 forbidden former pole absent", "t^2 - 8*w^2" not in minus.expression)
check("G5 runtime CPV absent", minus.source_ledger["runtime_cpv"] is False)
tp = 2*math.sqrt(2)/(1+2*math.sqrt(2))
former = evaluate_fixed_dag_binary64("g_minus_v1", tp)["reading"]
expected_former = -(128+144*math.sqrt(2))/25
check("G5 former pole is an ordinary finite point", math.isfinite(former) and abs(former-expected_former) < 2e-14)

rng = random.Random(0xDB128)
vectors = [(0.0, -0.0), (1.0, -1.0), (2.0**-1022, 2.0**-1074), (2.0**500, 2.0**-400)]
for _ in range(500):
    a = math.ldexp(rng.uniform(-1, 1), rng.randrange(-400, 400))
    b = math.ldexp(rng.uniform(-1, 1), rng.randrange(-400, 400))
    vectors.append((a, b))
for a,b in vectors:
    s,e=two_sum(a,b); check("two_sum identity", float_fraction(s)+e == float_fraction(a)+float_fraction(b))
    p,e=two_prod(a,b); check("two_prod identity", float_fraction(p)+e == float_fraction(a)*float_fraction(b))
    if b:
        q,r=division_defect(a,b); check("division defect identity", float_fraction(a)-float_fraction(q)*float_fraction(b)==r)
for x in (0.0, 2.0**-1074, 0.125, 2.0, 1e200):
    q,d=sqrt_defect(x); check("sqrt square defect identity", float_fraction(x)-float_fraction(q)**2==d)
limbs,residual=normalize_expansion([1.0,2.0**-53,-1.0])
check("expansion normalization", sum(map(float_fraction,limbs),Fraction())+residual == Fraction(1,2**53))
for kid in ("g_plus_v1","g_minus_v1"):
    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
        check("fixed DAG account closes", evaluate_fixed_dag_binary64(kid,t)["closed"])

check("primary domain witness", plus.domain_witnesses == ("P_plus >= 1/8", "t^2 + 8*w^2 >= 8/9"))
check("dual domain witness", minus.domain_witnesses == ("P_minus >= 1/64", "t^2 + 2*w^2 >= 2/3"))
check("M1 primary schedule admitted", len(admitted_m1_schedule("g_plus_v1")["panel_schedules"]) == 32)
check("M1 dual schedule admitted", len(admitted_m1_schedule("g_minus_v1")["panel_schedules"]) == 32)

wrong_curve = SourceRecord(CurveRecord(coefficients=(0,-1,0,1,-2)), DifferentialRecord(), PRIMARY_PATH)
wrong_diff = SourceRecord(CurveRecord(), DifferentialRecord(expression="7*(X-3)/(X+7)*dX/Y"), PRIMARY_PATH)
missing_sheet = SourceRecord(path=replace(DUAL_PATH, sheet=None))
wrong_orientation = SourceRecord(path=replace(PRIMARY_PATH, orientation="decreasing_X"))
one_sided = SourceRecord(path=RelativePathRecord("X=1","X=-infinity","decreasing_X",None,"one_sided"))
check("wrong curve refuses", compile_dbp_theta(wrong_curve).token == "unsupported_curve")
check("wrong differential refuses", compile_dbp_theta(wrong_diff).token == "unsupported_differential")
check("missing sheet refuses", compile_dbp_theta(missing_sheet).token == "sheet_not_declared")
check("wrong orientation refuses", compile_dbp_theta(wrong_orientation).token == "unsupported_relative_path")
check("one-sided missing side refuses", compile_dbp_theta(one_sided).token == "cpv_side_not_declared")

results = {t:evaluate_dbp_relative_period(t,150) for t in ("trace_primary","primary","trace_dual_real_cpv","dual_cpv")}
for target,result in results.items():
    check("M1 returns certified result", isinstance(result,CertifiedPeriodResult))
    check("M1 width", result.dyadic_bracket.width_bits >= 150)
    check("account closed", result.account_ledger["closed"])
    check("oracle pins listed unused", len(result.certificate_record["unused_oracle_pins"]) == 2)
check("primary prefix", results["primary"].rounded_value.startswith("-5.01049070266041876905002116052677764805699485672160"))
check("dual prefix", results["dual_cpv"].rounded_value.startswith("-3.988001085974558097719762257539087379694121855552360291"))
again = evaluate_dbp_relative_period("primary",150)
check("G8 certificate byte stable", again.certificate_record == results["primary"].certificate_record)
check("certificate verifier accepts canonical record", verify_dbp_certificate(results["dual_cpv"].certificate_record) is True)
tampered_pole = deepcopy(results["dual_cpv"].certificate_record)
tampered_pole["source_ledger"]["source_pole"] = ["-8", "20*i"]
check("altered pole refuses", verify_dbp_certificate(tampered_pole).token == "route_identity_failed")
tampered_account = deepcopy(results["dual_cpv"].certificate_record)
tampered_account["account_ledger"]["closed"] = False
check("account tampering refuses", verify_dbp_certificate(tampered_account).token == "account_not_closed")
check("certificate suppression changes no bracket", evaluate_dbp_relative_period("primary",150,False).dyadic_bracket == results["primary"].dyadic_bracket)
check("unknown target refuses", isinstance(evaluate_dbp_relative_period("K",150),PeriodRefusal))
m0 = evaluate_dbp_relative_period("primary",40)
check("M0 width", isinstance(m0,CertifiedPeriodResult) and m0.dyadic_bracket.width_bits >= 40 and m0.account_ledger["limb_count"] == 1)
def interval_of(result):
    b=result.dyadic_bracket
    return Fraction(b.lower_numerator,1<<b.denominator_exponent), Fraction(b.upper_numerator,1<<b.denominator_exponent)
m0lo,m0hi=interval_of(m0); m1lo,m1hi=interval_of(results["primary"])
check("precision escalation overlaps", max(m0lo,m1lo) <= min(m0hi,m1hi))

production = list((root/"src/cella/native_periods").glob("*.py"))
forbidden = ("mpmath","sympy","scipy","flint","sage","ellipk","ellipe","ellippi","carlson")
imports = "\n".join(p.read_text().lower() for p in production)
check("G6 no forbidden production dependency", not any(f in imports for f in forbidden))
check("pins do not enter computation", "decimal_prefix" not in imports and "5.010490702660" not in imports)

print(f"DBP native relative-period evaluator: {passed} assertions passed")
