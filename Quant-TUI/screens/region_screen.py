"""
Region/Category Train Screen
Displays vertical FlipBoard trains for drilling into regions or categories
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Container, Vertical, Horizontal
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text

from widgets.flipboard import FlipBoard
from widgets.charts import RegionalChart
from data.hierarchy import MODE_HIERARCHY, MODE_HEADERS


class RegionTrainScreen(Screen):
    """
    Screen showing vertical trains for each region/category of an asset class
    
    Key bindings:
    - 1-5: Jump to region/category
    - Enter: Drill down into selected region (TODO: future)
    - t: Cycle timeline (1D→1W→1M→3M→6M→1Y→5Y)
    - ESC: Return to main dashboard
    """
    
    BINDINGS = [
        Binding("1", "jump_region_1", "Region 1", show=False),
        Binding("2", "jump_region_2", "Region 2", show=False),
        Binding("3", "jump_region_3", "Region 3", show=False),
        Binding("4", "jump_region_4", "Region 4", show=False),
        Binding("5", "jump_region_5", "Region 5", show=False),
        Binding("t", "cycle_timeline", "Timeline", show=False),
        Binding("enter", "select_region", "Select", show=False),
        Binding("escape", "go_back", "Back to Main", show=False),
    ]
    
    # Timeline periods for yfinance (aligned with RegionalChart UI)
    TIMELINES = ["1d", "5d", "1mo", "1y", "5y"]
    TIMELINE_LABELS = ["1D", "5D", "1M", "1Y", "5Y"]
    
    def __init__(self, mode: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.hierarchy = MODE_HIERARCHY.get(mode, {})
        self.header_text = MODE_HEADERS.get(mode, f"{mode} Markets")
        self.current_timeline_index = 0  # Start with 1D
        self.selected_region_index = 0  # Track which region is focused
    
    CSS = """
    Screen {
        background: #121212;
    }
    
    #region-header {
        height: 1;
        text-align: center;
        color: cyan;
        background: #121212;
        text-style: bold;
    }
    
    Rule {
        color: white;
        background: #121212;
        height: 1;
    }
    
    #scroll-body {
        height: 1fr;
        background: #121212;
        layout: vertical;
        overflow-y: auto;
    }
    
    #trains-area {
        height: auto;
    }
    
    .region-train {
        height: 2;
        background: #121212;
        margin: 0;
    }
    
    #charts-area {
        height: auto;
        padding: 0;
        background: #121212;
        layout: vertical;
    }
    .chart-row {
        height: 14;
        margin: 0;
        layout: horizontal;
    }
    RegionalChart {
        width: 1fr;
        height: 14;
        margin: 0;
        background: transparent;
    }
    #chart-5 {
        width: 1fr;
    }
    .spacer-col { width: 1fr; }
    
    Rule.train-separator {
        color: #1a1a1a;
        background: #121212;
        height: 1;
    }
    
    #status-bar {
        height: 1;
        background: #001a2a;
        color: white;
        padding: 0 2;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Compose the region train screen"""
        # Header
        yield Static(self.header_text, id="region-header")
        
        # Scrollable Body
        with Container(id="scroll-body"):
            # Region Ticker Trains
            with Vertical(id="trains-area"):
                for idx, (region_name, region_data) in enumerate(self.hierarchy.items(), 1):
                    with Vertical(classes="region-train"):
                        ticker_str = self._build_ticker_string(region_name, region_data)
                        yield FlipBoard(mode=self.mode, id=f"train-{idx}", ticker_override=ticker_str)
                        if idx < len(self.hierarchy):
                            from textual.widgets import Rule
                            yield Rule(classes="train-separator")
            
            # Regional Charts
            with Vertical(id="charts-area"):
                with Horizontal(classes="chart-row"):
                    yield RegionalChart("Americas", id="chart-1", market_type=self.mode)
                    yield RegionalChart("Asia-Pacific", id="chart-2", market_type=self.mode)
                with Horizontal(classes="chart-row"):
                    yield RegionalChart("Europe", id="chart-3", market_type=self.mode)
                    yield RegionalChart("MEA", id="chart-4", market_type=self.mode)
                with Horizontal(classes="chart-row"):
                    yield RegionalChart("Frontier", id="chart-5", market_type=self.mode)
                    yield Static(classes="spacer-col") # Invisible spacer to balance width
        
        # Status bar
        yield Static(self._build_status_bar(), id="status-bar")
    
    def _build_ticker_string(self, region_name: str, region_data: dict) -> str:
        """Build full ticker string for FlipBoard to handle internally"""
        emoji = region_data.get("emoji", "📍")
        tickers = region_data.get("tickers", [])[:6]  # Limit to 6 stocks
        
        region_idx = list(self.hierarchy.keys()).index(region_name) + 1
        timeline_label = self.TIMELINE_LABELS[self.current_timeline_index]
        
        # Build the full sequence of tickers with a clear separator
        content_str = " | ".join([f"{timeline_label} {t}" for t in tickers])
        
        return f"({region_idx}) {emoji} {region_name} [{timeline_label}] | {content_str} |"
    
    def _build_status_bar(self) -> Text:
        """Build dynamic status bar"""
        status = Text()
        
        # Navigation hint
        status.append("[1-5]", style="cyan")
        status.append(" Select Region | ", style="dim")
        
        # Timeline
        timeline_label = self.TIMELINE_LABELS[self.current_timeline_index]
        status.append(f"[t] {timeline_label}", style="cyan")
        status.append(" | ", style="dim")
        
        # Back
        status.append("[ESC]", style="red")
        status.append(" Back to Main", style="dim")
        
        return status
    
    def action_jump_region_1(self) -> None:
        """Jump to region 1"""
        self._select_region(1)
    
    def action_jump_region_2(self) -> None:
        """Jump to region 2"""
        self._select_region(2)
    
    def action_jump_region_3(self) -> None:
        """Jump to region 3"""
        self._select_region(3)
    
    def action_jump_region_4(self) -> None:
        """Jump to region 4"""
        self._select_region(4)
    
    def action_jump_region_5(self) -> None:
        """Jump to region 5"""
        self._select_region(5)
    
    def _select_region(self, region_num: int) -> None:
        """Select a region by number"""
        if region_num <= len(self.hierarchy):
            self.selected_region_index = region_num - 1
            # Visual feedback through notification
            region_name = list(self.hierarchy.keys())[self.selected_region_index]
            self.notify(f"Selected: {region_name}", severity="information", timeout=1)
    
    def action_cycle_timeline(self) -> None:
        """Cycle through timeline periods"""
        self.current_timeline_index = (self.current_timeline_index + 1) % len(self.TIMELINES)
        timeline_label = self.TIMELINE_LABELS[self.current_timeline_index]
        
        # Refresh all trains with new timeline
        self._refresh_trains()
        
        # Sync charts with timeline label
        for chart in self.query(RegionalChart):
            chart.timeline = timeline_label
            chart.mode = "line"
        
        # Update status bar
        self._update_status_bar()
        
        # Notify user
        self.notify(f"Timeline: {timeline_label}", severity="information", timeout=1)
    
    def _refresh_trains(self) -> None:
        """Refresh all ticker trains with current timeline"""
        try:
            for idx, (region_name, region_data) in enumerate(self.hierarchy.items(), 1):
                train = self.query_one(f"#train-{idx}", FlipBoard)
                ticker_str = self._build_ticker_string(region_name, region_data)
                # Update the FlipBoard's ticker
                train.current_ticker = ticker_str
                train.refresh()
        except Exception as e:
            self.log(f"Error refreshing trains: {e}")
    
    def _update_status_bar(self) -> None:
        """Update status bar text"""
        try:
            status_bar = self.query_one("#status-bar", Static)
            status_bar.update(self._build_status_bar())
        except Exception as e:
            self.log(f"Error updating status bar: {e}")
    
    def action_select_region(self) -> None:
        """Select current region (placeholder for future drill-down)"""
        region_num = self.selected_region_index + 1
        region_name = list(self.hierarchy.keys())[self.selected_region_index] if self.selected_region_index < len(self.hierarchy) else "Unknown"
        self.notify(f"Selected {region_name} - Drill-down coming soon!", severity="information")
    
    def action_go_back(self) -> None:
        """Return to main dashboard"""
        self.app.pop_screen()
