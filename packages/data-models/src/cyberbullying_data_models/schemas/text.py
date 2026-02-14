# =============================================================================
# TEXT SCHEMAS
# =============================================================================
# Purpose: Pydantic schemas for text processing domain.
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
from datetime import datetime  # Datetime handling
from enum import Enum  # Enum support
from typing import Any, Dict, List, Optional  # Type hints

from pydantic import (
    BaseModel,  # Base Pydantic model
    ConfigDict,  # Model configuration
    Field,  # Field configuration
    field_validator,  # Custom validation
)


# =============================================================================
# CLASSIFICATION LABEL ENUM
# =============================================================================

class ClassificationLabel(str, Enum):
    """
    Classification labels for cyberbullying detection.
    
    These are the possible output classes when classifying text:
    - bullying: Contains bullying behavior
    - not_bullying: Does not contain bullying
    - harassment: Specific harassment content
    - hate_speech: Contains hate speech
    - aggression: Aggressive language
    - attack: Personal attacks
    - spam: Spam content
    - none: No detectable issue
    """
    
    # Positive cases - content contains issues
    BULLYING = "bullying"
    HARASSMENT = "harassment"
    HATE_SPEECH = "hate_speech"
    AGGRESSION = "aggression"
    ATTACK = "attack"
    SPAM = "spam"
    
    # Negative case - no issues detected
    NOT_BULLYING = "not_bullying"
    NONE = "none"


# =============================================================================
# RAW TEXT INPUT
# =============================================================================

class RawTextInput(BaseModel):
    """
    Raw text input from users or external sources.
    
    This is the entry point for all text data in the system.
    It validates incoming text before processing.
    
    Attributes:
        text: The actual text content to process (required)
        id: Unique identifier for tracking (optional, auto-generated)
        source: Origin of the text (twitter, youtube, api, etc.)
        timestamp: When text was collected (defaults to now)
        metadata: Additional context about the text
    
    Example:
        >>> text = RawTextInput(
        ...     text="Hello, this is a test message",
        ...     source="api"
        ... )
        >>> text.text
        'Hello, this is a test message'
    """
    
    # Pydantic configuration
    model_config = ConfigDict(
        # Use enum values (strings) instead of enum objects
        use_enum_values=True,
        # Validate assignment - catch extra fields
        validate_assignment=True,
        # Generate JSON schema
        json_schema_extra={
            "example": {
                "text": "Sample text to classify",
                "source": "twitter",
            }
        },
    )
    
    # Text content - the main input
    text: str = Field(
        ...,
        description="The text content to process",
        min_length=1,  # Cannot be empty
        max_length=10000,  # Limit for processing
    )
    
    # Unique identifier for tracking
    id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this text entry",
    )
    
    # Source of the text
    source: str = Field(
        default="unknown",
        description="Origin of the text (twitter, youtube, api, etc.)",
    )
    
    # Collection timestamp
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the text was collected",
    )
    
    # Additional metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context about the text",
    )
    
    # =================================================================
    # VALIDATORS
    # =================================================================
    
    @field_validator("text", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """
        Strip leading/trailing whitespace from text.
        
        This validator runs before other validation to ensure
        clean input.
        
        Args:
            v: Raw text input
        
        Returns:
            Stripped text
        """
        # Convert to string if not already
        if not isinstance(v, str):
            v = str(v)
        
        # Strip whitespace
        return v.strip()


# =============================================================================
# PROCESSING INFO
# =============================================================================

class ProcessingStep(BaseModel):
    """
    Information about a single preprocessing step.
    
    Tracks what preprocessing was applied to the text.
    """
    
    # Name of the step
    step: str = Field(..., description="Name of preprocessing step")
    
    # Whether step was applied
    applied: bool = Field(..., description="Whether step was applied")
    
    # Number of items affected
    affected_count: Optional[int] = Field(
        default=None,
        description="Number of characters/tokens affected",
    )
    
    # Step parameters
    params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Parameters used in this step",
    )


class ProcessingInfo(BaseModel):
    """
    Information about all preprocessing steps applied.
    
    This tracks the entire preprocessing pipeline for debugging.
    """
    
    # Steps applied in order
    steps_applied: List[ProcessingStep] = Field(
        default_factory=list,
        description="Preprocessing steps applied in order",
    )
    
    # Total processing time
    processing_time_ms: float = Field(
        ...,
        description="Total processing time in milliseconds",
    )
    
    # Original text length
    original_length: int = Field(
        ...,
        description="Original text length",
    )
    
    # Final text length
    final_length: int = Field(
        ...,
        description="Final text length after processing",
    )


# =============================================================================
# PREPROCESSED TEXT
# =============================================================================

class PreprocessedText(BaseModel):
    """
    Text after preprocessing (cleaning, normalization).
    
    This is the output from the preprocessing service.
    Contains cleaned text and processing metadata.
    """
    
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
    )
    
    # Unique identifier
    id: str = Field(..., description="Unique identifier")
    
    # Original text
    text: str = Field(..., description="Original text")
    
    # Cleaned text
    cleaned_text: str = Field(
        ...,
        description="Cleaned and normalized text",
    )
    
    # Processing information
    processing_info: ProcessingInfo = Field(
        ...,
        description="Information about preprocessing applied",
    )
    
    # Detected language
    language: Optional[str] = Field(
        default=None,
        description="Detected language (ISO 639-1 code)",
    )
    
    # Whether text is valid for processing
    is_valid: bool = Field(
        default=True,
        description="Whether text passed validation",
    )
    
    # Reason if invalid
    invalid_reason: Optional[str] = Field(
        default=None,
        description="Reason if text is invalid",
    )
    
    # Source
    source: str = Field(default="unknown")
    
    # Timestamp
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# TEXT METADATA
# =============================================================================

class TextMetadata(BaseModel):
    """
    Additional metadata about text data.
    
    Contains statistical information about the text for analysis.
    """
    
    # Unique identifier
    text_id: str = Field(..., description="Text ID")
    
    # Character count
    character_count: int = Field(..., description="Character count")
    
    # Word count
    word_count: int = Field(..., description="Word count")
    
    # Sentence count
    sentence_count: int = Field(..., description="Sentence count")
    
    # Average word length
    average_word_length: float = Field(..., description="Average word length")
    
    # Language detection
    language_detection: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Language detection results",
    )
    
    # Encoding
    encoding: str = Field(default="utf-8")
    
    # Social media features
    has_urls: bool = Field(default=False)
    has_emails: bool = Field(default=False)
    has_phone_numbers: bool = Field(default=False)
    has_emoji: bool = Field(default=False)
    has_mentions: bool = Field(default=False)
    has_hashtags: bool = Field(default=False)
    
    # Extraction timestamp
    extracted_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "ClassificationLabel",
    "RawTextInput",
    "PreprocessedText",
    "TextMetadata",
    "ProcessingStep",
    "ProcessingInfo",
]
