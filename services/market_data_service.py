"""
BTC Trend Trader Professional v4
Market Data Service
"""

from __future__ import annotations

from services.configuration_manager import ConfigurationManager

from core.market_data import MarketData
from core.mt5_connector import MT5Connector
from core.indicators import Indicators
from core.strategy import Strategy


class MarketDataService:
    """
    Responsible for:

    - Loading market data
    - Preparing market data
      (Indicators + Strategy)
    """

    def __init__(self) -> None:

        self.connector: MT5Connector | None = None

        self.config = ConfigurationManager()

    # -------------------------------------------------

    def load(self):

        market = MarketData()

        if self.config.get("USE_CSV_DATA"):

            print("Loading historical data from CSV...")

            return market.load_from_csv(
                self.config.get("CSV_DATA_FILE")
            )

        self.connector = MT5Connector()

        if not self.connector.connect():
            raise RuntimeError("Failed to connect to MT5.")

        if not self.connector.symbol_info(
            self.config.get("SYMBOL")
        ):
            raise RuntimeError(
                f"Unable to access symbol '{self.config.get('SYMBOL')}'."
            )

        print("Downloading historical data from MT5...")

        return market.get_candles(
            symbol=self.config.get("SYMBOL"),
            timeframe=self.config.get("TIMEFRAME"),
            bars=500,
        )

    # -------------------------------------------------

    def prepare(self, candles):

        indicators = Indicators()

        candles = indicators.calculate(candles)

        strategy = Strategy()

        candles = strategy.generate_signals(candles)

        return candles

    # -------------------------------------------------

    def shutdown(self) -> None:

        if self.connector is not None:

            self.connector.disconnect()