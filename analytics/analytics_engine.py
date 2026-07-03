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
from analytics.trade_duration import TradeDuration
from analytics.time_analysis import TimeAnalysis
from analytics.weekday_analysis import WeekdayAnalysis

from analytics.analytics_module_registry import (
    AnalyticsModuleRegistry,
)


class AnalyticsEngine:
    """
    Central analytics engine.

    Read-only component responsible for orchestrating
    all analytics modules.
    """

    def __init__(self) -> None:

        self.registry = AnalyticsModuleRegistry()

        #
        # Register analytics modules
        #

        self.registry.register(
            "performance",
            PerformanceMetrics(),
        )

        self.registry.register(
            "trade_statistics",
            TradeStatistics(),
        )

        self.registry.register(
            "risk_statistics",
            RiskStatistics(),
        )

        self.registry.register(
            "equity_curve",
            EquityCurve(),
        )

        self.registry.register(
            "drawdown",
            Drawdown(),
        )

        self.registry.register(
            "streak_analysis",
            StreakAnalysis(),
        )

        self.registry.register(
            "monthly_returns",
            MonthlyReturns(),
        )

        self.registry.register(
            "trade_duration",
            TradeDuration(),
        )

        self.registry.register(
            "time_analysis",
            TimeAnalysis(),
        )

        self.registry.register(
            "weekday_analysis",
            WeekdayAnalysis(),
        )

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

        for name, module in self.registry.modules():

            #
            # Modules requiring starting balance
            #

            if name in (
                "drawdown",
                "monthly_returns",
            ):

                if name == "drawdown":

                    analytics[name] = module.calculate(
                        trades,
                        starting_equity=starting_balance,
                    )

                else:

                    analytics[name] = module.calculate(
                        trades,
                        starting_balance=starting_balance,
                    )

            #
            # Standard analytics modules
            #

            else:

                analytics[name] = module.calculate(
                    trades,
                )

        return analytics