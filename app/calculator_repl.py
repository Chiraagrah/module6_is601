# app/calculator_repl.py
import sys
from app.calculator import Calculator
from app.operations import OperationFactory
from app.exceptions import CalculatorError

class CalculatorREPL:
    """Command-line interface implementing the REPL pattern for the calculator."""
    
    def __init__(self):
        self.calculator = Calculator()
        
    def print_help(self):
        """Displays available commands and operations."""
        print("\n=== Calculator REPL ===")
        print("Supported Operations:")
        ops = OperationFactory.get_supported_operations()
        print(f"  {', '.join(ops)}")
        print("\nUtility Commands:")
        print("  history       - Display calculation history")
        print("  clear         - Clear calculation history")
        print("  undo          - Undo the last calculation")
        print("  redo          - Redo the last undone calculation")
        print("  save          - Manually save history to file")
        print("  load          - Load history from file")
        print("  help          - Display this help message")
        print("  exit          - Exit the application")
        print("---------------------------------\n")

    def run(self):
        """Starts the REPL loop."""
        print("Welcome to the Calculator! Type 'help' for available commands.")
        
        while True:
            try:
                user_input = input("calc> ").strip()
                if not user_input:
                    continue
                    
                tokens = user_input.split()
                command = tokens[0].lower()
                
                if command == "exit":
                    print("Goodbye!")
                    break
                    
                elif command == "help":
                    self.print_help()
                    
                elif command == "history":
                    if not self.calculator.history:
                        print("History is empty.")
                    else:
                        print("\n--- Calculation History ---")
                        for idx, calc in enumerate(self.calculator.history, 1):
                            print(f"{idx}. {calc}")
                        print("---------------------------\n")
                        
                elif command == "clear":
                    self.calculator.clear_history()
                    print("History cleared.")
                    
                elif command == "undo":
                    if self.calculator.undo():
                        print("Successfully undone last calculation.")
                    else:
                        print("Nothing to undo.")
                        
                elif command == "redo":
                    if self.calculator.redo():
                        print("Successfully redone calculation.")
                    else:
                        print("Nothing to redo.")
                        
                elif command == "save":
                    self.calculator.save_history()
                    print(f"History successfully saved to {self.calculator.config.history_file}")
                    
                elif command == "load":
                    self.calculator.load_history()
                    print(f"History successfully loaded from {self.calculator.config.history_file}")
                    
                elif command in OperationFactory.get_supported_operations():
                    if len(tokens) != 3:
                        print(f"Error: Operation '{command}' requires exactly 2 operands. Usage: <operation> <a> <b>")
                        continue
                        
                    _, a_str, b_str = tokens
                    result = self.calculator.perform_operation(command, a_str, b_str)
                    print(f"Result: {result}")
                    
                else:
                    print(f"Unknown command or operation: '{command}'. Type 'help' for options.")
                    
            except CalculatorError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    repl = CalculatorREPL()
    repl.run()