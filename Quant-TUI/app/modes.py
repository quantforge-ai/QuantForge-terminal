"""
Mode Management - Global vs Personal View Toggle
Handles switching between Global (regions explorer) and Personal (watchlist) modes
"""

from typing import Literal

ViewMode = Literal["global", "personal"]


class ModeManager:
    """
    Manages view mode state for the application
    
    Modes:
    - Global: Browse market regions/sectors (default)
    - Personal: Personal watchlist/vault (requires assets)
    """
    
    def __init__(self):
        self._mode: ViewMode = "global"
    
    @property
    def mode(self) -> ViewMode:
        """Get current mode"""
        return self._mode
    
    @mode.setter
    def mode(self, value: ViewMode) -> None:
        """Set current mode"""
        if value in ("global", "personal"):
            self._mode = value
    
    def toggle(self, new_mode: ViewMode) -> ViewMode:
        """
        Toggle to a specific mode
        
        Args:
            new_mode: Target mode to switch to
            
        Returns:
            The new active mode
        """
        if new_mode in ("global", "personal"):
            self._mode = new_mode
        return self._mode
    
    def toggle_next(self) -> ViewMode:
        """
        Toggle to the next mode in sequence
        
        Returns:
            The new active mode
        """
        self._mode = "personal" if self._mode == "global" else "global"
        return self._mode
    
    def is_global(self) -> bool:
        """Check if currently in global mode"""
        return self._mode == "global"
    
    def is_personal(self) -> bool:
        """Check if currently in personal mode"""
        return self._mode == "personal"
    
    def get_status_text(self) -> str:
        """
        Get status bar text for current mode
        
        Returns:
            Formatted mode indicator for status bar
        """
        if self._mode == "global":
            return "[Global]"
        else:
            return "[Personal]"
    
    def get_content_description(self) -> str:
        """
        Get description of current mode's content
        
        Returns:
            Human-readable description of what the mode shows
        """
        if self._mode == "global":
            return "Exploring global markets by region"
        else:
            return "Personal watchlist - Add assets with 's' or '/'"
