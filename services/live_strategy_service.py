"""
BTC Trend Trader Professional v4
Live Strategy Service
"""

from __future__ import annotations

from core.indicators import Indicators
from core.strategy import Strategy


class LiveStrategyService:
    """
    Executes the existing trading strategy
    on live market candles.
    """

    def __init__(self) -> None:

        self.indicators = Indicators()

        self.strategy = Strategy()

    # -------------------------------------------------

    def generate_signals(
        self,
        candles,
        h4_candles,
    ):
        """
        Calculate indicators and generate
        trading signals.

        Parameters
        ----------
        candles:
            H1 market candles.

        h4_candles:
            H4 market candles used by the
            Strategy v5 higher-timeframe regime filter.
        """

        # Calculate H1 indicators
        candles = self.indicators.calculate(
            candles
        )

        # Generate signals using H1 + H4 data
        candles = self.strategy.generate_signals(
            candles,
            h4_candles,
        )

        return candles