import logging
import asyncio
from pathlib import Path
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_settings
from app.services.embedder import EmbedderService
from app.models.models import Project, FileEmbedding

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
            
            semaphore = asyncio.Semaphore(5)

            async def process_wrapper(file_info):
                async with semaphore:
                    return await self._create_embedding_data(project_id, file_info)

            tasks = [process_wrapper(f) for f in files]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
            indexed_count = 0
            for res in results:
                if isinstance(res, Exception):
                    logger.warning(f"File processing failed: {res}")
                    continue
                if res is None:
                    continue
                
                db.add(res)
                indexed_count += 1
            
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

            if any(skip_dir in path_str for skip_dir in SKIP_DIRS):
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

    async def _create_embedding_data(self, project_id: UUID, file_info: dict) -> FileEmbedding | None:

        try:
            file_path = Path(file_info['path'])
            content = file_path.read_text(encoding='utf-8', errors='replace')

            if not content.strip():
                return None

            embedding_vector = await self.embedder.embed_text(content)

            return FileEmbedding(
                project_id=project_id,
                file_path=file_info['relative_path'],
                file_name=file_info['name'],
                extension=file_info['extension'],
                content=content,
                embedding=embedding_vector
            )
        except Exception as e:
            logger.warning(f"Failed to process {file_info.get('path')}: {e}")
            return None