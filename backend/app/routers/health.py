from fastapi import APIRouter
from sqlalchemy import text
from app.database import async_session_maker

router = APIRouter()


@router.get("/health")
async def health_check():
    """Check API and database health."""
    db_status = "ok"
    
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "ok",
        "database": db_status,
        "version": "0.1.0",
    }
