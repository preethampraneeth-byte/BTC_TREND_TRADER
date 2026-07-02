"""
BTC Trend Trader Professional v4
Dashboard Refresh
"""

from __future__ import annotations

from dashboard.dashboard_controller import DashboardController
from dashboard.widgets.dashboard_renderer import DashboardRenderer


class DashboardRefresh:
    """
    Coordinates dashboard refresh operations.

    Refresh sequence:

        Controller
            ↓
        Renderer
    """

    def __init__(
        self,
        controller: DashboardController,
        renderer: DashboardRenderer,
    ) -> None:

        self.controller = controller
        self.renderer = renderer

    def refresh(self) -> None:
        """
        Refresh dashboard data and render.
        """

        self.controller.refresh()
        self.renderer.render()

    def run(self) -> None:
        """
        Entry point.
        """

        self.refresh()