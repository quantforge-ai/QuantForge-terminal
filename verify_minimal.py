#!/usr/bin/env python3
"""
QuantTerminal Infrastructure Verification Script (Minimal Version)
Tests only required services: PostgreSQL (and optionally Redis if configured)
"""

import asyncio
import sys

# Check if basic dependencies are installed
try:
    import asyncpg
    from pydantic_settings import BaseSettings
    from pydantic import ConfigDict
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\nInstall minimal requirements:")
    print("  pip install asyncpg pydantic pydantic-settings python-dotenv")
    sys.exit(1)


class Settings(BaseSettings):
    """Load settings from .env file"""
    DATABASE_URL: str
   
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Allow extra fields in .env
    )


async def verify_postgres(db_url: str) -> bool:
    """Test PostgreSQL connection"""
    try:
        # Handle SQLAlchemy format (postgresql+asyncpg://) -> asyncpg format (postgresql://)
        if "+asyncpg" in db_url:
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
        
        conn = await asyncpg.connect(db_url)
        version = await conn.fetchval('SELECT version()')
        await conn.close()
        print(f"✅ PostgreSQL: Connected")
        print(f"   {version[:80]}...")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL: Failed")
        print(f"   Error: {e}")
        return False


async def main():
    """Run verification checks"""
    print("=" * 60)
    print("QuantTerminal - Infrastructure Verification (Minimal)")
    print("=" * 60)
    print()
    
    # Load settings
    try:
        settings = Settings()
    except Exception as e:
        print(f"❌ Failed to load .env file: {e}")
        print("\nMake sure .env exists and contains DATABASE_URL")
        sys.exit(1)
    
    # Test database
    print("Testing Database Connection...")
    db_ok = await verify_postgres(settings.DATABASE_URL)
    print()
    
    # Summary
    print("=" * 60)
    if db_ok:
        print("🎉 Database verified successfully!")
        print("=" * 60)
        print()
        print("✅ Phase 0 Complete - Database Ready")
        print()
        print("Next steps:")
        print("  1. (Optional) Set up Redis and R2 for full features")
        print("  2. Proceed to Phase 1: Backend core development")
        return 0
    else:
        print("⚠️  Database verification failed")
        print("=" * 60)
        print()
        print("Check your DATABASE_URL in .env file")
        print("Format: postgresql+asyncpg://user:pass@host/db?sslmode=require")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
