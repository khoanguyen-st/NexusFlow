import os
from pathlib import Path
from uuid import UUID
from datetime import datetime

from app.config import get_settings
from app.database import async_session_maker
from app.models import Project, FileEmbedding
from app.services.embedder import EmbedderService
from sqlalchemy import select, delete

settings = get_settings()


class IndexerService:
    """Service for indexing project files."""
    
    def __init__(self):
        self.embedder = EmbedderService()
        self.supported_extensions = set(settings.supported_extensions)
        self.max_file_size = settings.max_file_size_kb * 1024  # Convert to bytes
    
    async def index_project(self, project_id: UUID, project_path: str) -> int:
        """
        Index all files in a project directory.
        
        Args:
            project_id: UUID of the project
            project_path: Path to the project directory
            
        Returns:
            Number of files indexed
        """
        async with async_session_maker() as db:
            try:
                # Get project
                result = await db.execute(select(Project).where(Project.id == project_id))
                project = result.scalar_one_or_none()
                
                if not project:
                    return 0
                
                # Clear existing embeddings
                await db.execute(
                    delete(FileEmbedding).where(FileEmbedding.project_id == project_id)
                )
                
                # Scan and index files
                files = self._scan_directory(project_path)
                indexed_count = 0
                
                for file_info in files:
                    try:
                        await self._index_file(db, project_id, file_info)
                        indexed_count += 1
                    except Exception as e:
                        print(f"Error indexing {file_info['path']}: {e}")
                        continue
                
                # Update project status
                project.status = "ready"
                project.file_count = indexed_count
                project.indexed_at = datetime.utcnow()
                await db.commit()
                
                return indexed_count
                
            except Exception as e:
                # Update project status to error
                project.status = "error"
                await db.commit()
                raise e
    
    def _scan_directory(self, directory: str) -> list[dict]:
        """Scan directory for supported files."""
        files = []
        root_path = Path(directory)
        
        if not root_path.exists():
            return files
        
        for file_path in root_path.rglob("*"):
            # Skip directories
            if file_path.is_dir():
                continue
            
            # Skip hidden files and directories
            if any(part.startswith(".") for part in file_path.parts):
                continue
            
            # Skip node_modules, venv, etc.
            skip_dirs = {"node_modules", "venv", ".venv", "__pycache__", ".git", "dist", "build"}
            if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                continue
            
            # Check extension
            if file_path.suffix.lower() not in self.supported_extensions:
                continue
            
            # Check file size
            try:
                if file_path.stat().st_size > self.max_file_size:
                    continue
            except OSError:
                continue
            
            files.append({
                "path": str(file_path),
                "relative_path": str(file_path.relative_to(root_path)),
                "name": file_path.name,
                "extension": file_path.suffix.lower(),
            })
        
        return files
    
    async def _index_file(self, db, project_id: UUID, file_info: dict) -> None:
        """Index a single file."""
        # Read file content
        try:
            with open(file_info["path"], "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with latin-1 as fallback
            with open(file_info["path"], "r", encoding="latin-1") as f:
                content = f.read()
        
        if not content.strip():
            return
        
        # Generate embedding
        embedding = await self.embedder.embed_text(content)
        
        # Store in database
        file_embedding = FileEmbedding(
            project_id=project_id,
            file_path=file_info["relative_path"],
            file_name=file_info["name"],
            extension=file_info["extension"],
            content=content[:5000],  # Store first 5000 chars for context
            chunk_index=0,
            embedding=embedding,
        )
        
        db.add(file_embedding)
        await db.commit()
