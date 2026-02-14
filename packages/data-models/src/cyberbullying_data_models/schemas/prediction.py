# =============================================================================
# PREDICTION SCHEMAS
# =============================================================================
# Purpose: Pydantic schemas for prediction results and model outputs.
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

from datetime import datetime  # Datetime handling
from enum import Enum  # Enum support
from typing import Any, Dict, List, Optional  # Type hints

from pydantic import (
    BaseModel,  # Base Pydantic model
    ConfigDict,  # Model configuration
    Field,  # Field configuration
)


# =============================================================================
# CONFIDENCE INTERVAL
# =============================================================================

class ConfidenceInterval(BaseModel):
    """
    Statistical confidence interval for predictions.
    
    Provides upper and lower bounds at a given confidence level.
    """
    
    # Lower bound
    lower: float = Field(..., ge=0, le=1, description="Lower bound")
    
    # Upper bound
    upper: float = Field(..., ge=0, le=1, description="Upper bound")
    
    # Confidence level
    level: float = Field(default=0.95, ge=0, le=1, description="Confidence level")


# =============================================================================
# PREDICTION RESULT
# =============================================================================

class PredictionResult(BaseModel):
    """
    Single prediction result from the model.
    
    This is the primary output for real-time predictions.
    Contains predicted class, confidence, and supporting information.
    """
    
    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "text_id": "550e8400-e29b-41d4-a716-446655440000",
                "predicted_label": "not_bullying",
                "confidence": 0.95,
                "probabilities": {
                    "bullying": 0.02,
                    "not_bullying": 0.95,
                    "harassment": 0.01,
                },
                "model_version": "1.0.0",
                "model_architecture": "bert-base",
            }
        },
    )
    
    # Text identifier
    text_id: str = Field(..., description="Text ID")
    
    # Predicted classification label
    predicted_label: str = Field(..., description="Predicted classification")
    
    # Confidence score (0-1)
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    
    # Probability distribution over all labels
    probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution over labels",
    )
    
    # Whether prediction meets confidence threshold
    is_high_confidence: bool = Field(
        ...,
        description="Whether prediction meets confidence threshold",
    )
    
    # Confidence threshold used
    confidence_threshold: float = Field(
        default=0.5,
        ge=0,
        le=1,
        description="Confidence threshold used",
    )
    
    # Model version
    model_version: str = Field(..., description="Model version")
    
    # Model architecture
    model_architecture: str = Field(..., description="Model architecture")
    
    # Prediction timestamp
    predicted_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When prediction was made",
    )
    
    # Inference time
    inference_time_ms: Optional[float] = Field(
        default=None,
        description="Inference time in milliseconds",
    )
    
    # Confidence interval
    confidence_interval: Optional[ConfidenceInterval] = Field(
        default=None,
        description="Confidence interval",
    )
    
    # Additional metadata
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata",
    )


# =============================================================================
# BATCH PREDICTION RESULT
# =============================================================================

class BatchPredictionResult(BaseModel):
    """
    Batch prediction results for multiple texts.
    
    Optimized schema for bulk processing.
    """
    
    # Batch identifier
    batch_id: str = Field(..., description="Batch ID")
    
    # Individual predictions
    predictions: List[PredictionResult] = Field(
        ...,
        description="Individual prediction results",
    )
    
    # Total processed
    total_processed: int = Field(..., description="Total texts processed")
    
    # Failed count
    failed_count: int = Field(default=0, description="Number of failures")
    
    # Errors
    errors: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Error details",
    )
    
    # Batch statistics
    batch_stats: Dict[str, float] = Field(
        ...,
        description="Batch processing statistics",
    )
    
    # Start timestamp
    started_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Batch start time",
    )
    
    # Completion timestamp
    completed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Batch completion time",
    )


# =============================================================================
# TOKEN IMPORTANCE
# =============================================================================

class TokenImportance(BaseModel):
    """
    Importance score for a single token.
    
    Used in text explanations.
    """
    
    # Token text
    token: str = Field(..., description="Token text")
    
    # Importance score
    importance: float = Field(..., description="Importance score")
    
    # Position in text
    position: int = Field(..., description="Token position")


# =============================================================================
# HIGHLIGHTED SEGMENT
# =============================================================================

class HighlightedSegment(BaseModel):
    """
    Text segment identified as contributing to prediction.
    
    Used for highlighting toxic parts of text.
    """
    
    # Segment text
    text: str = Field(..., description="Segment text")
    
    # Start position
    start_position: int = Field(..., description="Start position")
    
    # End position
    end_position: int = Field(..., description="End position")
    
    # Importance
    importance: float = Field(..., description="Importance score")
    
    # Reason
    reason: Optional[str] = Field(default=None, description="Explanation")


# =============================================================================
# PREDICTION EXPLANATION
# =============================================================================

class PredictionExplanation(BaseModel):
    """
    Explainable AI output for model interpretability.
    
    Contains feature importance, attention weights, and explanations.
    """
    
    # Prediction ID
    prediction_id: str = Field(..., description="Prediction ID")
    
    # Text ID
    text_id: str = Field(..., description="Text ID")
    
    # Explanation method
    explanation_method: str = Field(
        ...,
        description="Method used (shap, lime, attention)",
    )
    
    # Feature importance
    feature_importance: Dict[str, float] = Field(
        default_factory=dict,
        description="Feature importance scores",
    )
    
    # Token importance
    token_importance: Optional[List[TokenImportance]] = Field(
        default=None,
        description="Token-level importance",
    )
    
    # Attention weights
    attention_weights: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Attention weights",
    )
    
    # Highlighted segments
    highlighted_segments: Optional[List[HighlightedSegment]] = Field(
        default=None,
        description="Text segments to highlight",
    )
    
    # Natural language explanation
    text_explanation: Optional[str] = Field(
        default=None,
        description="Natural language explanation",
    )
    
    # Model version
    model_version: str = Field(..., description="Model version")
    
    # Generation timestamp
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When explanation was generated",
    )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "ConfidenceInterval",
    "PredictionResult",
    "BatchPredictionResult",
    "TokenImportance",
    "HighlightedSegment",
    "PredictionExplanation",
]
