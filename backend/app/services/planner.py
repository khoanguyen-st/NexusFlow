import json
import logging
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import google.generativeai as genai

from app.config import get_settings
from app.schemas import PlanResponse, PlanData
from app.models.models import Plan, Project
from app.services.searcher import SearcherService

settings = get_settings()
logger = logging.getLogger(__name__)

PLAN_GENERATION_PROMPT = """
You are a senior software architect. Analyze the task and codebase context to create a detailed implementation plan.

Task: {task}

Relevant code files:
{context}

Provide a JSON response with this exact structure:
{{
  "summary": "Brief overview of what needs to be done",
  "affected_files": [
    {{"path": "file_path", "action": "modify/create/delete"}}
  ],
  "steps": [
    {{"order": 1, "description": "Step description", "file": "file_path"}}
  ],
  "reusable_components": [
    {{"name": "Component Name", "description": "Description", "location": "file_path"}}
  ]
}}
"""

class PlannerService:
    """Service for generating implementation plans using AI."""
    
    def __init__(self, db: AsyncSession, searcher: SearcherService = None):
        self.db = db
        self.searcher = searcher or SearcherService(db)
        
        # Initialize Gemini client
        self.api_key = settings.gemini_api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=settings.llm_model,
                generation_config={"response_mime_type": "application/json"}
            )
        else:
            logger.warning("NO GEMINI_API_KEY. Planner functionality will fail.")
            self.model = None
    
    async def generate_plan(
        self,
        project_id: UUID,
        task: str,
    ) -> PlanResponse:
        """
        Generate an implementation plan for a task.
        """
        if not self.model:
            raise ValueError("LLM client not initialized (missing API Key)")

        # 1. Verify project exists
        stmt = select(Project).where(Project.id == project_id)
        result = await self.db.execute(stmt)
        project = result.scalar_one_or_none()
        
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # 2. Search for relevant files and build context string from search results
        search_results = await self.searcher.search(
            project_id=project_id,
            query=task,
            top_k=10
        )
        
        context_files = []
        context_parts = []
        for res in search_results:
            context_files.append(res.file_path)
            content_snippet = res.content if res.content else ""
            context_parts.append(f"File: {res.file_path}\nContent:\n{content_snippet}\n")
            
        context_str = "\n\n".join(context_parts)
        
        # 3. Build prompt
        prompt = PLAN_GENERATION_PROMPT.format(task=task, context=context_str)
        
        # 4. Call LLM
        try:
            response = self.model.generate_content(prompt)
            plan_json = json.loads(response.text)
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise ValueError(f"Failed to generate plan: {str(e)}")

        # 5. Parse and validate using Pydantic
        try:
            plan_data = PlanData(**plan_json)
        except Exception as e:
            logger.error(f"Failed to parse plan JSON: {e}")
            raise ValueError("LLM returned invalid plan structure")

        # 6. Store Plan in database
        new_plan = Plan(
            project_id=project_id,
            task_description=task,
            plan_data=plan_data.model_dump(),
            context_files=context_files,
            confidence=0.85
        )
        
        self.db.add(new_plan)
        await self.db.commit()
        await self.db.refresh(new_plan)
        
        # 7. Return PlanResponse
        return PlanResponse(
            id=new_plan.id,
            project_id=new_plan.project_id,
            task_description=new_plan.task_description,
            plan=PlanData(**new_plan.plan_data),
            context_used=new_plan.context_files,
            confidence=new_plan.confidence,
            created_at=new_plan.created_at
        )
