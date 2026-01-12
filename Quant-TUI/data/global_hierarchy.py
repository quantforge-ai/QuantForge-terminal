"""
Global Stocks Hierarchy - Regions → Countries → Sectors → Stocks
Comprehensive coverage of major stock markets worldwide
"""

GLOBAL_HIERARCHY = {
    "🌎 Americas": {
        "🇺🇸 United States": {
            "Tech": ["AAPL", "MSFT", "GOOGL", "NVDA", "META", "AMZN", "TSLA"],
            "Finance": ["JPM", "BAC", "WFC", "GS", "MS", "C", "AXP"],
            "Energy": ["XOM", "CVX", "COP", "SLB", "EOG"],
            "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "MRK"],
        },
        "🇨🇦 Canada": {
            "Tech": ["SHOP", "BB", "OTEX", "CSU.TO"],
            "Finance": ["RY", "TD", "BMO", "BNS", "CM"],
            "Energy": ["CNQ", "SU", "ENB", "TRP"],
        },
        "🇧🇷 Brazil": {
            "Finance": ["ITUB", "BBD", "BSBR"],
            "Energy": ["PBR", "VALE", "CSAN3.SA"],
            "Consumer": ["ABEV", "CBD"],
        },
        "🇲🇽 Mexico": {
            "Finance": ["GFNORTEO.MX", "GFINBURO.MX"],
            "Consumer": ["WALMEX.MX", "FEMSAUBD.MX"],
        },
        "🇦🇷 Argentina": {
            "Finance": ["GGAL", "BMA", "SUPV"],
            "Energy": ["YPF", "PAM"],
        },
        "🇨🇱 Chile": {
            "Mining": ["SQM", "CCU"],
            "Finance": ["BCH", "BSANTANDER.SN"],
        },
        "🇨🇴 Colombia": {
            "Finance": ["CIB", "EC"],
            "Energy": ["EC"],
        },
        "🇵🇪 Peru": {
            "Mining": ["BVN", "SCCO"],
        },
    },
    "🌏 Asia": {
        "🇮🇳 India": {
            "Tech": ["INFY.NS", "TCS.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"],
            "Finance": ["HDFC.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS"],
            "Energy": ["RELIANCE.NS", "ONGC.NS", "BPCL.NS", "IOC.NS"],
            "Auto": ["TATAMOTORS.NS", "MARUTI.NS", "M&M.NS"],
        },
        "🇯🇵 Japan": {
            "Tech": ["SONY", "6758.T", "6902.T", "6861.T"],
            "Finance": ["8306.T", "8316.T", "8411.T"],
            "Auto": ["TM", "HMC", "7267.T", "7269.T"],
        },
        "🇨🇳 China": {
            "Tech": ["BABA", "BIDU", "JD", "PDD", "TCEHY"],
            "Finance": ["LFC", "ACH", "CIHKY"],
            "Consumer": ["NIO", "XPEV", "LI"],
        },
        "🇭🇰 Hong Kong": {
            "Finance": ["0005.HK", "0011.HK", "0388.HK"],
            "Property": ["0016.HK", "0001.HK"],
        },
        "🇰🇷 South Korea": {
            "Tech": ["005930.KS", "000660.KS", "035420.KS"],
            "Auto": ["005380.KS", "000270.KS"],
        },
        "🇹🇼 Taiwan": {
            "Tech": ["TSM", "2330.TW", "2454.TW"],
            "Electronics": ["2317.TW", "2308.TW"],
        },
        "🇸🇬 Singapore": {
            "Finance": ["DBS", "OCBC", "UOB"],
            "REIT": ["A17U.SI", "C38U.SI"],
        },
        "🇮🇩 Indonesia": {
            "Finance": ["BBCA.JK", "BMRI.JK"],
            "Consumer": ["UNVR.JK", "TLKM.JK"],
        },
        "🇹🇭 Thailand": {
            "Finance": ["SCB.BK", "KBANK.BK"],
            "Energy": ["PTT.BK", "PTTEP.BK"],
        },
        "🇲🇾 Malaysia": {
            "Finance": ["MAYBANK.KL", "PBBANK.KL"],
            "Plantation": ["SIME.KL", "IOI.KL"],
        },
        "🇵🇭 Philippines": {
            "Finance": ["BDO", "MBT"],
            "Telecom": ["TEL", "GLO.PS"],
        },
        "🇻🇳 Vietnam": {
            "Finance": ["VCB.VN", "BID.VN"],
            "Real Estate": ["VIC.VN", "VHM.VN"],
        },
        "🇵🇰 Pakistan": {
            "Finance": ["MCB.KA", "UBL.KA"],
            "Energy": ["PPL.KA", "OGDC.KA"],
        },
        "🇧🇩 Bangladesh": {
            "Pharma": ["SQPHARMA.BD", "BEXIMCO.BD"],
        },
        "🇱🇰 Sri Lanka": {
            "Finance": ["JKH.N0000", "COMB.N0000"],
        },
    },
    "🌍 Europe": {
        "🇬🇧 UK": {
            "Finance": ["HSBC", "BARC", "LLOY", "NWG"],
            "Energy": ["BP", "SHEL", "SSE.L"],
            "Consumer": ["ULVR", "DGE", "RKT.L"],
        },
        "🇩🇪 Germany": {
            "Auto": ["VOW3.DE", "BMW.DE", "MBG.DE"],
            "Tech": ["SAP", "IFX.DE", "SIEGY"],
            "Industrial": ["SIE.DE", "BAS.DE"],
        },
        "🇫🇷 France": {
            "Luxury": ["MC.PA", "KER.PA", "RMS.PA"],
            "Finance": ["BNP.PA", "GLE.PA", "ACA.PA"],
            "Energy": ["TTE.PA", "ENGI.PA"],
        },
        "🇨🇭 Switzerland": {
            "Pharma": ["NOVN.SW", "ROG.SW"],
            "Finance": ["UBSG.SW", "CSGN.SW"],
            "Consumer": ["NESN.SW"],
        },
        "🇳🇱 Netherlands": {
            "Tech": ["ASML", "ASML.AS"],
            "Consumer": ["UNA.AS", "HEIA.AS"],
        },
        "🇪🇸 Spain": {
            "Finance": ["SAN.MC", "BBVA.MC"],
            "Energy": ["IBE.MC", "REE.MC"],
        },
        "🇮🇹 Italy": {
            "Finance": ["UCG.MI", "ISP.MI"],
            "Energy": ["ENI.MI", "ENEL.MI"],
        },
        "🇸🇪 Sweden": {
            "Tech": ["SPOT", "ERIC"],
            "Industrial": ["VOLV-B.ST", "ABB.ST"],
        },
        "🇳🇴 Norway": {
            "Energy": ["EQNR.OL", "DNO.OL"],
            "Shipping": ["GOGL.OL", "FRO.OL"],
        },
        "🇩🇰 Denmark": {
            "Pharma": ["NOVO-B.CO", "LUN.CO"],
            "Shipping": ["MAERSK-B.CO"],
        },
        "🇫🇮 Finland": {
            "Tech": ["NOKIA.HE", "TIETO.HE"],
            "Industrial": ["KNEBV.HE", "WRT1V.HE"],
        },
        "🇧🇪 Belgium": {
            "Pharma": ["UCB.BR", "GBLB.BR"],
        },
        "🇦🇹 Austria": {
            "Finance": ["EBS.VI", "RBI.VI"],
        },
        "🇵🇱 Poland": {
            "Finance": ["PKO.WA", "PEO.WA"],
        },
        "🇮🇪 Ireland": {
            "Tech": ["CRWD", "LSEG.L"],
        },
    },
    "🌍 Africa": {
        "🇿🇦 South Africa": {
            "Mining": ["AGL.JO", "BHP.JO", "ANG.JO"],
            "Finance": ["SBK.JO", "FSR.JO", "NED.JO"],
            "Retail": ["SHP.JO", "WHL.JO"],
        },
        "🇪🇬 Egypt": {
            "Finance": ["COMI.CA", "HRHO.CA"],
            "Real Estate": ["TMGH.CA", "PHDC.CA"],
        },
        "🇳🇬 Nigeria": {
            "Finance": ["ZENITHBANK.LG", "GTCO.LG"],
            "Consumer": ["DANGCEM.LG", "NESTLE.LG"],
        },
        "🇰🇪 Kenya": {
            "Finance": ["EQTY.NR", "KCB.NR"],
            "Telecom": ["SCOM.NR"],
        },
        "🇲🇦 Morocco": {
            "Finance": ["ATW.CS", "BCP.CS"],
        },
        "🇬🇭 Ghana": {
            "Finance": ["GCB.GH", "EGH.GH"],
        },
        "🇹🇿 Tanzania": {
            "Finance": ["CRDB.TZ", "NMB.TZ"],
        },
        "🇺🇬 Uganda": {
            "Finance": ["SBU.UG", "DFCU.UG"],
        },
    },
    "🌏 Frontier": {
        "🇦🇺 Australia": {
            "Mining": ["BHP.AX", "RIO.AX", "FMG.AX"],
            "Finance": ["CBA.AX", "NAB.AX", "WBC.AX", "ANZ.AX"],
            "Healthcare": ["CSL.AX", "COH.AX"],
        },
        "🇳🇿 New Zealand": {
            "Dairy": ["FCG.NZ", "SAN.NZ"],
            "Energy": ["MEL.NZ", "GNE.NZ"],
        },
    },
}

# Sample stocks to display in region overview (4 random from each region)
REGION_SAMPLES = {
    "🌎 Americas": [("AAPL", "+2.5%"), ("SHOP", "+1.8%"), ("ITUB", "-0.3%"), ("YPF", "+4.2%")],
    "🌏 Asia": [("TCS.NS", "+1.2%"), ("SONY", "+0.8%"), ("BABA", "-1.5%"), ("DBS", "+0.6%")],
    "🌍 Europe": [("HSBC", "+0.4%"), ("SAP", "+1.1%"), ("MC.PA", "+2.1%"), ("NOVN.SW", "-0.2%")],
    "🌍 Africa": [("AGL.JO", "+3.2%"), ("COMI.CA", "-0.8%"), ("GTCO.LG", "+1.5%"), ("EQTY.NR", "+0.9%")],
    "🌏 Frontier": [("BHP.AX", "+1.7%"), ("CBA.AX", "+0.5%"), ("CSL.AX", "+2.3%"), ("FCG.NZ", "-0.1%")],
}


# ═══════════════════════════════════════════════════════════════════════════════
# CRYPTO TAB - Cryptocurrency Categories (24/7 Markets)
# ═══════════════════════════════════════════════════════════════════════════════
CRYPTO_TRAINS = {
    "₿ Core Networks": [
        # Major blockchain platforms - Store of value & Smart contracts
        ("BTC-USD", "$97,250", "+2.8%", True),     # Bitcoin - Digital gold
        ("ETH-USD", "$3,450", "+3.2%", True),      # Ethereum - Smart contracts
        ("SOL-USD", "$185.30", "+5.1%", True),     # Solana - High throughput
        ("ADA-USD", "$0.92", "+1.5%", True),       # Cardano - Research-driven
        ("AVAX-USD", "$38.50", "+4.2%", True),     # Avalanche - Subnets
        ("DOT-USD", "$7.85", "-0.8%", False),      # Polkadot - Parachains
    ],
    "🔷 Scaling Layer": [
        # Scaling solutions for Ethereum
        ("MATIC-USD", "$0.98", "+2.1%", True),     # Polygon - L2 scaling
        ("ARB-USD", "$1.25", "+3.8%", True),       # Arbitrum - Optimistic rollup
        ("OP-USD", "$2.15", "+2.5%", True),        # Optimism - Superchain
        ("IMX-USD", "$1.85", "+1.9%", True),       # Immutable X - NFT gaming
        ("STRK-USD", "$0.75", "-1.2%", False),     # Starknet - ZK rollup
        ("LRC-USD", "$0.28", "+0.8%", True),       # Loopring - DEX
    ],
    "🏦 DeFi": [
        # Decentralized finance protocols
        ("UNI-USD", "$12.50", "+2.3%", True),      # Uniswap - DEX leader
        ("AAVE-USD", "$285.30", "+4.1%", True),    # Aave - Lending
        ("MKR-USD", "$1,850", "+1.8%", True),      # Maker - DAI stablecoin
        ("LDO-USD", "$2.45", "+3.5%", True),       # Lido - Liquid staking
        ("CRV-USD", "$0.65", "-0.5%", False),      # Curve - Stablecoin AMM
        ("SUSHI-USD", "$1.15", "+1.2%", True),     # SushiSwap - DEX
    ],
    "🎮 Gaming & Metaverse": [
        # Web3 gaming and virtual worlds
        ("SAND-USD", "$0.58", "+2.8%", True),      # Sandbox - Metaverse
        ("MANA-USD", "$0.52", "+1.9%", True),      # Decentraland - VR world
        ("AXS-USD", "$8.25", "+3.2%", True),       # Axie Infinity - Play-to-earn
        ("GALA-USD", "$0.045", "+5.5%", True),     # Gala Games - Gaming
        ("ENJ-USD", "$0.32", "-0.3%", False),      # Enjin - NFT gaming
        ("ILV-USD", "$52.30", "+2.1%", True),      # Illuvium - AAA gaming
    ],
    "🤖 AI & Infrastructure": [
        # AI tokens and infrastructure
        ("RNDR-USD", "$8.50", "+6.2%", True),      # Render - GPU compute
        ("FET-USD", "$2.25", "+4.8%", True),       # Fetch.ai - AI agents
        ("AGIX-USD", "$0.85", "+3.9%", True),      # SingularityNET - AI
        ("LINK-USD", "$18.50", "+2.1%", True),     # Chainlink - Oracles
        ("GRT-USD", "$0.22", "+1.5%", True),       # The Graph - Indexing
        ("FIL-USD", "$5.85", "-0.6%", False),      # Filecoin - Storage
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# FOREX TAB - Currency Pairs by Category
# ═══════════════════════════════════════════════════════════════════════════════
FOREX_TRAINS = {
    "💵 Major Pairs": [
        # G10 majors - Most liquid pairs
        ("EUR/USD", "1.0825", "+0.15%", True),     # Euro - Dollar
        ("GBP/USD", "1.2650", "+0.22%", True),     # Pound - Dollar
        ("USD/JPY", "157.85", "+0.35%", True),     # Dollar - Yen
        ("USD/CHF", "0.8925", "-0.12%", False),    # Dollar - Swiss
        ("AUD/USD", "0.6285", "+0.18%", True),     # Aussie - Dollar
        ("USD/CAD", "1.4385", "-0.08%", False),    # Dollar - Loonie
    ],
    "💶 Euro Crosses": [
        # EUR cross pairs
        ("EUR/GBP", "0.8555", "-0.05%", False),    # Euro - Pound
        ("EUR/JPY", "170.85", "+0.42%", True),     # Euro - Yen
        ("EUR/CHF", "0.9665", "+0.08%", True),     # Euro - Swiss
        ("EUR/AUD", "1.7225", "-0.15%", False),    # Euro - Aussie
        ("EUR/CAD", "1.5575", "+0.12%", True),     # Euro - Loonie
        ("EUR/NZD", "1.8450", "+0.25%", True),     # Euro - Kiwi
    ],
    "🌏 Asian Pairs": [
        # Asian currency pairs
        ("USD/CNH", "7.3285", "+0.18%", True),     # Dollar - Offshore Yuan
        ("USD/INR", "85.65", "+0.08%", True),      # Dollar - Rupee
        ("USD/SGD", "1.3625", "+0.05%", True),     # Dollar - Sing Dollar
        ("USD/HKD", "7.7865", "+0.01%", True),     # Dollar - HK Dollar
        ("USD/KRW", "1,485.50", "+0.22%", True),   # Dollar - Won
        ("USD/THB", "34.85", "-0.12%", False),     # Dollar - Baht
    ],
    "💹 Emerging Markets": [
        # EM currency pairs - Higher volatility
        ("USD/TRY", "35.85", "+0.85%", True),      # Dollar - Lira
        ("USD/ZAR", "18.45", "+0.32%", True),      # Dollar - Rand
        ("USD/MXN", "20.25", "-0.15%", False),     # Dollar - Peso
        ("USD/BRL", "6.15", "+0.28%", True),       # Dollar - Real
        ("USD/RUB", "102.50", "+0.45%", True),     # Dollar - Ruble
        ("USD/PLN", "4.08", "-0.08%", False),      # Dollar - Zloty
    ],
    "🥇 Commodity Currencies": [
        # Resource-linked currencies
        ("AUD/JPY", "99.25", "+0.38%", True),      # Aussie - Yen
        ("NZD/USD", "0.5865", "+0.12%", True),     # Kiwi - Dollar
        ("USD/NOK", "11.35", "-0.18%", False),     # Dollar - Krone
        ("CAD/JPY", "109.75", "+0.28%", True),     # Loonie - Yen
        ("AUD/NZD", "1.0725", "+0.05%", True),     # Trans-Tasman
        ("NZD/JPY", "92.55", "+0.42%", True),      # Kiwi - Yen
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# COMMODITIES TAB - Raw Materials & Futures
# ═══════════════════════════════════════════════════════════════════════════════
COMMODITIES_TRAINS = {
    "🛢️ Energy": [
        # Oil, Gas, and Energy futures
        ("CL=F", "$72.85", "+1.2%", True),         # WTI Crude Oil
        ("BZ=F", "$76.45", "+0.9%", True),         # Brent Crude
        ("NG=F", "$3.25", "-2.1%", False),         # Natural Gas
        ("RB=F", "$2.15", "+0.8%", True),          # RBOB Gasoline
        ("HO=F", "$2.45", "+1.1%", True),          # Heating Oil
        ("URA", "$28.50", "+3.2%", True),          # Uranium ETF
    ],
    "🥇 Precious Metals": [
        # Gold, Silver, Platinum, Palladium
        ("GC=F", "$2,685", "+0.45%", True),        # Gold Futures
        ("SI=F", "$31.25", "+1.2%", True),         # Silver Futures
        ("PL=F", "$985.50", "-0.3%", False),       # Platinum
        ("PA=F", "$1,025", "+0.8%", True),         # Palladium
        ("GLD", "$248.50", "+0.42%", True),        # Gold ETF
        ("SLV", "$28.85", "+1.15%", True),         # Silver ETF
    ],
    "🔩 Industrial Metals": [
        # Base metals for industry
        ("HG=F", "$4.25", "+0.65%", True),         # Copper
        ("ALI=F", "$2,550", "+0.35%", True),       # Aluminum
        ("ZN=F", "$2,850", "-0.22%", False),       # Zinc
        ("NI=F", "$16,250", "+0.48%", True),       # Nickel
        ("COPX", "$42.50", "+0.72%", True),        # Copper Miners ETF
        ("LIT", "$45.25", "+1.8%", True),          # Lithium ETF
    ],
    "🌾 Agriculture": [
        # Soft commodities and grains
        ("ZC=F", "$4.85", "+0.32%", True),         # Corn
        ("ZS=F", "$10.25", "-0.18%", False),       # Soybeans
        ("ZW=F", "$5.65", "+0.42%", True),         # Wheat
        ("CC=F", "$8,250", "+2.5%", True),         # Cocoa
        ("KC=F", "$3.25", "+1.8%", True),          # Coffee
        ("SB=F", "$0.22", "-0.65%", False),        # Sugar
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# INDICES TAB - Global Stock Market Benchmarks
# ═══════════════════════════════════════════════════════════════════════════════
INDICES_TRAINS = {
    "🇺🇸 US Indices": [
        # Major US stock market indices
        ("^GSPC", "5,985.50", "+0.52%", True),     # S&P 500
        ("^DJI", "42,850", "+0.38%", True),        # Dow Jones
        ("^IXIC", "19,850", "+0.75%", True),       # NASDAQ Composite
        ("^RUT", "2,285", "+0.65%", True),         # Russell 2000
        ("^VIX", "14.25", "-3.2%", False),         # VIX Volatility
        ("^SOX", "5,125", "+1.2%", True),          # Philadelphia Semi
    ],
    "🌏 Asia-Pacific Indices": [
        # Major Asian stock indices
        ("^N225", "39,850", "+0.85%", True),       # Nikkei 225
        ("000001.SS", "3,450", "+0.42%", True),    # Shanghai Composite
        ("^HSI", "19,850", "-0.35%", False),       # Hang Seng
        ("^NSEI", "23,850", "+0.65%", True),       # NIFTY 50
        ("^BSESN", "78,250", "+0.58%", True),      # SENSEX
        ("^AXJO", "8,285", "+0.32%", True),        # ASX 200
    ],
    "🇪🇺 European Indices": [
        # Major European stock indices
        ("^FTSE", "8,225", "+0.28%", True),        # FTSE 100
        ("^GDAXI", "19,850", "+0.45%", True),      # DAX 40
        ("^FCHI", "7,585", "+0.38%", True),        # CAC 40
        ("^STOXX50E", "4,850", "+0.42%", True),    # Euro Stoxx 50
        ("^IBEX", "11,650", "+0.25%", True),       # IBEX 35
        ("^SSMI", "11,925", "-0.12%", False),      # Swiss Market
    ],
    "🌍 Emerging Markets": [
        # EM stock indices
        ("^BVSP", "125,850", "+0.85%", True),      # Brazil Bovespa
        ("^MXX", "56,250", "+0.32%", True),        # Mexico IPC
        ("^TWII", "22,850", "+0.65%", True),       # Taiwan Weighted
        ("^KS11", "2,585", "+0.48%", True),        # KOSPI
        ("XU100.IS", "9,850", "+1.2%", True),      # BIST 100 Turkey
        ("^JKSE", "7,125", "-0.18%", False),       # Jakarta Composite
    ],
    "📊 Sector Indices": [
        # US Sector-specific indices
        ("^GSPE", "985.50", "+0.72%", True),       # S&P 500 Energy
        ("^GSPT", "3,250", "+0.95%", True),        # S&P 500 Tech
        ("^GSPF", "725.50", "+0.28%", True),       # S&P 500 Financials
        ("^GSPA", "1,485", "+0.35%", True),        # S&P 500 Healthcare
        ("^GSPU", "385.25", "-0.15%", False),      # S&P 500 Utilities
        ("^GSPM", "585.75", "+0.42%", True),       # S&P 500 Materials
    ],
}


def get_country_count():
    """Get total number of countries covered"""
    total = 0
    for region in GLOBAL_HIERARCHY.values():
        total += len(region)
    return total


def get_region_list():
    """Get list of all regions"""
    return list(GLOBAL_HIERARCHY.keys())
