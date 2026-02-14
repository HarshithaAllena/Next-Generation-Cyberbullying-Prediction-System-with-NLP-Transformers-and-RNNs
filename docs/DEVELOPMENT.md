# Development Guide

This guide covers setting up the development environment and contributing to the Cyberbullying NLP Monorepo.

## Prerequisites

- Python 3.11+
- Poetry (package manager)
- Git

### Windows Setup

This project runs on Windows with some platform-specific considerations.

#### Python Installation

1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Choose "Install launcher for all users"
4. Select "Create desktop shortcut" (optional)
5. Verify installation:
   ```powershell
   python --version
   ```

#### Poetry Installation (Windows)

```powershell
# Using PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Or via pip
pip install poetry

# Add Poetry to PATH if needed
$env:PATH += ";$env:APPDATA\Python\Scripts"
```

#### Verify Poetry Works

```powershell
poetry --version
```

#### Windows-Specific Environment Setup

```powershell
# Set environment variables (PowerShell)
$env:PYTHONPATH = "$PWD"

# Or use set for Command Prompt
set PYTHONPATH=%CD%

# For persistent environment variables
[System.Environment]::SetEnvironmentVariable("PYTHONPATH", "$PWD", "User")
```

#### Running Commands on Windows

All `poetry run` commands work identically on Windows:

```powershell
poetry install
poetry run pytest
poetry run python -m api_gateway.main
```

#### Port Checking on Windows

```powershell
# Check what's using a port (PowerShell)
netstat -ano | Select-String ":3000"

# Or use Resource Monitor (GUI)
# Press Win+R, type "resmon", go to Network tab
```

#### Windows-Specific Issues

| Issue | Solution |
|-------|----------|
| Long paths not supported | Enable: `git config --global core.longpaths true` |
| Execution policy blocked | Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Poetry not found | Add Poetry to PATH or use: `py -m poetry` |
| Unicode errors | Set console encoding: `chcp 65001` |

#### Recommended Windows Tools

- **Terminal**: [Windows Terminal](https://aka.ms/terminal) (modern terminal with tabs)
- **Editor**: [VS Code](https://code.visualstudio.com/) with Python extension
- **Shell**: PowerShell 7+ or Windows Terminal

#### Quick Windows Setup Script

Run this in PowerShell to set up the environment:

```powershell
# Install Python if needed
winget install Python.Python.3.11

# Install Poetry
pip install poetry

# Clone and setup project
git clone <repository-url>
cd cyberbullying_project
poetry install
poetry shell
```

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cyberbullying_project
```

### 2. Install Poetry

```bash
# macOS / Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### 3. Install Dependencies

```bash
poetry install
```

This installs all packages defined in the workspace:
- Apps (microservices)
- Packages (shared libraries)
- Dev dependencies (testing, linting)

### 4. Activate Virtual Environment

```bash
poetry shell
```

## Running Services

### Individual Services

Each service can be run independently:

```bash
# API Gateway (port 3000)
poetry run python -m api_gateway.main

# Web GUI (port 8501)
poetry run streamlit run apps/web-gateway/src/main.py

# Preprocessing Service (port 3001)
poetry run python -m preprocessing_service.main

# Feature Service (port 3002)
poetry run python -m feature_service.main

# Prediction Service (port 3003)
poetry run python -m prediction_service.main
```

### Running the Web GUI

The Web GUI provides an interactive browser-based interface:

```bash
# Run the Web GUI
poetry run streamlit run apps/web-gateway/src/main.py
```

Access at: `http://localhost:8501`

**Prerequisites**: Ensure the Prediction Service is running (port 3003) or configure the Web GUI to point to your API Gateway.

**Configuration**: Set the API endpoint in the Web GUI or via environment variable:

```bash
# macOS / Linux
export PREDICTION_API_URL=http://localhost:3003
poetry run streamlit run apps/web-gateway/src/main.py

# Windows (PowerShell)
$env:PREDICTION_API_URL="http://localhost:3003"
poetry run streamlit run apps/web-gateway/src/main.py
```

### Using Docker

```bash
# Build all services
docker-compose build

# Run all services
docker-compose up
```

## Development Commands

### Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=packages --cov=apps

# Run specific test file
poetry run pytest tests/test_extractor.py

# Run with verbose output
poetry run pytest -v
```

### Code Quality

```bash
# Format code (Black)
poetry run black .

# Sort imports (isort)
poetry run isort .

# Lint code (Flake8)
poetry run flake8 .

# Type checking (Mypy)
poetry run mypy packages apps
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
poetry run pre-commit install
```

This runs checks before each commit:
- Black formatting
- isort import sorting
- Flake8 linting
- Mypy type checking

## Project Structure

```
cyberbullying_project/
├── apps/                      # Microservices
│   ├── api-gateway/
│   │   ├── pyproject.toml
│   │   └── src/
│   ├── web-gateway/          # Streamlit Web GUI
│   ├── preprocessing-service/
│   ├── feature-service/
│   ├── training-service/
│   └── prediction-service/
├── packages/                  # Shared packages
│   ├── shared-common/
│   │   └── src/
│   ├── ml-core/
│   │   └── src/
│   └── data-models/
│       └── src/
├── tests/                     # Test files
├── docs/                      # Documentation
├── pyproject.toml            # Root config
└── poetry.lock               # Locked dependencies
```

## Package Management

### Adding a Dependency

```bash
# Add to root
poetry add <package>

# Add to specific app
poetry add <package> --project apps/api-gateway

# Add dev dependency
poetry add --group-dev <package>
```

### Updating Dependencies

```bash
# Update all
poetry update

# Update specific package
poetry update <package>
```

## Testing Guidelines

### Writing Tests

Tests should be in `tests/` directory:

```python
# tests/test_extractor.py
import pytest
from feature_service.extractor import FeatureExtractor

def test_extract_statistical_features():
    extractor = FeatureExtractor()
    result = extractor.extract("Hello world")
    
    assert result.statistical_features["word_count"] == 2
    assert result.statistical_features["character_count"] == 11
```

### Test Fixtures

Use pytest fixtures for common setup:

```python
@pytest.fixture
def sample_text():
    return "This is a sample text for testing"
```

## Code Style

### Formatting

- Line length: 100 characters
- Use Black for formatting
- Use isort for imports

### Type Hints

Use type hints throughout:

```python
def process_text(text: str) -> dict[str, float]:
    """Process text and return features."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def function(param: str) -> bool:
    """Short summary.

    Longer description if needed.

    Args:
        param: Description of parameter.

    Returns:
        Description of return value.

    Example:
        >>> function("test")
        True
    """
```

## Common Tasks

### Create a New Service

1. Create directory: `apps/new-service/`
2. Add `pyproject.toml` with service config
3. Add src structure
4. Register in workspace (root pyproject.toml)

### Add a New Model

1. Add to `packages/ml-core/src/cyberbullying_ml_core/models/`
2. Extend BaseClassifier
3. Add tests
4. Update documentation

### Update Configuration

Edit `packages/shared-common/src/cyberbullying_shared_common/config.py`:

```python
class Settings(BaseSettings):
    new_setting: str = Field(default="default_value")
```

## Troubleshooting

### Poetry Lock Issues

```bash
# Remove lock file and recreate
rm poetry.lock
poetry lock
poetry install
```

### Import Errors

Ensure packages are installed:
```bash
poetry install
```

### Port Already in Use

Check what's using the port:

```bash
# macOS / Linux
lsof -i :3000

# Windows (PowerShell)
netstat -ano | Select-String ":3000"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests and code quality checks
5. Submit a pull request

## Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
