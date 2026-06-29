import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import config

from core.mt5_connector import MT5Connector
from core.market_data import MarketData
from core.indicators import Indicators
from core.strategy import Strategy
from core.risk_manager import RiskManager


def main():

    connector = MT5Connector()

    if not connector.connect():
        return

    market = MarketData()

    df = market.get_candles(
        symbol=config.SYMBOL,
        timeframe=config.TIMEFRAME,
        bars=300,
    )

    df = Indicators().calculate(df)
    df = Strategy().generate_signals(df)

    latest = df.iloc[-1]

    trade = RiskManager().calculate_trade_levels(
        latest["Signal"],
        latest,
    )

    print("\n===== TRADE DETAILS =====\n")

    for key, value in trade.items():
        print(f"{key:15}: {value}")

    connector.disconnect()


if __name__ == "__main__":
    main()