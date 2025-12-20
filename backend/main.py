"""
QuantTerminal - FastAPI Application Entry Point
Production-ready async API server
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core import settings, log
from backend.db import check_db_connection, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown tasks
    """
    # Startup
    log.info(f"🚀 Starting {settings.APP_NAME}")
    log.info(f"Environment: {settings.APP_ENV}")
    
    # Check database
    db_ok = await check_db_connection()
    if not db_ok:
        log.warning("⚠️  Database connection failed on startup")
    
    # Create tables in development
    if settings.is_development:
        await create_tables()
    
    yield
    
    # Shutdown
    log.info(f"👋 Shutting down {settings.APP_NAME}")


def create_app() -> FastAPI:
    """
    Application factory
    Creates and configures FastAPI instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description="Bloomberg-style financial intelligence platform with AI integration",
        debug=settings.APP_DEBUG,
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    from backend.routes import health
    app.include_router(health.router, tags=["Health"])
    
    return app


# Create app instance
app = create_app()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running",
        "environment": settings.APP_ENV
    }
