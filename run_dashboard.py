# Quick run script for Main Dashboard
# Usage: python run_dashboard.py

import sys
from pathlib import Path

# Add Quant-TUI directory to path (handles hyphenated name)
quant_tui_path = Path(__file__).parent / "Quant-TUI"
sys.path.insert(0, str(quant_tui_path))

# Now we can import from app module
from app.main_dashboard import MainDashboard

if __name__ == "__main__":
    print("🚀 Launching Quant-TUI Dashboard...")
    app = MainDashboard()
    app.run()
