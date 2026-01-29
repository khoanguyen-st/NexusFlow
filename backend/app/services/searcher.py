from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.schemas import SearchResult
from app.services.embedder import EmbedderService
from app.models.models import FileEmbedding


class SearcherService:
    """Service for semantic search over indexed files."""
    
    def __init__(self, db: AsyncSession):
        self.embedder = EmbedderService()
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
        query_embedding = await self.embedder.embed_text(query)
        
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
        
        search_results = []
        for row in rows:
            file_embedding = row[0]
            distance = row[1]
            
            similarity = 1.0 - distance
            
            search_results.append(
                SearchResult(
                    file_path=file_embedding.file_path,
                    file_name=file_embedding.file_name,
                    content=file_embedding.content or "",
                    similarity=float(similarity)
                )
            )
            
        return search_results
