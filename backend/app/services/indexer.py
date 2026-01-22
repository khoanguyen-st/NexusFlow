from pathlib import Path
from uuid import UUID

from app.config import get_settings

settings = get_settings()


class IndexerService:
    """Service for indexing project files."""
    
    def __init__(self):
        # TODO: Initialize embedder service
        # TODO: Get supported extensions from settings
        # TODO: Get max file size from settings
        pass
    
    async def index_project(self, project_id: UUID, project_path: str) -> int:
        """
        Index all files in a project directory.
        
        TODO: Implement this method following these steps:
        1. Get the project from database
        2. Clear existing embeddings for this project
        3. Scan directory for files using _scan_directory()
        4. For each file, call _index_file()
        5. Update project status to 'ready' and set file_count
        6. Handle errors and update status to 'error' if needed
        
        Returns:
            Number of files indexed
        """
        # TODO: Implement indexing logic
        raise NotImplementedError("Indexing not yet implemented")
    
    def _scan_directory(self, directory: str) -> list[dict]:
        """
        Scan directory for supported files.
        
        TODO: Implement file scanning:
        1. Walk through directory recursively
        2. Skip hidden files (starting with .)
        3. Skip node_modules, venv, __pycache__, .git, dist, build
        4. Filter by supported extensions (.py, .js, .ts, .tsx, .jsx, .md)
        5. Check file size (skip if > max_file_size)
        6. Return list of file info dicts with: path, relative_path, name, extension
        """
        # TODO: Implement directory scanning
        return []
    
    async def _index_file(self, db, project_id: UUID, file_info: dict) -> None:
        """
        Index a single file.
        
        TODO: Implement file indexing:
        1. Read file content (handle encoding errors)
        2. Generate embedding using embedder service
        3. Create FileEmbedding object
        4. Save to database
        """
        # TODO: Implement file indexing
        pass