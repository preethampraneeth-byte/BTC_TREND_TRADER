"""
BTC Trend Trader Professional v4
Live Market Feed
"""

from __future__ import annotations

import config

from core.mt5_connector import MT5Connector


class LiveMarketFeed:
    """
    Provides live market data
    for paper trading.

    Retrieves the latest candles
    directly from MT5.
    """

    def __init__(self):

        self.connector = MT5Connector()

        if not self.connector.connect():
            raise RuntimeError(
                "Unable to connect to MT5."
            )

        if not self.connector.symbol_info(
            config.SYMBOL
        ):
            raise RuntimeError(
                f"Symbol '{config.SYMBOL}' unavailable."
            )

    # -------------------------------------------------

    def latest(
        self,
        bars: int = 500,
    ):

        return self.connector.get_latest_candles(

            symbol=config.SYMBOL,

            timeframe=config.TIMEFRAME,

            bars=bars,

        )

    # -------------------------------------------------
    def latest_h4(self, bars: int = 500):
        """
        Retrieve the latest H4 candles from MT5.

        Used by Strategy v5 for the higher-timeframe
        trend regime filter.
        """

        return self.connector.get_latest_candles(
            symbol=config.SYMBOL,
            timeframe="H4",
            bars=bars,
        )

    # -------------------------------------------------

    def shutdown(self):

        self.connector.disconnect()