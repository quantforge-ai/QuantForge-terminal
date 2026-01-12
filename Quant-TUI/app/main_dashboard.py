"""
Main Dashboard - Quant-TUI Primary Screen
Layout: Header → Rule → "Global Market" → Mode Tabs → Rule → Ticker → Empty Center → News + Portfolio
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Rule
from textual.containers import Container, Horizontal, Vertical
from textual.binding import Binding
from textual.reactive import reactive
from textual import on
from rich.text import Text
from datetime import datetime

# Import widgets
from widgets.flipboard import FlipBoard
from widgets.news_train import NewsTrain
from widgets.portfolio import PortfolioPanel, PortfolioFull
from widgets.search_overlay import SearchOverlay

# Import data
from data.ticker_data import MODE_ICONS

# Import mode manager
from app.modes import ModeManager

# Platform-specific driver import
import sys
import os

# Import custom driver on Windows
if sys.platform == "win32":
    # Add project root to path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, project_root)
    
    try:
        from drivers.responsive_windows_driver import ResponsiveWindowsDriver
        USING_CUSTOM_DRIVER = True
    except ImportError as e:
        print(f"Warning: Could not import ResponsiveWindowsDriver: {e}")
        USING_CUSTOM_DRIVER = False
else:
    USING_CUSTOM_DRIVER = False


class MainDashboard(App):
    """
    Main Dashboard for Quant-TUI
    
    Layout:
    ┌─────────────────────────────────────────────┐
    │ Header (time, title)                        │
    ├─────────────────────────────────────────────┤
    │ FlipBoard Ticker Train (auto-cycling)       │
    ├─────────────────────────────────────────────┤
    │                                             │
    │          4x4 HeatGrid (emoji mood)          │
    │                                             │
    ├──────────────────────────┬──────────────────┤
    │ News Train (3 headlines) │ Portfolio Panel  │
    └──────────────────────────┴──────────────────┘
    │ Status Bar (breadcrumb, connection)         │
    └─────────────────────────────────────────────┘
    
    Keybindings:
    - r: Refresh data
    - M: Toggle map overlay (future)
    - /: Search overlay
    - Enter: Drill down from HeatGrid
    - ESC: Go back
    """
    
    BINDINGS = [
        Binding("g", "toggle_global_mode", "Global", show=True),
        Binding("v", "toggle_personal_mode", "Vault", show=True),
        Binding("p", "toggle_portfolio_full", "Portfolio", show=True),
        Binding("r", "refresh_data", "Refresh", show=True),
        Binding("M", "toggle_map", "Map", show=True),
        Binding("/", "open_search", "Search", show=True),
        Binding("escape", "go_back", "Back", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]
    
    current_mode = reactive("STOCKS")
    navigation_path = reactive(["Global", "Dashboard"])
    view_mode = reactive("global")  # global or personal
    
    # Application configuration
    TITLE = "QuantTerminal"
    CSS_PATH = None
    
    def get_driver_class(self):
        """
        Override driver class to use custom responsive driver on Windows.
        
        This fixes the terminal sizing issue where the app renders at 80×25
        despite detecting larger terminal sizes.
        
        Returns:
            Driver class to use (ResponsiveWindowsDriver on Windows, default otherwise)
        """
        if USING_CUSTOM_DRIVER:
            print(f"✅ Using ResponsiveWindowsDriver")
            return ResponsiveWindowsDriver
        else:
            print(f"❌ Using DEFAULT driver (USING_CUSTOM_DRIVER={USING_CUSTOM_DRIVER})")
        return super().get_driver_class()
    
    CSS = """
    Screen {
        width: 100%;
        height: 100%;
        overflow: hidden hidden;  /* No scrolling */
        padding: 0;  /* CRITICAL: No padding on screen */
    }

    #main-wrapper {
        width: 100%;
        height: 100%;
        padding: 0;  /* No padding */
    }

    #header-container {
        width: 100%;
        padding: 0;
    }

    #ticker-container{
        width: 100%;
        padding: 0;  /* Was causing gap */
    }

    #middle-section {
        width: 100%;
        padding: 0;
    }

    #heatgrid-container {
        width: 100%;
        padding: 0;
    }

    #news-container {
        width: 100%;
        padding: 0;  /* Removed vertical padding */
    }

    #portfolio-container {
        width: 100%;
        padding: 0;
    }

    #status-container {
        width: 100%;
        padding: 0;
    }

    /* Force all widgets to 100% width with no padding */
    FlipBoard {
        width: 100%;
        padding: 0;  /* Override widget default */
    }

    HeatGrid {
        width: 100%;
        padding: 0;
    }

    NewsTrain {
        width: 100%;
        padding: 0;
    }

    PortfolioPanel {
        width: 100%;
        padding: 0;
    }

    StatusBar {
        width: 100%;
        padding: 0;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Compose dashboard layout matching reference screenshot"""
        
        # Wrap everything in a container to ensure full-screen fill
        with Container(id="main-wrapper"):
            # Header with centered title
            with Container(id="header-container"):
                yield Static(
                    "QuantTerminal v1.0 - Multi-Asset Dashboard - Real-time Market Data",
                    id="header-title"
                )
                yield Static(self._build_clock(), id="header-clock")
            
            # First separator line
            yield Rule()
            
            # View mode label (Global Market / Personal Watchlist)
            label_text = "Global Market" if self.view_mode == "global" else "Personal Watchlist"
            yield Static(label_text, id="mode-label")
            
            # Mode tabs (STOCKS | CRYPTO | FOREX | COMMODITIES | INDICES)
            with Horizontal(id="mode-tabs"):
                for mode in ["STOCKS", "CRYPTO", "FOREX", "COMMODITIES", "INDICES"]:
                    yield Button(f"{MODE_ICONS[mode]} {mode}", id=f"mode-{mode}", classes="mode-tab")
            
            # Second separator line
            yield Rule()
            
            # Ticker train (FlipBoard) - shows GLOBAL trending assets, unchanging
            with Container(id="ticker-container"):
                if self.view_mode == "global":
                    yield FlipBoard(mode="GLOBAL", id="ticker-train")
                else:
                    # Personal mode: show empty state
                    yield Static("Your watchlist is empty. Press 's' or '/' to add assets.", id="empty-watchlist")
            
            # Center area - EMPTY by default
            with Container(id="center-area"):
                yield Static("", id="center-content")
            
            # Bottom section: News (left) + Portfolio (right)
            with Horizontal(id="bottom-section"):
                with Container(id="news-container"):
                    yield NewsTrain(mode=self.current_mode, id="news-train")
                
                with Container(id="portfolio-container"):
                    yield PortfolioPanel(id="portfolio-panel")
            
            # Status bar
            with Container(id="status-container"):
                yield Static(
                    self._build_status_bar(),
                    id="status-bar"
                )
    
    def _build_clock(self) -> str:
        """Build clock string"""
        now = datetime.now().strftime("%H:%M IST")
        return f"⏰ {now}"
    
    def _build_status_bar(self) -> Text:
        """Build status bar: [Global/Personal] | Dashboard | STOCKS | HH:MM IST | ● Connected"""
        status = Text()
        
        # View mode indicator [Global] or [Vault]
        status.append("[", style="cyan")
        mode_text = "Global" if self.view_mode == "global" else "Vault"
        status.append(mode_text, style="cyan")
        status.append("]", style="cyan")
        
        for segment in self.navigation_path[1:]:
            status.append(" | ", style="dim")
            status.append(segment, style="cyan")
        
        # Mode
        status.append(" | ", style="dim")
        status.append(self.current_mode, style="#ff8800")
        
        # Time
        status.append(" | ", style="dim")
        now = datetime.now().strftime("%H:%M IST")
        status.append(now, style="#121212")
        
        # Connection
        status.append(" | ", style="dim")
        status.append("● ", style="#00ff88")
        status.append("Connected", style="#00ff88")
        
        return status
    
    def on_mount(self) -> None:
        """Initialize dashboard on mount"""
        # Show app size
        self.notify(f"App size: {self.size}")
        try:
            size = os.get_terminal_size()
            self.log(f"Python detected: {size.columns}×{size.lines}")
            
            # Access Textual's console driver directly and force resize
            if hasattr(self.app, '_driver'):
                driver = self.app._driver
                if hasattr(driver, '_size'):
                    from textual.geometry import Size
                    driver._size = Size(size.columns, size.lines)
                    self.log(f"Forced driver size to: {size.columns}×{size.lines}")
                    # Trigger full refresh
                    self.app.refresh(layout=True)
            else:
                self.log("Could not access driver, using Textual defaults")
        except Exception as e:
            self.log(f"Size override failed: {e}")
        
        # Initialize mode manager
        self.mode_manager = ModeManager()
        
        # Update clock every second
        self.set_interval(1.0, self.update_clock)
        # Update status bar every second (for time)
        self.set_interval(1.0, self.update_status_bar)
        # No default focus - let user navigate with Tab key
        
    def update_clock(self) -> None:
        """Update header clock"""
        try:
            clock = self.query_one("#header-clock", Static)
            clock.update(self._build_clock())
        except Exception:
            pass
    
    def update_status_bar(self) -> None:
        """Update status bar time"""
        try:
            status = self.query_one("#status-bar", Static)
            status.update(self._build_status_bar())
        except Exception:
            pass
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle mode tab clicks and navigation"""
        button_id = event.button.id
        if button_id and button_id.startswith("mode-"):
            new_mode = button_id.replace("mode-", "")
            self.current_mode = new_mode
            
            # Update active tab styling
            for mode in ["STOCKS", "CRYPTO", "FOREX", "COMMODITIES", "INDICES"]:
                try:
                    btn = self.query_one(f"#mode-{mode}", Button)
                    if mode == new_mode:
                        btn.add_class("active")
                    else:
                        btn.remove_class("active")
                except Exception:
                    pass
            
            # Update news for new mode (ticker stays GLOBAL)
            try:
                self.query_one("#news-train", NewsTrain).set_mode(new_mode)
            except Exception:
                pass
            
            # Navigate to regional view
            from screens.region_screen import RegionTrainScreen
            self.push_screen(RegionTrainScreen(new_mode))
            
            self.notify(f"Switched to {new_mode} mode", severity="information")
    
    def action_refresh_data(self) -> None:
        """Refresh all data (r key)"""
        self.notify("🔄 Refreshing market data...", severity="information")
        # Global Refresh logic
        try:
            ticker = self.query_one("#ticker-train", FlipBoard)
            ticker.update_ticker()
        except Exception:
            pass
        self.notify("✅ Data refreshed", severity="information")
    
    def action_toggle_map(self) -> None:
        """Toggle map overlay (M key) - TODO: Implement"""
        self.notify("🗺️  Map overlay - Coming soon!", severity="information")
    
    def action_open_search(self) -> None:
        """Open search overlay (/ key)"""
        self.push_screen(SearchOverlay())
    
    def action_go_back(self) -> None:
        """Go back in navigation"""
        if len(self.navigation_path) > 1:
            self.navigation_path = list(self.navigation_path)[:-1]
        else:
            self.notify("Already at root", severity="warning")
    
    def action_drill_down_mode(self) -> None:
        """Drill down into current mode's regional/category view"""
        from screens.region_screen import RegionTrainScreen
        self.push_screen(RegionTrainScreen(self.current_mode))
    
    def action_toggle_global_mode(self) -> None:
        """Toggle to Global mode (g key)"""
        # Don't switch if already in global mode
        if self.view_mode == "global":
            return
        
        self.view_mode = "global"
        self.mode_manager.toggle("global")
        self.refresh_mode_ui()
        self.update_status_bar()
        self.notify("📍 Switched to Global view - Explore regions", severity="information")
    
    
    
    def action_toggle_portfolio_full(self) -> None:
        """Open full portfolio screen (p key)"""
        self.push_screen(PortfolioFull())
    
    def action_toggle_personal_mode(self) -> None:
        """Toggle to Personal mode (p key)"""
        # Don't switch if already in personal mode
        if self.view_mode == "personal":
            return
        
        self.view_mode = "personal"
        self.mode_manager.toggle("personal")
        self.refresh_mode_ui()
        self.update_status_bar()
        self.notify("👤 Switched to Personal Vault - Your Portfolio", severity="information")
    
    def refresh_mode_ui(self) -> None:
        """Refresh UI elements that change based on view mode"""
        try:
            # Update mode label
            label = self.query_one("#mode-label", Static)
            label.update("Global Market" if self.view_mode == "global" else "Personal Watchlist")
            
            # Update ticker container
            container = self.query_one("#ticker-container", Container)
           
            # Remove all children from container
            container.remove_children()
            
            # Mount new content based on mode (ticker always GLOBAL)
            if self.view_mode == "global":
                container.mount(FlipBoard(mode="GLOBAL", id="ticker-train"))
            else:
                container.mount(Static("Your watchlist is empty. Press 's' or '/' to add assets.", id="empty-watchlist"))
        except Exception as e:
            self.log(f"Error refreshing mode UI: {e}")
    
    def set_mode(self, new_mode: str) -> None:
        """Change mode and update all widgets (except ticker which stays GLOBAL)"""
        self.current_mode = new_mode
        
        # Update mode-aware widgets (news only, ticker stays GLOBAL)
        try:
            self.query_one("#news-train", NewsTrain).set_mode(new_mode)
        except Exception:
            pass


if __name__ == "__main__":
    app = MainDashboard()
    app.run()
