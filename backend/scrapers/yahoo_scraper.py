"""
YFinance Wrapper - Battle-Tested Yahoo Finance Access

Uses the yfinance library which handles:
- Rate limiting with exponential backoff
- User agent rotation
- Proper cookie handling
- Retry logic

This is MORE reliable than raw scraping.
"""

import yfinance as yf
from datetime import datetime
from typing import Dict, List
from loguru import logger as log


class YFinanceScraper:
    """Use yfinance library for reliable Yahoo Finance access"""
    
    async def get_batch(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        Fetch multiple quotes using yfinance
        
        Returns:
            {
                "AAPL": {
                    "price": 273.08,
                    "change": -0.68,
                    "change_percent": -0.25,
                    "timestamp": "2025-12-31T00:00:00",
                    "source": "yfinance"
                }
            }
        """
        try:
            # Download data for all symbols at once
            tickers = yf.Tickers(" ".join(symbols))
            
            results = {}
            for symbol in symbols:
                try:
                    ticker = tickers.tickers[symbol]
                    info = ticker.info
                    
                    # Get current price
                    current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0.0)
                    prev_close = info.get('previousClose') or info.get('regularMarketPreviousClose', 0.0)
                    
                    # Calculate change
                    change = current_price - prev_close if current_price and prev_close else 0.0
                    change_percent = (change / prev_close * 100) if prev_close else 0.0
                    
                    results[symbol.upper()] = {
                        "symbol": symbol.upper(),
                        "price": float(current_price),
                        "change": float(change),
                        "change_percent": float(change_percent),
                        "open": float(info.get('regularMarketOpen', 0.0)),
                        "high": float(info.get('regularMarketDayHigh', 0.0)),
                        "low": float(info.get('regularMarketDayLow', 0.0)),
                        "previous_close": float(prev_close),
                        "timestamp": datetime.utcnow().isoformat(),
                        "source": "yfinance"
                    }
                    
                except Exception as e:
                    log.warning(f"⚠️ Failed to get {symbol}: {e}")
                    continue
            
            log.info(f"✅ YFinance: Fetched {len(results)}/{len(symbols)} quotes")
            return results
            
        except Exception as e:
            log.error(f"❌ YFinance batch failed: {e}")
            return {}
    
    async def get_single(self, symbol: str) -> Dict:
        """Get single quote"""
        results = await self.get_batch([symbol])
        return results.get(symbol.upper(), {})
    
    async def close(self):
        """Cleanup (yfinance doesn't need cleanup)"""
        pass
