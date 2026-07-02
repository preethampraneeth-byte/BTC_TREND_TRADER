"""
BTC Trend Trader Professional v4
Market Data Service
"""

from __future__ import annotations

import config

from core.market_data import MarketData
from core.mt5_connector import MT5Connector


class MarketDataService:
    """
    Loads historical market data from either
    CSV or MetaTrader 5.
    """

    def __init__(self) -> None:

        self.connector: MT5Connector | None = None

    # -------------------------------------------------

    def load(self):

        market = MarketData()

        if config.USE_CSV_DATA:

            print("Loading historical data from CSV...")

            return market.load_from_csv(
                config.CSV_DATA_FILE
            )

        self.connector = MT5Connector()

        if not self.connector.connect():
            raise RuntimeError("Failed to connect to MT5.")

        if not self.connector.symbol_info(config.SYMBOL):
            raise RuntimeError(
                f"Unable to access symbol '{config.SYMBOL}'."
            )

        print("Downloading historical data from MT5...")

        return market.get_candles(
            symbol=config.SYMBOL,
            timeframe=config.TIMEFRAME,
            bars=500,
        )

    # -------------------------------------------------

    def shutdown(self):

        if self.connector is not None:
            self.connector.disconnect()