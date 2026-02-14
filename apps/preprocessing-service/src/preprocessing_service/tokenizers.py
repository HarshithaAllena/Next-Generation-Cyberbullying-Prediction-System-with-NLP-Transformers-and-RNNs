# =============================================================================
# TOKENIZERS
# =============================================================================
# Purpose: Text tokenization utilities.
#
# Author: Cyberbullying Prediction Team
# Version: 1.0.0
# =============================================================================

import re  # Regular expressions
from typing import List  # Type hints


# =============================================================================
# SIMPLE TOKENIZER
# =============================================================================

class SimpleTokenizer:
    """
    Simple whitespace-based tokenizer.
    
    Splits text into tokens based on whitespace.
    Suitable for basic tokenization needs.
    
    Example:
        >>> tokenizer = SimpleTokenizer()
        >>> tokenizer.tokenize("Hello world!")
        ['Hello', 'world!']
    """
    
    def __init__(self, lowercase: bool = False) -> None:
        """
        Initialize tokenizer.
        
        Args:
            lowercase: Whether to lowercase tokens
        """
        self.lowercase = lowercase
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Input text
        
        Returns:
            List of tokens
        """
        # Split on whitespace
        tokens = text.split()
        
        # Lowercase if requested
        if self.lowercase:
            tokens = [t.lower() for t in tokens]
        
        return tokens
    
    def __call__(self, text: str) -> List[str]:
        """Allow calling as function."""
        return self.tokenize(text)


# =============================================================================
# WORD TOKENIZER
# =============================================================================

class WordTokenizer:
    """
    Word-level tokenizer with punctuation handling.
    
    Separates punctuation from words for cleaner tokenization.
    
    Example:
        >>> tokenizer = WordTokenizer()
        >>> tokenizer.tokenize("Hello, world!")
        ['Hello', ',', 'world', '!']
    """
    
    # Pattern to split words and punctuation
    PATTERN = re.compile(r"(\w+|[^\w\s])")
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text.
        
        Args:
            text: Input text
        
        Returns:
            List of tokens
        """
        # Find all matches
        tokens = self.PATTERN.findall(text)
        
        # Filter empty strings
        tokens = [t for t in tokens if t.strip()]
        
        return tokens


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "SimpleTokenizer",
    "WordTokenizer",
]
