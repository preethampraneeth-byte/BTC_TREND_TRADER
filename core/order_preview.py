"""
BTC Trend Trader v1.0
Order Preview Module

Displays the trade details before any order is sent.
This module NEVER places a trade.
"""

from __future__ import annotations

import config


class OrderPreview:
    """
    Displays a formatted preview of a trade.
    """

    def show(self, trade: dict) -> None:

        print("\n" + "=" * 50)
        print("        BTC TREND TRADER v1.0")
        print("=" * 50)

        print(f"Symbol       : {config.SYMBOL}")
        print(f"Signal       : {trade['Signal']}")
        print(f"Reason       : {trade['Reason']}")

        print("-" * 50)

        print(f"Entry        : {trade['Entry']}")
        print(f"Stop Loss    : {trade['StopLoss']}")
        print(f"Take Profit  : {trade['TakeProfit']}")

        print("-" * 50)

        print(f"Risk         : {trade['RiskPercent']} %")
        print(f"Reward Ratio : 1 : {trade['RiskReward']}")
        print(f"Lot Size     : {trade.get('LotSize', 0.0)}")

        print("=" * 50)
        print(" PREVIEW ONLY - NO ORDER WILL BE SENT ")
        print("=" * 50)