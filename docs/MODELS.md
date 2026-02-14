# Model Documentation

## Overview

This document describes the machine learning models used in the Cyberbullying Detection System.

## Model Architecture Comparison

| Model | Type | Parameters | Size | Speed | Accuracy |
|-------|------|------------|------|-------|----------|
| DistilBERT | Transformer | 66M | 250MB | Fast | ~89% |
| BERT-base | Transformer | 110M | 400MB | Medium | ~92% |
| RoBERTa-base | Transformer | 125M | 480MB | Medium | ~93% |
| DeBERTa-v3 | Transformer | 86M | 350MB | Medium | ~94% |
| BiLSTM | RNN | 4M | 50MB | Fast | ~88% |
| GRU | RNN | 1M | 30MB | Very Fast | ~86% |

## Transformer Models

### BERT (Bidirectional Encoder Representations from Transformers)

**Architecture:**
- 12 encoder layers
- 12 attention heads
- 768 hidden dimensions
- 3072 feed-forward dimensions

**Strengths:**
- Excellent contextual understanding
- Pre-trained on large corpus
- Good for general NLP tasks

**Use Case:** 
- Default choice for most classification tasks

### RoBERTa (Robustly Optimized BERT)

**Key Differences from BERT:**
- Dynamic masking during training
- No Next Sentence Prediction (NSP)
- Larger batch sizes
- More training data

**Strengths:**
- Better than BERT on most benchmarks
- More robust training

**Use Case:**
- When slightly better accuracy is needed

### DeBERTa (Decoding-enhanced BERT)

**Key Innovations:**
- Disentangled attention mechanism
- Enhanced mask decoder
- 2021+ state-of-the-art

**Strengths:**
- Best single-model performance
- Better handling of long-range dependencies

**Use Case:**
- Best accuracy requirements
- Critical classification tasks

### DistilBERT

**Knowledge Distillation:**
- 40% smaller than BERT
- 60% faster
- 97% of BERT performance

**Strengths:**
- Fast inference
- Low memory usage
- Good for production

**Use Case:**
- Real-time applications
- Resource-constrained environments

## RNN Models

### BiLSTM (Bidirectional LSTM)

**Architecture:**
- 2 LSTM layers (forward + backward)
- 256 hidden dimensions
- Dropout: 0.3

**Strengths:**
- Captures sequential patterns
- Bidirectional context
- Lightweight

**Use Case:**
- When interpretability matters
- Quick prototyping

### GRU (Gated Recurrent Unit)

**Simplified compared to LSTM:**
- Fewer gates (2 vs 3)
- Faster training
- Less memory

**Strengths:**
- Very efficient
- Good for simple patterns

**Use Case:**
- Baseline comparisons
- Resource-limited scenarios

## Ensemble Model

Combining multiple models for better performance:

```
Ensemble = BERT + RoBERTa + DeBERTa + BiLSTM
```

**Expected Improvement:**
- +1-2% over best single model
- More robust predictions

## Training Configuration

### Hyperparameters

| Parameter | Transformer | RNN |
|-----------|-------------|-----|
| Learning Rate | 2e-5 | 1e-3 |
| Batch Size | 32 | 64 |
| Epochs | 10 | 20 |
| Max Length | 256 | 128 |
| Dropout | 0.1 | 0.3 |

### Optimizer

- **Transformers:** AdamW with weight decay 0.01
- **RNNs:** Adam with learning rate scheduling

### Loss Function

- Primary: CrossEntropyLoss
- Alternative: Focal Loss (for imbalanced data)

## Evaluation Metrics

### Primary Metrics

1. **Accuracy** - Overall correct predictions
2. **Precision** - True Positives / (TP + FP)
3. **Recall** - True Positives / (TP + FN)
4. **F1-Score** - Harmonic mean of precision/recall

### Additional Metrics

5. **ROC-AUC** - Area Under ROC Curve
6. **Confusion Matrix** - Detailed prediction analysis

## Model Selection Guide

### Choose DistilBERT if:
- Speed is critical
- Running on CPU
- Resource-constrained

### Choose BERT if:
- Balance of speed/accuracy
- General use case

### Choose DeBERTa if:
- Maximum accuracy needed
- Critical applications

### Choose BiLSTM if:
- Learning NLP fundamentals
- Interpretability needed
- Quick experimentation

### Choose Ensemble if:
- Best accuracy required
- Multiple model comparison available

## Loading Models

```python
from cyberbullying_ml_core.models import BertClassifier, BiLSTMClassifier

# Load BERT
model = BertClassifier(num_labels=4)

# Load BiLSTM
model = BiLSTMClassifier(vocab_size=30000, num_labels=4)
```

## Inference

```python
# Single prediction
result = model.predict(input_ids, attention_mask)

# Get probabilities
probs = model.predict_proba(input_ids, attention_mask)

# Get labels
labels = model.predict_labels(input_ids, attention_mask)
```

## Model Files

Models are stored in:
```
models/
├── bert-base-uncased/
├── roberta-base/
├── microsoft-deberta-v3-base/
└── checkpoints/
```

## Version History

| Version | Model | Date | Notes |
|---------|-------|------|-------|
| 1.0.0 | BERT | Initial | Base model |
| 1.1.0 | RoBERTa | Added | Better performance |
| 1.2.0 | DeBERTa | Added | State-of-the-art |
| 2.0.0 | Ensemble | Added | Combined models |

## References

- BERT: Devlin et al. (2019)
- RoBERTa: Liu et al. (2019)
- DeBERTa: He et al. (2021)
- LSTM: Hochreiter & Schmidhuber (1997)
