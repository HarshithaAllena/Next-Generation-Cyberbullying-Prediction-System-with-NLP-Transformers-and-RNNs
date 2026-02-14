# System Architecture

This document describes the microservices architecture of the Cyberbullying NLP Monorepo.

## Architecture Overview

The system follows a microservices architecture with the following components:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     API Gateway (Port 3000)                              │
│                    Main entry point, routing, auth                      │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
┌─────────────────────────────────────┴───────────────────────────────────┐
│                     Web GUI (Port 8501)                                  │
│              Streamlit Interface for Predictions                         │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
           ┌───────────────────────────┼───────────────────────────┐
           │                           │                           │
           ▼                           ▼                           ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│ Preprocessing      │   │ Feature Service     │   │ Training Service     │
│ Service (3001)     │   │ (3002)              │   │ (3004)               │
│                    │   │                     │   │                     │
│ • Text cleaning    │   │ • Feature extraction │   │ • Model training    │
│ • Normalization   │   │ • Embeddings        │   │ • Evaluation        │
│ • Tokenization    │   │ • Similarity        │   │ • Checkpointing     │
└─────────────────────┘   └──────────┬──────────┘   └─────────────────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │ Prediction Service  │
                          │ (3003)             │
                          │                     │
                          │ • Inference        │
                          │ • Real-time pred.  │
                          │ • Batch processing │
                          └─────────────────────┘
```

## Microservices

### API Gateway (Port 3000)

**Purpose**: Main entry point for all client requests

**Responsibilities**:
- Request routing to downstream services
- Authentication and authorization
- Rate limiting
- Request/response transformation

**Key Files**:
- `apps/api-gateway/src/main.py` — FastAPI application

### Web GUI (Port 8501)

**Purpose**: Interactive browser-based interface for predictions

**Responsibilities**:
- Real-time text input for instant predictions
- Model selection and comparison
- Display confidence scores and prediction breakdown
- Batch prediction support
- Historical prediction tracking

**Key Files**:
- `apps/web-gateway/src/main.py` — Streamlit application
- `apps/web-gateway/src/gui/prediction_view.py` — Prediction interface
- `apps/web-gateway/src/gui/batch_view.py` — Batch processing interface

**Integration**:
- Communicates with Prediction Service via REST API
- Displays results from API Gateway or direct prediction service calls

### Preprocessing Service (Port 3001)

**Purpose**: Clean and normalize raw text input

**Responsibilities**:
- Text cleaning (remove special characters, HTML)
- Case normalization
- Tokenization
- Language detection

**Key Files**:
- `apps/preprocessing-service/src/preprocessing_service/cleaners.py`
- `apps/preprocessing-service/src/preprocessing_service/tokenizers.py`

### Feature Service (Port 3002)

**Purpose**: Extract features from preprocessed text

**Responsibilities**:
- Statistical feature extraction (word count, char count)
- Social feature extraction (mentions, hashtags, URLs)
- Linguistic feature extraction (lexical diversity, sentiment)
- Embedding generation

**Key Files**:
- `apps/feature-service/src/feature_service/extractor.py`
- `apps/feature-service/src/feature_service/embeddings.py`

### Training Service (Port 3004)

**Purpose**: Train ML models on labeled data

**Responsibilities**:
- Data loading and preprocessing
- Model training (Transformers, RNNs)
- Evaluation metrics
- Model checkpointing

**Key Files**:
- `apps/training-service/src/training_service/trainer.py`

### Prediction Service (Port 3003)

**Purpose**: Run inference on trained models

**Responsibilities**:
- Real-time prediction
- Batch prediction
- Confidence scoring
- Model versioning

**Key Files**:
- `apps/prediction-service/src/prediction_service/predictor.py`

## Shared Packages

### shared-common

**Purpose**: Common utilities used across all services

**Contents**:
- Logging configuration (`logging_config.py`)
- Custom decorators (`decorators.py`)
- Exception classes (`exceptions.py`)
- Configuration management (`config.py`)
- Utility functions (`utils.py`)

### ml-core

**Purpose**: Core ML functionality

**Contents**:
- Base classifier (`models/base.py`)
- RNN models (`models/rnn_models.py`) — LSTM, GRU, BiLSTM, BiGRU
- Transformer models (`models/transformer_models.py`) — BERT, RoBERTa, DeBERTa
- Ensemble models (`models/ensemble.py`)
- Evaluation metrics (`evaluation/metrics.py`)

### data-models

**Purpose**: Pydantic schemas for data validation

**Schemas**:
- Text schemas (`schemas/text.py`)
- Feature schemas (`schemas/features.py`)
- Training schemas (`schemas/training.py`)
- Prediction schemas (`schemas/prediction.py`)

## Data Flow

### Web GUI Prediction Pipeline

```
User Input (Browser)
       │
       ▼
Web GUI (Streamlit)
       │
       ▼
Prediction Service
       │
       ▼
Preprocessed Result
       │
       ▼
User Display
```

### REST API Prediction Pipeline

```
Client Request
      │
      ▼
API Gateway ───────┐
      │            │
      ▼            │
Preprocessing ────┤
Service           │
      │           │
      ▼           │
Feature Service ──┼──► Pipeline Coordinator
      │           │
      ▼           │
Prediction ──────┘
Service
      │
      ▼
Client Response
```

### Training Pipeline

```
Training Data
      │
      ▼
Preprocessing
      │
      ▼
Feature Extraction
      │
      ▼
Model Training
(Transformers/RNNs)
      │
      ▼
Evaluation
      │
      ▼
Model Registry
```

## Configuration

All services use environment-based configuration via Pydantic Settings. See `packages/shared-common/src/cyberbullying_shared_common/config.py` for all available settings.

Key settings include:

- Service URLs (preprocessing, feature, prediction, training)
- Database and Redis connections
- MLflow tracking URI
- Model settings (cache directory, default versions)
- Security settings (JWT secret, algorithms)
- Web GUI settings (port, theme, API endpoint)

## Service Communication

Services communicate via:

1. **HTTP/REST** — Synchronous calls between services
2. **Web GUI to API** — Streamlit calls prediction service endpoints
3. **Message Queue** (future) — Asynchronous processing
4. **gRPC** (future) — High-performance inter-service communication

## Health Checks

Each service exposes a `/health` endpoint for monitoring:

```bash
curl http://localhost:3000/health  # API Gateway
curl http://localhost:3001/health  # Preprocessing
curl http://localhost:3002/health  # Feature
curl http://localhost:3003/health  # Prediction
```

Web GUI uses Streamlit's built-in health check at `http://localhost:8501/_stcore/health`

## Scalability

The architecture supports:

- **Horizontal Scaling**: Each service can be scaled independently
- **Load Balancing**: API Gateway distributes load
- **Caching**: Redis caching for predictions
- **Batch Processing**: Efficient bulk inference
- **Web GUI Scaling**: Multiple Streamlit instances behind load balancer
