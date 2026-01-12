"""
Services module - Business logic layer for QuantTerminal

Structure:
- user_service: User management and authentication (Phase 2A) ✅
- redis_service: Caching and session storage (Phase 2B)
- quote_service: Market data quotes (Phase 2B)
- trade_service: Paper trading execution (Phase 2D)
- news_service: Financial news aggregation (Phase 2E)
- analytics_service: Technical indicators (Phase 3)
- websocket_service: Real-time updates (Phase 2B)
- interest_engine: Silent Guardian library (Phase 2C)
- r2_service: Object storage (Phase 3)
"""
from backend.services.user_service import UserService

# Service exports (import as needed in routes)
__all__ = [
    "UserService",
    # Phase 2B+: Import these as we implement them
    # "redis_service",
    # "quote_service",
    # "websocket_service",
    # etc.
]
