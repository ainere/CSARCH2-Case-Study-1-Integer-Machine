"""Streamlit workbench for fixed-width integer-machine demonstrations."""

from __future__ import annotations

import html
from dataclasses import asdict
from typing import Any

import streamlit as st

from integer_machine.conversion import convert_decimal
from integer_machine.division import divide_unsigned
from integer_machine.models import (
    ConversionResult,
    DivisionResult,
    RepresentationOutcome,
    SignedMultiplicationResult,
)
from integer_machine.multiplication import multiply_signed
from integer_machine.parsing import (
    InputValidationError,
    format_bits,
    format_signed_bits,
    group_bits,
    parse_decimal,
    parse_signed_operand,
    parse_unsigned_operand,
)

st.set_page_config(
    page_title="Integer Machine",
    page_icon="▦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_theme() -> None:
    """Apply the restrained computer-architecture laboratory theme."""
    st.markdown(
        """
        <style>
        :root {
          --board: #0F1E22;
          --board-raised: #14282C;
          --paper: #0F1E22;
          --ink: #EAF3DE;
          --blueprint: #EAF3DE;
          --teal: #5DCAA5;
          --teal-dim: #1D9E75;
          --amber: #EF9F27;
          --muted: #7FA69C;
          --line: #2C4A46;
          --wash: #14282C;
          --mono: "Cascadia Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace;
          --display: "Arial Narrow", "Aptos Display", "Segoe UI", sans-serif;
          --body: "Aptos", "Segoe UI", system-ui, sans-serif;
        }

        .stApp {
          background:
            linear-gradient(rgba(93, 202, 165, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(93, 202, 165, 0.05) 1px, transparent 1px),
            var(--board);
          background-size: 28px 28px, 28px 28px;
          color: var(--ink);
          font-family: var(--body);
        }

        .block-container {
          max-width: 1380px;
          padding-top: 2.2rem;
          padding-bottom: 4rem;
        }

        h1, h2, h3 {
          color: var(--blueprint) !important;
          font-family: var(--display) !important;
          letter-spacing: -0.025em !important;
        }

        h1 {
          font-size: clamp(2.35rem, 5vw, 4.5rem) !important;
          font-weight: 700 !important;
          line-height: 0.92 !important;
          margin: 0.1rem 0 0.6rem !important;
        }

        .lab-eyebrow {
          color: var(--teal);
          font-family: var(--mono);
          font-size: 0.72rem;
          font-weight: 700;
          letter-spacing: 0.16em;
          margin: 0;
          text-transform: uppercase;
        }

        .machine-rail {
          align-items: center;
          background: var(--board-raised);
          border: 1px solid var(--line);
          border-radius: 3px;
          color: var(--ink);
          display: grid;
          font-family: var(--mono);
          grid-template-columns: auto 1fr auto 1fr auto;
          margin: 1rem 0 0.7rem;
          max-width: 540px;
          padding: 0.62rem 0.8rem;
        }

        .rail-node {
          border: 1px solid var(--teal);
          border-radius: 2px;
          color: var(--ink);
          font-size: 0.76rem;
          font-weight: 700;
          min-width: 2.1rem;
          padding: 0.22rem 0.45rem;
          text-align: center;
        }

        .rail-bus {
          background: var(--amber);
          height: 2px;
        }

        .machine-rail small {
          color: var(--muted);
          font-size: 0.62rem;
          grid-column: 1 / -1;
          letter-spacing: 0.08em;
          margin-top: 0.45rem;
          text-transform: uppercase;
        }

        .workbench-intro {
          color: var(--muted);
          font-size: 0.95rem;
          line-height: 1.55;
          margin-bottom: 1.25rem;
          max-width: 72ch;
        }

        .bay-label {
          border-bottom: 1px solid var(--line);
          color: var(--muted);
          font-family: var(--mono);
          font-size: 0.69rem;
          font-weight: 700;
          letter-spacing: 0.13em;
          margin: 0.35rem 0 1rem;
          padding-bottom: 0.45rem;
          text-transform: uppercase;
        }

        .register-card {
          background: var(--board-raised);
          border: 1px solid var(--line);
          border-left: 4px solid var(--teal);
          border-radius: 0 3px 3px 0;
          margin: 0.6rem 0;
          padding: 0.8rem 0.9rem 0.75rem;
        }

        .register-card > span {
          color: var(--muted);
          display: block;
          font-family: var(--mono);
          font-size: 0.67rem;
          font-weight: 700;
          letter-spacing: 0.11em;
          text-transform: uppercase;
        }

        .register-card code {
          background: transparent;
          color: var(--blueprint);
          display: block;
          font-family: var(--mono);
          font-size: clamp(0.92rem, 1.6vw, 1.15rem);
          font-weight: 700;
          line-height: 1.65;
          overflow-wrap: anywhere;
          padding: 0.12rem 0;
          white-space: pre-wrap;
        }

        .register-card small {
          color: var(--muted);
          display: block;
          font-size: 0.75rem;
        }

        .representation-error {
          background: rgba(239, 159, 39, 0.1);
          border: 1px solid var(--amber);
          border-left: 4px solid var(--amber);
          border-radius: 0 3px 3px 0;
          color: var(--ink);
          margin: 0.6rem 0;
          padding: 0.8rem 0.9rem;
        }

        .representation-error strong {
          display: block;
          font-family: var(--mono);
          font-size: 0.7rem;
          letter-spacing: 0.08em;
          margin-bottom: 0.2rem;
          text-transform: uppercase;
        }

        div[data-testid="stMetric"] {
          background: var(--board-raised);
          border: 1px solid var(--line);
          border-radius: 3px;
          padding: 0.7rem 0.85rem;
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] *,
        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricLabel"] span,
        div[data-testid="stMetricLabel"] label {
          color: var(--muted) !important;
          font-family: var(--mono);
          letter-spacing: 0.04em;
        }

        div[data-testid="stMetricValue"] {
          color: var(--teal) !important;
        }

        div[data-testid="stDataFrame"] {
          border: 1px solid var(--line);
          border-radius: 3px;
        }

        div[data-testid="stForm"] {
          background: rgba(20, 40, 44, 0.55);
          border: 1px solid var(--line);
          border-radius: 3px;
          padding: 1rem;
        }

        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stBaseButton-secondaryFormSubmit"],
        div[data-testid="stButton"] button {
          background: var(--board-raised) !important;
          border: 1px solid var(--teal) !important;
          color: var(--ink) !important;
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        div[data-testid="stButton"] button:hover {
          background: var(--board) !important;
          border-color: var(--amber) !important;
          color: var(--amber) !important;
        }

        div[data-testid="stFormSubmitButton"] button p,
        div[data-testid="stButton"] button p {
          color: inherit !important;
        }

        /* Tab styling - increased spacing */
        div[data-baseweb="tab-list"] {
            gap: 2rem !important;
            padding: 0.5rem 0 !important;
        }

        button[data-baseweb="tab"] {
            color: #A9C4BE !important;
            font-family: var(--mono);
            font-weight: 700;
            font-size: 1.1rem !important;
            letter-spacing: 0.02em;
            padding: 0.75rem 1.5rem !important;
            border-radius: 4px !important;
            transition: all 0.2s ease !important;
        }

        button[data-baseweb="tab"]:hover {
            background: rgba(93, 202, 165, 0.1) !important;
            color: var(--teal) !important;
        }

        button[aria-selected="true"][data-baseweb="tab"] {
            color: var(--teal) !important;
            background: rgba(93, 202, 165, 0.08) !important;
            border-bottom: 3px solid var(--teal) !important;
        }

        div[data-baseweb="tab-highlight"] {
            background-color: var(--teal) !important;
            height: 3px !important;
            bottom: 0 !important;
            top: auto !important;
        }

        div[data-testid="stExpander"] details {
          background: var(--board-raised) !important;
          border: 1px solid var(--line) !important;
          border-radius: 3px;
        }

        div[data-testid="stExpander"] summary {
          color: var(--ink) !important;
        }

        div[data-testid="stExpander"] summary p,
        div[data-testid="stExpander"] summary span {
          color: var(--ink) !important;
        }

        div[data-testid="stExpander"] details:hover,
        div[data-testid="stExpander"] summary:hover {
          background: var(--board-raised) !important;
          color: var(--ink) !important;
        }

        div[data-testid="stExpander"] summary:hover p,
        div[data-testid="stExpander"] summary:hover span {
          color: var(--teal) !important;
        }

        div[data-testid="stExpander"] summary svg {
          fill: var(--ink) !important;
          color: var(--ink) !important;
        }

        /* Widget labels */
        div[data-testid="stWidgetLabel"] label,
        div[data-testid="stWidgetLabel"] p,
        div[data-testid="stWidgetLabel"] span {
          color: var(--ink) !important;
        }

        /* Metric labels */
        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricLabel"] span {
          color: var(--muted) !important;
        }

        /* Radio group */
        div[data-testid="stRadio"] label,
        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label span {
          color: var(--ink) !important;
        }

        div[data-testid="stRadio"] label:hover,
        div[data-testid="stRadio"] label:hover p,
        div[data-testid="stRadio"] label:hover span {
          color: var(--teal) !important;
        }

        /* Tooltips */
        div[data-testid="stTooltipContent"],
        div[data-baseweb="tooltip"] {
          background: var(--board-raised) !important;
          border: 1px solid var(--line) !important;
          color: var(--ink) !important;
        }

        div[data-testid="stTooltipContent"] p {
          color: var(--ink) !important;
        }

        .trace-heading {
          align-items: baseline;
          border-top: 2px solid var(--teal-dim);
          display: flex;
          gap: 1rem;
          justify-content: space-between;
          margin-top: 1.35rem;
          padding-top: 0.85rem;
        }

        .trace-heading strong {
          color: var(--ink);
          font-family: var(--display);
          font-size: 1.15rem;
        }

        .trace-heading span {
          color: var(--muted);
          font-family: var(--mono);
          font-size: 0.68rem;
          text-transform: uppercase;
        }

        @media (max-width: 720px) {
          .block-container { padding: 1.25rem 1rem 3rem; }
          .machine-rail { max-width: none; }
          .trace-heading { align-items: flex-start; flex-direction: column; gap: 0.2rem; }
          div[data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
          div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            flex: 1 1 100%;
            min-width: 100%;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_state() -> None:
    """Create operation state without overwriting results during widget reruns."""
    defaults: dict[str, Any] = {
        "conversion_result": None,
        "conversion_error": None,
        "multiplication_result": None,
        "multiplication_error": None,
        "division_result": None,
        "division_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def register_value(label: str, bits: str, caption: str = "") -> None:
    """Render a fixed-width bit value as a register card."""
    st.markdown(
        f"""
        <div class="register-card">
          <span>{html.escape(label)}</span>
          <code>{html.escape(group_bits(bits))}</code>
          <small>{html.escape(caption)}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_representation(outcome: RepresentationOutcome) -> None:
    """Render one independently evaluated conversion representation."""
    range_caption = f"Range {outcome.minimum:,} to {outcome.maximum:,}"
    if outcome.fits and outcome.bits is not None:
        register_value(outcome.label, outcome.bits, range_caption)
    else:
        st.markdown(
            f"""
            <div class="representation-error">
              <strong>{html.escape(outcome.label)}</strong>
              {html.escape(outcome.error or "This value cannot be represented.")}
              <br><small>{html.escape(range_caption)}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_trace(rows: list[dict[str, Any]], register_set: str) -> None:
    """Render every recorded trace row in a horizontally scrollable table."""
    st.markdown(
        f"""
        <div class="trace-heading">
          <strong>Register trace</strong>
          <span>{len(rows)} recorded states · {html.escape(register_set)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Scroll horizontally to inspect each register transition.")
    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
        height=min(38 * len(rows) + 44, 520),
    )


def signed_multiplication_trace(result: SignedMultiplicationResult) -> list[dict[str, Any]]:
    """Present signed multiplication steps in professor's Booth's algorithm format."""
    rows = []
    # Use format_signed_bits to handle negative multiplicands
    multiplicand_bits = format_signed_bits(result.multiplicand, result.width)
    
    for step in result.steps:
        row = {
            "Cycle": step.cycle,
            "Q₀Q₋₁": f"{step.q0}{step.q_minus_1}",
            "Action": step.action,
            "A before": step.a_before,
            "Q before": step.q_before,
            "A after op": step.a_after_operation,
            "A after shift": step.a_after,
            "Q after shift": step.q_after,
            "Q₋₁ after": step.q_minus_1_after,
            "M": multiplicand_bits,
        }
        rows.append(row)
    return rows


def division_trace(result: DivisionResult) -> list[dict[str, Any]]:
    """Present immutable division steps with the constant M register."""
    rows = []
    divisor_bits = format_bits(result.divisor, result.width)
    labels = {
        "cycle": "Cycle",
        "phase": "Phase",
        "action": "Action",
        "a_before": "A before",
        "q_before": "Q before",
        "a_after_shift": "A shifted",
        "q_after_shift": "Q shifted",
        "a_after_operation": "A after ±M",
        "q_bit": "Q₀",
        "a_after": "A",
        "q_after": "Q",
    }
    for step in result.steps:
        source = asdict(step)
        row = {label: source[field] for field, label in labels.items()}
        row["M"] = divisor_bits
        rows.append(row)
    return rows


def render_conversion() -> None:
    """Render the independent signed/unsigned conversion workbench."""
    left, right = st.columns([0.86, 1.14], gap="large")
    with left:
        st.markdown('<div class="bay-label">Input bay · fixed width</div>', unsafe_allow_html=True)
        with st.form("conversion-form"):
            value_text = st.text_input(
                "Decimal integer",
                value="42",
                key="conversion-value",
                help="A signed base-10 integer.",
            )
            width = st.number_input(
                "Data size (bits)",
                min_value=2,
                max_value=256,
                value=8,
                step=1,
                key="conversion-width",
            )
            submitted = st.form_submit_button(
                "Convert integer",
                use_container_width=True,
            )

        if submitted:
            try:
                value = parse_decimal(value_text)
                st.session_state.conversion_result = convert_decimal(value, int(width))
                st.session_state.conversion_error = None
            except InputValidationError as exc:
                st.session_state.conversion_result = None
                st.session_state.conversion_error = str(exc)

    with right:
        st.markdown('<div class="bay-label">Result bay · independent interpretations</div>', unsafe_allow_html=True)
        if st.session_state.conversion_error:
            st.error(st.session_state.conversion_error)
        result: ConversionResult | None = st.session_state.conversion_result
        if result is None and not st.session_state.conversion_error:
            st.info("Enter an integer, then convert it at the selected data size.")
        elif result is not None:
            st.metric("Input (decimal)", str(result.value))
            render_representation(result.unsigned)
            render_representation(result.signed)

    with st.expander("Guided reading · two interpretations, one bit width"):
        st.markdown(
            r"""
            1. **Set the width.** An \(n\)-bit register has exactly \(2^n\) bit patterns.
            2. **Check unsigned range.** Interpret every pattern from \(0\) through \(2^n-1\).
            3. **Check signed range independently.** Two's complement spans
               \(-2^{n-1}\) through \(2^{n-1}-1\).
            4. **Encode only when the value fits.** One interpretation may succeed while
               the other reports overflow.
            """
        )


def render_multiplication() -> None:
    """Render the signed Booth's algorithm multiplication workbench."""
    left, right = st.columns([0.86, 1.14], gap="large")
    with left:
        st.markdown('<div class="bay-label">Input bay · signed operands (Booth\'s algorithm)</div>', unsafe_allow_html=True)
        with st.form("multiplication-form"):
            base_label = st.radio(
                "Shared input format",
                ["Decimal", "Binary"],
                horizontal=True,
                key="multiplication-base",
                help="The selected format applies to both operands.",
            )
            multiplicand_text = st.text_input(
                "Multiplicand (M)",
                value="27",
                key="multiplication-multiplicand",
            )
            multiplier_text = st.text_input(
                "Multiplier (Q)",
                value="7",
                key="multiplication-multiplier",
            )
            width = st.number_input(
                "Data size (bits)",
                min_value=2,
                max_value=256,
                value=6,
                step=1,
                key="multiplication-width",
            )
            submitted = st.form_submit_button(
                "Run signed multiplier (Booth's algorithm)",
                use_container_width=True,
            )

        if submitted:
            try:
                base = "decimal" if base_label == "Decimal" else "binary"
                multiplicand = parse_signed_operand(multiplicand_text, base, int(width))
                multiplier = parse_signed_operand(multiplier_text, base, int(width))
                st.session_state.multiplication_result = multiply_signed(
                    multiplicand, multiplier, int(width)
                )
                st.session_state.multiplication_error = None
            except InputValidationError as exc:
                st.session_state.multiplication_result = None
                st.session_state.multiplication_error = str(exc)

    with right:
        st.markdown('<div class="bay-label">Result bay · A:Q product (2n bits)</div>', unsafe_allow_html=True)
        if st.session_state.multiplication_error:
            st.error(st.session_state.multiplication_error)
        result: SignedMultiplicationResult | None = st.session_state.multiplication_result
        if result is None and not st.session_state.multiplication_error:
            st.info("Run the signed multiplier to expose A, Q, Q-1, and M registers.")
        elif result is not None:
            st.metric("Product (decimal)", str(result.product))
            register_value(
                "Product (binary) · A:Q",
                result.product_bits,
                f"{result.width * 2}-bit signed product",
            )

    with st.expander("Guided reading · Booth's sequential multiplication"):
        st.markdown(
            r"""
            1. **Load registers.** Set \(A=0\), \(Q=\) multiplier, \(Q_{-1}=0\), and
               \(M=\) multiplicand.
            2. **Inspect \(Q_0Q_{-1}\).** 
               - If \(10\): \(A = A - M\)
               - If \(01\): \(A = A + M\)
               - If \(00\) or \(11\): no operation
            3. **Arithmetic shift right.** Shift the concatenated \(A,Q,Q_{-1}\) state
               right once with sign extension.
            4. **Repeat once per data bit.** After \(n\) cycles, concatenated \(A:Q\)
               is the \(2n\)-bit signed product.
            """
        )

    if result is not None:
        try:
            render_trace(signed_multiplication_trace(result), "A · Q · Q₋₁ · M")
        except ValueError as e:
            st.error(f"Error displaying trace: {e}")
            st.write("Product result:", result.product)
            st.write("Product binary:", result.product_bits)


def render_division() -> None:
    """Render the unsigned non-restoring division workbench."""
    left, right = st.columns([0.86, 1.14], gap="large")
    with left:
        st.markdown('<div class="bay-label">Input bay · unsigned operands</div>', unsafe_allow_html=True)
        with st.form("division-form"):
            base_label = st.radio(
                "Shared input format",
                ["Decimal", "Binary"],
                horizontal=True,
                key="division-base",
                help="The selected format applies to both operands.",
            )
            dividend_text = st.text_input(
                "Dividend (Q)",
                value="13",
                key="division-dividend",
            )
            divisor_text = st.text_input(
                "Divisor (M)",
                value="3",
                key="division-divisor",
            )
            width = st.number_input(
                "Data size (bits)",
                min_value=2,
                max_value=256,
                value=8,
                step=1,
                key="division-width",
            )
            submitted = st.form_submit_button(
                "Run unsigned divider",
                use_container_width=True,
            )

        if submitted:
            try:
                base = "decimal" if base_label == "Decimal" else "binary"
                dividend = parse_unsigned_operand(dividend_text, base, int(width))
                divisor = parse_unsigned_operand(divisor_text, base, int(width))
                st.session_state.division_result = divide_unsigned(
                    dividend, divisor, int(width)
                )
                st.session_state.division_error = None
            except InputValidationError as exc:
                st.session_state.division_result = None
                st.session_state.division_error = str(exc)

    with right:
        st.markdown('<div class="bay-label">Result bay · quotient and remainder</div>', unsafe_allow_html=True)
        if st.session_state.division_error:
            st.error(st.session_state.division_error)
        result: DivisionResult | None = st.session_state.division_result
        if result is None and not st.session_state.division_error:
            st.info("Run the unsigned divider to expose the A, Q, and M registers.")
        elif result is not None:
            quotient_column, remainder_column = st.columns(2)
            quotient_column.metric("Quotient (decimal)", str(result.quotient))
            remainder_column.metric("Remainder (decimal)", str(result.remainder))
            register_value("Quotient (binary) · Q", result.quotient_bits)
            register_value("Remainder (binary) · A", result.remainder_bits)

    with st.expander("Guided reading · non-restoring division"):
        st.markdown(
            r"""
            1. **Load registers.** Set signed \(A=0\), \(Q=\) dividend, and \(M=\) divisor.
            2. **Shift \(A,Q\) left.** Use the previous sign of \(A\) to choose the operation:
               subtract \(M\) after a nonnegative \(A\), or add \(M\) after a negative \(A\).
            3. **Write the quotient bit.** Set \(Q_0=1\) when the new \(A\) is nonnegative;
               otherwise write 0.
            4. **Restore once if needed.** After \(n\) cycles, add \(M\) to a negative
               final \(A\). Then \(Q\) is the quotient and \(A\) is the remainder.
            """
        )

    if result is not None:
        render_trace(division_trace(result), "A · Q · M")


inject_theme()
initialize_state()

st.markdown('<p class="lab-eyebrow">Machine 1 · register-state workbench</p>', unsafe_allow_html=True)
st.title("Integer Machine")
st.markdown(
    """
    <div class="machine-rail" aria-label="A Q Q-1 register bus">
      <span class="rail-node">A</span><span class="rail-bus"></span>
      <span class="rail-node">Q</span><span class="rail-bus"></span>
      <span class="rail-node">Q₋₁</span>
      <small>accumulator · multiplier/quotient · extra bit for Booth's algorithm</small>
    </div>
    <p class="workbench-intro">
      Convert fixed-width integers, then inspect signed multiplication (Booth's algorithm)
      and unsigned division (non-restoring) one register transition at a time.
      The interface is limited to 2–256 bits; the Python teaching core remains arbitrary precision.
    </p>
    """,
    unsafe_allow_html=True,
)

conversion_tab, multiplication_tab, division_tab = st.tabs(
    ["Conversion", "Multiplication", "Division"]
)
with conversion_tab:
    render_conversion()
with multiplication_tab:
    render_multiplication()
with division_tab:
    render_division()