# =============================================================================
# EVALUATION METRICS
# =============================================================================
# Purpose: Metrics for evaluating classification models.
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
from typing import Any, Dict, List, Optional, Tuple  # Type hints

import numpy as np  # Numerical computing
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    roc_auc_score,
)  # Scikit-learn metrics
import torch  # PyTorch


# =============================================================================
# COMPUTE METRICS
# =============================================================================

def compute_metrics(
    predictions: np.ndarray,
    labels: np.ndarray,
    average: str = "weighted",
    num_labels: int = 2,
) -> Dict[str, float]:
    """
    Compute comprehensive evaluation metrics.
    
    Args:
        predictions: Predicted class indices
        labels: Ground truth labels
        average: Averaging method (binary, micro, macro, weighted)
        num_labels: Number of classes
    
    Returns:
        Dictionary of metric names and values
    """
    # Compute basic metrics
    metrics = {}
    
    # Accuracy
    metrics["accuracy"] = compute_accuracy(predictions, labels)
    
    # Precision, Recall, F1
    precision, recall, f1, _ = compute_precision_recall_f1(
        predictions, labels, average=average
    )
    
    metrics["precision"] = precision
    metrics["recall"] = recall
    metrics["f1"] = f1
    
    # Per-class metrics
    precision_per_class, recall_per_class, f1_per_class, _ = (
        precision_recall_fscore_support(
            labels,
            predictions,
            average=None,
            labels=range(num_labels),
        )
    )
    
    metrics["precision_per_class"] = precision_per_class.tolist()
    metrics["recall_per_class"] = recall_per_class.tolist()
    metrics["f1_per_class"] = f1_per_class.tolist()
    
    # Confusion matrix
    metrics["confusion_matrix"] = compute_confusion_matrix(
        predictions, labels, num_labels
    ).tolist()
    
    return metrics


def compute_accuracy(predictions: np.ndarray, labels: np.ndarray) -> float:
    """
    Compute accuracy score.
    
    Args:
        predictions: Predicted labels
        labels: Ground truth labels
    
    Returns:
        Accuracy score
    """
    return float(accuracy_score(labels, predictions))


def compute_precision(
    predictions: np.ndarray,
    labels: np.ndarray,
    average: str = "weighted",
) -> float:
    """
    Compute precision score.
    
    Args:
        predictions: Predicted labels
        labels: Ground truth labels
        average: Averaging method
    
    Returns:
        Precision score
    """
    precision, _, _, _ = precision_recall_fscore_support(
        labels, predictions, average=average, zero_division=0
    )
    return float(precision)


def compute_recall(
    predictions: np.ndarray,
    labels: np.ndarray,
    average: str = "weighted",
) -> float:
    """
    Compute recall score.
    
    Args:
        predictions: Predicted labels
        labels: Ground truth labels
        average: Averaging method
    
    Returns:
        Recall score
    """
    _, recall, _, _ = precision_recall_fscore_support(
        labels, predictions, average=average, zero_division=0
    )
    return float(recall)


def compute_f1(
    predictions: np.ndarray,
    labels: np.ndarray,
    average: str = "weighted",
) -> float:
    """
    Compute F1 score.
    
    Args:
        predictions: Predicted labels
        labels: Ground truth labels
        average: Averaging method
    
    Returns:
        F1 score
    """
    _, _, f1, _ = precision_recall_fscore_support(
        labels, predictions, average=average, zero_division=0
    )
    return float(f1)


def compute_precision_recall_f1(
    predictions: np.ndarray,
    labels: np.ndarray,
    average: str = "weighted",
) -> Tuple[float, float, float, np.ndarray]:
    """
    Compute precision, recall, and F1 together.
    
    Args:
        predictions: Predicted labels
        labels: Ground truth labels
        average: Averaging method
    
    Returns:
        Tuple of (precision, recall, f1, support)
    """
    precision, recall, f1, support = precision_recall_fscore_support(
        labels, predictions, average=average, zero_division=0
    )
    
    return float(precision), float(recall), float(f1), support


def compute_confusion_matrix(
    predictions: np.ndarray,
    labels: np.ndarray,
    num_labels: int,
) -> np.ndarray:
    """
    Compute confusion matrix.
    
    Args:
        predictions: Predicted labels
        labels: Ground truth labels
        num_labels: Number of classes
    
    Returns:
        Confusion matrix (num_labels x num_labels)
    """
    return confusion_matrix(labels, predictions, labels=range(num_labels))


def compute_roc_auc(
    predictions: np.ndarray,
    labels: np.ndarray,
    probabilities: Optional[np.ndarray] = None,
    average: str = "weighted",
) -> float:
    """
    Compute ROC AUC score.
    
    Args:
        predictions: Predicted labels
        labels: Ground truth labels
        probabilities: Predicted probabilities (if None, uses predictions)
        average: Averaging method
    
    Returns:
        ROC AUC score
    """
    if probabilities is None:
        # Convert predictions to one-hot
        num_classes = len(np.unique(labels))
        probabilities = np.eye(num_classes)[predictions]
    
    # Compute AUC
    try:
        return float(roc_auc_score(labels, probabilities, average=average, multi_class="ovr"))
    except ValueError:
        # Handle edge case
        return 0.0


# =============================================================================
# PYTORCH METRICS
# =============================================================================

def compute_metrics_from_tensors(
    predictions: torch.Tensor,
    labels: torch.Tensor,
    num_labels: int = 2,
) -> Dict[str, float]:
    """
    Compute metrics from PyTorch tensors.
    
    Args:
        predictions: Predicted tensor
        labels: Ground truth tensor
        num_labels: Number of classes
    
    Returns:
        Dictionary of metrics
    """
    # Convert to numpy
    pred_np = predictions.cpu().numpy()
    labels_np = labels.cpu().numpy()
    
    # Compute metrics
    return compute_metrics(pred_np, labels_np, num_labels=num_labels)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "compute_metrics",
    "compute_accuracy",
    "compute_precision",
    "compute_recall",
    "compute_f1",
    "compute_precision_recall_f1",
    "compute_confusion_matrix",
    "compute_roc_auc",
    "compute_metrics_from_tensors",
]
