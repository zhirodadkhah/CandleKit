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
# SINGLE-CANDLE PATTERNS
# --------------------------

def is_doji(candle: CandleStick, max_body_ratio: float = 0.1) -> bool:
    """Detect general Doji pattern (indecision).
    :param candle: The candlestick to evaluate
    :param max_body_ratio: Maximum body-to-total-length ratio
    """
    return _valid_candle(candle) and is_thin_enough(candle, max_body_ratio)

def is_hammer(candle: CandleStick,
              max_body_ratio: float = 0.25,
              min_lower_wick_to_body: float = 2.0,
              max_upper_wick_ratio: float = 0.33,
              min_wick_length_ratio: float = 0.6) -> bool:
    """Detect Hammer pattern.
    :param candle: The candlestick to evaluate
    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_lower_wick_to_body: Minimum required ratio of lower wick to body length
    :param max_upper_wick_ratio: Maximum allowed upper wick as fraction of total length
    :param min_wick_length_ratio: Minimum lower wick as fraction of total candle length
    """
    if not _valid_candle(candle):
        return False
    min_wick_required = max(
        candle.body_length * min_lower_wick_to_body,
        candle.length * min_wick_length_ratio
    )
    return (is_thin_enough(candle, max_body_ratio)
            and candle.top_wick <= max_upper_wick_ratio * candle.length
            and candle.bottom_wick >= min_wick_required)

def is_hanging_man(candle: CandleStick, **kwargs) -> bool:
    """Structurally identical to Hammer, different context.
    :param candle: The candlestick to evaluate
    :param kwargs: Same parameters as is_hammer()
    """
    return is_hammer(candle, **kwargs)

def is_shooting_star(candle: CandleStick,
                     max_body_ratio: float = 0.25,
                     min_upper_wick_to_body: float = 2.0,
                     max_lower_wick_ratio: float = 0.33,
                     min_wick_length_ratio: float = 0.6) -> bool:
    """Detect Shooting Star pattern.
    :param candle: The candlestick to evaluate
    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_upper_wick_to_body: Minimum required ratio of upper wick to body length
    :param max_lower_wick_ratio: Maximum allowed lower wick as fraction of total length
    :param min_wick_length_ratio: Minimum upper wick as fraction of total candle length
    """
    if not _valid_candle(candle):
        return False
    min_wick_required = max(
        candle.body_length * min_upper_wick_to_body,
        candle.length * min_wick_length_ratio
    )
    return (is_thin_enough(candle, max_body_ratio)
            and candle.bottom_wick <= max_lower_wick_ratio * candle.length
            and candle.top_wick >= min_wick_required)

def is_inverted_hammer(candle: CandleStick, **kwargs) -> bool:
    """Structurally identical to Shooting Star, different context.
    :param candle: The candlestick to evaluate
    :param kwargs: Same parameters as is_shooting_star()
    """
    return is_shooting_star(candle, **kwargs)

def is_bullish_belt_hold(candle: CandleStick, min_body_ratio: float = 0.7) -> bool:
    """Detect Bullish Belt Hold.
    :param candle: The candlestick to evaluate
    :param min_body_ratio: Minimum body-to-total-length ratio
    """
    if not _valid_candle(candle) or not candle.is_bullish:
        return False
    max_wick_allowed = candle.length * 0.01
    return (is_thick_enough(candle, min_body_ratio)
            and _rel_close(candle.open, candle.low, abs_tol=max_wick_allowed)
            and candle.bottom_wick <= max_wick_allowed)

def is_bearish_belt_hold(candle: CandleStick, min_body_ratio: float = 0.7) -> bool:
    """Detect Bearish Belt Hold.
    :param candle: The candlestick to evaluate
    :param min_body_ratio: Minimum body-to-total-length ratio
    """
    if not _valid_candle(candle) or candle.is_bullish:
        return False
    max_wick_allowed = candle.length * 0.01
    return (is_thick_enough(candle, min_body_ratio)
            and _rel_close(candle.open, candle.high, abs_tol=max_wick_allowed)
            and candle.top_wick <= max_wick_allowed)

def is_dragonfly_doji(candle: CandleStick,
                      max_body_ratio: float = 0.1,
                      min_lower_wick_ratio: float = 0.6) -> bool:
    """Detect Dragonfly Doji.
    :param candle: The candlestick to evaluate
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
    """Detect Gravestone Doji.
    :param candle: The candlestick to evaluate
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
    """Detect Long-Legged Doji.
    :param candle: The candlestick to evaluate
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
    """Detect Spinning Top.
    :param candle: The candlestick to evaluate
    :param max_body_ratio: Maximum body-to-total-length ratio
    :param min_wick_ratio: Minimum wick length as fraction of total length
    """
    if not _valid_candle(candle):
        return False
    return (is_thin_enough(candle, max_body_ratio)
            and candle.top_wick >= min_wick_ratio * candle.length
            and candle.bottom_wick >= min_wick_ratio * candle.length)

def is_bullish_marubozu(candle: CandleStick, min_body_ratio: float = 0.95) -> bool:
    """Detect Bullish Marubozu.
    :param candle: The candlestick to evaluate
    :param min_body_ratio: Minimum body-to-total-length ratio
    """
    if not _valid_candle(candle) or not candle.is_bullish:
        return False
    max_wick_ratio = 1.0 - min_body_ratio
    return (is_thick_enough(candle, min_body_ratio)
            and candle.top_wick <= max_wick_ratio * candle.length
            and candle.bottom_wick <= max_wick_ratio * candle.length)

def is_bearish_marubozu(candle: CandleStick, min_body_ratio: float = 0.95) -> bool:
    """Detect Bearish Marubozu.
    :param candle: The candlestick to evaluate
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
    """Detect Bullish Engulfing pattern.
    :param c0: Previous (bearish) candle
    :param c1: Current (bullish) candle
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (not c0.is_bullish
            and c1.is_bullish
            and body_engulf(c0, c1))

def is_bearish_engulfing(c0: CandleStick, c1: CandleStick) -> bool:
    """Detect Bearish Engulfing pattern.
    :param c0: Previous (bullish) candle
    :param c1: Current (bearish) candle
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (c0.is_bullish
            and not c1.is_bullish
            and body_engulf(c0, c1))

def is_bullish_harami(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.3) -> bool:
    """Detect Bullish Harami pattern.
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
    """Detect Bearish Harami pattern.
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
                            min_body_ratio: float = 0.4, close_to_high_tol = 0.2) -> bool:
    """Detect Three White Soldiers pattern.
    :param c0: First bullish candle
    :param c1: Second bullish candle
    :param c2: Third bullish candle
    :param close_to_high_tol: Close to high tolerance
    :param min_body_ratio: Minimum body ratio for each candle
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    if not all(c.is_bullish and is_thick_bullish(c, min_body_ratio) for c in (c0, c1, c2)):
        return False
    if not (c0.close < c1.close < c2.close and c0.open < c1.open < c2.open):
        return False
    if not (c1.open > c0.open and c1.open < c0.close and
            c2.open > c1.open and c2.open < c1.close):
        return False
    return all(_rel_close(c.close, c.high, abs_tol=c.length * close_to_high_tol)
               for c in (c0, c1, c2))

def is_three_black_crows(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                         min_body_ratio: float = 0.4,
                         close_to_low_tol = 0.2) -> bool:
    """Detect Three Black Crows pattern.
    :param c0: First bearish candle
    :param c1: Second bearish candle
    :param c2: Third bearish candle
    :param min_body_ratio: Minimum body ratio for each candle
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    if not all(not c.is_bullish and is_thick_bearish(c, min_body_ratio) for c in (c0, c1, c2)):
        return False
    if not (c0.close > c1.close > c2.close and c0.open > c1.open > c2.open):
        return False
    if not (c1.open < c0.open and c1.open > c0.close and
            c2.open < c1.open and c2.open > c1.close):
        return False
    close_to_low_tol = 0.1
    return all(_rel_close(c.close, c.low, abs_tol=c.length * close_to_low_tol)
               for c in (c0, c1, c2))

def is_piercing_line(c0: CandleStick, c1: CandleStick,
                     min_body_ratio: float = 0.4,
                     require_gap_down: bool = True) -> bool:
    """Detect Piercing Line pattern.
    :param c0: Previous (bearish) candle
    :param c1: Current (bullish) candle
    :param min_body_ratio: Minimum body ratio for both candles
    :param require_gap_down: Whether to require a gap down between candles
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    midpoint = (c0.open + c0.close) / 2
    base = (is_thick_bearish(c0, min_body_ratio)
            and is_thick_bullish(c1, min_body_ratio)
            and c1.close > midpoint
            and c1.open < c0.low
            and c1.close <= c0.open)
    if not require_gap_down:
        return base
    return base and gap_down(c0, c1)

def is_dark_cloud_cover(c0: CandleStick, c1: CandleStick,
                        min_body_ratio: float = 0.4,
                        require_gap_up: bool = True) -> bool:
    """Detect Dark Cloud Cover pattern.
    :param c0: Previous (bullish) candle
    :param c1: Current (bearish) candle
    :param min_body_ratio: Minimum body ratio for both candles
    :param require_gap_up: Whether to require a gap up between candles
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    midpoint = (c0.open + c0.close) / 2
    base = (is_thick_bullish(c0, min_body_ratio)
            and is_thick_bearish(c1, min_body_ratio)
            and c1.close < midpoint
            and c1.open > c0.high
            and c1.close >= c0.open)
    if not require_gap_up:
        return base
    return base and gap_up(c0, c1)

def is_tweezer_bottom(c0: CandleStick, c1: CandleStick, tolerance_ratio: float = 0.01) -> bool:
    """Detect Tweezer Bottom pattern.
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
    """Detect Tweezer Top pattern.
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
                    min_body_ratio: float = 0.4,
                    max_star_body_ratio: float = 0.2,
                    require_gaps: bool = True) -> bool:
    """Detect Morning Star pattern.
    :param c0: First (bearish) candle
    :param c1: Middle (small/doji) candle
    :param c2: Third (bullish) candle
    :param min_body_ratio: Minimum body ratio for strong candles (c0, c2)
    :param max_star_body_ratio: Maximum body ratio for the star (c1)
    :param require_gaps: Whether to require gaps between candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    base = (is_thick_bearish(c0, min_body_ratio)
            and is_thin_enough(c1, max_star_body_ratio)
            and is_thick_bullish(c2, min_body_ratio)
            and c2.close > (c0.open + c0.close) / 2)
    if not require_gaps:
        return base
    return base and gap_down(c0, c1) and gap_up(c1, c2)



def is_evening_star(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                    min_body_ratio: float = 0.4,
                    max_star_body_ratio: float = 0.2,
                    require_gaps: bool = True) -> bool:
    """Detect Evening Star pattern.
    :param c0: First (bullish) candle
    :param c1: Middle (small/doji) candle
    :param c2: Third (bearish) candle
    :param min_body_ratio: Minimum body ratio for strong candles (c0, c2)
    :param max_star_body_ratio: Maximum body ratio for the star (c1)
    :param require_gaps: Whether to require gaps between candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    base = (is_thick_bullish(c0, min_body_ratio)
            and is_thin_enough(c1, max_star_body_ratio)
            and is_thick_bearish(c2, min_body_ratio)
            and c2.close < (c0.open + c0.close) / 2)
    if not require_gaps:
        return base
    return base and gap_up(c0, c1) and gap_down(c1, c2)

def is_inside_bar(prev: CandleStick, curr: CandleStick) -> bool:
    """Detect Inside Bar pattern (consolidation).
    :param prev: Previous candle
    :param curr: Current candle
    """
    if not (_valid_candle(prev) and _valid_candle(curr)):
        return False
    return body_contained(curr, prev)

def is_outside_bar(prev: CandleStick, curr: CandleStick) -> bool:
    """Detect Outside Bar pattern (increased volatility).
    :param prev: Previous candle
    :param curr: Current candle
    """
    if not (_valid_candle(prev) and _valid_candle(curr)):
        return False
    return body_engulf(prev, curr)

def is_separating_lines_bullish(c0: CandleStick, c1: CandleStick,
                               tolerance_ratio: float = 0.01) -> bool:
    """Detect Bullish Separating Lines pattern.
    :param c0: First (bearish) candle
    :param c1: Second (bullish) candle with same open
    :param tolerance_ratio: Open alignment tolerance as fraction of max length
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    tol = max(c0.length, c1.length, 1e-8) * tolerance_ratio
    return (not c0.is_bullish
            and c1.is_bullish
            and abs(c0.open - c1.open) <= tol)

def is_separating_lines_bearish(c0: CandleStick, c1: CandleStick,
                               tolerance_ratio: float = 0.01) -> bool:
    """Detect Bearish Separating Lines pattern.
    :param c0: First (bullish) candle
    :param c1: Second (bearish) candle with same open
    :param tolerance_ratio: Open alignment tolerance as fraction of max length
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    tol = max(c0.length, c1.length, 1e-8) * tolerance_ratio
    return (c0.is_bullish
            and not c1.is_bullish
            and abs(c0.open - c1.open) <= tol)


def is_kicking_bullish(c0: CandleStick, c1: CandleStick,
                      min_marubozu_ratio: float = 0.9) -> bool:
    """Detect Bullish Kicking pattern.
    :param c0: First (bearish marubozu) candle
    :param c1: Second (bullish marubozu) candle
    :param min_marubozu_ratio: Minimum body ratio for marubozu candles
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_bearish_marubozu(c0, min_marubozu_ratio)
            and is_bullish_marubozu(c1, min_marubozu_ratio)
            and gap_up(c0, c1))

def is_kicking_bearish(c0: CandleStick, c1: CandleStick,
                      min_marubozu_ratio: float = 0.9) -> bool:
    """Detect Bearish Kicking pattern.
    :param c0: First (bullish marubozu) candle
    :param c1: Second (bearish marubozu) candle
    :param min_marubozu_ratio: Minimum body ratio for marubozu candles
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_bullish_marubozu(c0, min_marubozu_ratio)
            and is_bearish_marubozu(c1, min_marubozu_ratio)
            and gap_down(c0, c1))

def is_counterattack_bullish(c0: CandleStick, c1: CandleStick,
                            min_body_ratio: float = 0.4) -> bool:
    """Detect Bullish Counterattack (Meeting Lines) pattern.
    :param c0: First (bearish) candle closing near low
    :param c1: Second (bullish) candle opening below c0's close
    :param min_body_ratio: Minimum body ratio for both candles
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and _rel_close(c0.close, c0.low, abs_tol=c0.length * 0.1)   # ← NEW
            and is_thick_bullish(c1, min_body_ratio)
            and c1.open < c0.close
            and _rel_close(c0.close, c1.close, abs_tol=c0.length * 0.01))

def is_counterattack_bearish(c0: CandleStick, c1: CandleStick,
                            min_body_ratio: float = 0.4) -> bool:
    """Detect Bearish Counterattack (Meeting Lines) pattern.
    :param c0: First (bullish) candle closing near high
    :param c1: Second (bearish) candle opening above c0's close
    :param min_body_ratio: Minimum body ratio for both candles
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and _rel_close(c0.close, c0.high, abs_tol=c0.length * 0.1)  # ← NEW
            and is_thick_bearish(c1, min_body_ratio)
            and c1.open > c0.close
            and _rel_close(c0.close, c1.close, abs_tol=c0.length * 0.01))

def is_upside_gap_two_crows(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                           min_body_ratio: float = 0.4) -> bool:
    """Detect Upside Gap Two Crows pattern.
    :param c0: First (bullish) candle
    :param c1: Second (bearish) gap candle
    :param c2: Third (bearish) engulfing candle
    :param min_body_ratio: Minimum body ratio for all candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and c1.open > c0.high  # Clear gap above c0
            and is_thick_bearish(c1, min_body_ratio)
            and is_thick_bearish(c2, min_body_ratio)
            and body_engulf(c1, c2)  # c2 engulfs c1's body
            and c2.close < c0.close)  # Closes below first bullish candle


def is_harami_cross_bullish(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.3) -> bool:
    """Detect Bullish Harami Cross pattern.
    :param c0: Previous (large bearish) candle
    :param c1: Current (doji) candle contained within c0's body
    :param min_body_ratio: Minimum body ratio for first candle to be considered "large"
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and is_doji(c1, max_body_ratio=0.1)
            and body_contained(c1, c0))

def is_harami_cross_bearish(c0: CandleStick, c1: CandleStick, min_body_ratio: float = 0.3) -> bool:
    """Detect Bearish Harami Cross pattern.
    :param c0: Previous (large bullish) candle
    :param c1: Current (doji) candle contained within c0's body
    :param min_body_ratio: Minimum body ratio for first candle to be considered "large"
    """
    if not (_valid_candle(c0) and _valid_candle(c1)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and is_doji(c1, max_body_ratio=0.1)
            and body_contained(c1, c0))

# --------------------------
# THREE-CANDLE PATTERNS (Bulkowski Compliant)
# --------------------------

def is_mat_hold(c0: CandleStick, c1: CandleStick, c2: CandleStick, c3: CandleStick, c4: CandleStick,
                min_body_ratio: float = 0.4, max_consolidation_body_ratio: float = 0.3) -> bool:
    """Detect Mat Hold pattern (bullish continuation) - Bulkowski p. 244.
    :param c0: Strong bullish candle
    :param c1-c3: Three small bearish candles inside c0's range
    :param c4: Bullish confirmation candle closing above c0 high
    :param min_body_ratio: Minimum body ratio for strong candles
    :param max_consolidation_body_ratio: Maximum body ratio for consolidation candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2, c3, c4)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and all(not c.is_bullish and is_thin_enough(c, max_consolidation_body_ratio) for c in (c1, c2, c3))
            and all(c.high <= c0.high and c.low >= c0.low for c in (c1, c2, c3))
            and is_thick_bullish(c4, min_body_ratio)
            and c4.close > c0.high)

def is_three_stars_south(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                         min_body_ratio: float = 0.3) -> bool:
    """Detect Three Stars in the South pattern (bearish continuation) - Bulkowski p. 325.
    :param c0: Long bearish candle with long lower wick
    :param c1: Smaller bearish candle within c0's range
    :param c2: Small bearish candle (doji-like) closing near low
    :param min_body_ratio: Minimum body ratio for c0
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and c0.bottom_wick > c0.body_length
            and not c1.is_bullish
            and c1.high < c0.high and c1.low > c0.low
            and not c2.is_bullish
            and is_thin_enough(c2, max_ratio=0.2)
            and _rel_close(c2.close, c2.low, abs_tol=c2.length * 0.1))

def is_advance_block(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                     min_body_ratio: float = 0.4) -> bool:
    """Detect Advance Block pattern (bearish reversal) - Bulkowski p. 2.
    :param c0: Bullish candle
    :param c1: Bullish candle with long upper wick
    :param c2: Bullish candle with even longer upper wick
    :param min_body_ratio: Minimum body ratio for c0
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and c1.is_bullish and c2.is_bullish
            and c1.top_wick > c1.body_length
            and c2.top_wick > c2.body_length
            and c2.top_wick > c1.top_wick
            and _rel_close(c2.close, c2.low, abs_tol=c2.length * 0.1))

def is_deliberation(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                    min_body_ratio: float = 0.4) -> bool:
    """Detect Deliberation pattern (bearish reversal) - Bulkowski p. 72.
    :param c0: Strong bullish candle
    :param c1: Strong bullish candle
    :param c2: Small candle (doji/spinning top) gapping up
    :param min_body_ratio: Minimum body ratio for c0, c1
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and is_thick_bullish(c1, min_body_ratio)
            and (is_doji(c2, max_body_ratio=0.2) or is_spinning_top(c2))
            and gap_up(c1, c2))

def is_three_inside_up(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                       min_body_ratio: float = 0.4) -> bool:
    """Detect Three Inside Up pattern (bullish reversal) - Bulkowski p. 306.
    :param c0: Bearish candle
    :param c1: Bullish candle contained within c0
    :param c2: Bullish confirmation candle closing above c0 high
    :param min_body_ratio: Minimum body ratio for c0, c2
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and c1.is_bullish
            and body_contained(c1, c0)
            and is_thick_bullish(c2, min_body_ratio)
            and c2.close > c0.high)

def is_three_outside_up(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                        min_body_ratio: float = 0.4) -> bool:
    """Detect Three Outside Up pattern (bullish reversal) - Bulkowski p. 309.
    :param c0: Bearish candle
    :param c1: Bullish engulfing candle
    :param c2: Bullish confirmation candle
    :param min_body_ratio: Minimum body ratio for strong candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and is_bullish_engulfing(c0, c1)
            and is_thick_bullish(c2, min_body_ratio)
            and c2.close > c1.close)

def is_rising_three_methods(c0: CandleStick, c1: CandleStick, c2: CandleStick, c3: CandleStick, c4: CandleStick,
                            min_body_ratio: float = 0.5, max_consolidation_body_ratio: float = 0.3) -> bool:
    """Detect Rising Three Methods pattern (bullish continuation) - Bulkowski p. 280.
    :param c0: Long bullish candle
    :param c1-c3: Three small bearish candles inside c0's range
    :param c4: Long bullish candle closing above c0 high
    :param min_body_ratio: Minimum body ratio for c0, c4
    :param max_consolidation_body_ratio: Maximum body ratio for corrective candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2, c3, c4)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and all(not c.is_bullish and is_thin_enough(c, max_consolidation_body_ratio) for c in (c1, c2, c3))
            and all(c.high <= c0.high and c.low >= c0.low for c in (c1, c2, c3))
            and is_thick_bullish(c4, min_body_ratio)
            and c4.close > c0.high)

def is_falling_three_methods(c0: CandleStick, c1: CandleStick, c2: CandleStick, c3: CandleStick, c4: CandleStick,
                             min_body_ratio: float = 0.5, max_consolidation_body_ratio: float = 0.3) -> bool:
    """Detect Falling Three Methods pattern (bearish continuation) - Bulkowski p. 104.
    :param c0: Long bearish candle
    :param c1-c3: Three small bullish candles inside c0's range
    :param c4: Long bearish candle closing below c0 low
    :param min_body_ratio: Minimum body ratio for c0, c4
    :param max_consolidation_body_ratio: Maximum body ratio for corrective candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2, c3, c4)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and all(c.is_bullish and is_thin_enough(c, max_consolidation_body_ratio) for c in (c1, c2, c3))
            and all(c.high <= c0.high and c.low >= c0.low for c in (c1, c2, c3))
            and is_thick_bearish(c4, min_body_ratio)
            and c4.close < c0.low)

def is_upside_gap_three_methods(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                                min_body_ratio: float = 0.4) -> bool:
    """Detect Upside Gap Three Methods pattern (bullish continuation) - Bulkowski p. 331.
    :param c0: Bullish candle
    :param c1: Bullish candle with gap up
    :param c2: Bearish candle closing inside the gap
    :param min_body_ratio: Minimum body ratio for c0, c1
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and is_thick_bullish(c1, min_body_ratio)
            and gap_up(c0, c1)
            and not c2.is_bullish
            and c2.open > c0.close
            and c2.open < c1.open
            and c2.close > c0.close
            and c2.close < c1.open)

def is_downside_gap_three_methods(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                                  min_body_ratio: float = 0.4) -> bool:
    """Detect Downside Gap Three Methods pattern (bearish continuation) - Bulkowski p. 77.
    :param c0: Bearish candle
    :param c1: Bearish candle with gap down
    :param c2: Bullish candle closing inside the gap
    :param min_body_ratio: Minimum body ratio for c0, c1
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and is_thick_bearish(c1, min_body_ratio)
            and gap_down(c0, c1)
            and c2.is_bullish
            and c2.open < c0.close
            and c2.open > c1.open
            and c2.close < c0.close
            and c2.close > c1.open)

def is_side_by_side_white_lines(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                                tolerance_ratio: float = 0.02) -> bool:
    """Detect Side-by-Side White Lines pattern (bullish continuation)
    :param c0: Any candle (often bearish)
    :param c1: Bullish candle with gap up
    :param c2: Bullish candle with similar open/close as c1
    :param tolerance_ratio: Allowed deviation between c1/c2 open/close
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    tol = max(c1.length, c2.length, 1e-8) * tolerance_ratio
    return (c1.is_bullish and c2.is_bullish
            and gap_up(c0, c1)
            and abs(c1.open - c2.open) <= tol
            and abs(c1.close - c2.close) <= tol)

def is_upside_tasuki_gap(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                         min_body_ratio: float = 0.4) -> bool:
    """Detect Upside Tasuki Gap pattern (bullish continuation)
    :param c0: Bullish candle
    :param c1: Bullish candle with gap up
    :param c2: Bearish candle opening in gap and closing in c0's body
    :param min_body_ratio: Minimum body ratio for c0, c1
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and is_thick_bullish(c1, min_body_ratio)
            and gap_up(c0, c1)
            and not c2.is_bullish
            and c2.open > c0.close
            and c2.open < c1.open
            and c2.close > c0.body_low
            and c2.close < c1.open)

def is_bearish_tasuki_gap(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                          min_body_ratio: float = 0.4) -> bool:
    """Detect Bearish Tasuki Gap pattern (bearish continuation)
    :param c0: Bearish candle
    :param c1: Bearish candle with gap down
    :param c2: Bullish candle opening in gap and closing in c0's body
    :param min_body_ratio: Minimum body ratio for c0, c1
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and is_thick_bearish(c1, min_body_ratio)
            and gap_down(c0, c1)
            and c2.is_bullish
            and c2.open < c0.close
            and c2.open > c1.open
            and c2.close < c0.body_high
            and c2.close > c1.open)

def is_three_line_strike_bullish(c0: CandleStick, c1: CandleStick, c2: CandleStick, c3: CandleStick,
                                 min_body_ratio: float = 0.4) -> bool:
    """Detect Bullish Three-Line Strike pattern (bullish reversal)
    :param c0-c2: Three consecutive bearish candles
    :param c3: Bullish candle engulfing all three
    :param min_body_ratio: Minimum body ratio for all candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2, c3)):
        return False
    return (all(is_thick_bearish(c, min_body_ratio) for c in (c0, c1, c2))
            and c0.close > c1.close > c2.close
            and c3.is_bullish
            and c3.body_low < c2.body_low and c3.body_high > c0.body_high)

def is_three_line_strike_bearish(c0: CandleStick, c1: CandleStick, c2: CandleStick, c3: CandleStick,
                                 min_body_ratio: float = 0.4) -> bool:
    """Detect Bearish Three-Line Strike pattern (bearish reversal)
    :param c0-c2: Three consecutive bullish candles
    :param c3: Bearish candle engulfing all three
    :param min_body_ratio: Minimum body ratio for all candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2, c3)):
        return False
    return (all(c.is_bullish and is_thick_bullish(c, min_body_ratio) for c in (c0, c1, c2))
            and c0.close < c1.close < c2.close
            and not c3.is_bullish
            and c3.body_low < c0.body_low and c3.body_high > c2.body_high)

def is_two_crows(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                 min_body_ratio: float = 0.4) -> bool:
    """Detect Two Crows pattern (bearish reversal)
    :param c0: Long bullish candle
    :param c1: Bearish candle gapping above c0
    :param c2: Bearish candle engulfing c1
    :param min_body_ratio: Minimum body ratio for strong candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bullish(c0, min_body_ratio)
            and not c1.is_bullish
            and c1.open > c0.high
            and not c2.is_bullish
            and body_engulf(c1, c2)
            and c2.close < c0.close)


# --------------------------
# FOUR-CANDLE PATTERNS (Bulkowski Compliant)
# --------------------------

def is_concealing_baby_swallow(c0: CandleStick, c1: CandleStick, c2: CandleStick, c3: CandleStick,
                               min_body_ratio: float = 0.6) -> bool:
    """Detect Concealing Baby Swallow pattern (bearish continuation)
    :param c0: First bearish candle
    :param c1: Second bearish candle with gap down
    :param c2: Third bearish candle with upper shadow
    :param c3: Fourth bearish candle engulfing c2's upper shadow
    :param min_body_ratio: Minimum body ratio for strong candles
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2, c3)):
        return False
    return (all(not c.is_bullish for c in (c0, c1, c2, c3))
            and is_thick_bearish(c0, min_body_ratio)
            and is_thick_bearish(c1, min_body_ratio)
            and gap_down(c0, c1)
            and c2.top_wick > c2.length * 0.2
            and c3.high > c2.high
            and c3.close < c2.close)

def is_three_river_bottom(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                          min_body_ratio: float = 0.4) -> bool:
    """Detect Three River Bottom pattern (bullish reversal)
    :param c0: Long bearish candle
    :param c1: Hammer candle
    :param c2: Doji or spinning top contained in c1
    :param min_body_ratio: Minimum body ratio for c0
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and is_hammer(c1, max_body_ratio=0.3)
            and (is_doji(c2, max_body_ratio=0.2) or is_spinning_top(c2))
            and body_contained(c2, c1))

def is_unique_three_river_bottom(c0: CandleStick, c1: CandleStick, c2: CandleStick,
                                 min_body_ratio: float = 0.4) -> bool:
    """Detect Unique Three River Bottom pattern (bullish reversal)
    :param c0: Bearish candle with long lower shadow
    :param c1: Small bullish candle near c0 low
    :param c2: Bullish candle closing above c0 midpoint
    :param min_body_ratio: Minimum body ratio for c0
    """
    if not all(_valid_candle(c) for c in (c0, c1, c2)):
        return False
    return (is_thick_bearish(c0, min_body_ratio)
            and c0.bottom_wick > c0.body_length
            and c1.is_bullish
            and c1.close > c0.close
            and c2.is_bullish
            and c2.close > (c0.open + c0.close) / 2)