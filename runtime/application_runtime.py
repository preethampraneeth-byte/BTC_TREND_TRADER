"""
BTC Trend Trader Professional v4
Application Runtime
"""

from __future__ import annotations

from runtime.backtest_runtime import BacktestRuntime
from services.live_trading_service import LiveTradingService


class ApplicationRuntime:
    """
    Main application runtime.

    Supports:

    - Backtesting
    - Live Paper Trading
    """

    def __init__(self):

        self.backtest = BacktestRuntime()

        self.live = LiveTradingService()

    # -------------------------------------------------

    def run(
        self,
        mode: str = "backtest",
    ) -> None:

        mode = mode.lower()

        if mode == "backtest":

            self.backtest.run()

            return

        if mode == "paper":

            self.live.start()

            return

        raise ValueError(
            f"Unknown application mode: {mode}"
        )