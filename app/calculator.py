# app/calculator.py
from typing import List, Optional
from decimal import Decimal
import pandas as pd

from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.operations import OperationFactory
from app.calculator_memento import HistoryCaretaker
from app.history import HistoryObserver, LoggingObserver, AutoSaveObserver
from app.exceptions import OperationError, ValidationError, CalculatorError
from app.input_validators import InputValidator

class Calculator:
    """Core Calculator class integrating Factory, Strategy, Observer, and Memento patterns."""
    
    def __init__(self, config: Optional[CalculatorConfig] = None):
        self.config = config or CalculatorConfig()
        self.history: List[Calculation] = []
        self._observers: List[HistoryObserver] = []
        self.caretaker = HistoryCaretaker()
        
        # Register default observers based on configuration
        self.register_observer(LoggingObserver(self.config))
        if self.config.auto_save:
            self.register_observer(AutoSaveObserver(self.config))
            
    def register_observer(self, observer: HistoryObserver):
        """Registers a new history observer."""
        if observer not in self._observers:
            self._observers.append(observer)
            
    def unregister_observer(self, observer: HistoryObserver):
        """Unregisters an existing history observer."""
        if observer in self._observers:
            self._observers.remove(observer)
            
    def notify_observers(self, calculation: Calculation):
        """Notifies all registered observers about a new calculation."""
        for observer in self._observers:
            observer.update(calculation, self.history)
            
    def perform_operation(self, operation_name: str, a_val, b_val) -> Decimal:
        """Validates inputs, executes operation, updates history, and notifies observers."""
        # Validate inputs against configuration limits
        a = InputValidator.validate_number(a_val, self.config.max_input_value)
        b = InputValidator.validate_number(b_val, self.config.max_input_value)
        
        # Create operation using Factory Pattern
        operation = OperationFactory.create_operation(operation_name)
        
        # Save state to caretaker before modifying history (Memento pattern)
        self.caretaker.save_state(self.history)
        
        # Execute calculation
        result_val = operation.execute(a, b)
        
        # Round result based on configuration precision
        result = round(result_val, self.config.precision)
        
        # Create calculation record
        calculation = Calculation(operation_name.lower(), a, b, result)
        
        # Add to history
        self.history.append(calculation)
        
        # Enforce max history size limit
        if len(self.history) > self.config.max_history_size:
            self.history.pop(0)
            
        # Notify observers (logging, auto-save)
        self.notify_observers(calculation)
        
        return result
        
    def undo(self) -> bool:
        """Undoes the last calculation."""
        restored = self.caretaker.undo(self.history)
        if restored is not None:
            self.history = restored
            return True
        return False
        
    def redo(self) -> bool:
        """Redoes the last undone calculation."""
        restored = self.caretaker.redo(self.history)
        if restored is not None:
            self.history = restored
            return True
        return False
        
    def clear_history(self):
        """Clears calculation history and reset caretaker stacks."""
        self.caretaker.save_state(self.history)
        self.history.clear()
        self.caretaker.clear()
        
    def save_history(self):
        """Manually saves calculation history to CSV using pandas."""
        try:
            self.config.history_dir.mkdir(parents=True, exist_ok=True)
            if not self.history:
                # Save empty DataFrame with headers if history is empty
                df = pd.DataFrame(columns=["operation", "operand_a", "operand_b", "result", "timestamp"])
            else:
                df = pd.DataFrame([calc.to_dict() for calc in self.history])
            df.to_csv(self.config.history_file, index=False, encoding=self.config.default_encoding)
        except Exception as e:
            raise CalculatorError(f"Failed to save history to file: {e}") from e
            
    def load_history(self):
        """Loads calculation history from CSV using pandas."""
        if not self.config.history_file.exists():
            raise CalculatorError(f"History file not found at '{self.config.history_file}'")
            
        try:
            df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)
            self.caretaker.save_state(self.history)
            self.history.clear()
            
            for _, row in df.iterrows():
                calc = Calculation.from_dict(row.to_dict())
                self.history.append(calc)
        except Exception as e:
            raise CalculatorError(f"Failed to load history from file: {e}") from e