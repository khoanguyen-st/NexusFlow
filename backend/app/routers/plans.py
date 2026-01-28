from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.schemas import PlanGenerateRequest, PlanResponse, PlanData
from app.services.planner import PlannerService
from sqlalchemy import select
from app.models import Plan

router = APIRouter()

@router.post("/generate", response_model=PlanResponse)
async def generate_plan(
    request: PlanGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /api/plans/generate
    Body: { project_id, task }
    Returns: Generated implementation plan
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
    """
    GET /api/plans/{id}
    Returns: Plan details
    """
    
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalar_one_or_none()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return PlanResponse(
        id=plan.id,
        project_id=plan.project_id,
        task_description=plan.task_description,
        plan=PlanData(**plan.plan_data),
        context_used=plan.context_files or [],
        confidence=plan.confidence or 0.0,
        created_at=plan.created_at,
    )


@router.get("/project/{project_id}", response_model=list[PlanResponse])
async def list_project_plans(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    GET /api/plans/project/{project_id}
    Returns: All plans for a project
    """
    
    result = await db.execute(
        select(Plan)
        .where(Plan.project_id == project_id)
        .order_by(Plan.created_at.desc())
    )
    plans = result.scalars().all()
    
    return [
        PlanResponse(
            id=p.id,
            project_id=p.project_id,
            task_description=p.task_description,
            plan=PlanData(**p.plan_data),
            context_used=p.context_files or [],
            confidence=p.confidence or 0.0,
            created_at=p.created_at,
        )
        for p in plans
    ]