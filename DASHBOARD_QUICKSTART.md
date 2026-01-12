# Main Dashboard - Quick Start Guide

## Running the Dashboard

### Option 1: Direct Run
```bash
cd d:\QuantForge-terminal
python run_dashboard.py
```

### Option 2: Module Run
```bash
cd d:\QuantForge-terminal\Quant-TUI
python -m app.main_dashboard
```

## Features Implemented

### ✅ Core Widgets
- **FlipBoard**: Animated ticker train with 0.3s scramble effect
- **HeatGrid**: 4x4 emoji mood indicators with drill-down
- **NewsTrain**: Mode-aware headline rotation (5s dwell)
- **Portfolio Panel**: Compact P&L summary (bottom-right dock)

### ✅ Keybindings
- `r` - Refresh market data (yfinance)
- `M` - Toggle map overlay (placeholder)
- `/` - Open search overlay
- `Enter` - Drill down from HeatGrid cell
- `ESC` - Navigate back
- `q` - Quit application

### ✅ Layout
```
┌─────────────────────────────────────────┐
│ Header (⏰ clock + title)               │
├─────────────────────────────────────────┤
│ FlipBoard Ticker (auto-cycle 10s)       │
├─────────────────────────────────────────┤
│          HeatGrid 4x4                   │
│    🍎 AAPL +2.5%   💻 MSFT +1.2%       │
│    🔍 GOOGL -0.3%  📦 AMZN +3.1%       │
│           ... (16 cells)                │
├────────────────────┬────────────────────┤
│ News Headlines     │ Portfolio Panel    │
│ (3 rotating)       │ (Top 5 holdings)   │
└────────────────────┴────────────────────┘
│ Status Bar (breadcrumb)                 │
└─────────────────────────────────────────┘
```

## Testing

### Run Tests
```bash
cd d:\QuantForge-terminal
pytest tests/test_main_dashboard.py -v
```

### Test Coverage
- Dashboard composition
- Widget initialization
- Keybinding registration
- Mode switching
- Symbol data validation

## Next Steps

1. **Run the dashboard** to verify visual layout
2. **Test keybindings**: Press `r` to refresh, `Enter` on grid cells
3. **Observe animations**: FlipBoard scramble, news rotation
4. **Check responsiveness**: Terminal resize handling

## Known Limitations

- HeatGrid uses mock data (TODO: integrate backend quote service)
- News uses static headlines (TODO: RSS feed integration)
- Asset drill-down screen not yet implemented
- Map overlay placeholder only

## Integration Points

### Backend Connection (TODO)
Replace mock data with backend API:
```python
# In widgets/heatgrid.py
async def refresh_data(self):
    # Replace this:
    change_pct = random.uniform(-5.0, 5.0)
    
    # With this:
    from backend.services.quote_service import get_batch_quotes
    quotes = await get_batch_quotes([symbol for symbol, _ in symbols])
```

### RSS Integration (TODO)
```python
# In widgets/news_train.py
import feedparser
feed = feedparser.parse("https://www.cnbc.com/id/100003114/device/rss/rss.html")
```

## File Structure
```
Quant-TUI/
├── app/
│   ├── __init__.py
│   └── main_dashboard.py       ← Main dashboard screen
├── widgets/
│   ├── flipboard.py            ← Ticker train widget
│   ├── heatgrid.py             ← 4x4 emoji grid
│   ├── news_train.py           ← News headline widget
│   ├── portfolio.py            ← Portfolio panel (existing)
│   └── ...
└── tests/
    └── test_main_dashboard.py  ← Test suite
```
