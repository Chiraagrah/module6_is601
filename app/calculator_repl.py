# app/calculator_repl.py
from functools import wraps
from colorama import Fore, Style, init
from app.calculator import Calculator
from app.operations import OperationFactory
from app.exceptions import CalculatorError
from app.logger import setup_logger

init(autoreset=True)


def include_supported_operations(help_renderer):
    """Decorate the utility help renderer with the current operation list."""
    @wraps(help_renderer)
    def wrapper(self):
        print(f"\n{Style.BRIGHT}{Fore.CYAN}=== Calculator REPL ===")
        print(f"{Style.BRIGHT}Supported Operations:")
        print(f"  {Fore.CYAN}{', '.join(OperationFactory.get_supported_operations())}")
        help_renderer(self)

    return wrapper


class CalculatorREPL:
    """Command-line interface implementing the REPL pattern for the calculator."""
    
    def __init__(self):
        self.calculator = Calculator()
        self.logger = setup_logger(self.calculator.config.log_file)
        
    @include_supported_operations
    def print_help(self):
        """Displays available commands and operations."""
        print(f"\n{Style.BRIGHT}Utility Commands:")
        print(f"  {Fore.CYAN}history       - Display calculation history")
        print(f"  {Fore.CYAN}clear         - Clear calculation history")
        print(f"  {Fore.CYAN}undo          - Undo the last calculation")
        print(f"  {Fore.CYAN}redo          - Redo the last undone calculation")
        print(f"  {Fore.CYAN}save          - Manually save history to file")
        print(f"  {Fore.CYAN}load          - Load history from file")
        print(f"  {Fore.CYAN}help          - Display this help message")
        print(f"  {Fore.CYAN}exit          - Exit the application")
        print("---------------------------------\n")

    def run(self):
        """Starts the REPL loop."""
        print(
            f"{Fore.CYAN}Welcome to the Calculator! "
            "Type 'help' for available commands."
        )
        
        while True:
            try:
                user_input = input("calc> ").strip()
                if not user_input:
                    continue
                    
                tokens = user_input.split()
                command = tokens[0].lower()
                
                if command == "exit":
                    print(f"{Fore.CYAN}Goodbye!")
                    break
                    
                elif command == "help":
                    self.print_help()
                    
                elif command == "history":
                    if not self.calculator.history:
                        print(f"{Fore.YELLOW}History is empty.")
                    else:
                        print(f"\n{Style.BRIGHT}--- Calculation History ---")
                        for idx, calc in enumerate(self.calculator.history, 1):
                            print(f"{idx}. {calc}")
                        print("---------------------------\n")
                        
                elif command == "clear":
                    self.calculator.clear_history()
                    print(f"{Fore.GREEN}History cleared.")
                    
                elif command == "undo":
                    if self.calculator.undo():
                        print(f"{Fore.GREEN}Successfully undone last calculation.")
                    else:
                        print(f"{Fore.YELLOW}Nothing to undo.")
                        
                elif command == "redo":
                    if self.calculator.redo():
                        print(f"{Fore.GREEN}Successfully redone calculation.")
                    else:
                        print(f"{Fore.YELLOW}Nothing to redo.")
                        
                elif command == "save":
                    self.calculator.save_history()
                    print(
                        f"{Fore.GREEN}History successfully saved to "
                        f"{self.calculator.config.history_file}"
                    )
                    
                elif command == "load":
                    self.calculator.load_history()
                    print(
                        f"{Fore.GREEN}History successfully loaded from "
                        f"{self.calculator.config.history_file}"
                    )
                    
                elif command in OperationFactory.get_supported_operations():
                    if len(tokens) != 3:
                        print(
                            f"{Fore.YELLOW}Error: Operation '{command}' requires "
                            "exactly 2 operands. Usage: <operation> <a> <b>"
                        )
                        continue
                        
                    _, a_str, b_str = tokens
                    result = self.calculator.perform_operation(command, a_str, b_str)
                    print(f"{Fore.GREEN}Result: {result}")
                    
                else:
                    print(
                        f"{Fore.YELLOW}Unknown command or operation: '{command}'. "
                        "Type 'help' for options."
                    )
                    
            except CalculatorError as e:
                self.logger.warning("Calculator command failed: %s", e)
                print(f"{Fore.RED}Error: {e}")
            except Exception as e:
                self.logger.exception("Unexpected calculator error: %s", e)
                print(f"{Fore.RED}Unexpected error: {e}")

if __name__ == "__main__":
    repl = CalculatorREPL()
    repl.run()