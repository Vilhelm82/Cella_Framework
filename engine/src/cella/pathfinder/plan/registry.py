"""Route-provider registry.

Every provider exposes its recognition predicate, contract (hypotheses,
evidence requirements, invariants, obligations, refusal conditions, wrapper
capability requirements), and the native scouts that gather its route
evidence.  The registry contains route discovery only, never host executors.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..scout.protocol import Scout

Recognizer = Callable[[PathfinderRequest], RecognitionOutcome]


@dataclass(frozen=True, slots=True)
class RouteProvider:
    route_family: str
    contract: RouteContract
    recognizer: Recognizer
    native_scouts: tuple[Scout, ...] = ()
    wrapper_capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.route_family != self.contract.route_family:
            raise ValueError("provider family must match its contract")


PROVIDERS: dict[str, RouteProvider] = {}


def register_provider(provider: RouteProvider) -> None:
    if provider.route_family in PROVIDERS:
        raise ValueError(f"duplicate route provider: {provider.route_family}")
    PROVIDERS[provider.route_family] = provider


def _register_builtin_providers() -> None:
    from ..recognize.contact import CONTACT_RESTRICTION_CONTRACT, recognize_contact_restriction
    from ..recognize.contact_orbit import CONTACT_ORBIT_CONTRACT, recognize_contact_orbit

    register_provider(
        RouteProvider(
            route_family="contact_restriction",
            contract=CONTACT_RESTRICTION_CONTRACT,
            recognizer=recognize_contact_restriction,
            wrapper_capabilities=("signed_contact_substitution", "linear_wall_solve"),
        )
    )
    register_provider(
        RouteProvider(
            route_family="signed_contact_orbit_projection",
            contract=CONTACT_ORBIT_CONTRACT,
            recognizer=recognize_contact_orbit,
            wrapper_capabilities=("signed_contact_substitution", "sign_orbit_enumeration"),
        )
    )

    # Corpus-derived providers register themselves through the recognize package.
    from ..recognize import register_corpus_providers

    register_corpus_providers(register_provider)


_register_builtin_providers()

# Compatibility view used by existing callers and tests.
RECOGNIZERS: dict[str, Recognizer] = {
    family: provider.recognizer for family, provider in PROVIDERS.items()
}
