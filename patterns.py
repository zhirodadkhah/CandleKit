from entity import CandleStick

has_thick_body = lambda candle, min_body_ratio: candle.body_ratio >= min_body_ratio

has_thin_body = lambda candle, max_body_ratio: candle.body_ratio <= max_body_ratio


def is_doji(candle: CandleStick, max_body_ratio: 0.05) -> bool:
    """
    Candlestick's body is less than 5% of candle.
    :param candle: CandleStick
    :param max_body_ratio: maximum body/candle ratio. < 1
    :return:
    """
    if candle.body_length == 0:
        return False

    return True if candle.body_ratio <= max_body_ratio else False


def is_dragonfly(candle: CandleStick,
                 max_body_ratio: 0.05,
                 top_wick_ratio=0.1,
                 bottom_wick_ratio=0.6) -> bool:
    """
    :param candle:
    :param max_body_ratio:
    :param top_wick_ratio: top wick max ration to candle length
    :param bottom_wick_ratio: bottom wick min ration to candle length
    :return:
    """
    return (is_doji(candle, max_body_ratio)
            and candle.top_wick <= candle.length * top_wick_ratio
            and candle.bottom_wick >= candle.length * bottom_wick_ratio)


def is_gravestone(
    candle: CandleStick,
    max_body_ratio: float = 0.05,
    top_wick_ratio: float = 0.6,
    bottom_wick_ratio: float = 0.1,
) -> bool:
    """
    :param candle:
    :param max_body_ratio:
    :param top_wick_ratio: top wick min ratio to candle length
    :param bottom_wick_ratio: bottom wick max ratio to candle length
    :return:
    """
    return (is_doji(candle, max_body_ratio)
            and candle.top_wick >= candle.length * top_wick_ratio
            and candle.bottom_wick <= candle.length * bottom_wick_ratio)


def is_long_legged(candle: CandleStick,
                   max_body_ratio: float = 0.05,
                   min_wick_ratio: float = 0.4) -> bool:
    """
    :param candle:
    :param max_body_ratio:
    :param min_wick_ratio: minimum ratio for both top and bottom wicks relative to candle length
    :return:
    """
    return (is_doji(candle, max_body_ratio)
            and candle.top_wick >= candle.length * min_wick_ratio
            and candle.bottom_wick >= candle.length * min_wick_ratio)


def is_hammer(
    candle: CandleStick,
    max_body_ratio: float = 0.3,
    top_wick_ratio: float = 0.1,
    bottom_wick_ratio: float = 0.6,
) -> bool:
    """
    :param candle:
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick max ratio to candle length
    :param bottom_wick_ratio: bottom wick min ratio to candle length
    :return:
    """
    return (candle.is_bullish and candle.body_ratio <= max_body_ratio
            and candle.top_wick <= candle.length * top_wick_ratio
            and candle.bottom_wick >= candle.length * bottom_wick_ratio)


def is_hanging_man(
    candle: CandleStick,
    max_body_ratio: float = 0.3,
    top_wick_ratio: float = 0.1,
    bottom_wick_ratio: float = 0.6,
) -> bool:
    """
    :param candle:
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick max ratio to candle length
    :param bottom_wick_ratio: bottom wick min ratio to candle length
    :return:
    """
    return (not candle.is_bullish and candle.body_ratio <= max_body_ratio
            and candle.top_wick <= candle.length * top_wick_ratio
            and candle.bottom_wick >= candle.length * bottom_wick_ratio)


def is_inverted_hammer(
    candle: CandleStick,
    max_body_ratio: float = 0.3,
    top_wick_ratio: float = 0.6,
    bottom_wick_ratio: float = 0.1,
) -> bool:
    """
    :param candle:
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick min ratio to candle length
    :param bottom_wick_ratio: bottom wick max ratio to candle length
    :return:
    """
    return (candle.is_bullish and candle.body_ratio <= max_body_ratio
            and candle.top_wick >= candle.length * top_wick_ratio
            and candle.bottom_wick <= candle.length * bottom_wick_ratio)


def is_shooting_star(
    candle: CandleStick,
    max_body_ratio: float = 0.3,
    top_wick_ratio: float = 0.6,
    bottom_wick_ratio: float = 0.1,
) -> bool:
    """
    :param candle:
    :param max_body_ratio: maximum body/candle ratio
    :param top_wick_ratio: top wick min ratio to candle length
    :param bottom_wick_ratio: bottom wick max ratio to candle length
    :return:
    """
    return (not candle.is_bullish and candle.body_ratio <= max_body_ratio
            and candle.top_wick >= candle.length * top_wick_ratio
            and candle.bottom_wick <= candle.length * bottom_wick_ratio)


def is_spinning_top(candle: CandleStick,
                    max_body_ratio: float = 0.5,
                    min_wick_ratio: float = 0.2) -> bool:
    """
    :param candle:
    :param max_body_ratio: maximum body/candle ratio
    :param min_wick_ratio: minimum ratio for both top and bottom wicks relative to candle length
    :return:
    """
    return (candle.body_ratio <= max_body_ratio
            and candle.top_wick >= candle.length * min_wick_ratio
            and candle.bottom_wick >= candle.length * min_wick_ratio)


def is_marubozu(candle: CandleStick, max_wick_ratio: float = 0.05) -> bool:
    """
    :param candle:
    :param max_wick_ratio: maximum allowed wick (top or bottom) as ratio of candle length
    :return:
    """
    return (candle.top_wick <= candle.length * max_wick_ratio
            and candle.bottom_wick <= candle.length * max_wick_ratio)


def is_bullish_engulfing(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles to be meaningful
    :return:
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio) and not prev.is_bullish
            and curr.is_bullish and curr.open <= prev.close
            and curr.close >= prev.open)


def is_bearish_engulfing(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles to be meaningful
    :return:
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio) and prev.is_bullish
            and not curr.is_bullish and curr.open >= prev.close
            and curr.close <= prev.open)


def is_piercing_line(candles: list,
                     min_body_ratio: float = 0.3,
                     min_penetration: float = 0.5) -> bool:
    """
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles to be meaningful
    :param min_penetration: minimum fraction of prior bearish body that current bullish candle must close into
    :return:
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio) and not prev.is_bullish
            and curr.is_bullish and curr.open <= prev.low
            and curr.close > prev.open and curr.close >= prev.open +
            (prev.close - prev.open) * min_penetration)


def is_dark_cloud_cover(candles: list,
                        min_body_ratio: float = 0.3,
                        min_penetration: float = 0.5) -> bool:
    """
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles to be meaningful
    :param min_penetration: minimum fraction of prior bullish body that current bearish candle must close into
    :return:
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio) and prev.is_bullish
            and not curr.is_bullish and curr.open >= prev.high
            and curr.close < prev.close and curr.close <= prev.close +
            (prev.open - prev.close) * min_penetration)


def is_morning_star(candles: list,
                    min_body_ratio: float = 0.3,
                    max_middle_body_ratio: float = 0.1) -> bool:
    """
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for first and third candles
    :param max_middle_body_ratio: maximum body/candle ratio for middle candle (Doji-like)
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thin_body(curr, max_middle_body_ratio)
            and has_thick_body(nxt, min_body_ratio) and not prev.is_bullish
            and nxt.is_bullish and curr.low < prev.low
            and nxt.high > prev.open)


def is_evening_star(candles: list,
                    min_body_ratio: float = 0.3,
                    max_middle_body_ratio: float = 0.1) -> bool:
    """
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for first and third candles
    :param max_middle_body_ratio: maximum body/candle ratio for middle candle (Doji-like)
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thin_body(curr, max_middle_body_ratio)
            and has_thick_body(nxt, min_body_ratio) and prev.is_bullish
            and not nxt.is_bullish and curr.high > prev.high
            and nxt.low < prev.close)


def is_three_white_soldiers(candles: list,
                            min_body_ratio: float = 0.4) -> bool:
    """
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all three candles
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio)
            and has_thick_body(nxt, min_body_ratio) and prev.is_bullish
            and curr.is_bullish and nxt.is_bullish and curr.open > prev.open
            and curr.open < prev.close and nxt.open > curr.open
            and nxt.open < curr.close and curr.close > prev.close
            and nxt.close > curr.close)


def is_three_black_crows(candles: list, min_body_ratio: float = 0.4) -> bool:
    """
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all three candles
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    is_strong = lambda c: c.body_ratio >= min_body_ratio

    return (has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio)
            and has_thick_body(nxt, min_body_ratio) and not prev.is_bullish
            and not curr.is_bullish and not nxt.is_bullish
            and curr.open < prev.open and curr.open > prev.close
            and nxt.open < curr.open and nxt.open > curr.close
            and curr.close < prev.close and nxt.close < curr.close)


def is_morning_doji_star(candles: list,
                         min_body_ratio: float = 0.3,
                         max_doji_body_ratio: float = 0.05) -> bool:
    """
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for first and third candles
    :param max_doji_body_ratio: maximum body/candle ratio for middle Doji candle
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (is_doji(curr) and has_thick_body(prev, min_body_ratio)
            and has_thick_body(nxt, min_body_ratio) and not prev.is_bullish
            and nxt.is_bullish and curr.low < prev.low
            and nxt.high > prev.open)


def is_evening_doji_star(candles: list,
                         min_body_ratio: float = 0.3,
                         max_doji_body_ratio: float = 0.05) -> bool:
    """
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for first and third candles
    :param max_doji_body_ratio: maximum body/candle ratio for middle Doji candle
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (is_doji(curr) and has_thick_body(prev, min_body_ratio)
            and has_thick_body(nxt, min_body_ratio) and prev.is_bullish
            and not nxt.is_bullish and curr.high > prev.high
            and nxt.low < prev.close)


def is_tweezer_tops(candles: list,
                    min_body_ratio: float = 0.2,
                    price_tolerance: float = 0.01) -> bool:
    """
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles to be meaningful
    :param price_tolerance: maximum allowed difference between highs as ratio of average candle length
    :return:
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    # Use average length to normalize tolerance
    avg_length = (prev.length + curr.length) / 2
    if avg_length == 0:
        return False

    high_diff = abs(prev.high - curr.high)
    return (has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio) and prev.high >= prev.open
            and curr.high >= curr.open
            and high_diff <= avg_length * price_tolerance)


def is_tweezer_bottoms(candles: list,
                       min_body_ratio: float = 0.2,
                       price_tolerance: float = 0.01) -> bool:
    """
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for both candles to be meaningful
    :param price_tolerance: maximum allowed difference between lows as ratio of average candle length
    :return:
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    # Use average length to normalize tolerance
    avg_length = (prev.length + curr.length) / 2
    if avg_length == 0:
        return False

    low_diff = abs(prev.low - curr.low)
    return (has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio) and prev.low <= prev.close
            and curr.low <= curr.close
            and low_diff <= avg_length * price_tolerance)


def is_bearish_harami(candles: list,
                      min_body_ratio: float = 0.3,
                      max_inside_body_ratio: float = 0.5) -> bool:
    """
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for the first candle
    :param max_inside_body_ratio: maximum body/candle ratio for the second candle
    :return:
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thin_body(curr, max_inside_body_ratio) and prev.is_bullish
            and not curr.is_bullish and curr.open < prev.close
            and curr.close > prev.open)


def is_bullish_harami(candles: list,
                      min_body_ratio: float = 0.3,
                      max_inside_body_ratio: float = 0.5) -> bool:
    """
    :param candles: list of at least 2 CandleStick objects [prev, current]
    :param min_body_ratio: minimum body/candle ratio for the first candle
    :param max_inside_body_ratio: maximum body/candle ratio for the second candle
    :return:
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    return (has_thick_body(prev, min_body_ratio)
            and has_thin_body(curr, max_inside_body_ratio)
            and not prev.is_bullish and curr.is_bullish
            and curr.open > prev.close and curr.close < prev.open)


def is_bullish_belt_hold(candle: CandleStick,
                         min_body_ratio: float = 0.7,
                         max_lower_wick_ratio: float = 0.05) -> bool:
    """
    :param candle: CandleStick
    :param min_body_ratio: minimum body/candle ratio (strong bullish body)
    :param max_lower_wick_ratio: maximum lower wick as ratio of candle length
    :return:
    """
    return (candle.is_bullish and has_thick_body(candle, min_body_ratio)
            and candle.bottom_wick <= candle.length * max_lower_wick_ratio
            and candle.open == candle.low  # opens at the low
            )


def is_bearish_belt_hold(candle: CandleStick,
                         min_body_ratio: float = 0.7,
                         max_upper_wick_ratio: float = 0.05) -> bool:
    """
    :param candle: CandleStick
    :param min_body_ratio: minimum body/candle ratio (strong bearish body)
    :param max_upper_wick_ratio: maximum upper wick as ratio of candle length
    :return:
    """

    return (not candle.is_bullish and has_thick_body(candle, min_body_ratio)
            and candle.top_wick <= candle.length * max_upper_wick_ratio
            and candle.open == candle.high  # opens at the high
            )


def is_bullish_tasuki_gap(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all candles
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (curr.low > prev.high and nxt.close > prev.high
            and nxt.close < curr.low and has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio)
            and has_thick_body(nxt, min_body_ratio) and prev.is_bullish
            and curr.is_bullish and nxt.is_bullish)


def is_bearish_tasuki_gap(candles: list, min_body_ratio: float = 0.3) -> bool:
    """
    :param candles: list of at least 3 CandleStick objects [prev, curr, nxt]
    :param min_body_ratio: minimum body/candle ratio for all candles
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (curr.high < prev.low and nxt.close < prev.low
            and nxt.close > curr.high and has_thick_body(prev, min_body_ratio)
            and has_thick_body(curr, min_body_ratio)
            and has_thick_body(nxt, min_body_ratio) and not prev.is_bullish
            and not curr.is_bullish and not nxt.is_bullish)


def is_bullish_kicking(candles: list, max_wick_ratio: float = 0.05) -> bool:
    """
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_wick_ratio: tolerance for wicks in marubozu
    :return:
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]

    return (not prev.is_bullish and is_marubozu(prev, max_wick_ratio)
            and curr.is_bullish and is_marubozu(curr, max_wick_ratio)
            and curr.open > prev.open)


def is_bearish_kicking(candles: list, max_wick_ratio: float = 0.05) -> bool:
    """
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_wick_ratio: tolerance for wicks in marubozu
    :return:
    """
    if len(candles) < 2:
        return False
    prev, curr = candles[-2], candles[-1]

    return (prev.is_bullish and is_marubozu(prev, max_wick_ratio)
            and not curr.is_bullish and is_marubozu(curr, max_wick_ratio)
            and curr.open < prev.open)


def is_bullish_abandoned_baby(candles: list,
                              max_body_ratio: float = 0.05,
                              require_gap: bool = True) -> bool:
    """
    :param candles: list of at least 3 CandleStick (latest last)
    :param max_body_ratio: max body ratio for Doji
    :param require_gap: if False, skips gap validation
    :return: bool
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (not prev.is_bullish and is_doji(curr, max_body_ratio)
            and nxt.is_bullish
            and (not require_gap or
                 (curr.high < prev.low and nxt.low > curr.high)))


def is_bearish_abandoned_baby(candles: list,
                              max_body_ratio: float = 0.05,
                              require_gap: bool = True) -> bool:
    """
    :param candles: list of at least 3 CandleStick (latest last)
    :param max_body_ratio: max body ratio for Doji
    :param require_gap: if False, skips gap validation
    :return: bool
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (prev.is_bullish and is_doji(curr, max_body_ratio)
            and not nxt.is_bullish
            and (not require_gap or
                 (curr.low > prev.high and nxt.high < curr.low)))


def is_three_inside_up(candles: list, close_above_open: bool = True) -> bool:
    """
    :param candles: list of at least 3 CandleStick
    :param close_above_open: if True, requires nxt close > prev open (strict confirmation)
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (not prev.is_bullish and curr.is_bullish and prev.low <= curr.low
            and curr.high <= prev.high and nxt.is_bullish
            and (not close_above_open or nxt.close > prev.open))


def is_three_inside_down(candles: list, close_below_open: bool = True) -> bool:
    """
    :param candles: list of at least 3 CandleStick
    :param close_below_open: if True, requires nxt close < prev open (strict confirmation)
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (prev.is_bullish and not curr.is_bullish and prev.low <= curr.low
            and curr.high <= prev.high and not nxt.is_bullish
            and (not close_below_open or nxt.close < prev.open))


def is_three_outside_up(candles: list, strict_engulfing: bool = True) -> bool:
    """
    :param candles: list of at least 3 CandleStick
    :param strict_engulfing: if True, requires curr to fully engulf prev (open <= prev.close and close >= prev.open)
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    if (prev.is_bullish or not curr.is_bullish or not nxt.is_bullish
            or nxt.close <= curr.close):
        return False

    if strict_engulfing:
        if not (curr.open <= prev.close and curr.close >= prev.open):
            return False
    else:
        if not (curr.open <= prev.open and curr.close >= prev.close):
            return False

    return True


def is_three_outside_down(candles: list,
                          strict_engulfing: bool = True) -> bool:
    """
    :param candles: list of at least 3 CandleStick
    :param strict_engulfing: if True, requires curr to fully engulf prev (open >= prev.close and close <= prev.open)
    :return:
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    if (not prev.is_bullish
        or curr.is_bullish
        or nxt.is_bullish
        or nxt.close >= curr.close):
        return False

    if strict_engulfing:
        if not (curr.open >= prev.close and curr.close <= prev.open):
            return False
    else:
        if not (curr.open >= prev.open and curr.close <= prev.close):
            return False

    return True


def is_bullish_stick_sandwich(candles: list, close_tolerance: float = 0.005) -> bool:
    """
    :param candles: list of at least 3 CandleStick (latest last)
    :param close_tolerance: max allowed ratio difference between prev and nxt closes (relative to prev length)
    :return: bool
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (
        not prev.is_bullish
        and curr.is_bullish
        and not nxt.is_bullish
        and prev.length > 0
        and abs(nxt.close - prev.close) <= prev.length * close_tolerance
    )


def is_bearish_stick_sandwich(candles: list, close_tolerance: float = 0.005) -> bool:
    """
    :param candles: list of at least 3 CandleStick (latest last)
    :param close_tolerance: max allowed ratio difference between prev and nxt closes (relative to prev length)
    :return: bool
    """
    if len(candles) < 3:
        return False

    prev, curr, nxt = candles[-3], candles[-2], candles[-1]

    return (
        prev.is_bullish
        and not curr.is_bullish
        and nxt.is_bullish
        and prev.length > 0
        and abs(nxt.close - prev.close) <= prev.length * close_tolerance
    )


def is_bullish_counterattack(
    candles: list,
    max_body_ratio: float = 0.05,
    close_tolerance: float = 0.01
) -> bool:
    """
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_body_ratio: max body ratio for confirmation candle (curr)
    :param close_tolerance: max allowed ratio difference between prev and curr closes (relative to prev length)
    :return: bool
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    return (
        not prev.is_bullish
        and curr.open < prev.close
        and abs(curr.close - prev.close) <= prev.length * close_tolerance
        and has_thin_body(curr, max_body_ratio)
    )


def is_bearish_counterattack(
    candles: list,
    max_body_ratio: float = 0.05,
    close_tolerance: float = 0.01
) -> bool:
    """
    :param candles: list of at least 2 CandleStick (latest last)
    :param max_body_ratio: max body ratio for confirmation candle (curr)
    :param close_tolerance: max allowed ratio difference between prev and curr closes (relative to prev length)
    :return: bool
    """
    if len(candles) < 2:
        return False

    prev, curr = candles[-2], candles[-1]

    return (
        prev.is_bullish
        and curr.open > prev.close
        and abs(curr.close - prev.close) <= prev.length * close_tolerance
        and has_thin_body(curr <= max_body_ratio)
    )