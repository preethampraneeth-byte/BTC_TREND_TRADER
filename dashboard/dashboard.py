"""
BTC Trend Trader Professional v4
Dashboard
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from dashboard.dashboard_controller import DashboardController

from dashboard.widgets.account_panel import AccountPanel
from dashboard.widgets.position_panel import PositionPanel
from dashboard.widgets.order_panel import OrderPanel
from dashboard.widgets.risk_panel import RiskPanel
from dashboard.widgets.history_panel import HistoryPanel
from dashboard.widgets.event_panel import EventPanel
from dashboard.widgets.performance_panel import PerformancePanel
from dashboard.widgets.status_panel import StatusPanel
from dashboard.widgets.dashboard_layout import DashboardLayout


class Dashboard:
    """
    Professional console dashboard.

    Backward compatible with Dashboard v1.
    """

    def __init__(
        self,
        controller: Optional[DashboardController] = None,
    ) -> None:

        self.controller = controller or DashboardController()

        self.account_panel = AccountPanel()
        self.position_panel = PositionPanel()
        self.order_panel = OrderPanel()
        self.risk_panel = RiskPanel()
        self.history_panel = HistoryPanel()
        self.event_panel = EventPanel()
        self.performance_panel = PerformancePanel()
        self.status_panel = StatusPanel()

        self.layout = DashboardLayout(
            self.account_panel,
            self.position_panel,
            self.order_panel,
            self.risk_panel,
            self.history_panel,
            self.event_panel,
            self.performance_panel,
            self.status_panel,
        )

    # ---------------------------------------------------------

    def refresh(self) -> None:

        self.controller.refresh()

        self.account_panel.update(
            self.controller.get_account()
        )

        self.position_panel.update(
            self.controller.get_positions()
        )

        self.order_panel.update(
            self.controller.get_orders()
        )

        self.risk_panel.update(
            self.controller.get_risk()
        )

        self.history_panel.update(
            self.controller.get_history()
        )

        self.event_panel.update(
            self.controller.get_events()
        )

        self.performance_panel.update(
            self.controller.get_statistics()
        )

        self.status_panel.update(
            {
                "Controller": "Online",
                "Dashboard": "Ready",
            }
        )

    # ---------------------------------------------------------

    def render(self) -> None:

        self.refresh()
        self.layout.render()

    # ---------------------------------------------------------

    def run(self) -> None:

        self.render()

    # =========================================================
    #
    # Legacy Dashboard API (Backward Compatibility)
    #
    # =========================================================

    def show_header(self):

        print("\n" + "=" * 60)
        print("           BTC TREND TRADER v4 DASHBOARD")
        print("=" * 60)

    # ---------------------------------------------------------

    def show_summary(
        self,
        summary: Dict[str, Any],
    ):

        print("\nMARKET SUMMARY")
        print("-" * 60)

        for key, value in summary.items():
            print(f"{key:<25}: {value}")

    # ---------------------------------------------------------

    def show_diagnostics(
        self,
        diagnostics: Dict[str, Any],
    ):

        print("\nSTRATEGY DIAGNOSTICS")
        print("-" * 60)

        for key, value in diagnostics.items():
            print(f"{key:<25}: {value}")

    # ---------------------------------------------------------

    def show_performance(
        self,
        performance: Dict[str, Any],
    ):

        print("\nPERFORMANCE REPORT")
        print("-" * 60)

        for key, value in performance.items():
            print(f"{key:<25}: {value}")

    # ---------------------------------------------------------

    def show_recent_trades(
        self,
        trades: List[Any],
        limit: int = 10,
    ):

        print("\nRECENT TRADES")
        print("-" * 60)

        if not trades:
            print("No trades available.")
            return

        for i, trade in enumerate(trades[-limit:], start=1):

            print(f"\nTrade #{i}")

            for attribute in (
                "direction",
                "entry_time",
                "exit_time",
                "entry_price",
                "exit_price",
                "stop_loss",
                "take_profit",
                "lot_size",
                "profit",
                "result",
            ):

                if hasattr(trade, attribute):
                    print(
                        f"{attribute.replace('_', ' ').title():<15}: "
                        f"{getattr(trade, attribute)}"
                    )

    # ---------------------------------------------------------

    def show_complete_dashboard(
        self,
        summary: Dict[str, Any],
        performance: Dict[str, Any],
        trades: List[Any],
        diagnostics: Optional[Dict[str, Any]] = None,
    ):

        self.show_header()

        self.show_summary(summary)

        if diagnostics:
            self.show_diagnostics(diagnostics)

        self.show_performance(performance)

        self.show_recent_trades(trades)

        print("\n" + "=" * 60)