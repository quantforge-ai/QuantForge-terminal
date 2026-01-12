"""
Search Modal Screen
A popup search screen that appears on top of the dashboard.
"""

from textual.screen import ModalScreen
from textual.widgets import Input, Static, ListItem, ListView
from textual.containers import Vertical, Container
from textual.app import ComposeResult
from textual.message import Message
from rich.text import Text
from data.search_data import SEARCH_SUGGESTIONS

class SearchOverlay(ModalScreen):
    """A modal search screen that pops up over the dashboard."""
    
    class Selected(Message):
        """Sent when a search result is selected."""
        def __init__(self, symbol: str) -> None:
            self.symbol = symbol
            super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="search-container"):
            yield Static("🔍 Search (type symbol or name, use .NS/.US for region)", id="search-title")
            yield Input(placeholder="BTC", id="search-input")
            yield ListView(id="search-results")

    def on_mount(self) -> None:
        self.query_one("#search-input", Input).focus()
        self._update_results("")

    def _update_results(self, query: str) -> None:
        try:
            list_view = self.query_one("#search-results", ListView)
            list_view.clear()
            
            if not query:
                # Show recent/popular searches by default
                default_searches = SEARCH_SUGGESTIONS[:3]  # Top 3 suggestions
                for i, match in enumerate(default_searches, 1):
                    item_text = Text()
                    item_text.append(f"{i}. ", style="dim")
                    item_text.append(match["symbol"], style="bold cyan")
                    item_text.append(" - ", style="dim")
                    item_text.append(match["name"], style="white")
                    
                    # Color code by region
                    price_color = "#00ff88" if ".US" in match["symbol"] else "#ffaa00"
                    item_text.append(f" ({match['price']})", style=price_color)
                    
                    list_view.append(ListItem(Static(item_text), name=match["symbol"]))
                return

            query = query.upper()
            matches = [
                s for s in SEARCH_SUGGESTIONS 
                if query in s["symbol"].upper() or query in s["name"].upper()
            ]

            for i, match in enumerate(matches[:5], 1):
                item_text = Text()
                item_text.append(f"{i}. ", style="dim")
                item_text.append(match["symbol"], style="bold cyan")
                item_text.append(" - ", style="dim")
                item_text.append(match["name"], style="white")
                
                # Color code by region
                price_color = "#00ff88" if ".US" in match["symbol"] else "#ffaa00"
                item_text.append(f" ({match['price']})", style=price_color)
                
                list_view.append(ListItem(Static(item_text), name=match["symbol"]))
        except:
            pass

    def on_input_changed(self, event: Input.Changed) -> None:
        self._update_results(event.value)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item:
            self.post_message(self.Selected(event.item.name))
            self.dismiss()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss()

    DEFAULT_CSS = """
    SearchOverlay {
        align: left top;
    }
    
    SearchOverlay {
        layer: overlay;
        width: 80%;  /* Changed from fixed 66 */
        height: auto;
        background: #0a0a0a;
        border: solid cyan;
        padding: 1 2;
        align: center middle;
    }
    
    #search-title {
        color: #4488ff;
        height: 2;
    }
    
    #search-input {
        background: #111111;
        border: solid #00aaaa;
        color: white;
        margin-bottom: 1;
    }
    
    #search-results {
        background: transparent;
        height: auto;
        min-height: 2;
        max-height: 6;
        border: none;
    }
    
    ListItem {
        background: transparent;
        padding: 0 1;
    }
    
    ListItem:hover {
        background: #222222;
    }
    """
    # Override to make the modal scrim transparent
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styles.background = "transparent"