from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.schemas import PlanGenerateRequest, PlanResponse

router = APIRouter()

# TODO: Implement AI plan generation endpoints

# @router.post("/generate", response_model=PlanResponse)
# async def generate_plan(
#     request: PlanGenerateRequest,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     TODO: Implement AI plan generation endpoint
#     Steps:
#     1. Create PlannerService instance with db session
#     2. Call planner.generate_plan() with:
#        - project_id from request
#        - task from request
#     3. Return generated PlanResponse
#     4. Handle errors:
#        - ValueError -> HTTPException 400 (validation errors)
#        - General Exception -> HTTPException 500 (server errors)
#     
#     This is the core AI feature that analyzes code and generates plans!
#     """
#     pass


# @router.get("/{plan_id}", response_model=PlanResponse)
# async def get_plan(
#     plan_id: UUID,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     TODO: Implement get plan by ID endpoint
#     Steps:
#     1. Query Plan from database by ID
#     2. If not found, raise HTTPException with 404
#     3. Transform Plan model to PlanResponse
#     4. Return PlanResponse
#     
#     Hint: plan.plan_data is JSONB, needs to be unpacked
#     """
#     pass


# @router.get("/project/{project_id}", response_model=list[PlanResponse])
# async def list_project_plans(
#     project_id: UUID,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     TODO: Implement list all plans for a project endpoint
#     Steps:
#     1. Query all Plans for the given project_id
#     2. Order by created_at descending
#     3. Transform each Plan to PlanResponse
#     4. Return list of PlanResponses
#     """
#     pass
