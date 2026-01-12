"""
FlipBoard Widget - Animated Ticker Train
Scramble animation (0.3s) with auto-cycling tickers
"""

from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from datetime import datetime
import asyncio
import random
from data.ticker_data import TICKER_DATA


class FlipBoard(Widget):
    """
    Animated ticker train with scramble effect
    - Auto-cycles through tickers every 10s
    - 2s dwell time per ticker
    - 0.75s stagger between updates
    - Context-aware based on mode
    """
    
    current_ticker = reactive("")
    is_scrambling = reactive(False)
    mode = reactive("STOCKS")
    
    DEFAULT_CSS = """
    FlipBoard {
        width: 100%;
        height: auto;
        background: #121212;
        color: white;
        padding: 0;  /* Removed horizontal padding */
    }
    """
    
    def __init__(self, mode: str = "STOCKS", ticker_override: str = None, **kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        self.ticker_override = ticker_override  # Custom ticker string
        self.ticker_index = 0
        self.scramble_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        
    def on_mount(self) -> None:
        """Start auto-cycling when mounted"""
        self.update_ticker()
        # Only auto-cycle if no override
        if not self.ticker_override:
            self.set_interval(10.0, self.cycle_ticker)
            
    def update_ticker(self) -> None:
        """Update to current ticker from data"""
        if self.ticker_override:
            self.current_ticker = self.ticker_override
        else:
            raw_ticker = TICKER_DATA.get(self.mode, f"📊 {self.mode} [IST] | 00:00 N/A 0.00 0.0%")
            self.current_ticker = raw_ticker
            
    async def cycle_ticker(self) -> None:
        """Cycle to next ticker with scramble animation"""
        await self.scramble_transition()
        self.update_ticker()
        
    async def scramble_transition(self) -> None:
        """0.3s scramble animation"""
        self.is_scrambling = True
        original = self.current_ticker
        for _ in range(3):
            scrambled = ''.join(
                random.choice(self.scramble_chars) if c.isalnum() else c
                for c in original
            )
            self.current_ticker = scrambled
            await asyncio.sleep(0.1)
        self.current_ticker = original
        self.is_scrambling = False
        
    def render(self) -> Text:
        """Render the ticker tape without motion"""
        ticker = Text()
        raw = self.current_ticker
        if not raw:
            return ticker
            
        # Parse and colorize ticker string
        parts = raw.split(" | ")
        
        # Header (Icon + Mode + [Timezone])
        header_str = parts[0] if parts else raw
        if " [" in header_str:
            split_result = header_str.rsplit(" [", maxsplit=1)
            if len(split_result) == 2:
                label, timezone = split_result
                ticker.append(label, style="cyan bold")
                ticker.append(" [", style="dim")
                ticker.append(timezone.replace("]", ""), style="#ff8800")
                ticker.append("]", style="dim")
            else:
                ticker.append(header_str, style="cyan bold")
        else:
            ticker.append(header_str, style="cyan bold")
        
        # Data segments
        for item in parts[1:]:
            ticker.append(" | ", style="dim")
            subparts = item.strip().split(" ")
            
            if len(subparts) >= 4:
                time, symbol, price, change = subparts[0], subparts[1], subparts[2], subparts[3]
                ticker.append(time + " ", style="dim")
                ticker.append(symbol + " ", style="cyan")
                ticker.append(price + " ", style="white")
                color = "#00ff88" if "+" in change else "#ff4444"
                ticker.append(change, style=color)
            else:
                ticker.append(item, style="white")
        
        ticker.append(" |", style="dim")
        return ticker
    
    def set_mode(self, new_mode: str) -> None:
        """Change mode and update ticker"""
        self.mode = new_mode
        self.update_ticker()
