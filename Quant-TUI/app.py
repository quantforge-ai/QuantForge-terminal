"""
QuantTerminal TUI - Multi-Asset Dashboard
- Mode switching (STOCKS, CRYPTO, FOREX, COMMODITIES, INDICES)
- Clickable mode tabs
- Mode-specific ticker data
- Search overlay with region extensions
- Global stocks hierarchy navigation
"""

from textual.app import App, ComposeResult
from textual.widgets import Static, Rule, Button, Input
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import reactive
from textual.binding import Binding
from rich.text import Text
from datetime import datetime

# Import data modules
from data.ticker_data import TICKER_DATA, MODE_ICONS
from data.global_hierarchy import (
    GLOBAL_HIERARCHY, REGION_SAMPLES, 
    CRYPTO_TRAINS, FOREX_TRAINS, 
    COMMODITIES_TRAINS, INDICES_TRAINS
)

# Import widget builders
from widgets.search_overlay import SearchOverlay
from widgets.ticker import build_ticker
from widgets.portfolio import build_portfolio_widget
from widgets.status_bar import build_status_bar

# Import screens
from screens.mode_trains import ModeTrainScreen


class QuantTerminal(App):
    """Multi-Asset Dashboard with mode switching, search, and global hierarchy navigation"""
    
    BINDINGS = [
        Binding("/", "open_search", "Search", show=True),
        Binding("s", "open_search", "Search", show=False),
        Binding("escape", "go_back", "Back", show=True),
        Binding("g", "toggle_global_view", "Global", show=True),
        Binding("q", "quit", "Quit", show=True),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]
    
    current_mode = reactive("STOCKS")
    search_active = reactive(False)
    navigation_path = reactive(["Global"])
    global_view_active = reactive(False)
    
    CSS = """
    Screen {
        background: #121212;
        layers: base overlay;
    }
    
    #main-container {
        layer: base;
        layout: vertical;
        width: 100%;
        height: 100%;
    }
    
    #ticker {
        height: 1;
        background: #121212;
    }
    
    #header {
        height: 1;
        background: #121212;
        color: #888888;
        text-align: center;
        margin: 0;
    }
    
    Rule {
        color: white;
        background: #121212;
        height: 1;
        margin: 0;
    }
    
    #label {
        height: 1;
        text-align: center;
        background: #121212;
        color: #00ffff;
        margin: 0;
    }
    
    #mode-tabs {
        height: 1;
        background: #121212;
        align: center middle;
        margin: 0;
    }
    
    .mode-tab {
        min-width: 14;
        height: 1;
        background: #121212;
        color: #666666;
        border: none;
        padding: 0 1;
    }
    
    .mode-tab:hover {
        background: #333333;
        color: #00ffff;
    }
    
    .mode-tab:focus {
        background: #445566;
        color: #ffffff;
        text-style: bold;
    }
    
    .mode-tab.active {
        text-style: bold;
        color: #ffffff;
        background: #445566;
    }
    
    #ticker {
        height: 1;
        background: #121212;
        margin: 0;
    }
    
    #empty-space {
        height: 1fr;
        background: #121212;
    }
    
    #bottom-container {
        height: 12;
        layout: horizontal;
        background: #121212;
    }
    
    #news {
        width: 1fr;
        height: 1;
        background: #121212;
        border: none;
    }
    
    #portfolio {
        width: 32;
        height: 11;
        background: #121212;
        border: none;
    }
    
    #status-bar {
        height: 1;
        background: #111133;
        dock: bottom;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="main-container"):
            # Header
            yield Static("QuantTerminal v1.0 - Multi-Asset Dashboard - Real-time Market Data", id="header")
            yield Rule()
            yield Static("Global Market", id="label")
            
            # Mode tabs
            with Horizontal(id="mode-tabs"):
                for mode in ["STOCKS", "CRYPTO", "FOREX", "COMMODITIES", "INDICES"]:
                    yield Button(f"{MODE_ICONS[mode]} {mode}", id=f"mode-{mode}", classes="mode-tab")
            
            yield Rule()
            yield Static(build_ticker(self.current_mode), id="ticker")
            
            # Main content area - empty by default, populated when mode is selected
            yield Container(id="empty-space")
            
            # Bottom section
            with Horizontal(id="bottom-container"):
                news_text = Text()
                news_text.append("📰 ", style="white")
                news_text.append("Fed announces rate decision ", style="dim")
                news_text.append("• ", style="dim")
                news_text.append("Markets rally on tech earnings", style="dim")
                yield Static(news_text, id="news")
                yield build_portfolio_widget()
            
            yield Static(build_status_bar(list(self.navigation_path), self.current_mode), id="status-bar")
    
    # === Event Handlers ===
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle mode tab clicks"""
        button_id = event.button.id
        if button_id and button_id.startswith("mode-"):
            new_mode = button_id.replace("mode-", "")
            self.current_mode = new_mode
            
            # Push the unified ModeTrainScreen with the selected data
            if new_mode == "STOCKS":
                self.push_screen(ModeTrainScreen(new_mode, GLOBAL_HIERARCHY, list(GLOBAL_HIERARCHY.keys())))
            elif new_mode == "CRYPTO":
                self.push_screen(ModeTrainScreen(new_mode, CRYPTO_TRAINS, list(CRYPTO_TRAINS.keys())))
            elif new_mode == "FOREX":
                self.push_screen(ModeTrainScreen(new_mode, FOREX_TRAINS, list(FOREX_TRAINS.keys())))
            elif new_mode == "COMMODITIES":
                self.push_screen(ModeTrainScreen(new_mode, COMMODITIES_TRAINS, list(COMMODITIES_TRAINS.keys())))
            elif new_mode == "INDICES":
                self.push_screen(ModeTrainScreen(new_mode, INDICES_TRAINS, list(INDICES_TRAINS.keys())))
    
    def watch_current_mode(self, new_mode: str) -> None:
        """Update UI when mode changes (for ticker and tabs)"""
        try:
            for mode in ["STOCKS", "CRYPTO", "FOREX", "COMMODITIES", "INDICES"]:
                btn = self.query_one(f"#mode-{mode}", Button)
                if mode == new_mode:
                    btn.add_class("active")
                else:
                    btn.remove_class("active")
            
            ticker = self.query_one("#ticker", Static)
            ticker.update(build_ticker(new_mode))
        except Exception:
            pass

    def on_mount(self) -> None:
        """Initial mount - dashboard is clean until user clicks a mode"""
        pass
    
    def on_key(self, event) -> None:
        """Handle raw key events for search"""
        # Only handle if we're on the main screen
        if len(self.screen_stack) > 1:
            return
            
        if event.key == "slash" or event.key == "/":
            self.action_open_search()
            event.prevent_default()
            event.stop()
        elif event.key == "s":
            self.action_open_search()
            event.prevent_default()
            event.stop()
    
    # === Actions ===
    
    def action_open_search(self) -> None:
        """Open the search modal"""
        self.push_screen(SearchOverlay())
    
    def action_close_search(self) -> None:
        """Close the search overlay"""
        # Not needed - modal handles its own closing
        pass

    def on_search_overlay_selected(self, message: SearchOverlay.Selected) -> None:
        """Handle ticker selection from search"""
        self.action_close_search()
        self.notify(f"Selected: {message.symbol}", severity="information")
        # Update path
        self.navigation_path = ["Global", self.current_mode, message.symbol]
        self._update_status_bar()
    
    def action_go_back(self) -> None:
        """Go back - close search or navigate up"""
        if self.search_active:
            self.action_close_search()
        elif len(self.navigation_path) > 1:
            new_path = list(self.navigation_path)[:-1]
            self.navigation_path = new_path
            self._update_status_bar()
            if len(new_path) == 1:
                self._clear_content_area()
    
    def action_toggle_global_view(self) -> None:
        """Toggle global hierarchy view"""
        self.global_view_active = not self.global_view_active
        if self.global_view_active:
            self._show_global_regions()
        else:
            self._clear_content_area()
    
    # === Helper Methods ===
    
    def _show_stocks_dashboard(self) -> None:
        """Show default stocks dashboard summary"""
        try:
            empty_space = self.query_one("#empty-space")
            for child in empty_space.children:
                child.remove()
                
            dashboard_text = Text()
            dashboard_text.append("📊 ", style="white")
            dashboard_text.append("GLOBAL STOCKS BY REGION\n", style="cyan bold")
            dashboard_text.append("━" * 50 + "\n\n", style="dim")
            
            for region, samples in REGION_SAMPLES.items():
                dashboard_text.append(f"  {region}\n", style="yellow bold")
                for symbol, change in samples:
                    color = "#00ff88" if "+" in change else "#ff4444"
                    dashboard_text.append(f"    {symbol: <12} ", style="white")
                    dashboard_text.append(f"{change}\n", style=color)
                dashboard_text.append("\n")
            
            dashboard_text.append("Click a tab or press 'g' to explore regions", style="dim")
            empty_space.mount(Static(dashboard_text))
            self._update_status_bar()
        except Exception:
            pass
    
    def _show_global_regions(self) -> None:
        """Show regional hierarchy selection"""
        try:
            empty_space = self.query_one("#empty-space")
            for child in empty_space.children:
                child.remove()
            
            regions_text = Text()
            regions_text.append("🌍 ", style="white")
            regions_text.append("EXPLORE GLOBAL REGIONS\n\n", style="cyan bold")
            
            for i, region in enumerate(GLOBAL_HIERARCHY.keys(), 1):
                regions_text.append(f"  {i}. ", style="dim")
                regions_text.append(f"{region}\n", style="white")
            
            empty_space.mount(Static(regions_text))
        except Exception:
            pass
    
    def _update_status_bar(self) -> None:
        """Update status bar text"""
        try:
            status_bar = self.query_one("#status-bar", Static)
            status_bar.update(build_status_bar(list(self.navigation_path), self.current_mode))
        except Exception:
            pass
    
    def _clear_content_area(self) -> None:
        """Reset the dashboard view"""
        self._show_stocks_dashboard()
        self.global_view_active = False


if __name__ == "__main__":
    app = QuantTerminal()
    app.run()


if __name__ == "__main__":
    app = QuantTerminal()
    app.run()
