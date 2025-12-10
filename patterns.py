from entity import CandleStick

# --- Shared helpers ---
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


def is_doji(candle: CandleStick, max_body_ratio: float = 0.05) -> bool:
    """
    Candlestick's body is very small relative to its total length.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio. < 1
    :return: bool
    """
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
    return (is_doji(candle, max_body_ratio)
            and candle.top_wick >= candle.length * min_wick_ratio
            and candle.bottom_wick >= candle.length * min_wick_ratio)


def is_hammer(candle: CandleStick,
              max_body_ratio: float = 0.3,
              top_wick_ratio: float = 0.1,
              bottom_wick_ratio: float = 0.6) -> bool:
    """
    Hammer: bullish reversal at support.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick max ratio to candle length
    :param bottom_wick_ratio: bottom wick min ratio to candle length
    :return: bool
    """
    return (is_thin_bullish(candle, max_body_ratio)
            and candle.top_wick <= candle.length * top_wick_ratio
            and candle.bottom_wick >= candle.length * bottom_wick_ratio)


def is_hanging_man(candle: CandleStick,
                   max_body_ratio: float = 0.3,
                   top_wick_ratio: float = 0.1,
                   bottom_wick_ratio: float = 0.6) -> bool:
    """
    Hanging Man: bearish reversal at resistance.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick max ratio to candle length
    :param bottom_wick_ratio: bottom wick min ratio to candle length
    :return: bool
    """
    return (is_thin_bearish(candle, max_body_ratio)
            and candle.top_wick <= candle.length * top_wick_ratio
            and candle.bottom_wick >= candle.length * bottom_wick_ratio)


def is_inverted_hammer(candle: CandleStick,
                       max_body_ratio: float = 0.3,
                       top_wick_ratio: float = 0.6,
                       bottom_wick_ratio: float = 0.1) -> bool:
    """
    Inverted Hammer: early bullish signal after downtrend.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick min ratio to candle length
    :param bottom_wick_ratio: bottom wick max ratio to candle length
    :return: bool
    """
    return (is_thin_bullish(candle, max_body_ratio)
            and candle.top_wick >= candle.length * top_wick_ratio
            and candle.bottom_wick <= candle.length * bottom_wick_ratio)


def is_shooting_star(candle: CandleStick,
                     max_body_ratio: float = 0.3,
                     top_wick_ratio: float = 0.6,
                     bottom_wick_ratio: float = 0.1) -> bool:
    """
    Shooting Star: bearish reversal after uptrend.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick min ratio to candle length
    :param bottom_wick_ratio: bottom wick max ratio to candle length
    :return: bool
    """
    return (is_thin_bearish(candle, max_body_ratio)
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
    return (is_thin_enough(candle, max_body_ratio)
            and candle.top_wick >= candle.length * min_wick_ratio
            and candle.bottom_wick >= candle.length * min_wick_ratio)


def is_marubozu(candle: CandleStick, max_wick_ratio: float = 0.05) -> bool:
    """
    Marubozu: candle with no wicks — strong conviction.
    :param candle: CandleStick
    :param max_wick_ratio: maximum allowed wick (top or bottom) as ratio of candle length
    :return: bool
    """
    return (candle.top_wick <= candle.length * max_wick_ratio
            and candle.bottom_wick <= candle.length * max_wick_ratio)


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
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and curr.open <= prev.close
            and curr.close >= prev.open)


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
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and curr.open >= prev.close
            and curr.close <= prev.open)


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
    body_prev = prev.open - prev.close
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and curr.open <= prev.low
            and curr.close > prev.open
            and (curr.close - prev.open) >= body_prev * min_penetration)


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
    body_prev = prev.close - prev.open
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and curr.open >= prev.high
            and curr.close < prev.close
            and (prev.close - curr.close) >= body_prev * min_penetration)


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
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thin_enough(curr, max_middle_body_ratio)
            and is_thick_bullish(nxt, min_body_ratio)
            and curr.low < prev.low
            and nxt.close > prev.open)


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
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thin_enough(curr, max_middle_body_ratio)
            and is_thick_bearish(nxt, min_body_ratio)
            and curr.high > prev.high
            and nxt.close < prev.close)


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
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and is_thick_bullish(nxt, min_body_ratio)
            and curr.open > prev.open
            and curr.open < prev.close
            and nxt.open > curr.open
            and nxt.open < curr.close
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
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and is_thick_bearish(nxt, min_body_ratio)
            and curr.open < prev.open
            and curr.open > prev.close
            and nxt.open < curr.open
            and nxt.open > curr.close
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
    return (is_doji(curr, max_doji_body_ratio)
            and is_thick_bearish(prev, min_body_ratio)
            and is_thick_bullish(nxt, min_body_ratio)
            and curr.low < prev.low
            and nxt.close > prev.open)


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
    return (is_doji(curr, max_doji_body_ratio)
            and is_thick_bullish(prev, min_body_ratio)
            and is_thick_bearish(nxt, min_body_ratio)
            and curr.high > prev.high
            and nxt.close < prev.close)


def is_tweezer_tops(candles: list,
                    min_body_ratio: float = 0.2,
                    price_tolerance: float = 0.01) -> bool:
    """
    Tweezer Tops: two candles with nearly identical highs after uptrend.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles
    :param price_tolerance: max allowed high difference as ratio of average candle length
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    avg_length = (prev.length + curr.length) / 2
    if avg_length == 0:
        return False
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and abs(prev.high - curr.high) <= avg_length * price_tolerance)


def is_tweezer_bottoms(candles: list,
                       min_body_ratio: float = 0.2,
                       price_tolerance: float = 0.01) -> bool:
    """
    Tweezer Bottoms: two candles with nearly identical lows after downtrend.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles
    :param price_tolerance: max allowed low difference as ratio of average candle length
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    avg_length = (prev.length + curr.length) / 2
    if avg_length == 0:
        return False
    return (is_thick_enough(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and abs(prev.low - curr.low) <= avg_length * price_tolerance)


def is_bullish_harami(candles: list,
                      min_body_ratio: float = 0.3,
                      max_inside_body_ratio: float = 0.5) -> bool:
    """
    Bullish Harami: bearish candle followed by small bullish candle inside its range.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for the first candle
    :param max_inside_body_ratio: maximum body/candle ratio for the second candle
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    return (is_thick_bearish(prev, min_body_ratio)
            and is_thin_bullish(curr, max_inside_body_ratio)
            and prev.low <= curr.low
            and curr.high <= prev.high)


def is_bearish_harami(candles: list,
                      min_body_ratio: float = 0.3,
                      max_inside_body_ratio: float = 0.5) -> bool:
    """
    Bearish Harami: bullish candle followed by small bearish candle inside its range.
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for the first candle
    :param max_inside_body_ratio: maximum body/candle ratio for the second candle
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    return (is_thick_bullish(prev, min_body_ratio)
            and is_thin_bearish(curr, max_inside_body_ratio)
            and prev.low <= curr.low
            and curr.high <= prev.high)


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
    return (is_thick_bullish(candle, min_body_ratio)
            and candle.bottom_wick <= candle.length * max_lower_wick_ratio
            and abs(candle.open - candle.low) <= 1e-9)


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
    return (is_thick_bearish(candle, min_body_ratio)
            and candle.top_wick <= candle.length * max_upper_wick_ratio
            and abs(candle.open - candle.high) <= 1e-9)


def is_bullish_tasuki_gap(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Bullish Tasuki Gap: bullish continuation with partial gap fill.
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    return (curr.low > prev.high
            and nxt.close > prev.high
            and nxt.close < curr.low
            and is_thick_bullish(prev, min_body_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and is_thick_bullish(nxt, min_body_ratio))


def is_bearish_tasuki_gap(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    Bearish Tasuki Gap: bearish continuation with partial gap fill.
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all candles
    :return: bool
    """
    if len(candles) < 3:
        return False
    prev, curr, nxt = candles[-3], candles[-2], candles[-1]
    return (curr.high < prev.low
            and nxt.close < prev.low
            and nxt.close > curr.high
            and is_thick_bearish(prev, min_body_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and is_thick_bearish(nxt, min_body_ratio))


def is_bullish_kicking(candles: list, max_wick_ratio: float = 0.05, min_body_ratio: float = 0.7) -> bool:
    """
    Bullish Kicking: bearish marubozu followed by bullish marubozu with upward gap.
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_wick_ratio: tolerance for wicks in marubozu
    :param min_body_ratio: minimum body/candle ratio for all candles
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    return (is_thick_bearish(prev, min_body_ratio)
            and is_marubozu(prev, max_wick_ratio)
            and is_thick_bullish(curr, min_body_ratio)
            and is_marubozu(curr, max_wick_ratio)
            and curr.open > prev.open)



def is_bearish_kicking(candles: list, max_wick_ratio: float = 0.05, min_body_ratio: float = 0.7) -> bool:
    """
    Bearish Kicking: bullish marubozu followed by bearish marubozu with downward gap.
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_wick_ratio: tolerance for wicks in marubozu
    :param min_body_ratio: minimum body/candle ratio for all candles
    :return: bool
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]
    return (is_thick_bullish(prev, min_body_ratio)
            and is_marubozu(prev, max_wick_ratio)
            and is_thick_bearish(curr, min_body_ratio)
            and is_marubozu(curr, max_wick_ratio)
            and curr.open < prev.open)


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
    return (not prev.is_bullish
            and is_doji(curr, max_body_ratio)
            and nxt.is_bullish
            and (not require_gap or (curr.high < prev.low and nxt.low > curr.high)))


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
    return (prev.is_bullish
            and is_doji(curr, max_body_ratio)
            and not nxt.is_bullish
            and (not require_gap or (curr.low > prev.high and nxt.high < curr.low)))


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
    return (not prev.is_bullish
            and curr.is_bullish
            and nxt.is_bullish
            and nxt.close > curr.close
            and (strict_engulfing and (curr.open <= prev.close and curr.close >= prev.open)
                 or (not strict_engulfing and curr.open <= prev.open and curr.close >= prev.close)))


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
    return (prev.is_bullish
            and not curr.is_bullish
            and not nxt.is_bullish
            and nxt.close < curr.close
            and (strict_engulfing and (curr.open >= prev.close and curr.close <= prev.open)
                 or (not strict_engulfing and curr.open >= prev.open and curr.close <= prev.close)))


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
    return (not prev.is_bullish
            and curr.is_bullish
            and not nxt.is_bullish
            and prev.length > 0
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
    return (prev.is_bullish
            and not curr.is_bullish
            and nxt.is_bullish
            and prev.length > 0
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
    return (not prev.is_bullish
            and curr.open < prev.close
            and abs(curr.close - prev.close) <= prev.length * close_tolerance
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
    return (prev.is_bullish
            and curr.open > prev.close
            and abs(curr.close - prev.close) <= prev.length * close_tolerance
            and is_thin_enough(curr, max_body_ratio))