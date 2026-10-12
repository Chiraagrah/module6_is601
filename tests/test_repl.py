# tests/test_repl.py
import pytest
from unittest.mock import patch
from app.calculator_repl import CalculatorREPL

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

@patch('builtins.input', side_effect=[
    'undo', 'redo', 'add 1 2', 'divide 1 0', 'subtract 1 2', 'exit'
])
@patch('builtins.print')
def test_repl_success_and_error_handling(mock_print, mock_input):
    from decimal import Decimal
    from unittest.mock import patch
    from app.exceptions import OperationError

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

    printed = [call.args[0] for call in mock_print.call_args_list]
    assert 'Successfully undone last calculation.' in printed
    assert 'Successfully redone calculation.' in printed
    assert 'Result: 3' in printed
    assert 'Error: expected calculator error' in printed
    assert 'Unexpected error: unexpected failure' in printed

def test_repl_module_entry_point():
    from pathlib import Path
    from runpy import run_path

    module_path = Path(__file__).parents[1] / 'app' / 'calculator_repl.py'
    with patch('builtins.input', side_effect=['exit']), patch('builtins.print'):
        run_path(str(module_path), run_name='__main__')