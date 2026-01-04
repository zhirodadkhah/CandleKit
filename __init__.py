"""
Candlestick pattern recognition library for technical analysis.
"""

from .utils import CandlePatterns, scan_symbol, detect_pattern_at_index, scan_symbol_df

__all__ = ['CandlePatterns', 'scan_symbol', 'detect_pattern_at_index', 'scan_symbol_df']

__version__ = '1.0.1'
__author__ = 'Zhiro Dadkhah'