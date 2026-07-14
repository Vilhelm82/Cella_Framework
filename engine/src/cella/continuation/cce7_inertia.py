"""Source-locked normalized-incidence and generic inertia import for CCE-7."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .canonical import canonical_digest, canonical_json_bytes
from .model import Refusal


SOURCE_LOCKS = (
    ("paper_iv", "research/paper/Theorems/DBP/galois_horizon_cover_v1_0.tex", "777daf7b60d337709587606f0974f8d4c8ff9c79473b609aadd54827223613ce"),
    ("incidence_model", "docs/files/horizon_wreath_inertia_model.m2", "d7940c05f9021b211fad4bb0546504ee91b7e9135c28ef1ba9fcd6a1d3199d46"),
    ("run_report", "docs/galois_horizon_cover_v1_0_publication_package/certificates/m2_out_2026-07-10/REALIZATION_POSET_RUN_REPORT_2026-07-10.md", "5704c21d7e854a3789976d7053d86943a408e68fa04eb965896b93e7e693711f"),
    ("inertia_report", "docs/galois_horizon_cover_v1_0_publication_package/supporting_reports/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md", "5f3d1c65a6b07274611a386ee000cfb0cb411ead946cdd38dce600baa12ae9d0"),
    ("difference_decomposition", "docs/galois_horizon_cover_v1_0_publication_package/certificates/m2_out_2026-07-10/stage3_IZ_decomp.out.txt", "69accab83102118e8c23d7c0cf0f26615dfdddab4f78ac17d4748c8d485e5dfa"),
    ("realization_table", "docs/galois_horizon_cover_v1_0_publication_package/certificates/m2_out_2026-07-10/stage4_table.out.txt", "fe937841324760dd7f7a17547cc7c006a384b8e4e891e18caf83629367921666"),
)


def _source_ledger() -> tuple[tuple[str, str], ...]:
    import hashlib

    root = Path(__file__).parents[4]
    ledger = []
    for name, relative, expected in SOURCE_LOCKS:
        path = root / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"normalized-incidence source lock failed: {name}")
        ledger.append((name, expected))
    return tuple(ledger)


@dataclass(frozen=True, slots=True)
class NormalizedIncidenceInertiaCertificate:
    schema_id: str
    schema_version: str
    source_ledger: tuple[tuple[str, str], ...]
    implementation_ledger: tuple[tuple[str, str], ...]
    incidence_equations: tuple[str, ...]
    relative_jacobian: str
    branch_rule: str
    generic_inertia: tuple[tuple[str, str], ...]
    realized_strata: tuple[tuple[str, int, int], ...]
    eliminant_guard: str
    promoted_scope: str
    active_obligation: str
    certificate_digest: str


def normalized_incidence_inertia_certificate() -> NormalizedIncidenceInertiaCertificate:
    import hashlib

    unsigned = {
        "schema_id": "cella.continuation.cce7_normalized_incidence_inertia",
        "schema_version": "1.0",
        "source_ledger": _source_ledger(),
        "implementation_ledger": (("cce7_inertia_runtime", hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),),
        "incidence_equations": (
            "w1^2-u-N1^2=0", "w2^2-u-N2^2=0",
            "w3^2-u-N3^2=0", "w4^2-u-N4^2=0",
            "w1+w2+w3+w4-4M=0",
        ),
        "relative_jacobian": "8*e3(w1,w2,w3,w4)",
        "branch_rule": "away from residue characteristic 2, Kummer inertia flips exactly the square roots with odd valuation",
        "generic_inertia": (
            ("simple_mass_branch", "C2:uncolored_transposition"),
            ("even_signed_contact", "C2:axial_(1,0,0)"),
            ("odd_signed_contact", "C2:axial_sum_(1,1,0)"),
            ("rotating_difference", "C2:difference_(0,0,1)"),
            ("reciprocal_sub_balance", "C4:colored_transposition"),
            ("J=0", "unramified_relation_rank_drop"),
            ("generic_weighted_infinity", "unramified_even_parity"),
            ("equal_squared_charges", "unramified_normalized_sheet_crossing"),
        ),
        "realized_strata": (
            ("mass_ramification", 1, 48),
            ("even_or_odd_contact", 1, 2),
            ("rotating_difference", 1, 64),
            ("mass_ramification+rotating_difference", 2, 192),
            ("reciprocal_sub_balance", 2, 6),
            ("contact+rotating_difference", 2, 8),
            ("mass_ramification+contact+rotating_difference", 3, 24),
        ),
        "eliminant_guard": "projected quintic discriminant has squared factors from unramified crossings; only normalized-incidence ramification is admitted",
        "promoted_scope": "normalized incidence definition, genuine branch ideal, generic inertia catalogue, and stored realization-poset theorem",
        "active_obligation": "construct exact complex loop representatives and prove their braid action/naturality with CCE-5 transport",
    }
    return NormalizedIncidenceInertiaCertificate(**unsigned, certificate_digest=canonical_digest(unsigned))


def verify_normalized_incidence_inertia_certificate(
    certificate: NormalizedIncidenceInertiaCertificate,
) -> bool | Refusal:
    try:
        expected = normalized_incidence_inertia_certificate()
    except ValueError as error:
        return Refusal("StageDependencyUnavailable", "normalized_incidence_source_lock", "cella.continuation.cce7.inertia.verify", False, True, str(error))
    if canonical_json_bytes(expected) != canonical_json_bytes(certificate):
        return Refusal("InertiaCertificateMismatch", "normalized_incidence_replay", "cella.continuation.cce7.inertia.verify", False, False, "certificate bytes do not replay")
    return True


__all__ = [
    "NormalizedIncidenceInertiaCertificate",
    "normalized_incidence_inertia_certificate",
    "verify_normalized_incidence_inertia_certificate",
]
