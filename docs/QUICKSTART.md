# Quick Start Guide

> Get up and running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- Poetry (Python package manager)
- Git

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/HarshithaAllena/Next-Generation-Cyberbullying-Prediction-System-with-NLP-Transformers-and-RNNs.git
cd Next-Generation-Cyberbullying-Prediction-System-with-NLP-Transformers-and-RNNs
```

### Step 2: Install Python

**Windows:**
```powershell
# Download from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH"
python --version
```

**macOS:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt-get install python3.11 python3-pip
```

### Step 3: Install Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# macOS / Linux
curl -sSL https://install.python-poetry.org | python3 -
```

### Step 4: Install Dependencies

```bash
poetry install
```

### Step 5: Activate Virtual Environment

```bash
poetry shell
```

## Running the Application

### Option 1: Run with Docker (Recommended)

```bash
docker-compose up
```

### Option 2: Run Services Manually

**Terminal 1 - API Gateway:**
```bash
poetry run python -m api_gateway.main
```

**Terminal 2 - Web GUI:**
```bash
poetry run streamlit run apps/web-gateway/src/main.py
```

## Access the Application

- **Web GUI:** http://localhost:8501
- **API:** http://localhost:3000
- **API Docs:** http://localhost:3000/docs

## Quick Test

### Using the Web Interface

1. Open http://localhost:8501
2. Enter text in the input box
3. Click "Analyze"
4. View the prediction result

### Using the API

```bash
curl -X POST http://localhost:3000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "You are amazing!", "include_explanation": false}'
```

Expected Response:
```json
{
  "predicted_label": "not_bullying",
  "confidence": 0.95,
  "probabilities": {
    "bullying": 0.02,
    "not_bullying": 0.95
  }
}
```

## Sample Texts to Try

| Text | Expected Result |
|------|-----------------|
| "You are amazing! Great work!" | not_bullying |
| "You are such an idiot!" | bullying |
| "I love spending time with you!" | not_bullying |
| "You should kill yourself!" | hate_speech |

## Next Steps

- Read the API Documentation
- Learn about System Architecture
- Check out Development Guide

## Troubleshooting

### Port Already in Use

```bash
# Windows - Find process using port
netstat -ano | Select-String ":3000"

# macOS/Linux
lsof -i :3000
```

### Poetry Not Found

```bash
# Add to PATH (Windows)
$env:PATH += ";$env:APPDATA\Python\Scripts"

# Or use
py -m poetry --version
```

### Import Errors

```bash
poetry install
```

## Support

For issues, please open a GitHub issue.
