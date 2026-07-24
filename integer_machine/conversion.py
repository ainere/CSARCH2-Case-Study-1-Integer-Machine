"""Independent signed and unsigned fixed-width conversion."""

from integer_machine.models import ConversionResult, RepresentationOutcome
from integer_machine.parsing import format_bits, format_twos_complement, validate_width


def convert_decimal(value: int, width: int) -> ConversionResult:
    """Convert a decimal integer to unsigned and signed bit representations."""
    validate_width(width)
    unsigned_minimum, unsigned_maximum = 0, (1 << width) - 1
    signed_minimum = -(1 << (width - 1))
    signed_maximum = (1 << (width - 1)) - 1

    unsigned_fits = unsigned_minimum <= value <= unsigned_maximum
    signed_fits = signed_minimum <= value <= signed_maximum

    unsigned = RepresentationOutcome(
        label="Unsigned",
        minimum=unsigned_minimum,
        maximum=unsigned_maximum,
        bits=format_bits(value, width) if unsigned_fits else None,
        error=None if unsigned_fits else f"{value} is outside the unsigned range.",
    )
    signed = RepresentationOutcome(
        label="Signed two's complement",
        minimum=signed_minimum,
        maximum=signed_maximum,
        bits=format_twos_complement(value, width) if signed_fits else None,
        error=None if signed_fits else f"{value} is outside the signed range.",
    )
    return ConversionResult(value=value, width=width, unsigned=unsigned, signed=signed)
