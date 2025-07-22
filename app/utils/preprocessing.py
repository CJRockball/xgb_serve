"""
Data preprocessing utilities.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


def preprocess_single_sample(sample: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocess a single sample for prediction.
    
    Args:
        sample: Dictionary containing feature values
        
    Returns:
        Preprocessed sample
    """
    processed = sample.copy()
    
    # Handle categorical features
    categorical_mapping = {
        'Stage_fear': {'Yes': 1, 'No': 0},
        'Drained_after_socializing': {'Yes': 1, 'No': 0}
    }
    
    for feature, mapping in categorical_mapping.items():
        if feature in processed:
            value = processed[feature]
            if value is not None:
                processed[feature] = mapping.get(value, 0)
            else:
                processed[feature] = 0
    
    # Handle numerical features with default values
    numerical_defaults = {
        'Time_spent_Alone': 5.0,
        'Social_event_attendance': 5.0,
        'Going_outside': 5.0,
        'Friends_circle_size': 8.0,
        'Post_frequency': 5.0
    }
    
    for feature, default_value in numerical_defaults.items():
        if feature in processed:
            if processed[feature] is None:
                processed[feature] = default_value
        else:
            processed[feature] = default_value
    
    return processed


def validate_feature_ranges(sample: Dict[str, Any]) -> List[str]:
    """
    Validate feature ranges.
    
    Args:
        sample: Dictionary containing feature values
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Define valid ranges
    ranges = {
        'Time_spent_Alone': (0, 11),
        'Social_event_attendance': (0, 10),
        'Going_outside': (0, 10),
        'Friends_circle_size': (0, 15),
        'Post_frequency': (0, 10)
    }
    
    for feature, (min_val, max_val) in ranges.items():
        if feature in sample and sample[feature] is not None:
            value = sample[feature]
            if not (min_val <= value <= max_val):
                errors.append(f"{feature} must be between {min_val} and {max_val}")
    
    # Validate categorical features
    categorical_values = {
        'Stage_fear': ['Yes', 'No'],
        'Drained_after_socializing': ['Yes', 'No']
    }
    
    for feature, valid_values in categorical_values.items():
        if feature in sample and sample[feature] is not None:
            value = sample[feature]
            if value not in valid_values:
                errors.append(f"{feature} must be one of {valid_values}")
    
    return errors


def convert_to_model_format(sample: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert sample to model input format.
    
    Args:
        sample: Dictionary containing feature values
        
    Returns:
        DataFrame in model input format
    """
    # Define feature order expected by the model
    feature_order = [
        'Stage_fear',
        'Drained_after_socializing',
        'Time_spent_Alone',
        'Social_event_attendance',
        'Going_outside',
        'Friends_circle_size',
        'Post_frequency'
    ]
    
    # Create DataFrame with single row
    df = pd.DataFrame([sample])
    
    # Ensure all required features are present
    for feature in feature_order:
        if feature not in df.columns:
            df[feature] = 0 if feature in ['Stage_fear', 'Drained_after_socializing'] else 5.0
    
    # Reorder columns
    df = df[feature_order]
    
    return df