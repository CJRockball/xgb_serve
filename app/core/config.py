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
    
    # Database Configuration - MISSING IN CURRENT VERSION
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/xgb_serve"
    DATABASE_TEST_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/xgb_serve_test"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Model Configuration  
    xgb_model_path: str = "models/model.ubj"
    MODEL_VERSION: str = "1.0.0"  # Added for database logging
    
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
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
