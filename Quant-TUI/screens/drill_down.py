"""
Drill Down Screen
Individual stock/asset detail view
Shows: Full name, price, chart, metrics, news
"""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static


class DrillDownScreen(Screen):
    """Detail screen for individual stock/asset"""
    
    def compose(self) -> ComposeResult:
        yield Static("Drill Down Screen - To be implemented")
