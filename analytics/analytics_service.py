"""
BTC Trend Trader Professional v4
Analytics Service
"""

from __future__ import annotations

from analytics.analytics_engine import AnalyticsEngine


class AnalyticsService:
    """
    Service wrapper around AnalyticsEngine.
    """

    def __init__(self):

        self.engine = AnalyticsEngine()

    # -------------------------------------------------

    def generate(
        self,
        trades,
        starting_balance: float = 0.0,
    ):

        return self.engine.generate(
            trades,
            starting_balance,
        )