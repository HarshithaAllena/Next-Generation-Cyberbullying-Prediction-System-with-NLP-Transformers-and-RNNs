# =============================================================================
# DATA MODELS PACKAGE - __init__.py
# =============================================================================
# Purpose: Pydantic schemas and data validation models for Cyberbullying NLP.

__version__ = "1.0.0"

# Text processing schemas
from cyberbullying_data_models.schemas.text import (
    RawTextInput,
    PreprocessedText,
    TextMetadata,
)

# Prediction schemas
from cyberbullying_data_models.schemas.prediction import (
    PredictionResult,
    BatchPredictionResult,
    PredictionExplanation,
    ConfidenceInterval,
)

# Training schemas
from cyberbullying_data_models.schemas.training import (
    TrainingConfig,
    TrainingMetrics,
    EvaluationResult,
    ModelCheckpoint,
)

# Feature schemas
from cyberbullying_data_models.schemas.features import (
    TextFeatures,
    EmbeddingVector,
    FeatureImportance,
)

__all__ = [
    "__version__",
    "RawTextInput",
    "PreprocessedText",
    "TextMetadata",
    "PredictionResult",
    "BatchPredictionResult",
    "PredictionExplanation",
    "ConfidenceInterval",
    "TrainingConfig",
    "TrainingMetrics",
    "EvaluationResult",
    "ModelCheckpoint",
    "TextFeatures",
    "EmbeddingVector",
    "FeatureImportance",
]
