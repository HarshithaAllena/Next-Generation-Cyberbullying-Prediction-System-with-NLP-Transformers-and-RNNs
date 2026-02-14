# =============================================================================
# TRAINING SCHEMAS
# =============================================================================
# Purpose: Pydantic schemas for model training configuration and results.
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

from datetime import datetime  # Datetime handling
from typing import Any, Dict, List, Optional  # Type hints

from pydantic import (
    BaseModel,  # Base Pydantic model
    Field,  # Field configuration
)


# =============================================================================
# TRAINING CONFIGURATION
# =============================================================================

class TrainingConfig(BaseModel):
    """
    Configuration for model training.
    
    Contains all hyperparameters and training options.
    """
    
    # Run ID
    run_id: Optional[str] = Field(default=None, description="Training run ID")
    
    # Experiment name
    experiment_name: str = Field(..., description="Experiment name")
    
    # Model architecture
    model_architecture: str = Field(
        ...,
        description="Model architecture (bert-base, roberta, lstm, etc.)",
    )
    
    # Learning rate
    learning_rate: float = Field(
        default=0.001,
        ge=0,
        description="Learning rate",
    )
    
    # Batch size
    batch_size: int = Field(
        default=32,
        ge=1,
        description="Batch size",
    )
    
    # Epochs
    epochs: int = Field(
        default=10,
        ge=1,
        description="Number of epochs",
    )
    
    # Max sequence length
    max_seq_length: int = Field(
        default=128,
        ge=1,
        description="Maximum sequence length",
    )
    
    # Optimizer
    optimizer: str = Field(default="adamw", description="Optimizer")
    
    # Scheduler
    scheduler: str = Field(default="linear", description="Learning rate scheduler")
    
    # Warmup steps
    warmup_steps: int = Field(default=0, ge=0, description="Warmup steps")
    
    # Weight decay
    weight_decay: float = Field(default=0.01, ge=0, description="Weight decay")
    
    # Dropout rate
    dropout_rate: float = Field(
        default=0.1,
        ge=0,
        le=1,
        description="Dropout rate",
    )
    
    # Early stopping patience
    early_stopping_patience: int = Field(
        default=3,
        ge=0,
        description="Early stopping patience",
    )
    
    # Gradient clip norm
    gradient_clip_norm: Optional[float] = Field(
        default=None,
        ge=0,
        description="Gradient clipping threshold",
    )
    
    # Use mixed precision
    use_amp: bool = Field(default=False, description="Use automatic mixed precision")
    
    # Data paths
    data_paths: Dict[str, str] = Field(
        ...,
        description="Data file paths",
    )
    
    # Output directory
    output_dir: str = Field(..., description="Output directory")
    
    # Random seed
    seed: int = Field(default=42, description="Random seed")
    
    # Num workers
    num_workers: int = Field(default=4, ge=0, description="Data loader workers")


# =============================================================================
# TRAINING METRICS
# =============================================================================

class TrainingMetrics(BaseModel):
    """
    Metrics collected during training.
    
    Tracks loss, accuracy, and custom metrics per epoch.
    """
    
    # Run ID
    run_id: str = Field(..., description="Training run ID")
    
    # Epoch number
    epoch: int = Field(..., ge=1, description="Epoch number")
    
    # Training loss
    train_loss: float = Field(..., description="Training loss")
    
    # Training accuracy
    train_accuracy: float = Field(..., description="Training accuracy")
    
    # Validation loss
    val_loss: Optional[float] = Field(default=None, description="Validation loss")
    
    # Validation accuracy
    val_accuracy: Optional[float] = Field(default=None, description="Validation accuracy")
    
    # Learning rate
    learning_rate: float = Field(..., description="Learning rate")
    
    # Epoch duration
    epoch_duration_seconds: float = Field(..., description="Epoch duration")
    
    # Custom metrics
    custom_metrics: Optional[Dict[str, float]] = Field(
        default=None,
        description="Custom metrics",
    )
    
    # Timestamp
    recorded_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Recording timestamp",
    )


# =============================================================================
# EVALUATION RESULT
# =============================================================================

class PerClassMetrics(BaseModel):
    """Metrics for a single class."""
    
    precision: float  # Precision score
    recall: float  # Recall score
    f1_score: float  # F1 score
    support: int  # Number of samples


class EvaluationResult(BaseModel):
    """
    Comprehensive model evaluation results.
    
    Contains precision, recall, F1, and other metrics.
    """
    
    # Evaluation ID
    evaluation_id: str = Field(..., description="Evaluation ID")
    
    # Model version
    model_version: str = Field(..., description="Model version")
    
    # Dataset name
    dataset_name: str = Field(..., description="Dataset name")
    
    # Sample count
    sample_count: int = Field(..., ge=1, description="Sample count")
    
    # Overall accuracy
    accuracy: float = Field(..., description="Overall accuracy")
    
    # Per-class metrics
    per_class_metrics: Dict[str, PerClassMetrics] = Field(
        ...,
        description="Per-class metrics",
    )
    
    # Macro metrics
    macro_metrics: Dict[str, float] = Field(..., description="Macro-averaged metrics")
    
    # Weighted metrics
    weighted_metrics: Dict[str, float] = Field(..., description="Weighted metrics")
    
    # Confusion matrix
    confusion_matrix: List[List[int]] = Field(..., description="Confusion matrix")
    
    # Inference stats
    inference_stats: Dict[str, float] = Field(..., description="Inference statistics")
    
    # Evaluation timestamp
    evaluated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Evaluation timestamp",
    )


# =============================================================================
# MODEL CHECKPOINT
# =============================================================================

class ModelCheckpoint(BaseModel):
    """
    Saved model state during training.
    
    Contains model weights, optimizer state, and metadata.
    """
    
    # Checkpoint ID
    checkpoint_id: str = Field(..., description="Checkpoint ID")
    
    # Run ID
    run_id: str = Field(..., description="Training run ID")
    
    # Epoch
    epoch: int = Field(..., description="Epoch number")
    
    # Global step
    global_step: int = Field(..., description="Global step")
    
    # Checkpoint path
    checkpoint_path: str = Field(..., description="Checkpoint path")
    
    # Training config
    training_config: TrainingConfig = Field(..., description="Training config")
    
    # Metrics
    metrics: Dict[str, Any] = Field(..., description="Metrics")
    
    # File size
    file_size_bytes: int = Field(..., description="File size in bytes")
    
    # Is best
    is_best: bool = Field(default=False, description="Is best checkpoint")
    
    # Is latest
    is_latest: bool = Field(default=False, description="Is latest checkpoint")
    
    # Saved timestamp
    saved_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Save timestamp",
    )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "TrainingConfig",
    "TrainingMetrics",
    "EvaluationResult",
    "PerClassMetrics",
    "ModelCheckpoint",
]
