# app/history.py
from abc import ABC, abstractmethod
import pandas as pd
from typing import List
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.logger import setup_logger

class HistoryObserver(ABC):
    """Abstract Base Class for calculator history observers (Observer Pattern)."""
    
    @abstractmethod
    def update(self, calculation: Calculation, history: List[Calculation]):
        pass


class LoggingObserver(HistoryObserver):
    """Observer that logs calculation events."""
    
    def __init__(self, config: CalculatorConfig):
        self.logger = setup_logger(config.log_file)
        
    def update(self, calculation: Calculation, history: List[Calculation]):
        self.logger.info(f"New calculation performed: {calculation}")


class AutoSaveObserver(HistoryObserver):
    """Observer that automatically saves history to CSV using pandas."""
    
    def __init__(self, config: CalculatorConfig):
        self.config = config
        self.logger = setup_logger(config.log_file)
        
    def update(self, calculation: Calculation, history: List[Calculation]):
        if not self.config.auto_save:
            return
            
        try:
            if not history:
                return
            data = [calc.to_dict() for calc in history]
            df = pd.DataFrame(data)
            self.config.history_dir.mkdir(parents=True, exist_ok=True)
            df.to_csv(self.config.history_file, index=False, encoding=self.config.default_encoding)
        except Exception as e:
            self.logger.warning("Auto-save failed: %s", e, exc_info=True)