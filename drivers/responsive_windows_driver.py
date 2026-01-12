"""
Responsive Windows Driver for Textual
Fixes terminal sizing issue by querying actual window size instead of buffer size
"""
from textual.drivers.windows_driver import WindowsDriver
from textual.geometry import Size
import ctypes


class ResponsiveWindowsDriver(WindowsDriver):
    """
    Windows driver that respects actual window size, not buffer size.
    
    This fixes the issue where Textual renders at 80×25 despite detecting
    larger terminal dimensions (e.g., 120×30, 209×54).
    
    Root Cause:
    - Standard WindowsDriver uses shutil.get_terminal_size() which reads buffer size
    - Windows Terminal buffer is often 80×25 by default
    - Actual window can be much larger (e.g., 150×40)
    
    Solution:
    - Override __init__ to detect size BEFORE driver initialization
    - Use Win32 GetConsoleScreenBufferInfo API
    - Read srWindow (window rectangle) instead of dwSize (buffer size)
    - Fall back to parent implementation if API call fails
    """
    
    def __init__(self, app, *, debug: bool = False, mouse: bool = True, size: Size | None = None):
        """
        Initialize driver with correct terminal size.
        
        Args:
            app: Textual App instance
            debug: Enable debug mode
            mouse: Enable mouse support
            size: Optional size override
        """
        # Detect actual window size BEFORE calling parent __init__
        if size is None and app is not None:
            detected_size = self._detect_window_size()
            if detected_size:
                size = detected_size
        
        # Call parent __init__ with detected size
        super().__init__(app, debug=debug, mouse=mouse, size=size)
    
    def _detect_window_size(self) -> Size | None:
        """
        Get actual console window size using Win32 API.
        
        Returns:
            Size: Terminal dimensions (columns, rows) or None if detection fails
        """
        try:
            # Win32 API constants
            STD_OUTPUT_HANDLE = -11
            
            # Get console handle
            kernel32 = ctypes.windll.kernel32
            h = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            
            # Define CONSOLE_SCREEN_BUFFER_INFO structure
            class COORD(ctypes.Structure):
                _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
            
            class SMALL_RECT(ctypes.Structure):
                _fields_ = [
                    ("Left", ctypes.c_short),
                    ("Top", ctypes.c_short),
                    ("Right", ctypes.c_short),
                    ("Bottom", ctypes.c_short),
                ]
            
            class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
                _fields_ = [
                    ("dwSize", COORD),
                    ("dwCursorPosition", COORD),
                    ("wAttributes", ctypes.c_ushort),
                    ("srWindow", SMALL_RECT),
                    ("dwMaximumWindowSize", COORD),
                ]
            
            # Get console info
            csbi = CONSOLE_SCREEN_BUFFER_INFO()
            res = kernel32.GetConsoleScreenBufferInfo(h, ctypes.byref(csbi))
            
            if res:
                # Use WINDOW size (srWindow), not buffer size (dwSize)
                width = csbi.srWindow.Right - csbi.srWindow.Left + 1
                height = csbi.srWindow.Bottom - csbi.srWindow.Top + 1
                
                # Sanity check (prevent 0-size or absurd values)
                if width > 0 and height > 0 and width < 500 and height < 200:
                    return Size(width, height)
            
        except Exception:
            # Silently fail and let parent handle it
            pass
        
        return None
