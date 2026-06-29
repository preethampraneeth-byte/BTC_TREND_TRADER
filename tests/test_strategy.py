import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import config

from core.mt5_connector import MT5Connector
from core.market_data import MarketData
from core.indicators import Indicators
from core.strategy import Strategy


def main():

    connector = MT5Connector()

    if connector.connect():

        market = MarketData()

        df = market.get_candles(
            symbol=config.SYMBOL,
            timeframe=config.TIMEFRAME,
            bars=300,
        )

        indicators = Indicators()

        df = indicators.calculate(df)

        strategy = Strategy()

        df = strategy.generate_signals(df)

        print("\n===== LAST 10 SIGNALS =====\n")

        print(
            df[
                [
                    "Time",
                    "Close",
                    f"EMA_{config.EMA_FAST}",
                    f"EMA_{config.EMA_SLOW}",
                    "RSI",
                    "ADX",
                    "Signal",
                    "Reason",
                ]
            ].tail(10)
        )

        connector.disconnect()


if __name__ == "__main__":
    main()