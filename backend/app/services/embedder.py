import logging
import asyncio
import google.generativeai as genai
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class EmbedderService:
    """Service for generating text embeddings."""
    def __init__(self):
        self.api_key = settings.gemini_api_key
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.warning("NO GEMINI_API_KEY. Embedding doesn't work")
            
    async def embed_text(self, text: str) -> list[float]:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        loop = asyncio.get_event_loop()
        
        text = text[:8000].replace("\n", " ")

        try:
            result = await loop.run_in_executor(
                None,  
                lambda: genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
            )
            
            await asyncio.sleep(0.1)
            
            embedding = result['embedding']
            if len(embedding) != 768:
                logger.warning(f"Unexpected dimension: {len(embedding)}, expected 768")

            return embedding
            
        except Exception as e:
            logger.error(f"failed to embedding: {e}")
            raise e
    
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        
        tasks = [self.embed_text(text) for text in texts]
        
        try:
            embeddings = await asyncio.gather(*tasks)
            return embeddings
            
        except Exception as e:
            logger.error(f"error during batch processing: {e}")
            raise e