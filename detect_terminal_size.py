#!/usr/bin/env python3
"""
Terminal Size Detector
Run this in different terminal launch modes to see exact dimensions
"""
import os
import shutil

def detect_size():
    print("\n" + "="*60)
    print("   TERMINAL SIZE DETECTION")
    print("="*60 + "\n")
    
    # Method 1: os.get_terminal_size()
    try:
        size = os.get_terminal_size()
        print(f"📏 Method 1 (os.get_terminal_size):")
        print(f"   Columns: {size.columns}")
        print(f"   Rows:    {size.lines}")
        print(f"   Total:   {size.columns} × {size.lines}\n")
    except Exception as e:
        print(f"❌ Method 1 failed: {e}\n")
    
    # Method 2: shutil.get_terminal_size()
    try:
        size = shutil.get_terminal_size()
        print(f"📐 Method 2 (shutil.get_terminal_size):")
        print(f"   Columns: {size.columns}")
        print(f"   Rows:    {size.lines}")
        print(f"   Total:   {size.columns} × {size.lines}\n")
    except Exception as e:
        print(f"❌ Method 2 failed: {e}\n")
    
    # Method 3: Windows specific
    try:
        import ctypes
        from ctypes import wintypes
        
        # Get console screen buffer info
        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
        
        class SMALL_RECT(ctypes.Structure):
            _fields_ = [("Left", ctypes.c_short), ("Top", ctypes.c_short),
                       ("Right", ctypes.c_short), ("Bottom", ctypes.c_short)]
        
        class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
            _fields_ = [("dwSize", COORD),
                       ("dwCursorPosition", COORD),
                       ("wAttributes", wintypes.WORD),
                       ("srWindow", SMALL_RECT),
                       ("dwMaximumWindowSize", COORD)]
        
        h = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(h, ctypes.byref(csbi))
        
        # Window size (what you actually see)
        window_width = csbi.srWindow.Right - csbi.srWindow.Left + 1
        window_height = csbi.srWindow.Bottom - csbi.srWindow.Top + 1
        
        # Buffer size (total scrollback)
        buffer_width = csbi.dwSize.X
        buffer_height = csbi.dwSize.Y
        
        # Maximum possible size
        max_width = csbi.dwMaximumWindowSize.X
        max_height = csbi.dwMaximumWindowSize.Y
        
        print(f"🪟 Method 3 (Windows Console API):")
        print(f"   Window Size:  {window_width} × {window_height}")
        print(f"   Buffer Size:  {buffer_width} × {buffer_height}")
        print(f"   Max Possible: {max_width} × {max_height}\n")
        
    except Exception as e:
        print(f"❌ Method 3 failed: {e}\n")
    
    # Summary
    print("="*60)
    print("SUMMARY - Use this for QuantForge Terminal:")
    print("="*60)
    try:
        size = os.get_terminal_size()
        print(f"\n✅ Your current terminal is: {size.columns} columns × {size.lines} rows\n")
        
        # Categorize
        if size.columns <= 80 and size.lines <= 25:
            print("📦 Size category: SMALL (Legacy default)")
        elif size.columns <= 120 and size.lines <= 30:
            print("📦 Size category: MEDIUM (Modern default)")
        elif size.columns <= 150 and size.lines <= 40:
            print("📦 Size category: LARGE (Custom/Maximized)")
        else:
            print("📦 Size category: EXTRA LARGE (Ultra-wide/4K)")
    except:
        pass
    
    print("\n" + "="*60 + "\n")
    input("Press Enter to exit...")

if __name__ == "__main__":
    detect_size()
