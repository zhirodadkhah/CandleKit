from .entity import CandleStick

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

def body_engulfs(prev: CandleStick, curr: CandleStick) -> bool:
    """Bullish engulfing: current body covers previous body."""
    return curr.open < prev.close and curr.close > prev.open

def body_engulfed(prev: CandleStick, curr: CandleStick) -> bool:
    """Bearish engulfing: current body covered by previous body."""
    return curr.open > prev.close and curr.close < prev.open


# --- SINGLE-CANDLE PATTERNS (with zero-length guard) ---
def is_doji(candle: CandleStick, max_body_ratio: float = 0.05) -> bool:
    """
    Candlestick's body is very small relative to its total length.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio. < 1
    :return: bool
    """
    if candle.length == 0:
        return False
    return candle.body_ratio <= max_body_ratio

def is_dragonfly(candle: CandleStick,
                 max_body_ratio: float = 0.05,
                 top_wick_ratio: float = 0.1,
                 bottom_wick_ratio: float = 0.6) -> bool:
    """
    Dragonfly Doji: long lower wick, no upper wick.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick max ratio to candle length
    :param bottom_wick_ratio: bottom wick min ratio to candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (is_doji(candle, max_body_ratio)
            and candle.top_wick <= candle.length * top_wick_ratio
            and candle.bottom_wick >= candle.length * bottom_wick_ratio)

def is_gravestone(candle: CandleStick,
                  max_body_ratio: float = 0.05,
                  top_wick_ratio: float = 0.6,
                  bottom_wick_ratio: float = 0.1) -> bool:
    """
    Gravestone Doji: long upper wick, no lower wick.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick min ratio to candle length
    :param bottom_wick_ratio: bottom wick max ratio to candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (is_doji(candle, max_body_ratio)
            and candle.top_wick >= candle.length * top_wick_ratio
            and candle.bottom_wick <= candle.length * bottom_wick_ratio)

def is_long_legged(candle: CandleStick,
                   max_body_ratio: float = 0.05,
                   min_wick_ratio: float = 0.4) -> bool:
    """
    Long-Legged Doji: both wicks are long.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param min_wick_ratio: minimum ratio for both top and bottom wicks relative to candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (is_doji(candle, max_body_ratio)
            and candle.top_wick >= candle.length * min_wick_ratio
            and candle.bottom_wick >= candle.length * min_wick_ratio)

def is_hammer(candle: CandleStick,
              max_body_ratio: float = 0.3,
              top_wick_ratio: float = 0.1,
              bottom_wick_ratio: float = 0.6) -> bool:
    """
    Hammer: small body, long lower wick — bullish reversal signal (shape only).
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick max ratio to candle length
    :param bottom_wick_ratio: bottom wick min ratio to candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (candle.body_ratio <= max_body_ratio
            and candle.top_wick <= candle.length * top_wick_ratio
            and candle.bottom_wick >= candle.length * bottom_wick_ratio)

def is_hanging_man(candle: CandleStick,
                   max_body_ratio: float = 0.3,
                   top_wick_ratio: float = 0.1,
                   bottom_wick_ratio: float = 0.6) -> bool:
    """
    Hanging Man: small body, long lower wick — bearish reversal signal (shape only).
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick max ratio to candle length
    :param bottom_wick_ratio: bottom wick min ratio to candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (candle.body_ratio <= max_body_ratio
            and candle.top_wick <= candle.length * top_wick_ratio
            and candle.bottom_wick >= candle.length * bottom_wick_ratio)

def is_inverted_hammer(candle: CandleStick,
                       max_body_ratio: float = 0.3,
                       top_wick_ratio: float = 0.6,
                       bottom_wick_ratio: float = 0.1) -> bool:
    """
    Inverted Hammer: small body, long upper wick — bullish signal (shape only).
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick min ratio to candle length
    :param bottom_wick_ratio: bottom wick max ratio to candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (candle.body_ratio <= max_body_ratio
            and candle.top_wick >= candle.length * top_wick_ratio
            and candle.bottom_wick <= candle.length * bottom_wick_ratio)

def is_shooting_star(candle: CandleStick,
                     max_body_ratio: float = 0.3,
                     top_wick_ratio: float = 0.6,
                     bottom_wick_ratio: float = 0.1) -> bool:
    """
    Shooting Star: small body, long upper wick — bearish signal (shape only).
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick min ratio to candle length
    :param bottom_wick_ratio: bottom wick max ratio to candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (candle.body_ratio <= max_body_ratio
            and candle.top_wick >= candle.length * top_wick_ratio
            and candle.bottom_wick <= candle.length * bottom_wick_ratio)

def is_spinning_top(candle: CandleStick,
                    max_body_ratio: float = 0.5,
                    min_wick_ratio: float = 0.2) -> bool:
    """
    Spinning Top: small body with long wicks — indecision.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param min_wick_ratio: minimum ratio for both top and bottom wicks relative to candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (candle.body_ratio <= max_body_ratio
            and candle.top_wick >= candle.length * min_wick_ratio
            and candle.bottom_wick >= candle.length * min_wick_ratio)

def is_marubozu(candle: CandleStick, max_wick_ratio: float = 0.05) -> bool:
    """
    Marubozu: candle with no wicks — strong conviction.
    :param candle: CandleStick
    :param max_wick_ratio: maximum allowed wick (top or bottom) as ratio of candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    return (candle.top_wick <= candle.length * max_wick_ratio
            and candle.bottom_wick <= candle.length * max_wick_ratio)

def is_bullish_belt_hold(candle: CandleStick,
                         min_body_ratio: float = 0.7,
                         max_lower_wick_ratio: float = 0.05) -> bool:
    """
    Bullish Belt Hold: opens at low, strong bullish move.
    :param candle: CandleStick
    :param min_body_ratio: minimum body/candle ratio (strong bullish body)
    :param max_lower_wick_ratio: maximum lower wick as ratio of candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    open_eq_low = abs(candle.open - candle.low) <= max(candle.low * 1e-5, 1e-9)
    return (is_thick_bullish(candle, min_body_ratio)
            and candle.bottom_wick <= candle.length * max_lower_wick_ratio
            and open_eq_low)

def is_bearish_belt_hold(candle: CandleStick,
                         min_body_ratio: float = 0.7,
                         max_upper_wick_ratio: float = 0.05) -> bool:
    """
    Bearish Belt Hold: opens at high, strong bearish move.
    :param candle: CandleStick
    :param min_body_ratio: minimum body/candle ratio (strong bearish body)
    :param max_upper_wick_ratio: maximum upper wick as ratio of candle length
    :return: bool
    """
    if candle.length == 0:
        return False
    open_eq_high = abs(candle.open - candle.high) <= max(candle.high * 1e-5, 1e-9)
    return (is_thick_bearish(candle, min_body_ratio)
            and candle.top_wick <= candle.length * max_upper_wick_ratio
            and open_eq_high)

# --- TWO-CANDLE PATTERNS ---
def is_bullish_engulfing(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Bullish Engulfing: bearish candle engulfed by larger bullish candle.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles to be meaningful
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0:
        return False
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and body_engulfs(prev, curr))

def is_bearish_engulfing(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Bearish Engulfing: bullish candle engulfed by larger bearish candle.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles to be meaningful
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0:
        return False
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and body_engulfed(prev, curr))

def is_piercing_line(candles: list,
                     min_body_ratio: float = 0.3,
                     min_penetration: float = 0.5) -> bool:
    """
    Piercing Line: bullish reversal after downtrend; closes >50% into prior bearish body.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles
    :param min_penetration: minimum fraction of prior bearish body that current candle must penetrate
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0:
        return False
    body_prev = prev.open - prev.close
    penetration = curr.close - prev.close
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and gap_down(prev, curr)
            and penetration >= body_prev * min_penetration)

def is_dark_cloud_cover(candles: list,
                        min_body_ratio: float = 0.3,
                        min_penetration: float = 0.5) -> bool:
    """
    Dark Cloud Cover: bearish reversal after uptrend; closes >50% into prior bullish body.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles
    :param min_penetration: minimum fraction of prior bullish body that current candle must penetrate
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0:
        return False
    body_prev = prev.close - prev.open
    penetration = prev.close - curr.close
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and gap_up(prev, curr)
            and penetration >= body_prev * min_penetration)

def is_bullish_harami(candles: list,
                      min_body_ratio: float = 0.3,
                      max_inside_body_ratio: float = 0.5) -> bool:
    """
    Bullish Harami: bearish candle followed by small bullish candle **with body inside prior body**.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for the first candle
    :param max_inside_body_ratio: maximum body/candle ratio for the second candle
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0:
        return False
    # Body containment: curr's open/close within prev's open/close
    prev_body_low = min(prev.open, prev.close)
    prev_body_high = max(prev.open, prev.close)
    curr_body_contained = (prev_body_low <= curr.open <= prev_body_high and
                           prev_body_low <= curr.close <= prev_body_high)
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thin_bullish(curr, max_inside_body_ratio)
            and curr_body_contained)

def is_bearish_harami(candles: list,
                      min_body_ratio: float = 0.3,
                      max_inside_body_ratio: float = 0.5) -> bool:
    """
    Bearish Harami: bullish candle followed by small bearish candle **with body inside prior body**.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for the first candle
    :param max_inside_body_ratio: maximum body/candle ratio for the second candle
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0:
        return False
    prev_body_low = min(prev.open, prev.close)
    prev_body_high = max(prev.open, prev.close)
    curr_body_contained = (prev_body_low <= curr.open <= prev_body_high and
                           prev_body_low <= curr.close <= prev_body_high)
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thin_bearish(curr, max_inside_body_ratio)
            and curr_body_contained)

def is_tweezer_tops(candles: list,
                    min_body_ratio: float = 0.2,
                    price_tolerance: float = 0.01) -> bool:
    """
    Tweezer Tops: two candles with nearly identical highs after uptrend; second shows bearish rejection.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for first candle
    :param price_tolerance: max allowed high difference as ratio of average candle length
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    avg_length = (prev.length + curr.length) / 2
    if avg_length == 0:
        return False
    # First candle: strong bullish (uptrend context)
    # Second: bearish or has long upper wick (rejection)
    return (is_thick_bullish(prev, min_body_ratio)
            and (curr.is_bearish or curr.top_wick > curr.body_length)
            and abs(prev.high - curr.high) <= avg_length * price_tolerance)

def is_tweezer_bottoms(candles: list,
                       min_body_ratio: float = 0.2,
                       price_tolerance: float = 0.01) -> bool:
    """
    Tweezer Bottoms: two candles with nearly identical lows after downtrend; second shows bullish rejection.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for first candle
    :param price_tolerance: max allowed low difference as ratio of average candle length
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    avg_length = (prev.length + curr.length) / 2
    if avg_length == 0:
        return False
    return (is_thick_bearish(prev, min_body_ratio)
            and (curr.is_bullish or curr.bottom_wick > curr.body_length)
            and abs(prev.low - curr.low) <= avg_length * price_tolerance)


# --- THREE-CANDLE PATTERNS ---
def is_morning_star(candles: list,
                    min_body_ratio: float = 0.3,
                    max_middle_body_ratio: float = 0.1) -> bool:
    """
    Morning Star: bearish → small body → bullish; reversal after downtrend.
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for first and third candles
    :param max_middle_body_ratio: maximum body/candle ratio for middle candle
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (is_thick_bearish(prev, min_body_ratio)
            and curr.body_ratio <= max_middle_body_ratio
            and is_thick_bullish(nxt, min_body_ratio)
            and gap_down(prev, curr)
            and nxt.close > (prev.open + prev.close) / 2)

def is_evening_star(candles: list,
                    min_body_ratio: float = 0.3,
                    max_middle_body_ratio: float = 0.1) -> bool:
    """
    Evening Star: bullish → small body → bearish; reversal after uptrend.
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for first and third candles
    :param max_middle_body_ratio: maximum body/candle ratio for middle candle
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (is_thick_bullish(prev, min_body_ratio)
            and curr.body_ratio <= max_middle_body_ratio
            and is_thick_bearish(nxt, min_body_ratio)
            and gap_up(prev, curr)
            and nxt.close < (prev.open + prev.close) / 2)

def is_three_white_soldiers(candles: list, min_body_ratio: float = 0.4) -> bool:
    """
    Three White Soldiers: three strong bullish candles in a row.
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all three candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    tolerance = max(prev.length, curr.length, nxt.length) * 0.05
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and is_thick_bullish(nxt, min_body_ratio)
            and abs(curr.open - (prev.open + prev.close) / 2) <= tolerance
            and abs(nxt.open - (curr.open + curr.close) / 2) <= tolerance
            and curr.close > prev.close
            and nxt.close > curr.close)

def is_three_black_crows(candles: list, min_body_ratio: float = 0.4) -> bool:
    """
    Three Black Crows: three strong bearish candles in a row.
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all three candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    tolerance = max(prev.length, curr.length, nxt.length) * 0.05
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and is_thick_bearish(nxt, min_body_ratio)
            and abs(curr.open - (prev.open + prev.close) / 2) <= tolerance
            and abs(nxt.open - (curr.open + curr.close) / 2) <= tolerance
            and curr.close < prev.close
            and nxt.close < curr.close)

def is_morning_doji_star(candles: list,
                         min_body_ratio: float = 0.3,
                         max_doji_body_ratio: float = 0.05) -> bool:
    """
    Morning Doji Star: bearish → Doji → bullish; stronger reversal signal.
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for first and third candles
    :param max_doji_body_ratio: maximum body/candle ratio for middle Doji candle
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (is_doji(curr, max_doji_body_ratio)
            and is_thick_bearish(prev, min_body_ratio)
            and is_thick_bullish(nxt, min_body_ratio)
            and gap_down(prev, curr)
            and nxt.close > (prev.open + prev.close) / 2)

def is_evening_doji_star(candles: list,
                         min_body_ratio: float = 0.3,
                         max_doji_body_ratio: float = 0.05) -> bool:
    """
    Evening Doji Star: bullish → Doji → bearish; stronger reversal signal.
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for first and third candles
    :param max_doji_body_ratio: maximum body/candle ratio for middle Doji candle
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (is_doji(curr, max_doji_body_ratio)
            and is_thick_bullish(prev, min_body_ratio)
            and is_thick_bearish(nxt, min_body_ratio)
            and gap_up(prev, curr)
            and nxt.close < (prev.open + prev.close) / 2)

def is_bullish_tasuki_gap(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Bullish Tasuki Gap: in uptrend, bullish gap, then small bearish closing **partially into gap** (not fully).
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    # Must be in uptrend
    if not (prev.is_bullish and curr.is_bullish):
        return False
    # Gap exists
    if not (curr.low > prev.high):
        return False
    # Third candle closes into gap, but not below prev.high (partial fill)
    if not (nxt.close > prev.high and nxt.close < curr.low):
        return False
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and nxt.is_bullish)  # Can be small bullish or neutral

def is_bearish_tasuki_gap(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Bearish Tasuki Gap: in downtrend, bearish gap, then small bullish closing **partially into gap** (not fully).
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    # Must be in downtrend
    if not (not prev.is_bullish and not curr.is_bullish):
        return False
    # Gap exists
    if not (curr.high < prev.low):
        return False
    # Third candle closes into gap, but not above prev.low
    if not (nxt.close < prev.low and nxt.close > curr.high):
        return False
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and not nxt.is_bullish)


def is_bullish_kicking(candles: list, max_wick_ratio: float = 0.05) -> bool:
    """
    Bullish Kicking: bearish marubozu followed by bullish marubozu with upward gap.
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_wick_ratio: tolerance for wicks in marubozu
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0:
        return False
    return (not prev.is_bullish
            and is_marubozu(prev, max_wick_ratio)
            and curr.is_bullish
            and is_marubozu(curr, max_wick_ratio)
            and gap_up(prev, curr))

def is_bearish_kicking(candles: list, max_wick_ratio: float = 0.05) -> bool:
    """
    Bearish Kicking: bullish marubozu followed by bearish marubozu with downward gap.
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_wick_ratio: tolerance for wicks in marubozu
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0:
        return False
    return (prev.is_bullish
            and is_marubozu(prev, max_wick_ratio)
            and not curr.is_bullish
            and is_marubozu(curr, max_wick_ratio)
            and gap_down(prev, curr))

# --- ABANDONED BABY ---
def is_bullish_abandoned_baby(candles: list,
                              max_body_ratio: float = 0.05,
                              require_gap: bool = True) -> bool:
    """
    Bullish Abandoned Baby: rare strong reversal with gaps around Doji.
    :param candles: list of at least 3 CandleStick (latest last)
    :param max_body_ratio: max body ratio for Doji
    :param require_gap: if False, skips gap validation
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (not prev.is_bullish
            and is_doji(curr, max_body_ratio)
            and nxt.is_bullish
            and (not require_gap or (curr.low > prev.high and nxt.low > curr.high)))

def is_bearish_abandoned_baby(candles: list,
                              max_body_ratio: float = 0.05,
                              require_gap: bool = True) -> bool:
    """
    Bearish Abandoned Baby: rare strong reversal with gaps around Doji.
    :param candles: list of at least 3 CandleStick (latest last)
    :param max_body_ratio: max body ratio for Doji
    :param require_gap: if False, skips gap validation
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (prev.is_bullish
            and is_doji(curr, max_body_ratio)
            and not nxt.is_bullish
            and (not require_gap or (curr.high < prev.low and nxt.high < curr.low)))

# --- INSIDE/OUTSIDE, SANDWICH, COUNTERATTACK ---
def is_three_inside_up(candles: list, close_above_open: bool = True) -> bool:
    """
    Three Inside Up: bearish → inside bullish → bullish break.
    :param candles: list of at least 3 CandleStick
    :param close_above_open: if True, requires final candle to close above first candle's open
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (not prev.is_bullish
            and curr.is_bullish
            and prev.low <= curr.low
            and curr.high <= prev.high
            and nxt.is_bullish
            and (not close_above_open or nxt.close > prev.open))

def is_three_inside_down(candles: list, close_below_open: bool = True) -> bool:
    """
    Three Inside Down: bullish → inside bearish → bearish break.
    :param candles: list of at least 3 CandleStick
    :param close_below_open: if True, requires final candle to close below first candle's open
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (prev.is_bullish
            and not curr.is_bullish
            and prev.low <= curr.low
            and curr.high <= prev.high
            and not nxt.is_bullish
            and (not close_below_open or nxt.close < prev.open))

def is_three_outside_up(candles: list, strict_engulfing: bool = True) -> bool:
    """
    Three Outside Up: bearish → engulfing bullish → bullish confirmation.
    :param candles: list of at least 3 CandleStick
    :param strict_engulfing: if True, uses body-based engulfing; else uses full range
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (not prev.is_bullish
            and curr.is_bullish
            and nxt.is_bullish
            and nxt.close > curr.close
            and body_engulfs(prev, curr))

def is_three_outside_down(candles: list, strict_engulfing: bool = True) -> bool:
    """
    Three Outside Down: bullish → engulfing bearish → bearish confirmation.
    :param candles: list of at least 3 CandleStick
    :param strict_engulfing: if True, uses body-based engulfing; else uses full range
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (prev.is_bullish
            and not curr.is_bullish
            and not nxt.is_bullish
            and nxt.close < curr.close
            and body_engulfed(prev, curr))

def is_bullish_stick_sandwich(candles: list, close_tolerance: float = 0.005) -> bool:
    """
    Bullish Stick Sandwich: support holds as price closes back to prior close.
    :param candles: list of at least 3 CandleStick (latest last)
    :param close_tolerance: max allowed ratio difference between first and third closes
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0:
        return False
    return (not prev.is_bullish
            and curr.is_bullish
            and not nxt.is_bullish
            and abs(nxt.close - prev.close) <= prev.length * close_tolerance)

def is_bearish_stick_sandwich(candles: list, close_tolerance: float = 0.005) -> bool:
    """
    Bearish Stick Sandwich: resistance holds as price closes back to prior close.
    :param candles: list of at least 3 CandleStick (latest last)
    :param close_tolerance: max allowed ratio difference between first and third closes
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0:
        return False
    return (prev.is_bullish
            and not curr.is_bullish
            and nxt.is_bullish
            and abs(nxt.close - prev.close) <= prev.length * close_tolerance)

def is_bullish_counterattack(candles: list,
                             max_body_ratio: float = 0.05,
                             close_tolerance: float = 0.01) -> bool:
    """
    Bullish Counterattack: rejection of new lows; closes back to prior close.
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_body_ratio: max body ratio for confirmation candle
    :param close_tolerance: max allowed ratio difference between first and second closes
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0:
        return False
    return (not prev.is_bullish
            and gap_down(prev, curr)
            and abs(curr.close - prev.close) <= prev.length * close_tolerance
            and curr.body_length >= prev.body_length * 0.5
            and is_thin_enough(curr, max_body_ratio))

def is_bearish_counterattack(candles: list,
                             max_body_ratio: float = 0.05,
                             close_tolerance: float = 0.01) -> bool:
    """
    Bearish Counterattack: rejection of new highs; closes back to prior close.
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_body_ratio: max body ratio for confirmation candle
    :param close_tolerance: max allowed ratio difference between first and second closes
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    if prev.length == 0:
        return False
    return (prev.is_bullish
            and gap_up(prev, curr)
            and abs(curr.close - prev.close) <= prev.length * close_tolerance
            and curr.body_length >= prev.body_length * 0.5
            and is_thin_enough(curr, max_body_ratio))

# === NEW HIGH/MEDIUM RELIABILITY PATTERNS (Bulkowski) ===

def is_three_river_bottom(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Three River Bottom: bearish → Doji (new low) → small bullish closing above first candle's midpoint.
    Rare bullish reversal with 77% success (Bulkowski).
    :param candles: list of at least 3 CandleStick
    :param min_body_ratio: minimum body ratio for first candle
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (is_thick_bearish(prev, min_body_ratio)
            and is_doji(curr, max_body_ratio=0.05)
            and nxt.is_bullish
            and nxt.body_ratio <= 0.3
            and curr.low < prev.low
            and nxt.low > curr.low
            and nxt.close > (prev.open + prev.close) / 2)

def is_three_mountain_top(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Three Mountain Top: bullish → Doji (new high) → small bearish closing below first candle's midpoint.
    Bearish counterpart to Three River Bottom.
    :param candles: list of at least 3 CandleStick
    :param min_body_ratio: minimum body ratio for first candle
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (is_thick_bullish(prev, min_body_ratio)
            and is_doji(curr, max_body_ratio=0.05)
            and not nxt.is_bullish
            and nxt.body_ratio <= 0.3
            and curr.high > prev.high
            and nxt.high < curr.high
            and nxt.close < (prev.open + prev.close) / 2)

def is_upside_gap_three_methods(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Upside Gap Three Methods: bullish → bullish gap → small bearish closing into gap.
    Bullish continuation pattern.
    :param candles: list of at least 3 CandleStick
    :param min_body_ratio: minimum body ratio for first two candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and gap_up(prev, curr)
            and not nxt.is_bullish
            and nxt.close > prev.high
            and nxt.close < curr.low)

def is_downside_gap_three_methods(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Downside Gap Three Methods: bearish → bearish gap → small bullish closing into gap.
    Bearish continuation pattern.
    :param candles: list of at least 3 CandleStick
    :param min_body_ratio: minimum body ratio for first two candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    if prev.length == 0 or curr.length == 0 or nxt.length == 0:
        return False
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and gap_down(prev, curr)
            and nxt.is_bullish
            and nxt.close < prev.low
            and nxt.close > curr.high)

def is_bullish_breakaway(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Bullish Breakaway: downtrend → long bearish → Doji/gap → 2 bullish candles closing above first candle's high.
    Strong bullish reversal.
    :param candles: list of at least 5 CandleStick
    :param min_body_ratio: minimum body ratio for confirmation candles
    :return: bool
    """
    if len(candles) < 5:
        return False
    c1, c2, c3, c4, c5 = candles[-5], candles[-4], candles[-3], candles[-2], candles[-1]
    if c1.length == 0 or c5.length == 0:
        return False
    downtrend = not c1.is_bullish and not c2.is_bullish
    return (downtrend
            and is_doji(c3, max_body_ratio=0.1)
            and is_thick_bullish(c4, min_body_ratio)
            and is_thick_bullish(c5, min_body_ratio)
            and c5.close > c1.high)

def is_bearish_breakaway(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Bearish Breakaway: uptrend → long bullish → Doji/gap → 2 bearish candles closing below first candle's low.
    Strong bearish reversal.
    :param candles: list of at least 5 CandleStick
    :param min_body_ratio: minimum body ratio for confirmation candles
    :return: bool
    """
    if len(candles) < 5:
        return False
    c1, c2, c3, c4, c5 = candles[-5], candles[-4], candles[-3], candles[-2], candles[-1]
    if c1.length == 0 or c5.length == 0:
        return False
    uptrend = c1.is_bullish and c2.is_bullish
    return (uptrend
            and is_doji(c3, max_body_ratio=0.1)
            and is_thick_bearish(c4, min_body_ratio)
            and is_thick_bearish(c5, min_body_ratio)
            and c5.close < c1.low)

def is_concealing_baby_swalllow(candles: list, tolerance: float = 1e-5) -> bool:
    """
    Concealing Baby Swallow: 4 bearish marubozu candles, each opening within prior body.
    Rare bearish continuation (68% success).
    :param candles: list of at least 4 CandleStick
    :param tolerance: tolerance for open within prior body (relative)
    :return: bool
    """
    if len(candles) < 4:
        return False
    c1, c2, c3, c4 = candles[-4], candles[-3], candles[-2], candles[-1]
    if any(c.length == 0 for c in [c1, c2, c3, c4]):
        return False

    def open_in_body(curr, prev):
        lower = min(prev.open, prev.close)
        upper = max(prev.open, prev.close)
        return lower - tolerance <= curr.open <= upper + tolerance

    return (is_marubozu(c1, max_wick_ratio=0.03)
            and is_marubozu(c2, max_wick_ratio=0.03)
            and is_marubozu(c3, max_wick_ratio=0.03)
            and is_marubozu(c4, max_wick_ratio=0.03)
            and not c1.is_bullish and not c2.is_bullish and not c3.is_bullish and not c4.is_bullish
            and open_in_body(c2, c1)
            and open_in_body(c3, c2)
            and open_in_body(c4, c3))

def is_ladder_bottom(candles: list, min_body_ratio: float = 0.3, min_wick_ratio: float = 0.6) -> bool:
    """
    Ladder Bottom: 4 consecutive lower lows with long lower shadows, then strong bullish reversal.
    Bullish reversal with 61% success.
    :param candles: list of at least 5 CandleStick
    :param min_body_ratio: minimum body ratio for final bullish candle
    :param min_wick_ratio: minimum lower wick ratio for first 4 candles
    :return: bool
    """
    if len(candles) < 5:
        return False
    c1, c2, c3, c4, c5 = candles[-5], candles[-4], candles[-3], candles[-2], candles[-1]
    if any(c.length == 0 for c in [c1, c2, c3, c4, c5]):
        return False
    downtrend = (not c1.is_bullish and not c2.is_bullish and not c3.is_bullish and not c4.is_bullish
                 and c2.low < c1.low and c3.low < c2.low and c4.low < c3.low)
    long_wicks = (c1.bottom_wick >= c1.length * min_wick_ratio
                  and c2.bottom_wick >= c2.length * min_wick_ratio
                  and c3.bottom_wick >= c3.length * min_wick_ratio
                  and c4.bottom_wick >= c4.length * min_wick_ratio)
    return (downtrend
            and long_wicks
            and is_thick_bullish(c5, min_body_ratio)
            and c5.close > c4.open)

def is_advance_block(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Advance Block: 3 bullish candles with diminishing body ratios and long upper wicks.
    Bearish reversal in uptrend.
    :param candles: list of at least 3 CandleStick
    :param min_body_ratio: minimum body ratio for first candle
    :return: bool
    """
    if len(candles) < 3:
        return False
    c1, c2, c3 = candles[-3], candles[-2], candles[-1]
    if c1.length == 0 or c2.length == 0 or c3.length == 0:
        return False
    return (is_thick_bullish(c1, min_body_ratio)
            and c2.is_bullish and c3.is_bullish
            and c2.body_ratio < c1.body_ratio
            and c3.body_ratio < c2.body_ratio
            and c2.top_wick > c2.body_length
            and c3.top_wick > c3.body_length)

def is_deliberation(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Deliberation: 3 strong bullish candles; third has small body (indecision).
    Bearish reversal warning.
    :param candles: list of at least 3 CandleStick
    :param min_body_ratio: minimum body ratio for first two candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    c1, c2, c3 = candles[-3], candles[-2], candles[-1]
    if c1.length == 0 or c2.length == 0 or c3.length == 0:
        return False
    return (is_thick_bullish(c1, min_body_ratio)
            and is_thick_bullish(c2, min_body_ratio)
            and c3.is_bullish
            and c3.body_ratio <= 0.3)