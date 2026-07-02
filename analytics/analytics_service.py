"""
BTC Trend Trader Professional v4
Analytics Service
"""

from __future__ import annotations

from analytics.analytics_engine import AnalyticsEngine


class AnalyticsService:
    """
    Service responsible for executing
    the Analytics Engine.
    """

    def __init__(self) -> None:

        self.engine = AnalyticsEngine()

    # -------------------------------------------------

    def generate(
        self,
        trades,
    ):

        return self.engine.generate(trades)