#!/usr/bin/env python3
"""
QuantTerminal - Initial Setup Script
Helps configure environment and generates secure secrets
"""

import secrets
import sys
from pathlib import Path

def generate_secret_key():
    """Generate a secure secret key for JWT"""
    return secrets.token_urlsafe(64)

def create_env_file():
    """Create .env from .env.example if it doesn't exist"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_example.exists():
        print("❌ .env.example not found")
        return False
    
    if env_file.exists():
        overwrite = input(".env already exists. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            print("Keeping existing .env file")
            return True
    
    # Copy .env.example to .env
    content = env_example.read_text()
    
    # Generate and replace SECRET_KEY
    secret_key = generate_secret_key()
    content = content.replace(
        "TEMPORARY_KEY_REPLACE_WITH_ACTUAL_GENERATED_SECRET",
        secret_key
    )
    
    env_file.write_text(content)
    print(f"✅ Created .env file")
    print(f"✅ Generated secure SECRET_KEY")
    
    return True

def main():
    print("=" * 60)
    print("QuantTerminal - Phase 0 Setup")
    print("=" * 60)
    print()
    
    # Step 1: Create .env
    print("Step 1: Creating .env file...")
    if not create_env_file():
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Edit .env and add your actual credentials:")
    print("   - DATABASE_URL (from Neon)")
    print("   - REDIS_URL (from Redis Cloud)")
    print("   - R2 credentials (from Cloudflare)")
    print()
    print("2. Follow phase0_setup_guide.md for infrastructure setup")
    print()
    print("3. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("4. Verify infrastructure:")
    print("   python verify_infrastructure.py")
    print()

if __name__ == "__main__":
    main()
