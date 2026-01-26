from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy import String, Text, Integer, Float, DateTime, text, ForeignKey, UniqueConstraint
from app.config import get_settings
from datetime import datetime
import uuid
from pgvector.sqlalchemy import Vector
from typing import Any

settings = get_settings()

# Convert postgresql:// to postgresql+asyncpg:// for async
database_url = settings.database_url.replace(
    "postgresql://", "postgresql+asyncpg://"
)

engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass

class Project(Base):
    """ class for projects table """
    __tablename__ = "projects"
    
    # id UUID PRIMARY KEY DEFAULT gen_random_uuid()
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("gen_random_uuid()") 
    )

    # name VARCHAR(255) NOT NULL
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # path VARCHAR(500) NOT NULL
    path: Mapped[str] = mapped_column(String(500), nullable=False)

    # description TEXT
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # status VARCHAR(50) DEFAULT 'pending'
    status: Mapped[str] = mapped_column(
        String(50), 
        server_default="pending", 
        default="pending" 
    )

    # file_count INTEGER DEFAULT 0
    file_count: Mapped[int] = mapped_column(
        Integer, 
        server_default=text("0"), 
        default=0
    )

    # indexed_at TIMESTAMP
    indexed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    # updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=text("CURRENT_TIMESTAMP"), 
        onupdate=datetime.now,
        nullable=False
    )

class FileEmbedding(Base):
    """ class for file_embeddings table """
    __tablename__ = "file_embeddings"
    
    # UNIQUE(project_id, file_path, chunk_index)
    __table_args__ = (
        UniqueConstraint('project_id', 'file_path', 'chunk_index', name='uq_project_file_chunk'),
    )
    
    # id UUID PRIMARY KEY DEFAULT gen_random_uuid()
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("gen_random_uuid()") 
    )
    
    # project_id UUID REFERENCES projects(id) ON DELETE CASCADE
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # file_path VARCHAR(500) NOT NULL
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # file_name VARCHAR(255) NOT NULL
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # extension VARCHAR(50)
    extension: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # content TEXT
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # chunk_index INTEGER DEFAULT 0
    chunk_index: Mapped[int] = mapped_column(
        Integer, 
        server_default=text("0"), 
        default=0
    )
    
    # embedding vector(1536)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
    
class Plan(Base):
    """ class for Plans table """
    
    # id UUID PRIMARY KEY DEFAULT gen_random_uuid()
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("gen_random_uuid()") 
    )
    
    # project_id UUID REFERENCES projects(id) ON DELETE CASCADE
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # task_description TEXT NOT NULL
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # plan_data JSONB NOT NULL
    plan_data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    
    # context_files TEXT[]
    context_files: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    
    # confidence FLOAT
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

async def get_db() -> AsyncSession:
    """Dependency to get database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
