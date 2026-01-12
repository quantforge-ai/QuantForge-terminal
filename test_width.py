# test_width.py - Nuclear Option Test
from textual.app import App
from textual.widgets import Static
import sys

# Import custom driver
if sys.platform == "win32":
    from drivers.responsive_windows_driver import ResponsiveWindowsDriver
    USING_CUSTOM_DRIVER = True
else:
    USING_CUSTOM_DRIVER = False

class TestApp(App):
    CSS = """
    Screen {
        width: 100%;
        height: 100%;
        background: red;
    }
    
    Static {
        width: 100%;
        height: 100%;
        background: green;
        text-align: center;
        content-align: center middle;
        text-style: bold;
    }
    """
    
    def get_driver_class(self):
        if USING_CUSTOM_DRIVER:
            return ResponsiveWindowsDriver
        return super().get_driver_class()
    
    def compose(self):
        yield Static("FULL WIDTH TEST - If you see RED on edges, driver isn't working.\nIf ONLY green, driver works but main app CSS is wrong.")
    
    def on_mount(self):
        self.notify(f"Test App Size: {self.size}")

if __name__ == "__main__":
    TestApp().run()
