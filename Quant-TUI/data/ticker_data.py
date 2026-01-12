"""
Ticker Data for QuantTerminal
Contains icons and specific ticker strings for each mode.
"""

MODE_ICONS = {
    "STOCKS": "📊",
    "CRYPTO": "₿",
    "FOREX": "🌍",
    "COMMODITIES": "🥇",
    "INDICES": "📈"
}

# Pre-formatted ticker strings matching the reference image structure:
# ICON MODE [TIMEZONE] | TIME SYMBOL PRICE CHANGE | ...
TICKER_DATA = {
    "GLOBAL": "🌍 GLOBAL TRENDING [IST] | 15:54 AAPL 185.20 +1.2% | 15:54 BTC 42500 -1.5% | 15:54 GOLD 2035.2 +0.5% | 15:54 NVDA 725.10 +3.5% | 15:54 ETH 2250 +0.4% | 15:54 CRUDE OIL 75.4 -1.2% | 15:54 TSLA 175.40 -2.4% | 15:54 ^GSPC 4,785 +0.65%",
    "STOCKS": "📊 STOCKS [IST] | 15:54 AAPL 185.20 +1.2% | 15:54 MSFT 412.50 +0.8% | 15:54 RELIANCE.NS 2950.0 +2.1% | 15:54 MELI 1650.0 +4.2% | 15:54 TSLA 175.40 -2.4% | 15:54 NVDA 725.10 +3.5% | 15:54 AMZN 178.90 +1.1%",
    "CRYPTO": "₿ CRYPTO [IST] | 15:54 BTC 42500 -1.5% | 15:54 ETH 2250 +0.4% | 15:54 SOL 95.5 +5.2% | 15:54 BNB 310.2 -0.8% | 15:54 ADA 0.58 +1.5% | 15:54 AVAX 38.5 +4.2% | 15:54 DOT 7.85 -0.6%",
    "FOREX": "🌍 FOREX [IST] | 15:54 EUR/USD 1.085 -0.1% | 15:54 USD/JPY 148.2 +0.4% | 15:54 GBP/USD 1.265 -0.2% | 15:54 AUD/USD 0.655 +0.1% | 15:54 USD/CHF 0.88 -0.05% | 15:54 USD/CAD 1.35 +0.12% | 15:54 EUR/GBP 0.85 -0.02%",
    "COMMODITIES": "🥇 COMMODITIES [IST] | 15:54 GOLD 2035.2 +0.5% | 15:54 CRUDE OIL 75.4 -1.2% | 15:54 SILVER 22.8 +0.8% | 15:54 COPPER 3.8 -0.4% | 15:54 NAT GAS 2.15 -2.1% | 15:54 PLATINUM 985.5 +0.3% | 15:54 BRENT 81.2 -0.9%",
    "INDICES": "📈 INDICES [IST] | 15:54 ^DJI 37,850 +0.45% | 15:54 ^IXIC 15,120 +1.2% | 15:54 ^GSPC 4,785 +0.65% | 15:54 ^NSEI 21,750 +0.85% | 15:54 ^FTSE 7,620 -0.15% | 15:54 ^N225 33,450 +0.55% | 15:54 ^HSI 16,580 -0.45%"
}
