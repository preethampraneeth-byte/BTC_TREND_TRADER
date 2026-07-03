"""
BTC Trend Trader Professional v4
Live Trading Service
"""

from __future__ import annotations

from live.live_runtime import LiveRuntime


class LiveTradingService:
    """
    Service responsible for managing
    the Live Paper Trading runtime.
    """

    def __init__(self) -> None:

        self.runtime = LiveRuntime()

    # -------------------------------------------------

    def start(self) -> None:
        """
        Start live paper trading.
        """

        self.runtime.start()

    # -------------------------------------------------

    def stop(self) -> None:
        """
        Stop live paper trading.
        """

        self.runtime.stop()

        self.runtime.shutdown()