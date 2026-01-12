"""
Multi-Source Aggregator - YFinance Primary

Strategy: Use yfinance (battle-tested) as primary source
Backup scrapers disabled due to rate limiting/bot detection
"""

import asyncio
from datetime import datetime
from typing import Dict, List
from loguru import logger as log

from .yahoo_scraper import YFinanceScraper


class MultiSourceAggregator:
    """
    Aggregate quotes using yfinance (reliable)
    
    Strategy:
    1. Use yfinance library (handles rate limits properly)
    2. Cache aggressively (5-10s TTL in quote_service)
    3. Future: Add paid sources for premium tier
    """
    
    def __init__(self):
        self.yfinance = YFinanceScraper()
    
    async def get_batch_fast(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        Get quotes using yfinance (reliable & fast)
        
        Returns: Dict of quotes keyed by symbol
        """
        start = datetime.utcnow()
        
        # Use yfinance (handles rate limits properly)
        quotes = await self.yfinance.get_batch(symbols)
        
        elapsed = (datetime.utcnow() - start).total_seconds()
        log.info(f"✅ Aggregator: Got {len(quotes)}/{len(symbols)} quotes in {elapsed:.2f}s")
        
        return quotes
    
    async def get_single_fast(self, symbol: str) -> Dict:
        """Get single quote"""
        return await self.yfinance.get_single(symbol)
    
    async def close(self):
        """Cleanup"""
        await self.yfinance.close()
