"""Markdown certificate reports assembled from result envelopes."""

from __future__ import annotations

from .spec import ProblemSpec


def _gate_table(gates: list[dict]) -> str:
    lines = ["| scope | gate | pass | value |", "|---|---|---|---|"]
    for g in gates:
        scope = g.get("divisor") or g.get("name") or "structural"
        if g.get("channel"):
            scope += f" / {g['channel']}"
        value = g.get("value", "")
        mark = "PASS" if g.get("pass") else ("FAIL" if g.get("pass") is False else "-")
        lines.append(f"| {scope} | {g.get('gate')} | {mark} | {value} |")
    return "\n".join(lines)


def render(ps: ProblemSpec, verify_env: dict | None = None,
           lift_env: dict | None = None, inertia_env: dict | None = None,
           realize_env: dict | None = None) -> str:
    out = [
        f"# Wreath Engine report — {ps.name}",
        "",
        f"- spec hash: `{ps.content_hash()}`",
        f"- base cover: degree {ps.d}, group {ps.base_cover.group.name} "
        f"(order {ps.base_cover.group.order}; claimed by "
        f"{ps.base_cover.group.claimed_by})",
        f"- channels (s={ps.s}): " + ", ".join(c.name for c in ps.channels),
        f"- divisors: " + ", ".join(f"{d.name}[{','.join(map(str, d.claimed_parity_row))}]"
                                    for d in ps.divisors),
        "",
    ]
    lift = lift_env or verify_env
    if lift:
        out += ["## Wreath lift", "", f"**Status: {lift.get('status')}**", ""]
        if lift.get("maximal_rank"):
            out += [
                f"- sheet-level matrix B rank: {lift.get('sheet_matrix_rank')} (invertible)",
                f"- orbit matrix rank (B tensor I_{ps.d}): {lift.get('orbit_matrix_rank')}",
                f"- Kummer rank rho = {lift.get('kummer_rank')}",
                f"- [H : K] = {lift.get('index_H_over_K')}, "
                f"[L : E] = {lift.get('index_L_over_E')}",
                f"- **Gal(L/F) = {lift.get('closure_group')}**, "
                f"order {lift.get('closure_order')}",
                "",
            ]
        elif "kernel_basis" in lift:
            out += [
                f"- sheet-level matrix B rank: {lift.get('sheet_matrix_rank')} "
                "(rank-deficient)",
                f"- kernel basis (square-class relation module): "
                f"{lift.get('kernel_basis')}",
                f"- {lift.get('kernel_note', '')}",
                "",
            ]
    if verify_env and verify_env.get("gates"):
        out += ["## Verification gates",
                "", f"run: `{verify_env.get('run_id')}` "
                f"({verify_env.get('elapsed_seconds', '?')}s)", "",
                _gate_table(verify_env["gates"]), ""]
        if verify_env.get("failed_gates"):
            out += ["### Failed gates", ""]
            out += [f"- {g}" for g in verify_env["failed_gates"]] + [""]
    if inertia_env:
        out += ["## Colored inertia table", "",
                "| divisor | type | sign vector | order | base cycles | action |",
                "|---|---|---|---|---|---|"]
        for row in inertia_env.get("inertia_table", []):
            out.append(
                f"| {row['divisor']} | {row['type']} | {row['sign_vector']} | "
                f"{row['kummer_inertia_order']} | {row['base_cycles']} | "
                f"{row['action']} |")
        out.append("")
    if realize_env:
        out += ["## Realization poset", "",
                f"run: `{realize_env.get('run_id')}` — status "
                f"{realize_env.get('status')}", ""]
        walls = realize_env.get("contact_walls", [])
        if walls:
            out += ["contact walls: " + ", ".join(
                f"{w.get('stratum')}={'ok' if w.get('pass') else 'FAIL'}"
                for w in walls), ""]
        table = realize_env.get("incidence_table", [])
        if table:
            out += ["| stratum | codim in X | degree | empty (generic) |",
                    "|---|---|---|---|"]
            out += [f"| {r.get('stratum')} | {r.get('codim_in_X')} | "
                    f"{r.get('degree')} | {r.get('empty_generic')} |"
                    for r in table]
            out.append("")
        for d in realize_env.get("decompositions", []):
            if d.get("stage") == "channel_min_primes":
                out.append(f"- channel `{d.get('stratum')}`: "
                           f"{d.get('value')} minimal prime(s), "
                           f"degrees {d.get('degrees')}")
            if d.get("stage") == "channel_primary_decomp" and d.get("is_prime_ideal"):
                out.append(f"- channel `{d.get('stratum')}` divisor ideal is prime")
        out.append("")
    if verify_env and verify_env.get("certificate_files"):
        out += ["## Certificates", ""]
        out += [f"- `{f}`" for f in verify_env["certificate_files"]]
        out.append("")
    return "\n".join(out)
