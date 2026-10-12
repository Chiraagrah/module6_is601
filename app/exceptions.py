# app/exceptions.py

class CalculatorError(Exception):
    """Base exception for all calculator-related errors."""
    pass

class ValidationError(CalculatorError):
    """Raised when input validation fails."""
    pass

class OperationError(CalculatorError):
    """Raised when an arithmetic or calculation error occurs (e.g., division by zero)."""
    pass

class ConfigurationError(CalculatorError):
    """Raised when configuration settings are invalid or missing."""
    pass