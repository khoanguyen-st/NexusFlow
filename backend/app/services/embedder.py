import logging
import asyncio
import google.generativeai as genai
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class EmbedderService:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model_name = settings.embedding_model
        self.semaphore = asyncio.Semaphore(5)
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.warning("NO GEMINI_API_KEY. Embedding doesn't work")
            
    async def embed_text(self, text: str) -> list[float]:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        text = text[:8000].replace("\n", " ")

        async with self.semaphore:
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,  
                    lambda: genai.embed_content(
                        model=self.model_name,
                        content=text,
                        task_type="retrieval_document"
                    )
                )
                
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
