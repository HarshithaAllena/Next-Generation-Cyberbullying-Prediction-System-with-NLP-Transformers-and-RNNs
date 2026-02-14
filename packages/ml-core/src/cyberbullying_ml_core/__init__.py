# =============================================================================
# ML-CORE PACKAGE - __init__.py
# =============================================================================
# Purpose: Core machine learning utilities and model architectures for NLP.
#
# This package provides:
# - Neural network models (RNN, LSTM, GRU, Transformer, BERT)
# - Training utilities (optimizers, schedulers, callbacks)
# - Evaluation metrics (precision, recall, F1, etc.)
# - Data processing utilities
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

"""
Cyberbullying NLP - ML Core Package

This package provides core machine learning components for building,
training, and evaluating cyberbullying detection models.

Example Usage:
    from cyberbullying_ml_core import (
        CyberbullyingClassifier,
        BiLSTMModel,
        BertClassifier,
    )
    
    # Create model
    model = BertClassifier(num_labels=2)
"""

# =============================================================================
# VERSION
# =============================================================================
__version__ = "1.0.0"

# =============================================================================
# MODEL IMPORTS
# =============================================================================

# Neural network models
from cyberbullying_ml_core.models.rnn_models import (
    LSTMClassifier,
    GRUClassifier,
    BiLSTMClassifier,
    BiGRUClassifier,
)

from cyberbullying_ml_core.models.transformer_models import (
    BertClassifier,
    RoBERTaClassifier,
    DeBERTaClassifier,
    DistilBertClassifier,
)

from cyberbullying_ml_core.models.ensemble import (
    EnsembleClassifier,
    VotingClassifier,
)

from cyberbullying_ml_core.models.base import (
    BaseClassifier,
    ModelOutput,
)

# =============================================================================
# TRAINING IMPORTS
# =============================================================================

from cyberbullying_ml_core.training.optimizers import (
    get_optimizer,
    get_scheduler,
)

from cyberbullying_ml_core.training.losses import (
    get_loss_function,
    FocalLoss,
    LabelSmoothingLoss,
)

from cyberbullying_ml_core.training.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    LearningRateScheduler,
)

# =============================================================================
# EVALUATION IMPORTS
# =============================================================================

from cyberbullying_ml_core.evaluation.metrics import (
    compute_metrics,
    compute_precision,
    compute_recall,
    compute_f1,
    compute_accuracy,
    compute_confusion_matrix,
    compute_roc_auc,
)

# =============================================================================
# DATA PROCESSING IMPORTS
# =============================================================================

from cyberbullying_ml_core.data.tokenizer import (
    Tokenizer,
    get_tokenizer,
)

from cyberbullying_ml_core.data.dataset import (
    CyberbullyingDataset,
    TextClassificationDataset,
)

from cyberbullying_ml_core.data.collator import (
    DataCollator,
    DataCollatorForClassification,
)

# =============================================================================
# PUBLIC API
# =============================================================================

__all__ = [
    # Version
    "__version__",
    
    # Models - RNN
    "LSTMClassifier",
    "GRUClassifier",
    "BiLSTMClassifier",
    "BiGRUClassifier",
    
    # Models - Transformer
    "BertClassifier",
    "RoBERTaClassifier",
    "DeBERTaClassifier",
    "DistilBertClassifier",
    
    # Models - Ensemble
    "EnsembleClassifier",
    "VotingClassifier",
    
    # Models - Base
    "BaseClassifier",
    "ModelOutput",
    
    # Training - Optimizers
    "get_optimizer",
    "get_scheduler",
    
    # Training - Losses
    "get_loss_function",
    "FocalLoss",
    "LabelSmoothingLoss",
    
    # Training - Callbacks
    "EarlyStopping",
    "ModelCheckpoint",
    "LearningRateScheduler",
    
    # Evaluation
    "compute_metrics",
    "compute_precision",
    "compute_recall",
    "compute_f1",
    "compute_accuracy",
    "compute_confusion_matrix",
    "compute_roc_auc",
    
    # Data - Tokenizer
    "Tokenizer",
    "get_tokenizer",
    
    # Data - Dataset
    "CyberbullyingDataset",
    "TextClassificationDataset",
    
    # Data - Collator
    "DataCollator",
    "DataCollatorForClassification",
]
