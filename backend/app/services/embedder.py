from app.config import get_settings

settings = get_settings()


class EmbedderService:
    """Service for generating text embeddings."""
    
    def __init__(self):
        # TODO: Initialize Gemini client based on settings.llm_provider
        # TODO: Set up API keys from settings
        pass
    
    async def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding for a text.
        
        TODO: Implement this method:
        1. Truncate text if too long (max 8000 chars)
        2. Call appropriate embedding API (Gemini)
        3. Return embedding vector as list of floats
        
        Hint: Use Gemini's embedding-001 model
        Dimension: 1536
        """
        # TODO: Implement embedding generation
        raise NotImplementedError("Embedding not yet implemented")
    
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        TODO: Implement batch embedding for efficiency:
        1. For Gemini: process one by one
        """
        # TODO: Implement batch embedding
        raise NotImplementedError("Batch embedding not yet implemented")