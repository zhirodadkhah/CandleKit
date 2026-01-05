import pytest
import pandas as pd
from candlekit import (
    detect_pattern_at_index,
    scan_symbol,
    scan_symbol_df,
    CandlePatterns
)

def make_candle_df(o, h, l, c):
    return pd.DataFrame([{"open": o, "high": h, "low": l, "close": c}])


# ============================================================================
# CORRECTED MOCK PATTERN FUNCTIONS
# ============================================================================

def mock_is_doji(candle) -> bool:
    if candle.length == 0:
        return True
    body = candle.body_length
    # Stricter Doji: only when body is very small relative to range
    return (body / candle.length) <= 0.05  # Reduced from 0.1


def mock_is_hammer(candle) -> bool:
    if candle.length == 0:
        return False
    body = candle.body_length
    bottom_wick = candle.bottom_wick
    top_wick = candle.top_wick

    if body == 0:
        return bottom_wick > 0 and top_wick <= bottom_wick * 0.33

    return (
            candle.body_ratio <= 0.3 and
            bottom_wick >= 2 * body and
            top_wick <= min(body, bottom_wick * 0.33)
    )


# Update Doji test data to still pass with stricter threshold
def test_detect_pattern_at_index_doji_positive():
    df = make_candle_df(100, 101, 99, 100.02)  # body = 0.02, length = 2, ratio = 0.01
    assert detect_pattern_at_index(CandlePatterns.Doji, df, 0) is True



def mock_is_doji(candle) -> bool:
    if candle.length == 0:
        return True
    body = candle.body_length
    return (body / candle.length) <= 0.1


def mock_is_hammer(candle) -> bool:
    if candle.length == 0:
        return False

    # Realistic hammer conditions:
    # 1. Small body (body <= 30% of total length)
    # 2. Long lower shadow (bottom wick >= 2 * body)
    # 3. Very small or no upper shadow (top wick <= 0.33 * bottom wick OR top wick <= body)
    body = candle.body_length
    bottom_wick = candle.bottom_wick
    top_wick = candle.top_wick

    if body == 0:
        return bottom_wick > 0 and top_wick <= bottom_wick * 0.33

    return (
            candle.body_ratio <= 0.3 and
            bottom_wick >= 2 * body and
            top_wick <= min(body, bottom_wick * 0.33)
    )


def mock_is_bullish_engulfing(c1, c2) -> bool:
    return (
            c1.close < c1.open and  # prior bearish
            c2.close > c2.open and  # current bullish
            c2.open < c1.close and  # current opens below prior close
            c2.close > c1.open  # current closes above prior open
    )


def mock_is_morning_star(c1, c2, c3) -> bool:
    return (
            c1.close < c1.open and  # first: bearish
            c2.body_ratio <= 0.1 and  # second: small body/doji
            c3.close > c3.open and  # third: bullish
            c3.close > c1.open  # third closes into first body
    )


def mock_is_rising_three(candles) -> bool:
    if len(candles) != 5:
        return False
    c1, c2, c3, c4, c5 = candles
    return (
            c1.close > c1.open and
            c5.close > c5.open and
            all(c.close < c.open for c in [c2, c3, c4]) and  # middle three bearish
            c5.close > c1.close
    )


# Patch the enum with our mocks
CandlePatterns.Doji.func = staticmethod(mock_is_doji)
CandlePatterns.Hammer.func = staticmethod(mock_is_hammer)
CandlePatterns.BullishEngulfing.func = staticmethod(mock_is_bullish_engulfing)
CandlePatterns.MorningStar.func = staticmethod(mock_is_morning_star)
CandlePatterns.RisingThreeMethods.func = staticmethod(mock_is_rising_three)


# ============================================================================
# POSITIVE TESTS
# ============================================================================

def test_detect_pattern_at_index_doji_positive():
    df = make_candle_df(100, 101, 99, 100.05)
    assert detect_pattern_at_index(CandlePatterns.Doji, df, 0) is True


def test_detect_pattern_at_index_hammer_positive():
    # Create a CLEAR hammer: very small top wick
    df = make_candle_df(100, 100.2, 90, 99)  # top wick = 0.2, bottom wick = 9, body = 1
    assert detect_pattern_at_index(CandlePatterns.Hammer, df, 0) is True


def test_detect_pattern_at_index_engulfing_positive():
    df = pd.concat([
        make_candle_df(100, 102, 98, 99),  # bearish
        make_candle_df(98.5, 105, 97, 104)  # bullish engulfing
    ], ignore_index=True)
    assert detect_pattern_at_index(CandlePatterns.BullishEngulfing, df, 1) is True





def test_scan_symbol_df_returns_correct_dataframe():
    df = make_candle_df(100, 100.2, 90, 99)
    result_df = scan_symbol_df(df, [CandlePatterns.Hammer])
    assert len(result_df) == 1
    assert result_df.iloc[0]["index"] == 0
    assert result_df.iloc[0]["pattern_name"] == "Hammer"
    assert result_df.iloc[0]["signal_type"] == "bullish"
    assert result_df.iloc[0]["candles"] == 1


# ============================================================================
# NEGATIVE TESTS
# ============================================================================

def test_detect_hammer_negative_body_too_large():
    df = make_candle_df(100, 110, 90, 108)  # large body
    assert detect_pattern_at_index(CandlePatterns.Hammer, df, 0) is False


def test_detect_hammer_negative_no_lower_wick():
    df = make_candle_df(100, 105, 100, 102)  # no lower wick (low = min(open,close))
    assert detect_pattern_at_index(CandlePatterns.Hammer, df, 0) is False


def test_detect_hammer_negative_large_top_wick():
    df = make_candle_df(100, 105, 90, 99)  # top wick = 5, too large
    assert detect_pattern_at_index(CandlePatterns.Hammer, df, 0) is False


def test_detect_engulfing_negative_not_engulfing():
    df = pd.concat([
        make_candle_df(100, 102, 98, 99),
        make_candle_df(99.5, 101, 99, 100.5)
    ], ignore_index=True)
    assert detect_pattern_at_index(CandlePatterns.BullishEngulfing, df, 1) is False


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

def test_detect_pattern_insufficient_data():
    df = make_candle_df(100, 101, 99, 100)
    assert detect_pattern_at_index(CandlePatterns.BullishEngulfing, df, 0) is False


def test_detect_pattern_index_out_of_bounds():
    df = make_candle_df(100, 101, 99, 100)
    with pytest.raises(IndexError):
        detect_pattern_at_index(CandlePatterns.Doji, df, 1)


def test_scan_symbol_empty_dataframe():
    df = pd.DataFrame(columns=["open", "high", "low", "close"])
    results = scan_symbol(df)
    assert results == []


def test_scan_symbol_df_empty_returns_empty_df():
    df = pd.DataFrame(columns=["open", "high", "low", "close"])
    result_df = scan_symbol_df(df)
    assert result_df.empty
    assert list(result_df.columns) == ["index", "pattern_name", "signal_type", "candles"]


def test_scan_symbol_finds_patterns():
    df = pd.concat([
        make_candle_df(100, 101, 99, 100),  # Perfect Doji: open == close
        make_candle_df(95, 96, 80, 94),  # Hammer: body=1, length=16, ratio=0.0625
    ], ignore_index=True)

    # Now:
    # Row 0: body=0 → Doji = True (always)
    # Row 1: body_ratio = 1/16 = 0.0625
    #   → If real is_doji uses <= 0.1 → this is STILL a Doji!

    # So make hammer body larger!
    df = pd.concat([
        make_candle_df(100, 101, 99, 100),  # Perfect Doji
        make_candle_df(90, 92, 80, 89),  # Body = 1, Length = 12, ratio = 0.083 → still risky
    ], ignore_index=True)