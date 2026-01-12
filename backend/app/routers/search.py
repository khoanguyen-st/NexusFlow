from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.schemas import SearchRequest, SearchResponse
from app.services.searcher import SearcherService

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Semantic search across indexed files.
    
    Returns the most relevant files based on the query.
    """
    searcher = SearcherService(db)
    
    try:
        results = await searcher.search(
            project_id=request.project_id,
            query=request.query,
            top_k=request.top_k,
        )
        
        return SearchResponse(
            query=request.query,
            results=results,
            total=len(results),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
