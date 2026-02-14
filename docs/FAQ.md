# Frequently Asked Questions (FAQ)

## General Questions

### What is this project?

This is a Next-Generation Cyberbullying Detection System that uses NLP (Natural Language Processing) with Transformer models (BERT, RoBERTa, DeBERTa) and RNN models (LSTM, GRU) to detect and classify cyberbullying in text.

### What does it do?

The system analyzes text input and classifies it into categories:
- not_bullying - Normal, non-offensive content
- bullying - General cyberbullying
- harassment - Repeated aggressive behavior
- hate_speech - Content targeting groups based on characteristics

### Who is this for?

- Researchers studying NLP and machine learning
- Developers building content moderation systems
- Students working on final year projects
- Organizations needing automated moderation tools

## Technical Questions

### What programming languages are used?

- **Python** - Main language for ML/NLP
- **TypeScript** - Web frontend
- **Shell scripts** - Setup scripts

### What ML models are used?

| Model | Type | Parameters | Use Case |
|-------|------|------------|----------|
| BERT | Transformer | 110M | Text classification |
| RoBERTa | Transformer | 125M | Enhanced classification |
| DeBERTa | Transformer | 86M | State-of-the-art classification |
| DistilBERT | Transformer | 66M | Fast, lightweight |
| BiLSTM | RNN | 4M | Sequential patterns |
| GRU | RNN | 1M | Efficient classification |

### Do I need GPU?

- **For training:** Yes, GPU strongly recommended (CUDA)
- **For inference:** CPU works fine, GPU faster

### How accurate is it?

Expected accuracy:
- BERT: ~92%
- RoBERTa: ~93%
- DeBERTa: ~94%
- Ensemble: ~95%

## Installation Questions

### What are the system requirements?

- Python 3.11+
- 8GB RAM (16GB recommended)
- 10GB disk space for models
- Internet for downloading models

### Why is Poetry recommended?

Poetry manages all Python dependencies consistently across different operating systems and ensures version compatibility.

### Can I use pip instead of Poetry?

Yes, but Poetry is recommended:
```bash
pip install -r requirements.txt
```

## Usage Questions

### How do I use the API?

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:3000/classify",
    json={"text": "Your text here"}
)
print(response.json())
```

**cURL:**
```bash
curl -X POST http://localhost:3000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

### Can I train my own model?

Yes! Use the training-service:
```bash
poetry run python -m training_service.main
```

### Can I use my own dataset?

Yes. Place your CSV file in the data folder with columns:
- `text` - The text to classify
- `label` - The classification label

## Windows-Specific Questions

### Why do Windows paths sometimes fail?

Windows uses backslashes (`\`) while Python prefers forward slashes (`/`). Always use forward slashes in code.

### How do I enable long paths on Windows?
```bash
git config --global core.longpaths true
```

### Poetry not found on Windows?

Add to PATH:
```powershell
$env:PATH += ";$env:APPDATA\Python\Scripts"
```

## Troubleshooting

### "Module not found" errors

```bash
poetry install
```

### "Port already in use" error

```bash
# Find and kill the process
# Windows
netstat -ano | Select-String ":3000"
taskkill /PID <process_id> /F

# macOS/Linux
lsof -i :3000
kill -9 <process_id>
```

### Models not downloading

Check internet connection. Models download from Hugging Face:
- First run requires internet
- ~2-5GB download depending on models

### Out of memory errors

- Reduce batch size
- Use lighter models (DistilBERT instead of BERT)
- Use CPU-friendly models (BiLSTM)

## Contributing

### How can I contribute?

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

### What coding standards should I follow?

- Use type hints
- Follow PEP 8
- Add docstrings (Google style)
- Test new features

## License

MIT License - See LICENSE file for details.

## Support

- Open an issue on GitHub
- Check documentation
- Review existing issues
