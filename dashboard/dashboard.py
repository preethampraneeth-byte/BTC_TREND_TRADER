"""
BTC Trend Trader v1.0
Dashboard

Displays backtesting and trading statistics
in a clean console format.
"""

from __future__ import annotations

from typing import List


class Dashboard:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def show_header(self):

        print("\n" + "=" * 60)
        print("           BTC TREND TRADER v1.0 DASHBOARD")
        print("=" * 60)

    # ---------------------------------------------------------

    def show_summary(self, summary: dict):

        print("\nMARKET SUMMARY")
        print("-" * 60)

        for key, value in summary.items():
            print(f"{key:<25}: {value}")

    # ---------------------------------------------------------

    def show_performance(self, performance: dict):

        print("\nPERFORMANCE REPORT")
        print("-" * 60)

        for key, value in performance.items():
            print(f"{key:<25}: {value}")

    # ---------------------------------------------------------

    def show_recent_trades(
        self,
        trades: List,
        limit: int = 10,
    ):

        print("\nRECENT TRADES")
        print("-" * 60)

        if not trades:
            print("No trades available.")
            return

        recent = trades[-limit:]

        for i, trade in enumerate(recent, start=1):

            print(f"\nTrade #{i}")

            print(f"Direction   : {trade.direction}")
            print(f"Entry Time  : {trade.entry_time}")
            print(f"Exit Time   : {trade.exit_time}")

            print(f"Entry Price : {trade.entry_price}")
            print(f"Exit Price  : {trade.exit_price}")

            print(f"Stop Loss   : {trade.stop_loss}")
            print(f"Take Profit : {trade.take_profit}")

            print(f"Lot Size    : {trade.lot_size}")

            print(f"Profit      : {round(trade.profit,2)}")
            print(f"Result      : {trade.result}")

    # ---------------------------------------------------------

    def show_complete_dashboard(
        self,
        summary: dict,
        performance: dict,
        trades: List,
    ):

        self.show_header()

        self.show_summary(summary)

        self.show_performance(performance)

        self.show_recent_trades(trades)

        print("\n" + "=" * 60)