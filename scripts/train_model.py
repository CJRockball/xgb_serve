"""
XGBoost Model Training Script for Personality Prediction

This script replicates the training process from xgb2_clean_single_model.py
with proper organization and model saving.
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging
import os


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def load_and_preprocess_data(data_path: str):
    """
    Load and preprocess the training data.
    
    Args:
        data_path: Path to the training data CSV file
        
    Returns:
        Tuple of (X, y) where X is features and y is target
    """
    logger = logging.getLogger(__name__)
    
    # Load data
    logger.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    
    # Drop ID column
    df = df.drop(columns=['id'])
    
    # Define target and features
    target = 'Personality'
    cats = ['Stage_fear', 'Drained_after_socializing', 'Time_spent_Alone', 
            'Social_event_attendance', 'Going_outside', 'Friends_circle_size', 
            'Post_frequency']
    
    # Ordinal transformation for target
    df[target], list_cat_names = df[target].factorize()
    target_dict = {i: name for i, name in enumerate(list_cat_names)}
    logger.info(f"Target mapping: {target_dict}")
    
    # Ordinal transformation for features
    for name in cats:
        df[name], _ = df[name].factorize(use_na_sentinel=True)
    
    # Set data types
    df[target] = df[target].astype(bool)
    df[cats] = df[cats].astype('category')
    
    # Separate features and target
    X = df[cats].copy()
    y = df[target].copy()
    
    logger.info(f"Data shape: {X.shape}")
    logger.info(f"Target distribution: {y.value_counts()}")
    
    return X, y, target_dict


def train_model(X, y, target_dict):
    """
    Train the XGBoost model.
    
    Args:
        X: Features
        y: Target
        target_dict: Target label mapping
        
    Returns:
        Trained XGBoost model
    """
    logger = logging.getLogger(__name__)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1337, stratify=y
    )
    
    logger.info(f"Training set shape: {X_train.shape}")
    logger.info(f"Test set shape: {X_test.shape}")
    
    # Initialize model with same parameters as original
    model = XGBClassifier(
        tree_method='hist',
        n_estimators=59,
        objective='binary:logistic',
        enable_categorical=True,
        eval_metric=['logloss', 'auc', 'error'],
        n_jobs=4,
        random_state=1337,
        max_depth=3,
        verbosity=1
    )
    
    # Train model
    logger.info("Training model...")
    model.fit(X_train, y_train, verbose=25)
    
    # Evaluate model
    logger.info("Evaluating model...")
    
    # Training accuracy
    train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_pred)
    logger.info(f"Training accuracy: {train_accuracy:.4f}")
    
    # Test accuracy
    test_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_pred)
    logger.info(f"Test accuracy: {test_accuracy:.4f}")
    
    # Classification report
    logger.info("Classification Report:")
    logger.info(classification_report(y_test, test_pred, 
                                   target_names=list(target_dict.values())))
    
    # Confusion matrix
    logger.info("Confusion Matrix:")
    logger.info(confusion_matrix(y_test, test_pred))
    
    return model


def save_model(model, model_path: str):
    """
    Save the trained model.
    
    Args:
        model: Trained XGBoost model
        model_path: Path to save the model
    """
    logger = logging.getLogger(__name__)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Save model
    logger.info(f"Saving model to {model_path}")
    model.save_model(model_path)
    
    logger.info("Model saved successfully")


def main():
    """Main training function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting XGBoost personality prediction model training")
    
    # Paths
    data_path = 'data/personality_train.csv'
    model_path = 'models/model.ubj'
    
    try:
        # Load and preprocess data
        X, y, target_dict = load_and_preprocess_data(data_path)
        
        # Train model
        model = train_model(X, y, target_dict)
        
        # Save model
        save_model(model, model_path)
        
        logger.info("Training completed successfully!")
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()