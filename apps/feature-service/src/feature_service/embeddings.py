# =============================================================================
# EMBEDDINGS MODULE
# =============================================================================
# Placeholder for embeddings module

from typing import List

class EmbeddingGenerator:
    """Generate text embeddings."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
    
    def generate(self, text: str) -> List[float]:
        """Generate single embedding."""
        import numpy as np
        # Fallback random embedding
        return np.random.randn(384).tolist()
    
    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate batch embeddings."""
        import numpy as np
        return [np.random.randn(384).tolist() for _ in texts]
