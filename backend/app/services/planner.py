from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.schemas import PlanResponse

settings = get_settings()

# TODO: Create a prompt template for plan generation
# The prompt should:
# 1. Ask LLM to analyze codebase context
# 2. Generate implementation plan with: summary, affected_files, steps, reusable_components
# 3. Request response in JSON format
PLAN_GENERATION_PROMPT = """
TODO: Design your prompt template here.

Hint: Include placeholders for {task} and {context}
"""

class PlannerService:
    """Service for generating implementation plans using AI."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        # TODO: Initialize OpenAI or Gemini client based on settings
    
    async def generate_plan(
        self,
        project_id: UUID,
        task: str,
    ) -> PlanResponse:
        """
        Generate an implementation plan for a task.
        
        TODO: Implement this method:
        1. Verify project exists and status is 'ready'
        2. Search for relevant files using SearcherService (top 10 results)
        3. Build context string from search results
        4. Format prompt with task and context
        5. Call LLM (OpenAI or Gemini) to generate plan
        6. Parse JSON response into plan_data
        7. Store Plan in database
        8. Return PlanResponse
        
        Response should include:
        - summary, affected_files, steps, reusable_components
        - context_used (list of file paths)
        - confidence score
        """
        # TODO: Implement plan generation
        raise NotImplementedError("Plan generation not yet implemented")
