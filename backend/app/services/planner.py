import json
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from openai import AsyncOpenAI
import google.generativeai as genai

from app.config import get_settings
from app.models import Project, Plan
from app.schemas import PlanResponse, PlanData
from app.services.searcher import SearcherService

settings = get_settings()

PLAN_GENERATION_PROMPT = """You are an expert software architect. Analyze the provided codebase context and generate a detailed implementation plan for the given task.

## Task
{task}

## Codebase Context
The following files are relevant to this task:

{context}

## Instructions
Based on the codebase context, create a detailed implementation plan. Your response must be valid JSON with the following structure:

{{
    "summary": "Brief summary of what needs to be done",
    "affected_files": [
        {{"path": "path/to/file.py", "action": "modify|create|delete"}}
    ],
    "steps": [
        {{"order": 1, "description": "What to do", "file": "path/to/file.py"}}
    ],
    "reusable_components": [
        {{"name": "function_name", "location": "path/to/file.py", "description": "How it can be reused"}}
    ]
}}

Focus on:
1. Identifying all files that need to be modified or created
2. Providing step-by-step implementation instructions
3. Finding existing components that can be reused
4. Following the existing code patterns and conventions

Respond ONLY with valid JSON, no additional text."""


class PlannerService:
    """Service for generating implementation plans using AI."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.provider = settings.llm_provider
        
        if self.provider == "openai":
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        else:
            genai.configure(api_key=settings.gemini_api_key)
    
    async def generate_plan(
        self,
        project_id: UUID,
        task: str,
    ) -> PlanResponse:
        """
        Generate an implementation plan for a task.
        
        Args:
            project_id: UUID of the project
            task: Task description
            
        Returns:
            Generated plan response
        """
        # Verify project exists and is indexed
        result = await self.db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        
        if not project:
            raise ValueError("Project not found")
        
        if project.status != "ready":
            raise ValueError("Project is not indexed yet")
        
        # Search for relevant context
        searcher = SearcherService(self.db)
        search_results = await searcher.search(
            project_id=project_id,
            query=task,
            top_k=10,
        )
        
        # Build context from search results
        context = self._build_context(search_results)
        context_files = [r.file_path for r in search_results]
        
        # Generate plan using LLM
        prompt = PLAN_GENERATION_PROMPT.format(task=task, context=context)
        
        if self.provider == "openai":
            plan_data, confidence = await self._generate_openai(prompt)
        else:
            plan_data, confidence = await self._generate_gemini(prompt)
        
        # Store plan in database
        plan = Plan(
            project_id=project_id,
            task_description=task,
            plan_data=plan_data,
            context_files=context_files,
            confidence=confidence,
        )
        
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        
        return PlanResponse(
            id=plan.id,
            project_id=plan.project_id,
            task_description=plan.task_description,
            plan=PlanData(**plan_data),
            context_used=context_files,
            confidence=confidence,
            created_at=plan.created_at,
        )
    
    def _build_context(self, search_results) -> str:
        """Build context string from search results."""
        context_parts = []
        
        for result in search_results:
            context_parts.append(f"""
### File: {result.file_path}
```
{result.content}
```
""")
        
        return "\n".join(context_parts)
    
    async def _generate_openai(self, prompt: str) -> tuple[dict, float]:
        """Generate plan using OpenAI."""
        response = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": "You are an expert software architect. Always respond with valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            response_format={"type": "json_object"},
        )
        
        content = response.choices[0].message.content
        plan_data = json.loads(content)
        
        # Simple confidence based on context match
        confidence = min(0.9, 0.5 + len(plan_data.get("affected_files", [])) * 0.1)
        
        return plan_data, confidence
    
    async def _generate_gemini(self, prompt: str) -> tuple[dict, float]:
        """Generate plan using Gemini."""
        import asyncio
        
        def _generate():
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=settings.llm_temperature,
                    max_output_tokens=settings.llm_max_tokens,
                ),
            )
            return response.text
        
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, _generate)
        
        # Parse JSON from response
        # Try to extract JSON if there's extra text
        try:
            plan_data = json.loads(content)
        except json.JSONDecodeError:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                plan_data = json.loads(json_match.group())
            else:
                raise ValueError("Failed to parse plan from LLM response")
        
        confidence = min(0.9, 0.5 + len(plan_data.get("affected_files", [])) * 0.1)
        
        return plan_data, confidence
