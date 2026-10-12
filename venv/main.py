'''
An object oriented based repl calculator that can performs basic arithmetic operations

It demonstrates OOP Principles, design patterns, and Python best practices through a calculator application.

Key Features:
1. Design Patterns: Singleton, Strategy, Observer, Factory, Command, Memento
2. Error Handling: Custom exception hierarchy
3. Input Validation: Robust input checking
4. Persistence: History saving/loading
5. Testing: Unit test suite
6. Logging: Comprehensive logging system
7. Documentation: Educational comments
8. Type Hints: Static type checking support

'''

from app.calculator import calculator

if __name__ == "__main__":
    calc = calculator.Calculator()
    calc.run()
    