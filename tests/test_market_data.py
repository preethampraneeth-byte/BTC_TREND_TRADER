import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import config
from core.mt5_connector import MT5Connector
from core.market_data import MarketData

connector = MT5Connector()

if connector.connect():
    market = MarketData()

    df = market.get_candles(
        symbol=config.SYMBOL,
        timeframe=config.TIMEFRAME,
        bars=10
    )

    print("\n===== LAST 10 CANDLES =====\n")
    print(df)

    connector.disconnect()