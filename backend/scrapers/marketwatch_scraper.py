"""
MarketWatch Scraper - Real-Time Backup

Scrapes MarketWatch's website which often shows real-time data
- Speed: ~2-3 seconds
- Delay: Often real-time or <1 min!
- Rate Limit: ~50 req/min safe
"""

import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict
from loguru import logger as log


class MarketWatchScraper:
    """Scrape MarketWatch for often-realtime quotes"""
    
    BASE_URL = "https://www.marketwatch.com/investing/stock"
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=5.0,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
    
    async def get_single(self, symbol: str) -> Dict:
        """
        Scrape single stock (MarketWatch is slow for batch)
        
        Returns quote dict or empty dict on failure
        """
        try:
            url = f"{self.BASE_URL}/{symbol.lower()}"
            response = await self.client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Parse price (class: "intraday__price")
            price_elem = soup.find('bg-quote', {'class': 'value'})
            change_elem = soup.find('bg-quote', {'class': 'change--point--q'})
            change_pct_elem = soup.find('bg-quote', {'class': 'change--percent--q'})
            
            if not price_elem:
                log.warning(f"⚠️ MarketWatch: No price found for {symbol}")
                return {}
            
            price = float(price_elem.text.strip().replace('$', '').replace(',', ''))
            change = float(change_elem.text.strip().replace('$', '').replace(',', '')) if change_elem else 0.0
            change_pct_str = change_pct_elem.text.strip().replace('%', '') if change_pct_elem else '0'
            change_pct = float(change_pct_str)
            
            return {
                "symbol": symbol.upper(),
                "price": price,
                "change": change,
                "change_percent": change_pct,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "marketwatch"
            }
            
        except Exception as e:
            log.error(f"❌ MarketWatch scraper failed for {symbol}: {e}")
            return {}
    
    async def get_batch(self, symbols: list) -> Dict[str, Dict]:
        """Batch fetch (sequential - slow)"""
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
