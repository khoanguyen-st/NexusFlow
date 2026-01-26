from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.schemas import ProjectCreate, ProjectResponse, IndexResponse
from sqlalchemy import select
from app.models import Project
from app.services.indexer import IndexerService

router = APIRouter()

# TODO: Implement CRUD endpoints for projects
# Reference: https://fastapi.tiangulo.com/tutorial/

@router.get("", response_model=list[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    """
    TODO: Implement list all projects endpoint
    Steps:
    1. Query all projects from database using SQLAlchemy
    2. Order by created_at descending
    3. Return list of projects
    
    Hint: Use db.execute(select(Project).order_by(...))
    """
    
    """
    GET /api/projects
    Returns: List of all projects
    """
    
    result = await db.execute(
        select(Project).order_by(Project.created_at.desc())
    )
    projects = result.scalars().all()
    return projects


@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    TODO: Implement create project endpoint
    Steps:
    1. Create new Project instance with data from request
    2. Set status to 'pending'
    3. Add to database session
    4. Commit and refresh
    5. Return created project
    """
    
    """
    POST /api/projects
    Body: { name, path, description? }
    Returns: Created project
    """
    
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
    """
    TODO: Implement get project by ID endpoint
    Steps:
    1. Query project from database by ID
    2. If not found, raise HTTPException with 404
    3. Return project
    """
    
    """
    GET /api/projects/{id}
    Returns: Single project or 404
    """
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    TODO: Implement delete project endpoint
    Steps:
    1. Query project from database by ID
    2. If not found, raise HTTPException with 404
    3. Delete project from database
    4. Commit changes
    5. Return success message
    
    Note: Embeddings will be auto-deleted due to CASCADE
    """
    
    """
    DELETE /api/projects/{id}
    Returns: Success message
    """
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
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
    """
    TODO: Implement project indexing endpoint
    Steps:
    1. Get project by ID from database
    2. If not found, raise HTTPException with 404
    3. Update project status to 'indexing'
    4. Commit the status change
    5. Add indexer.index_project() to background_tasks
    6. Return IndexResponse with status 'indexing'
    
    Hint: Use background_tasks.add_task(function, *args)
    Hint: IndexerService() needs to be instantiated
    """
    
    """
    POST /api/projects/{id}/index
    Starts indexing in background
    Returns: Status message
    """
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update status
    project.status = "indexing"
    await db.commit()
    
    # Run in background
    indexer = IndexerService()
    background_tasks.add_task(indexer.index_project, project_id, project.path)
    
    return IndexResponse(
        project_id=project_id,
        status="indexing",
        files_indexed=0,
        message="Indexing started in background",
    )