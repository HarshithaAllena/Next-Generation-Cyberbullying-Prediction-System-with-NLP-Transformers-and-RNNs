# =============================================================================
# PREDICTION SERVICE - __init__.py
# =============================================================================

__version__ = "1.0.0"

from prediction_service.predictor import ModelPredictor

__all__ = ["__version__", "ModelPredictor"]
