"""
Ticker Tape Widget
Provides formatted ticker tapes based on market mode.
"""

from rich.text import Text
from data.ticker_data import TICKER_DATA

def build_ticker(mode: str) -> Text:
    """
    Returns a formatted rich Text object for the given mode.
    Matches reference image exactly: [ICON] [MODE] [TIMEZONE] | TIME SYMBOL PRICE CHANGE
    """
    raw_ticker = TICKER_DATA.get(mode, f"📊 {mode} [IST] | 00:00 N/A 0.00 0.0%")
    
    ticker = Text()
    parts = raw_ticker.split(" | ")
    
    # 1. Header part (Icon + Mode + [IST])
    header_str = parts[0]
    # Split header into Icon+Mode and [IST]
    if " [" in header_str:
        label, timezone = header_str.split(" [")
        ticker.append(label, style="cyan bold")
        ticker.append(" [", style="dim")
        ticker.append(timezone.replace("]", ""), style="#ff8800") # Orange IST
        ticker.append("]", style="dim")
    else:
        ticker.append(header_str, style="cyan bold")
    
    # 2. Data parts
    for item in parts[1:]:
        ticker.append(" | ", style="dim")
        
        # Split item into components: 15:54 ^DJI 37,850 +0.45%
        subparts = item.split(" ")
        if len(subparts) >= 4:
            time = subparts[0]
            symbol = subparts[1]
            price = subparts[2]
            change = subparts[3]
            
            ticker.append(time + " ", style="dim")
            ticker.append(symbol + " ", style="cyan")
            ticker.append(price + " ", style="white")
            
            color = "#00ff88" if "+" in change else "#ff4444"
            ticker.append(change, style=color)
        else:
            ticker.append(item, style="white")
    
    # Final delimiter to match look
    ticker.append(" |", style="dim")
        
    return ticker
