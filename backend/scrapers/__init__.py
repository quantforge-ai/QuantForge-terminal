"""
Multi-Source Data Scrapers

QuantTerminal's data layer: YFinance for quotes (reliable)
"""

from .yahoo_scraper import YFinanceScraper
from .aggregator import MultiSourceAggregator

__all__ = [
    'YFinanceScraper',
    'MultiSourceAggregator'
]
