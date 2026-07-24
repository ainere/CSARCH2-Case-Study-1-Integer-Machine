# CSARCH2 Case Study 1

**Machine:** _Machine 1 - Integer Machine_ <br>
**Subject:** _CSARCH2_ <br>
**Section:** _S03_ <br>
**Group:** _Group 7_ <br>
**GitHub Link:** https://github.com/ainere/CSARCH2-Case-Study-1-Integer-Machine <br>
**Website Link:** _Pending deployment_

## Group Members

- Alain Zuriel Marcos
- Elkan La Madrid
- Jenrick Lim
- Kent Lopez

---

## Project Overview

The **Machine 1 Integer Machine** is a functional Streamlit web application
that demonstrates fixed-width integer representation and register-level
arithmetic. It is intended to make each algorithm easier to follow by showing
both the final answer and the intermediate register states used to reach it.

The website currently includes three working tools:

1. decimal-to-binary integer conversion;
2. unsigned sequential add-and-shift multiplication; and
3. unsigned non-restoring division.

Each tool accepts user input, validates it against the selected data size, and
displays an explanation of the result. Multiplication and division also include
complete cycle-by-cycle trace tables.

---

## Tech Stack

| Technology | Role |
| --- | --- |
| Python 3.12+ | Implements the integer algorithms, validation, and application logic |
| Streamlit | Provides the interactive web interface and technical-lab layout |
| CSS | Adds the custom colors, cards, tables, typography, and responsive styling |

### 1. Python

Python provides the calculation layer for the machine. The arithmetic modules
are separate from the interface, allowing the algorithms to be tested without
running Streamlit.

**Used for:**

- fixed-width signed and unsigned conversion;
- input parsing and range validation;
- sequential multiplication using `C`, `A`, `Q`, and `M`;
- non-restoring division using `A`, `Q`, and `M`; and
- immutable result and trace records.

### 2. Streamlit

Streamlit provides the website interface. It allows the group to build a
working Python-based web application without maintaining a separate frontend
and backend.

**Used for:**

- data-size and number-format controls;
- separate Conversion, Multiplication, and Division tabs;
- inline validation messages that preserve the user's input;
- result cards and guided explanations; and
- responsive register trace tables.

---

## I. Machine Features

### 1. Decimal Integer Conversion

**Concept:** Converts one decimal integer into fixed-width binary while
evaluating its unsigned and signed two's-complement interpretations
independently.

**Inputs:**

- a decimal integer; and
- a data size from 2 to 256 bits.

**Outputs:**

- unsigned decimal and fixed-width binary, when the value fits;
- signed decimal and fixed-width two's-complement binary, when the value fits;
- minimum and maximum values for both interpretations; and
- a separate overflow message for any interpretation that cannot represent the
  input.

This separation is important because a value may fit one interpretation but
not the other. For example, `255` fits unsigned 8-bit representation but does
not fit signed 8-bit two's complement.

### 2. Sequential Multiplication

**Concept:** Demonstrates unsigned add-and-shift multiplication using the
`C`, `A`, `Q`, and `M` registers.

**How it works:**

- `M` stores the multiplicand.
- `Q` stores the multiplier.
- `A` stores the partial product.
- `C` stores the carry bit.
- If the current least-significant multiplier bit `Q0` is `1`, the machine
  adds `M` to `A`.
- The combined `C,A,Q` registers are shifted right after every cycle.
- The final product is the concatenated `A:Q` value.

The website shows the initial register state, every add/no-add decision, the
registers before and after each shift, and the final product in decimal and
binary.

### 3. Non-Restoring Division

**Concept:** Demonstrates unsigned non-restoring division using the `A`, `Q`,
and `M` registers.

**How it works:**

- `Q` begins with the dividend.
- `M` stores the divisor.
- `A` stores the signed partial remainder.
- The combined `A,Q` registers are shifted left during each cycle.
- The machine subtracts `M` when the previous `A` is non-negative and adds `M`
  when it is negative.
- A quotient bit is assigned after each arithmetic operation.
- If the final partial remainder is negative, the machine restores it by
  adding `M`.

The website displays the quotient, remainder, final registers, optional
restoration step, and a complete cycle trace.

---

## II. Input Rules

The interface uses one shared data-size control and supports two operand
formats for multiplication and division.

| Input | Accepted values |
| --- | --- |
| Data size | Whole numbers from 2 to 256 bits; 8 bits by default |
| Conversion value | Signed base-10 integer |
| Decimal arithmetic operand | Non-negative base-10 integer |
| Binary arithmetic operand | `0` and `1`, with optional `0b` prefix, spaces, or underscores |
| Divisor | Any supported positive value; zero is rejected |

Arithmetic operands must fit the selected unsigned width. Invalid values are
reported beside the form without clearing the user's entries.

The 256-bit maximum is an interface guardrail that prevents accidentally
generating an impractically large trace table. The pure Python calculation
modules use arbitrary-precision integers and are not internally limited to 256
bits.

---

## III. Running the Website Locally

### 1. Requirements

- Python 3.12 or newer
- `pip`

### 2. Installation

Clone the repository and enter its folder:

```powershell
git clone https://github.com/ainere/CSARCH2-Case-Study-1-Integer-Machine.git
cd CSARCH2-Case-Study-1-Integer-Machine
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

### 3. Start the Application

```powershell
python -m streamlit run app.py
```

Streamlit will print a local address, normally
`http://localhost:8501`. Open that address in a browser and stop the server
with `Ctrl+C` when finished.

---

## IV. Project Structure

```text
app.py                     Streamlit forms, tabs, and result presentation
integer_machine/
  conversion.py            Fixed-width signed and unsigned conversion
  multiplication.py        Unsigned sequential add-and-shift multiplier
  division.py              Unsigned non-restoring divider
  models.py                Immutable result and trace records
  parsing.py               Input validation and binary formatting
.streamlit/config.toml     Streamlit theme and server defaults
requirements.txt           Runtime dependency
```

The `integer_machine/` package is the independent teaching core. It has no
Streamlit dependency. The `app.py` file acts as the presentation layer: it
collects inputs, calls the appropriate algorithm, and renders the results.

---

# Development Documentation

## All Technical and Creative Accomplishments

- Created a working Streamlit website with a responsive technical-laboratory
  visual style.
- Implemented independent unsigned and signed fixed-width conversion results.
- Implemented unsigned sequential multiplication with complete `C,A,Q,M`
  register traces.
- Implemented unsigned non-restoring division with complete `A,Q,M` traces and
  final remainder restoration.
- Added decimal and binary operand formats with readable grouped binary output.
- Added inline validation while retaining the user's entered values.
- Separated the arithmetic core from the Streamlit presentation layer.
- Documented local installation, execution, input rules, limitations, and
  project structure.

## Current Limitations and Pending Work

- Multiplication and division currently support **unsigned operands only**.
- Signed multiplication and signed division are not implemented.
- Calculations are not saved after the application session ends.
- Per-cycle animation is not included; the complete states are presented in
  tables instead.
- Representative screenshots still need to be added.
- Repository visibility should be confirmed before final submission.
- A public 5-8 minute YouTube walkthrough still needs to be recorded and linked.
- Live website deployment is still pending.

## Completed Checking

- All 48 local development tests passed before preparing the clean repository.
- Python compilation checks passed for the application and calculation package.
- A separate 65-bit multiplication and division smoke check matched Python's
  arithmetic results.
- Desktop and mobile-width browser layouts were reviewed.
- The complete branch received a final review with no critical or important
  findings.

---

## Disclosure on the Use of AI / LLM Tools

The group used **OpenAI Codex** to support the initial implementation,
interface prototyping, local verification, and documentation of this working
draft.
The generated work must still be reviewed, understood, and verified by the
group before final submission and presentation.

| Tool | Purpose |
| --- | --- |
| OpenAI Codex | Streamlit prototyping, Python implementation support, local verification, and README organization |
