#!/usr/bin/env python3
"""
Test script to validate the FastAPI setup and model loading.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

async def test_setup():
    """Test the basic setup."""
    print("Testing XGBoost Personality Prediction API Setup...")
    
    # Test 1: Import modules
    try:
        from app.core.config import get_settings
        from app.models.model_loader import ModelLoader
        from app.models.predictor import PersonalityPredictor
        print("✓ All modules imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Test 2: Configuration
    try:
        settings = get_settings()
        print(f"✓ Configuration loaded: {settings.xgb_model_path}")
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False
    
    # Test 3: Check model file exists
    if os.path.exists(settings.xgb_model_path):
        print(f"✓ Model file exists: {settings.xgb_model_path}")
    else:
        print(f"✗ Model file not found: {settings.xgb_model_path}")
        return False
    
    # Test 4: Model loading
    try:
        model_loader = ModelLoader(settings.xgb_model_path)
        await model_loader.load_model()
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"✗ Model loading error: {e}")
        return False
    
    # Test 5: Prediction test
    try:
        predictor = PersonalityPredictor(model_loader)
        
        # Test sample
        test_features = {
            'Time_spent_Alone': 5.0,
            'Stage_fear': 'No',
            'Social_event_attendance': 7.0,
            'Going_outside': 6.0,
            'Drained_after_socializing': 'Yes',
            'Friends_circle_size': 8.0,
            'Post_frequency': 4.0
        }
        
        result = predictor.predict_single(test_features)
        print(f"✓ Test prediction successful: {result['prediction']} (confidence: {result['confidence']:.3f})")
    except Exception as e:
        print(f"✗ Prediction error: {e}")
        return False
    
    print("\\n🎉 All tests passed! The API is ready to run.")
    print("\\nTo start the server, run:")
    print("python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
    return True

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run tests
    success = asyncio.run(test_setup())
    sys.exit(0 if success else 1)

"""
# Make it executable
os.chmod('test_setup.py', 0o755)

print("\\nSetup complete! Here's what was created:")
print("\\n📁 Folder Structure:")
print("├── app/                    # FastAPI application")
print("│   ├── main.py            # Main FastAPI app")
print("│   ├── api/endpoints/     # API endpoints")
print("│   ├── core/              # Configuration & logging")
print("│   ├── models/            # Model loading & prediction")
print("│   ├── schemas/           # Request/response schemas")
print("│   └── utils/             # Utilities")
print("├── data/                  # Training data")
print("├── models/                # Trained model")
print("├── scripts/               # Training scripts")
print("├── requirements.txt       # Dependencies")
print("├── Dockerfile            # Docker configuration")
print("├── README.md             # Documentation")
print("└── test_setup.py         # Setup validation")

print("\\n🚀 Next steps:")
print("1. Run the setup test: python test_setup.py")
print("2. Install dependencies: pip install -r requirements.txt")
print("3. Start the server: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
print("4. Access the API docs: http://localhost:8000/docs")
"""