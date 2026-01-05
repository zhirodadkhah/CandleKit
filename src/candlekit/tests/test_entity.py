import pytest
import pandas as pd
import math
from candlekit.src.candlekit.entity import CandleStick  # 👈 Replace with your actual module name


def make_candle(o, h, l, c):
    df = pd.DataFrame([{"open": o, "high": h, "low": l, "close": c}])
    return CandleStick(df, 0)


# ================
# POSITIVE TESTS
# ================

def test_positive_normal_bullish_candle():
    candle = make_candle(100, 110, 95, 108)
    assert candle.open == 100.0
    assert candle.high == 110.0
    assert candle.low == 95.0
    assert candle.close == 108.0
    assert candle.is_bullish is True
    assert candle.body_length == 8.0
    assert candle.top_wick == 2.0
    assert candle.bottom_wick == 5.0
    assert candle.length == 15.0
    assert abs(candle.body_ratio - (8.0 / 15.0)) < 1e-10
    assert candle.body_low == 100.0
    assert candle.body_high == 108.0
    assert candle.body_average == 104.0


def test_positive_doji():
    candle = make_candle(100, 105, 95, 100)
    assert candle.body_length == 0.0
    assert candle.body_ratio == 0.0
    assert candle.top_wick == 5.0
    assert candle.bottom_wick == 5.0


# ================
# NEGATIVE TESTS (invalid OHLC logic — but NO exception expected)
# ================

def test_negative_high_less_than_open():
    # Invalid real-world candle: high < open and high < close
    candle = make_candle(100, 95, 90, 98)
    # top_wick = high - max(open, close) = 95 - 100 = -5
    assert candle.top_wick == -5.0
    assert candle.bottom_wick == 8.0  # min(100,98) - 90 = 98 - 90


def test_negative_low_greater_than_both():
    candle = make_candle(100, 110, 105, 98)
    assert candle.bottom_wick == 98 - 105 == -7.0
    assert candle.top_wick == 10.0


# ================
# EDGE CASE TESTS
# ================

def test_edge_zero_length_candle():
    candle = make_candle(100, 100, 100, 100)
    assert candle.length == 0.0
    assert candle.body_length == 0.0
    assert candle.body_ratio == 0.0
    assert candle.top_wick == 0.0
    assert candle.bottom_wick == 0.0


def test_edge_nan_input():
    # Should not crash; just propagate NaN
    candle = make_candle(float('nan'), 100, 90, 95)
    assert math.isnan(candle.open)
    assert math.isnan(candle.body_length)
    assert math.isnan(candle.body_ratio)


def test_edge_inf_input():
    # Case: all inf → body_length = |inf - inf| = nan
    candle = make_candle(float('inf'), float('inf'), float('inf'), float('inf'))
    assert math.isinf(candle.high)
    assert math.isnan(candle.body_length)  # inf - inf = nan
    assert math.isnan(candle.body_ratio)   # nan / inf = nan

    # Case: valid inf candle (rare but possible in theory)
    candle2 = make_candle(0, float('inf'), 0, 100)
    assert math.isinf(candle2.length)
    assert candle2.body_length == 100.0
    assert candle2.body_ratio == 0.0  # 100 / inf = 0.0


def test_edge_high_less_than_low():
    candle = make_candle(50, 40, 60, 45)
    assert candle.length == -20.0
    assert candle.body_length == 5.0
    # body_ratio = 5.0 / (-20.0) = -0.25
    assert candle.body_ratio == -0.25


def test_edge_empty_dataframe():
    df = pd.DataFrame(columns=["open", "high", "low", "close"])
    with pytest.raises(IndexError):
        CandleStick(df, 0)


def test_edge_missing_column():
    df = pd.DataFrame([{"open": 1, "high": 2, "low": 0}])
    with pytest.raises(KeyError, match="close"):
        CandleStick(df, 0)


def test_edge_wrong_index():
    df = pd.DataFrame([{"open": 1, "high": 2, "low": 0, "close": 1.5}])
    with pytest.raises(IndexError):
        CandleStick(df, 1)