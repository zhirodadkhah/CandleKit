from .entity import CandleStick
import math

# --- Shared helpers ---
def is_thick_enough(candle: CandleStick, min_ratio: float) -> bool:
    """Check if candle has a thick body (strong conviction), regardless of direction.
    :param candle: The candlestick to evaluate
    :param min_ratio: Minimum body-to-total-length ratio
    """
    return candle.body_ratio >= min_ratio

def is_thick_bearish(candle: CandleStick, min_ratio: float) -> bool:
    """Check if candle is bearish and has a thick body.
    :param candle: The candlestick to evaluate
    :param min_ratio: Minimum body-to-total-length ratio
    """
    return not candle.is_bullish and candle.body_ratio >= min_ratio

def is_thick_bullish(candle: CandleStick, min_ratio: float) -> bool:
    """Check if candle is bullish and has a thick body.
    :param candle: The candlestick to evaluate
    :param min_ratio: Minimum body-to-total-length ratio
    """
    return candle.is_bullish and candle.body_ratio >= min_ratio

def is_thin_enough(candle: CandleStick, max_ratio: float) -> bool:
    """Check if candle has a thin body (indecision), regardless of direction.
    :param candle: The candlestick to evaluate
    :param max_ratio: Maximum body-to-total-length ratio
    """
    return candle.body_ratio <= max_ratio

def is_thin_bearish(candle: CandleStick, max_ratio: float) -> bool:
    """Check if candle is bearish and has a thin body.
    :param candle: The candlestick to evaluate
    :param max_ratio: Maximum body-to-total-length ratio
    """
    return not candle.is_bullish and candle.body_ratio <= max_ratio

def is_thin_bullish(candle: CandleStick, max_ratio: float) -> bool:
    """Check if candle is bullish and has a thin body.
    :param candle: The candlestick to evaluate
    :param max_ratio: Maximum body-to-total-length ratio
    """
    return candle.is_bullish and candle.body_ratio <= max_ratio

def gap_down(prev: CandleStick, curr: CandleStick) -> bool:
    """Check if current candle gaps down (open < previous close).
    :param prev: Previous candle
    :param curr: Current candle
    """
    return curr.open < prev.close

def gap_up(prev: CandleStick, curr: CandleStick) -> bool:
    """Check if current candle gaps up (open > previous close).
    :param prev: Previous candle
    :param curr: Current candle
    """
    return curr.open > prev.close

def body_engulf(prev: CandleStick, curr: CandleStick) -> bool:
    """Check if current candle's body engulfs previous candle's body.
    :param prev: Previous candle
    :param curr: Current candle
    """
    return curr.body_high > prev.body_high and curr.body_low < prev.body_low

def wick_engulf(prev: CandleStick, curr: CandleStick) -> bool:
    """Check if current candle's wicks engulf previous candle's wicks.
    :param prev: Previous candle
    :param curr: Current candle
    """
    return curr.high > prev.high and curr.low < prev.low

def body_contained(inner: CandleStick, outer: CandleStick) -> bool:
    """Check if inner candle's body is completely within outer candle's body.
    :param inner: Inner (smaller) candle
    :param outer: Outer (larger) candle
    """
    return inner.body_high <= outer.body_high and inner.body_low >= outer.body_low

def _valid_candle(candle: CandleStick) -> bool:
    return candle.length > 0

def _rel_close(a: float, b: float, rel_tol: float = 1e-4, abs_tol: float = 1e-8) -> bool:
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

# --------------------------
# SINGLE-CANDLE PATTERNS (Nison - Japanese Candlestick Charting Techniques, 2nd Ed.)
# --------------------------

def is_doji(candle: CandleStick, max_body_ratio: float = 0.1) -> bool:
    """Detect general Doji pattern (indecision).
    :param candle: The candlestick to evaluate
    :param max_body_ratio: Maximum body-to-total-length ratio
    :ref: Nison p. 38
    """
    return _valid_candle(candle) and is_thin_enough(candle, max_body_ratio)

def is_hammer(candle: CandleStick,
              max_body_ratio: float = 0.25,
              min_lower_wick_to_body: float = 2.0,
              max_upper_wick_ratio: float = 0.33) -> bool:
    """Detect Hammer pattern (bullish reversal after downtrend).
    :param candle: The candlestick to evaluate
    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_lower_wick_to_body: Minimum required ratio of lower wick to body length
    :param max_upper_wick_ratio: Maximum allowed upper wick as fraction of total length
    :ref: Nison p. 27
    """
    if not _valid_candle(candle):
        return False
    return (is_thin_enough(candle, max_body_ratio)
            and candle.bottom_wick >= candle.body_length * min_lower_wick_to_body
            and candle.top_wick <= max_upper_wick_ratio * candle.length)

def is_shooting_star(candle: CandleStick,
                     max_body_ratio: float = 0.25,
                     min_upper_wick_to_body: float = 2.0,
                     max_lower_wick_ratio: float = 0.33) -> bool:
    """Detect Shooting Star pattern (bearish reversal after uptrend).
    :param candle: The candlestick to evaluate
    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_upper_wick_to_body: Minimum required ratio of upper wick to body length
    :param max_lower_wick_ratio: Maximum allowed lower wick as fraction of total length
    :ref: Nison p. 28
    """
    if not _valid_candle(candle):
        return False
    return (is_thin_enough(candle, max_body_ratio)
            and candle.top_wick >= candle.body_length * min_upper_wick_to_body
            and candle.bottom_wick <= max_lower_wick_ratio * candle.length)

def is_bullish_belt_hold(candle: CandleStick, min_body_ratio: float = 0.95) -> bool:
    """Detect Bullish Belt Hold.
    :param candle: The candlestick to evaluate
    :param min_body_ratio: Minimum body-to-total-length ratio
    :ref: Nison p. 32
    """
    if not _valid_candle(candle) or not candle.is_bullish:
        return False
    # No lower shadow (open = low)
    # Close near high
    return (is_thick_enough(candle, min_body_ratio)
            and _rel_close(candle.open, candle.low, abs_tol=1e-5)
            and _rel_close(candle.close, candle.high, abs_tol=1e-5))

def is_bearish_belt_hold(candle: CandleStick, min_body_ratio: float = 0.95) -> bool:
    """Detect Bearish Belt Hold.
    :param candle: The candlestick to evaluate
    :param min_body_ratio: Minimum body-to-total-length ratio
    :ref: Nison p. 32
    """
    if not _valid_candle(candle) or candle.is_bullish:
        return False
    return (is_thick_enough(candle, min_body_ratio)
            and _rel_close(candle.open, candle.high, abs_tol=1e-5)
            and _rel_close(candle.close, candle.low, abs_tol=1e-5))