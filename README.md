# CandleKit

A lightweight, pandas-friendly Python library for detecting candlestick patterns in financial time-series data.

## ✨ Features
- **20+ Classic Patterns**: Detect Hammer, Engulfing, Morning Star, and more
- **Pandas Integration**: Works directly with pandas DataFrames (OHLC format)
- **Clear Classification**: Bullish/bearish/neutral signal identification
- **Academic Foundation**: Based on Nison's "Japanese Candlestick Charting Techniques"
- **Production Ready**: Comprehensive testing and type hints
- **Easy Extension**: Simple API for adding custom patterns

## 📊 Supported Patterns

### Single-Candle Patterns
- **Doji** - Indecision (neutral)
- **Hammer** - Bullish reversal after downtrend
- **Shooting Star** - Bearish reversal after uptrend
- **Bullish/Bearish Marubozu** - Strong conviction with minimal shadows
- **Bullish/Bearish Belt Hold** - Strong opening at extreme

### Two-Candle Patterns
- **Bullish/Bearish Engulfing** - Reversal patterns
- **Piercing Line / Dark Cloud Cover** - Counter-trend reversals
- **Harami Cross** - Reversal with doji
- **Kicking** - Reversal with marubozu gap

### Three-Candle Patterns
- **Morning/Evening Star** - Classic reversal patterns
- **Morning/Evening Doji Star** - Reversal with doji confirmation
- **Three White Soldiers** - Strong bullish continuation
- **Three Black Crows** - Strong bearish continuation
- **Three Inside/Outside Up** - Bullish reversal variations

### Five-Candle Patterns
- **Rising/Falling Three Methods** - Continuation patterns
- **Mat Hold** - Bullish continuation with pullback

## 📦 Installation

```bash
pip install candlekit
```

## 🚀 Quick Start

```python
import pandas as pd
from candlekit import scan_symbol_df, CandlePatterns

# Your OHLC data (lowercase column names required)
data = {
    'open':  [100, 102, 101, 103, 105],
    'high':  [103, 104, 102, 106, 107],
    'low':   [99,  101, 100, 102, 104],
    'close': [102, 101, 102, 105, 106]
}
df = pd.DataFrame(data)

# Scan for all patterns
results_df = scan_symbol_df(df)
print(results_df)
```

**Output:**
```
   index        pattern_name signal_type  candles
0      1              Hammer     bullish        1
1      3   Bullish Engulfing     bullish        2
```

## 📚 Basic Usage

### Detect Specific Pattern
```python
from candlekit import detect_pattern_at_index

# Check if index 1 is a Hammer
is_hammer = detect_pattern_at_index(CandlePatterns.Hammer, df, index=1)
print(f"Hammer detected: {is_hammer}")  # True
```

### Get Results as List
```python
from candlekit import scan_symbol

results_list = scan_symbol(df)
# Returns: [(1, 'Hammer', 'bullish'), (3, 'BullishEngulfing', 'bullish')]
```

### Scan Specific Patterns Only
```python
# Scan only for reversal patterns
reversal_patterns = [
    CandlePatterns.Hammer,
    CandlePatterns.ShootingStar,
    CandlePatterns.BullishEngulfing,
    CandlePatterns.MorningStar
]

results = scan_symbol_df(df, patterns=reversal_patterns)
```

## 🔧 Working with Real Data

### Using yfinance (Optional)
```python
import yfinance as yf
from candlekit import scan_symbol_df

# Download data
ticker = yf.Ticker("AAPL")
df = ticker.history(period="1mo", interval="1d")

# Ensure correct column names
df.columns = [col.lower() for col in df.columns]

# Scan for patterns
patterns = scan_symbol_df(df)

# Filter recent bullish patterns
recent_bullish = patterns[
    (patterns['signal_type'] == 'bullish') & 
    (patterns['index'] > len(df) - 5)
]
```

### Using CSV Data
```python
import pandas as pd
from candlekit import scan_symbol_df

# Load from CSV (ensure column names match)
df = pd.read_csv('your_data.csv')
df.columns = ['open', 'high', 'low', 'close', 'volume']  # Rename if needed

# Scan for patterns
results = scan_symbol_df(df)
```

## ⚙️ Advanced Configuration

### Custom Pattern Parameters
```python
# Adjust sensitivity for Doji detection
detect_pattern_at_index(
    CandlePatterns.Doji, 
    df, 
    index=0, 
    max_body_ratio=0.15  # Default: 0.1
)

# Custom Hammer parameters
detect_pattern_at_index(
    CandlePatterns.Hammer,
    df,
    index=1,
    max_body_ratio=0.3,           # Default: 0.25
    min_lower_wick_to_body=1.5,   # Default: 2.0
    max_upper_wick_ratio=0.4      # Default: 0.33
)
```

### Pattern-Specific Parameters
Each pattern has sensible defaults, but you can adjust:
- `max_body_ratio`: Maximum body-to-total-length ratio (for thin candles)
- `min_body_ratio`: Minimum body-to-total-length ratio (for thick candles)
- `min_lower_wick_to_body`: For Hammer pattern
- `min_upper_wick_to_body`: For Shooting Star pattern

## 🧠 Understanding CandleStick Objects

The library uses `CandleStick` objects internally. You can access their properties:

```python
from candlekit.src.candlekit.entity import CandleStick

candle = CandleStick(df, index=0)
print(f"Body length: {candle.body_length}")
print(f"Top wick: {candle.top_wick}")
print(f"Bottom wick: {candle.bottom_wick}")
print(f"Body ratio: {candle.body_ratio:.2%}")
print(f"Is bullish: {candle.is_bullish}")
```

## 📊 Complete Pattern List

### Access All Patterns
```python
from candlekit import CandlePatterns

# List all available patterns
for pattern in CandlePatterns:
    print(f"{pattern.pattern_name}: {pattern.signal_type} ({pattern.candles} candle(s))")
```

### Pattern Categories
```python
# Single-candle patterns
single_candle = [p for p in CandlePatterns if p.candles == 1]

# Multi-candle patterns
multi_candle = [p for p in CandlePatterns if p.candles > 1]

# Bullish patterns
bullish = [p for p in CandlePatterns if p.signal_type == 'bullish']

# Bearish patterns
bearish = [p for p in CandlePatterns if p.signal_type == 'bearish']
```

## 🧪 Testing & Quality

### Run Tests
```bash
# Install test dependencies
pip install pytest

# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_patterns.py -v

# Run with coverage
python -m pytest --cov=candlekit tests/
```

### Example Test
```python
import pytest
import pandas as pd
from candlekit import detect_pattern_at_index, CandlePatterns

def test_hammer_detection():
    """Test Hammer pattern detection"""
    df = pd.DataFrame({
        'open': [100],
        'high': [105],
        'low': [95],
        'close': [99]
    })
    
    # This is NOT a hammer (body too large relative to wick)
    result = detect_pattern_at_index(CandlePatterns.Hammer, df, index=0)
    assert result == False
    
    # This IS a hammer
    df = pd.DataFrame({
        'open': [95],
        'high': [98],
        'low': [80],
        'close': [96]
    })
    result = detect_pattern_at_index(CandlePatterns.Hammer, df, index=0)
    assert result == True
```

## 🛠️ Development

### Setup Development Environment
```bash
# Clone and install
git clone https://github.com/zhirodadkhah/candlekit.git
cd candlekit
pip install -e ".[dev]"

# Run code quality tools
flake8 src/candlekit      # Linting
black src/candlekit       # Formatting
mypy src/candlekit        # Type checking
```

### Adding New Patterns
1. Add detection function in `patterns.py`
2. Add to `CandlePatterns` enum in `utils.py`
3. Write comprehensive tests

Example:
```python
# In patterns.py
def is_tweezers_top(candle1: CandleStick, candle2: CandleStick) -> bool:
    """Detect Tweezer Top pattern."""
    return (
        candle1.high == candle2.high and
        candle1.is_bullish and
        not candle2.is_bullish
    )

# In utils.py
CandlePatterns.TweezerTop = (2, is_tweezers_top, "bearish", "Tweezer Top")
```

## 📖 Pattern References & Methodology

All patterns are implemented according to **Steve Nison's "Japanese Candlestick Charting Techniques, 2nd Edition"**. Each pattern function includes page references to the textbook.

### Key Concepts
- **Body Ratio**: `body_length / total_length` - measures conviction
- **Window Gap**: Price gap between candles with no overlap
- **Engulfment**: Current candle's body completely contains previous
- **Containment**: Candle's body is within another's range

### Academic Sources
- Nison, S. (2001). *Japanese Candlestick Charting Techniques*
- Bulkowski, T. N. (2005). *Encyclopedia of Candlestick Charts*
- Morris, G. L. (1995). *Candlestick Charting Explained*

## 🤝 Contributing

We welcome contributions! Please:

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-pattern`
3. **Add tests** for new functionality
4. **Ensure tests pass**: `pytest`
5. **Update documentation** as needed
6. **Submit a Pull Request**

### Contribution Ideas
- Add more candlestick patterns
- Improve performance for large datasets
- Add visualization helpers
- Create Jupyter notebook examples
- Add pattern combination analysis


## 🙏 Acknowledgments

- **Steve Nison** for bringing candlestick analysis to markets
- The **pandas** and **numpy** communities
- All **contributors** and **users** of this library
- Financial analysts and quants who provided feedback

## ⚠️ Disclaimer

**IMPORTANT**: This library is for **educational and research purposes only**.

- Trading involves substantial risk of loss
- Past performance is not indicative of future results
- Always conduct your own research and consult financial advisors
- The authors are not responsible for any trading losses

Use this tool as part of a comprehensive trading strategy, not as standalone advice.

---

**Happy analyzing!** 📈

*Found a bug or have a feature request? Please open an issue on GitHub!*
```
