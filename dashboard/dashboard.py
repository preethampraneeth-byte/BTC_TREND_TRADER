"""
BTC Trend Trader Professional v4
Dashboard
"""

from __future__ import annotations

from dashboard.widgets.analytics_panel import AnalyticsPanel


class Dashboard:
    """
    Main dashboard.

    Responsible only for rendering data supplied
    by the runtime/services.
    """

    def __init__(self):

        self.analytics_panel = AnalyticsPanel()

    # ---------------------------------------------------------

    def show_complete_dashboard(
        self,
        summary,
        performance,
        trades,
        diagnostics,
        analytics=None,
    ):

        print()

        print("=" * 60)
        print("           BTC TREND TRADER v4 DASHBOARD")
        print("=" * 60)

        #
        # Market Summary
        #

        print("\nMARKET SUMMARY")
        print("-" * 60)

        for key, value in summary.items():
            print(f"{key:<25}: {value}")

        #
        # Diagnostics
        #

        print("\nSTRATEGY DIAGNOSTICS")
        print("-" * 60)

        for key, value in diagnostics.items():
            print(f"{key:<25}: {value}")

        #
        # Performance
        #

        print("\nPERFORMANCE REPORT")
        print("-" * 60)

        for key, value in performance.items():
            print(f"{key:<25}: {value}")

        #
        # Analytics
        #

        if analytics is not None:

            self.analytics_panel.update(
                analytics
            )

            self.analytics_panel.render()

        #
        # Trades
        #

        print("\nRECENT TRADES")
        print("-" * 60)

        for i, trade in enumerate(trades, start=1):

            print(f"\nTrade #{i}")

            #
            # Dictionary trades
            #

            if isinstance(trade, dict):

                for key, value in trade.items():
                    print(f"{key:<20}: {value}")

            #
            # Dataclass/Object trades
            #

            else:

                for key, value in vars(trade).items():
                    print(f"{key:<20}: {value}")

        print()
        print("=" * 60)

    # ---------------------------------------------------------
    # Compatibility methods
    # ---------------------------------------------------------

    def refresh(self):
        """
        Refresh dashboard.

        Placeholder for future GUI refresh.
        """
        pass

    # ---------------------------------------------------------

    def render(self):
        """
        Render dashboard.

        Placeholder for future GUI rendering.
        """
        pass

    # ---------------------------------------------------------

    def run(self):
        """
        Dashboard runtime.

        Placeholder for future GUI runtime.
        """
        self.render()