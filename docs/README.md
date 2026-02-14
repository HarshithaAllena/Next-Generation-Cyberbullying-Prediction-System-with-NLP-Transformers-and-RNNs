# Cyberbullying NLP Monorepo

> Next-Generation Cyberbullying Prediction System with NLP, Transformers, and RNNs

A production-ready microservices architecture for detecting cyberbullying in text using state-of-the-art NLP techniques including BERT, RoBERTa, DeBERTa, and recurrent neural networks (LSTM, GRU, BiLSTM).

## Overview

This monorepo contains a complete pipeline for cyberbullying detection:

- **Text Preprocessing** — Cleaning, normalization, tokenization
- **Feature Extraction** — Statistical, social, and linguistic features
- **Model Training** — Transformer and RNN-based classifiers
- **Prediction** — Real-time and batch inference
- **Explainability** — SHAP, LIME, attention visualization
- **Web GUI** — Interactive browser-based interface for predictions

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.11+ |
| **Package Manager** | Poetry |
| **NLP** | Transformers (BERT, RoBERTa, DeBERTa), RNNs (LSTM, GRU, BiLSTM) |
| **ML Frameworks** | PyTorch, TensorFlow |
| **API** | FastAPI |
| **Web GUI** | Streamlit |
| **XAI** | SHAP, LIME |
| **Tracking** | MLflow |

## Quick Start

### Install Dependencies

```bash
# macOS / Linux
poetry install

# Windows (PowerShell)
poetry install
```

### Run API Gateway

```bash
# macOS / Linux
poetry run python -m api_gateway.main

# Windows
poetry run python -m api_gateway.main
```

### Run Web GUI

```bash
# macOS / Linux
poetry run streamlit run apps/web-gateway/src/main.py

# Windows
poetry run streamlit run apps/web-gateway/src/main.py
```

> **Note for Windows Users**: Ensure you have Python 3.11+ installed from [python.org](https://www.python.org/downloads/) with "Add Python to PATH" enabled. For best performance, use Python 64-bit version.

## Project Structure

```
cyberbullying_project/
├── apps/                      # Microservices
│   ├── api-gateway/          # Main entry point, routing
│   ├── web-gateway/          # Streamlit Web GUI
│   ├── preprocessing-service # Text cleaning, normalization
│   ├── feature-service       # Embeddings, feature extraction
│   ├── training-service      # Model training pipeline
│   ├── prediction-service    # Inference, prediction
│   ├── explainability-service # XAI visualizations
│   ├── model-registry        # Model versioning
│   └── monitoring-service    # Metrics, health checks
├── packages/                  # Shared libraries
│   ├── shared-common         # Utilities, decorators, logging
│   ├── ml-core               # ML models, evaluation
│   └── data-models           # Pydantic schemas
└── docs/                      # Documentation
```

## Key Features

- **Multi-model Support**: BERT, RoBERTa, DeBERTa, LSTM, GRU, BiLSTM
- **Ensemble Methods**: Combine multiple models for robust predictions
- **Feature Extraction**: Statistical, social, and linguistic features
- **Batch Processing**: Process multiple texts efficiently
- **UUID Tracking**: Unique identifiers for all entities
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **Interactive Web GUI**: Browser-based interface for real-time predictions

## Web GUI

The Web GUI provides an interactive interface for cyberbullying detection:

```bash
# Run the Web GUI
poetry run streamlit run apps/web-gateway/src/main.py
```

Access at: `http://localhost:8501`

Features:
- Real-time text input for instant predictions
- Confidence scores and prediction breakdown
- Batch prediction support
- Model selection (choose different models)
- Historical prediction results

## Test Results

All feature extraction tests passed:

- Single text extraction ✓
- Batch extraction ✓
- Social features (mentions, URLs, hashtags) ✓
- Statistical features (word count, char count, etc.) ✓
- Linguistic features (lexical diversity, sentiment) ✓

## Documentation

- [Architecture](ARCHITECTURE.md) — System architecture and design
- [API Reference](API.md) — Endpoints and schemas
- [Development Guide](DEVELOPMENT.md) — Setup and contribution

## License

MIT
