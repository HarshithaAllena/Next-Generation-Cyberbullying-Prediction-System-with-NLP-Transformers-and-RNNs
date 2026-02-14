# =============================================================================
# TEXT PREPROCESSOR
# =============================================================================
# Purpose: Main text preprocessing pipeline.
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

import re  # Regular expressions
import time  # Time tracking
from dataclasses import dataclass  # Data classes
from typing import Any, Dict, List, Optional  # Type hints

# Import shared components
from cyberbullying_shared_common import get_logger, generate_uuid

# Import cleaners
from preprocessing_service.cleaners import (
    URLCleaner,
    EmailCleaner,
    MentionCleaner,
    HashtagCleaner,
    EmojiCleaner,
    SpecialCharCleaner,
)

# Import tokenizer
from preprocessing_service.tokenizers import SimpleTokenizer

# Get logger
logger = get_logger(__name__)


# =============================================================================
# PROCESSING RESULT
# =============================================================================

@dataclass
class ProcessingResult:
    """
    Result of text preprocessing.
    
    Contains the cleaned text and metadata about processing steps.
    """
    # Unique ID for this result
    id: str
    # Original text
    original_text: str
    # Cleaned text
    cleaned_text: str
    # Whether processing was successful
    is_valid: bool
    # Reason if invalid
    invalid_reason: Optional[str] = None
    # Processing steps applied
    steps_applied: List[Dict[str, Any]] = None
    # Processing time in milliseconds
    processing_time_ms: float = 0.0
    
    def __post_init__(self):
        if self.steps_applied is None:
            self.steps_applied = []


# =============================================================================
# TEXT PREPROCESSOR
# =============================================================================

class TextPreprocessor:
    """
    Main text preprocessing pipeline.
    
    This class orchestrates the entire preprocessing pipeline:
    1. URL removal/replacement
    2. Email removal
    3. Mention handling
    4. Hashtag handling
    5. Emoji handling
    6. Special character cleaning
    7. Lowercasing
    8. Whitespace normalization
    9. Tokenization
    
    Attributes:
        remove_urls: Whether to remove URLs
        remove_emails: Whether to remove emails
        lowercase: Whether to convert to lowercase
        remove_special_chars: Whether to remove special characters
        max_length: Maximum text length
        min_length: Minimum text length
    
    Example:
        >>> preprocessor = TextPreprocessor(
        ...     remove_urls=True,
        ...     lowercase=True,
        ...     max_length=1000
        ... )
        >>> result = preprocessor.process("Check this! http://example.com")
        >>> result.cleaned_text
        'check this !'
    """
    
    def __init__(
        self,
        remove_urls: bool = True,
        remove_emails: bool = True,
        remove_mentions: bool = False,
        remove_hashtags: bool = False,
        remove_emoji: bool = False,
        lowercase: bool = True,
        remove_special_chars: bool = False,
        max_length: int = 10000,
        min_length: int = 3,
    ) -> None:
        """
        Initialize text preprocessor.
        
        Args:
            remove_urls: Remove URLs from text
            remove_emails: Remove email addresses
            remove_mentions: Remove @mentions
            remove_hashtags: Remove #hashtags
            remove_emoji: Remove emojis
            lowercase: Convert to lowercase
            remove_special_chars: Remove special characters
            max_length: Maximum text length
            min_length: Minimum text length
        """
        # Store configuration
        self.remove_urls = remove_urls
        self.remove_emails = remove_emails
        self.remove_mentions = remove_mentions
        self.remove_hashtags = remove_hashtags
        self.remove_emoji = remove_emoji
        self.lowercase = lowercase
        self.remove_special_chars = remove_special_chars
        self.max_length = max_length
        self.min_length = min_length
        
        # Initialize cleaners
        self.url_cleaner = URLCleaner()
        self.email_cleaner = EmailCleaner()
        self.mention_cleaner = MentionCleaner()
        self.hashtag_cleaner = HashtagCleaner()
        self.emoji_cleaner = EmojiCleaner()
        self.special_char_cleaner = SpecialCharCleaner()
        
        # Initialize tokenizer
        self.tokenizer = SimpleTokenizer()
        
        logger.info("TextPreprocessor initialized", config=self._get_config())
    
    def _get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return {
            "remove_urls": self.remove_urls,
            "remove_emails": self.remove_emails,
            "remove_mentions": self.remove_mentions,
            "remove_hashtags": self.remove_hashtags,
            "remove_emoji": self.remove_emoji,
            "lowercase": self.lowercase,
            "remove_special_chars": self.remove_special_chars,
            "max_length": self.max_length,
            "min_length": self.min_length,
        }
    
    def process(self, text: str, track_steps: bool = True) -> ProcessingResult:
        """
        Process text through the preprocessing pipeline.
        
        Args:
            text: Input text to process
            track_steps: Whether to track processing steps
        
        Returns:
            ProcessingResult with cleaned text and metadata
        """
        # Generate unique ID
        result_id = generate_uuid()
        
        # Record start time
        start_time = time.perf_counter()
        
        # Initialize steps list
        steps = [] if track_steps else None
        
        # Store original
        original_text = text
        original_length = len(text)
        
        # Validate input
        if not text or not text.strip():
            return ProcessingResult(
                id=result_id,
                original_text=text or "",
                cleaned_text="",
                is_valid=False,
                invalid_reason="empty_text",
                steps_applied=[],
                processing_time_ms=0.0,
            )
        
        # Track current text
        current_text = text
        
        # Step 1: Remove URLs
        if self.remove_urls:
            before_len = len(current_text)
            current_text = self.url_cleaner.clean(current_text)
            if track_steps:
                steps.append({
                    "step": "remove_urls",
                    "applied": True,
                    "affected_count": before_len - len(current_text),
                })
        
        # Step 2: Remove emails
        if self.remove_emails:
            before_len = len(current_text)
            current_text = self.email_cleaner.clean(current_text)
            if track_steps:
                steps.append({
                    "step": "remove_emails",
                    "applied": True,
                    "affected_count": before_len - len(current_text),
                })
        
        # Step 3: Remove mentions
        if self.remove_mentions:
            before_len = len(current_text)
            current_text = self.mention_cleaner.clean(current_text)
            if track_steps:
                steps.append({
                    "step": "remove_mentions",
                    "applied": True,
                    "affected_count": before_len - len(current_text),
                })
        
        # Step 4: Remove hashtags
        if self.remove_hashtags:
            before_len = len(current_text)
            current_text = self.hashtag_cleaner.clean(current_text)
            if track_steps:
                steps.append({
                    "step": "remove_hashtags",
                    "applied": True,
                    "affected_count": before_len - len(current_text),
                })
        
        # Step 5: Remove emoji
        if self.remove_emoji:
            before_len = len(current_text)
            current_text = self.emoji_cleaner.clean(current_text)
            if track_steps:
                steps.append({
                    "step": "remove_emoji",
                    "applied": True,
                    "affected_count": before_len - len(current_text),
                })
        
        # Step 6: Lowercase
        if self.lowercase:
            current_text = current_text.lower()
            if track_steps:
                steps.append({
                    "step": "lowercase",
                    "applied": True,
                })
        
        # Step 7: Remove special characters
        if self.remove_special_chars:
            before_len = len(current_text)
            current_text = self.special_char_cleaner.clean(current_text)
            if track_steps:
                steps.append({
                    "step": "remove_special_chars",
                    "applied": True,
                    "affected_count": before_len - len(current_text),
                })
        
        # Step 8: Normalize whitespace
        current_text = self._normalize_whitespace(current_text)
        if track_steps:
            steps.append({
                "step": "normalize_whitespace",
                "applied": True,
            })
        
        # Step 9: Trim
        current_text = current_text.strip()
        
        # Calculate processing time
        processing_time_ms = (time.perf_counter() - start_time) * 1000
        
        # Validate output
        is_valid = True
        invalid_reason = None
        
        if len(current_text) > self.max_length:
            is_valid = False
            invalid_reason = "text_too_long"
        elif len(current_text) < self.min_length:
            is_valid = False
            invalid_reason = "text_too_short"
        
        return ProcessingResult(
            id=result_id,
            original_text=original_text,
            cleaned_text=current_text,
            is_valid=is_valid,
            invalid_reason=invalid_reason,
            steps_applied=steps or [],
            processing_time_ms=processing_time_ms,
        )
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text.
        
        - Replace multiple spaces with single space
        - Replace tabs with spaces
        - Remove leading/trailing whitespace
        
        Args:
            text: Input text
        
        Returns:
            Normalized text
        """
        # Replace tabs with spaces
        text = text.replace("\t", " ")
        
        # Replace multiple spaces with single space
        text = re.sub(r" +", " ", text)
        
        # Replace multiple newlines with single newline
        text = re.sub(r"\n+", "\n", text)
        
        return text
    
    def process_batch(self, texts: List[str]) -> List[ProcessingResult]:
        """
        Process multiple texts.
        
        Args:
            texts: List of input texts
        
        Returns:
            List of ProcessingResults
        """
        return [self.process(text) for text in texts]
