from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid

from app.database import Base


class Project(Base):
    """Project model representing an indexed codebase."""
    
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, indexing, ready, error
    file_count = Column(Integer, default=0)
    indexed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class FileEmbedding(Base):
    """File embedding model for vector search."""
    
    __tablename__ = "file_embeddings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    extension = Column(String(50), nullable=True)
    content = Column(Text, nullable=True)
    chunk_index = Column(Integer, default=0)
    embedding = Column(Vector(1536))  # OpenAI embedding dimension
    created_at = Column(DateTime, server_default=func.now())


class Plan(Base):
    """Generated implementation plan."""
    
    __tablename__ = "plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    task_description = Column(Text, nullable=False)
    plan_data = Column(JSONB, nullable=False)
    context_files = Column(ARRAY(Text), nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
