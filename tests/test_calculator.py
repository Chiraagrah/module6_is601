# tests/test_calculator.py
import pytest
from decimal import Decimal
from pathlib import Path
import pandas as pd

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError, OperationError, CalculatorError
from app.calculation import Calculation
from app.operations import OperationFactory

@pytest.mark.parametrize(
    ("operation", "operand_a", "operand_b", "expected"),
    [
        ("add", "5", "3", "8"),
        ("subtract", "10", "4", "6"),
        ("multiply", "3", "4", "12"),
        ("divide", "10", "2", "5"),
        ("power", "2", "3", "8"),
        ("power", "2", "-3", "0.125"),
        ("root", "9", "2", "3"),
        ("root", "-8", "3", "-2"),
        ("modulus", "10", "3", "1"),
        ("int_divide", "10", "3", "3"),
        ("percent", "50", "200", "25"),
        ("abs_diff", "5", "12", "7"),
    ],
)
def test_calculator_operations(operation, operand_a, operand_b, expected):
    calc = Calculator()

    assert calc.perform_operation(operation, operand_a, operand_b) == Decimal(expected)

@pytest.mark.parametrize(
    ("operation", "operand_a", "operand_b", "message"),
    [
        ("divide", "5", "0", "Division by zero"),
        ("modulus", "5", "0", "Modulus by zero"),
        ("int_divide", "5", "0", "Integer division by zero"),
        ("percent", "5", "0", "Percentage base cannot be zero"),
        ("root", "-4", "2", "odd integer index"),
        ("root", "8", "0", "Root index cannot be zero"),
        ("unknown_op", "1", "1", "Unknown operation"),
    ],
)
def test_operation_errors(operation, operand_a, operand_b, message):
    calc = Calculator()

    with pytest.raises(OperationError, match=message):
        calc.perform_operation(operation, operand_a, operand_b)

@pytest.mark.parametrize(
    ("operand_a", "operand_b"),
    [
        ("-8", "2"),
        ("-8", "3.5"),
    ],
)
def test_negative_root_rejects_non_odd_integer_indices(operand_a, operand_b):
    calc = Calculator()

    with pytest.raises(OperationError, match="odd integer index"):
        calc.perform_operation("root", operand_a, operand_b)

def test_root_of_negative_number_with_odd_index():
    from unittest.mock import patch
    from app.operations import Root

    calc = Calculator()

    assert calc.perform_operation("root", "-8", "3") == Decimal("-2")

    with patch("builtins.float", side_effect=OverflowError("float conversion failed")):
        with pytest.raises(OperationError, match="Root operation failed"):
            Root().execute(Decimal("-8"), Decimal("3"))

@pytest.mark.parametrize(
    ("operand_a", "operand_b"),
    [
        ("abc", "3"),
        ("2000000", "3"),
    ],
)
def test_input_validation(operand_a, operand_b):
    calc = Calculator()

    with pytest.raises(ValidationError):
        calc.perform_operation("add", operand_a, operand_b)

def test_undo_redo_history():
    calc = Calculator()
    calc.perform_operation("add", "1", "1")
    calc.perform_operation("add", "2", "2")
    
    assert len(calc.history) == 2
    
    # Undo last
    assert calc.undo() is True
    assert len(calc.history) == 1
    assert calc.history[0].result == Decimal("2")
    
    # Redo last
    assert calc.redo() is True
    assert len(calc.history) == 2
    assert calc.history[1].result == Decimal("4")
    
    # Nothing to undo/redo checks
    calc_empty = Calculator()
    assert calc_empty.undo() is False
    assert calc_empty.redo() is False

def test_clear_and_history_limit():
    config = CalculatorConfig()
    config.max_history_size = 2
    calc = Calculator(config)
    
    calc.perform_operation("add", "1", "1")
    calc.perform_operation("add", "2", "2")
    calc.perform_operation("add", "3", "3") # Should pop the first one
    
    assert len(calc.history) == 2
    assert calc.history[0].result == Decimal("4") # 2+2
    
    calc.clear_history()
    assert len(calc.history) == 0

def test_save_and_load_history(tmp_path):
    config = CalculatorConfig()
    config.history_file = tmp_path / "test_history.csv"
    config.history_dir = tmp_path
    
    calc = Calculator(config)
    calc.perform_operation("add", "5", "5")
    calc.save_history()
    
    assert config.history_file.exists()
    
    calc2 = Calculator(config)
    assert len(calc2.history) == 0
    calc2.load_history()
    assert len(calc2.history) == 1
    assert calc2.history[0].result == Decimal("10")

def test_load_nonexistent_history(tmp_path):
    config = CalculatorConfig()
    config.history_file = tmp_path / "nonexistent.csv"
    calc = Calculator(config)
    
    with pytest.raises(CalculatorError):
        calc.load_history()

def test_calculation_serialization():
    calc = Calculation("add", Decimal("2"), Decimal("3"), Decimal("5"))
    d = calc.to_dict()
    calc_reconstructed = Calculation.from_dict(d)
    
    assert calc_reconstructed.operation_name == "add"
    assert calc_reconstructed.a == Decimal("2")
    assert calc_reconstructed.result == Decimal("5")
    assert repr(calc) is not None

@pytest.mark.parametrize(
    ("setting", "value", "message"),
    [
        ("CALCULATOR_PRECISION", "not_an_int", "CALCULATOR_PRECISION"),
        ("CALCULATOR_MAX_HISTORY_SIZE", "not_an_int", "CALCULATOR_MAX_HISTORY_SIZE"),
        ("CALCULATOR_MAX_HISTORY_SIZE", "0", "CALCULATOR_MAX_HISTORY_SIZE"),
        ("CALCULATOR_PRECISION", "-1", "CALCULATOR_PRECISION"),
        ("CALCULATOR_MAX_INPUT_VALUE", "not_a_number", "CALCULATOR_MAX_INPUT_VALUE"),
        ("CALCULATOR_MAX_INPUT_VALUE", "nan", "CALCULATOR_MAX_INPUT_VALUE"),
        ("CALCULATOR_MAX_INPUT_VALUE", "0", "CALCULATOR_MAX_INPUT_VALUE"),
        ("CALCULATOR_AUTO_SAVE", "sometimes", "CALCULATOR_AUTO_SAVE"),
    ],
)
def test_invalid_configuration_is_rejected(monkeypatch, tmp_path, setting, value, message):
    from app.calculator_config import CalculatorConfig
    from app.exceptions import ConfigurationError

    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv(setting, value)
    with pytest.raises(ConfigurationError, match=message):
        CalculatorConfig()

def test_auto_save_disabled_and_empty_history():
    config = CalculatorConfig()
    config.auto_save = False
    calc = Calculator(config)
    # Should skip auto-save safely
    calc.perform_operation("add", "2", "2")
    
    # Test saving empty history explicitly
    calc.history.clear()
    calc.save_history()
    assert config.history_file.exists()

def test_repl_additional_branches():
    from unittest.mock import patch
    from app.calculator_repl import CalculatorREPL
    
    # Cover history empty message, invalid token counts, save/load via REPL
    inputs = [
        "history", 
        "save", 
        "load", 
        "add 5",  # incorrect operand count
        "unknowncmd 1 2", # unknown command
        "  ", # blank input
        "exit"
    ]
    with patch('builtins.input', side_effect=inputs), patch('builtins.print'):
        repl = CalculatorREPL()
        repl.run()

def test_remaining_coverage_branches():
    from app.calculator import Calculator
    from app.history import LoggingObserver
    from app.operations import Power, Root
    from decimal import Decimal
    
    calc = Calculator()
    obs = LoggingObserver(calc.config)
    
    # Cover unregistering non-existent observer and existing observer
    calc.register_observer(obs)
    calc.unregister_observer(obs)
    calc.unregister_observer(obs)
    
    # Cover undo/redo when empty via REPL branches or direct calls
    assert calc.undo() is False
    assert calc.redo() is False

def test_history_observer_empty_and_failed_autosave(tmp_path, caplog):
    from unittest.mock import patch
    from app.calculation import Calculation
    from app.history import AutoSaveObserver, HistoryObserver
    from app.operations import Operation

    class ConcreteObserver(HistoryObserver):
        def update(self, calculation, history):
            return super().update(calculation, history)

    class ConcreteOperation(Operation):
        def execute(self, a, b):
            return super().execute(a, b)

    # Exercise the abstract base implementations as well as observer early returns.
    ConcreteObserver().update(None, [])
    assert ConcreteOperation().execute(Decimal("1"), Decimal("2")) is None

    config = CalculatorConfig()
    config.history_dir = tmp_path
    config.history_file = tmp_path / "history.csv"
    observer = AutoSaveObserver(config)
    calculation = Calculation("add", Decimal("1"), Decimal("2"), Decimal("3"))

    config.auto_save = False
    observer.update(calculation, [calculation])
    config.auto_save = True
    observer.update(calculation, [])

    with patch.object(pd.DataFrame, "to_csv", side_effect=OSError("disk unavailable")):
        observer.update(calculation, [calculation])

    assert any(
        record.levelname == "WARNING"
        and "Auto-save failed: disk unavailable" in record.message
        for record in caplog.records
    )

def test_manual_history_persistence_errors_are_wrapped(tmp_path):
    from unittest.mock import patch

    config = CalculatorConfig()
    config.history_dir = tmp_path
    config.history_file = tmp_path / "history.csv"
    calc = Calculator(config)

    with patch.object(pd.DataFrame, "to_csv", side_effect=OSError("disk unavailable")):
        with pytest.raises(CalculatorError, match="Failed to save history"):
            calc.save_history()

    config.history_file.touch()
    with patch.object(pd, "read_csv", side_effect=OSError("file unreadable")):
        with pytest.raises(CalculatorError, match="Failed to load history"):
            calc.load_history()

def test_power_fractional_and_operation_failure_wrappers():
    calc = Calculator()

    assert calc.perform_operation("power", "2", "0.5") == Decimal("1.4142")

    with pytest.raises(OperationError, match="Power operation failed"):
        calc.perform_operation("power", "10", "1000000")

    with pytest.raises(OperationError, match="Root operation failed"):
        calc.perform_operation("root", "1", "1e-10000")