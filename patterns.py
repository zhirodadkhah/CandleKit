from .entity import CandleStick
import math


# --- Shared helpers ---
def is_thick_enough(candle: CandleStick, min_ratio: float) -> bool:
    """Check if candle has a thick body (strong conviction), regardless of direction."""
    return candle.body_ratio >= min_ratio


def is_thick_bearish(candle: CandleStick, min_ratio: float) -> bool:
    """Check if candle is bearish and has a thick body."""
    return not candle.is_bullish and candle.body_ratio >= min_ratio


def is_thick_bullish(candle: CandleStick, min_ratio: float) -> bool:
    """Check if candle is bullish and has a thick body."""
    return candle.is_bullish and candle.body_ratio >= min_ratio


def is_thin_enough(candle: CandleStick, max_ratio: float) -> bool:
    """Check if candle has a thin body (indecision), regardless of direction."""
    return candle.body_ratio <= max_ratio


def is_thin_bearish(candle: CandleStick, max_ratio: float) -> bool:
    """Check if candle is bearish and has a thin body."""
    return not candle.is_bullish and candle.body_ratio <= max_ratio


def is_thin_bullish(candle: CandleStick, max_ratio: float) -> bool:
    """Check if candle is bullish and has a thin body."""
    return candle.is_bullish and candle.body_ratio <= max_ratio


def gap_down(prev: CandleStick, curr: CandleStick) -> bool:
    """Check if current candle gaps down (open < previous close)."""
    return curr.open < prev.close


def gap_up(prev: CandleStick, curr: CandleStick) -> bool:
    """Check if current candle gaps up (open > previous close)."""
    return curr.open > prev.close


def body_engulf(prev: CandleStick, curr: CandleStick) -> bool:
    """Check if current candle's body engulfs previous candle's body."""
    return curr.body_high > prev.body_high and curr.body_low < prev.body_low


def wick_engulf(prev: CandleStick, curr: CandleStick) -> bool:
    """Check if current candle's wicks engulf previous candle's wicks."""
    return curr.high > prev.high and curr.low < prev.low


def _valid_candle(candle: CandleStick) -> bool:
    return candle.length > 0


def _rel_close(a: float, b: float, rel_tol: float = 1e-4, abs_tol: float = 1e-8) -> bool:
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def body_contained(inner: CandleStick, outer: CandleStick) -> bool:
    """Check if inner candle's body is completely within outer candle's body."""
    return inner.body_high <= outer.body_high and inner.body_low >= outer.body_low


# --------------------------
# SINGLE-CANDLE PATTERNS
# --------------------------

def is_doji(candle: CandleStick, max_body_ratio: float = 0.05) -> bool:
    """
    Detect general Doji pattern (indecision).

    :param max_body_ratio: Maximum body-to-total-length ratio
    """
    return _valid_candle(candle) and is_thin_enough(candle, max_body_ratio)


def is_hammer(candle: CandleStick,
              max_body_ratio: float = 0.25,
              min_lower_wick_to_body: float = 2.0,
              max_upper_wick_ratio: float = 0.1) -> bool:
    """
    Detect Hammer pattern.

    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_lower_wick_to_body: Minimum ratio of lower wick to body length
    :param max_upper_wick_ratio: Maximum upper wick as fraction of total length
    """
    if not _valid_candle(candle):
        return False

    return (is_thin_enough(candle, max_body_ratio)
            and candle.top_wick <= max_upper_wick_ratio * candle.length
            and candle.bottom_wick >= candle.body_length * min_lower_wick_to_body)


def is_hanging_man(candle: CandleStick, **kwargs) -> bool:
    """
    Structurally identical to Hammer, different context.

    :param kwargs: Same parameters as is_hammer()
    """
    return is_hammer(candle, **kwargs)


def is_shooting_star(candle: CandleStick,
                     max_body_ratio: float = 0.25,
                     min_upper_wick_to_body: float = 2.0,
                     max_lower_wick_ratio: float = 0.1) -> bool:
    """
    Detect Shooting Star pattern.

    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_upper_wick_to_body: Minimum ratio of upper wick to body length
    :param max_lower_wick_ratio: Maximum lower wick as fraction of total length
    """
    if not _valid_candle(candle):
        return False

    return (is_thin_enough(candle, max_body_ratio)
            and candle.bottom_wick <= max_lower_wick_ratio * candle.length
            and candle.top_wick >= candle.body_length * min_upper_wick_to_body)


def is_inverted_hammer(candle: CandleStick, **kwargs) -> bool:
    """
    Structurally identical to Shooting Star, different context.

    :param kwargs: Same parameters as is_shooting_star()
    """
    return is_shooting_star(candle, **kwargs)


def is_bullish_belt_hold(candle: CandleStick, min_body_ratio: float = 0.7) -> bool:
    """
    Detect Bullish Belt Hold.

    :param min_body_ratio: Minimum body-to-total-length ratio
    """
    if not _valid_candle(candle) or not candle.is_bullish:
        return False

    return (is_thick_enough(candle, min_body_ratio)
            and _rel_close(candle.open, candle.low, abs_tol=candle.length * 0.01))


def is_bearish_belt_hold(candle: CandleStick, min_body_ratio: float = 0.7) -> bool:
    """
    Detect Bearish Belt Hold.

    :param min_body_ratio: Minimum body-to-total-length ratio
    """
    if not _valid_candle(candle) or candle.is_bullish:
        return False

    return (is_thick_enough(candle, min_body_ratio)
            and _rel_close(candle.open, candle.high, abs_tol=candle.length * 0.01))


def is_dragonfly_doji(candle: CandleStick,
                      max_body_ratio: float = 0.1,
                      min_lower_wick_ratio: float = 0.6) -> bool:
    """
    Detect Dragonfly Doji.

    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_lower_wick_ratio: Minimum lower wick as fraction of total length
    """
    if not is_doji(candle, max_body_ratio):
        return False

    return (_rel_close(candle.close, candle.high, abs_tol=candle.length * 0.02)
            and candle.bottom_wick >= min_lower_wick_ratio * candle.length)


def is_gravestone_doji(candle: CandleStick,
                       max_body_ratio: float = 0.1,
                       min_upper_wick_ratio: float = 0.6) -> bool:
    """
    Detect Gravestone Doji.

    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_upper_wick_ratio: Minimum upper wick as fraction of total length
    """
    if not is_doji(candle, max_body_ratio):
        return False

    return (_rel_close(candle.close, candle.low, abs_tol=candle.length * 0.02)
            and candle.top_wick >= min_upper_wick_ratio * candle.length)


def is_long_legged_doji(candle: CandleStick,
                        max_body_ratio: float = 0.1,
                        min_wick_ratio: float = 0.4) -> bool:
    """
    Detect Long-Legged Doji.

    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_wick_ratio: Minimum wick length as fraction of total length
    """
    if not is_doji(candle, max_body_ratio):
        return False

    return (candle.top_wick >= min_wick_ratio * candle.length
            and candle.bottom_wick >= min_wick_ratio * candle.length)


def is_spinning_top(candle: CandleStick,
                    max_body_ratio: float = 0.3,
                    min_wick_ratio: float = 0.3) -> bool:
    """
    Detect Spinning Top.

    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_wick_ratio: Minimum wick length as fraction of total length
    """
    if not _valid_candle(candle):
        return False

    return (is_thin_enough(candle, max_body_ratio)
            and candle.top_wick >= min_wick_ratio * candle.length
            and candle.bottom_wick >= min_wick_ratio * candle.length)


def is_bullish_marubozu(candle: CandleStick, min_body_ratio: float = 0.95) -> bool:
    """
    Detect Bullish Marubozu.

    :param min_body_ratio: Minimum body-to-total-length ratio
    """
    if not _valid_candle(candle) or not candle.is_bullish:
        return False

    max_wick_ratio = 1.0 - min_body_ratio
    return (is_thick_enough(candle, min_body_ratio)
            and candle.top_wick <= max_wick_ratio * candle.length
            and candle.bottom_wick <= max_wick_ratio * candle.length)


def is_bearish_marubozu(candle: CandleStick, min_body_ratio: float = 0.95) -> bool:
    """
    Detect Bearish Marubozu.

    :param min_body_ratio: Minimum body-to-total-length ratio
    """
    if not _valid_candle(candle) or candle.is_bullish:
        return False

    max_wick_ratio = 1.0 - min_body_ratio
    return (is_thick_enough(candle, min_body_ratio)
            and candle.top_wick <= max_wick_ratio * candle.length
            and candle.bottom_wick <= max_wick_ratio * candle.length)


# Add compatibility aliases
is_white_marubozu = is_bullish_marubozu
is_black_marubozu = is_bearish_marubozu


# --------------------------
# MULTI-CANDLE PATTERNS
# --------------------------

def is_bullish_engulfing(c0: CandleStick, c1: CandleStick) -> bool:
    """
    Detect Bullish Engulfing pattern.

    :param c0: Previous (bearish) candle
    :param c1: Current (bullish) candle
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False

    return (not c0.is_bullish
            and c1.is_bullish
            and body_engulf(c0, c1))


def is_bearish_engulfing(c0: CandleStick, c1: CandleStick) -> bool:
    """
    Detect Bearish Engulfing pattern.

    :param c0: Previous (bullish) candle
    :param c1: Current (bearish) candle
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False

    return (c0.is_bullish
            and not c1.is_bullish
            and body_engulf(c0, c1))


def is_bullish_harami(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.3) -> bool:
    """
    Detect Bullish Harami pattern.

    :param c0: Previous (large bearish) candle
    :param c1: Current (small bullish) candle
    :param min_body_ratio: Minimum body ratio for first candle to be considered "large"
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False

    return (is_thick_bearish(c0, min_body_ratio)
            and c1.is_bullish
            and body_contained(c1, c0))


def is_bearish_harami(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.3) -> bool:
    """
    Detect Bearish Harami pattern.

    :param c0: Previous (large bullish) candle
    :param c1: Current (small bearish) candle
    :param min_body_ratio: Minimum body ratio for first candle to be considered "large"
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False

    return (is_thick_bullish(c0, min_body_ratio)
            and not c1.is_bullish
            and body_contained(c1, c0))


def is_three_white_soldiers(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                            min_body_ratio: float = 0.4) -> bool:
    """
    Detect Three White Soldiers pattern.

    :param c0: First bullish candle
    :param c1: Second bullish candle
    :param c2: Third bullish candle
    :param min_body_ratio: Minimum body ratio for each candle
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False

    return (all(c.is_bullish for c in (c0, c1, c2))
            and all(is_thick_bullish(c, min_body_ratio) for c in (c0, c1, c2))
            and c0.close < c1.close < c2.close
            and c0.open < c1.open < c2.open)


def is_three_black_crows(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                         min_body_ratio: float = 0.4) -> bool:
    """
    Detect Three Black Crows pattern.

    :param c0: First bearish candle
    :param c1: Second bearish candle
    :param c2: Third bearish candle
    :param min_body_ratio: Minimum body ratio for each candle
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False

    return (all(not c.is_bullish for c in (c0, c1, c2))
            and all(is_thick_bearish(c, min_body_ratio) for c in (c0, c1, c2))
            and c0.close > c1.close > c2.close
            and c0.open > c1.open > c2.open)


def is_piercing_line(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.4) -> bool:
    """
    Detect Piercing Line pattern.

    :param c0: Previous (bearish) candle
    :param c1: Current (bullish) candle
    :param min_body_ratio: Minimum body ratio for both candles
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False

    midpoint = (c0.open + c0.close) / 2
    return (is_thick_bearish(c0, min_body_ratio)
            and is_thick_bullish(c1, min_body_ratio)
            and c1.close > midpoint
            and c1.open < c0.low
            and c1.close <= c0.open)


def is_dark_cloud_cover(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.4) -> bool:
    """
    Detect Dark Cloud Cover pattern.

    :param c0: Previous (bullish) candle
    :param c1: Current (bearish) candle
    :param min_body_ratio: Minimum body ratio for both candles
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False

    midpoint = (c0.open + c0.close) / 2
    return (is_thick_bullish(c0, min_body_ratio)
            and is_thick_bearish(c1, min_body_ratio)
            and c1.close < midpoint
            and c1.open > c0.high
            and c1.close >= c0.open)


def is_tweezer_bottom(c0: CandleStick, c1: CandleStick, tolerance_ratio: float = 0.01) -> bool:
    """
    Detect Tweezer Bottom pattern.

    :param c0: First candle
    :param c1: Second candle
    :param tolerance_ratio: Allowed deviation between lows as fraction of candle length
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False

    tolerance = tolerance_ratio * max(c0.length, c1.length, 1e-8)
    return (abs(c0.low - c1.low) <= tolerance
            and c1.close > c1.open)


def is_tweezer_top(c0: CandleStick, c1: CandleStick, tolerance_ratio: float = 0.01) -> bool:
    """
    Detect Tweezer Top pattern.

    :param c0: First candle
    :param c1: Second candle
    :param tolerance_ratio: Allowed deviation between highs as fraction of candle length
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False

    tolerance = tolerance_ratio * max(c0.length, c1.length, 1e-8)
    return (abs(c0.high - c1.high) <= tolerance
            and c1.close < c1.open)


def is_morning_star(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                    min_body_ratio: float = 0.4, max_star_body_ratio: float = 0.2) -> bool:
    """
    Detect Morning Star pattern.

    :param c0: First (bearish) candle
    :param c1: Middle (small/doji) candle
    :param c2: Third (bullish) candle
    :param min_body_ratio: Minimum body ratio for strong candles (c0, c2)
    :param max_star_body_ratio: Maximum body ratio for the star (c1)
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False

    midpoint = (c0.open + c0.close) / 2
    return (is_thick_bearish(c0, min_body_ratio)
            and is_thin_enough(c1, max_star_body_ratio)
            and is_thick_bullish(c2, min_body_ratio)
            and c2.close > midpoint)


def is_evening_star(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                    min_body_ratio: float = 0.4, max_star_body_ratio: float = 0.2) -> bool:
    """
    Detect Evening Star pattern.

    :param c0: First (bullish) candle
    :param c1: Middle (small/doji) candle
    :param c2: Third (bearish) candle
    :param min_body_ratio: Minimum body ratio for strong candles (c0, c2)
    :param max_star_body_ratio: Maximum body ratio for the star (c1)
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False

    midpoint = (c0.open + c0.close) / 2
    return (is_thick_bullish(c0, min_body_ratio)
            and is_thin_enough(c1, max_star_body_ratio)
            and is_thick_bearish(c2, min_body_ratio)
            and c2.close < midpoint)


def is_inside_bar(prev: CandleStick, curr: CandleStick) -> bool:
    """
    Detect Inside Bar pattern (consolidation).

    :param prev: Previous candle
    :param curr: Current candle
    """
    if not (_valid_candle(prev) and _valid_candle(curr)):
        return False

    return body_contained(curr, prev)


def is_outside_bar(prev: CandleStick, curr: CandleStick) -> bool:
    """
    Detect Outside Bar pattern (increased volatility).

    :param prev: Previous candle
    :param curr: Current candle
    """
    if not (_valid_candle(prev) and _valid_candle(curr)):
        return False

    return body_engulf(prev, curr)