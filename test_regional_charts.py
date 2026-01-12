import sys
import os
sys.path.append(os.path.join(os.getcwd(), "Quant-TUI"))

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical, Horizontal
from widgets.charts import RegionalChart

class ChartTestApp(App):
    """Test environment for RegionalChart widget"""
    
    BINDINGS = [
        ("t", "cycle_timeline", "Cycle Timeline / Toggle"),
        ("m", "toggle_mode", "Toggle Line/Bar"),
        ("q", "quit", "Quit")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield RegionalChart("Americas", id="chart-a")
            yield RegionalChart("Asia-Pacific", id="chart-b")
        with Horizontal():
            yield RegionalChart("Europe", id="chart-c")
            yield RegionalChart("Africa", id="chart-d")
        yield Footer()

    def action_cycle_timeline(self) -> None:
        for chart in self.query(RegionalChart):
            chart.cycle_timeline()
            # If going to 1W, also toggle mode as per test spec? 
            # "1m line... t to 1w bar"
            if chart.timeline == "1W":
                chart.mode = "bar"
            else:
                chart.mode = "line"

    def action_toggle_mode(self) -> None:
        for chart in self.query(RegionalChart):
            chart.toggle_mode()

if __name__ == "__main__":
    app = ChartTestApp()
    app.run()
