# app/input_validators.py
from decimal import Decimal, InvalidOperation
from app.exceptions import ValidationError

class InputValidator:
    """Validates and converts user inputs for calculator operations."""
    
    @staticmethod
    def validate_number(value, max_limit: float = 1000000.0) -> Decimal:
        """Validates that a value can be converted to Decimal and is within limits."""
        try:
            dec_val = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError) as e:
            raise ValidationError(f"Invalid numeric input: '{value}'. Must be a valid number.") from e
        
        if abs(dec_val) > Decimal(str(max_limit)):
            raise ValidationError(f"Input '{dec_val}' exceeds maximum allowed limit of {max_limit}.")
        
        return dec_val