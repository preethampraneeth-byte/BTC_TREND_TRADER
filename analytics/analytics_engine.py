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


class AnalyticsEngine:
    """
    Central analytics engine.

    Read-only component responsible for aggregating
    trading analytics from completed trades.
    """

    def __init__(self) -> None:

        self.performance = PerformanceMetrics()
        self.trade_statistics = TradeStatistics()
        self.risk_statistics = RiskStatistics()
        self.equity_curve = EquityCurve()

    def generate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:
        """
        Generate complete analytics snapshot.
        """

        return {
            "performance": self.performance.calculate(trades),
            "trade_statistics": self.trade_statistics.calculate(trades),
            "risk_statistics": self.risk_statistics.calculate(trades),
            "equity_curve": self.equity_curve.calculate(trades),
        }