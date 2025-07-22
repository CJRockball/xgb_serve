"""
Model loading utilities for XGBoost model.
"""

import os
import logging
from typing import Optional, List, Dict, Any
import xgboost as xgb
import pandas as pd
import numpy as np

from app.core.config import get_settings


class ModelLoader:
    """XGBoost model loader and manager."""
    
    def __init__(self, model_path: str):
        """
        Initialize model loader.
        
        Args:
            model_path: Path to the XGBoost model file
        """
        self.model_path = model_path
        self.model: Optional[xgb.XGBClassifier] = None
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        
    async def load_model(self) -> None:
        """Load the XGBoost model from file."""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            self.logger.info(f"Loading model from {self.model_path}")
            
            # Load the model
            self.model = xgb.XGBClassifier()
            self.model.load_model(self.model_path)
            
            self.logger.info("Model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None
    
    def get_model(self) -> xgb.XGBClassifier:
        """Get the loaded model."""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded")
        return self.model
    
    def get_feature_names(self) -> List[str]:
        """Get feature names from settings."""
        return self.settings.feature_names
    
    def get_target_mapping(self) -> Dict[int, str]:
        """Get target mapping from settings."""
        return self.settings.target_mapping