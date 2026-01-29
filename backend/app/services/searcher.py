from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import SearchResult
from app.services.embedder import EmbedderService
from app.models.models import FileEmbedding

class SearcherService:
    """Service for semantic search over indexed files."""
    
    def __init__(self, db: AsyncSession):
        self.embedder = embedder or EmbedderService()
        self.db = db
    
    async def search(
        self,
        project_id: UUID,
        query: str,
        top_k: int = 10,
    ) -> list[SearchResult]:
        """
        Search for files semantically similar to the query.
        """

        # Generate embedding for the query
        try:
            query_embedding = await self.embedder.embed_text(query)
            
            if not query_embedding:
                    logger.warning(f"Empty embedding generated for query: {query[:50]}")
                    return []
                
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise RuntimeError(f"Embedding generation failed: {e}")
        
        # Search using pgvector cosine distance
        distance_col = FileEmbedding.embedding.cosine_distance(query_embedding).label("distance")
        
        stmt = (
            select(FileEmbedding, distance_col)
            .where(FileEmbedding.project_id == project_id)
            .order_by(distance_col)
            .limit(top_k)
        )
        
        result = await self.db.execute(stmt)
        rows = result.all()
        
        return [
            SearchResult(
                file_path=file_embedding.file_path,
                file_name=file_embedding.file_name,
                content=file_embedding.content or "",
                similarity=float(1.0 - distance)
            )
            for file_embedding, distance in rows
        ]
