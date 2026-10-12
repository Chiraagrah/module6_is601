# app/calculator_config.py
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
            
            self.max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
            self.auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
            self.precision = int(os.getenv("CALCULATOR_PRECISION", "4"))
            self.max_input_value = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000.0"))
            self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
            
            # Ensure directories exist
            self.log_dir.mkdir(parents=True, exist_ok=True)
            self.history_dir.mkdir(parents=True, exist_ok=True)
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}") from e