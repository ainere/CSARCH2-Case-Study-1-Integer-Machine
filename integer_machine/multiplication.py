"""Signed sequential-circuit binary multiplier (Booth's algorithm, A/Q/Q-1/M registers).

This matches "Machine 1" spec's requirement for a "sequential circuit binary
multiplier" and reproduces the professor's Try #4 worked trace (27 * 7 = 189)
cycle for cycle: each pass inspects (Q0, Q-1), does A-M / A+M / no-op, then
arithmetically shifts A:Q:Q-1 right by one bit. After `width` passes, the
concatenation A:Q is the 2*width-bit signed product.
"""

from integer_machine.models import SignedMultiplicationResult, SignedMultiplicationStep
from integer_machine.parsing import InputValidationError, format_register_bits, validate_width


def multiply_signed(multiplicand: int, multiplier: int, width: int) -> SignedMultiplicationResult:
    """Multiply two signed fixed-width operands using the ``A, Q, Q-1, M`` sequential circuit."""
    validate_width(width)
    lower = -(1 << (width - 1))
    upper = (1 << (width - 1)) - 1
    if not lower <= multiplicand <= upper or not lower <= multiplier <= upper:
        raise InputValidationError(
            f"Both operands must fit in {width}-bit signed range ({lower} to {upper})."
        )

    mask = (1 << width) - 1
    m = multiplicand & mask
    a = 0
    q = multiplier & mask
    q_minus_1 = 0

    steps = [
        SignedMultiplicationStep(
            cycle=0,
            q0="—",
            q_minus_1=str(q_minus_1),
            action="Initial registers",
            a_before=format_register_bits(a, width),
            q_before=format_register_bits(q, width),
            a_after_operation="—",
            a_after=format_register_bits(a, width),
            q_after=format_register_bits(q, width),
            q_minus_1_after=str(q_minus_1),
        )
    ]

    for cycle in range(1, width + 1):
        a_before, q_before, q_minus_1_before = a, q, q_minus_1
        q0 = q & 1

        if q0 == 1 and q_minus_1 == 0:
            a = (a - m) & mask
            action = "Q₀Q₋₁ = 10: A = A − M"
        elif q0 == 0 and q_minus_1 == 1:
            a = (a + m) & mask
            action = "Q₀Q₋₁ = 01: A = A + M"
        else:
            action = f"Q₀Q₋₁ = {q0}{q_minus_1}: no operation (copy)"
        a_after_operation = a

        # Arithmetic shift right of the concatenated A:Q:Q-1 register
        sign_bit = (a >> (width - 1)) & 1
        new_q_minus_1 = q & 1
        new_q = ((q >> 1) | ((a & 1) << (width - 1))) & mask
        new_a = ((a >> 1) | (sign_bit << (width - 1))) & mask
        a, q, q_minus_1 = new_a, new_q, new_q_minus_1

        steps.append(
            SignedMultiplicationStep(
                cycle=cycle,
                q0=str(q0),
                q_minus_1=str(q_minus_1_before),
                action=action,
                a_before=format_register_bits(a_before, width),
                q_before=format_register_bits(q_before, width),
                a_after_operation=format_register_bits(a_after_operation, width),
                a_after=format_register_bits(a, width),
                q_after=format_register_bits(q, width),
                q_minus_1_after=str(q_minus_1),
            )
        )

    product_pattern = (a << width) | q
    product_bits = format(product_pattern, f"0{width * 2}b")
    product = (
        product_pattern
        if product_pattern < (1 << (2 * width - 1))
        else product_pattern - (1 << (2 * width))
    )

    return SignedMultiplicationResult(
        width=width,
        multiplicand=multiplicand,
        multiplier=multiplier,
        product=product,
        product_bits=product_bits,
        steps=tuple(steps),
    )