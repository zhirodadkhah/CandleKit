"""
Candlestick pattern recognition library for technical analysis.
"""
from .utils import CandlePatterns, scan_symbol, detect_pattern_at_index

__all__ = ['CandlePatterns', 'scan_symbol', 'detect_pattern_at_index']

__version__ = '1.0.0'
__author__ = 'Zhiro Dadkhah'
