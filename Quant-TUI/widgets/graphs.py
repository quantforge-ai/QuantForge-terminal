"""
Graph/Chart Widgets
All chart rendering widgets for the TUI
"""

from textual.widget import Widget
from rich.text import Text


class ASCIILineChart(Widget):
    """Sparkline-style ASCII chart using rich"""
    
    def render(self) -> Text:
        return Text("▁▂▃▅▇")


class MarketChart(Widget):
    """Chart with title, region, timeline selector"""
    
    def render(self) -> Text:
        return Text("Market Chart")


class RegionalChart(Widget):
    """Chart for regional data"""
    
    def render(self) -> Text:
        return Text("Regional Chart")


class RegionalSummaryChart(Widget):
    """Condensed chart for summaries"""
    
    def render(self) -> Text:
        return Text("Summary Chart")


class MarketPulse(Widget):
    """Ranking widget showing top movers"""
    
    def render(self) -> Text:
        return Text("1. Middle East +13.5%")
