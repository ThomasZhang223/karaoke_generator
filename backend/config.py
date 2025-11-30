"""
Backend configuration settings.
Environment variables and application configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    api_title: str = "Karaoke Video Generator API"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS settings
    cors_origins: list[str] = ["http://localhost:5173"]
    
    # File paths
    upload_dir: str = "uploads"
    output_dir: str = "output"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()

