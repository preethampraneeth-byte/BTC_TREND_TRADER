"""
BTC Trend Trader Professional v4
Application Runtime
"""

from __future__ import annotations

from runtime.backtest_runtime import BacktestRuntime
from services.live_trading_service import LiveTradingService
from services.startup_validator import StartupValidator


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

        self.startup_validator = StartupValidator()

    # -------------------------------------------------

    def run(
        self,
        mode: str = "backtest",
    ) -> None:
        """
        Run the requested application mode.

        This method dispatches execution to the appropriate runtime.
        Trading logic is intentionally delegated to the runtime classes.
        """

        mode = mode.lower()

        print(f"ApplicationRuntime: starting '{mode}' mode.")

        try:

            self.startup_validator.validate()

            if mode == "backtest":

                self.backtest.run()
                return

            if mode == "paper":

                self.live.start()
                return

            raise ValueError(
                f"Unknown application mode: {mode}"
            )

        finally:

            print(f"ApplicationRuntime: '{mode}' mode finished.")