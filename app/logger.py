# app/logger.py
import logging
import sys
from pathlib import Path

def setup_logger(log_file: Path) -> logging.Logger:
    """Configures and returns the application logger."""
    logger = logging.getLogger("CalculatorLogger")
    logger.setLevel(logging.INFO)
    
    # Avoid adding duplicate handlers if already configured
    if logger.handlers:
        return logger
        
    # File handler
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger