"""Conservative structural route recognizers."""

from __future__ import annotations

from typing import Callable

from .contact import CONTACT_RESTRICTION_CONTRACT, recognize_contact_restriction
from .contact_orbit import CONTACT_ORBIT_CONTRACT, recognize_contact_orbit

__all__ = [
    "CONTACT_ORBIT_CONTRACT",
    "CONTACT_RESTRICTION_CONTRACT",
    "recognize_contact_orbit",
    "recognize_contact_restriction",
    "register_corpus_providers",
]

# Modules holding corpus-derived providers; each exposes a PROVIDERS tuple.
_CORPUS_PROVIDER_MODULES: tuple[str, ...] = (
    "dbp_native",
    "rewrite",
    "triangular",
    "complete_intersection",
    "elimination",
    "finite_extension",
    "modular_groebner",
    "realization",
    "kummer",
    "wreath",
    "cover",
    "inertia_strata",
    "curvature",
    "local_germ",
    "real",
)


def register_corpus_providers(register: Callable[[object], None]) -> None:
    """Register every corpus-derived provider module's PROVIDERS tuple."""

    import importlib

    for module_name in _CORPUS_PROVIDER_MODULES:
        module = importlib.import_module(f".{module_name}", __name__)
        for provider in module.PROVIDERS:
            register(provider)
