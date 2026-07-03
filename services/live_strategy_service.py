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
    ):
        """
        Calculate indicators and generate
        trading signals.
        """

        candles = self.indicators.calculate(
            candles
        )

        candles = self.strategy.generate_signals(
            candles
        )

        return candles