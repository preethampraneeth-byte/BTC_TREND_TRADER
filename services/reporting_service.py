"""
BTC Trend Trader Professional v4
Reporting Service
"""

from __future__ import annotations

from backtesting.performance_report import PerformanceReport


class ReportingService:
    """
    Generates performance reports from
    completed backtests.
    """

    def generate(
        self,
        trades,
        statistics,
    ):

        return PerformanceReport().generate(
            trades=trades,
            starting_balance=statistics["starting_balance"],
            ending_balance=statistics["ending_balance"],
            equity_curve=statistics["equity_curve"],
        )