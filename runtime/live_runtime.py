"""
BTC Trend Trader Professional v4
Live Runtime
"""

from __future__ import annotations


class LiveRuntime:
    """
    Runtime responsible for executing
    the live MT5 trading engine.

    The execution pipeline will be
    connected in the next sprint.
    """

    def __init__(self) -> None:

        self.name = "LIVE"

    def run(self) -> None:
        """
        Execute the Live Trading runtime.

        Full MT5 execution will be added
        during the Live Integration sprint.
        """

        print(
            "LiveRuntime selected."
        )