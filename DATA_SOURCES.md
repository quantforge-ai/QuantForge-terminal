# Main Dashboard - Data Sources

## Current Data Status: **ALL DUMMY DATA** 🔴

### Widgets Using Mock Data

#### 1. FlipBoard Ticker Train ❌ DUMMY
**Source**: `data/ticker_data.py` → `TICKER_DATA` dictionary
- **Static hardcoded strings** like:
  ```python
  "STOCKS": "📊 STOCKS [IST] | 15:54 AAPL 185.20 +1.2% | 15:54 MSFT 412.50 +0.8%..."
  ```
- **NOT live data** - just pre-formatted text
- **NO API calls** to backend or yfinance

---

#### 2. HeatGrid Widget ❌ DUMMY
**Source**: `widgets/heatgrid.py` → `random.uniform()`
- **Mock percentages**: `change_pct = random.uniform(-5.0, 5.0)`
- **NO real quotes** from backend
- **Symbols are real** (AAPL, MSFT, etc.) but prices are fake

```python
async def refresh_data(self) -> None:
    """Fetch real-time data from yfinance (mock for now)"""
    import random
    
    for symbol, emoji in symbols:
        # Mock data: random percentage between -5% and +5%
        change_pct = random.uniform(-5.0, 5.0)  # 🔴 FAKE
        self.quote_data[symbol] = change_pct
```

---

#### 3. NewsTrain Widget ❌ DUMMY
**Source**: `widgets/news_train.py` → `NEWS_DATA` dictionary
- **Hardcoded headlines** per mode:
  ```python
  "STOCKS": [
      "📰 Fed signals potential rate cuts in 2026...",
      "📰 Tech stocks rally as AI earnings beat...",
      "📰 S&P 500 reaches new all-time high..."
  ]
  ```
- **NO RSS feed** integration yet
- **NOT live news**

---

#### 4. Portfolio Panel ❌ DUMMY
**Source**: `widgets/portfolio.py` → `build_portfolio_widget()`
- **Hardcoded values**:
  - Balance: $100,000
  - P&L: +$2,450 (+2.4%)
  - Holdings: Static list
- **NO connection** to backend portfolio service

---

## Integration Points (Ready but Not Connected)

### Backend Services Available ✅
Your backend already has these services ready:

1. **Quote Service** (`backend/services/quote_service.py`)
   - `get_batch_quotes()` - fetch multiple symbols
   - `get_single_quote()` - fetch one symbol
   - Uses yfinance with Redis caching

2. **Portfolio Service** (`backend/services/portfolio_service.py`)
   - Get holdings, P&L, balance
   - Real paper trading data

3. **WebSocket Service** (`backend/services/websocket_service.py`)
   - Real-time price updates
   - Portfolio change notifications

---

## How to Connect Real Data

### Step 1: FlipBoard → Backend Quote Service

```python
# In widgets/flipboard.py
import httpx

async def update_ticker(self) -> None:
    """Fetch real quotes from backend"""
    # Get top symbols for mode
    symbols = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
    
    # Call backend
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/quotes/batch",
            json={"symbols": symbols}
        )
        quotes = response.json()
    
    # Build ticker string from real data
    ticker_parts = []
    for symbol, data in quotes.items():
        price = data['price']
        change_pct = data['change_percent']
        ticker_parts.append(f"{symbol} {price} {change_pct:+.1f}%")
    
    self.current_ticker = " | ".join(ticker_parts)
```

### Step 2: HeatGrid → Backend Quote Service

```python
# In widgets/heatgrid.py
async def refresh_data(self) -> None:
    """Fetch real-time data from backend"""
    symbols = [s for s, _ in self.GRID_SYMBOLS[self.mode]]
    
    # Replace random.uniform() with API call
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/quotes/batch",
            json={"symbols": symbols}
        )
        quotes = response.json()
    
    for symbol, data in quotes.items():
        change_pct = data.get('change_percent', 0.0)  # Real data!
        self.quote_data[symbol] = change_pct
        
        # Update button
        btn = self.query_one(f"#grid-{symbol}", Button)
        btn.label = self._format_cell(symbol, emoji, change_pct)
```

### Step 3: NewsTrain → RSS Feed

```python
# In widgets/news_train.py
import feedparser

async def fetch_news(self):
    """Fetch real RSS headlines"""
    feed_urls = {
        "STOCKS": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "CRYPTO": "https://cointelegraph.com/rss",
        "FOREX": "https://www.forexlive.com/feed/news",
        # ... other modes
    }
    
    feed = feedparser.parse(feed_urls[self.mode])
    headlines = [f"📰 {entry.title}" for entry in feed.entries[:3]]
    return headlines
```

### Step 4: Portfolio → Backend Service

```python
# In widgets/portfolio.py
async def build_portfolio_widget() -> Text:
    """Fetch real portfolio from backend"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/portfolio/summary",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        portfolio_data = response.json()
    
    # Build widget from real data
    balance = portfolio_data['total_value']
    pnl = portfolio_data['total_pnl']
    pnl_pct = portfolio_data['pnl_percent']
    holdings = portfolio_data['holdings'][:5]
    
    # ... render with real values
```

---

## Summary

| Widget | Current Status | Data Source | Integration Effort |
|--------|----------------|-------------|-------------------|
| FlipBoard | ❌ DUMMY | Hardcoded strings | ~30 min (backend call) |
| HeatGrid | ❌ DUMMY | `random.uniform()` | ~30 min (backend call) |
| NewsTrain | ❌ DUMMY | Hardcoded headlines | ~45 min (RSS parsing) |
| Portfolio | ❌ DUMMY | Hardcoded values | ~30 min (backend call) |

**Total Integration Time**: ~2-3 hours to wire all widgets to live data

---

## Decision Point

**Option 1**: Keep dummy data for UI/UX development (current)
- Fast iteration
- No backend dependency
- Visual design perfection

**Option 2**: Integrate live data now
- Requires backend running (`uvicorn main:app`)
- Add `httpx` for async HTTP calls
- Wire all 4 widgets to APIs
- ~2-3 hours work

**Recommendation**: 
Since we're "almost done with main dashboard" (UI complete), next logical step is **Option 2** - integrate live data from your backend. The backend services are already built, just need to connect the dots.

Want me to wire the live data integration?
