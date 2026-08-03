"""Immutable result models for fixed-width integer conversion."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RepresentationOutcome:
    """The result of interpreting a value in one representation."""

    label: str
    minimum: int
    maximum: int
    bits: str | None
    error: str | None

    @property
    def fits(self) -> bool:
        """Whether the value can be represented in this format."""
        return self.bits is not None


@dataclass(frozen=True)
class ConversionResult:
    """Both fixed-width interpretations of one decimal value."""

    value: int
    width: int
    unsigned: RepresentationOutcome
    signed: RepresentationOutcome


@dataclass(frozen=True)
class MultiplicationStep:
    """One recorded cycle of unsigned sequential multiplication."""

    cycle: int
    q0: str
    action: str
    c_before: str
    a_before: str
    q_before: str
    addition_result: str
    c_after: str
    a_after: str
    q_after: str


@dataclass(frozen=True)
class MultiplicationResult:
    """The fixed-width product and register trace of a multiplication."""

    width: int
    multiplicand: int
    multiplier: int
    product: int
    product_bits: str
    steps: tuple[MultiplicationStep, ...]


# ===== ADD THESE NEW CLASSES =====
@dataclass(frozen=True)
class SignedMultiplicationStep:
    """One recorded cycle of Booth's signed sequential multiplication."""
    cycle: int
    q0: str
    q_minus_1: str
    action: str
    a_before: str
    q_before: str
    a_after_operation: str
    a_after: str
    q_after: str
    q_minus_1_after: str


@dataclass(frozen=True)
class SignedMultiplicationResult:
    """The fixed-width product and register trace of Booth's multiplication."""
    width: int
    multiplicand: int
    multiplier: int
    product: int
    product_bits: str
    steps: tuple[SignedMultiplicationStep, ...]
# ===== END ADDED CLASSES =====


@dataclass(frozen=True)
class DivisionStep:
    """One recorded phase of unsigned non-restoring division."""

    cycle: int
    phase: str
    action: str
    a_before: str
    q_before: str
    a_after_shift: str
    q_after_shift: str
    a_after_operation: str
    q_bit: str
    a_after: str
    q_after: str


@dataclass(frozen=True)
class DivisionResult:
    """The quotient, remainder, and register trace of a division."""

    width: int
    dividend: int
    divisor: int
    quotient: int
    remainder: int
    quotient_bits: str
    remainder_bits: str
    steps: tuple[DivisionStep, ...]