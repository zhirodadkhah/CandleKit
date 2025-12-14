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

def gap_down(prev: CandleStick, curr: CandleStick, window = False) -> bool:
    """Check if current candle gaps down (open < previous close).
    :param prev: Previous candle
    :param curr: Current candle
    :param window:
    """
    return curr.open < prev.close if not window else curr.high < prev.low

def gap_up(prev: CandleStick, curr: CandleStick, window = False) -> bool:
    """Check if current candle gaps up (open > previous close).
    :param prev: Previous candle
    :param curr: Current candle
    :param window:
    """
    return curr.open > prev.close if not window else curr.low > prev.high

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

def is_bullish_belt_hold(candle: CandleStick, min_body_ratio: float = 0.95, max_wick_ratio: float = 0.05) -> bool:
    """Detect Bullish Belt Hold.
    :param candle: The candlestick to evaluate
    :param min_body_ratio: Minimum body-to-total-length ratio
    :param max_wick_ratio: Max allowed lower/upper wick as fraction of total length (Nison: "no lower shadow")
    :ref: Nison p. 32
    """
    if not _valid_candle(candle) or not candle.is_bullish:
        return False
    return (is_thick_enough(candle, min_body_ratio)
            and candle.bottom_wick <= max_wick_ratio * candle.length
            and candle.top_wick <= max_wick_ratio * candle.length)

def is_bearish_belt_hold(candle: CandleStick, min_body_ratio: float = 0.95, max_wick_ratio: float = 0.05) -> bool:
    """Detect Bearish Belt Hold.
    :param candle: The candlestick to evaluate
    :param min_body_ratio: Minimum body-to-total-length ratio
    :param max_wick_ratio: Max allowed lower/upper wick as fraction of total length
    :ref: Nison p. 32
    """
    if not _valid_candle(candle) or candle.is_bullish:
        return False
    return (is_thick_enough(candle, min_body_ratio)
            and candle.top_wick <= max_wick_ratio * candle.length
            and candle.bottom_wick <= max_wick_ratio * candle.length)

def is_bullish_marubozu(candle: CandleStick, max_wick_ratio: float = 0.01) -> bool:
    """Detect Bullish Marubozu (no shadows per Nison).
    :param candle: The candlestick to evaluate
    :param max_wick_ratio: Max allowed wick as fraction of total length (Nison: zero shadows)
    :ref: Nison p. 24
    """
    if not _valid_candle(candle) or not candle.is_bullish:
        return False
    return (candle.bottom_wick <= max_wick_ratio * candle.length
            and candle.top_wick <= max_wick_ratio * candle.length)

def is_bearish_marubozu(candle: CandleStick, max_wick_ratio: float = 0.01) -> bool:
    """Detect Bearish Marubozu (no shadows per Nison).
    :param candle: The candlestick to evaluate
    :param max_wick_ratio: Max allowed wick as fraction of total length (Nison: zero shadows)
    :ref: Nison p. 24
    """
    if not _valid_candle(candle) or candle.is_bullish:
        return False
    return (candle.top_wick <= max_wick_ratio * candle.length
            and candle.bottom_wick <= max_wick_ratio * candle.length)

# --------------------------
# TWO-CANDLE PATTERNS (Nison - Japanese Candlestick Charting Techniques, 2nd Ed.)
# --------------------------

def is_bullish_engulfing(c0: CandleStick, c1: CandleStick) -> bool:
    """Detect Bullish Engulfing pattern.
    :param c0: First (bearish) candle
    :param c1: Second (bullish) candle whose body engulfs c0's body
    :ref: Nison p. 45
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (not c0.is_bullish
            and c1.is_bullish
            and body_engulf(c0, c1))

def is_bearish_engulfing(c0: CandleStick, c1: CandleStick) -> bool:
    """Detect Bearish Engulfing pattern.
    :param c0: First (bullish) candle
    :param c1: Second (bearish) candle whose body engulfs c0's body
    :ref: Nison p. 45
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (c0.is_bullish
            and not c1.is_bullish
            and body_engulf(c0, c1))

def is_piercing_line(c0: CandleStick, c1: CandleStick) -> bool:
    """Detect Piercing Line pattern.
    :param c0: First long bearish candle
    :param c1: Second bullish candle that opens below c0's low and closes above c0's midpoint
    :ref: Nison p. 48
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    midpoint = (c0.open + c0.close) / 2
    return (not c0.is_bullish
            and c1.is_bullish
            and c1.open < c0.low
            and c1.close > midpoint
            and c1.close <= c0.open)

def is_dark_cloud_cover(c0: CandleStick, c1: CandleStick) -> bool:
    """Detect Dark Cloud Cover pattern.
    :param c0: First long bullish candle
    :param c1: Second bearish candle that opens above c0's high and closes below c0's midpoint
    :ref: Nison p. 49
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    midpoint = (c0.open + c0.close) / 2
    return (c0.is_bullish
            and not c1.is_bullish
            and c1.open > c0.high
            and c1.close < midpoint
            and c1.close >= c0.open)

def is_harami_cross_bullish(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.3) -> bool:
    """Detect Bullish Harami Cross pattern.
    :param c0: First large bearish candle
    :param c1: Second doji candle contained within c0's body
    :param min_body_ratio: Minimum body ratio for c0 to be considered "large"
    :ref: Nison p. 52
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and is_doji(c1, max_body_ratio=0.1)
            and body_contained(c1, c0))

def is_harami_cross_bearish(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.3) -> bool:
    """Detect Bearish Harami Cross pattern.
    :param c0: First large bullish candle
    :param c1: Second doji candle contained within c0's body
    :param min_body_ratio: Minimum body ratio for c0 to be considered "large"
    :ref: Nison p. 52
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and is_doji(c1, max_body_ratio=0.1)
            and body_contained(c1, c0))

def is_kicking_bullish(c0: CandleStick, c1: CandleStick, min_marubozu_ratio: float = 0.9) -> bool:
    """Detect Bullish Kicking pattern.
    :param c0: First bearish marubozu
    :param c1: Second bullish marubozu with upward gap from c0
    :param min_marubozu_ratio: Minimum body ratio for marubozu candles
    :ref: Nison p. 170
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_bearish_marubozu(c0, min_marubozu_ratio)
            and is_bullish_marubozu(c1, min_marubozu_ratio)
            and gap_up(c0, c1, window=True))

def is_kicking_bearish(c0: CandleStick, c1: CandleStick, min_marubozu_ratio: float = 0.9) -> bool:
    """Detect Bearish Kicking pattern.
    :param c0: First bullish marubozu
    :param c1: Second bearish marubozu with downward gap from c0
    :param min_marubozu_ratio: Minimum body ratio for marubozu candles
    :ref: Nison p. 170
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_bullish_marubozu(c0, min_marubozu_ratio)
            and is_bearish_marubozu(c1, min_marubozu_ratio)
            and gap_down(c0, c1, window=True))