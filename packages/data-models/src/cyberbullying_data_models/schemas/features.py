# =============================================================================
# FEATURES SCHEMAS
# =============================================================================
# Purpose: Pydantic schemas for feature extraction and embeddings.
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
# EMBEDDING VECTOR
# =============================================================================

class EmbeddingVector(BaseModel):
    """
    Dense vector representation of text.
    
    Used for similarity search and as ML model input.
    """
    
    # Embedding ID
    embedding_id: Optional[str] = Field(default=None, description="Embedding ID")
    
    # Text ID
    text_id: str = Field(..., description="Text ID")
    
    # Vector values
    vector: List[float] = Field(..., description="Embedding vector")
    
    # Dimensions
    dimensions: int = Field(..., description="Vector dimensions")
    
    # Model name
    model_name: str = Field(..., description="Embedding model name")
    
    # Pooling method
    pooling_method: str = Field(default="mean", description="Pooling method")
    
    # Normalized
    normalized: bool = Field(default=False, description="L2 normalized")
    
    # Timestamp
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Generation timestamp",
    )


# =============================================================================
# STATISTICAL FEATURES
# =============================================================================

class StatisticalFeatures(BaseModel):
    """Statistical features extracted from text."""
    
    # Character count
    character_count: int = Field(..., description="Character count")
    
    # Word count
    word_count: int = Field(..., description="Word count")
    
    # Unique word count
    unique_word_count: int = Field(..., description="Unique word count")
    
    # Average word length
    average_word_length: float = Field(..., description="Average word length")
    
    # Sentence count
    sentence_count: int = Field(..., description="Sentence count")
    
    # Average sentence length
    average_sentence_length: float = Field(..., description="Average sentence length")
    
    # Uppercase count
    uppercase_count: int = Field(default=0, description="Uppercase count")
    
    # Uppercase ratio
    uppercase_ratio: float = Field(default=0, description="Uppercase ratio")
    
    # Exclamation count
    exclamation_count: int = Field(default=0, description="Exclamation count")
    
    # Question count
    question_count: int = Field(default=0, description="Question count")
    
    # Repeated character count
    repeated_char_count: int = Field(default=0, description="Repeated char count")


# =============================================================================
# SOCIAL FEATURES
# =============================================================================

class SocialFeatures(BaseModel):
    """Social media specific features."""
    
    # Mention count
    mention_count: int = Field(default=0, description="Mention count")
    
    # Hashtag count
    hashtag_count: int = Field(default=0, description="Hashtag count")
    
    # URL count
    url_count: int = Field(default=0, description="URL count")
    
    # Emoji count
    emoji_count: int = Field(default=0, description="Emoji count")
    
    # Unique mention count
    unique_mention_count: int = Field(default=0, description="Unique mention count")
    
    # Is retweet
    is_retweet: bool = Field(default=False, description="Is retweet")
    
    # Has media
    has_media: bool = Field(default=False, description="Has media")


# =============================================================================
# LINGUISTIC FEATURES
# =============================================================================

class LinguisticFeatures(BaseModel):
    """Linguistic features from text analysis."""
    
    # Lexical diversity
    lexical_diversity: float = Field(..., description="Lexical diversity")
    
    # Readability score
    readability_score: Optional[float] = Field(
        default=None,
        description="Readability score",
    )
    
    # Sentiment polarity
    sentiment_polarity: Optional[float] = Field(
        default=None,
        description="Sentiment polarity (-1 to 1)",
    )
    
    # Sentiment subjectivity
    sentiment_subjectivity: Optional[float] = Field(
        default=None,
        description="Sentiment subjectivity (0 to 1)",
    )


# =============================================================================
# TEXT FEATURES
# =============================================================================

class TextFeatures(BaseModel):
    """
    Complete feature set extracted from text.
    
    Contains embeddings, statistical, social, and linguistic features.
    """
    
    # Features ID
    features_id: Optional[str] = Field(default=None, description="Features ID")
    
    # Text ID
    text_id: str = Field(..., description="Text ID")
    
    # Preprocessed text
    preprocessed_text: str = Field(..., description="Preprocessed text")
    
    # Statistical features
    statistical_features: StatisticalFeatures = Field(
        ...,
        description="Statistical features",
    )
    
    # Social features
    social_features: SocialFeatures = Field(
        ...,
        description="Social media features",
    )
    
    # Linguistic features
    linguistic_features: LinguisticFeatures = Field(
        ...,
        description="Linguistic features",
    )
    
    # Embedding
    embedding: Optional[EmbeddingVector] = Field(
        default=None,
        description="Embedding vector",
    )
    
    # Custom features
    custom_features: Optional[Dict[str, float]] = Field(
        default=None,
        description="Custom features",
    )
    
    # Extraction timestamp
    extracted_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Extraction timestamp",
    )


# =============================================================================
# FEATURE IMPORTANCE
# =============================================================================

class TopFeature(BaseModel):
    """Top feature information."""
    
    feature_name: str  # Feature name
    importance: float  # Importance score
    rank: int  # Rank


class FeatureImportance(BaseModel):
    """
    Feature importance analysis results.
    
    Used for model interpretability and feature selection.
    """
    
    # Importance ID
    importance_id: Optional[str] = Field(default=None, description="Importance ID")
    
    # Model version
    model_version: str = Field(..., description="Model version")
    
    # Feature importances
    feature_importances: Dict[str, float] = Field(
        ...,
        description="Feature importance scores",
    )
    
    # Top features
    top_features: List[TopFeature] = Field(..., description="Top features")
    
    # Analysis method
    analysis_method: str = Field(..., description="Analysis method")
    
    # Dataset name
    dataset_name: Optional[str] = Field(default=None, description="Dataset name")
    
    # Sample size
    sample_size: Optional[int] = Field(default=None, description="Sample size")
    
    # Analysis timestamp
    analyzed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Analysis timestamp",
    )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "EmbeddingVector",
    "StatisticalFeatures",
    "SocialFeatures",
    "LinguisticFeatures",
    "TextFeatures",
    "TopFeature",
    "FeatureImportance",
]
