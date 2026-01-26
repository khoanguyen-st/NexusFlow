from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.schemas import ProjectCreate, ProjectResponse, IndexResponse

router = APIRouter()

# TODO: Implement CRUD endpoints for projects
# Reference: https://fastapi.tiangulo.com/tutorial/

# @router.get("", response_model=list[ProjectResponse])
# async def list_projects(db: AsyncSession = Depends(get_db)):
#     """
#     TODO: Implement list all projects endpoint
#     Steps:
#     1. Query all projects from database using SQLAlchemy
#     2. Order by created_at descending
#     3. Return list of projects
#     
#     Hint: Use db.execute(select(Project).order_by(...))
#     """
#     pass


# @router.post("", response_model=ProjectResponse)
# async def create_project(
#     project: ProjectCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     TODO: Implement create project endpoint
#     Steps:
#     1. Create new Project instance with data from request
#     2. Set status to 'pending'
#     3. Add to database session
#     4. Commit and refresh
#     5. Return created project
#     """
#     pass


# @router.get("/{project_id}", response_model=ProjectResponse)
# async def get_project(
#     project_id: UUID,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     TODO: Implement get project by ID endpoint
#     Steps:
#     1. Query project from database by ID
#     2. If not found, raise HTTPException with 404
#     3. Return project
#     """
#     pass


# @router.delete("/{project_id}")
# async def delete_project(
#     project_id: UUID,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     TODO: Implement delete project endpoint
#     Steps:
#     1. Query project from database by ID
#     2. If not found, raise HTTPException with 404
#     3. Delete project from database
#     4. Commit changes
#     5. Return success message
#     
#     Note: Embeddings will be auto-deleted due to CASCADE
#     """
#     pass


# @router.post("/{project_id}/index", response_model=IndexResponse)
# async def index_project(
#     project_id: UUID,
#     background_tasks: BackgroundTasks,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     TODO: Implement project indexing endpoint
#     Steps:
#     1. Get project by ID from database
#     2. If not found, raise HTTPException with 404
#     3. Update project status to 'indexing'
#     4. Commit the status change
#     5. Add indexer.index_project() to background_tasks
#     6. Return IndexResponse with status 'indexing'
#     
#     Hint: Use background_tasks.add_task(function, *args)
#     Hint: IndexerService() needs to be instantiated
#     """
#     pass
