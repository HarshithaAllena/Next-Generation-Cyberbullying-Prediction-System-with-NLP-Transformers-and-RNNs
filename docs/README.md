# Cyberbullying Detection System

> Next-Generation NLP-Based Solution for Detecting Cyberbullying in Text

A production-ready microservices architecture for detecting cyberbullying using state-of-the-art NLP techniques including BERT, RoBERTa, DeBERTa, and RNN models (LSTM, GRU, BiLSTM).

---

## Features

- **Multi-Model Support**: BERT, RoBERTa, DeBERTa, DistilBERT, BiLSTM, GRU
- **Ensemble Methods**: Combine multiple models for robust predictions
- **Feature Extraction**: Statistical, social, and linguistic features
- **Interactive Web GUI**: Real-time predictions in your browser
- **REST API**: Programmatic access for developers
- **Microservices Architecture**: Scalable and maintainable

---

## Quick Start (5 minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/HarshithaAllena/Next-Generation-Cyberbullying-Prediction-System-with-NLP-Transformers-and-RNNs.git
cd Next-Generation-Cyberbullying-Prediction-System-with-NLP-Transformers-and-RNNs
```

### 2. Install Dependencies

```bash
# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

### 3. Run the Application

```bash
# Start API (Terminal 1)
poetry run python -m api_gateway.main

# Start Web GUI (Terminal 2)
poetry run streamlit run apps/web-gateway/src/main.py
```

### 4. Open in Browser

- **Web GUI**: http://localhost:8501
- **API**: http://localhost:3000

---

## Try It Out

### Sample API Request

```bash
curl -X POST http://localhost:3000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "You are amazing!", "include_explanation": false}'
```

### Response

```json
{
  "predicted_label": "not_bullying",
  "confidence": 0.95,
  "probabilities": {
    "bullying": 0.02,
    "not_bullying": 0.95,
    "harassment": 0.01,
    "hate_speech": 0.02
  }
}
```

---

## Project Structure

```
cyberbullying_project/
├── apps/                      # Microservices
│   ├── api-gateway/          # Main entry point
│   ├── preprocessing-service # Text cleaning
│   ├── feature-service       # Feature extraction
│   ├── training-service      # Model training
│   └── prediction-service    # Inference
├── packages/                  # Shared libraries
│   ├── shared-common         # Utilities
│   ├── ml-core              # ML models
│   └── data-models           # Schemas
├── web/                       # Web frontend
├── docs/                      # Documentation
└── notebooks/                # Research notebooks
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11+ |
| ML | PyTorch, Transformers |
| API | FastAPI |
| Web | Streamlit |
| Package Manager | Poetry |
| Containerization | Docker |

---

## Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](QUICKSTART.md) | Get started in 5 minutes |
| [API Reference](API.md) | API endpoints and usage |
| [Architecture](ARCHITECTURE.md) | System design |
| [Development Guide](DEVELOPMENT.md) | Setup and contribution |
| [Models](MODELS.md) | ML model documentation |
| [FAQ](FAQ.md) | Frequently asked questions |

---

## Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|-----------|
| BERT | ~92% | ~91% | ~90% | ~90% |
| RoBERTa | ~93% | ~92% | ~91% | ~91% |
| DeBERTa | ~94% | ~93% | ~92% | ~92% |
| BiLSTM | ~88% | ~87% | ~86% | ~86% |
| **Ensemble** | **~95%** | **~94%** | **~93%** | **~93%** |

---

## Classification Categories

| Category | Description |
|----------|-------------|
| not_bullying | Normal, non-offensive content |
| bullying | General cyberbullying |
| harassment | Repeated aggressive behavior |
| hate_speech | Content targeting groups |

---

## System Requirements

- Python 3.11+
- 8GB RAM (16GB recommended)
- 10GB disk space
- Internet (for downloading models)

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

---

## License

MIT License

---

## Support

- Open an issue on GitHub
- Check the FAQ
- Review documentation

---

**Note for Windows Users**: Ensure Python is added to PATH during installation. See [Quick Start Guide](QUICKSTART.md) for detailed Windows setup instructions.
