import os
import shutil

# Method 1: os.get_terminal_size()
try:
    size = os.get_terminal_size()
    print(f"Method 1 (os.get_terminal_size): {size.columns} cols × {size.lines} rows")
except:
    print("Method 1 failed")

# Method 2: shutil
try:
    size = shutil.get_terminal_size()
    print(f"Method 2 (shutil.get_terminal_size): {size.columns} cols × {size.lines} rows")
except:
    print("Method 2 failed")

# Method 3: Environment variables
print(f"\nEnvironment Variables:")
print(f"COLUMNS: {os.environ.get('COLUMNS', 'not set')}")
print(f"LINES: {os.environ.get('LINES', 'not set')}")

input("\nPress Enter to close...")
