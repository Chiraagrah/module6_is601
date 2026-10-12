# tests/test_repl.py
import pytest
import re
from unittest.mock import patch
from colorama import Fore
from app.calculator_repl import CalculatorREPL
from app.operations import Addition, OperationFactory

@patch('builtins.input', side_effect=['add 2 3', 'history', 'clear', 'undo', 'redo', 'help', 'exit'])
@patch('builtins.print')
def test_repl_commands(mock_print, mock_input):
    repl = CalculatorREPL()
    repl.run()
    # Verifies REPL runs successfully through the command sequence and exits cleanly
    assert mock_input.call_count == 7

@patch('builtins.input', side_effect=['unknown_command', 'add 2', 'exit'])
@patch('builtins.print')
def test_repl_edge_cases(mock_print, mock_input):
    repl = CalculatorREPL()
    repl.run()
    assert mock_input.call_count == 3

@patch('builtins.input', side_effect=['undo', 'redo', 'exit'])
@patch('builtins.print')
def test_repl_undo_redo_empty(mock_print, mock_input):
    from app.calculator_repl import CalculatorREPL
    repl = CalculatorREPL()
    repl.run()

def test_help_decorator_includes_registered_operations(monkeypatch, capsys):
    monkeypatch.setitem(OperationFactory._operations, "test_operation", Addition)
    repl = CalculatorREPL()

    repl.print_help()

    output = capsys.readouterr().out
    assert "test_operation" in output
    assert "history" in output

@patch('builtins.input', side_effect=[
    'undo', 'redo', 'add 1 2', 'divide 1 0', 'subtract 1 2', 'exit'
])
@patch('builtins.print')
def test_repl_success_and_error_handling(mock_print, mock_input, caplog):
    from decimal import Decimal
    from unittest.mock import patch
    from app.exceptions import OperationError
    import logging

    caplog.set_level(logging.WARNING, logger="CalculatorLogger")
    repl = CalculatorREPL()
    repl.calculator.config.auto_save = False
    repl.calculator.perform_operation('add', '2', '3')

    with patch.object(
        repl.calculator,
        'perform_operation',
        side_effect=[
            Decimal('3'),
            OperationError('expected calculator error'),
            RuntimeError('unexpected failure'),
        ],
    ):
        repl.run()

    raw_printed = [call.args[0] for call in mock_print.call_args_list]
    printed = [re.sub(r"\x1b\[[0-9;]*m", "", text) for text in raw_printed]
    assert any(Fore.GREEN in text for text in raw_printed)
    assert any(Fore.RED in text for text in raw_printed)
    assert 'Successfully undone last calculation.' in printed
    assert 'Successfully redone calculation.' in printed
    assert 'Result: 3' in printed
    assert 'Error: expected calculator error' in printed
    assert 'Unexpected error: unexpected failure' in printed
    assert any(
        record.levelname == "WARNING"
        and "Calculator command failed" in record.message
        for record in caplog.records
    )
    assert any(
        record.levelname == "ERROR"
        and "Unexpected calculator error" in record.message
        for record in caplog.records
    )

def test_repl_module_entry_point():
    from pathlib import Path
    from runpy import run_path

    module_path = Path(__file__).parents[1] / 'app' / 'calculator_repl.py'
    with patch('builtins.input', side_effect=['exit']), patch('builtins.print'):
        run_path(str(module_path), run_name='__main__')