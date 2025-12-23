from pprint import pprint
import pandas as pd
from candlekit import scan_symbol_df, CandlePatterns

# Example OHLC data
data = {
    'open':  [100, 102, 101, 103, 105],
    'high':  [103, 104, 102, 106, 107],
    'low':   [99,  101, 100, 102, 104],
    'close': [102, 101, 102, 105, 106]
}
df = pd.DataFrame(data)

# Scan for all patterns
results = scan_symbol_df('EXAMPLE', df) # returns a DataFrame instance
pprint(results)

results = scan_symbol(df) # returns a list
pprint(results)

# Scan for specific pattern
from candlekit import detect_pattern_at_index
is_hammer = detect_pattern_at_index(CandlePatterns.Hammer, df, index=1)
print("Hammer at index 1?", is_hammer)