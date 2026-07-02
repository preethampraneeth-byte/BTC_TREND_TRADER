"""
BTC Trend Trader Professional v4
Dashboard Service
"""

from __future__ import annotations

from dashboard.dashboard import Dashboard


class DashboardService:
    """
    Service responsible for rendering the dashboard.
    """

    def __init__(self) -> None:

        self.dashboard = Dashboard()

    # -------------------------------------------------

    def show(
        self,
        summary,
        performance,
        trades,
        diagnostics,
        analytics=None,
    ) -> None:

        self.dashboard.show_complete_dashboard(
            summary=summary,
            performance=performance,
            trades=trades,
            diagnostics=diagnostics,
            analytics=analytics,
        )