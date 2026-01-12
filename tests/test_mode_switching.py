"""
Integration Tests for Mode Switching Feature
Tests Global/Personal view toggling with g/p keys
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Quant-TUI'))

from app.modes import ModeManager


def test_mode_manager_initialization():
    """Test ModeManager initializes in global mode"""
    manager = ModeManager()
    assert manager.mode == "global"
    assert manager.is_global()
    assert not manager.is_personal()


def test_mode_toggle():
    """Test toggling between modes"""
    manager = ModeManager()
    
    # Toggle to personal
    result = manager.toggle("personal")
    assert result == "personal"
    assert manager.is_personal()
    assert not manager.is_global()
    
    # Toggle back to global
    result = manager.toggle("global")
    assert result == "global"
    assert manager.is_global()
    assert not manager.is_personal()


def test_mode_toggle_next():
    """Test sequential toggling"""
    manager = ModeManager()
    assert manager.mode == "global"
    
    # First toggle
    manager.toggle_next()
    assert manager.mode == "personal"
    
    # Second toggle
    manager.toggle_next()
    assert manager.mode == "global"


def test_status_text():
    """Test status bar text generation"""
    manager = ModeManager()
    
    assert manager.get_status_text() == "[Global]"
    
    manager.toggle("personal")
    assert manager.get_status_text() == "[Personal]"


def test_content_description():
    """Test content description text"""
    manager = ModeManager()
    
    global_desc = manager.get_content_description()
    assert "global" in global_desc.lower()
    assert "region" in global_desc.lower()
    
    manager.toggle("personal")
    personal_desc = manager.get_content_description()
    assert "personal" in personal_desc.lower() or "watchlist" in personal_desc.lower()


def test_invalid_mode():
    """Test handling of invalid mode"""
    manager = ModeManager()
    original_mode = manager.mode
    
    # Invalid mode should not change state
    result = manager.toggle("invalid")  # type: ignore
    assert manager.mode == original_mode


def test_mode_manager_reactivity():
    """Test that mode changes are reactive"""
    manager = ModeManager()
    mode_changes = []
    
    # Simple test without actual reactive framework
    # Just verify toggle returns new mode
    mode_changes.append(manager.toggle("personal"))
    mode_changes.append(manager.toggle("global"))
    
    assert mode_changes == ["personal", "global"]


if __name__ == "__main__":
    # Run all tests
    test_mode_manager_initialization()
    test_mode_toggle()
    test_mode_toggle_next()
    test_status_text()
    test_content_description()
    test_invalid_mode()
    test_mode_manager_reactivity()
    
    print("✅ All mode switching tests passed!")
