"""Validation and fixed-width formatting helpers for machine inputs."""

import re
from typing import Literal

InputBase = Literal["decimal", "binary"]
_DECIMAL_PATTERN = re.compile(r"[+-]?\d+")


class InputValidationError(ValueError):
    """An expected problem with user-entered machine input."""


def validate_width(width: int) -> int:
    if isinstance(width, bool) or not isinstance(width, int) or width < 2:
        raise InputValidationError("Data size must be an integer of at least 2 bits.")
    return width


def parse_decimal(text: str) -> int:
    normalized = text.strip()
    if not normalized:
        raise InputValidationError("Enter a decimal integer.")
    if _DECIMAL_PATTERN.fullmatch(normalized) is None:
        raise InputValidationError("Use decimal digits with an optional leading + or -.")
    return int(normalized, 10)


def normalize_binary(text: str) -> str:
    normalized = "".join(text.split()).replace("_", "")
    if normalized.lower().startswith("0b"):
        normalized = normalized[2:]
    if not normalized:
        raise InputValidationError("Enter a binary value.")
    if any(character not in "01" for character in normalized):
        raise InputValidationError("Binary input may contain only 0 and 1.")
    return normalized


def parse_unsigned_operand(text: str, base: InputBase, width: int) -> int:
    validate_width(width)
    if base == "decimal":
        value = parse_decimal(text)
    elif base == "binary":
        bits = normalize_binary(text)
        if len(bits) > width:
            raise InputValidationError(f"Binary input exceeds the selected {width}-bit size.")
        value = int(bits, 2)
    else:
        raise InputValidationError("Choose Decimal or Binary input.")
    if value < 0:
        raise InputValidationError("Arithmetic operands must be unsigned.")
    if value >= 1 << width:
        raise InputValidationError(f"Value does not fit in {width} unsigned bits.")
    return value


def parse_signed_operand(text: str, base: InputBase, width: int) -> int:
    """Parse a signed decimal or binary operand that fits in width bits."""
    validate_width(width)
    if base == "decimal":
        value = parse_decimal(text)
    elif base == "binary":
        bits = normalize_binary(text)
        if len(bits) > width:
            raise InputValidationError(f"Binary input exceeds the selected {width}-bit size.")
        value = int(bits, 2)
        # Handle two's complement for binary input
        if len(bits) == width and bits[0] == '1':
            value = value - (1 << width)
    else:
        raise InputValidationError("Choose Decimal or Binary input.")
    
    # Check signed range
    lower = -(1 << (width - 1))
    upper = (1 << (width - 1)) - 1
    if not lower <= value <= upper:
        raise InputValidationError(
            f"Value {value} does not fit in {width}-bit signed range ({lower} to {upper})."
        )
    return value


def format_bits(value: int, width: int) -> str:
    """Format an unsigned value as fixed-width bits."""
    validate_width(width)
    if value < 0 or value >= 1 << width:
        raise ValueError(f"{value} cannot be formatted as {width} unsigned bits")
    return format(value, f"0{width}b")


def format_signed_bits(value: int, width: int) -> str:
    """Format a signed integer as fixed-width two's complement bits."""
    validate_width(width)
    lower = -(1 << (width - 1))
    upper = (1 << (width - 1)) - 1
    if not lower <= value <= upper:
        raise ValueError(f"{value} cannot be formatted as {width}-bit signed value")
    return format(value & ((1 << width) - 1), f"0{width}b")


def format_twos_complement(value: int, width: int) -> str:
    """Alias for format_signed_bits (for backwards compatibility)."""
    return format_signed_bits(value, width)


def format_register_bits(value: int, width: int) -> str:
    """Format a register value as fixed-width bits (unsigned mask)."""
    validate_width(width)
    return format(value & ((1 << width) - 1), f"0{width}b")


def group_bits(bits: str, size: int = 4) -> str:
    first_group = len(bits) % size or size
    groups = [bits[:first_group]]
    groups.extend(bits[index : index + size] for index in range(first_group, len(bits), size))
    return " ".join(groups)