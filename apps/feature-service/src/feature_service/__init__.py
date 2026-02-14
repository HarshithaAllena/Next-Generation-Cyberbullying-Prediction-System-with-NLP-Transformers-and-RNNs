# =============================================================================
# FEATURE SERVICE - __init__.py
# =============================================================================
# Purpose: Feature extraction microservice for text embeddings and features.

__version__ = "1.0.0"

from feature_service.extractor import FeatureExtractor
from feature_service.embeddings import EmbeddingGenerator

__all__ = [
    "__version__",
    "FeatureExtractor",
    "EmbeddingGenerator",
]
