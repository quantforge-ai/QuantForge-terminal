"""
Debug Script - Check if ResponsiveWindowsDriver is Actually Running
"""
import sys
import os

# Add project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("RESPONSIVE DRIVER DEBUG CHECK")
print("=" * 70)

# Test 1: Can we import the driver?
print("\n1. Testing Driver Import...")
try:
    from drivers.responsive_windows_driver import ResponsiveWindowsDriver
    print("   ✅ ResponsiveWindowsDriver imported successfully")
except ImportError as e:
    print(f"   ❌ FAILED to import: {e}")
    print("   → Driver won't be used!")
    exit(1)

# Test 2: Can we instantiate it?
print("\n2. Testing Driver Instantiation...")
try:
    class MockApp:
        pass
    
    driver = ResponsiveWindowsDriver(MockApp(), debug=True, mouse=True)
    print(f"   ✅ Driver instantiated")
    print(f"   → Driver class: {type(driver).__name__}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 3: What size does it detect?
print("\n3. Testing Size Detection...")
try:
    detected = driver._detect_window_size()
    if detected:
        print(f"   ✅ Detected size: {detected.width} × {detected.height}")
    else:
        print(f"   ❌ Detection returned None")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 4: Run the actual app and check driver
print("\n4. Running MainDashboard to verify driver is used...")
print("   (Launching app - press 'q' to quit)")
print("=" * 70)

from Quant_TUI.app.main_dashboard import MainDashboard

class DebugDashboard(MainDashboard):
    def on_mount(self):
        # Check what driver we're using
        driver_class = type(self.driver).__name__
        self.notify(f"Driver: {driver_class} | Size: {self.size}")
        
        # Call parent on_mount
        super().on_mount()

app = DebugDashboard()
app.run()
