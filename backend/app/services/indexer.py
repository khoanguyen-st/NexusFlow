import logging
from pathlib import Path
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_settings
from app.services.embedder import EmbedderService
from app.models import Project, FileEmbedding

settings = get_settings()
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'.py', '.ts', '.js', '.tsx', '.jsx', '.md'}
MAX_FILE_SIZE = 100 * 1024  # 100KB
SKIP_DIRS = {'node_modules', 'venv', '__pycache__', '.git', 'dist', 'build'}

class IndexerService:

    def __init__(self):
        self.embedder = EmbedderService() 
        self.allowed_extensions = ALLOWED_EXTENSIONS
        self.max_file_size = MAX_FILE_SIZE
    
    async def index_project(self, db: AsyncSession, project_id: UUID, project_path: str) -> int:
        
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        if not project:
            raise ValueError("Project not found")

        try:
            project.status = 'indexing'
            await db.commit()

            await db.execute(delete(FileEmbedding).where(FileEmbedding.project_id == project_id))
            await db.commit()
            
            files = self._scan_directory(project_path)
            
            indexed_count = 0
            for file_info in files:
                try:
                    await self._index_file(db, project_id, file_info)
                    indexed_count += 1
                except Exception as e:
                    logger.warning(f"Skipping file {file_info.get('path')}: {e}")
                    continue
            
            project.status = 'ready'
            project.file_count = indexed_count
            project.indexed_at = datetime.utcnow()
            await db.commit()
            
            return indexed_count

        except Exception as e:
            project.status = 'error'
            await db.commit()
            logger.error(f"Error: {e}")
            raise e
    
    def _scan_directory(self, directory: str) -> list[dict]:
        files_to_process = []
        base_path = Path(directory)

        if not base_path.exists() or not base_path.is_dir():
            return files_to_process

        for file_path in base_path.rglob('*'):
            if not file_path.is_file():
                continue
            path_str = str(file_path)

            if file_path.name.startswith('.'):
                continue
            if "node_modules" in path_str:
                continue
            if ".git" in path_str:
                continue
            if "venv" in path_str:
                continue
            if "__pycache__" in path_str:
                continue
            if "dist" in path_str or "build" in path_str:
                continue

            if file_path.suffix not in self.allowed_extensions:
                continue

            try:
                if file_path.stat().st_size > self.max_file_size:
                    continue
            except OSError:
                continue

            files_to_process.append({
                'path': str(file_path),
                'relative_path': str(file_path.relative_to(base_path)),
                'name': file_path.name,
                'extension': file_path.suffix
            })
        return files_to_process

    
    async def _index_file(self, db: AsyncSession, project_id: UUID, file_info: dict) -> None:
        try:
            file_path = Path(file_info['path'])
            
            content = file_path.read_text(encoding='utf-8', errors='replace')

            if not content.strip():
                return

            embedding_vector = await self.embedder.embed_text(content)

            file_embedding = FileEmbedding(
                project_id=project_id,
                file_path=file_info['relative_path'],
                file_name=file_info['name'],
                extension=file_info['extension'],
                content=content,
                embedding=embedding_vector
            )
            
            db.add(file_embedding)
            
        except Exception as e:
            logger.warning(f"Skipping file: {e}")