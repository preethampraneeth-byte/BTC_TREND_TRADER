"""
BTC Trend Trader Professional v4
Strategy Service
"""

from __future__ import annotations

from core.indicators import Indicators
from core.strategy import Strategy


class StrategyService:
    """
    Prepares market data for trading by calculating
    technical indicators and generating strategy signals.
    """

    def __init__(self) -> None:

        self.indicators = Indicators()

        self.strategy = Strategy()

    # -------------------------------------------------

    def prepare(self, candles):

        candles = self.indicators.calculate(
            candles
        )

        candles = self.strategy.generate_signals(
            candles
        )

        return candles