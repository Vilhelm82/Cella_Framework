"""Immutable source, compiler, result, and refusal records."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


THEOREM_VERSION = "DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1"
ROUTE_VERSION = "DBP_NATIVE_RELATIVE_PERIOD_ROUTE_THEOREM_v1.0"


@dataclass(frozen=True, slots=True)
class CurveRecord:
    id: str = "E128"
    coefficients: tuple[int, int, int, int, int] = (0, -1, 0, 1, -1)
    factorization: str = "(X - 1)*(X^2 + 1)"


@dataclass(frozen=True, slots=True)
class DifferentialRecord:
    id: str = "Theta"
    expression: str = "8*(X - 3)/(X + 7) * dX/Y"


@dataclass(frozen=True, slots=True)
class RelativePathRecord:
    start: str
    end: str
    orientation: str
    sheet: str | None
    prescription: str


PRIMARY_PATH = RelativePathRecord("X=1", "X=+infinity", "increasing_X", "Y>0 for X>1", "ordinary")
DUAL_PATH = RelativePathRecord(
    "X=1", "X=-infinity", "decreasing_X",
    "Y=+i*sqrt(-(X-1)*(X^2+1)) for X<1", "real_cauchy_principal_value",
)


@dataclass(frozen=True, slots=True)
class SourceRecord:
    curve: CurveRecord = CurveRecord()
    differential: DifferentialRecord = DifferentialRecord()
    path: RelativePathRecord = PRIMARY_PATH


@dataclass(frozen=True, slots=True)
class CompiledKernel:
    route_id: str
    kernel_id: str
    radicand: str
    expression: str
    domain_witnesses: tuple[str, ...]
    source_ledger: dict[str, Any]
    theorem_version: str = THEOREM_VERSION
    route_version: str = ROUTE_VERSION


@dataclass(frozen=True, slots=True)
class DyadicBracket:
    lower_numerator: int
    upper_numerator: int
    denominator_exponent: int
    width_bits: int
    rounded_value_bits: int

    def to_record(self):
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PeriodRefusal:
    token: str
    stage: str
    detail: str
    first_unclosed_obligation: str

    def to_record(self):
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CertifiedPeriodResult:
    target: str
    dyadic_bracket: DyadicBracket
    rounded_value: str
    route_id: str
    source_ledger: dict[str, Any]
    account_ledger: dict[str, Any]
    remainder_ledger: dict[str, Any]
    certificate_digest: str
    certificate_record: dict[str, Any] | None

    def to_record(self):
        return asdict(self)
