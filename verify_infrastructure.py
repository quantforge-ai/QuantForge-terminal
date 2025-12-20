#!/usr/bin/env python3
"""
QuantTerminal Infrastructure Verification Script
Tests connectivity to all production services before Phase 1
"""

import asyncio
import sys

# Check if dependencies are installed
try:
    import asyncpg
    import redis.asyncio as redis
    import boto3
    from pydantic_settings import BaseSettings
    from pydantic import ConfigDict
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\nInstall requirements first:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


class Settings(BaseSettings):
    """Load settings from .env file"""
    DATABASE_URL: str
    REDIS_URL: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str
    R2_ENDPOINT_URL: str
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Allow extra fields in .env without validation errors
    )


async def verify_postgres(db_url: str) -> bool:
    """Test PostgreSQL connection"""
    try:
        conn = await asyncpg.connect(db_url)
        version = await conn.fetchval('SELECT version()')
        await conn.close()
        print(f"✅ PostgreSQL: Connected")
        print(f"   {version[:60]}...")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL: Failed")
        print(f"   Error: {e}")
        return False


async def verify_redis(redis_url: str) -> bool:
    """Test Redis connection"""
    try:
        r = redis.from_url(redis_url, decode_responses=True)
        result = await r.ping()
        await r.close()
        print(f"✅ Redis: Connected (Ping = {result})")
        return True
    except Exception as e:
        print(f"❌ Redis: Failed")
        print(f"   Error: {e}")
        return False


def verify_r2(access_key: str, secret_key: str, endpoint: str, bucket: str) -> bool:
    """Test Cloudflare R2 connection"""
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        s3.head_bucket(Bucket=bucket)
        print(f"✅ Cloudflare R2: Connected")
        print(f"   Bucket '{bucket}' accessible")
        return True
    except Exception as e:
        print(f"❌ Cloudflare R2: Failed")
        print(f"   Error: {e}")
        return False


async def main():
    """Run all verification checks"""
    print("=" * 60)
    print("QuantTerminal - Infrastructure Verification")
    print("=" * 60)
    print()
    
    # Load settings
    try:
        settings = Settings()
    except Exception as e:
        print(f"❌ Failed to load .env file: {e}")
        print("\nMake sure .env exists and contains all required values")
        print("Run: python setup.py")
        sys.exit(1)
    
    # Run verification checks
    results = []
    
    print("Testing Database Connection...")
    results.append(await verify_postgres(settings.DATABASE_URL))
    print()
    
    print("Testing Cache Connection...")
    results.append(await verify_redis(settings.REDIS_URL))
    print()
    
    print("Testing Object Storage...")
    results.append(verify_r2(
        settings.R2_ACCESS_KEY_ID,
        settings.R2_SECRET_ACCESS_KEY,
        settings.R2_ENDPOINT_URL,
        settings.R2_BUCKET_NAME
    ))
    print()
    
    # Summary
    print("=" * 60)
    if all(results):
        print("🎉 All infrastructure verified successfully!")
        print("=" * 60)
        print()
        print("✅ Phase 0 Complete - Ready for Phase 1")
        print()
        print("Next: Backend core development")
        print("  - Create FastAPI application structure")
        print("  - Implement database models")
        print("  - Set up authentication")
        print("  - Build API routes")
        return 0
    else:
        print("⚠️  Some components failed verification")
        print("=" * 60)
        print()
        print("Review errors above and update .env with correct credentials")
        print("See: phase0_setup_guide.md for setup instructions")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
