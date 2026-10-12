# main.py
from app.calculator_repl import CalculatorREPL

def main():
    """Entry point for the Enhanced Calculator application."""
    repl = CalculatorREPL()
    repl.run()

if __name__ == "__main__":
    main()