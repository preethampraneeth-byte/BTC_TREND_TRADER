"""
BTC Trend Trader Professional v4
Paper Runtime
"""

from __future__ import annotations

from paper_trading.paper_engine import PaperEngine


class PaperRuntime:
    """
    Runtime responsible for executing
    the Paper Trading engine.
    """

    def __init__(self) -> None:

        self.name = "PAPER"

        self.engine = PaperEngine()

    def run(self) -> None:
        """
        Start the Paper Trading runtime.

        Full market integration will be
        added in the next sprint.
        """

        self.engine.start()

        print(
            "PaperRuntime selected."
        )