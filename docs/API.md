# API Reference

This document describes the API endpoints and data schemas for the Cyberbullying NLP Monorepo.

## Base URL

```
http://localhost:3000
```

## Endpoints

### Health Check

**GET** `/health`

Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "version": "1.0.0"
}
```

### Root

**GET** `/`

Get API information.

**Response:**
```json
{
  "message": "Cyberbullying Detection API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Classify Text

**POST** `/classify`

Classify text for cyberbullying detection.

**Request:**
```json
{
  "text": "Text to classify",
  "include_explanation": false
}
```

**Response:**
```json
{
  "text_id": "550e8400-e29b-41d4-a716-446655440000",
  "predicted_label": "not_bullying",
  "confidence": 0.95,
  "probabilities": {
    "bullying": 0.02,
    "not_bullying": 0.95,
    "harassment": 0.01,
    "hate_speech": 0.02
  },
  "is_high_confidence": true,
  "model_version": "1.0.0"
}
```

## Data Models

### ClassifyRequest

| Field | Type | Description |
|-------|------|-------------|
| text | string | Text to classify (required, min 1 character) |
| include_explanation | boolean | Include XAI explanation (default: false) |

### ClassifyResponse

| Field | Type | Description |
|-------|------|-------------|
| text_id | string | Unique text identifier (UUID) |
| predicted_label | string | Predicted classification label |
| confidence | float | Confidence score (0-1) |
| probabilities | object | Probability distribution over labels |
| is_high_confidence | boolean | Whether confidence exceeds threshold |
| model_version | string | Model version used |

### PredictionResult

| Field | Type | Description |
|-------|------|-------------|
| text_id | string | Text identifier |
| predicted_label | string | Classification result |
| confidence | float | Confidence score |
| probabilities | dict | Label probability distribution |
| is_high_confidence | bool | High confidence flag |
| confidence_threshold | float | Threshold used (default: 0.5) |
| model_version | string | Model version |
| model_architecture | string | Model architecture name |
| predicted_at | datetime | Prediction timestamp |
| inference_time_ms | float | Inference time in milliseconds |
| confidence_interval | object | Confidence interval (optional) |
| metadata | object | Additional metadata (optional) |

### TextFeatures

| Field | Type | Description |
|-------|------|-------------|
| features_id | string | Features identifier (UUID) |
| text_id | string | Text identifier |
| preprocessed_text | string | Cleaned text |
| statistical_features | object | Statistical feature set |
| social_features | object | Social media features |
| linguistic_features | object | Linguistic features |
| embedding | object | Embedding vector (optional) |
| extracted_at | datetime | Extraction timestamp |

### StatisticalFeatures

| Field | Type | Description |
|-------|------|-------------|
| character_count | int | Total characters |
| word_count | int | Total words |
| unique_word_count | int | Unique words |
| average_word_length | float | Average word length |
| sentence_count | int | Sentence count |
| average_sentence_length | float | Avg words per sentence |
| uppercase_count | int | Uppercase character count |
| uppercase_ratio | float | Uppercase ratio |
| exclamation_count | int | Exclamation marks |
| question_count | int | Question marks |
| repeated_char_count | int | Repeated characters |

### SocialFeatures

| Field | Type | Description |
|-------|------|-------------|
| mention_count | int | @mentions count |
| hashtag_count | int | #hashtags count |
| url_count | int | URLs count |
| emoji_count | int | Emoji count |
| unique_mention_count | int | Unique mentions |
| is_retweet | bool | Is retweet flag |
| has_media | bool | Has media attachment |

### LinguisticFeatures

| Field | Type | Description |
|-------|------|-------------|
| lexical_diversity | float | Unique words / total words |
| readability_score | float | Readability score (optional) |
| sentiment_polarity | float | -1 to 1 (optional) |
| sentiment_subjectivity | float | 0 to 1 (optional) |

### EmbeddingVector

| Field | Type | Description |
|-------|------|-------------|
| embedding_id | string | Embedding ID |
| text_id | string | Text ID |
| vector | list[float] | Dense vector |
| dimensions | int | Vector dimensions |
| model_name | string | Model name |
| pooling_method | string | Pooling method |
| normalized | bool | L2 normalized flag |
| generated_at | datetime | Generation timestamp |

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Text is required"
}
```

### 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "String should have at least 1 character",
      "type": "string_too_short"
    }
  ]
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

## Service Ports

| Service | Port |
|---------|------|
| API Gateway | 3000 |
| Preprocessing | 3001 |
| Feature | 3002 |
| Prediction | 3003 |
| Training | 3004 |

## Example Usage

### Python

```python
import requests

url = "http://localhost:3000/classify"
payload = {
    "text": "You are amazing!",
    "include_explanation": False
}

response = requests.post(url, json=payload)
print(response.json())
```

### cURL

```bash
curl -X POST http://localhost:3000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "You are amazing!", "include_explanation": false}'
```

### JavaScript

```javascript
const response = await fetch('http://localhost:3000/classify', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'You are amazing!',
    include_explanation: false
  })
});
const data = await response.json();
console.log(data);
```
