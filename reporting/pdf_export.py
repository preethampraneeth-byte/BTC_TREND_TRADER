"""
BTC Trend Trader Professional v4
Report Builder

Builds a complete backtest report by combining
all analytics modules.

This class performs NO calculations.
"""

from __future__ import annotations

from analytics.performance_report import PerformanceReport
from analytics.risk_statistics import RiskStatistics
from analytics.trade_duration import TradeDuration
from analytics.monthly_performance import MonthlyPerformance
from analytics.exit_analysis import ExitAnalysis


class ReportBuilder:
    """
    Builds a complete trading report.

    Responsibilities
    ----------------
    - Performance summary
    - Risk statistics
    - Trade duration statistics
    - Monthly performance
    - Exit analysis

    Does NOT:
    - Calculate trading results
    - Execute trades
    - Print reports
    - Export reports
    """

    def build(
        self,
        trades,
        starting_balance,
        ending_balance,
        equity_curve,
    ):
        """
        Build the complete report.
        """

        performance = PerformanceReport().generate(
            trades=trades,
            starting_balance=starting_balance,
            ending_balance=ending_balance,
            equity_curve=equity_curve,
        )

        risk = RiskStatistics().calculate(
            trades
        )

        duration = TradeDuration().calculate(
            trades
        )

        monthly = MonthlyPerformance().calculate(
            trades
        )

        exit_analysis = ExitAnalysis().calculate(
            trades
        )

        return {
            "performance": performance,
            "risk": risk,
            "duration": duration,
            "monthly": monthly,
            "exit_analysis": exit_analysis,
        }