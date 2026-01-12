"""
Portfolio Widget System
Provides compact dashboard view and full-screen detailed management.
"""

import csv
import os
from datetime import datetime
from decimal import Decimal
import math
from data.portfolio_models import STRATEGY_MODELS

from textual import on, events
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button, Rule, Header, Footer
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

from widgets.flipboard import FlipBoard

# Dummy Data
PORTFOLIO_DATA = {
    "balance": 100000.00,
    "pl_percent": 2.45,
    "pl_value": 2450.00,
    "holdings": [
        {"symbol": "AAPL", "qty": 83, "avg": 175.50, "current": 185.20, "sector": "Tech", "weight": 15},
        {"symbol": "MSFT", "qty": 29, "avg": 385.00, "current": 412.50, "sector": "Tech", "weight": 12},
        {"symbol": "BTC", "qty": 0.23, "avg": 38500, "current": 42500, "sector": "Crypto", "weight": 10},
        {"symbol": "GOOGL", "qty": 55, "avg": 135.20, "current": 145.80, "sector": "Tech", "weight": 8},
        {"symbol": "ETH", "qty": 2.2, "avg": 1950, "current": 2250, "sector": "Crypto", "weight": 5},
        {"symbol": "GOLD", "qty": 10, "avg": 1950, "current": 2035, "sector": "Commodity", "weight": 20},
        {"symbol": "TSLA", "qty": 30, "avg": 190.00, "current": 175.40, "sector": "Auto", "weight": 5},
        {"symbol": "EUR/USD", "qty": 10000, "avg": 1.09, "current": 1.085, "sector": "ForeX", "weight": 25},
    ]
}

class PortfolioPanel(Static):
    """Compact portfolio view for the bottom dashboard panel"""
    
    DEFAULT_CSS = """
    PortfolioPanel {
        width: 100%;
        height: 100%;
        background: #121212;
        padding: 0;  /* No padding */
    }
    
    #portfolio-glass-container {
        width: 100%;
        height: 100%;
        background: rgba(25, 35, 45, 0.8);
        border: solid cyan;
        border-left: solid cyan;
        padding: 1 1;  /* Minimal padding for content */
    }
    
    #port-top-line {
        width: 100%;
        height: 1;
        color: cyan;
    }
    
    #port-header {
        width: 100%;
        text-align: center;
        color: cyan;
        text-style: bold;
        margin-bottom: 1;
    }
    .balance-label {
        color: #aaaaaa;
        height: 1;
        margin-top: 1;
    }
    .balance-row {
        height: 1;
        align: left middle;
    }
    #balance-amount {
        width: 50%;
        text-style: bold;
        content-align: left middle;
    }
    #pl-info {
        width: 50%;
        content-align: right middle;
    }
    .holdings-label {
        color: #aaaaaa;
        height: 1;
        margin-top: 1;
    }
    .holdings-row {
        height: 1;
        margin-top: 0;
    }
    .view-details {
        color: #888888;
        height: 1;
        margin-top: 1;
    }
    .dim { color: #888888; }
    .up { color: #00ff88; }
    .down { color: #ff4444; }
    """

    def compose(self) -> ComposeResult:
        with Container(id="portfolio-glass-container"):
            # Top decorative line (thinner)
            yield Static("─" * 80, id="port-top-line")
            
            with Vertical():
                yield Static("🧊 PORTFOLIO SUMMARY", id="port-header")
                
                # Balance label (small)
                yield Static("Balance:", classes="balance-label")
                
                # Balance and P&L on same line
                with Horizontal(classes="balance-row"):
                    # Large balance amount
                    balance_text = Text()
                    balance_text.append("$100,000", style="white bold")
                    yield Static(balance_text, id="balance-amount")
                    
                    # Right-aligned P&L
                    pl_text = Text()
                    pl_text.append("P&L: ", style="dim")
                    pl_text.append("+$2,450 ", style="#00ff88 bold")
                    pl_text.append("(+2.45%)", style="#00ff88")
                    yield Static(pl_text, id="pl-info")
                
                # Top 5 Holdings label
                yield Static("Top 5 Holdings", classes="holdings-label")
                
                # Holdings in horizontal layout
                holdings_text = Text()
                for i, h in enumerate(PORTFOLIO_DATA["holdings"][:5]):
                    sym = h["symbol"]
                    pnl = ((h["current"] / h["avg"]) - 1) * 100
                    color = "#00ff88" if pnl >= 0 else "#ff4444"
                    holdings_text.append(f"{sym} ", style="cyan")
                    holdings_text.append(f"{pnl:+.1f}%", style=color)
                    if i < 4:
                        holdings_text.append("  |  ", style="#444444")
                
                yield Static(holdings_text, classes="holdings-row")
                
                # View Details link
                yield Static("\nView Details", classes="view-details")

class PortfolioFull(Screen):
    """Full-screen detailed portfolio management with diagnostic analytics"""
    
    strategy_id = reactive("balanced_core")
    
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("e", "export_csv", "Export CSV"),
        ("left", "prev_strategy", "Prev Strat"),
        ("right", "next_strategy", "Next Strat"),
    ]

    CSS = """
    PortfolioFull { background: #0a0a0a; }
    #full-title {
        height: 3; content-align: center middle;
        text-style: bold; color: cyan; background: #111111;
    }
    #port-container { padding: 1 2; align: center top; }
    DataTable { 
        height: 15; 
        width: 100%; 
        border: tall #222222; 
        background: #111111;
    }
    
    #strategy-selector {
        height: 3; margin: 1 0; background: #161616;
        border: solid #333333; align: center middle;
        width: 100%;
    }
    #strategy-selector Button {
        min-width: 18; margin: 0 1; border: none; background: #222222;
    }
    #strategy-selector Button:hover { background: #333333; }
    #strategy-selector Button.-active { background: cyan; color: black; text-style: bold; }

    #analysis-area {
        height: 20; border: solid #333333; padding: 1 2;
        background: #111111; margin-top: 1;
        width: 100%;
    }
    .score-title { color: #888888; text-style: bold underline; }
    .score-val { color: cyan; text-style: bold; }
    .strategy-desc { color: #aaaaaa; text-style: italic; margin-bottom: 1; height: 1; }
    
    #stats-row { height: 14; align: center middle; }
    #graph-a { width: 60%; height: 100%; border-right: tall #222222; }
    #legend-col { padding-left: 4; width: 40%; }
    
    #actions { height: 3; margin-top: 1; align: center middle; }
    #action-btns { width: 100%; align: center middle; }
    Button { margin: 0 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("📊 PERSONAL VAULT - STRATEGY DIAGNOSTICS", id="full-title")
        
        with Vertical(id="port-container"):
            table = DataTable(id="port-table")
            table.cursor_type = "row"
            table.add_columns("Symbol", "Qty", "Avg Price", "Current", "P&L %", "Value")
            yield table
            
            with Horizontal(id="strategy-selector"):
                for sid, model in STRATEGY_MODELS.items():
                    btn = Button(model["name"], id=f"strat-{sid}")
                    if sid == self.strategy_id: btn.add_class("-active")
                    yield btn

            with Vertical(id="analysis-area"):
                with Horizontal():
                    yield Static("DIVERSIFICATION ANALYSIS", classes="score-title")
                    yield Static(f" | MODEL: {STRATEGY_MODELS[self.strategy_id]['name']}", id="active-model-name", classes="score-val")
                
                yield Static(STRATEGY_MODELS[self.strategy_id]["description"], id="strategy-desc", classes="strategy-desc")
                
                with Horizontal(id="stats-row"):
                    yield Static("", id="graph-a")
                    with Vertical(id="legend-col"):
                        yield Static("", id="analysis-legend")
            
            with Vertical(id="actions"):
                with Horizontal(id="action-btns"):
                    yield Button("BUY ASSET", variant="success", id="buy-btn")
                    yield Button("SELL ASSET", variant="error", id="sell-btn")
                    yield Button("EXPORT CSV [E]", id="export-btn")
        
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        for h in PORTFOLIO_DATA["holdings"]:
            pnl = ((h["current"] / h["avg"]) - 1) * 100
            val = h["qty"] * h["current"]
            pnl_style = "#00ff88 bold" if pnl >= 0 else "#ff4444 bold"
            table.add_row(
                Text(h["symbol"], style="cyan bold"), 
                f"{h['qty']:.2f}", f"${h['avg']:,.2f}", f"${h['current']:,.2f}", 
                Text(f"{pnl:+.2f}%", style=pnl_style), f"${val:,.0f}"
            )
        self._refresh_analysis()

    def watch_strategy_id(self, val: str) -> None:
        if not self.is_mounted: return
        for sid in STRATEGY_MODELS:
            btn = self.query_one(f"#strat-{sid}")
            if sid == val: btn.add_class("-active")
            else: btn.remove_class("-active")
        self._refresh_analysis()

    def _refresh_analysis(self) -> None:
        model = STRATEGY_MODELS[self.strategy_id]
        self.query_one("#active-model-name").update(f" | MODEL: {model['name']}")
        self.query_one("#strategy-desc").update(model["description"])
        self.query_one("#graph-a").update(self._build_bar_graph())
        self.query_one("#analysis-legend").update(self._build_legend())

    @on(Button.Pressed)
    def handle_btn(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid and bid.startswith("strat-"):
            self.strategy_id = bid.replace("strat-", "")
        elif bid == "export-btn":
            self.action_export_csv()

    @on(events.Key)
    def on_key(self, event: events.Key) -> None:
        if event.key == "e":
            self.action_export_csv()
        elif event.key == "left":
            self.action_prev_strategy()
            event.stop()
        elif event.key == "right":
            self.action_next_strategy()
            event.stop()

    def action_next_strategy(self) -> None:
        self._cycle_strat(1)

    def action_prev_strategy(self) -> None:
        self._cycle_strat(-1)

    def _cycle_strat(self, delta: int) -> None:
        keys = list(STRATEGY_MODELS.keys())
        idx = (keys.index(self.strategy_id) + delta) % len(keys)
        self.strategy_id = keys[idx]

    def action_export_csv(self) -> None:
        filename = "portfolio_export.csv"
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["symbol", "qty", "avg", "current", "sector", "weight"])
                writer.writeheader(); writer.writerows(PORTFOLIO_DATA["holdings"])
            self.notify(f"Exported to {os.path.abspath(filename)}", severity="information")
        except Exception as e: self.notify(f"Export failed: {e}", severity="error")

    def _build_legend(self) -> Text:
        legend = Text()
        actual_sectors = {}
        h_total = sum(h["weight"] for h in PORTFOLIO_DATA["holdings"])
        for h in PORTFOLIO_DATA["holdings"]:
            s = h["sector"]; actual_sectors[s] = actual_sectors.get(s, 0) + (h["weight"] / h_total * 100)

        legend.append(f"{'Sector': <12} {'Actual %': <10} {'Target %': <10} {'Drift': <8}\n", style="bold underline")
        targets = STRATEGY_MODELS[self.strategy_id]["targets"]
        legend.append("-" * 45 + "\n", style="dim")
        
        all_sectors = sorted(set(list(targets.keys()) + list(actual_sectors.keys())))
        COLORS = ["cyan", "#00ff88", "#ffff00", "#ffaa00", "#ff4444", "#9400D3"]
        
        for i, sector in enumerate(all_sectors):
            color = COLORS[i % len(COLORS)]
            legend.append("■ ", style=color)
            legend.append(f"{sector: <11} ", style="white")
            
            a_pct = actual_sectors.get(sector, 0)
            t_pct = targets.get(sector, 0)
            legend.append(f"{a_pct:>7.1f}%   {t_pct:>7.1f}%   ", style="dim")
            drift = a_pct - t_pct
            drift_style = "#00ff88" if abs(drift) < 5 else "#ff4444"
            legend.append(f"{drift:>+6.1f}%\n", style=drift_style)
            
        return legend

    def _build_bar_graph(self) -> Text:
        model = STRATEGY_MODELS[self.strategy_id]
        targets = model["targets"]
        graph = Text()
        
        # Get actuals for comparison
        actual_sectors = {}
        h_total = sum(h["weight"] for h in PORTFOLIO_DATA["holdings"])
        for h in PORTFOLIO_DATA["holdings"]:
            s = h["sector"]; actual_sectors[s] = actual_sectors.get(s, 0) + (h["weight"] / h_total * 100)

        all_sectors = sorted(set(list(targets.keys()) + list(actual_sectors.keys())))
        COLORS = ["cyan", "#00ff88", "#ffff00", "#ffaa00", "#ff4444", "#9400D3"]
        
        graph.append("\n  SECTOR ALLOCATION (TARGET VS ACTUAL)\n", style="bold underline")
        graph.append("  " + "─" * 60 + "\n\n", style="dim")
        
        max_bar_width = 40
        for i, sector in enumerate(all_sectors):
            color = COLORS[i % len(COLORS)]
            t_pct = targets.get(sector, 0)
            a_pct = actual_sectors.get(sector, 0)
            
            # Target Bar
            graph.append(f"  {sector: <12} ", style="white")
            t_width = int((t_pct / 100) * max_bar_width)
            graph.append("█" * t_width, style=color)
            if t_width < max_bar_width: graph.append("░" * (max_bar_width - t_width), style="#222222")
            graph.append(f" {t_pct:>5.1f}% [Target]\n", style="dim")
            
            # Actual Indicator (mini bar)
            graph.append(f"  {' ': <12} ", style="white")
            a_width = int((a_pct / 100) * max_bar_width)
            graph.append("▉" * a_width, style="#888888")
            graph.append(f" {a_pct:>5.1f}% [Actual]\n\n", style="dim")
            
        return graph

def build_portfolio_widget() -> PortfolioPanel: 
    return PortfolioPanel(id="portfolio")
