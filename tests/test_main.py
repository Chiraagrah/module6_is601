from unittest.mock import patch
from pathlib import Path
from runpy import run_path

import main


@patch("main.CalculatorREPL")
def test_main_runs_calculator_repl(mock_repl):
    main.main()

    mock_repl.assert_called_once_with()
    mock_repl.return_value.run.assert_called_once_with()


@patch("app.calculator_repl.CalculatorREPL")
def test_main_script_entry_point(mock_repl):
    run_path(str(Path(main.__file__)), run_name="__main__")

    mock_repl.assert_called_once_with()
    mock_repl.return_value.run.assert_called_once_with()
