"""
BTC Trend Trader Professional v4
Analytics Engine
"""

from __future__ import annotations

from typing import Any, Dict, List

from analytics.performance_metrics import PerformanceMetrics
from analytics.trade_statistics import TradeStatistics
from analytics.risk_statistics import RiskStatistics
from analytics.equity_curve import EquityCurve
from analytics.drawdown import Drawdown
from analytics.streak_analysis import StreakAnalysis
from analytics.monthly_returns import MonthlyReturns


class AnalyticsEngine:
    """
    Central analytics engine.

    Read-only component responsible for orchestrating
    all analytics modules.
    """

    def __init__(self) -> None:

        self.performance = PerformanceMetrics()

        self.trade_statistics = TradeStatistics()

        self.risk_statistics = RiskStatistics()

        self.equity_curve = EquityCurve()

        self.drawdown = Drawdown()

        self.streak_analysis = StreakAnalysis()

        self.monthly_returns = MonthlyReturns()

    # -------------------------------------------------

    def generate(
        self,
        trades: List[Any],
        starting_balance: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Generate complete analytics snapshot.
        """

        analytics: Dict[str, Any] = {}

        #
        # Performance
        #

        analytics["performance"] = (
            self.performance.calculate(
                trades,
            )
        )

        #
        # Trade Statistics
        #

        analytics["trade_statistics"] = (
            self.trade_statistics.calculate(
                trades,
            )
        )

        #
        # Risk Statistics
        #

        analytics["risk_statistics"] = (
            self.risk_statistics.calculate(
                trades,
            )
        )

        #
        # Equity Curve
        #

        analytics["equity_curve"] = (
            self.equity_curve.calculate(
                trades,
            )
        )

        #
        # Drawdown
        #

        analytics["drawdown"] = (
            self.drawdown.calculate(
                trades,
                starting_equity=starting_balance,
            )
        )

        #
        # Streak Analysis
        #

        analytics["streak_analysis"] = (
            self.streak_analysis.calculate(
                trades,
            )
        )

        #
        # Monthly Returns
        #

        analytics["monthly_returns"] = (
            self.monthly_returns.calculate(
                trades,
                starting_balance=starting_balance,
            )
        )

        return analytics