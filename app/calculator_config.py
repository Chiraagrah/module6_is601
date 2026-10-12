# app/calculator_config.py
import math
import os
from pathlib import Path
from dotenv import load_dotenv
from app.exceptions import ConfigurationError

load_dotenv()

class CalculatorConfig:
    """Manages application configurations using environment variables."""
    
    def __init__(self):
        try:
            self.log_dir = Path(os.getenv("CALCULATOR_LOG_DIR", "logs"))
            self.history_dir = Path(os.getenv("CALCULATOR_HISTORY_DIR", "data"))
            
            # Resolve file paths relative to directories
            self.log_file = self.log_dir / os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
            self.history_file = self.history_dir / os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")
            
            try:
                self.max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
            except ValueError as e:
                raise ValueError("CALCULATOR_MAX_HISTORY_SIZE must be an integer.") from e
            auto_save_value = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower()
            if auto_save_value not in {"true", "false"}:
                raise ValueError("CALCULATOR_AUTO_SAVE must be 'true' or 'false'.")
            self.auto_save = auto_save_value == "true"
            try:
                self.precision = int(os.getenv("CALCULATOR_PRECISION", "4"))
            except ValueError as e:
                raise ValueError("CALCULATOR_PRECISION must be an integer.") from e
            try:
                self.max_input_value = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000.0"))
            except ValueError as e:
                raise ValueError("CALCULATOR_MAX_INPUT_VALUE must be numeric.") from e
            self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

            if self.max_history_size <= 0:
                raise ValueError("CALCULATOR_MAX_HISTORY_SIZE must be greater than zero.")
            if self.precision < 0:
                raise ValueError("CALCULATOR_PRECISION must be zero or greater.")
            if not math.isfinite(self.max_input_value) or self.max_input_value <= 0:
                raise ValueError("CALCULATOR_MAX_INPUT_VALUE must be a finite number greater than zero.")
            
            # Ensure directories exist
            self.log_dir.mkdir(parents=True, exist_ok=True)
            self.history_dir.mkdir(parents=True, exist_ok=True)
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}") from e