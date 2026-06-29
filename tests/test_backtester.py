import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from backtesting.backtester import Backtester

df = pd.DataFrame([
    {
        "Time": "2025-01-01 00:00",
        "Open": 100,
        "High": 101,
        "Low": 99,
        "Close": 100,
        "Signal": "BUY",
        "StopLoss": 95,
        "TakeProfit": 110,
    },
    {
        "Time": "2025-01-01 01:00",
        "Open": 100,
        "High": 111,
        "Low": 99,
        "Close": 110,
        "Signal": "HOLD",
        "StopLoss": 95,
        "TakeProfit": 110,
    },
])

bt = Backtester()

print(bt.summarize(df))

result = bt.simulate(df)

print(result["statistics"])
print(result["trades"])