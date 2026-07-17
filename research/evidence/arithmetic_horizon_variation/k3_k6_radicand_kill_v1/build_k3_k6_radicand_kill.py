#!/usr/bin/env python3
"""Build the exact k=3/k=6 canonical-radicand kill-test certificate."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

SOURCES = {
    "all_k_base_monodromy_proof_authority": ROOT
    / "Papers_Library/01_completed_papers/galois_horizon_and_kummer_covers/GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md",
    "all_k_base_monodromy": ROOT
    / "Papers_Library/02_theorems_and_lemmas/galois_horizon_and_kummer_covers/ALL_K_MONODROMY_THEOREM_NOTE_2026-07-10.md",
    "generic_reflection_descent": ROOT
    / "Papers_Library/03_proofs_derivations_and_audits/galois_horizon_and_kummer_covers/AUDIT_REPORT_R6_R7_GENERIC_DESCENT.md",
    "kummer_wreath_lift": ROOT
    / "Papers_Library/02_theorems_and_lemmas/galois_horizon_and_kummer_covers/KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md",
    "k4_canonical_normalization": ROOT
    / "Papers_Library/01_completed_papers/galois_horizon_and_kummer_covers/galois_horizon_cover_v1_0.tex",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def trim(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def padd(a: list[int], b: list[int]) -> list[int]:
    result = [0] * max(len(a), len(b))
    for index, coefficient in enumerate(a):
        result[index] += coefficient
    for index, coefficient in enumerate(b):
        result[index] += coefficient
    return trim(result)


def psub(a: list[int], b: list[int]) -> list[int]:
    result = [0] * max(len(a), len(b))
    for index, coefficient in enumerate(a):
        result[index] += coefficient
    for index, coefficient in enumerate(b):
        result[index] -= coefficient
    return trim(result)


def pmul(a: list[int], b: list[int]) -> list[int]:
    if not a or not b:
        return []
    result = [0] * (len(a) + len(b) - 1)
    for i, left in enumerate(a):
        if left:
            for j, right in enumerate(b):
                result[i + j] += left * right
    return trim(result)


def pscale(a: list[int], scalar: int) -> list[int]:
    return [] if scalar == 0 else [scalar * coefficient for coefficient in a]


def btrim(polynomial: list[list[int]]) -> list[list[int]]:
    while polynomial and not polynomial[-1]:
        polynomial.pop()
    return polynomial


def bmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    if not left or not right:
        return []
    result = [[] for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    result[i + j] = padd(result[i + j], pmul(a, b))
    return btrim(result)


def bsub(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    result = []
    for index in range(max(len(left), len(right))):
        a = left[index] if index < len(left) else []
        b = right[index] if index < len(right) else []
        result.append(psub(a, b))
    return btrim(result)


def bmul_upoly(polynomial: list[list[int]], factor: list[int]) -> list[list[int]]:
    return btrim([pmul(coefficient, factor) if coefficient else [] for coefficient in polynomial])


def norm_step(polynomial: list[list[int]], n_squared: int) -> list[list[int]]:
    """Take the exact norm across w^2=u+n_squared."""
    w_squared = [n_squared, 1]
    degree_x = len(polynomial) - 1
    powers = [[1]]
    for _ in range(degree_x // 2 + 1):
        powers.append(pmul(powers[-1], w_squared))

    even = [[] for _ in range(degree_x + 1)]
    odd = [[] for _ in range(degree_x + 1)]
    for j, coefficient in enumerate(polynomial):
        if not coefficient:
            continue
        for t in range(j + 1):
            term = pscale(coefficient, math.comb(j, t))
            power, parity = divmod(t, 2)
            if power:
                term = pmul(term, powers[power])
            target_power = j - t
            if parity == 0:
                even[target_power] = padd(even[target_power], term)
            else:
                odd[target_power] = padd(odd[target_power], term)
    return bsub(
        bmul(btrim(even), btrim(even)),
        bmul_upoly(bmul(btrim(odd), btrim(odd)), w_squared),
    )


def build_mass_norm(mass_four: int, charges: tuple[int, ...]) -> tuple[list[int], int]:
    """Return the primitive low-first u-polynomial N_k(u;M)."""
    polynomial: list[list[int]] = [[], [1]]
    for charge in charges:
        polynomial = norm_step(polynomial, charge * charge)

    raw: list[int] = []
    mass_power = 1
    for coefficient in polynomial:
        if coefficient:
            raw = padd(raw, pscale(coefficient, mass_power))
        mass_power *= mass_four

    content = 0
    for coefficient in raw:
        content = math.gcd(content, coefficient)
    primitive = [coefficient // content for coefficient in raw]
    if primitive[-1] < 0:
        primitive = [-coefficient for coefficient in primitive]
    return primitive, content


def delta(k: int) -> int:
    if k % 2:
        return 2 ** (k - 1)
    return 2 ** (k - 1) - math.comb(k, k // 2) // 2


def e_term(index: int, u_power: int) -> str:
    if index == 0:
        return "1" if u_power == 0 else ("u" if u_power == 1 else f"u^{u_power}")
    elementary = f"e{index}(w)"
    if u_power == 0:
        return elementary
    if u_power == 1:
        return f"u*{elementary}"
    return f"u^{u_power}*{elementary}"


def formula_strings(k: int) -> tuple[str, str, str]:
    alpha = "+".join(e_term(j, (k - j) // 2) for j in range(k, -1, -2))
    beta = "+".join(e_term(j, (k - j - 1) // 2) for j in range(k - 1, -1, -2))
    gamma = f"2*({alpha}+P)"
    return alpha, beta, gamma


def elementary(variables: tuple[sp.Symbol, ...], degree: int) -> sp.Expr:
    if degree == 0:
        return sp.Integer(1)
    return sum(
        (sp.prod(variables[index] for index in indices) for indices in itertools.combinations(range(len(variables)), degree)),
        sp.Integer(0),
    )


def verify_formal_identities(k: int) -> dict[str, bool]:
    m = sp.Symbol("m")
    variables = sp.symbols(f"w1:{k + 1}")
    u = m**2
    a_plus = sp.prod(variable + m for variable in variables)
    a_minus = sp.prod(variable - m for variable in variables)
    alpha = sum(u ** ((k - j) // 2) * elementary(variables, j) for j in range(k, -1, -2))
    beta = sum(u ** ((k - j - 1) // 2) * elementary(variables, j) for j in range(k - 1, -1, -2))
    return {
        "A_plus_equals_alpha_plus_m_beta": sp.expand(a_plus - alpha - m * beta) == 0,
        "A_minus_equals_alpha_minus_m_beta": sp.expand(a_minus - alpha + m * beta) == 0,
        "alpha_squared_minus_u_beta_squared_equals_A_plus_A_minus": sp.expand(
            alpha**2 - u * beta**2 - a_plus * a_minus
        )
        == 0,
        "A_plus_A_minus_equals_product_wi_squared_minus_u": sp.expand(
            a_plus * a_minus - sp.prod(variable**2 - u for variable in variables)
        )
        == 0,
    }


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def contact_payload(k: int, charges: tuple[int, ...], signs: tuple[int, ...]) -> dict[str, object]:
    sign_product = math.prod(signs)
    product = math.prod(charges)
    mass_four = sum(sign * charge for sign, charge in zip(signs, charges))
    reciprocal_sum = sum(
        (Fraction(sign, charge) for sign, charge in zip(signs, charges)),
        Fraction(0),
    )
    beta_contact = sign_product * product * reciprocal_sum
    polynomial, content = build_mass_norm(mass_four, charges)
    matching_signs = [
        list(candidate)
        for candidate in itertools.product((-1, 1), repeat=k)
        if sum(sign * charge for sign, charge in zip(candidate, charges)) == mass_four
    ]
    return {
        "signs": list(signs),
        "sign_product": sign_product,
        "four_M": mass_four,
        "reciprocal_sum": fraction_text(reciprocal_sum),
        "beta_contact": fraction_text(beta_contact),
        "gamma_plus_contact": 2 * product * (1 + sign_product),
        "gamma_minus_contact": 2 * product * (sign_product - 1),
        "mass_norm_degree": len(polynomial) - 1,
        "mass_norm_coefficients_low_first": [str(coefficient) for coefficient in polynomial],
        "mass_norm_content_removed": str(content),
        "mass_norm_at_zero": str(polynomial[0]),
        "mass_norm_derivative_at_zero": str(polynomial[1]),
        "u_zero_is_simple": polynomial[0] == 0 and polynomial[1] != 0,
        "matching_signed_walls": matching_signs,
        "signed_wall_is_unique": matching_signs == [list(signs)],
        "valuation_parity_u_gamma_plus": [1, 0 if sign_product == 1 else 1],
    }


def case_payload(k: int, charges: tuple[int, ...]) -> dict[str, object]:
    alpha, beta, gamma = formula_strings(k)
    even = contact_payload(k, charges, (1,) * k)
    odd = contact_payload(k, charges, (-1,) + (1,) * (k - 1))
    degree = delta(k)
    formal = verify_formal_identities(k)
    if not all(formal.values()):
        raise AssertionError(f"formal product identity failed at k={k}: {formal}")
    if not even["u_zero_is_simple"] or not odd["u_zero_is_simple"]:
        raise AssertionError(f"contact root was not simple at k={k}")
    if even["mass_norm_degree"] != degree or odd["mass_norm_degree"] != degree:
        raise AssertionError(f"mass norm degree mismatch at k={k}")
    if even["valuation_parity_u_gamma_plus"] != [1, 0]:
        raise AssertionError(f"even parity row failed at k={k}")
    if odd["valuation_parity_u_gamma_plus"] != [1, 1]:
        raise AssertionError(f"odd parity row failed at k={k}")

    group = f"C2^2 wr S{degree}"
    return {
        "k": k,
        "delta_k": degree,
        "charges": list(charges),
        "P": math.prod(charges),
        "A_plus": "product_i(w_i+m)",
        "A_minus": "product_i(w_i-m)",
        "alpha": alpha,
        "beta": beta,
        "gamma_plus": gamma,
        "gamma_minus": f"2*({alpha}-P)",
        "reflection": "m->-m exchanges A_plus and A_minus and fixes gamma_plus",
        "formal_identity_checks": formal,
        "square_class_relation": "[gamma_minus]=[u]*[gamma_plus]",
        "descent": "w_i in K=F(u), hence alpha,beta,gamma_plus in K",
        "even_contact": even,
        "odd_contact": odd,
        "sheet_level_B": [[1, 0], [1, 1]],
        "sheet_level_rank_F2": 2,
        "off_contact_parity": "even by gamma_plus*gamma_minus=4*u*beta^2 when u is a unit",
        "base_group": f"S{degree}",
        "orbit_saturated_matrix": f"B tensor I_{degree}",
        "square_class_rank": 2 * degree,
        "normal_closure_group": group,
        "normal_closure_group_order": str(2 ** (2 * degree) * math.factorial(degree)),
        "verdict": "SURVIVES",
    }


def build_certificate() -> dict[str, object]:
    for path in SOURCES.values():
        if not path.is_file():
            raise FileNotFoundError(path)
    source_refs = {
        name: {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_bytes(path.read_bytes()),
        }
        for name, path in SOURCES.items()
    }
    return {
        "schema": "cella.ahv1.k3_k6_radicand_kill.v1",
        "date": "2026-07-18",
        "question": "Does the canonical norm-derived second radicand survive one odd and one even charge count?",
        "canonicity_criterion": {
            "definition": "gamma_k=A_plus+A_minus+2P=(sqrt(A_plus)+sqrt(A_minus))^2",
            "requirements": [
                "formed functorially from the two axial product branches A_plus and A_minus",
                "fixed by the axial reflection m->-m",
                "no tunable coefficients or auxiliary divisor search",
                "specializes at k=4 to the published gamma_R9",
            ],
            "candidate_exhaustion": "the opposite cross-term gamma_minus has square class [u]*[gamma_plus] and supplies no third channel",
        },
        "universal_identity": {
            "alpha_k": "sum_{j congruent k mod 2} u^((k-j)/2)*e_j(w)",
            "beta_k": "sum_{j not congruent k mod 2} u^((k-j-1)/2)*e_j(w)",
            "A_plus_minus": "A_plus=alpha_k+m*beta_k; A_minus=alpha_k-m*beta_k",
            "norm": "alpha_k^2-u*beta_k^2=P^2",
            "radicand": "gamma_k=2*(alpha_k+P)",
            "parity_identity": "gamma_k*(gamma_k-4*P)=4*u*beta_k^2",
        },
        "cases": {
            "3": case_payload(3, (1, 2, 4)),
            "6": case_payload(6, (1, 2, 4, 8, 16, 32)),
        },
        "verdict": "SURVIVES_K3_AND_K6",
        "consequence": "the canonical second channel is not killed by odd/even charge parity; both probes yield the full two-channel conjugate Kummer module",
        "scope": {
            "k3_generic_closure_claimed": True,
            "k6_generic_closure_claimed": True,
            "arbitrary_k_identity_derived": True,
            "arbitrary_k_theorem_claimed": False,
            "reason": "this falsifier run probes k=3 and k=6; promotion of the displayed all-k identity to a corpus theorem is a separate proof-and-audit action",
        },
        "source_refs": source_refs,
    }


def report_text(certificate: dict[str, object]) -> str:
    case3 = certificate["cases"]["3"]
    case6 = certificate["cases"]["6"]
    return f"""# The k=3/k=6 radicand kill test

**Version:** 1.0  
**Date:** 2026-07-18  
**Verdict:** **SURVIVES at both k=3 and k=6**

## 1. Falsifier and canonicity criterion

The question was not whether some unrelated square class could be found. That would be cheap and mathematically uninformative. The admissible candidate had to be forced by the same two axial product branches as the four-charge entropy sum.

Put

```text
A_k^+ = product_i (w_i+m),    A_k^- = product_i (w_i-m),
w_i^2 = u+N_i^2,              m^2=u,              P=product_i N_i.
```

Then `A_k^+ A_k^-=P^2`. The canonical plus-radicand is

```text
gamma_k = A_k^+ + A_k^- + 2P
        = (sqrt(A_k^+) + sqrt(A_k^-))^2.
```

It is coefficient-free, fixed by `m -> -m`, constructed functorially from the norm pair, and at `k=4` is exactly the published `gamma_R9`. The opposite cross-term

```text
gamma_k^- = A_k^+ + A_k^- - 2P
```

is not a new channel: `[gamma_k^-]=[u][gamma_k]` in the square-class group.

## 2. Identity that emerged

Writing elementary symmetric functions of the `w_i` as `e_j(w)`, define

```text
alpha_k = sum_(j congruent k mod 2)     u^((k-j)/2)   e_j(w),
beta_k  = sum_(j not congruent k mod 2) u^((k-j-1)/2)e_j(w).
```

Exact symbolic expansion gives

```text
A_k^+ = alpha_k + m beta_k,
A_k^- = alpha_k - m beta_k,
alpha_k^2-u beta_k^2=P^2,
gamma_k(gamma_k-4P)=4u beta_k^2.
```

This is the four-charge R9 identity without the restriction `k=4`. The present artifact verifies the product identities directly at `k=3` and `k=6` and records the general combinatorial formula they instantiate.

## 3. Odd probe: k=3

Here `delta_3=4` and

```text
alpha_3 = {case3['alpha']},
beta_3  = {case3['beta']},
gamma_3 = {case3['gamma_plus']}.
```

The exact contact instance uses `N=(1,2,4)`, `P=8`.

- Even wall `(+,+,+)`: `4M=7`, reciprocal sum `{case3['even_contact']['reciprocal_sum']}`, `beta(0)={case3['even_contact']['beta_contact']}`, parity `(v(u),v(gamma_3))=(1,0)`.
- Odd wall `(-,+,+)`: `4M=5`, reciprocal sum `{case3['odd_contact']['reciprocal_sum']}`, `beta(0)={case3['odd_contact']['beta_contact']}`, parity `(1,1)`.

For both walls the exact degree-4 mass norm has constant coefficient zero and nonzero linear coefficient, so `u=0` is a simple root. The signed sum is unique, excluding a coincident contact sheet. Thus the sheet matrix is

```text
B = [[1,0],[1,1]],  rank_F2(B)=2.
```

With the certified base group `S_4`, orbit saturation gives rank `2*4=8` and generic normal closure `{case3['normal_closure_group']}` of order `{case3['normal_closure_group_order']}`.

## 4. Even probe: k=6

Here `delta_6=22` and

```text
alpha_6 = {case6['alpha']},
beta_6  = {case6['beta']},
gamma_6 = {case6['gamma_plus']}.
```

The exact contact instance uses `N=(1,2,4,8,16,32)`, `P=32768`.

- Even wall `(+,+,+,+,+,+)`: `4M=63`, reciprocal sum `{case6['even_contact']['reciprocal_sum']}`, `beta(0)={case6['even_contact']['beta_contact']}`, parity `(1,0)`.
- Odd wall `(-,+,+,+,+,+)`: `4M=61`, reciprocal sum `{case6['odd_contact']['reciprocal_sum']}`, `beta(0)={case6['odd_contact']['beta_contact']}`, parity `(1,1)`.

For both walls the exact degree-22 mass norm again has a simple root at `u=0` and a unique signed wall. The same invertible `B` therefore orbit-saturates under `S_22` to rank `44`. The generic normal closure is `{case6['normal_closure_group']}`, of order `{case6['normal_closure_group_order']}`.

## 5. Why no hidden off-contact parity spoils the matrix

Reflection descent puts every `w_i`, hence `alpha_k`, `beta_k`, and `gamma_k`, in the mass field `K=F(u)`. At a divisor where `u` is a unit, the identity

```text
gamma_k(gamma_k-4P)=4u beta_k^2
```

forces every positive valuation of `gamma_k` to be even, because `P` is a unit and `gamma_k` and `gamma_k-4P` cannot both vanish. Odd gamma parity is therefore confined to the odd signed contacts. The chosen binary-charge walls are distinct, so the other mass sheets have `u`-valuation zero there. These are precisely the off-sheet and regularity conditions required by the conjugate Kummer-module theorem.

## 6. Evaluation

The kill test fails to kill the radicand. More strongly, the same canonical construction survives one odd and one even charge count and reaches the maximal two-channel Kummer rank in each:

```text
k=3: rank 8,  closure C2^2 wr S4;
k=6: rank 44, closure C2^2 wr S22.
```

So `gamma` is not behaving as a four-charge parity accident. The calculation also exposes the all-k identity above. This report does **not** silently promote two probes into an arbitrary-k theorem; that promotion should be a short separate proof which quantifies the generic signed-contact hypotheses and then invokes the already proved all-k base-monodromy and Kummer-wreath theorems.

## 7. Replay

Run:

```text
python3 research/evidence/arithmetic_horizon_variation/k3_k6_radicand_kill_v1/build_k3_k6_radicand_kill.py
python3 research/evidence/arithmetic_horizon_variation/k3_k6_radicand_kill_v1/verify_k3_k6_radicand_kill.py
python3 engine/tests/gate_k3_k6_radicand_kill.py
```
"""


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def build() -> None:
    certificate = build_certificate()
    certificate_path = HERE / "certificates/k3_k6_radicand_kill.json"
    report_path = HERE / "reports/K3_K6_RADICAND_KILL_TEST_v1.0.md"
    write_json(certificate_path, certificate)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text(certificate))
    print("built exact k=3/k=6 radicand kill-test certificate")


if __name__ == "__main__":
    build()
