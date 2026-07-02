"""
BTC Trend Trader Professional v4
Dashboard Renderer
"""

from __future__ import annotations

from dashboard.widgets.dashboard_layout import DashboardLayout


class DashboardRenderer:
    """
    Responsible for rendering the dashboard.

    This class contains no business logic and performs
    no data collection.
    """

    def __init__(
        self,
        layout: DashboardLayout,
    ) -> None:

        self.layout = layout

    def render(self) -> None:
        """
        Render the complete dashboard.
        """

        self.layout.render()

    def refresh(self) -> None:
        """
        Alias for render().
        """

        self.render()