from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import SearchRequest, SearchResponse
from app.services.searcher import SearcherService

router = APIRouter()

# TODO: Implement semantic search endpoint
# This endpoint will use vector similarity to find relevant files

@router.post("", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    TODO: Implement semantic search endpoint
    Steps:
    1. Create SearcherService instance with db session
    2. Call searcher.search() with:
       - project_id from request
       - query from request
       - top_k from request (default 10)
    3. Return SearchResponse with query, results, and total count
    4. Handle exceptions and return appropriate error responses
    
    Error handling:
    - Catch general exceptions and raise HTTPException with 500
    """
    
    """
    POST /api/search
    Body: { project_id, query, top_k? }
    Returns: List of similar files
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