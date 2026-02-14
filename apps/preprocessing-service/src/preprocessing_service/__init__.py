# =============================================================================
# PREPROCESSING SERVICE - __init__.py
# =============================================================================
# Purpose: Text preprocessing microservice for cleaning and normalization.
#
# This service provides:
# - Text cleaning (removing URLs, emails, special characters)
# - Tokenization
# - Text normalization (lowercasing, stemming)
# - Language detection
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

"""
Cyberbullying NLP - Preprocessing Service

This service handles text preprocessing for the cyberbullying detection pipeline.
It cleans, normalizes, and prepares text for feature extraction.

Example Usage:
    from preprocessing_service import TextPreprocessor
    
    preprocessor = TextPreprocessor()
    cleaned = preprocessor.clean_text("Check this out! http://example.com")
"""

__version__ = "1.0.0"

# Main exports
from preprocessing_service.preprocessor import TextPreprocessor
from preprocessing_service.cleaners import (
    URLCleaner,
    EmailCleaner,
    SpecialCharCleaner,
)
from preprocessing_service.tokenizers import SimpleTokenizer

__all__ = [
    "__version__",
    "TextPreprocessor",
    "URLCleaner",
    "EmailCleaner",
    "SpecialCharCleaner",
    "SimpleTokenizer",
]
