"""
BTC Trend Trader Professional v4
Reporting Service
"""

from __future__ import annotations

from backtesting.performance_report import PerformanceReport


class ReportingService:
    """
    Service responsible for generating performance reports.
    """

    def __init__(self) -> None:

        self.report = PerformanceReport()

    # -------------------------------------------------

    def generate(
        self,
        trades,
        statistics,
    ):

        return self.report.generate(
            trades=trades,
            starting_balance=statistics["starting_balance"],
            ending_balance=statistics["ending_balance"],
            equity_curve=statistics["equity_curve"],
        )