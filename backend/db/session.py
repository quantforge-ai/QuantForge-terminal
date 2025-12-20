"""
QuantTerminal Database Session Management
Async SQLAlchemy engine and session factory
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.core.config import settings
from backend.core.logger import log


# Create async engine
# Note: asyncpg requires SSL params in connect_args, not in URL
engine_url = settings.DATABASE_URL
if "?" in engine_url:
    # Strip query parameters from URL
    engine_url = engine_url.split("?")[0]

engine = create_async_engine(
    engine_url,
    echo=settings.APP_DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10,
    connect_args={
        "ssl": "require",  # Force SSL connection
        "server_settings": {
            "application_name": settings.APP_NAME
        }
    }
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Declarative base for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency for FastAPI routes to get database session
    
    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def check_db_connection() -> bool:
    """
    Test database connectivity
    
    Returns:
        True if database is reachable, False otherwise
    """
    try:
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        log.info("✅ Database connection successful")
        return True
    except Exception as e:
        log.error(f"❌ Database connection failed: {e}")
        return False


async def create_tables():
    """
    Create all database tables (development only)
    In production, use Alembic migrations instead
    """
    if not settings.is_production:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        log.info("✅ Database tables created")
