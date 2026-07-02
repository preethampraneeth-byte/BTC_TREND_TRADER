"""
BTC Trend Trader Professional v4
Backtest Runtime
"""

from __future__ import annotations


class BacktestRuntime:
    """
    Runtime responsible for executing
    the existing backtesting workflow.

    At this stage it is a placeholder that
    preserves backward compatibility.
    """

    def __init__(self) -> None:

        self.name = "BACKTEST"

    def run(self) -> None:
        """
        Execute the backtest runtime.

        The existing implementation in
        main.py remains the authoritative
        execution path until runtime
        integration is completed.
        """

        print(
            "BacktestRuntime selected."
        )