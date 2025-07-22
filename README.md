# XGBoost Personality Prediction API

A FastAPI-based REST API for predicting personality types (Introvert/Extrovert) using an XGBoost machine learning model.

## Features

- **Single Prediction**: Predict personality type for individual samples
- **Batch Prediction**: Predict personality types for multiple samples at once
- **Health Checks**: Comprehensive health monitoring endpoints
- **Metrics**: Application performance and usage metrics
- **Input Validation**: Robust input validation and error handling
- **Containerized**: Docker support for easy deployment

## Model Features

The model uses the following features to predict personality type:

- `time_spent_alone`: Hours spent alone per day (0-11)
- `stage_fear`: Stage fear (Yes/No)
- `social_event_attendance`: Social event attendance frequency (0-10)
- `going_outside`: Going outside frequency (0-10)
- `drained_after_socializing`: Drained after socializing (Yes/No)
- `friends_circle_size`: Number of friends in circle (0-15)
- `post_frequency`: Social media posting frequency (0-10)

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Metrics: http://localhost:8000/health/metrics

### Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t xgb-personality-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 xgb-personality-api
   ```

## API Endpoints

### Prediction Endpoints

#### Single Prediction
```
POST /predict/single
```

Example request:
```json
{
  "features": {
    "time_spent_alone": 5.0,
    "stage_fear": "No",
    "social_event_attendance": 7.0,
    "going_outside": 6.0,
    "drained_after_socializing": "Yes",
    "friends_circle_size": 8.0,
    "post_frequency": 4.0
  }
}
```

Example response:
```json
{
  "success": true,
  "result": {
    "prediction": "Extrovert",
    "prediction_code": 1,
    "probabilities": {
      "Introvert": 0.23,
      "Extrovert": 0.77
    },
    "confidence": 0.77
  },
  "message": "Prediction completed successfully"
}
```

#### Batch Prediction
```
POST /predict/batch
```

Example request:
```json
{
  "features": [
    {
      "time_spent_alone": 5.0,
      "stage_fear": "No",
      "social_event_attendance": 7.0,
      "going_outside": 6.0,
      "drained_after_socializing": "Yes",
      "friends_circle_size": 8.0,
      "post_frequency": 4.0
    },
    {
      "time_spent_alone": 2.0,
      "stage_fear": "Yes",
      "social_event_attendance": 3.0,
      "going_outside": 2.0,
      "drained_after_socializing": "No",
      "friends_circle_size": 12.0,
      "post_frequency": 8.0
    }
  ]
}
```

### Health Check Endpoints

- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check (model loaded)
- `GET /health/live` - Liveness check
- `GET /health/metrics` - Application metrics

### Example Endpoint
```
GET /predict/example
```
Returns example request formats for both single and batch predictions.

## Model Training

To retrain the model with new data:

1. **Prepare your data**: Ensure your CSV file has the same structure as `data/personality_train.csv`

2. **Run training script**:
   ```bash
   python scripts/train_model.py
   ```

3. **The trained model will be saved to** `models/model.ubj`

## Configuration

The application can be configured using environment variables:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)
- `MODEL_PATH`: Path to model file (default: models/model.ubj)

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── health.py    # Health check endpoints
│   │       └── predict.py   # Prediction endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration
│   │   └── logging.py       # Logging setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── model_loader.py  # Model loading
│   │   └── predictor.py     # Prediction logic
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── request.py       # Request schemas
│   │   └── response.py      # Response schemas
│   └── utils/
│       ├── __init__.py
│       ├── preprocessing.py # Data preprocessing
│       └── validation.py    # Input validation
├── data/
│   └── personality_train.csv # Training data
├── models/
│   └── model.ubj            # Trained XGBoost model
├── scripts/
│   └── train_model.py       # Training script
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Error Handling

The API provides comprehensive error handling with detailed error messages:

- **400 Bad Request**: Invalid input data
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server errors
- **503 Service Unavailable**: Model not loaded

## Performance Considerations

- The model is loaded once at startup and cached in memory
- Predictions are fast (typically < 10ms per sample)
- Batch predictions are optimized for multiple samples
- Health checks and metrics have minimal overhead

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Quality

The codebase follows Python best practices:

- Type hints throughout
- Comprehensive logging
- Input validation
- Error handling
- Documentation strings

## License

This project is licensed under the MIT License.