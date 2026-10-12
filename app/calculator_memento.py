# app/calculator_memento.py
from typing import List
from app.calculation import Calculation

class CalculatorMemento:
    """Stores a snapshot of the calculation history."""
    
    def __init__(self, history: List[Calculation]):
        # Store a copy of the history list to preserve state immutability
        self._history = list(history)
        
    @property
    def history(self) -> List[Calculation]:
        return list(self._history)


class HistoryCaretaker:
    """Manages undo and redo states using the Memento pattern."""
    
    def __init__(self):
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []
        
    def save_state(self, history: List[Calculation]):
        """Saves the current state onto the undo stack and clears the redo stack."""
        self._undo_stack.append(CalculatorMemento(history))
        self._redo_stack.clear()
        
    def undo(self, current_history: List[Calculation]) -> List[Calculation]:
        """Pops the last state from undo stack, pushes current to redo, and returns previous history."""
        if not self._undo_stack:
            return None
        
        # Save current state to redo stack before restoring
        self._redo_stack.append(CalculatorMemento(current_history))
        memento = self._undo_stack.pop()
        return memento.history
        
    def redo(self, current_history: List[Calculation]) -> List[Calculation]:
        """Pops the last state from redo stack, pushes current to undo, and returns restored history."""
        if not self._redo_stack:
            return None
            
        # Save current state to undo stack before restoring
        self._undo_stack.append(CalculatorMemento(current_history))
        memento = self._redo_stack.pop()
        return memento.history
        
    def clear(self):
        """Clears both undo and redo stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()