"""Unsigned non-restoring division with a fixed-width register trace."""

from integer_machine.models import DivisionResult, DivisionStep
from integer_machine.parsing import (
    InputValidationError,
    format_bits,
    format_register_bits,
    format_twos_complement,
    validate_width,
)


def divide_unsigned(dividend: int, divisor: int, width: int) -> DivisionResult:
    """Divide two unsigned operands with the non-restoring A,Q,M algorithm."""
    validate_width(width)
    limit = 1 << width
    if not 0 <= dividend < limit or not 0 <= divisor < limit:
        raise InputValidationError(f"Both operands must fit in {width} unsigned bits.")
    if divisor == 0:
        raise InputValidationError("The divisor must not be zero.")

    a_width = width + 1
    mask = limit - 1
    a, q, m = 0, dividend, divisor
    steps = [
        DivisionStep(
            cycle=0,
            phase="Initial",
            action="Initial registers",
            a_before=format_twos_complement(a, a_width),
            q_before=format_bits(q, width),
            a_after_shift="—",
            q_after_shift="—",
            a_after_operation="—",
            q_bit="—",
            a_after=format_twos_complement(a, a_width),
            q_after=format_bits(q, width),
        )
    ]

    for cycle in range(1, width + 1):
        a_before, q_before = a, q
        was_nonnegative = a >= 0
        incoming_q_bit = (q >> (width - 1)) & 1
        a = (a << 1) | incoming_q_bit
        q = (q << 1) & mask
        a_after_shift, q_after_shift = a, q

        if was_nonnegative:
            a -= m
            action = "Previous A ≥ 0: shift A,Q left, then subtract M"
        else:
            a += m
            action = "Previous A < 0: shift A,Q left, then add M"
        a_after_operation = a

        q_bit = 1 if a >= 0 else 0
        q |= q_bit
        steps.append(
            DivisionStep(
                cycle=cycle,
                phase="Cycle",
                action=action,
                a_before=format_twos_complement(a_before, a_width),
                q_before=format_bits(q_before, width),
                a_after_shift=format_register_bits(a_after_shift, a_width),
                q_after_shift=format_bits(q_after_shift, width),
                a_after_operation=format_twos_complement(a_after_operation, a_width),
                q_bit=str(q_bit),
                a_after=format_twos_complement(a, a_width),
                q_after=format_bits(q, width),
            )
        )

    if a < 0:
        before_restore = a
        a += m
        steps.append(
            DivisionStep(
                cycle=width + 1,
                phase="Final restoration",
                action="A < 0 after the last cycle, so add M once",
                a_before=format_twos_complement(before_restore, a_width),
                q_before=format_bits(q, width),
                a_after_shift="—",
                q_after_shift="—",
                a_after_operation=format_twos_complement(a, a_width),
                q_bit="—",
                a_after=format_twos_complement(a, a_width),
                q_after=format_bits(q, width),
            )
        )

    return DivisionResult(
        width=width,
        dividend=dividend,
        divisor=divisor,
        quotient=q,
        remainder=a,
        quotient_bits=format_bits(q, width),
        remainder_bits=format_bits(a, width),
        steps=tuple(steps),
    )
