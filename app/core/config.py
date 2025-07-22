"""
Configuration management for the XGBoost personality prediction API.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"
    
    # Model Configuration
    xgb_model_path: str = "models/model.ubj"  # Path to XGBoost model file
    # Add other config fields here, e.g.:
    # app_name: str = "Personality Predictor API"
    # log_level: str = "INFO"

    
    # Features configuration
    feature_names: list = [
        "Stage_fear",
        "Drained_after_socializing", 
        "Time_spent_Alone",
        "Social_event_attendance",
        "Going_outside",
        "Friends_circle_size",
        "Post_frequency"
    ]
    
    # Target mapping
    target_mapping: dict = {0: "Introvert", 1: "Extrovert"}
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()