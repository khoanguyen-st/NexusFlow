from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectResponse, IndexRequest, IndexResponse
from app.services.indexer import IndexerService

router = APIRouter()


@router.get("", response_model=list[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    """List all projects."""
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    projects = result.scalars().all()
    return projects


@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new project."""
    new_project = Project(
        name=project.name,
        path=project.path,
        description=project.description,
        status="pending",
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a project by ID."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a project and its embeddings."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.delete(project)
    await db.commit()
    
    return {"message": "Project deleted successfully"}


@router.post("/{project_id}/index", response_model=IndexResponse)
async def index_project(
    project_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Start indexing a project (runs in background)."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update status to indexing
    project.status = "indexing"
    await db.commit()
    
    # Run indexing in background
    indexer = IndexerService()
    background_tasks.add_task(indexer.index_project, project_id, project.path)
    
    return IndexResponse(
        project_id=project_id,
        status="indexing",
        files_indexed=0,
        message="Indexing started in background",
    )
