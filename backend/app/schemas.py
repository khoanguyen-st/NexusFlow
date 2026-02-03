from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime


class ProjectCreate(BaseModel):
    """Request model for creating a project."""
    name: str = Field(..., min_length=1, max_length=255)
    path: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    """Response model for a project."""
    id: UUID
    name: str
    path: str
    description: Optional[str]
    status: str
    file_count: int
    indexed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndexRequest(BaseModel):
    """Request model for indexing a project."""
    project_id: UUID


class IndexResponse(BaseModel):
    """Response model for indexing status."""
    project_id: UUID
    status: str
    files_indexed: int
    message: str


class SearchRequest(BaseModel):
    """Request model for semantic search."""
    project_id: UUID
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=10, ge=1, le=50)


class SearchResult(BaseModel):
    """Single search result."""
    file_path: str
    file_name: str
    content: str
    similarity: float


class SearchResponse(BaseModel):
    """Response model for search results."""
    query: str
    results: list[SearchResult]
    total: int


class PlanGenerateRequest(BaseModel):
    """Request model for generating an implementation plan."""
    project_id: UUID
    task: str = Field(..., min_length=10)


class AffectedFile(BaseModel):
    """File affected by the implementation."""
    path: str
    action: Literal["create", "modify", "delete"]


class ImplementationStep(BaseModel):
    """Single implementation step."""
    order: int
    description: str
    file: Optional[str] = None


class ReusableComponent(BaseModel):
    """Reusable component found in the codebase."""
    name: str
    location: str
    description: Optional[str] = None


class PlanData(BaseModel):
    """Generated implementation plan data."""
    summary: str
    affected_files: list[AffectedFile]
    steps: list[ImplementationStep]
    reusable_components: list[ReusableComponent]


class PlanResponse(BaseModel):
    """Response model for a generated plan."""
    id: UUID
    project_id: UUID
    task_description: str
    plan: PlanData
    context_used: list[str]
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True
