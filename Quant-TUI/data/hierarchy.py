"""
Global Market Hierarchy Data Structure
Defines regions/categories and dummy ticker data for all asset classes
"""

# STOCKS - 5 Regions (48 countries total)
STOCKS_HIERARCHY = {
    "Americas": {
        "emoji": "🌎",
        "tickers": [
            "AAPL.US $180.50 +2.5%",
            "MSFT.US $415.20 +1.8%",
            "GOOGL.US $142.30 +1.2%",
            "TSLA.US $238.50 -2.1%",
            "NVDA.US $725.10 +3.5%",
        ]
    },
    "Asia-Pacific": {
        "emoji": "🌏",
        "tickers": [
            "TCG.HK ¥9,858 +1.8%",
            "RELIANCE.NS ₹2,450 +2.1%",
            "SONY.JP ¥12,450 +0.5%",
            "BABA.HK HK$590.30 -1.8%",
            "TSM.TW NT$580 +2.8%",
        ]
    },
    "Europe": {
        "emoji": "🌍",
        "tickers": [
            "HSBC.UK £6.05 +0.5%",
            "SAP.DE €158.20 +1.1%",
            "MC.FR €805.30 +2.3%",
            "ASML.NL €685.30 +1.8%",
            "NOVO.DK DKK280 -1.5%",
        ]
    },
    "MEA": {
        "emoji": "🌍",
        "tickers": [
            "AGL.ZA R 450.20 +1.2%",
            "MTN.ZA R110.50 -0.9%",
            "COMI.EG EGP2.50 +1.8%",
            "GTCO.NG ₦28.50 +0.9%",
            "EQTY.KE KSh62.80 +1.1%",
        ]
    },
    "Frontier": {
        "emoji": "🌎",
        "tickers": [
            "BHP.AU A$45.80 +1.7%",
            "CBA.AU A$112.30 +0.5%",
            "NAB.AU A$32.15 +0.8%",
            "WBC.AU A$27.50 +1.2%",
            "ANZ.AU A$28.30 +0.3%",
        ]
    }
}

# CRYPTO - 5 Categories
CRYPTO_HIERARCHY = {
    "Smart Contract Platforms": {
        "emoji": "⛓️",
        "tickers": [
            "BTC-USD $42,150 +2.5%",
            "ETH-USD $2,240 +3.1%",
            "BNB-USD $315 +1.8%",
            "ADA-USD $0.52 +4.2%",
            "SOL-USD $98.50 +5.5%",
        ]
    },
    "Scaling Solutions": {
        "emoji": "⚡",
        "tickers": [
            "MATIC-USD $0.88 +2.8%",
            "ARB-USD $1.25 +3.5%",
            "OP-USD $2.15 +4.1%",
            "LRC-USD $0.35 +2.2%",
            "IMX-USD $1.80 +3.8%",
        ]
    },
    "Decentralized Finance": {
        "emoji": "💰",
        "tickers": [
            "UNI-USD $6.50 +1.9%",
            "AAVE-USD $98.20 +2.5%",
            "MKR-USD $1,580 +1.2%",
            "COMP-USD $52.30 +0.8%",
            "CRV-USD $0.95 +3.1%",
        ]
    },
    "Web3 Gaming & NFTs": {
        "emoji": "🎮",
        "tickers": [
            "AXS-USD $7.80 +4.5%",
            "SAND-USD $0.52 +3.2%",
            "MANA-USD $0.48 +2.8%",
            "GALA-USD $0.025 +5.1%",
            "ENJ-USD $0.38 +2.9%",
        ]
    },
    "AI & Data Networks": {
        "emoji": "🤖",
        "tickers": [
            "FET-USD $0.68 +6.2%",
            "OCEAN-USD $0.42 +4.8%",
            "GRT-USD $0.18 +3.5%",
            "RNDR-USD $3.25 +5.8%",
            "AGIX-USD $0.35 +4.2%",
        ]
    },
}

# FOREX - 5 Categories
FOREX_HIERARCHY = {
    "Major Pairs": {
        "emoji": "💱",
        "tickers": [
            "EUR/USD 1.0825 +0.15%",
            "GBP/USD 1.2660 +0.25%",
            "USD/JPY 147.85 -0.35%",
            "USD/CHF 0.8925 -0.12%",
            "USD/CAD 1.4350 -0.08%",
        ]
    },
    "Euro Crosses": {
        "emoji": "€",
        "tickers": [
            "EUR/GBP 0.8555 -0.05%",
            "EUR/JPY 170.85 +0.42%",
            "EUR/CHF 0.9625 +0.12%",
            "EUR/AUD 1.7225 -0.32%",
            "EUR/CAD 1.5575 +0.12%",
        ]
    },
    "Asian Pairs": {
        "emoji": "🏯",
        "tickers": [
            "USD/CNY 7.3285 -0.18%",
            "USD/INR 85.66 +0.08%",
            "USD/KRW 1,385.5 +0.22%",
            "USD/THW 34.85 +0.32%",
            "USD/MYR 4.7865 +0.01%",
        ]
    },
    "Emerging Markets": {
        "emoji": "🌱",
        "tickers": [
            "USD/BRL 6.15 +0.25%",
            "USD/ZAR 18.05 +0.32%",
            "USD/TRY 35.85 +0.85%",
            "USD/MXN 16.92 +0.15%",
            "USD/RUB 102.35 +0.28%",
        ]
    },
    "Commodity Currencies": {
        "emoji": "⛏️",
        "tickers": [
            "AUD/USD 0.6285 +0.38%",
            "NZD/USD 0.5865 +0.12%",
            "USD/CAD 1.4350 -0.08%",
            "CAD/JPY 109.75 +0.28%",
            "AUD/NZD 1.0725 +0.05%",
        ]
    }
}

# COMMODITIES - 5 Categories
COMMODITIES_HIERARCHY = {
    "Energy": {
        "emoji": "⛽",
        "tickers": [
            "CLCF $72.85 +1.2%",
            "BZCF $76.05 +0.9%",
            "MGCF $2.05 +1.1%",
            "RBCF $2.10 +0.8%",
            "HOCF $2.25 +1.5%",
            "COAL $135.0 -0.5%",
            "ETHNL $2.45 +0.3%",
        ]
    },
    "Precious Metals": {
        "emoji": "💎",
        "tickers": [
            "GCCF $2,085.50 +0.82%",
            "SICF $23.25 -0.1%",
            "PLCF $985.30 +0.8%",
            "PDCF $1,050 +1.2%",
            "GLDCF $248.05 +0.12%",
            "SLVCF $26.05 -0.15%",
        ]
    },
    "Industrial Metals": {
        "emoji": "🔧",
        "tickers": [
            "HGCF $4.25 +0.65%",
            "ZHCF $2,450 +0.35%",
            "NICF $16.50 -1.1%",
            "LHCF $2,125 +1.5%",
            "ALCF $2,550 +0.85%",
            "TINCF $25,800 +0.5%",
            "LITH $13,500 -2.1%",
        ]
    },
    "Agri: Grains & Oilseeds": {
        "emoji": "🌾",
        "tickers": [
            "ZCCF $4.65 -0.32%",
            "ZSCF $11.58 +2.1%",
            "ZWCF $6.15 +1.5%",
            "ZOCF $3.25 -0.12%",
            "ZMCF $385.0 +0.5%",
        ]
    },
    "Agri: Softs & Meats": {
        "emoji": "☕",
        "tickers": [
            "KCCF $1.85 +4.2%",
            "SBCF $0.22 -0.5%",
            "CCCF $4,250 +2.1%",
            "LCCF $185.30 +0.42%",
            "LHCF $88.25 -0.12%",
            "OJCF $3.85 +0.9%",
            "CTCF $0.85 +1.1%",
        ]
    }
}

# INDICES - 5 Categories
INDICES_HIERARCHY = {
    "US Indices": {
        "emoji": "🇺🇸",
        "tickers": [
            "^GSPC 5,985.50 +0.35%",
            "^DJI 42,850 +0.38%",
            "^IXIC 19,850 +0.75%",
            "^RUT 2,285 +0.65%",
            "^VIX 14.25 -3.2%",
        ]
    },
    "Asia-Pacific Indices": {
        "emoji": "🌏",
        "tickers": [
            "^N225 39,850 +0.85%",
            "^HSI 19,850 +0.42%",
            "^NSEI 21,925 +0.65%",
            "^SSEC 3,120 -0.18%",
            "^AXJO 8,285 +0.32%",
        ]
    },
    "European Indices": {
        "emoji": "🇪🇺",
        "tickers": [
            "^FTSE 8,225 +0.28%",
            "^GDAXI 19,850 +0.45%",
            "^FCHI 7,585 +0.42%",
            "^STOXX50 4,985 +0.35%",
            "^IBEX 11,650 +0.25%",
        ]
    },
    "Emerging Markets": {
        "emoji": "🌱",
        "tickers": [
            "^BVSP 125,850 +0.85%",
            "^MXX 56,250 +0.32%",
            "^N11I 2,585 +0.45%",
            "^JKSE 7,125 -0.18%",
            "^KLSE 9,450 +1.2%",
        ]
    },
    "Sector Indices": {
        "emoji": "📊",
        "tickers": [
            "^GSDA 1,985.70 +0.35%",
            "^GSPF 725.50 +0.42%",
            "^GSPH 1,485 +0.35%",
            "^GSPE 1,025 +0.28%",
            "^GSPU 855.70 +0.82%",
        ]
    }
}

# Mode to Hierarchy mapping
MODE_HIERARCHY = {
    "STOCKS": STOCKS_HIERARCHY,
    "CRYPTO": CRYPTO_HIERARCHY,
    "FOREX": FOREX_HIERARCHY,
    "COMMODITIES": COMMODITIES_HIERARCHY,
    "INDICES": INDICES_HIERARCHY,
}

# Mode-specific headers
MODE_HEADERS = {
    "STOCKS": "Global Stocks by Region",
    "CRYPTO": "Crypto Markets - 24/7 Live",
    "FOREX": "Forex Markets - 24/7 Live",
    "COMMODITIES": "Commodities & Futures - Live",
    "INDICES": "Global Indices - Live Benchmarks",
}
