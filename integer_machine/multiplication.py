"""Unsigned sequential add-and-shift multiplication."""

from integer_machine.models import MultiplicationResult, MultiplicationStep
from integer_machine.parsing import InputValidationError, format_bits, validate_width


def multiply_unsigned(multiplicand: int, multiplier: int, width: int) -> MultiplicationResult:
    """Multiply two unsigned fixed-width operands using ``C,A,Q,M`` registers."""
    validate_width(width)
    limit = 1 << width
    if not 0 <= multiplicand < limit or not 0 <= multiplier < limit:
        raise InputValidationError(f"Both operands must fit in {width} unsigned bits.")

    mask = limit - 1
    c, a, q, m = 0, 0, multiplier, multiplicand
    steps = [
        MultiplicationStep(
            cycle=0,
            q0="—",
            action="Initial registers",
            c_before="0",
            a_before=format_bits(a, width),
            q_before=format_bits(q, width),
            addition_result="—",
            c_after="0",
            a_after=format_bits(a, width),
            q_after=format_bits(q, width),
        )
    ]

    for cycle in range(1, width + 1):
        c_before, a_before, q_before = c, a, q
        q0 = q & 1
        if q0:
            total = a + m
            c, a = (total >> width) & 1, total & mask
            action = "Q₀ = 1: add M to A, then shift C,A,Q right"
            addition_result = format(total, f"0{width + 1}b")
        else:
            c = 0
            action = "Q₀ = 0: keep A, then shift C,A,Q right"
            addition_result = format(a, f"0{width + 1}b")

        combined = (c << (width * 2)) | (a << width) | q
        shifted = combined >> 1
        c = (shifted >> (width * 2)) & 1
        a = (shifted >> width) & mask
        q = shifted & mask
        steps.append(
            MultiplicationStep(
                cycle=cycle,
                q0=str(q0),
                action=action,
                c_before=str(c_before),
                a_before=format_bits(a_before, width),
                q_before=format_bits(q_before, width),
                addition_result=addition_result,
                c_after=str(c),
                a_after=format_bits(a, width),
                q_after=format_bits(q, width),
            )
        )

    product = (a << width) | q
    return MultiplicationResult(
        width=width,
        multiplicand=multiplicand,
        multiplier=multiplier,
        product=product,
        product_bits=format_bits(product, width * 2),
        steps=tuple(steps),
    )
