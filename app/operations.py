# app/operations.py
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from app.exceptions import OperationError

class Operation(ABC):
    """Abstract Base Class for all calculator operations (Strategy Pattern)."""
    
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Execute the operation on two operands and return the result."""
        pass

class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b

class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b

class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b

class Division(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Division by zero is not allowed.")
        return a / b

class Power(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        try:
            if b % 1 == 0:
                return a ** int(b)
            return Decimal(str(float(a) ** float(b)))
        except (InvalidOperation, Exception) as e:
            raise OperationError(f"Power operation failed: {e}") from e

class Root(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Root index cannot be zero.")
        if a < 0 and b % 2 == 0:
            raise OperationError("Even root of a negative number is not a real number.")
        try:
            return Decimal(str(float(a) ** (1.0 / float(b))))
        except (InvalidOperation, Exception) as e:
            raise OperationError(f"Root operation failed: {e}") from e
        
class Modulus(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Modulus by zero is not allowed.")
        return a % b

class IntegerDivision(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Integer division by zero is not allowed.")
        return a // b

class Percentage(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Percentage base cannot be zero.")
        return (a / b) * Decimal("100")

class AbsoluteDifference(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return abs(a - b)

class OperationFactory:
    """Factory class to manage and instantiate operations dynamically."""
    
    _operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntegerDivision,
        "percent": Percentage,
        "abs_diff": AbsoluteDifference,
    }
    
    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        op_class = cls._operations.get(operation_name.lower())
        if not op_class:
            raise OperationError(f"Unknown operation: '{operation_name}'")
        return op_class()
    
    @classmethod
    def get_supported_operations(cls) -> list:
        return list(cls._operations.keys())