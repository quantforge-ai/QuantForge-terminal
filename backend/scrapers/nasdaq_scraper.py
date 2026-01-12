"""
NASDAQ Public Page Scraper - Direct Exchange Data

Scrapes NASDAQ's public stock pages (5-15s delay from exchange)
- Speed: ~2-3 seconds
- Delay: 5-15 seconds (direct from exchange!)
- Rate Limit: ~30 req/min safe
"""

import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict
from loguru import logger as log


class NASDAQScraper:
    """Scrape NASDAQ public pages for near-exchange quotes"""
    
    BASE_URL = "https://www.nasdaq.com/market-activity/stocks"
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=5.0,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
    
    async def get_single(self, symbol: str) -> Dict:
        """
        Scrape NASDAQ public page
        
        Returns quote dict or empty dict on failure
        """
        try:
            url = f"{self.BASE_URL}/{symbol.lower()}"
            response = await self.client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Parse last sale price
            price_elem = soup.find('span', {'class': 'symbol-page-header__pricing-price'})
            if not price_elem:
                log.warning(f"⚠️ NASDAQ: No price found for {symbol}")
                return {}
            
            price = float(price_elem.text.strip().replace('$', '').replace(',', ''))
            
            # Try to get change
            change_elem = soup.find('span', {'class': 'symbol-page-header__pricing-change'})
            change = float(change_elem.text.strip().split()[0]) if change_elem else 0.0
            
            return {
                "symbol": symbol.upper(),
                "price": price,
                "change": change,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "nasdaq"
            }
            
        except Exception as e:
            log.error(f"❌ NASDAQ scraper failed for {symbol}: {e}")
            return {}
    
    async def get_batch(self, symbols: list) -> Dict[str, Dict]:
        """Batch fetch (sequential)"""
        import asyncio
        tasks = [self.get_single(sym) for sym in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            symbols[i]: results[i] 
            for i in range(len(symbols)) 
            if not isinstance(results[i], Exception) and results[i]
        }
    
    async def close(self):
        """Cleanup"""
        await self.client.aclose()
