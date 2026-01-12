"""
Portfolio Strategy Models for 2026
Defines target allocations and strategy rationale.
"""

STRATEGY_MODELS = {
    "balanced_core": {
        "name": "Balanced Core",
        "risk": "Low-Medium",
        "description": "Diversified base for steady growth. Focus on cooling inflation.",
        "targets": {
            "Tech": 40,
            "ForeX": 30,
            "Commodity": 20,
            "Crypto": 10
        },
        "color": "cyan"
    },
    "growth_tech": {
        "name": "Growth Tech Tilt",
        "risk": "Medium-High",
        "description": "Heavy bets on AI buildout and industrial power.",
        "targets": {
            "Tech": 60,
            "Crypto": 20,
            "Auto": 10,
            "Commodity": 10
        },
        "color": "magenta"
    },
    "income_fortress": {
        "name": "Income Fortress",
        "risk": "Low",
        "description": "Yield hunters' sanctuary with stable sectors.",
        "targets": {
            "Tech": 30,
            "ForeX": 50,
            "Commodity": 20
        },
        "color": "#00ff88"
    },
    "frontier_edge": {
        "name": "EM Frontier Edge",
        "risk": "High",
        "description": "Focus on high-growth regions and commodities.",
        "targets": {
            "ForeX": 40,
            "Commodity": 30,
            "Crypto": 20,
            "Tech": 10
        },
        "color": "yellow"
    },
    "sustainable_yield": {
        "name": "Sustainable Yield",
        "risk": "Medium",
        "description": "Eco-conscious energy and sustainable tech plays.",
        "targets": {
            "Tech": 40,
            "Auto": 30,
            "Commodity": 30
        },
        "color": "#aaff00"
    },
    "defensive_buffer": {
        "name": "Defensive Buffer",
        "risk": "Low",
        "description": "High cash yields to weather geopolitical volatility.",
        "targets": {
            "ForeX": 60,
            "Commodity": 20,
            "Tech": 20
        },
        "color": "#888888"
    },
    "ai_power_play": {
        "name": "🔒 AI Power Play (Coming Soon)",
        "risk": "High",
        "description": "The 'Picks & Shovels' of AI: Tech + Energy Grid Utilities.",
        "targets": {
            "Tech": 70,
            "Commodity": 20,
            "Crypto": 10
        },
        "color": "#888888"  # Grayed out to show it's locked
    }
}
