"""
Input validation utilities.
"""

from typing import Dict, Any, List, Optional, Union
import logging


logger = logging.getLogger(__name__)


def validate_required_features(sample: Dict[str, Any], required_features: List[str]) -> List[str]:
    """
    Validate that required features are present.
    
    Args:
        sample: Dictionary containing feature values
        required_features: List of required feature names
        
    Returns:
        List of validation errors
    """
    errors = []
    
    for feature in required_features:
        if feature not in sample:
            errors.append(f"Missing required feature: {feature}")
    
    return errors


def validate_feature_types(sample: Dict[str, Any]) -> List[str]:
    """
    Validate feature data types.
    
    Args:
        sample: Dictionary containing feature values
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Define expected types
    type_mapping = {
        'Time_spent_Alone': (int, float),
        'Social_event_attendance': (int, float),
        'Going_outside': (int, float),
        'Friends_circle_size': (int, float),
        'Post_frequency': (int, float),
        'Stage_fear': str,
        'Drained_after_socializing': str
    }
    
    for feature, expected_type in type_mapping.items():
        if feature in sample and sample[feature] is not None:
            value = sample[feature]
            if not isinstance(value, expected_type):
                errors.append(f"{feature} must be of type {expected_type}")
    
    return errors


def validate_feature_values(sample: Dict[str, Any]) -> List[str]:
    """
    Validate feature values are within acceptable ranges.
    
    Args:
        sample: Dictionary containing feature values
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Validate numerical ranges
    numerical_ranges = {
        'Time_spent_Alone': (0, 11),
        'Social_event_attendance': (0, 10),
        'Going_outside': (0, 10),
        'Friends_circle_size': (0, 15),
        'Post_frequency': (0, 10)
    }
    
    for feature, (min_val, max_val) in numerical_ranges.items():
        if feature in sample and sample[feature] is not None:
            value = sample[feature]
            if not (min_val <= value <= max_val):
                errors.append(f"{feature} must be between {min_val} and {max_val}, got {value}")
    
    # Validate categorical values
    categorical_values = {
        'Stage_fear': ['Yes', 'No', 'yes', 'no'],
        'Drained_after_socializing': ['Yes', 'No', 'yes', 'no']
    }
    
    for feature, valid_values in categorical_values.items():
        if feature in sample and sample[feature] is not None:
            value = sample[feature]
            if value not in valid_values:
                errors.append(f"{feature} must be one of {valid_values}, got {value}")
    
    return errors


def validate_sample(sample: Dict[str, Any], required_features: Optional[List[str]] = None) -> List[str]:
    """
    Comprehensive validation of a sample.
    
    Args:
        sample: Dictionary containing feature values
        required_features: Optional list of required features
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Validate required features
    if required_features:
        errors.extend(validate_required_features(sample, required_features))
    
    # Validate feature types
    errors.extend(validate_feature_types(sample))
    
    # Validate feature values
    errors.extend(validate_feature_values(sample))
    
    if errors:
        logger.warning(f"Validation errors found: {errors}")
    
    return errors


def sanitize_sample(sample: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize sample by cleaning and normalizing values.
    
    Args:
        sample: Dictionary containing feature values
        
    Returns:
        Sanitized sample
    """
    sanitized = sample.copy()
    
    # Normalize categorical values
    categorical_features = ['Stage_fear', 'Drained_after_socializing']
    
    for feature in categorical_features:
        if feature in sanitized and sanitized[feature] is not None:
            value = str(sanitized[feature]).strip().title()
            sanitized[feature] = value
    
    # Ensure numerical values are numeric
    numerical_features = [
        'Time_spent_Alone', 'Social_event_attendance', 'Going_outside',
        'Friends_circle_size', 'Post_frequency'
    ]
    
    for feature in numerical_features:
        if feature in sanitized and sanitized[feature] is not None:
            try:
                sanitized[feature] = float(sanitized[feature])
            except (ValueError, TypeError):
                logger.warning(f"Could not convert {feature} to float: {sanitized[feature]}")
                sanitized[feature] = None
    
    return sanitized