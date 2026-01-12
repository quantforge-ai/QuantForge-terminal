"""
Status Bar Widget
Builds a rich Text object showing navigation path and state.
"""

from rich.text import Text

def build_status_bar(path: list, mode: str) -> Text:
    """Returns a formatted status bar showing breadcrumbs and connection"""
    status = Text()
    
    # Path / Breadcrumbs
    path_len = len(path)
    for i, segment in enumerate(path):
        status.append(segment, style="cyan")
        if i < path_len - 1:
            status.append(" > ", style="dim")
            
    status.append(" │ ", style="dim")
    
    # Mode
    status.append(mode, style="#ff8800" if mode == "STOCKS" else "cyan")
    status.append("  21:44 IST", style="white")
    
    status.append(" │ ", style="dim")
    
    # Connection status
    status.append("● ", style="#00ff88")
    status.append("Connected", style="#00ff88")
    
    status.append(" │ ", style="dim")
    
    # Shadow Watch branding
    status.append("🌑 ", style="white")
    status.append("Powered by ", style="dim")
    status.append("Shadow Watch", style="#9d4edd")
    
    return status
