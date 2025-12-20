"""
QuantTerminal Backend Core Configuration
Handles all environment variables and application settings
"""

from functools import lru_cache
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Uses Pydantic for type validation and .env file loading
    """
    
    # Application
    APP_NAME: str = "QuantTerminal"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    
    # Database (Neon PostgreSQL)
    DATABASE_URL: str
    
    # Cache (Redis) - Optional for now
    REDIS_URL: str | None = None
    
    # Object Storage (Cloudflare R2) - Optional for now
    R2_ACCESS_KEY_ID: str | None = None
    R2_SECRET_ACCESS_KEY: str | None = None
    R2_BUCKET_NAME: str | None = None
    R2_ENDPOINT_URL: str | None = None
    R2_PUBLIC_URL: str | None = None
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    # Market Data Providers (All optional - configure as needed)
    POLYGON_API_KEY: str | None = None
    FINNHUB_API_KEY: str | None = None
    ALPHA_VANTAGE_API_KEY: str | None = None
    
    # CORS & Frontend
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Allow extra fields in .env
        case_sensitive=False
    )
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.APP_ENV == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.APP_ENV == "production"
    
    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Uses lru_cache to avoid reloading .env on every call
    """
    return Settings()


# Export for easy imports
settings = get_settings()
