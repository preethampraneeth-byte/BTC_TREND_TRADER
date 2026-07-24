"""
BTC Trend Trader Professional v4
Backtest Service
"""

from __future__ import annotations

from backtesting.backtester import Backtester
from services.configuration_manager import ConfigurationManager


class BacktestService:
    """
    Service responsible for executing the backtesting
    workflow.

    Encapsulates the Backtester while preserving the
    existing runtime behaviour.
    """

    def __init__(self) -> None:

        self.config = ConfigurationManager()

        self.backtester = Backtester(
            starting_balance=self.config.get("INITIAL_BALANCE")
        )

    # -------------------------------------------------

    def run(self, candles):

        summary = self.backtester.summarize(candles)

        simulation = self.backtester.simulate(
            candles,
            lot_size=1.0,
        )

        return {
            "summary": summary,
            "statistics": simulation["statistics"],
            "trades": simulation["trades"],
            "starting_balance": self.config.get("INITIAL_BALANCE"),
        }