"""
HeatGrid Widget - 4x4 Emoji Mood Indicators
Interactive grid with color-coded percentages
"""

from textual.widget import Widget
from textual.widgets import Button, Static
from textual.containers import Grid
from textual.reactive import reactive
from textual.message import Message
from rich.text import Text
import asyncio


class HeatGrid(Widget):
    """
    4x4 grid of emoji mood indicators
    - Green for positive (>0%)
    - Red for negative (<0%)
    - Enter to drill down
    - Auto-refresh every 10s
    """
    
    # Symbol data for each mode (16 symbols per mode)
    GRID_SYMBOLS = {
        "STOCKS": [
            ("AAPL", "🍎"), ("MSFT", "💻"), ("GOOGL", "🔍"), ("AMZN", "📦"),
            ("NVDA", "🎮"), ("TSLA", "🚗"), ("META", "📘"), ("JPM", "🏦"),
            ("V", "💳"), ("WMT", "🛒"), ("JNJ", "💊"), ("PG", "🧼"),
            ("DIS", "🎬"), ("NFLX", "📺"), ("PYPL", "💰"), ("INTC", "🔌")
        ],
        "CRYPTO": [
            ("BTC-USD", "₿"), ("ETH-USD", "Ξ"), ("SOL-USD", "◎"), ("BNB-USD", "🔶"),
            ("ADA-USD", "🔷"), ("AVAX-USD", "🔺"), ("DOT-USD", "⚫"), ("MATIC-USD", "🟣"),
            ("UNI-USD", "🦄"), ("LINK-USD", "🔗"), ("AAVE-USD", "👻"), ("SAND-USD", "🏖️"),
            ("MANA-USD", "🌐"), ("AXS-USD", "🎮"), ("GALA-USD", "🎲"), ("ENJ-USD", "⚔️")
        ],
        "FOREX": [
            ("EURUSD=X", "🇪🇺"), ("GBPUSD=X", "🇬🇧"), ("USDJPY=X", "🇯🇵"), ("USDCHF=X", "🇨🇭"),
            ("AUDUSD=X", "🇦🇺"), ("USDCAD=X", "🇨🇦"), ("NZDUSD=X", "🇳🇿"), ("EURGBP=X", "💶"),
            ("EURJPY=X", "💴"), ("GBPJPY=X", "💷"), ("USDCNH=X", "🇨🇳"), ("USDINR=X", "🇮🇳"),
            ("USDSGD=X", "🇸🇬"), ("USDHKD=X", "🇭🇰"), ("USDKRW=X", "🇰🇷"), ("USDTRY=X", "🇹🇷")
        ],
        "COMMODITIES": [
            ("GC=F", "🥇"), ("SI=F", "⚪"), ("CL=F", "🛢️"), ("NG=F", "🔥"),
            ("HG=F", "🔩"), ("PL=F", "⚙️"), ("PA=F", "🔘"), ("ZC=F", "🌽"),
            ("ZS=F", "🌱"), ("ZW=F", "🌾"), ("KC=F", "☕"), ("SB=F", "🍬"),
            ("CC=F", "🍫"), ("CT=F", "🧵"), ("LBS=F", "🪵"), ("HG=F", "⚡")
        ],
        "INDICES": [
            ("^GSPC", "🇺🇸"), ("^DJI", "📊"), ("^IXIC", "💻"), ("^RUT", "📈"),
            ("^NSEI", "🇮🇳"), ("^BSESN", "📉"), ("^N225", "🇯🇵"), ("^HSI", "🇭🇰"),
            ("^FTSE", "🇬🇧"), ("^GDAXI", "🇩🇪"), ("^FCHI", "🇫🇷"), ("^STOXX50E", "🇪🇺"),
            ("^AXJO", "🇦🇺"), ("^BVSP", "🇧🇷"), ("^MXX", "🇲🇽"), ("^KS11", "🇰🇷")
        ]
    }
    
    mode = reactive("STOCKS")
    
    DEFAULT_CSS = """
    HeatGrid {
        height: auto;
        background: #121212;
        padding: 1 2;
    }
    
    HeatGrid Grid {
        grid-size: 4 4;
        grid-gutter: 1 2;
        height: auto;
    }
    
    HeatGrid Button {
        height: 3;
        min-width: 18;
        background: #1a1a1a;
        border: solid #333333;
        text-align: center;
    }
    
    HeatGrid Button:hover {
        background: #2a2a2a;
        border: solid #00ffff;
    }
    
    HeatGrid Button:focus {
        background: #3a3a3a;
        border: solid #00ff88;
    }
    """
    
    class CellSelected(Message):
        """Message when grid cell is selected"""
        def __init__(self, symbol: str, emoji: str) -> None:
            self.symbol = symbol
            self.emoji = emoji
            super().__init__()
    
    def __init__(self, mode: str = "STOCKS", **kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        self.quote_data = {}
        
    def compose(self):
        """Build 4x4 grid of buttons"""
        with Grid():
            symbols = self.GRID_SYMBOLS.get(self.mode, self.GRID_SYMBOLS["STOCKS"])
            for symbol, emoji in symbols:
                btn = Button(
                    self._format_cell(symbol, emoji, 0.0),
                    id=f"grid-{symbol}",
                    classes="heat-cell"
                )
                btn.symbol = symbol
                btn.emoji = emoji
                yield btn
    
    def on_mount(self) -> None:
        """Start auto-refresh on mount"""
        self.refresh_data()
        self.set_interval(10.0, self.refresh_data)
        
    def _format_cell(self, symbol: str, emoji: str, change_pct: float) -> Text:
        """Format cell text with emoji and percentage"""
        cell = Text()
        cell.append(f"{emoji}\n", style="white")
        cell.append(f"{symbol}\n", style="cyan")
        
        # Color based on percentage
        if change_pct > 0:
            cell.append(f"+{change_pct:.1f}%", style="#00ff88 bold")
        elif change_pct < 0:
            cell.append(f"{change_pct:.1f}%", style="#ff4444 bold")
        else:
            cell.append(f"{change_pct:.1f}%", style="#888888")
        
        return cell
    
    async def refresh_data(self) -> None:
        """Fetch real-time data from yfinance (mock for now)"""
        # TODO: Integrate with backend quote service
        # For now, generate mock percentages
        import random
        
        symbols = self.GRID_SYMBOLS.get(self.mode, self.GRID_SYMBOLS["STOCKS"])
        
        for symbol, emoji in symbols:
            # Mock data: random percentage between -5% and +5%
            change_pct = random.uniform(-5.0, 5.0)
            self.quote_data[symbol] = change_pct
            
            # Update button
            try:
                btn = self.query_one(f"#grid-{symbol}", Button)
                btn.label = self._format_cell(symbol, emoji, change_pct)
            except Exception:
                pass
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle cell selection"""
        if hasattr(event.button, 'symbol'):
            self.post_message(
                self.CellSelected(event.button.symbol, event.button.emoji)
            )
    
    def set_mode(self, new_mode: str) -> None:
        """Change mode and rebuild grid"""
        self.mode = new_mode
        # Rebuild grid with new symbols
        # TODO: Implement dynamic grid rebuild
        self.refresh_data()
