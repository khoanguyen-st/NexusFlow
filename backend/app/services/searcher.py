from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.services.embedder import EmbedderService
from app.schemas import SearchResult


class SearcherService:
    """Service for semantic search over indexed files."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.embedder = EmbedderService()
    
    async def search(
        self,
        project_id: UUID,
        query: str,
        top_k: int = 10,
    ) -> list[SearchResult]:
        """
        Search for files semantically similar to the query.
        
        Args:
            project_id: UUID of the project to search in
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of search results with similarity scores
        """
        # Generate query embedding
        query_embedding = await self.embedder.embed_text(query)
        
        # Convert to string for SQL
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        # Perform vector similarity search using pgvector
        sql = text("""
            SELECT 
                file_path,
                file_name,
                content,
                1 - (embedding <=> :embedding::vector) as similarity
            FROM file_embeddings
            WHERE project_id = :project_id
            ORDER BY embedding <=> :embedding::vector
            LIMIT :limit
        """)
        
        result = await self.db.execute(
            sql,
            {
                "project_id": str(project_id),
                "embedding": embedding_str,
                "limit": top_k,
            }
        )
        
        rows = result.fetchall()
        
        return [
            SearchResult(
                file_path=row.file_path,
                file_name=row.file_name,
                content=row.content[:500] if row.content else "",  # Truncate for response
                similarity=float(row.similarity),
            )
            for row in rows
        ]
