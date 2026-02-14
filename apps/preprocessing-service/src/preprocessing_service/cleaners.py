# =============================================================================
# TEXT CLEANERS
# =============================================================================
# Purpose: Individual cleaning functions for different text patterns.
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

import re  # Regular expressions
from abc import ABC, abstractmethod  # Abstract base class


# =============================================================================
# BASE CLEANER
# =============================================================================

class BaseCleaner(ABC):
    """
    Abstract base class for text cleaners.
    
    All cleaners inherit from this class to ensure consistent interface.
    """
    
    @abstractmethod
    def clean(self, text: str) -> str:
        """
        Clean text.
        
        Args:
            text: Input text
        
        Returns:
            Cleaned text
        """
        pass


# =============================================================================
# URL CLEANER
# =============================================================================

class URLCleaner(BaseCleaner):
    """
    Removes or replaces URLs from text.
    
    Handles:
    - http:// URLs
    - https:// URLs
    - www. URLs
    
    Example:
        >>> cleaner = URLCleaner()
        >>> cleaner.clean("Check http://example.com now")
        'Check  now'
    """
    
    # URL pattern
    URL_PATTERN = re.compile(
        r"(?:https?://|www\.)[^\s]+",
        re.IGNORECASE,
    )
    
    def clean(self, text: str) -> str:
        """
        Remove URLs from text.
        
        Args:
            text: Input text with URLs
        
        Returns:
            Text with URLs removed
        """
        # Replace URLs with space
        cleaned = self.URL_PATTERN.sub(" ", text)
        
        return cleaned


# =============================================================================
# EMAIL CLEANER
# =============================================================================

class EmailCleaner(BaseCleaner):
    """
    Removes email addresses from text.
    
    Example:
        >>> cleaner = EmailCleaner()
        >>> cleaner.clean("Contact test@example.com please")
        'Contact  please'
    """
    
    # Email pattern
    EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    )
    
    def clean(self, text: str) -> str:
        """Remove email addresses."""
        return self.EMAIL_PATTERN.sub(" ", text)


# =============================================================================
# MENTION CLEANER
# =============================================================================

class MentionCleaner(BaseCleaner):
    """
    Removes or extracts @mentions from text.
    
    Example:
        >>> cleaner = MentionCleaner()
        >>> cleaner.clean("Hello @user123!")
        'Hello !'
    """
    
    # Mention pattern
    MENTION_PATTERN = re.compile(r"@[a-zA-Z0-9_]+")
    
    def clean(self, text: str) -> str:
        """Remove @mentions."""
        return self.MENTION_PATTERN.sub(" ", text)


# =============================================================================
# HASHTAG CLEANER
# =============================================================================

class HashtagCleaner(BaseCleaner):
    """
    Removes or extracts #hashtags from text.
    
    Example:
        >>> cleaner = HashtagCleaner()
        >>> cleaner.clean(" trending now")
        ' now'
    """
    
    # Hashtag pattern
    HASHTAG_PATTERN = re.compile(r"#[a-zA-Z0-9_]+")
    
    def clean(self, text: str) -> str:
        """Remove #hashtags."""
        return self.HASHTAG_PATTERN.sub(" ", text)


# =============================================================================
# EMOJI CLEANER
# =============================================================================

class EmojiCleaner(BaseCleaner):
    """
    Removes emojis from text.
    
    Uses Unicode emoji ranges to identify and remove emojis.
    
    Example:
        >>> cleaner = EmojiCleaner()
        >>> cleaner.clean("Hello !")
        'Hello !'
    """
    
    # Emoji pattern (comprehensive)
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    
    def clean(self, text: str) -> str:
        """Remove emojis."""
        return self.EMOJI_PATTERN.sub(" ", text)


# =============================================================================
# SPECIAL CHARACTER CLEANER
# =============================================================================

class SpecialCharCleaner(BaseCleaner):
    """
    Removes special characters from text.
    
    Keeps alphanumeric characters, spaces, and basic punctuation.
    
    Example:
        >>> cleaner = SpecialCharCleaner()
        >>> cleaner.clean("Hello! @#$%")
        'Hello! '
    """
    
    def __init__(self, keep_punctuation: bool = True) -> None:
        """
        Initialize cleaner.
        
        Args:
            keep_punctuation: Whether to keep basic punctuation
        """
        self.keep_punctuation = keep_punctuation
        
        if keep_punctuation:
            # Keep letters, numbers, spaces, and common punctuation
            self.pattern = re.compile(r"[^a-zA-Z0-9\s!?.,'\"-]")
        else:
            # Keep only letters, numbers, spaces
            self.pattern = re.compile(r"[^a-zA-Z0-9\s]")
    
    def clean(self, text: str) -> str:
        """Remove special characters."""
        return self.pattern.sub(" ", text)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "BaseCleaner",
    "URLCleaner",
    "EmailCleaner",
    "MentionCleaner",
    "HashtagCleaner",
    "EmojiCleaner",
    "SpecialCharCleaner",
]
