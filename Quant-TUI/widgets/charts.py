"""
Regional Chart Widgets for Quant-TUI
Provides ASCII-based line and bar visualizations for global market regions.
"""

import pandas as pd
import math
import numpy as np
import random
from datetime import datetime
from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns

class RegionalChart(Static):
    """
    Refined ASCII chart with Braille 'smooth' curves and asset-specific colors.
    """
    
    timeline = reactive("1M")
    mode = reactive("line")
    market_mode = reactive("STOCKS")
    
    def __init__(self, region: str, market_type: str = "STOCKS", **kwargs):
        super().__init__(**kwargs)
        self.chart_region = region
        self.market_mode = market_type
        self.data = []
        self.change_pct = 0.0
        self.last_price = 0.0
        self._generate_dummy_data()

    def _generate_dummy_data(self) -> None:
        random.seed(hash(self.chart_region + self.timeline))
        vol = {"1D": 0.005, "5D": 0.015, "1M": 0.03, "1Y": 0.15, "5Y": 0.4}.get(self.timeline, 0.03)
        start_price = random.uniform(1000, 5000)
        self.data = [start_price]
        for _ in range(120): # More points for smooth Braille
            self.data.append(self.data[-1] * (1 + random.uniform(-vol/5, vol/4.5)))
        
        self.last_price = self.data[-1]
        self.change_pct = ((self.last_price / self.data[0]) - 1) * 100
        
        # Calculate OHLC for sidebar
        self.open = self.data[0]
        self.high = max(self.data)
        self.low = min(self.data)
        self.close = self.last_price
        self.volume = random.randint(1000, 9999) * (10 if self.timeline in ["1Y", "5Y"] else 1)

    def watch_timeline(self) -> None:
        self._generate_dummy_data()
        self.refresh()

    def _get_asset_color(self) -> str:
        """User defined color scheme"""
        is_gain = self.change_pct >= 0
        if not is_gain: return "#ff4444" # Standard Red for all losses
        
        mapping = {
            "STOCKS": "#00ff88",      # Green
            "CRYPTO": "#ffaa00",      # Orange
            "FOREX": "#00ff88",       # Green
            "COMMODITIES": "#c0c0c0", # Silver
            "INDICES": "#0099ff"      # Blue
        }
        return mapping.get(self.market_mode, "#00ff88")

    def render(self) -> Panel:
        color = self._get_asset_color()
        header = Text()
        header.append(f"{self.chart_region} {self.market_mode} ", style="bold white")
        header.append(f"{self.change_pct:+.1f}%", style=f"bold {color}")

        if self.mode == "line":
            chart_body = self._render_line()
        else:
            chart_body = self._render_bar()

        pulse_body = self._render_market_pulse()
        ohlc_body = self._render_ohlc()
        
        # Triple-Column Layout (Graph | Pulse | OHLC)
        # Increased padding from 1 to 2 for better separation between Pulse and Stats
        combined = Columns([chart_body, pulse_body, ohlc_body], padding=2, expand=False)

        return Panel(combined, title=header, border_style="#333333", padding=(0, 1))

    def _render_ohlc(self) -> Text:
        """Vertical stack of price stats"""
        ohlc = Text()
        ohlc.append("\n\n") # Matches graph offset
        ohlc.append("  == STATS ==\n", style="bold yellow")
        
        # Vertical Label/Value stack
        items = [
            ("OPN", self.open),
            ("HGH", self.high),
            ("LOW", self.low),
            ("CLS", self.close)
        ]
        
        for lbl, val in items:
            ohlc.append(f" {lbl}: ", style="dim")
            ohlc.append(f"{val:>8,.0f}\n", style="white")
            
        ohlc.append(" " + "─" * 12 + "\n", style="#222222")
        ohlc.append(" VOL: ", style="dim")
        ohlc.append(f"{self.volume:>8,}\n", style="bold white")
        
        return ohlc

    def _render_market_pulse(self) -> Text:
        """Compact Market Pulse sidebar"""
        pulse = Text()
        pulse.append("\n\n") # Matches graph offset
        
        # 1. Sentiment
        sentiment_label = "BULL" if self.change_pct > 1 else ("BEAR" if self.change_pct < -1 else "NEUT")
        sentiment_color = "#00ff88" if sentiment_label == "BULL" else ("#ff4444" if sentiment_label == "BEAR" else "#ffaa00")
        pulse.append(f" PULSE: {sentiment_label}\n", style=f"bold {sentiment_color}")
        
        # Super compact gauge
        sentiment_val = min(max(50 + (self.change_pct * 5), 10), 90)
        filled = int(sentiment_val / 20)
        gauge = "[" + "■" * filled + "·" * (5 - filled) + "]"
        pulse.append(f" {gauge} {sentiment_val:,.0f}%\n", style="#888888")
        pulse.append(" " + "─" * 12 + "\n", style="#222222")

        # 2. Top 3 Drivers
        drivers_map = {
            "Americas": [("USA", 1.2), ("CAN", 0.5), ("BRA", -0.8)],
            "Asia-Pacific": [("JPN", 1.5), ("AUS", 0.8), ("IND", 2.1)],
            "Europe": [("UK", -0.5), ("GER", 0.3), ("FRA", 0.1)],
            "MEA": [("ZAF", 0.9), ("UAE", 1.2), ("ISR", -0.4)],
            "Frontier": [("VNM", 2.5), ("EGY", 1.1), ("NGA", -1.5)]
        }
        
        drivers = drivers_map.get(self.chart_region, [("IDX", 0.5), ("SEC", 0.2), ("CUR", -0.1)])
        for name, chg in drivers:
            color = "#00ff88" if chg >= 0 else "#ff4444"
            pulse.append(f" {name: <3} {chg:+.1f}%\n", style=color)
            
        return pulse

    def _get_axis_labels(self) -> list:
        """Dynamic labels based on timeline"""
        if self.timeline == "1D": return ["09:00", "12:00", "15:30"]
        if self.timeline == "5D": return ["Mon", "Wed", "Fri"]
        if self.timeline == "1M": return ["W1", "W2", "W3", "W4"]
        if self.timeline == "1Y": return ["Q1", "Q2", "Q3", "Q4"]
        return ["2021", "2023", "2025"]

    def _render_line(self) -> Text:
        """Braille-based smooth line plotter with dynamic axes"""
        prices = self.data
        h_chars, w_chars = 7, 58 # Taller but fits in 14-height panel
        rows, cols = h_chars * 4, w_chars * 2
        
        p_min, p_max = min(prices), max(prices)
        if p_min == p_max: p_min *= 0.95; p_max *= 1.05
        
        grid = np.zeros((rows, cols), dtype=int)
        x_coords = np.linspace(0, cols - 1, len(prices))
        y_coords = rows - 1 - ((np.array(prices) - p_min) / (p_max - p_min) * (rows - 1))
        
        for i in range(len(prices) - 1):
            x1, y1 = int(x_coords[i]), int(y_coords[i])
            x2, y2 = int(x_coords[i+1]), int(y_coords[i+1])
            num_steps = max(abs(x2 - x1), abs(y2 - y1))
            for s in range(num_steps + 1):
                t = s / num_steps if num_steps > 0 else 0
                grid[int(y1 + t*(y2-y1)), int(x1 + t*(x2-x1))] = 1

        res_lines = []
        for r in range(0, rows, 4):
            line = []
            for c in range(0, cols, 2):
                codepoint = 0x2800
                if grid[r][c]: codepoint |= 0x1
                if grid[r+1][c]: codepoint |= 0x2
                if grid[r+2][c]: codepoint |= 0x4
                if grid[r][c+1]: codepoint |= 0x8
                if grid[r+1][c+1]: codepoint |= 0x10
                if grid[r+2][c+1]: codepoint |= 0x20
                if grid[r+3][c]: codepoint |= 0x40
                if grid[r+3][c+1]: codepoint |= 0x80
                line.append(chr(codepoint))
            res_lines.append("".join(line))

        result = Text()
        result.append("\n\n") # Push the graph lower within the panel
        color = self._get_asset_color()
        for y in range(h_chars):
            label = f"{p_max if y==0 else (p_min if y==h_chars-1 else (p_max+p_min)/2 if y==h_chars//2 else 0):,.0f}"
            if y in [0, h_chars-1, h_chars//2]: result.append(f"{label:>6} ┤", style="#444444")
            else: result.append(" " * 7 + "│", style="#222222")
            result.append(res_lines[y], style=color)
            result.append("\n")
            
        # Precise X-Axis with Dynamic Labels
        result.append(" " * 8 + "└" + "─" * (w_chars-2) + "┘\n", style="#222222")
        labels = self._get_axis_labels()
        all_labels = labels + ["Now"]
        x_axis = Text(" " * 8)
        
        # Spread all labels (including 'Now') across the chart width precisely
        if len(all_labels) > 1:
            total_labels_len = sum(len(str(l)) for l in all_labels)
            total_space = w_chars - total_labels_len
            gap = total_space // (len(all_labels) - 1)
            rem = total_space % (len(all_labels) - 1)
            
            for i, lbl in enumerate(all_labels):
                x_axis.append(str(lbl), style="dim")
                if i < len(all_labels) - 1:
                    padding = gap + (1 if i < rem else 0)
                    x_axis.append(" " * padding)
        else:
            x_axis.append(str(all_labels[0]), style="dim")
            
        result.append(x_axis)
        result.append("\n") # Reduced newline to bring nav closer
        
        # UI Footer (Selectable) - Better spacing
        nav = Text(" " * 8)
        periods = ["1D", "5D", "1M", "1Y", "5Y"]
        btn_bg = color if self.change_pct >= 0 else "#ff4444"
        for p in periods:
            if p == self.timeline: 
                nav.append(f" [{p}] ", style=f"bold black on {btn_bg}")
            else: 
                nav.append(f"  {p}  ", style="dim")
        result.append(nav)
        
        return result

    def _render_bar(self) -> Text:
        sectors = [("INF", 45, "cyan"), ("FIN", 20, "blue"), ("HLT", 15, "green"), ("ENG", 12, "yellow")]
        res = Text("\n")
        for sym, weight, color in sectors:
            res.append(f"  {sym: <6} ", style="white")
            res.append("▉" * int(weight/3), style=color)
            res.append(f" {weight}%\n", style="bold")
        return res
