"""Integer Machine simulator package."""

from integer_machine.conversion import convert_decimal
from integer_machine.division import divide_unsigned
from integer_machine.models import (
    ConversionResult,
    DivisionResult,
    DivisionStep,
    MultiplicationResult,
    MultiplicationStep,
    RepresentationOutcome,
)
from integer_machine.multiplication import multiply_unsigned

__all__ = [
    "ConversionResult",
    "DivisionResult",
    "DivisionStep",
    "MultiplicationResult",
    "MultiplicationStep",
    "RepresentationOutcome",
    "convert_decimal",
    "divide_unsigned",
    "multiply_unsigned",
]
