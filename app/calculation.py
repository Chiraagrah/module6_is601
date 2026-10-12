# app/calculation.py
from decimal import Decimal
from datetime import datetime

class Calculation:
    """Represents a single calculation instance."""
    
    def __init__(self, operation_name: str, a: Decimal, b: Decimal, result: Decimal, timestamp: datetime = None):
        self.operation_name = operation_name
        self.a = a
        self.b = b
        self.result = result
        self.timestamp = timestamp or datetime.now()
        
    def to_dict(self) -> dict:
        """Serializes calculation to a dictionary for pandas/CSV storage."""
        return {
            "operation": self.operation_name,
            "operand_a": float(self.a),
            "operand_b": float(self.b),
            "result": float(self.result),
            "timestamp": self.timestamp.isoformat()
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Calculation instance from a dictionary."""
        return cls(
            operation_name=data["operation"],
            a=Decimal(str(data["operand_a"])),
            b=Decimal(str(data["operand_b"])),
            result=Decimal(str(data["result"])),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        
    def __repr__(self) -> str:
        return f"{self.operation_name}({self.a}, {self.b}) = {self.result} [{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]"