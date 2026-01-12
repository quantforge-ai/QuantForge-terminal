"""
QuantTerminal - FastAPI Application Entry Point
Production-ready async API server
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.core import settings, log
from backend.db import check_db_connection, create_tables
from shadowwatch import ShadowWatch
from backend.services.shadow_watch_client import set_shadow_watch_instance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown tasks
    """
    # Startup
    log.info("🚀 QuantTerminal API - Starting Up")
    log.info(f"Server environment: {settings.APP_ENV}")
    
    # Initialize Shadow Watch Package 🌑
    log.info("🌑 Initializing Shadow Watch...")
    shadow_watch = ShadowWatch(
        database_url=settings.DATABASE_URL,
        redis_url=settings.REDIS_URL if settings.REDIS_URL else None,
        license_key=None  # Local dev mode first, then add production license
    )
    
    # Initialize database tables
    try:
        await shadow_watch.init_database()
        log.info("✅ Shadow Watch tables created/verified")
    except Exception as e:
        log.warning(f"⚠️ Shadow Watch database init warning: {e}")
    
    # Set global instance for compatibility wrapper
    set_shadow_watch_instance(shadow_watch)
    log.info("✅ Shadow Watch initialized and ready")
    
    # Start background streaming tasks (Phase 3)
    import asyncio
    from backend.services.websocket_service import start_price_streaming, start_portfolio_streaming
    asyncio.create_task(start_price_streaming())
    asyncio.create_task(start_portfolio_streaming())
    log.info("📡 WebSocket streaming tasks started")

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
    
    # Shadow Watch Middleware - Silent activity tracking 🌑
    @app.middleware("http")
    async def shadow_watch_middleware(request: Request, call_next):
        """
        Silently track user activity for Shadow Watch library
        Runs AFTER response to avoid blocking user requests
        """
        response = await call_next(request)
        
        # Track only successful GET requests to quote endpoints
        if (
            request.method == "GET" 
            and request.url.path.startswith("/quotes/") 
            and response.status_code == 200
        ):
            # Extract symbol from URL path
            path_parts = request.url.path.split("/")
            if len(path_parts) >= 3:
                symbol = path_parts[2].upper()
                
                # Basic validation (symbol should be short)
                if 1 <= len(symbol) <= 10 and symbol.isalpha():
                    # TODO: Extract user_id from JWT token (when auth integrated)
                    user_id = 1  # Placeholder for now
                    
                    # Track asynchronously (fire and forget)
                    import asyncio
                    from backend.services.shadow_watch_client import track_activity
                    
                    asyncio.create_task(
                        track_activity(
                            user_id=user_id,
                            symbol=symbol,
                            action="view",
                            event_metadata={"source": "quote_api"}
                        )
                    )
        
        return response
    
    # Include routers
    try:
        from backend.routes import health, auth, quotes, shadow_watch, paper_trading, news, indicators, websocket, search, market_movers, historical
        log.info("✅ Successfully imported all routers")
        app.include_router(health.router, tags=["Health"])
        log.info("✅ Health router registered")
        app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
        log.info(f"✅ Auth router registered")
        app.include_router(quotes.router, tags=["Quotes"])
        log.info("✅ Quotes router registered")
        app.include_router(shadow_watch.router, prefix="/shadow-watch", tags=["Shadow Watch 🌑"])
        log.info("✅ Shadow Watch router registered")
        app.include_router(paper_trading.router, prefix="/paper-trading", tags=["Paper Trading 📈"])
        log.info("✅ Paper Trading router registered")
        app.include_router(news.router, prefix="/news", tags=["News 📰"])
        log.info("✅ News router registered")
        app.include_router(indicators.router, prefix="/indicators", tags=["Indicators 📊"])
        log.info("✅ Indicators router registered")
        app.include_router(websocket.router, tags=["WebSocket 🔌"])
        log.info("✅ WebSocket router registered")
        app.include_router(search.router, tags=["Search 🔍"])
        log.info("✅ Search router registered")
        app.include_router(market_movers.router, tags=["Market Movers 📈"])
        log.info("✅ Market Movers router registered")
        app.include_router(historical.router, tags=["Historical Data 📋"])
        log.info("✅ Historical Data router registered")
    except Exception as e:
        log.error(f"❌ Error loading routers: {e}")
        import traceback
        log.error(traceback.format_exc())
    
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
        "environment": settings.APP_ENV,
        "powered_by": {
            "name": "Shadow Watch",
            "version": "0.3.0",
            "description": "Behavioral intelligence for financial applications",
            "github": "https://github.com/Tanishq1030/Shadow_Watch",
            "pypi": "https://pypi.org/project/shadowwatch/",
            "tagline": "Always there. Never seen. Forever watching. 🌑"
        }
    }
