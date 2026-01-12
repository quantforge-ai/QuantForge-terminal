"""
News Train Widget - Mode-Aware RSS Headlines
Flip animation with 5s dwell time
"""

from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
import asyncio


class NewsTrain(Widget):
    """
    Scrolling news headlines with flip animation
    - RSS feed from CNBC (mode-aware filtering)
    - 5s dwell between headlines
    - Shows 3 headlines in rotation
    """
    
    # Mock news data per mode (TODO: Replace with real RSS)
    NEWS_DATA = {
        "STOCKS": [
            "📰 Fed signals potential rate cuts in 2026 amid cooling inflation",
            "📰 Tech stocks rally as AI earnings beat expectations",
            "📰 S&P 500 reaches new all-time high on strong economic data"
        ],
        "CRYPTO": [
            "📰 Bitcoin ETF sees record inflows as institutional adoption grows",
            "📰 Ethereum upgrade reduces gas fees by 40%",
            "📰 SEC approves new framework for crypto regulation"
        ],
        "FOREX": [
            "📰 Dollar weakens against major currencies on dovish Fed comments",
            "📰 ECB maintains rates as Eurozone inflation moderates",
            "📰 Yuan strengthens as China economic data exceeds forecasts"
        ],
        "COMMODITIES": [
            "📰 Gold hits $2,100 as safe-haven demand surges",
            "📰 Oil prices steady amid OPEC+ production cuts",
            "📰 Copper rallies on infrastructure spending optimism"
        ],
        "INDICES": [
            "📰 Global markets mixed as investors await earnings season",
            "📰 Nikkei 225 closes at 10-year high on weak yen",
            "📰 Emerging market indices outperform developed markets"
        ]
    }
    
    current_headline = reactive("")
    headline_index = reactive(0)
    mode = reactive("STOCKS")
    
    DEFAULT_CSS = """
    NewsTrain {
        height: 1;
        background: #121212;
        padding: 0;  /* Removed padding */
        color: #888888;
    }
    """
    
    def __init__(self, mode: str = "STOCKS", **kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        self.update_headline()
        
    def on_mount(self) -> None:
        """Start headline rotation"""
        self.set_interval(5.0, self.cycle_headline)
        
    def update_headline(self) -> None:
        """Update to current headline"""
        headlines = self.NEWS_DATA.get(self.mode, self.NEWS_DATA["STOCKS"])
        self.current_headline = headlines[self.headline_index % len(headlines)]
        
    async def cycle_headline(self) -> None:
        """Rotate to next headline"""
        headlines = self.NEWS_DATA.get(self.mode, self.NEWS_DATA["STOCKS"])
        self.headline_index = (self.headline_index + 1) % len(headlines)
        self.update_headline()
        
    def render(self) -> Text:
        """Render current headline"""
        news = Text()
        news.append(self.current_headline, style="dim")
        return news
    
    def set_mode(self, new_mode: str) -> None:
        """Change mode and reset headlines"""
        self.mode = new_mode
        self.headline_index = 0
        self.update_headline()
