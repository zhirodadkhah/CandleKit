from enum import Enum
from typing import Callable
from .patterns import *
import pandas as pd


from enum import Enum
from typing import Callable

class CandlePatterns(Enum):
    # Format: (candles: int, func: Callable, signal_type: str, pattern_name: str)

    # --- SINGLE-CANDLE PATTERNS ---
    Doji = (1, is_doji, "neutral", "Doji")
    Hammer = (1, is_hammer, "bullish", "Hammer")
    ShootingStar = (1, is_shooting_star, "bearish", "Shooting Star")
    BullishBeltHold = (1, is_bullish_belt_hold, "bullish", "Bullish Belt Hold")
    BearishBeltHold = (1, is_bearish_belt_hold, "bearish", "Bearish Belt Hold")
    BullishMarubozu = (1, is_bullish_marubozu, "bullish", "Bullish Marubozu")
    BearishMarubozu = (1, is_bearish_marubozu, "bearish", "Bearish Marubozu")

    # --- TWO-CANDLE PATTERNS ---
    BullishEngulfing = (2, is_bullish_engulfing, "bullish", "Bullish Engulfing")
    BearishEngulfing = (2, is_bearish_engulfing, "bearish", "Bearish Engulfing")
    PiercingLine = (2, is_piercing_line, "bullish", "Piercing Line")
    DarkCloudCover = (2, is_dark_cloud_cover, "bearish", "Dark Cloud Cover")
    HaramiCrossBullish = (2, is_harami_cross_bullish, "bullish", "Bullish Harami Cross")
    HaramiCrossBearish = (2, is_harami_cross_bearish, "bearish", "Bearish Harami Cross")
    KickingBullish = (2, is_kicking_bullish, "bullish", "Bullish Kicking")
    KickingBearish = (2, is_kicking_bearish, "bearish", "Bearish Kicking")

    # --- THREE-CANDLE PATTERNS ---
    MorningDojiStar = (3, is_morning_doji_star, "bullish", "Morning Doji Star")
    EveningDojiStar = (3, is_evening_doji_star, "bearish", "Evening Doji Star")
    MorningStar = (3, is_morning_star, "bullish", "Morning Star")
    EveningStar = (3, is_evening_star, "bearish", "Evening Star")
    ThreeWhiteSoldiers = (3, is_three_white_soldiers, "bullish", "Three White Soldiers")
    ThreeBlackCrows = (3, is_three_black_crows, "bearish", "Three Black Crows")
    ThreeInsideUp = (3, is_three_inside_up, "bullish", "Three Inside Up")
    ThreeOutsideUp = (3, is_three_outside_up, "bullish", "Three Outside Up")

    # --- FIVE-CANDLE PATTERNS ---
    RisingThreeMethods = (5, is_rising_three_methods, "bullish", "Rising Three Methods")
    FallingThreeMethods = (5, is_falling_three_methods, "bearish", "Falling Three Methods")
    MatHold = (5, is_mat_hold, "bullish", "Mat Hold")

    def __init__(self, candles: int, func: Callable, signal_type: str, pattern_name: str):
        self.candles = candles
        self.func = func
        self.signal_type = signal_type
        self.pattern_name = pattern_name  # <-- NEW FIELD



def detect_pattern_at_index(
    pattern: CandlePatterns,
    df,
    index: int,
    **kwargs
) -> bool:
    """
    Detect whether a given candlekit pattern occurs ending at a specific index in a price DataFrame.

    This function dynamically constructs the required number of `CandleStick` objects
    (1, 2, 3, or 5) based on the pattern definition and passes them to the pattern's
    detection function along with any optional keyword arguments (e.g., `min_body_ratio`).

    :param pattern: A member of the `CandleStickPatterns` enum describing the pattern to detect.
    :param df: A pandas DataFrame containing OHLC columns: 'Open', 'High', 'Low', 'Close'.
    :param index: The row index in `df` where the pattern is expected to end (0-based).
    :param **kwargs: Optional keyword arguments passed directly to the pattern's detection function
                     (e.g., `min_body_ratio`, `max_body_ratio`). These are pattern-specific.
    :return: `True` if the pattern is detected at the given index; `False` otherwise.
    :raises IndexError: If `index` is out of bounds or insufficient history exists for the pattern.
    """
    if index + 1 < pattern.candles:
        return False

    # Build candle list in chronological order: [oldest, ..., newest]
    if pattern.candles == 5:
        candles = [CandleStick(df, index - i) for i in range(4, -1, -1)]
        return pattern.func(candles, **kwargs)
    else:
        candles = [CandleStick(df, index - i) for i in reversed(range(pattern.candles))]
        return pattern.func(*candles, **kwargs)


def scan_symbol(
    df,
    patterns: list[CandlePatterns] = None
) -> list[tuple[int, str, str]]:
    """
    Scan an entire price series for all occurrences of specified candlekit patterns.

    :param df: A pandas DataFrame with columns 'Open', 'High', 'Low', 'Close'.
               Must have at least one row.
    :param patterns: Optional list of `CandleStickPatterns` to scan for.
                     If `None`, all defined patterns are used (default behavior).
    :return: A list of detected patterns, where each item is a tuple:
               `(index: int, pattern_name: str, signal_type: str)`.
    :note: This function uses default parameter values for pattern-specific thresholds
           (as defined in each detection function). To customize thresholds,
           use `detect_pattern_at_index` directly or enhance this function with kwargs.
    """
    if patterns is None:
        patterns = list(CandlePatterns)

    results = []
    for i in range(len(df)):
        for pat in patterns:
            if detect_pattern_at_index(pat, df, i):
                results.append((i, pat.name, pat.signal_type))
    return results


def scan_symbol_df(
    df,
    patterns: list[CandlePatterns] = None
) -> pd.DataFrame:
    """
    Scan for candlekit patterns and return results as a pandas DataFrame.

    Columns:
        - 'symbol': ticker symbol
        - 'index': row index in original df where pattern ends
        - 'date': date of the pattern (if 'date' column exists in df)
        - 'pattern_name': human-readable name (e.g., 'Hammer')
        - 'signal_type': 'bullish', 'bearish', or 'neutral'
        - 'candles': number of candles in the pattern

    Returns:
        pd.DataFrame with detected patterns, empty if none found.
    """

    results = scan_symbol(df, patterns)

    if not results:
        return pd.DataFrame(columns=['index', 'pattern_name', 'signal_type', 'candles'])

    # Build records
    records = []
    for idx, pattern_enum_name, signal_type in results:
        pattern_member = CandlePatterns[pattern_enum_name]
        record = {
            'index': idx,
            'pattern_name': pattern_member.pattern_name,
            'signal_type': signal_type,
            'candles': pattern_member.candles
        }
        records.append(record)

    return pd.DataFrame(records)