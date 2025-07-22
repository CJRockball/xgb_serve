"""
Prediction logic for XGBoost model.
"""

import logging
from typing import Dict, Any, List, Union, Optional
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

from app.models.model_loader import ModelLoader


class PersonalityPredictor:
    """Personality prediction using XGBoost model."""
    
    def __init__(self, model_loader: ModelLoader):
        """
        Initialize predictor.
        
        Args:
            model_loader: Model loader instance
        """
        self.model_loader = model_loader
        self.logger = logging.getLogger(__name__)
        
        # Initialize encoders for categorical features
        self.label_encoders = {}
        self._setup_encoders()
    
    def _setup_encoders(self) -> None:
        """Setup label encoders for categorical features."""
        # These are the categorical features that need encoding
        categorical_features = {
            'Stage_fear': ['No', 'Yes'],
            'Drained_after_socializing': ['No', 'Yes']
        }
        
        for feature, categories in categorical_features.items():
            encoder = LabelEncoder()
            encoder.fit(categories)
            self.label_encoders[feature] = encoder
    
    def _preprocess_features(self, features: Dict[str, Any]) -> pd.DataFrame:
        """
        Preprocess features for prediction.
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Preprocessed features as DataFrame
        """
        # Create DataFrame
        df = pd.DataFrame([features])
        
        # Handle categorical features
        for feature, encoder in self.label_encoders.items():
            if feature in df.columns:
                # Handle missing values - replace with most common class
                df[feature] = df[feature].fillna('No')
                try:
                    df[feature] = encoder.transform(df[feature])
                except ValueError as e:
                    self.logger.warning(f"Unknown category in {feature}: {df[feature].iloc[0]}")
                    # Use default value (0 for 'No')
                    df[feature] = 0
        
        # Handle numerical features - fill missing values with median
        numerical_features = [
            'Time_spent_Alone', 'Social_event_attendance', 'Going_outside',
            'Friends_circle_size', 'Post_frequency'
        ]
        
        for feature in numerical_features:
            if feature in df.columns:
                # For missing values, use reasonable defaults
                if feature == 'Time_spent_Alone':
                    df[feature] = df[feature].fillna(5.0)
                elif feature == 'Social_event_attendance':
                    df[feature] = df[feature].fillna(5.0)
                elif feature == 'Going_outside':
                    df[feature] = df[feature].fillna(5.0)
                elif feature == 'Friends_circle_size':
                    df[feature] = df[feature].fillna(8.0)
                elif feature == 'Post_frequency':
                    df[feature] = df[feature].fillna(5.0)
        
        # Ensure all required features are present
        required_features = self.model_loader.get_feature_names()
        for feature in required_features:
            if feature not in df.columns:
                # Add missing feature with default value
                if feature in ['Stage_fear', 'Drained_after_socializing']:
                    df[feature] = 0  # Default to 'No' encoded
                else:
                    df[feature] = 5.0  # Default numerical value
        
        # Reorder columns to match expected feature order
        df = df[required_features]
        
        return df
    
    def predict_single(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction for a single sample.
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Preprocess features
            processed_features = self._preprocess_features(features)
            
            # Get model and make prediction
            model = self.model_loader.get_model()
            
            # Get prediction and probability
            prediction = model.predict(processed_features)[0]
            probabilities = model.predict_proba(processed_features)[0]
            
            # Map prediction to label
            target_mapping = self.model_loader.get_target_mapping()
            predicted_label = target_mapping[prediction]
            
            # Create result
            result = {
                'prediction': predicted_label,
                'prediction_code': int(prediction),
                'probabilities': {
                    'Introvert': float(probabilities[0]),
                    'Extrovert': float(probabilities[1])
                },
                'confidence': float(max(probabilities))
            }
            
            self.logger.info(f"Prediction made: {predicted_label} (confidence: {result['confidence']:.3f})")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Prediction failed: {str(e)}")
            raise
    
    def predict_batch(self, features_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Make predictions for a batch of samples.
        
        Args:
            features_list: List of feature dictionaries
            
        Returns:
            List of prediction results
        """
        try:
            results = []
            
            for features in features_list:
                result = self.predict_single(features)
                results.append(result)
            
            self.logger.info(f"Batch prediction completed for {len(features_list)} samples")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Batch prediction failed: {str(e)}")
            raise