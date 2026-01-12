"""
Test suite for Main Dashboard
"""

import pytest
from app.main_dashboard import MainDashboard
from widgets.flipboard import FlipBoard
from widgets.heatgrid import HeatGrid
from widgets.news_train import NewsTrain


class TestMainDashboard:
    """Test Main Dashboard composition and functionality"""
    
    def test_dashboard_compose(self):
        """Test that all widgets are composed correctly"""
        app = MainDashboard()
        
        # Check that app initializes
        assert app is not None
        assert app.current_mode == "STOCKS"
        assert len(app.navigation_path) == 2
        assert app.navigation_path == ["Global", "Dashboard"]
    
    def test_keybindings_registered(self):
        """Test that all keybindings are registered"""
        app = MainDashboard()
        
        binding_keys = [b.key for b in app.BINDINGS]
        
        assert "r" in binding_keys  # Refresh
        assert "M" in binding_keys  # Map
        assert "/" in binding_keys  # Search
        assert "escape" in binding_keys  # Back
        assert "q" in binding_keys  # Quit
    
    def test_mode_switching(self):
        """Test mode switching updates widgets"""
        app = MainDashboard()
        
        # Switch to CRYPTO mode
        app.set_mode("CRYPTO")
        assert app.current_mode == "CRYPTO"


class TestFlipBoard:
    """Test FlipBoard widget"""
    
    def test_flipboard_init(self):
        """Test FlipBoard initialization"""
        widget = FlipBoard(mode="STOCKS")
        
        assert widget.mode == "STOCKS"
        assert widget.ticker_index == 0
    
    def test_scramble_chars(self):
        """Test scramble character set exists"""
        widget = FlipBoard()
        
        assert len(widget.scramble_chars) > 0
        assert isinstance(widget.scramble_chars, str)


class TestHeatGrid:
    """Test HeatGrid widget"""
    
    def test_heatgrid_symbols(self):
        """Test that symbol data exists for all modes"""
        modes = ["STOCKS", "CRYPTO", "FOREX", "COMMODITIES", "INDICES"]
        
        for mode in modes:
            assert mode in HeatGrid.GRID_SYMBOLS
            assert len(HeatGrid.GRID_SYMBOLS[mode]) == 16
    
    def test_heatgrid_init(self):
        """Test HeatGrid initialization"""
        widget = HeatGrid(mode="CRYPTO")
        
        assert widget.mode == "CRYPTO"
        assert isinstance(widget.quote_data, dict)


class TestNewsTrain:
    """Test NewsTrain widget"""
    
    def test_news_data_exists(self):
        """Test that news data exists for all modes"""
        modes = ["STOCKS", "CRYPTO", "FOREX", "COMMODITIES", "INDICES"]
        
        for mode in modes:
            assert mode in NewsTrain.NEWS_DATA
            assert len(NewsTrain.NEWS_DATA[mode]) == 3
    
    def test_news_train_init(self):
        """Test NewsTrain initialization"""
        widget = NewsTrain(mode="FOREX")
        
        assert widget.mode == "FOREX"
        assert widget.headline_index == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
