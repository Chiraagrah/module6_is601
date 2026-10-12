# Calculator

A command-line calculator built with Python. It supports common arithmetic operations, validates numeric input, keeps a calculation history, and provides undo/redo and CSV persistence.

## Features

- Decimal-based arithmetic with configurable result precision.
- Addition, subtraction, multiplication, division, powers, roots, modulus, integer division, percentage, and absolute difference.
- Input validation with a configurable maximum absolute operand value.
- In-memory calculation history with undo, redo, clear, and configurable history size.
- CSV history load/save, with automatic saving enabled by default.
- Calculation logging and automated tests with a 100% coverage threshold.
- Decorator-based help output that dynamically lists registered operations.
- Color-coded terminal output for results, help, status messages, and errors.

## Requirements

- Python 3.10 or newer
- `pip`

## Installation

Clone the repository and change into its directory:

```bash
git clone https://github.com/Chiraagrah/module6_is601.git
cd module6_is601
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

Start the interactive calculator from the repository root:

```bash
python main.py
```

At the `calc>` prompt, enter an operation followed by two operands:

```text
calc> add 12 30
Result: 42
calc> divide 10 4
Result: 2.5
```

Operands must be valid numbers and must not exceed the configured maximum absolute value. Results are rounded to the configured precision.

### Operations

| Command | Behavior | Example |
| --- | --- | --- |
| `add` | Add the operands | `add 2 3` |
| `subtract` | Subtract the second operand from the first | `subtract 5 2` |
| `multiply` | Multiply the operands | `multiply 4 3` |
| `divide` | Divide the first operand by the second | `divide 10 2` |
| `power` | Raise the first operand to the second | `power 2 3` |
| `root` | Calculate the root of the first operand using the second as the index | `root 27 3` |
| `modulus` | Return the remainder after division | `modulus 10 3` |
| `int_divide` | Integer division | `int_divide 10 3` |
| `percent` | Calculate the first operand as a percentage of the second (`a / b * 100`) | `percent 25 200` |
| `abs_diff` | Return the absolute difference | `abs_diff 3 8` |

### Utility commands

| Command | Behavior |
| --- | --- |
| `history` | Display the current calculation history |
| `clear` | Clear the calculation history |
| `undo` | Undo the latest calculation |
| `redo` | Redo the latest undone calculation |
| `save` | Save the current history to CSV |
| `load` | Replace the current history with the saved CSV history |
| `help` | Display the available operations and commands |
| `exit` | Quit the calculator |

## Configuration

The application reads optional settings from environment variables and a `.env` file in the working directory. If a setting is not provided, its default is used.

| Variable | Default | Description |
| --- | --- | --- |
| `CALCULATOR_LOG_DIR` | `logs` | Directory for the application log |
| `CALCULATOR_LOG_FILE` | `calculator.log` | Log filename within the log directory |
| `CALCULATOR_HISTORY_DIR` | `data` | Directory for CSV calculation history |
| `CALCULATOR_HISTORY_FILE` | `history.csv` | History filename within the history directory |
| `CALCULATOR_MAX_HISTORY_SIZE` | `100` | Maximum number of calculations retained in memory |
| `CALCULATOR_AUTO_SAVE` | `true` | Automatically save history after calculations (`true` or `false`) |
| `CALCULATOR_PRECISION` | `4` | Number of decimal places used when rounding results |
| `CALCULATOR_MAX_INPUT_VALUE` | `1000000.0` | Maximum absolute value allowed for each operand |
| `CALCULATOR_DEFAULT_ENCODING` | `utf-8` | Encoding used for history CSV files |

For example, create a `.env` file to disable automatic saving and limit operands:

```dotenv
CALCULATOR_AUTO_SAVE=false
CALCULATOR_MAX_INPUT_VALUE=10000
CALCULATOR_PRECISION=2
```

Alternatively, copy the tracked safe template (`cp .env.example .env` on macOS/Linux) and edit the values you need. The local `.env` file is ignored by Git.

Relative log and history directories are created automatically in the current working directory. The default log file is `logs/calculator.log`; the default history file is `data/history.csv`.

## Tests

Run the test suite from the repository root:

```bash
python -m pytest
```

The repository's pytest configuration reports coverage for the application and requires 100% coverage. To generate an HTML coverage report:

```bash
python -m pytest --cov-report=html
```

Open `htmlcov/index.html` in a browser to view the report.

## Continuous integration

GitHub Actions runs the test suite when changes are pushed to `main` or a pull request targets `main`. The workflow installs dependencies from `requirements.txt` and runs `python -m pytest`. Pytest uses the repository's coverage configuration, so CI fails if total measured coverage falls below 100%.

## Project structure

```text
.
├── app/
│   ├── calculation.py          # Calculation records and serialization
│   ├── calculator.py           # Calculator operations, history, and persistence
│   ├── calculator_config.py    # Environment-based configuration
│   ├── calculator_memento.py   # Undo/redo state management
│   ├── calculator_repl.py      # Interactive command-line interface
│   ├── exceptions.py           # Application-specific exceptions
│   ├── history.py              # Calculation history observers
│   ├── input_validators.py     # Operand validation
│   ├── logger.py               # Logging setup
│   └── operations.py           # Arithmetic strategies and operation factory
├── tests/                      # Automated tests
├── main.py                     # Application entry point
├── pytest.ini                  # Pytest and coverage configuration
└── requirements.txt            # Python dependencies
```
