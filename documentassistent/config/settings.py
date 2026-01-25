"""Type-safe configuration models using Pydantic."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """Configuration for LLM providers."""

    provider: Literal["ollama", "openai"] = Field(
        default="ollama",
        description="LLM provider to use",
    )
    model: str = Field(
        default="gemma:7b",
        description="Model name/identifier",
    )
    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="Temperature for generation",
    )
    max_tokens: int = Field(
        default=2000,
        gt=0,
        description="Maximum tokens to generate",
    )


class PathsConfig(BaseModel):
    """Configuration for data paths."""

    data_dir: str = Field(default="data", description="Base data directory")
    pdfs_dir: str = Field(default="data/pdfs", description="PDF files directory")
    pictures_dir: str = Field(
        default="data/Pictures",
        description="Image files directory",
    )


class DatabaseConfig(BaseModel):
    """Configuration for database."""

    path: str = Field(
        default="data/extractions.db",
        description="SQLite database path",
    )


class GraphRAGConfig(BaseModel):
    """Configuration for GraphRAG (future feature)."""

    enabled: bool = Field(
        default=False,
        description="Enable GraphRAG integration",
    )
    vector_store: str = Field(
        default="chroma",
        description="Vector store backend",
    )
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model to use",
    )
    chunk_size: int = Field(
        default=512,
        gt=0,
        description="Text chunk size for embeddings",
    )


class APIConfig(BaseModel):
    """Configuration for API server (future feature)."""

    host: str = Field(
        default="0.0.0.0",  # noqa: S104
        description="API host address",
    )
    port: int = Field(
        default=8000,
        gt=0,
        lt=65536,
        description="API port number",
    )
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="CORS allowed origins",
    )


class AppConfig(BaseModel):
    """Root application configuration."""

    llm: LLMConfig = Field(default_factory=LLMConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    graphrag: GraphRAGConfig = Field(default_factory=GraphRAGConfig)
    api: APIConfig = Field(default_factory=APIConfig)


class ConfigManager:
    """Singleton configuration manager."""

    _instance: "ConfigManager | None" = None
    _config: AppConfig | None = None
    _config_path: str | None = None

    def __new__(cls) -> "ConfigManager":
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self, config_path: str = "config.yaml") -> AppConfig:
        """Load configuration from YAML file."""
        if self._config is None or self._config_path != config_path:
            config_file = Path(config_path)
            if config_file.exists():
                with config_file.open() as f:
                    data = yaml.safe_load(f) or {}
            else:
                # Use defaults if file doesn't exist
                data = {}

            self._config = AppConfig(**data)
            self._config_path = config_path

        return self._config

    def reload(self, config_path: str = "config.yaml") -> AppConfig:
        """Force reload configuration from file."""
        self._config = None
        return self.load(config_path)

    def get(self) -> AppConfig:
        """Get current configuration (loads with defaults if not loaded)."""
        if self._config is None:
            return self.load()
        return self._config

    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return self.get().model_dump()
