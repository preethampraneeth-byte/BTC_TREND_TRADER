"""
BTC Trend Trader Professional v4
Analytics Report Builder
"""

from __future__ import annotations

from typing import Any, Dict


class AnalyticsReportBuilder:
    """
    Builds a complete analytics report from
    analytics modules.
    """

    # -------------------------------------------------

    def build(
        self,
        analytics: Dict[str, Any],
    ) -> Dict[str, Any]:

        report = {}

        #
        # Performance
        #

        report["performance"] = analytics.get(
            "performance",
            {},
        )

        #
        # Trade Statistics
        #

        report["trade_statistics"] = analytics.get(
            "trade_statistics",
            {},
        )

        #
        # Risk Statistics
        #

        report["risk_statistics"] = analytics.get(
            "risk_statistics",
            {},
        )

        #
        # Equity Curve
        #

        report["equity_curve"] = analytics.get(
            "equity_curve",
            {},
        )

        #
        # Drawdown
        #

        report["drawdown"] = analytics.get(
            "drawdown",
            {},
        )

        #
        # Streak Analysis
        #

        report["streak_analysis"] = analytics.get(
            "streak_analysis",
            {},
        )

        #
        # Monthly Returns
        #

        report["monthly_returns"] = analytics.get(
            "monthly_returns",
            {},
        )

        #
        # Trade Duration
        #

        report["trade_duration"] = analytics.get(
            "trade_duration",
            {},
        )

        #
        # Time Analysis
        #

        report["time_analysis"] = analytics.get(
            "time_analysis",
            {},
        )

        #
        # Weekday Analysis
        #

        report["weekday_analysis"] = analytics.get(
            "weekday_analysis",
            {},
        )

        #
        # Risk Metrics
        #

        report["risk_metrics"] = analytics.get(
            "risk_metrics",
            {},
        )

        return report