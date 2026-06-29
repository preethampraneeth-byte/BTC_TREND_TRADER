import sys
from pathlib import Path

# Add the project root to Python's search path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import config

print("===== Configuration Test =====")
print(f"Symbol: {config.SYMBOL}")
print(f"Timeframe: {config.TIMEFRAME}")
print(f"Risk: {config.RISK_PER_TRADE}")
print(f"Fast EMA: {config.EMA_FAST}")
print(f"Slow EMA: {config.EMA_SLOW}")