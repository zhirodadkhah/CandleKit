# CandleKit

A lightweight, pandas-friendly Python library for detecting candlestick patterns in financial time-series data.

## ✨ Features
- Detect 20+ classic candlestick patterns (Hammer, Engulfing, Morning Star, etc.)
- Works directly with pandas DataFrames (OHLC format)
- Clear bullish/bearish/neutral signal classification
- Easy to extend with custom patterns

## 📊 Supported Patterns

### Single-Candle Patterns
- Doji
- Hammer
- Shooting Star
- Bullish Marubozu
- Bearish Marubozu
- Bullish Belt Hold
- Bearish Belt Hold

### Two-Candle Patterns
- Bullish Engulfing
- Bearish Engulfing
- Piercing Line
- Dark Cloud Cover
- Bullish Harami Cross
- Bearish Harami Cross
- Bullish Kicking
- Bearish Kicking

### Three-Candle Patterns
- Morning Star
- Evening Star
- Morning Doji Star
- Evening Doji Star
- Three White Soldiers
- Three Black Crows
- Three Inside Up
- Three Outside Up

### Five-Candle Patterns
- Rising Three Methods
- Falling Three Methods
- Mat Hold

## 📦 Installation
```bash
pip install candlekit