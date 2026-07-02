"""
BTC Trend Trader Professional v4
Dashboard Layout
"""

from __future__ import annotations

from dashboard.widgets.account_panel import AccountPanel
from dashboard.widgets.position_panel import PositionPanel
from dashboard.widgets.order_panel import OrderPanel
from dashboard.widgets.risk_panel import RiskPanel
from dashboard.widgets.history_panel import HistoryPanel
from dashboard.widgets.event_panel import EventPanel
from dashboard.widgets.performance_panel import PerformancePanel
from dashboard.widgets.status_panel import StatusPanel


class DashboardLayout:
    """
    Coordinates rendering of all dashboard panels.

    This class contains no business logic.
    It simply renders each panel in the desired order.
    """

    def __init__(
        self,
        account_panel: AccountPanel,
        position_panel: PositionPanel,
        order_panel: OrderPanel,
        risk_panel: RiskPanel,
        history_panel: HistoryPanel,
        event_panel: EventPanel,
        performance_panel: PerformancePanel,
        status_panel: StatusPanel,
    ) -> None:

        self.account_panel = account_panel
        self.position_panel = position_panel
        self.order_panel = order_panel
        self.risk_panel = risk_panel
        self.history_panel = history_panel
        self.event_panel = event_panel
        self.performance_panel = performance_panel
        self.status_panel = status_panel

    def render(self) -> None:
        """
        Render the complete dashboard.
        """

        print("\n" + "=" * 70)
        print("        BTC TREND TRADER PROFESSIONAL v4")
        print("=" * 70)

        self.account_panel.render()
        self.position_panel.render()
        self.order_panel.render()
        self.risk_panel.render()
        self.history_panel.render()
        self.event_panel.render()
        self.performance_panel.render()
        self.status_panel.render()

        print("\n" + "=" * 70)