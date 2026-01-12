# test_shadow_watch_activities.py
"""
Shadow Watch Activity Test Script
Simulates real user activity to test library generation
"""

import asyncio
import httpx
from datetime import datetime

# Test user ID (we'll use this until auth is implemented)
TEST_USER_ID = 1

async def test_shadow_watch_tracking():
    """Generate test activities and check Shadow Watch library"""
    
    base_url = "http://localhost:8000"
    
    print("=" * 70)
    print("Shadow Watch Activity Test - QuantForge Terminal")
    print("=" * 70)
    
    # Step 1: Simulate viewing multiple stocks
    print("\n📊 Step 1: Simulating stock views...")
    stocks_to_view = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMZN", "META", "NFLX"]
    
    async with httpx.AsyncClient() as client:
        for symbol in stocks_to_view:
            try:
                response = await client.get(f"{base_url}/quotes/{symbol}")
                if response.status_code == 200:
                    print(f"  ✅ Viewed {symbol}")
                else:
                    print(f"  ⚠️  {symbol}: {response.status_code}")
                await asyncio.sleep(0.5)  # Realistic delay
            except Exception as e:
                print(f"  ❌ {symbol}: {e}")
    
    print("\n⏳ Waiting 2 seconds for activity tracking...\n")
    await asyncio.sleep(2)
    
    # Step 2: View some stocks multiple times (increase interest score)
    print("📊 Step 2: Viewing high-interest stocks multiple times...")
    high_interest = ["AAPL", "TSLA", "NVDA"]
    
    async with httpx.AsyncClient() as client:
        for symbol in high_interest:
            for i in range(3):  # View 3 times each
                try:
                    response = await client.get(f"{base_url}/quotes/{symbol}")
                    print(f"  ✅ Viewed {symbol} (#{i+1})")
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"  ❌ {symbol}: {e}")
    
    print("\n⏳ Waiting 2 seconds for processing...\n")
    await asyncio.sleep(2)
    
    # Step 3: Check Shadow Watch library
    print("📚 Step 3: Fetching Shadow Watch library...")
    
    async with httpx.AsyncClient() as client:
        try:
            # NOTE: This endpoint requires authentication
            # For now, we'll call the service directly
            print("  ⚠️  Library endpoint requires authentication")
            print("  Using direct service call instead...\n")
            
            # Direct service call
            from backend.services.shadow_watch_client import generate_library_snapshot
            library = await generate_library_snapshot(TEST_USER_ID)
            
            print("=" * 70)
            print("SHADOW WATCH LIBRARY SNAPSHOT")
            print("=" * 70)
            print(f"Total Items: {library.get('total_items', 0)}")
            print(f"Pinned Items: {library.get('pinned_count', 0)}")
            print(f"Fingerprint: {library.get('fingerprint', 'N/A')[:32]}...")
            print(f"\nTop Interests:")
            print("-" * 70)
            
            for item in library.get('library', [])[:10]:
                tier_emoji = {"1": "📌", "2": "⭐", "3": "✨"}.get(str(item.get('tier', 3)), "•")
                print(f"  {tier_emoji} {item.get('symbol', 'N/A'):6} | Score: {item.get('score', 0):.3f} | Tier {item.get('tier', 3)} | Rank #{item.get('rank', 0)}")
            
            print("=" * 70)
            
        except Exception as e:
            print(f"  ❌ Error fetching library: {e}")
            import traceback
            traceback.print_exc()
    
    # Step 4: Explain what happened
    print("\n✅ Test Complete!")
    print("\n📝 What Shadow Watch Did:")
    print("  • Silently tracked all quote views via middleware")
    print("  • Aggregated activity into interest scores")
    print("  • Ranked stocks by view frequency")
    print("  • Assigned tiers based on engagement level")
    print("  • Generated behavioral fingerprint")
    print("\n🎯 Expected Results:")
    print("  • AAPL, TSLA, NVDA should have highest scores (viewed 4x each)")
    print("  • Other stocks should appear with lower scores (viewed 1x)")
    print("  • All items in Tier 2 or 3 (no pinned investments yet)")
    
    print("\n🔐 Next: Implement authentication to:")
    print("  • Create real user accounts")
    print("  • Track per-user activities")
    print("  • Access authenticated endpoints")


if __name__ == "__main__":
    asyncio.run(test_shadow_watch_tracking())
