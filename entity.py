

class CandleStick:
    """
    Represents a single candlestick extracted from a pandas DataFrame.
    """

    def __init__(self, df, index: int):
        """
        Initialize by extracting OHLC values from the DataFrame at the given index.

        :param df: pandas DataFrame with columns 'Open', 'High', 'Low', 'Close'
        :param index: integer row index
        """
        row = df.iloc[index]
        self.open = float(row['Open'])
        self.high = float(row['High'])
        self.low = float(row['Low'])
        self.close = float(row['Close'])

    @property
    def top_wick(self) -> float:
        return self.high - max(self.open, self.close)

    @property
    def bottom_wick(self) -> float:
        return min(self.open, self.close) - self.low

    @property
    def body_length(self) -> float:
        return abs(self.open - self.close)

    @property
    def body_average(self) -> float:
        return (self.open + self.close) / 2

    @property
    def length(self) -> float:
        return self.high - self.low

    @property
    def is_bullish(self) -> bool:
        return self.close >= self.open