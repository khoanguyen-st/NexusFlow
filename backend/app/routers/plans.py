from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.database import get_db
from app.models import Plan
from app.schemas import PlanGenerateRequest, PlanResponse
from app.services.planner import PlannerService

router = APIRouter()


@router.post("/generate", response_model=PlanResponse)
async def generate_plan(
    request: PlanGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate an implementation plan for a task.
    
    Uses AI to analyze the codebase and create a detailed plan.
    """
    planner = PlannerService(db)
    
    try:
        plan = await planner.generate_plan(
            project_id=request.project_id,
            task=request.task,
        )
        return plan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a plan by ID."""
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return PlanResponse(
        id=plan.id,
        project_id=plan.project_id,
        task_description=plan.task_description,
        plan=plan.plan_data,
        context_used=plan.context_files or [],
        confidence=plan.confidence or 0.0,
        created_at=plan.created_at,
    )


@router.get("/project/{project_id}", response_model=list[PlanResponse])
async def list_project_plans(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """List all plans for a project."""
    result = await db.execute(
        select(Plan)
        .where(Plan.project_id == project_id)
        .order_by(Plan.created_at.desc())
    )
    plans = result.scalars().all()
    
    return [
        PlanResponse(
            id=plan.id,
            project_id=plan.project_id,
            task_description=plan.task_description,
            plan=plan.plan_data,
            context_used=plan.context_files or [],
            confidence=plan.confidence or 0.0,
            created_at=plan.created_at,
        )
        for plan in plans
    ]
