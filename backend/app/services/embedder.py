from openai import AsyncOpenAI
import google.generativeai as genai
from app.config import get_settings

settings = get_settings()


class EmbedderService:
    """Service for generating text embeddings."""
    
    def __init__(self):
        self.provider = settings.llm_provider
        
        if self.provider == "openai":
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            self.model = settings.embedding_model
        else:
            # Gemini uses sync client, we'll wrap it
            genai.configure(api_key=settings.gemini_api_key)
    
    async def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding for a text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        # Truncate text if too long (for token limits)
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars]
        
        if self.provider == "openai":
            return await self._embed_openai(text)
        else:
            return await self._embed_gemini(text)
    
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if self.provider == "openai":
            return await self._embed_batch_openai(texts)
        else:
            # Gemini doesn't have batch API, process one by one
            return [await self._embed_gemini(text) for text in texts]
    
    async def _embed_openai(self, text: str) -> list[float]:
        """Generate embedding using OpenAI."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return response.data[0].embedding
    
    async def _embed_batch_openai(self, texts: list[str]) -> list[list[float]]:
        """Generate batch embeddings using OpenAI."""
        # Truncate texts
        max_chars = 8000
        truncated = [t[:max_chars] for t in texts]
        
        response = await self.client.embeddings.create(
            model=self.model,
            input=truncated,
        )
        return [item.embedding for item in response.data]
    
    async def _embed_gemini(self, text: str) -> list[float]:
        """Generate embedding using Gemini."""
        # Gemini embedding is synchronous, run in thread pool
        import asyncio
        
        def _embed():
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document",
            )
            return result["embedding"]
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _embed)
