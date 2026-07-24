"""
BTC Trend Trader Professional v4
Execution Router
"""

from __future__ import annotations

from services.configuration_manager import ConfigurationManager

from runtime.backtest_runtime import BacktestRuntime
from runtime.paper_runtime import PaperRuntime
from runtime.live_runtime import LiveRuntime


class ExecutionRouter:
    """
    Selects the runtime according to
    EXECUTION_MODE.
    """

    def __init__(self):

        self._runtime = None

        self.config = ConfigurationManager()

    # ---------------------------------------------------------

    def runtime(self):

        if self._runtime is not None:
            return self._runtime

        mode = self.config.get("EXECUTION_MODE").upper()

        if mode == "BACKTEST":

            self._runtime = BacktestRuntime()

        elif mode == "PAPER":

            self._runtime = PaperRuntime()

        elif mode == "LIVE":

            self._runtime = LiveRuntime()

        else:

            raise ValueError(
                f"Unsupported EXECUTION_MODE: {mode}"
            )

        return self._runtime

    # ---------------------------------------------------------

    def run(self):

        return self.runtime().run()