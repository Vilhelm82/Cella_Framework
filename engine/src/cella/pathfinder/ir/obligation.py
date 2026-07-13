"""Mathematical obligation labels carried by a route."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Obligation:
    obligation_id: str
    statement: str
    warrant_level: str

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.obligation_id, self.statement, self.warrant_level)):
            raise ValueError("obligation id, statement, and warrant level must be non-empty")
