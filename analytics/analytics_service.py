"""
BTC Trend Trader Professional v4
Analytics Service
"""

from __future__ import annotations

from analytics.analytics_engine import AnalyticsEngine
from analytics.analytics_report_builder import AnalyticsReportBuilder


class AnalyticsService:
    """
    Service wrapper around AnalyticsEngine.
    """

    def __init__(self):

        self.engine = AnalyticsEngine()

        self.report_builder = AnalyticsReportBuilder()

    # -------------------------------------------------

    def generate(
        self,
        trades,
        starting_balance: float = 0.0,
    ):

        analytics = self.engine.generate(
            trades,
            starting_balance,
        )

        return self.report_builder.build(
            analytics,
        )