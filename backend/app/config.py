from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://nexusflow:nexusflow123@localhost:5432/nexusflow"
    
    # LLM Provider
    llm_provider: str = "openai"  # "openai" or "gemini"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    
    # Embedding settings
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1500
    
    # LLM settings
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 4096
    
    # Indexing settings
    supported_extensions: list[str] = [
        ".py", ".js", ".ts", ".tsx", ".jsx",
        ".java", ".go", ".rs", ".cpp", ".c", ".h",
        ".md", ".txt", ".json", ".yaml", ".yml"
    ]
    max_file_size_kb: int = 100  # Skip files larger than this
    chunk_size: int = 1000  # Characters per chunk
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()\
    