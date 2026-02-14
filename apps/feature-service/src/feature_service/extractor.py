# =============================================================================
# FEATURE EXTRACTOR
# =============================================================================
# Purpose: Extract features from preprocessed text.

import re  # Regular expressions
from dataclasses import dataclass  # Data classes
from typing import Any, Dict, List, Optional  # Type hints

# Import shared components
from cyberbullying_shared_common import get_logger, generate_uuid

# Get logger
logger = get_logger(__name__)


# =============================================================================
# FEATURE RESULT
# =============================================================================

@dataclass
class FeatureResult:
    """Result of feature extraction."""
    id: str
    text_id: str
    preprocessed_text: str
    statistical_features: Dict[str, float]
    social_features: Dict[str, Any]
    linguistic_features: Dict[str, float]
    extraction_time_ms: float


# =============================================================================
# FEATURE EXTRACTOR
# =============================================================================

class FeatureExtractor:
    """
    Extract features from preprocessed text.
    
    Features include:
    - Statistical: char count, word count, etc.
    - Social: mentions, hashtags, URLs, etc.
    - Linguistic: lexical diversity, sentiment, etc.
    """
    
    def __init__(self):
        """Initialize feature extractor."""
        logger.info("FeatureExtractor initialized")
    
    def extract(self, text: str, text_id: Optional[str] = None) -> FeatureResult:
        """
        Extract features from text.
        
        Args:
            text: Preprocessed text
            text_id: Optional text ID
        
        Returns:
            FeatureResult with extracted features
        """
        import time
        start_time = time.perf_counter()
        
        # Generate ID if not provided
        if text_id is None:
            text_id = generate_uuid()
        
        result_id = generate_uuid()
        
        # Extract features
        statistical = self._extract_statistical_features(text)
        social = self._extract_social_features(text)
        linguistic = self._extract_linguistic_features(text)
        
        extraction_time_ms = (time.perf_counter() - start_time) * 1000
        
        return FeatureResult(
            id=result_id,
            text_id=text_id,
            preprocessed_text=text,
            statistical_features=statistical,
            social_features=social,
            linguistic_features=linguistic,
            extraction_time_ms=extraction_time_ms,
        )
    
    def _extract_statistical_features(self, text: str) -> Dict[str, float]:
        """Extract statistical features."""
        words = text.split()
        
        # Basic counts
        char_count = len(text)
        word_count = len(words)
        unique_words = len(set(words))
        
        # Average lengths
        avg_word_length = sum(len(w) for w in words) / max(word_count, 1)
        
        # Sentence count (approximate)
        sentence_count = max(1, text.count('.') + text.count('!') + text.count('?'))
        avg_sentence_length = word_count / sentence_count
        
        # Uppercase
        uppercase_count = sum(1 for c in text if c.isupper())
        uppercase_ratio = uppercase_count / max(char_count, 1)
        
        # Punctuation
        exclamation_count = text.count('!')
        question_count = text.count('?')
        
        # Repeated characters (e.g., "sooo")
        repeated_char_count = len(re.findall(r'(.)\1{2,}', text))
        
        return {
            "character_count": char_count,
            "word_count": word_count,
            "unique_word_count": unique_words,
            "average_word_length": avg_word_length,
            "sentence_count": sentence_count,
            "average_sentence_length": avg_sentence_length,
            "uppercase_count": uppercase_count,
            "uppercase_ratio": uppercase_ratio,
            "exclamation_count": exclamation_count,
            "question_count": question_count,
            "repeated_char_count": repeated_char_count,
        }
    
    def _extract_social_features(self, text: str) -> Dict[str, Any]:
        """Extract social media features."""
        # Mentions (@username)
        mentions = re.findall(r'@\w+', text)
        mention_count = len(mentions)
        unique_mention_count = len(set(mentions))
        
        # Hashtags (#hashtag)
        hashtags = re.findall(r'#\w+', text)
        hashtag_count = len(hashtags)
        
        # URLs
        urls = re.findall(r'https?://\S+', text)
        url_count = len(urls)
        
        # Emoji
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "]+"
        )
        emojis = emoji_pattern.findall(text)
        emoji_count = len(emojis)
        
        # Retweet check
        is_retweet = text.lower().startswith('rt ')
        
        return {
            "mention_count": mention_count,
            "unique_mention_count": unique_mention_count,
            "hashtag_count": hashtag_count,
            "url_count": url_count,
            "emoji_count": emoji_count,
            "is_retweet": is_retweet,
        }
    
    def _extract_linguistic_features(self, text: str) -> Dict[str, float]:
        """Extract linguistic features."""
        words = text.split()
        word_count = len(words)
        
        # Lexical diversity (unique words / total words)
        lexical_diversity = len(set(words)) / max(word_count, 1)
        
        # Simple sentiment approximation (basic word lists)
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'best', 'love', 'happy', 'nice', 'beautiful'}
        negative_words = {'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'ugly', 'stupid', 'idiot', 'worst'}
        
        words_lower = set(w.lower() for w in words)
        positive_count = len(words_lower & positive_words)
        negative_count = len(words_lower & negative_words)
        
        # Simple polarity: -1 to 1
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words > 0:
            sentiment_polarity = (positive_count - negative_count) / total_sentiment_words
        else:
            sentiment_polarity = 0.0
        
        return {
            "lexical_diversity": lexical_diversity,
            "sentiment_polarity": sentiment_polarity,
            "positive_word_count": positive_count,
            "negative_word_count": negative_count,
        }
    
    def extract_batch(self, texts: List[str], text_ids: Optional[List[str]] = None) -> List[FeatureResult]:
        """Extract features from multiple texts."""
        if text_ids is None:
            text_ids = [None] * len(texts)
        
        return [self.extract(text, tid) for text, tid in zip(texts, text_ids)]


# =============================================================================
# EMBEDDING GENERATOR
# =============================================================================

class EmbeddingGenerator:
    """
    Generate text embeddings using transformers.
    
    Supports:
    - Sentence transformers
    - BERT embeddings
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding generator.
        
        Args:
            model_name: Name of the embedding model
        """
        self.model_name = model_name
        self.model = None
        self.device = None
        logger.info(f"EmbeddingGenerator initialized with model: {model_name}")
    
    def _load_model(self):
        """Load the embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            self.device = self.model.device
            logger.info(f"Loaded embedding model: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers not installed, using fallback")
            self.model = None
    
    def generate(self, text: str) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
        
        Returns:
            Embedding vector as list of floats
        """
        if self.model is None:
            self._load_model()
        
        if self.model is not None:
            # Generate embedding
            embedding = self.model.encode(text)
            return embedding.tolist()
        else:
            # Fallback: random embedding
            import numpy as np
            return np.random.randn(384).tolist()
    
    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        if self.model is None:
            self._load_model()
        
        if self.model is not None:
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
        else:
            import numpy as np
            return [np.random.randn(384).tolist() for _ in texts]
