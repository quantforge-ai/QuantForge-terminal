"""
Debug script to test terminal size detection
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Terminal Size Detection Test")
print("=" * 60)

# Test 1: os.get_terminal_size()
try:
    size = os.get_terminal_size()
    print(f"✅ os.get_terminal_size(): {size.columns} × {size.lines}")
except Exception as e:
    print(f"❌ os.get_terminal_size() failed: {e}")

# Test 2: shutil.get_terminal_size()
import shutil
try:
    size = shutil.get_terminal_size()
    print(f"✅ shutil.get_terminal_size(): {size.columns} × {size.lines}")
except Exception as e:
    print(f"❌ shutil.get_terminal_size() failed: {e}")

# Test 3: Custom driver
if sys.platform == "win32":
    try:
        from drivers.responsive_windows_driver import ResponsiveWindowsDriver
        # Create a mock driver instance
        class MockApp:
            pass
        driver = ResponsiveWindowsDriver(MockApp(), None)
        size = driver._get_terminal_size()
        print(f"✅ ResponsiveWindowsDriver: {size.width} × {size.height}")
    except Exception as e:
        print(f"❌ ResponsiveWindowsDriver failed: {e}")
        import traceback
        traceback.print_exc()

# Test 4: Run Textual app and check its size
print("\n" + "=" * 60)
print("Starting Textual App (press Ctrl+C to exit)...")
print("=" * 60)

from textual.app import App
from textual.widgets import Static

class DebugApp(App):
    def on_mount(self):
        # Print actual app size
        print(f"\n🔍 App.size inside Textual: {self.size}")
        print(f"🔍 Screen.size: {self.screen.size}")
        print(f"🔍 App region: {self.screen.region}")
        
    def compose(self):
        yield Static(f"Terminal Size Test\nApp thinks size is: {self.size}", id="test")

if __name__ == "__main__":
    # Check if on Windows and use custom driver
    if sys.platform == "win32":
        from drivers.responsive_windows_driver import ResponsiveWindowsDriver
        
        class DebugAppWithDriver(DebugApp):
            def get_driver_class(self):
                return ResponsiveWindowsDriver
        
        app = DebugAppWithDriver()
    else:
        app = DebugApp()
    
    app.run()
