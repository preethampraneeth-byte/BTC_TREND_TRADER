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

        report["drawdown"] = analytics.get(
            "drawdown",
            {},
        )

        report["streak_analysis"] = analytics.get(
            "streak_analysis",
            {},
        )

        report["monthly_returns"] = analytics.get(
            "monthly_returns",
            {},
        )

        report["performance"] = analytics.get(
            "performance",
            {},
        )

        report["trade_statistics"] = analytics.get(
            "trade_statistics",
            {},
        )

        report["risk_statistics"] = analytics.get(
            "risk_statistics",
            {},
        )

        report["equity_curve"] = analytics.get(
            "equity_curve",
            {},
        )

        return report