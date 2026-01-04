import pandas as pd

class CandleStick:
    """
    Represents a single OHLC candlekit for technical pattern analysis.

    Designed to work seamlessly with Nison-style candlekit pattern detection.
    All properties are lightweight and calculated on-the-fly.
    """

    def __init__(self, df: pd.DataFrame, index: int) -> None:
        """
        Initialize a candlekit from a pandas DataFrame at the given row index.

        :param df: DataFrame with columns ['Open', 'High', 'Low', 'Close']
        :param index: Integer row index (0-based)
        :raises IndexError: If index is out of bounds
        :raises KeyError: If required OHLC columns are missing
        """
        row = df.iloc[index]
        self.open = float(row['open'])
        self.high = float(row['high'])
        self.low = float(row['low'])
        self.close = float(row['close'])

    @property
    def top_wick(self) -> float:
        """Length of the upper shadow (wick)."""
        return self.high - max(self.open, self.close)

    @property
    def bottom_wick(self) -> float:
        """Length of the lower shadow (wick)."""
        return min(self.open, self.close) - self.low

    @property
    def body_length(self) -> float:
        """Absolute size of the real body."""
        return abs(self.close - self.open)

    @property
    def body_average(self) -> float:
        """Midpoint of the real body."""
        return (self.open + self.close) / 2.0

    @property
    def length(self) -> float:
        """Total range of the candle (high - low)."""
        return self.high - self.low

    @property
    def is_bullish(self) -> bool:
        """True if close > open (bullish candle)."""
        return self.close > self.open

    @property
    def body_ratio(self) -> float:
        """
        Ratio of body length to total candle length.

        Returns 0.0 for flat candles (high == low).
        Used extensively in pattern logic (e.g., doji, marubozu).
        """
        if self.length == 0.0:
            return 0.0
        return self.body_length / self.length

    @property
    def body_low(self) -> float:
        """Lower edge of the real body."""
        return min(self.open, self.close)

    @property
    def body_high(self) -> float:
        """Upper edge of the real body."""
        return max(self.open, self.close)